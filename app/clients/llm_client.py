from openai import OpenAI

from app.core.config import settings


class LlmError(Exception):
    pass

client = OpenAI(
    api_key=settings.llm_api_key,
    base_url=settings.llm_base_url
)

def chat(message: str) -> str:
    response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": "你是一个Ai智能助理,负责回答用户的问题"},
                {"role": "user", "content": message}],
    )
    content = response.choices[0].message.content

    if content is None:
        raise LlmError("LLM response is None")

    return content
