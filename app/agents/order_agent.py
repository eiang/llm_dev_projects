import json

from app.clients import llm_client
from app.tools.order_tools import AVAILABLE_TOOLS, TOOLS


def run_order_agent(messages: list[dict[str,object]],max_steps: int = 5) -> str:
    for step in range(max_steps):
        print(
        f"agent step: {step + 1}/{max_steps}"
        )
        message = llm_client.complete(messages,tools=TOOLS)
        # print("message type:",type(message))
        # print("message.model_dump type:",type(message.model_dump()))
        # print("message.model_dump exclude_none:",message.model_dump(exclude_none=True))
        messages.append(message.model_dump(exclude_none=True))
        print("messages:",messages)
        if not message.tool_calls:
            return message.content
        print("tool_calls:",message.tool_calls)
        for tool_call in message.tool_calls:
            print("tool_call:",tool_call)
            # print("tool_call type:",type(tool_call))
            function = AVAILABLE_TOOLS.get(tool_call.function.name)
            if function is None:
                continue
            arguments = json.loads(tool_call.function.arguments)
            result = function(**arguments)
           
            tool_message = {
                "role": "tool",
                "content": json.dumps(result, ensure_ascii=False),
                "tool_call_id": tool_call.id,
            }
            messages.append(tool_message)

    raise RuntimeError(f"Agent exceed max_steps: {max_steps}")



messages = [
    {
        "role": "user",
        "content": "帮我查一下订单 1001 的状态，并用自然语言告诉我。",
    }
]
if __name__ == "__main__":
    answer = run_order_agent(messages)  # pyright: ignore[reportArgumentType]

print("final answer:", answer)
print("final messages:", messages)
        

    