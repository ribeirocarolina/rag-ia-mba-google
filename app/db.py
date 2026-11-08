import psycopg

from app.config import settings


def get_connection() -> psycopg.Connection:
    return psycopg.connect(settings.psycopg_dsn)


def test_connection() -> None:
    with get_connection() as conn:
        conn.execute("SELECT 1")


def enable_vector_extension() -> None:
    with get_connection() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.commit()
