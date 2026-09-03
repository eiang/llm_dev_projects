from openai import OpenAI
import openai

from app.core.config import settings


class LlmError(Exception):
    pass

client = OpenAI(
    api_key=settings.llm_api_key,
    base_url=settings.llm_base_url
)

def chat(input_messages: list[dict[str,str]],system_message: dict[str,str], *,json_mode: bool = False)  -> str:
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    try:
        response = client.chat.completions.create(  # pyright: ignore[reportCallIssue]
                model=settings.llm_model,
                messages=[  # pyright: ignore[reportArgumentType]
                    system_message,
                    *input_messages],
                **kwargs,
        )
    except openai.APIError as e:
        raise LlmError(
            "LLM API request failed"
        ) from e

    content = response.choices[0].message.content
    if content is None:
        raise LlmError("LLM response is None")

    return content
