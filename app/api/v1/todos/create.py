from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.todo import todo
from app.schemas.todo import Todo, TodoCreate
from app.database.database import get_async_session

router = APIRouter()


@router.post("/", response_model=Todo, summary="Create a new Todo")
async def create_todo(
    *, db: AsyncSession = Depends(get_async_session), todo_in: TodoCreate
) -> Todo:
    """
    Create a new Todo.

    Args:
    - db (AsyncSession): AsyncSession dependency from get_db to interact with the database.
    - todo_in (TodoCreate): Input data for creating the Todo.

    Returns:
    - Todo: The created Todo object.

    Raises:
    - HTTPException 400: If the request data is invalid.
    """
    return await todo.create(db=db, obj_in=todo_in)
