from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200, description="任务标题")
    description: str | None = None
    priority: int = Field(default=1, ge=1, le=5, description="任务优先级")
    category: str | None  = Field(None,max_length=20,description="任务分类")




class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None = None
    priority: int
    completed: bool
    category: str | None = None