import json

from app.clients import llm_client
from app.tools.order_tools import AVAILABLE_TOOLS, TOOLS


def run_order_agent(messages: list[dict[str,object]]) -> str:
    while True:
        message = llm_client.complete(messages,tools=TOOLS)
        print("message type:",type(message))
        print("message.model_dump type:",type(message.model_dump()))
        print("message.model_dump exclude_none:",message.model_dump(exclude_none=True))
        # messages.append(message.model_dump(exclude_none=True))
        print("messages:",messages)
        if not message.tool_calls:
            return message.content
        print("tool_calls:",message.tool_calls)
        for tool_call in message.tool_calls:
            print("tool_call:",tool_call)
            print("tool_call type:",type(tool_call))
            function = AVAILABLE_TOOLS.get(tool_call.function.name)
            if function is None:
                continue
            arguments = json.loads(tool_call.function.arguments)
            result = function(**arguments)
            assistant_message = {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": tool_call.type,
                        "function": {
                        "name": tool_call.function.name,  
                        "arguments": tool_call.function.arguments, 
                        }
                    }
                ]
            }
            messages.append(assistant_message)
            tool_message = {
                "role": "tool",
                "content": json.dumps(result, ensure_ascii=False),
                "tool_call_id": tool_call.id,
            }
            messages.append(tool_message)
        
        

    