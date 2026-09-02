from openai import OpenAI

from app.core.config import settings


class LlmError(Exception):
    pass

client = OpenAI(
    api_key=settings.llm_api_key,
    base_url=settings.llm_base_url
)

def chat(input_messages: list[dict[str,str]]) -> str:
    system_message = {"role": "system", "content": "你是一个Ai智能助理,负责回答用户的问题"}
    response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[  # pyright: ignore[reportArgumentType]
                system_message,
                *input_messages],
    )
    content = response.choices[0].message.content
    print(response.usage)
    if content is None:
        raise LlmError("LLM response is None")

    return content
