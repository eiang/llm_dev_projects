from openai import OpenAI
import openai

from app.core.config import settings
from app.tools.order_tools import TOOLS


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


def test_tool_call():
    user_messages = [
    {
        "role": "user",
        "content": "请你介绍一下你自己",
    },
    ]

    response = client.chat.completions.create(
        model=settings.llm_model,
        messages= user_messages,  # pyright: ignore[reportArgumentType]
        
        tools=TOOLS,  # pyright: ignore[reportArgumentType]
    )
    print(response.choices[0].message)


# print("我是 llm_client.py，我的 __name__ =", repr(__name__))
if __name__ == "__main__":
    test_tool_call()
