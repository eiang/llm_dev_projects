from openai import OpenAI
import openai

from app.core.config import settings



class LlmError(Exception):
    pass

client = OpenAI(
    api_key=settings.llm_api_key,
    base_url=settings.llm_base_url
)

def complete(
    input_messages: list[dict[str,object]],
    *,
    tools: list[dict[str,object]] | None = None,
    json_mode: bool = False,
):
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    if tools is not None:
        kwargs["tools"] = tools
    try:
        response = client.chat.completions.create(  # pyright: ignore[reportCallIssue]
            model=settings.llm_model,
            messages= input_messages,  # pyright: ignore[reportArgumentType]
            **kwargs,  
        )
        return response.choices[0].message
    except openai.APIError as e:
        raise LlmError(
            "LLM API request failed"
        ) from e
    

def chat(input_messages: list[dict[str,object]],system_message: dict[str,object], *,json_mode: bool = False)  -> str:
      
    message = complete(
        input_messages = [system_message,
        *input_messages],
        json_mode=json_mode,
    )
    content = message.content
    if content is None:
        raise LlmError("LLM response is None")

    return content




