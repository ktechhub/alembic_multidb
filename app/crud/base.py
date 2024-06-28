# app/crud/base.py
from typing import Generic, Type, TypeVar, List, Optional, Any
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from app.database.base import Base

ModelType = TypeVar("ModelType", bound="Base")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Retrieve a single record by its ID.

        **Parameters**

        * `db`: The database session
        * `id`: The ID of the record to retrieve

        **Returns**

        The retrieved record or `None` if not found.
        """
        result = await db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Retrieve multiple records with pagination.

        **Parameters**

        * `db`: The database session
        * `skip`: The number of records to skip (default is 0)
        * `limit`: The maximum number of records to return (default is 100)

        **Returns**

        A list of retrieved records.
        """
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.

        **Parameters**

        * `db`: The database session
        * `obj_in`: The data for the new record

        **Returns**

        The created record.
        """
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """
        Update an existing record.

        **Parameters**

        * `db`: The database session
        * `db_obj`: The existing record to update
        * `obj_in`: The new data for the record

        **Returns**

        The updated record.
        """
        obj_data = db_obj.__dict__
        update_data = obj_in.model_dump(exclude_defaults=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        """
        Delete a record by its ID.

        **Parameters**

        * `db`: The database session
        * `id`: The ID of the record to delete

        **Returns**

        The deleted record.
        """
        obj = await self.get(db, id)
        await db.delete(obj)
        await db.commit()
        return obj

    async def increment_views(self, db: AsyncSession, *, id: int) -> None:
        """
        Increment the views count for a record.

        **Parameters**

        * `db`: The database session
        * `id`: The ID of the record to increment views

        **Returns**

        None
        """
        await db.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(views=self.model.views + 1)
        )
        await db.commit()
