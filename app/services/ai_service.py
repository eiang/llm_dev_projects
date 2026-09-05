import json
from pydantic import ValidationError
from app.clients import llm_client
from app.schemas.ai import TaskExtractResult
from app.tools.order_tools import AVAILABLE_TOOLS, TOOLS

conversations: dict[str, list[dict[str, str]]] = {}

SYSTEM_PROMPT = """
你是一个通用助手,负责回答用户的问题。
"""




TASK_EXTRACT_SYSTEM_PROMPT = """
你是一个任务提取助手,负责从文本中提取任务信息。
你的任务是根据用户输入的文本,提取出任务的标题、描述和优先级。
字段:
    title: 任务标题
    description: 任务描述
    priority: 任务优先级,取值为"low"、"medium"或"high"
    如果没有明确的任务描述，description 必须为 null，
    不要使用空字符串。
规则：
1. title 必须简洁。
2. description 可以为空。
3. priority 只能是 low、medium、high。
4. 如果用户明确表达“重要、紧急、必须尽快完成、优先处理”等含义，
   priority 为 high。
5. 如果用户明确表达“不着急、有时间再做、可以延后”等含义，
   priority 为 low。
6. 如果没有明显优先级信息，
   priority 默认为 medium。
示例:
用户输入：
今晚必须完成数据库作业，这件事情很重要。

请将结果以 json 格式输出，不要输出其他任何内容：
{
    "title": "完成数据库作业",
    "description": "今晚完成数据库作业",
    "priority": "high"
}
"""


def chat(conversation_id: str, message: str) -> str:
    
    history = conversations.setdefault(conversation_id, [])
    system_message = {"role": "system", "content": SYSTEM_PROMPT}
    user_message = {
        "role": "user",
        "content": message,
    }
    # 新建临时 list，不直接修改正式 history
    input_messages =  [*history, user_message]

    answer = llm_client.chat(input_messages,system_message)  # pyright: ignore[reportArgumentType]
    # LLM 成功后才保存本轮对话
    
    history.append(user_message)
    history.append({"role": "assistant", "content": answer})
    return answer


def extract_task(text: str) -> TaskExtractResult:
    
    system_message = {"role": "system", "content": TASK_EXTRACT_SYSTEM_PROMPT}
    user_message = {
        "role": "user",
        "content": text,
    }
    

    answer = llm_client.chat([user_message],system_message,json_mode=True)  # pyright: ignore[reportArgumentType]
  
    try:
        data = json.loads(answer)
        return TaskExtractResult.model_validate(data)

    except (json.JSONDecodeError, ValidationError) as e:
        raise llm_client.LlmError(
            "Invalid structured output from LLM"
        ) from e


def chat_with_tools(input_message: str) -> str:
    user_messages: list[dict[str, object]]  = [
    {
        "role": "user",
        "content": input_message,
    },
    ]

    
    message = llm_client.complete(user_messages,tools=TOOLS)
    
    
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name  
        arguments_json = tool_call.function.arguments  
        arguments = json.loads(arguments_json)
        function = AVAILABLE_TOOLS.get(function_name)
        if function is None:
            raise ValueError(f"Unknown tool:{function_name}")
        result = function(**arguments)
        assistant_message =  {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,  
                        "arguments": tool_call.function.arguments, 
                    },
                    },
                ],
            }
        
        user_messages.append(assistant_message)  
        tool_message = {
            "role": "tool",
            "content": json.dumps(result, ensure_ascii=False),
            "tool_call_id": tool_call.id,
        }
        user_messages.append(tool_message)
        final_message = llm_client.complete(user_messages,tools=TOOLS)  
        if final_message.content is None:
            raise llm_client.LlmError("LLM returned None")
        return final_message.content
    if message.content is None:
        raise llm_client.LlmError("LLM returned None")
    return message.content

if __name__ == "__main__":
    print(  
        chat_with_tools(
        "你好，介绍下自己"
    )
    )

