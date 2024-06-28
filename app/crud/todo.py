# app/crud/todo.py
from app.models.todo import Todo
from app.crud.base import CRUDBase
from app.schemas.todo import TodoCreate, TodoUpdate


class CRUDTodo(CRUDBase[Todo, TodoCreate, TodoUpdate]):
    pass


todo = CRUDTodo(Todo)
