import json
from pydantic import ValidationError
from app.clients import llm_client
from app.schemas.ai import TaskExtractResult

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

    answer = llm_client.chat(input_messages,system_message)
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
    

    answer = llm_client.chat([user_message],system_message,json_mode=True)
  
    try:
        data = json.loads(answer)
        return TaskExtractResult.model_validate(data)

    except (json.JSONDecodeError, ValidationError) as e:
        raise llm_client.LlmError(
            "Invalid structured output from LLM"
        ) from e