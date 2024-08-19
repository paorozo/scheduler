from pydantic import BaseModel, ConfigDict


class TaskResponse(BaseModel):
    id: int
    time_left: int

    model_config = ConfigDict(from_attributes=True)
