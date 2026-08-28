from fastapi import APIRouter, HTTPException, status
from app.schemas.task import TaskCreate, TaskResponse
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=TaskResponse)
def create_task(task: TaskCreate):
    return task_service.create_task(task)
   

@router.get("/",status_code=status.HTTP_200_OK,response_model=list[TaskResponse])
def get_tasks():
    return  task_service.get_tasks()

@router.get("/{task_id}",status_code=status.HTTP_200_OK,response_model=TaskResponse)  
def get_task(task_id: int):
    task = task_service.get_task(task_id)
    if task is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )
    return task

@router.delete("/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if not task_service.delete_task(task_id):
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )
    return  None
