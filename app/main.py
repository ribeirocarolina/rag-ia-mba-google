from app.config import settings
from app.db import enable_vector_extension, test_connection


def main() -> None:
    assert settings.database_url
    print("Environment loaded.")

    test_connection()
    print("Database connection ok.")

    enable_vector_extension()
    print("pgvector extension enabled.")

    print("Project setup completed.")


if __name__ == "__main__":
    main()
