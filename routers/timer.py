import logging
from datetime import datetime, timezone
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from models.database import get_db
from models.task import create_task, get_task
from schemas.tasks import TaskResponse
from services.task_service import trigger_webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


def ensure_url_scheme(url: str) -> str:
    """
    Ensure that the URL has a scheme (http or https) and return the URL with the scheme.
    """
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = "https://" + url
    return url


@router.post("/timer", response_model=TaskResponse)
def set_timer(
    hours: int,
    minutes: int,
    seconds: int,
    url: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Set a timer for the given duration and URL. The timer will trigger a webhook when it expires.
    """
    url = ensure_url_scheme(url)
    new_task = create_task(db, hours, minutes, seconds, url)
    now_time = datetime.now(timezone.utc)

    logger.info(f"Expiration time: {new_task.expiration_time} - Now time: {now_time}")

    if new_task.expiration_time <= now_time:
        trigger_webhook(new_task, db)

    return TaskResponse(id=new_task.id, time_left=new_task.time_left())


@router.get("/timer/{timer_id}", response_model=TaskResponse)
async def get_timer(timer_id: int, db: Session = Depends(get_db)):
    """
    Get the time left for the timer with the given ID.
    """
    task = get_task(db, timer_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(id=task.id, time_left=task.time_left())
