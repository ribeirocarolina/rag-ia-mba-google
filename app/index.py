import argparse
import asyncio
import json
import re
import sys
import time
from pathlib import Path

from langchain_core.documents import Document
from langchain_postgres import PGEngine, PGVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import settings
from app.db import enable_vector_extension, get_connection
from app.ingest import OUTPUT_PATH as CHUNKS_PATH
from app.manifest import MANIFEST_PATH, load_manifest, save_manifest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TABLE_NAME = "fcai_knowledge_base"
ID_COLUMN = {"name": "chunk_id", "data_type": "TEXT", "nullable": False}

# Limites conservadores para a cota gratuita do Gemini.
# Com 10 documentos por lote e 10 segundos entre lotes, o pipeline
# evita disparar mais de aproximadamente 60 documentos por minuto.
EMBEDDING_BATCH_SIZE = 10
EMBEDDING_BATCH_DELAY_SECONDS = 10
MAX_EMBEDDING_RETRIES = 5


if sys.platform == "win32":
    # Psycopg async precisa de SelectorEventLoop no Windows.
    # Esta política está deprecated em versões recentes do Python,
    # mas ainda é necessária para este caminho de compatibilidade.
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class IndexingError(Exception):
    pass


def load_chunks() -> list[Document]:
    if not CHUNKS_PATH.exists():
        raise IndexingError(f"chunks file not found: {CHUNKS_PATH}")

    documents: list[Document] = []
    with CHUNKS_PATH.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise IndexingError(f"line {number}: invalid JSON ({exc})") from exc

            content = record.get("content")
            metadata = record.get("metadata") or {}
            if not content:
                raise IndexingError(f"line {number}: missing content")

            for field in ("chunk_id", "source_file", "document_hash"):
                if not metadata.get(field):
                    raise IndexingError(f"line {number}: missing metadata.{field}")

            documents.append(Document(page_content=content, metadata=metadata))

    if not documents:
        raise IndexingError(f"no chunks found in {CHUNKS_PATH}")

    return documents


def group_by_source(documents: list[Document]) -> dict[str, list[Document]]:
    grouped: dict[str, list[Document]] = {}
    for document in documents:
        grouped.setdefault(document.metadata["source_file"], []).append(document)
    return grouped


def classify_sources(
    grouped: dict[str, list[Document]], indexed_sources: dict
) -> dict[str, list[str]]:
    changes: dict[str, list[str]] = {
        "new": [],
        "changed": [],
        "unchanged": [],
        "removed": [],
    }

    for source, documents in grouped.items():
        previous = indexed_sources.get(source)
        if previous is None:
            changes["new"].append(source)
        elif previous["document_hash"] != documents[0].metadata["document_hash"]:
            changes["changed"].append(source)
        else:
            changes["unchanged"].append(source)

    changes["removed"] = [
        source for source in indexed_sources if source not in grouped
    ]
    return changes


def table_exists() -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT to_regclass(%s)", (f"public.{TABLE_NAME}",)
        ).fetchone()
    return row[0] is not None


def connect_store(
    embeddings: GoogleGenerativeAIEmbeddings, create_table: bool
) -> PGVectorStore:
    engine = PGEngine.from_connection_string(url=settings.database_url)

    if create_table:
        # Uma chamada simples para descobrir a dimensão dos vetores.
        vector_size = len(embeddings.embed_query("dimension probe"))
        engine.init_vectorstore_table(
            table_name=TABLE_NAME,
            vector_size=vector_size,
            id_column=ID_COLUMN,
            overwrite_existing=True,
        )

    return PGVectorStore.create_sync(
        engine=engine,
        embedding_service=embeddings,
        table_name=TABLE_NAME,
        id_column=ID_COLUMN["name"],
    )


def manifest_entry(documents: list[Document]) -> dict:
    metadata = documents[0].metadata
    return {
        "document_hash": metadata["document_hash"],
        "title": metadata.get("title"),
        "tenant": metadata.get("tenant"),
        "product": metadata.get("product"),
        "version": metadata.get("version"),
        "status": metadata.get("status"),
        "chunk_ids": [document.metadata["chunk_id"] for document in documents],
    }


def retry_delay_seconds(error: Exception, attempt: int) -> float:
    """Obtém o tempo sugerido pelo Gemini ou usa backoff exponencial."""
    message = str(error)

    patterns = (
        r"retry in\s+([\d.]+)\s*s",
        r"retryDelay['\"]?\s*:\s*['\"]?([\d.]+)\s*s",
    )
    for pattern in patterns:
        match = re.search(pattern, message, flags=re.IGNORECASE)
        if match:
            return float(match.group(1)) + 2

    return min(60 * (2 ** attempt), 300)


