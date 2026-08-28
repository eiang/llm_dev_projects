from app.schemas.task import TaskCreate, TaskResponse

tasks_db: list[TaskResponse] = []

def create_task(task: TaskCreate) -> TaskResponse:
    new_task = TaskResponse(
        id=max((item.id for item in tasks_db), default=0) + 1,
        title=task.title,
        description=task.description,
        priority=task.priority,
    )
    tasks_db.append(new_task)
   
    return new_task

def get_tasks() -> list[TaskResponse]:
    return tasks_db

def get_task(task_id: int) -> TaskResponse | None:
    task = next((t for t in tasks_db if t.id == task_id), None)
    return task

def delete_task(task_id: int) -> bool:
    task = get_task(task_id)
    if task is None:
        return False
    tasks_db.remove(task)
    return True