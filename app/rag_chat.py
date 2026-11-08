"""RAG chat in the terminal, on top of the shared pipeline.

The pipeline (planning, retrieval, reranking, answer, sources) lives in
app/rag_pipeline.py. This file only owns the conversation loop and printing.
"""

import argparse

from langchain_core.prompt_values import PromptValue

from app.rag_pipeline import (
    QueryPlanDebug,
    RagDebug,
    RagPipeline,
    RetrievalChunkDebug,
    Source,
)
from app.retrieve import format_filters


def print_prompt(label: str, prompt_value: PromptValue) -> None:
    print(f"\n--- {label} ---")
    for message in prompt_value.to_messages():
        print(f"\n[{message.type}]")
        print(message.text)
    print(f"\n--- End of {label.lower()} ---")


def print_query_plan(plan: QueryPlanDebug) -> None:
    print("\n--- Query plan ---")
    print(f"Normalized question: {plan.normalized_question}")
    print(f"Doc types: {', '.join(plan.doc_types) or None}")
    print(f"Plan: {plan.plan}")
    print(f"Exact terms: {', '.join(plan.exact_terms) or None}")
    print(f"Needs clarification: {plan.needs_clarification}")
    print(f"Search query: {plan.search_query}")
    print(f"Filters: {format_filters(plan.filters)}")
    print("--- End of query plan ---")


def print_retrieved_chunks(chunks: list[RetrievalChunkDebug]) -> None:
    print("\n--- Retrieved chunks ---\n")
    if not chunks:
        print("No chunks retrieved.")
    for chunk in chunks:
        print(f"{chunk.rank}. Score: {chunk.score:.2f}")
        print(f"   Chunk ID: {chunk.chunk_id}")
        print(f"   Source: {chunk.source_file}")
        print(f"   Title: {chunk.title}")
        if chunk.section:
            print(f"   Section: {chunk.section}")
        print(f"   Version: {chunk.version}")
        print("   Preview:")
        for line in chunk.preview.splitlines():
            print(f"     {line}")
        print()
    print("--- End of retrieved chunks ---")


def print_selected_chunks(selected_chunk_ids: list[str]) -> None:
    print("\n--- Selected chunks ---")
    print(f"Selected chunks: {', '.join(selected_chunk_ids) or None}")
    print(f"Selected count: {len(selected_chunk_ids)}")
    print("--- End of selected chunks ---")


def format_ms(value: float | None) -> str:
    return f"{value} ms" if value is not None else "-"


def print_pipeline_debug(debug: RagDebug) -> None:
    timings = debug.timings
    print("\n--- Pipeline debug ---")
    print(f"Request ID: {debug.request_id}")
    print("Timings:")
    print(f"  Query planning: {format_ms(timings.query_planning_ms)}")
    print(f"  Retrieval: {format_ms(timings.retrieval_ms)}")
    print(f"  Reranking: {format_ms(timings.reranking_ms)}")
    print(f"  Answer generation: {format_ms(timings.answer_generation_ms)}")
    print(f"  Total: {format_ms(timings.total_ms)}")
    if debug.model_usage:
        print("Model usage:")
        for usage in debug.model_usage:
            print(
                f"  {usage.model}: {usage.input_tokens} input + "
                f"{usage.output_tokens} output = {usage.total_tokens} tokens"
            )
    print("--- End of pipeline debug ---")


def print_debug(debug: RagDebug) -> None:
    print_query_plan(debug.query_plan)
    if not debug.query_plan.needs_clarification:
        print_retrieved_chunks(debug.retrieved_chunks)
        if debug.retrieved_chunks:
            print_selected_chunks(debug.selected_chunk_ids)
    print_pipeline_debug(debug)


def print_sources(sources: list[Source]) -> None:
    print("\nSources:")
    if not sources:
        print("No sources.")
        return

    for rank, source in enumerate(sources, start=1):
        print(f"{rank}. {source.source_file}")
        print(f"   Title: {source.title}")
        if source.section:
            print(f"   Section: {source.section}")
        print(f"   Version: {source.version}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="RAG chat.")
    parser.add_argument("--show-prompt", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--no-rerank", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pipeline = RagPipeline()

    print("RAG chat started.")
    print("This chat uses the internal knowledge base.")
    print("Type 'exit' to quit.")

    while True:
        question = input("\n> ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue

        result = pipeline.run(
            question,
            use_rerank=not args.no_rerank,
            include_debug=args.debug,
            on_prompt=print_prompt if args.show_prompt else None,
        )

        if result.debug:
            print_debug(result.debug)

        print("\nAnswer:")
        print(result.answer)

        if not result.needs_clarification:
            print_sources(result.sources)


if __name__ == "__main__":
    main()
