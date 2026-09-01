from app.clients import llm_client


def chat(message: str) -> str:
    return llm_client.chat(message)