"""Shared RAG pipeline: plan the query, retrieve, rerank and answer.

One implementation used by both the terminal chat (app/rag_chat.py) and the
HTTP API (app/api.py). The result is a plain data object: the callers decide
how to present it.
"""

import json
import logging
import sys
import time
from contextlib import contextmanager
from typing import Callable
from uuid import uuid4

from langchain.chat_models import init_chat_model
from langchain_core.callbacks import UsageMetadataCallbackHandler
from langchain_core.documents import Document
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from app.config import settings
from app.query_planner import (
    QueryPlan,
    build_filters,
    build_planner_prompt,
    build_search_query,
    ensure_planner_covers_index,
    search_chunks,
)
from app.rerank import (
    RERANK_TOP_N,
    RerankResult,
    build_rerank_prompt,
    select_documents_by_ids,
    select_reranked_documents,
)
from app.retrieve import connect_store, ensure_collection_ready

GEMINI_HTTP_OPTIONS = {
    "api_version": "v1beta"
} 

PREVIEW_LIMIT = 300
NO_ANSWER_MESSAGE = (
    "Não encontrei informação suficiente na base de conhecimento "
    "para responder com segurança."
)
FALLBACK_CLARIFICATION = "Pode detalhar melhor a sua pergunta?"

SYSTEM_PROMPT = (
    "You are a support assistant for FCAI. "
    "Answer the user's question using ONLY the context below. "
    "Do not use prior knowledge and do not invent information or sources.\n\n"
    "Rules:\n"
    "- Write 'answer' in Portuguese, objective and clear.\n"
    "- Set 'has_answer' to true only if the context supports the answer.\n"
    "- 'used_chunk_ids' must contain only Chunk IDs present in the context.\n"
    f"- If the context is not enough, set 'has_answer' to false, set 'answer' to "
    f"'{NO_ANSWER_MESSAGE}' and leave 'used_chunk_ids' empty.\n\n"
    "Context:\n{context}"
)

ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_PROMPT), ("human", "{question}")]
)

PromptCallback = Callable[[str, PromptValue], None]

# One JSON line per pipeline run on stdout: counts, timings and file names only —
# never prompts, chunks, answers or credentials.
logger = logging.getLogger("rag.pipeline")
logger.setLevel(logging.INFO)
logger.propagate = False
if not logger.handlers:
    logger.addHandler(logging.StreamHandler(sys.stdout))


def _elapsed_ms(started: float) -> float:
    return round((time.perf_counter() - started) * 1000, 1)


def _log_run(record: dict) -> None:
    logger.info(json.dumps(record, ensure_ascii=False))


@contextmanager
def _timed(timings: "PipelineTimings", field: str):
    started = time.perf_counter()
    try:
        yield
    finally:
        setattr(timings, field, _elapsed_ms(started))


class RagAnswer(BaseModel):
    answer: str = Field(description="Answer in Portuguese, based only on the context.")
    has_answer: bool = Field(description="True only if the context supports the answer.")
    used_chunk_ids: list[str] = Field(
        description="Chunk IDs from the context that support the answer."
    )


class Source(BaseModel):
    source_file: str | None = None
    title: str | None = None
    section: str | None = None
    version: str | None = None


class RetrievalChunkDebug(Source):
    rank: int
    score: float
    chunk_id: str | None = None
    preview: str


class QueryPlanDebug(QueryPlan):
    search_query: str
    filters: dict


class PipelineTimings(BaseModel):
    query_planning_ms: float | None = None
    retrieval_ms: float | None = None
    reranking_ms: float | None = None
    answer_generation_ms: float | None = None
    total_ms: float | None = None


class ModelUsage(BaseModel):
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int


class RagDebug(BaseModel):
    request_id: str
    query_plan: QueryPlanDebug
    retrieved_chunks: list[RetrievalChunkDebug] = Field(default_factory=list)
    selected_chunk_ids: list[str] = Field(default_factory=list)
    timings: PipelineTimings = Field(default_factory=PipelineTimings)
    model_usage: list[ModelUsage] = Field(default_factory=list)


class RagPipelineResult(BaseModel):
    answer: str
    has_answer: bool
    needs_clarification: bool
    sources: list[Source]
    debug: RagDebug | None = None


def format_context(documents: list[Document]) -> str:
    # The chunk text already carries title, section, plan and version (context header
    # added at ingestion). The model only needs the id it must cite back.
    blocks = [
        f"[Chunk ID: {document.metadata.get('chunk_id')}]\nContent:\n{document.page_content}"
        for document in documents
    ]
    return "\n\n".join(blocks)


def build_query_plan_debug(query_plan: QueryPlan, filters: dict) -> QueryPlanDebug:
    return QueryPlanDebug(
        **query_plan.model_dump(),
        search_query=build_search_query(query_plan),
        filters=filters,
    )


def build_retrieval_debug(
    results: list[tuple[Document, float]],
) -> list[RetrievalChunkDebug]:
    # model_validate picks the declared fields out of the chunk metadata and
    # ignores the rest.
    return [
        RetrievalChunkDebug.model_validate(
            {
                **document.metadata,
                "rank": rank,
                "score": score,
                "preview": document.page_content[:PREVIEW_LIMIT],
            }
        )
        for rank, (document, score) in enumerate(results, start=1)
    ]


