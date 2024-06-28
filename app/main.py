# app/main.py
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.todos import todo

description_text = """
FastAPI TODO API Asynchronous Demo
"""

app = FastAPI(
    title="FastAPI TODO API Asynchronous Demo",
    openapi_url="/openapi.json",
    description=description_text,
    version=settings.API_VERSION,
    contact=settings.CONTACT,
    terms_of_service="https://www.ktechhub.com/terms/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url="/docs")


@app.get("/ready", status_code=status.HTTP_200_OK, include_in_schema=True)
async def ready() -> str:
    """Check if API it's ready"""
    return "ready"


app.include_router(
    todo.router,
    prefix="/api/v1/todos",
    tags=["todos"],
)
