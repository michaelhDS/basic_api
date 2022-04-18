from pydantic import BaseModel
from typing import Optional


class ToDoTask(BaseModel):
    task: str


class ToDoResponse(BaseModel):
    uid: Optional[str] = None
    task: str
