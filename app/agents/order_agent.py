import json

from app.clients import llm_client
from app.tools.order_tools import AVAILABLE_TOOLS, TOOLS

def _append_tool_message(messages: list[dict[str,object]], 
tool_call_id: str, result: object) -> None:
    tool_message: dict[str,object] = {
        "role": "tool",
        "content": json.dumps(result, ensure_ascii=False),
        "tool_call_id": tool_call_id,
    }
    
    messages.append(tool_message)  

def run_order_agent(messages: list[dict[str,object]],max_steps: int = 5) -> str:
    for step in range(max_steps):
        print(
        f"agent step: {step + 1}/{max_steps}"
        )
        message = llm_client.complete(messages,tools=TOOLS)
        messages.append(message.model_dump(exclude_none=True,exclude={"reasoning_content"}))
        print("messages:",messages)
        if not message.tool_calls:
            if message.content is None:
                raise llm_client.LlmError(
                    "LLM returned no content"
                )

            return message.content
        print("tool_calls:",message.tool_calls)
        for tool_call in message.tool_calls:
            function = AVAILABLE_TOOLS.get(tool_call.function.name)
            if function is None:
                error_result: dict[str,object] = {
                    "error": "tool_not_found",
                    "message": f"Tool {tool_call.function.name} not found",
                }
                _append_tool_message(messages, tool_call.id, error_result) 
                continue
            try:
                arguments = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                error_result = {
                    "error": "invalid_tool_arguments",
                    "message": "Tool arguments are not valid JSON",
                }
                _append_tool_message(messages, tool_call.id, error_result) 
                continue
            try:
                result = function(**arguments)
            except Exception:
                error_result = {
                    "error": "tool_execution_error",
                    "message": "Tool execution error",
                }
                _append_tool_message(messages, tool_call.id, error_result)  
                continue
         
            _append_tool_message(messages, tool_call.id, result) 

    raise RuntimeError(f"Agent exceed max_steps: {max_steps}")




if __name__ == "__main__":
    messages: list[dict[str,object]] = [
        {
            "role": "user",
            "content": "帮我查一下订单 1001 的状态，并用自然语言告诉我。",
        }
    ]
    answer = run_order_agent(messages)  

    print("final answer:", answer)
    print("final messages:", messages)
        

    