# app/schemas/base_schema.py
from pydantic import BaseModel
from datetime import datetime


class BaseSchema(BaseModel):
    id: int
    views: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BaseSlugSchema(BaseSchema):
    slug: str

    class Config:
        orm_mode = True
