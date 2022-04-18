from pydantic import BaseModel


class ToDoTask(BaseModel):
    task: str


class ToDoResponse(BaseModel):
    id: int
    task: str

    class Config:
        orm_mode = True
