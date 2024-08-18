from pydantic import BaseModel


class TaskResponse(BaseModel):
    id: int
    time_left: int

    class Config:
        orm_mode: True