def add_documents_with_retry(
    store: PGVectorStore,
    documents: list[Document],
) -> None:
    ids = [document.metadata["chunk_id"] for document in documents]

    for attempt in range(MAX_EMBEDDING_RETRIES + 1):
        try:
            store.add_documents(documents, ids=ids)
            return
        except Exception as exc:
            message = str(exc).upper()
            is_rate_limit = (
                "429" in message
                or "RESOURCE_EXHAUSTED" in message
                or "TOO MANY REQUESTS" in message
            )

            if not is_rate_limit or attempt >= MAX_EMBEDDING_RETRIES:
                raise

            delay = retry_delay_seconds(exc, attempt)
            print(
                f"Limite de requisições do Gemini atingido. "
                f"Tentativa {attempt + 1}/{MAX_EMBEDDING_RETRIES}. "
                f"Aguardando {delay:.0f} segundos..."
            )
            time.sleep(delay)


def index_in_batches(
    store: PGVectorStore,
    documents: list[Document],
) -> None:
    total = len(documents)
    batches = [
        documents[i : i + EMBEDDING_BATCH_SIZE]
        for i in range(0, total, EMBEDDING_BATCH_SIZE)
    ]

    for batch_number, batch in enumerate(batches, start=1):
        print(
            f"Indexando lote {batch_number}/{len(batches)} "
            f"({len(batch)} chunks)..."
        )
        add_documents_with_retry(store, batch)

        if batch_number < len(batches):
            time.sleep(EMBEDDING_BATCH_DELAY_SECONDS)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Index chunks into pgvector, reindexing only what changed."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="delete every indexed chunk and reindex all current chunks",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print(f"Loading chunks from {CHUNKS_PATH.relative_to(PROJECT_ROOT)}...")
    try:
        documents = load_chunks()
    except IndexingError as exc:
        print(f"Indexing failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    grouped = group_by_source(documents)
    print(f"Loaded chunks: {len(documents)}")
    print(f"Sources in chunks: {len(grouped)}")

    print("Connecting to Postgres...")
    enable_vector_extension()

    indexed_sources = load_manifest().get("sources", {})

    # Sem manifesto ou sem tabela, o estado do índice é desconhecido.
    # Nesse caso, recria a tabela para evitar inconsistências.
    rebuild = not indexed_sources or not table_exists()
    if rebuild:
        indexed_sources = {}

    changes = classify_sources(grouped, indexed_sources)
    print(f"New sources: {len(changes['new'])}")
    print(f"Changed sources: {len(changes['changed'])}")
    print(f"Removed sources: {len(changes['removed'])}")
    print(f"Unchanged sources: {len(changes['unchanged'])}")

    if args.force:
        delete_ids = [
            chunk_id
            for entry in indexed_sources.values()
            for chunk_id in entry["chunk_ids"]
        ]
        sources_to_index = list(grouped)
    else:
        delete_ids = [
            chunk_id
            for source in changes["removed"] + changes["changed"]
            for chunk_id in indexed_sources[source]["chunk_ids"]
        ]
        sources_to_index = changes["new"] + changes["changed"]

    documents_to_index = [
        document for source in sources_to_index for document in grouped[source]
    ]

    embeddings = GoogleGenerativeAIEmbeddings(
        model=settings.openai_embedding_model,
        api_key=settings.openai_api_key,
    )
    store = connect_store(embeddings, create_table=rebuild)

    # Remove também IDs atuais que possam ter sido parcialmente gravados
    # por uma execução anterior que falhou antes de salvar o manifesto.
    target_ids = [
        document.metadata["chunk_id"] for document in documents_to_index
    ]
    ids_to_delete = list(dict.fromkeys(delete_ids + target_ids))

    if ids_to_delete:
        store.delete(ids=ids_to_delete)

    if documents_to_index:
        index_in_batches(store, documents_to_index)

    # O manifesto só é atualizado depois que todos os lotes terminarem.
    save_manifest(
        {source: manifest_entry(docs) for source, docs in grouped.items()}
    )

    print(f"Deleted chunks: {len(ids_to_delete)}")
    print(f"Indexed chunks: {len(documents_to_index)}")
    print(f"Manifest saved to {MANIFEST_PATH.relative_to(PROJECT_ROOT)}")
    print("Indexing completed.")


if __name__ == "__main__":
    main()
