from app.clients import llm_client

conversations: dict[str, list[dict[str, str]]] = {}

def chat(conversation_id: str, message: str) -> str:
    
    history = conversations.setdefault(conversation_id, [])
   
    user_message = {
        "role": "user",
        "content": message,
    }
    # 新建临时 list，不直接修改正式 history
    input_messages =  [*history, user_message]

    answer = llm_client.chat(input_messages)
    # LLM 成功后才保存本轮对话
    
    history.append(user_message)
    history.append({"role": "assistant", "content": answer})
    return answer
