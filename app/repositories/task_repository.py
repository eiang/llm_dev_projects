from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate


def get_tasks(db: Session) -> list[Task]:
    stmt = select(Task)
    result = db.execute(stmt)
    return list(result.scalars().all())


def get_task_by_id(db: Session, task_id: int) -> Task | None:
    return db.get(Task, task_id)


def create_task(db: Session, task: TaskCreate) -> Task:
    # db_task = Task(title=task.title, description=task.description, priority=task.priority)
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task: Task, task_update: TaskCreate) -> Task:
    task.title = task_update.title
    task.description = task_update.description
    task.priority = task_update.priority
    task.category = task_update.category
    
    db.commit()
    db.refresh(task)
    return task
   

def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
