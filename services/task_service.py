import logging
from datetime import datetime, timezone
import asyncio

import requests
from sqlalchemy.orm import Session

from models.task import Task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def trigger_webhook(task: Task, session: Session):
    try:
        # Fire the webhook
        response = requests.get(task.url)
        response.raise_for_status()

        # Update the task to mark it as triggered
        task.task_triggered = True
        session.commit()
        logger.info(f"Webhook triggered successfully for task {task.id}")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to trigger webhook for task {task.id}: {e}")


def check_expired_tasks(session: Session):
    expired_tasks = (
        session.query(Task)
        .filter(
            Task.expiration_time <= datetime.now(timezone.utc),
            Task.task_triggered == False,
            Task.task_triggered == False,
        )
        .all()
    )

    for task in expired_tasks:
        trigger_webhook(task, session)


async def periodic_task_checker(interval: int, session: Session):
    while True:
        check_expired_tasks(session)
        await asyncio.sleep(interval)
