from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class ChatRequest(BaseModel):
        conversation_id: Annotated[
                str,
                StringConstraints(min_length=1,strip_whitespace=True),
                Field(description="会话ID"),
                ]
        message: Annotated[
                str,
                StringConstraints(min_length=1,strip_whitespace=True),
                Field(description="用户输入的消息"),
                ]


class ChatResponse(BaseModel):
        conversation_id: Annotated[
                str,
                StringConstraints(min_length=1,strip_whitespace=True),
                Field(description="会话ID"),
                ]
        answer: str = Field(description="AI回复的消息")
