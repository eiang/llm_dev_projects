from openai import OpenAI

from app.core.config import settings


class LlmError(Exception):
    pass

client = OpenAI(
    api_key=settings.llm_api_key,
    base_url=settings.llm_base_url
)
TASK_EXTRACT_SYSTEM_PROMPT = """
你是一个任务提取助手,负责从文本中提取任务信息。
你的任务是根据用户输入的文本,提取出任务的标题、描述和优先级。
字段:
    title: 任务标题
    description: 任务描述
    priority: 任务优先级,取值为"low"、"medium"或"high"
    如果文本中没有明确的任务描述，则 description 为 null。
业务规则：
priority 判断规则：
- high：用户明确表达紧急、重要、必须尽快完成、截止时间临近等含义
- low：用户明确表达不着急、有空再做、可以延后等含义
- medium：没有明显高优先级或低优先级信号时默认使用 medium
输出Json格式的字符串，包含title、description和priority字段
示例:
用户输入：
今晚必须完成数据库作业，这件事情很重要。

输出：
{
    "title": "完成数据库作业",
    "description": "今晚完成数据库作业",
    "priority": "high"
}
"""
def chat(input_messages: list[dict[str,str]]) -> str:
    system_message = {"role": "system", "content": TASK_EXTRACT_SYSTEM_PROMPT}
    response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[  # pyright: ignore[reportArgumentType]
                system_message,
                *input_messages],
            response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    print(response.usage)
    if content is None:
        raise LlmError("LLM response is None")

    return content
