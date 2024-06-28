# app/api/v1/todos/read.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.todo import todo
from app.schemas.todo import Todo
from app.database.database import get_async_session
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Todo] or None, summary="Get all Todos")
async def read_todos(
    *, db: AsyncSession = Depends(get_async_session), skip: int = 0, limit: int = 100
) -> List[Todo]:
    """
    Retrieve all Todos.

    Args:
    - db (AsyncSession): AsyncSession dependency from get_db to interact with the database.
    - skip (int): Number of records to skip (default is 0).
    - limit (int): Maximum number of records to return (default is 100).

    Returns:
    - List[Todo]: A list of retrieved Todo objects.

    Raises:
    - HTTPException 404: If no Todos are found.
    """
    todos = await todo.get_multi(db=db, skip=skip, limit=limit)
    return todos


@router.get("/{id}", response_model=Todo, summary="Get a Todo by ID")
async def read_todo(*, db: AsyncSession = Depends(get_async_session), id: int) -> Todo:
    """
    Get a Todo by ID.

    Args:
    - db (AsyncSession): AsyncSession dependency from get_db to interact with the database.
    - id (int): The ID of the Todo to retrieve.

    Returns:
    - Todo: The retrieved Todo object.

    Raises:
    - HTTPException 404: If the Todo with the given ID does not exist.
    """
    todo_item = await todo.get(db=db, id=id)
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_item
