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
    session: Session = next(get_db())
    asyncio.create_task(task_service.periodic_task_checker(60, session))  # Sin `await`
