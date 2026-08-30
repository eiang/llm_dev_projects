from pydantic import BaseModel, Field,ConfigDict


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200, description="任务标题")
    description: str | None = None
    priority: int = Field(default=1, ge=1, le=5, description="任务优先级")


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None = None
    priority: int
    completed: bool
