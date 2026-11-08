from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage

from app.config import settings


def main() -> None:
    model = init_chat_model(
        settings.openai_chat_model,
        model_provider="openai",
        api_key=settings.openai_api_key,
    )

    print("No-RAG chat started.")
    print("This chat does not use the internal knowledge base yet.")
    print("Type 'exit' to quit.")

    while True:
        question = input("\n> ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue
        for chunk in model.stream([HumanMessage(question)]):
            print(chunk.text, end="", flush=True)
        print()


if __name__ == "__main__":
    main()
