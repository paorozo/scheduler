import asyncio
import logging
from datetime import datetime, timezone

import requests
from sqlalchemy.orm import Session

from models.task import Task

logger = logging.getLogger(__name__)


def trigger_webhook(task: Task, session: Session):
    """
    Trigger the webhook for the given task
    """
    try:
        response = requests.get(task.url)
        response.raise_for_status()

        # Update the task to mark it as triggered
        task_triggered = (
            session.query(Task)
            .filter(Task.id == task.id, Task.task_triggered == False)
            .update({"task_triggered": True})
        )

        if task_triggered:
            session.commit()
            logger.info(f"Webhook triggered successfully for task {task.id}")
        else:
            session.rollback()
            logger.info(f"Task {task.id} was already triggered by another instance.")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to trigger webhook for task {task.id}: {e}")


def check_expired_tasks(session: Session):
    """
    Check for expired tasks and trigger their webhooks  if they haven't been triggered yet
    """
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
    """
    Periodically check for expired tasks and trigger their web hooks
    """
    while True:
        check_expired_tasks(session)
        await asyncio.sleep(interval)
