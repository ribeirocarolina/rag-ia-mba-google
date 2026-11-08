import sys
from pathlib import Path

from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

from app.config import settings

KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parent.parent / "knowledge_base"
DEFAULT_DOCUMENT = "product-support-sla.md"

INSTRUCTION = (
    "You are a support assistant for FCAI. "
    "Answer the user's question using ONLY the document provided below. "
    "Do not use prior knowledge and do not invent information. "
    "If the document does not contain enough information to answer, say clearly "
    "that the document does not have enough information. "
    "Always answer in Portuguese."
)


def load_document(name: str) -> str:
    path = KNOWLEDGE_BASE_DIR / name
    return path.read_text(encoding="utf-8")


def main() -> None:
    document_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DOCUMENT
    document = load_document(document_name)

    model = init_chat_model(
        settings.openai_chat_model,
        model_provider="openai",
        api_key=settings.openai_api_key,
    )

    system_message = SystemMessage(f"{INSTRUCTION}\n\nDocument:\n{document}")

    print("Full-document context chat started.")
    print("This chat uses one full Markdown document as context.")
    print(f"Loaded document: {document_name}")
    print("This is not RAG yet.")
    print("Type 'exit' to quit.")

    while True:
        question = input("\n> ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue
        for chunk in model.stream([system_message, HumanMessage(question)]):
            print(chunk.text, end="", flush=True)
        print()


if __name__ == "__main__":
    main()
