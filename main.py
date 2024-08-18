from fastapi import FastAPI

from initialization import create_tables
from routers.timer import router as timer_router

app = FastAPI()

create_tables()

app.include_router(timer_router)


@app.get("/")
def root():
    return {"message": "This is the Task Scheduler Service"}
