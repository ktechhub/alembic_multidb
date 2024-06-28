# app/schemas/todo.py
from pydantic import BaseModel
from typing import Optional
from .base_schema import BaseSchema


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    pass


class Todo(BaseSchema, TodoBase):
    pass
