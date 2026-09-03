from fastapi import APIRouter, HTTPException
from app.clients.llm_client import LlmError
from app.schemas.ai import ChatRequest, ChatResponse, TaskExtractRequest, TaskExtractResult
from app.services import ai_service

router = APIRouter(prefix="/ai",tags=["ai"])

@router.post("/chat", response_model=ChatResponse)
def chat(chat_request: ChatRequest) -> ChatResponse:
    try:
        answer = ai_service.chat(chat_request.conversation_id, chat_request.message)
    except LlmError as e:
        raise HTTPException(
            status_code=500,
            detail="AI服务返回异常"
        ) from e

    return ChatResponse(conversation_id=chat_request.conversation_id, answer=answer)

@router.post("/extract_task", response_model=TaskExtractResult)
def extract_task( request: TaskExtractRequest) -> TaskExtractResult:
    try:
        answer = ai_service.extract_task(request.text)
    except LlmError as e:
        raise HTTPException(
            status_code=500,
            detail="AI服务返回异常"
        ) from e

    return answer