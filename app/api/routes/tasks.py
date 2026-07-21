from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.task import TaskCreate, TaskRead
from app.services import task_service

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("", response_model=TaskRead, status_code=201)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
):
    return task_service.create_task(db, payload)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    db: Session = Depends(get_db),
):
    return task_service.get_tasks(db)


@router.get("/overdue", response_model=list[TaskRead])
def list_overdue_tasks(
    db: Session = Depends(get_db),
):
    return task_service.get_overdue_tasks(db)

@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = task_service.get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.patch("/{task_id}/complete", response_model=TaskRead)
def mark_complete(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = task_service.complete_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task

