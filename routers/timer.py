from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from models.task import create_task, get_task
from models.database import get_db
from schemas.tasks import TaskResponse

router = APIRouter()


@router.post("/timer", response_model=TaskResponse)
def set_timer(
    hours: int,
    minutes: int,
    seconds: int,
    url: str,
    db: Session = Depends(get_db),
):
    new_task = create_task(db, hours, minutes, seconds, url)
    return TaskResponse(id=new_task.id, time_left=new_task.time_left())


@router.get("/timer/{timer_id}", response_model=TaskResponse)
async def get_timer(timer_id: int, db: Session = Depends(get_db)):
    task = get_task(db, timer_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(id=task.id, time_left=task.time_left())
