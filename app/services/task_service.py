from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import date

from app.models.task import Task
from app.schemas.task import TaskCreate

def create_task(
    db: Session,
    payload: TaskCreate,
) -> Task:
    task = Task(**payload.model_dump())

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_tasks(
  db: Session,
        )->list[Task]:
    return db.scalars(select(Task)).all()

def get_task(
  db: Session,
  task_id: int,
        )->Task | None:
        return db.scalar(
            select(Task).where(Task.id == task_id)
        )

def complete_task(
    db: Session,
    task_id: int,
) -> Task | None:

    task = db.get(Task, task_id)

    if task is None:
        return None

    task.completed = True

    db.commit()

    db.refresh(task)

    return task

def get_overdue_tasks(
    db: Session,
) -> list[Task]:

    return db.scalars(
        select(Task).where(
            Task.completed.is_(False),
            Task.due_date.is_not(None),
            Task.due_date < date.today(),
        )
    ).all()
