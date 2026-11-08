"""Reranking: the model picks which retrieved chunks deserve the final prompt.

Retrieval optimizes recall (bring every candidate that might help); this step
optimizes precision (keep only the chunks that actually answer the question).
"""

from langchain_core.documents import Document
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from app.query_planner import QueryPlan

RERANK_TOP_N = 4

RERANK_SYSTEM_PROMPT = (
    "You rerank retrieved chunks for a RAG assistant. You never answer the "
    "question.\n\n"
    "Analyze only the candidate chunks below and select the ones worth sending to "
    "the answer model.\n\n"
    "Rules:\n"
    f"- Select at most {RERANK_TOP_N} chunk_ids, best first.\n"
    "- Choose only chunks that directly help answer the question.\n"
    "- Prefer specific chunks over generic ones.\n"
    "- Prefer chunks that contain the exact terms, when given.\n"
    "- Return an empty list if no chunk supports the answer.\n"
    "- Use only Chunk IDs present in the candidates.\n\n"
    "Candidates:\n{candidates}"
)

RERANK_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", RERANK_SYSTEM_PROMPT),
        (
            "human",
            "Question: {question}\n"
            "Normalized question: {normalized_question}\n"
            "Exact terms: {exact_terms}",
        ),
    ]
)


class RerankResult(BaseModel):
    selected_chunk_ids: list[str] = Field(
        description="Chunk IDs that directly help answer the question, best first. "
        "Empty when no candidate supports the answer."
    )


def format_rerank_candidates(results: list[tuple[Document, float]]) -> str:
    blocks = []
    for document, _ in results:
        metadata = document.metadata
        lines = [
            f"[Chunk ID: {metadata.get('chunk_id')}]",
            f"Source: {metadata.get('source_file')}",
            f"Title: {metadata.get('title')}",
        ]
        if metadata.get("section"):
            lines.append(f"Section: {metadata['section']}")
        lines.append(f"Version: {metadata.get('version')}")
        lines.append(f"Content:\n{document.page_content}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def build_rerank_prompt(
    results: list[tuple[Document, float]], question: str, query_plan: QueryPlan
) -> PromptValue:
    return RERANK_PROMPT.invoke(
        {
            "candidates": format_rerank_candidates(results),
            "question": question,
            "normalized_question": query_plan.normalized_question,
            "exact_terms": ", ".join(query_plan.exact_terms) or "none",
        }
    )


def select_documents_by_ids(
    documents: list[Document], chunk_ids: list[str]
) -> list[Document]:
    documents_by_id = {
        document.metadata.get("chunk_id"): document for document in documents
    }
    selected = []
    for chunk_id in chunk_ids:
        document = documents_by_id.get(chunk_id)
        if document is not None and document not in selected:
            selected.append(document)
    return selected


def select_reranked_documents(
    results: list[tuple[Document, float]], selected_chunk_ids: list[str]
) -> list[Document]:
    documents = [document for document, _ in results]
    return select_documents_by_ids(documents, selected_chunk_ids)[:RERANK_TOP_N]