def build_model_usage(usage_metadata: dict) -> list[ModelUsage]:
    # usage_metadata comes straight from LangChain's UsageMetadataCallbackHandler,
    # aggregated per model across every call of the run.
    return [
        ModelUsage.model_validate({"model": model, **usage})
        for model, usage in usage_metadata.items()
    ]


def build_sources(documents: list[Document], used_chunk_ids: list[str]) -> list[Source]:
    # Sources come from the application, never from the model: only chunk ids that
    # were really in the context are kept, joined back with their own metadata.
    return [
        Source.model_validate(document.metadata)
        for document in select_documents_by_ids(documents, used_chunk_ids)
    ]


class RagPipeline:
    def __init__(self) -> None:
        ensure_collection_ready()
        ensure_planner_covers_index()
        self.store = connect_store()

        # temperature=0: the planner is a classifier, and the same question must always
        # produce the same plan. With the default temperature it flip-flopped between
        # asking for clarification and guessing.
        model = init_chat_model(
            "gemini-2.5-flash",
            model_provider="google_genai",
            api_key=settings.openai_api_key,
            temperature=0,
        )
        self.planner = model.with_structured_output(QueryPlan)
        self.reranker = model.with_structured_output(RerankResult)
        self.answerer = model.with_structured_output(RagAnswer)

    def run(
        self,
        question: str,
        use_rerank: bool = True,
        include_debug: bool = False,
        on_prompt: PromptCallback | None = None,
    ) -> RagPipelineResult:
        request_id = str(uuid4())
        timings = PipelineTimings()
        usage = UsageMetadataCallbackHandler()

        config = {"callbacks": [usage]}

        try:
            with _timed(timings, "total_ms"):
                result = self._execute(
                    question, use_rerank, request_id, timings, config, on_prompt
                )
        except Exception as exc:
            _log_run(
                {
                    "request_id": request_id,
                    "used_rerank": use_rerank,
                    "timings": timings.model_dump(),
                    "model_usage": [
                        entry.model_dump()
                        for entry in build_model_usage(usage.usage_metadata)
                    ],
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                }
            )
            raise

        debug = result.debug
        debug.model_usage = build_model_usage(usage.usage_metadata)
        _log_run(
            {
                "request_id": request_id,
                "has_answer": result.has_answer,
                "needs_clarification": result.needs_clarification,
                "used_rerank": use_rerank,
                "retrieved_chunks_count": len(debug.retrieved_chunks),
                "selected_chunks_count": len(debug.selected_chunk_ids),
                "source_files": [source.source_file for source in result.sources],
                "timings": timings.model_dump(),
                "model_usage": [entry.model_dump() for entry in debug.model_usage],
            }
        )

        # The debug payload is always built (the log above needs it) and only
        # stripped from the result when the caller did not ask for it.
        if not include_debug:
            result.debug = None
        return result


    def _execute(
        self,
        question: str,
        use_rerank: bool,
        request_id: str,
        timings: PipelineTimings,
        config: dict,
        on_prompt: PromptCallback | None,
    ) -> RagPipelineResult:
        planner_prompt = build_planner_prompt(question)
        if on_prompt:
            on_prompt("Query planner prompt", planner_prompt)

        with _timed(timings, "query_planning_ms"):
            query_plan = self.planner.invoke(planner_prompt, config=config)

        filters = build_filters(query_plan)
        debug = RagDebug(
            request_id=request_id,
            query_plan=build_query_plan_debug(query_plan, filters),
            timings=timings,
        )

        if query_plan.needs_clarification:
            return RagPipelineResult(
                answer=query_plan.clarification_question or FALLBACK_CLARIFICATION,
                has_answer=False,
                needs_clarification=True,
                sources=[],
                debug=debug,
            )

        with _timed(timings, "retrieval_ms"):
            results = search_chunks(self.store, query_plan, filters)
        debug.retrieved_chunks = build_retrieval_debug(results)

        if not results:
            return self._no_answer(debug)

        if use_rerank:
            rerank_prompt = build_rerank_prompt(results, question, query_plan)
            if on_prompt:
                on_prompt("Reranker prompt", rerank_prompt)

            with _timed(timings, "reranking_ms"):
                rerank_result = self.reranker.invoke(rerank_prompt, config=config)
            documents = select_reranked_documents(
                results, rerank_result.selected_chunk_ids
            )
        else:
            documents = [document for document, _ in results[:RERANK_TOP_N]]

        debug.selected_chunk_ids = [
            document.metadata.get("chunk_id") for document in documents
        ]

        if not documents:
            return self._no_answer(debug)

        answer_prompt = ANSWER_PROMPT.invoke(
            {"context": format_context(documents), "question": question}
        )
        if on_prompt:
            on_prompt("Final answer prompt", answer_prompt)

        with _timed(timings, "answer_generation_ms"):
            response = self.answerer.invoke(answer_prompt, config=config)

        sources = (
            build_sources(documents, response.used_chunk_ids)
            if response.has_answer
            else []
        )
        return RagPipelineResult(
            answer=response.answer,
            has_answer=response.has_answer,
            needs_clarification=False,
            sources=sources,
            debug=debug,
        )

    def _no_answer(self, debug: RagDebug) -> RagPipelineResult:
        return RagPipelineResult(
            answer=NO_ANSWER_MESSAGE,
            has_answer=False,
            needs_clarification=False,
            sources=[],
            debug=debug,
        )
