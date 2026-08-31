from sqlalchemy.orm import Session

from app.models.task import Task
from app.repositories import task_repository
from app.schemas.task import TaskCreate


def create_task(db: Session, task: TaskCreate) -> Task:
    return task_repository.create_task(db, task)


def get_tasks(db: Session) -> list[Task]:
    return task_repository.get_tasks(db)


def get_task(db: Session, task_id: int) -> Task | None:
    return task_repository.get_task_by_id(db, task_id)


def delete_task(db: Session, task_id: int) -> bool:
    task = task_repository.get_task_by_id(db, task_id)
    if task is None:
        return False

    task_repository.delete_task(db, task)
    return True

def update_task(db: Session, task_id: int, task_update: TaskCreate) -> Task | None:
    task = task_repository.get_task_by_id(db, task_id)
    if task is None:
        return None
    return task_repository.update_task(db, task, task_update)
