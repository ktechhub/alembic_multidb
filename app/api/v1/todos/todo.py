# app/api/v1/todos/todo.py
from fastapi import APIRouter
from app.api.v1.todos import read, create, update, delete

router = APIRouter()


router.include_router(read.router, prefix="", tags=["todos"])
router.include_router(create.router, prefix="", tags=["todos"])
router.include_router(update.router, prefix="", tags=["todos"])
router.include_router(delete.router, prefix="", tags=["todos"])
