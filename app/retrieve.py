import argparse
import sys

import psycopg
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGEngine, PGVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings


from app.config import settings
from app.db import get_connection
from app.index import ID_COLUMN, TABLE_NAME

DEFAULT_TOP_K = 30
FILTER_FIELDS = ["tenant", "product", "plan", "doc_type", "status"]
PREVIEW_LIMIT = 500


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Isolated retrieval test.")
    parser.add_argument("query", nargs="?")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--tenant")
    parser.add_argument("--product")
    parser.add_argument("--plan")
    parser.add_argument("--doc-type")
    parser.add_argument("--status")
    return parser.parse_args()


def ensure_collection_ready() -> None:
    try:
        with get_connection() as conn:
            count = conn.execute(f"SELECT count(*) FROM {TABLE_NAME}").fetchone()[0]
    except psycopg.errors.UndefinedTable:
        count = 0

    if not count:
        print(
            f"Collection '{TABLE_NAME}' is missing or empty. "
            "Run 'python -m app.ingest' and then 'python -m app.index' first.",
            file=sys.stderr,
        )
        raise SystemExit(1)


def connect_store() -> PGVectorStore:
    embeddings = GoogleGenerativeAIEmbeddings(
        model=settings.openai_embedding_model,
        api_key=settings.openai_api_key,
    )
    engine = PGEngine.from_connection_string(url=settings.database_url)
    return PGVectorStore.create_sync(
        engine=engine,
        embedding_service=embeddings,
        table_name=TABLE_NAME,
        id_column=ID_COLUMN["name"],
    )


def format_filters(filters: dict) -> str:
    if not filters:
        return "none"
    parts = []
    for key, value in filters.items():
        if isinstance(value, dict):
            value = " or ".join(value["$in"])
        parts.append(f"{key}={value}")
    return ", ".join(parts)


def print_chunk(
    rank: int, document: Document, score: float, preview_limit: int = PREVIEW_LIMIT
) -> None:
    metadata = document.metadata
    print(f"{rank}. Score: {score:.2f}")
    print(f"   Chunk ID: {metadata.get('chunk_id')}")
    print(f"   Source: {metadata.get('source_file')}")
    print(f"   Title: {metadata.get('title')}")
    if metadata.get("section"):
        print(f"   Section: {metadata['section']}")
    print(f"   Plan: {metadata.get('plan')}")
    print(f"   Type: {metadata.get('doc_type')}")
    print(f"   Version: {metadata.get('version')}")
    print(f"   Status: {metadata.get('status')}")
    print("   Preview:")
    for line in document.page_content[:preview_limit].splitlines():
        print(f"     {line}")
    print()


def main() -> None:
    args = parse_args()
    query = args.query or input("Question: ").strip()
    if not query:
        print("No question provided.", file=sys.stderr)
        raise SystemExit(1)

    filters = {
        field: getattr(args, field)
        for field in FILTER_FIELDS
        if getattr(args, field)
    }

    ensure_collection_ready()
    store = connect_store()
    results = store.similarity_search_with_score(
        query, k=args.top_k, filter=filters or None
    )

    print("Retrieval test started.")
    print(f"Query: {query}")
    print(f"Top K: {args.top_k}")
    print(f"Filters: {format_filters(filters)}")
    print(f"Total results: {len(results)}")
    print()

    if not results:
        print("No results found for this query and filters.")
        return

    print("Results:")
    print()
    for rank, (document, score) in enumerate(results, start=1):
        print_chunk(rank, document, score)


if __name__ == "__main__":
    main()
