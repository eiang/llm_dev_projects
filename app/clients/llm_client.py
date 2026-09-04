import json

from openai import OpenAI
import openai

from app.core.config import settings
from app.tools.order_tools import  AVAILABLE_TOOLS, TOOLS


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
        "content": "帮我查询一下订单号为1002的状态",
    },
    ]

    response = client.chat.completions.create(
        model=settings.llm_model,
        messages= user_messages,  # pyright: ignore[reportArgumentType]
        
        tools=TOOLS,  # pyright: ignore[reportArgumentType]
    )
    message = response.choices[0].message
    
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name  # pyright: ignore[reportAttributeAccessIssue]
        arguments_json = tool_call.function.arguments  # pyright: ignore[reportAttributeAccessIssue]
        arguments = json.loads(arguments_json)
        function = AVAILABLE_TOOLS.get(function_name)
        if function is None:
            raise ValueError(f"Unknown tool:{function_name}")
        result = function(**arguments)
        assistant_messages =  {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,  # pyright: ignore[reportAttributeAccessIssue]
                        "arguments": tool_call.function.arguments,  # pyright: ignore[reportAttributeAccessIssue]
                    },
                    },
                ],
            }
        
        user_messages.append(assistant_messages)  
        tool_message = {
            "role": "tool",
            "content": json.dumps(result, ensure_ascii=False),
            "tool_call_id": tool_call.id,
        }
        user_messages.append(tool_message)
        final_response = client.chat.completions.create(
            model=settings.llm_model,
            messages=user_messages,  # pyright: ignore[reportArgumentType]
            tools=TOOLS,  # pyright: ignore[reportArgumentType]
        )
        final_message = final_response.choices[0].message
        print("final answer:",final_message.content)
# print("我是 llm_client.py，我的 __name__ =", repr(__name__))
if __name__ == "__main__":
    test_tool_call()
