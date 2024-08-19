import asyncio

from fastapi import FastAPI
from sqlalchemy.orm import Session

from initialization import create_tables
from models.database import get_db
from routers.timer import router as timer_router
from services import task_service

app = FastAPI()

create_tables()

app.include_router(timer_router)


@app.on_event("startup")
async def startup_event():
    """
    This function is called when the application starts.
    It creates a new task to check for periodic tasks every 60 seconds.
    """
    session: Session = next(get_db())
    asyncio.create_task(task_service.periodic_task_checker(60, session))
