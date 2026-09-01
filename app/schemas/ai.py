from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
        message: str = Field(description="用户输入的消息")
