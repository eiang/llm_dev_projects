from typing import Annotated, Literal

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


class TaskExtractRequest(BaseModel):
        text:  Annotated[
                str,
                StringConstraints(min_length=1,strip_whitespace=True),
                Field(description="待提取任务的文本"),
                ]

class TaskExtractResult(BaseModel):
        title: str = Field(description="提取到的任务标题")
        description: str | None  = Field(default=None,description="提取到的任务描述")
        priority: Literal["low", "medium", "high"] = Field(description="提取到的任务优先级")



