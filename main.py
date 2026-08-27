from pydantic import BaseModel, Field
from fastapi import FastAPI, Query,status,HTTPException
import asyncio

app = FastAPI()

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    length: int
    preview: str

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=20, description="用户姓名")
    age: int = Field(ge=18, le=120, description="用户年龄")
    skills: list[str] = Field(default_factory=list, description="用户技能")
    nickname: str | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    skills: list[str]
    nickname: str | None = None

   
@app.post("/users",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
        
        await asyncio.sleep(0.5)
        return { "id": 1, "name": user.name, "age": user.age, "skills": user.skills, "nickname": user.nickname }

@app.get("/users/{user_id}",response_model=UserResponse)
def get_user_info(user_id: int):
    if user_id != 1:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )
    return {
        "id": 1,
        "name": "Tom",
        "age": 25,
        "skills": ["Java", "Python"],
        "nickname": None
        }


@app.get("/users")
def list_users(keywords: str | None = Query(None,max_length=20,min_length=2,description="搜索关键词"),
page: int = Query(1,ge=1,description="页码"),
page_size: int = Query(10,ge=1,le=100,description="每页数量")):
    return {"keywords": keywords,
            "page": page,
            "page_size": page_size}







@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    return AnalyzeResponse(length=len(request.text), preview=request.text[:20])
        
