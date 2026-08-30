from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.task import TaskCreate, TaskResponse
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task(task: TaskCreate, db: DbSession):
    return task_service.create_task(db, task)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[TaskResponse])
def get_tasks(db: DbSession):
    return task_service.get_tasks(db)


@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
def get_task(task_id: int, db: DbSession):
    task = task_service.get_task(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: DbSession) -> Response:
    if not task_service.delete_task(db, task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
