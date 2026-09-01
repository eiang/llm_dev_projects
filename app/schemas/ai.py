from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class ChatRequest(BaseModel):
        message: Annotated[
                str,
                StringConstraints(min_length=1,strip_whitespace=True),
                Field(description="用户输入的消息"),
                ]


class ChatResponse(BaseModel):
        answer: str = Field(description="AI回复的消息")
