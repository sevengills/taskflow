from datetime import date
from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="TaskFlow API", version="1.1.0")
class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = ""
    completed: bool = False
    due_date: Optional[date] = None
    @field_validator("due_date")
    def validate_due_date(cls, v):
        if v and v < date.today():
            raise ValueError("due_date cannot be in the past")
        return v
      
class Task(TaskCreate):
    id: int
    overdue: bool = False
_next_id = 1
_tasks: Dict[int, Task] = {}

def update_overdue_flags():
    today = date.today()
    for task in _tasks.values():
        task.overdue = bool(task.due_date and task.due_date < today and not task.completed)

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    global _next_id
    update_overdue_flags()
    task = Task(id=_next_id, **payload.model_dump())
    _tasks[task.id] = task
    _next_id += 1
    return task
  
@app.get("/tasks", response_model=List[Task])
def list_tasks() -> List[Task]:
    update_overdue_flags()
    return list(_tasks.values())
  
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    task = _tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="not found")
    return task
  
@app.patch("/tasks/{task_id}/complete", response_model=Task)
def mark_complete(task_id: int) -> Task:
    task = _tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = True
    task.overdue = False
    return task
    
@app.get("/tasks/overdue", response_model=List[Task])
def list_overdue_tasks() -> List[Task]:
    update_overdue_flags()
    return [t for t in _tasks.values() if t.overdue]