from typing import Generic, TypeVar
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import ASYNC_SCOPED_SESSION

T = TypeVar('T')
class DAO(Generic[T]):

    def __init__(self, model:T, session:AsyncSession=None, autocommit=True):
        self.model = model
        self.autocommit = autocommit
        if session is None:
            self.session:AsyncSession = ASYNC_SCOPED_SESSION()
        else:
            self.session = session

    async def clean_all(self) -> None:
        await self.session.execute(f"TRUNCATE TABLE {self.model.__tablename__}")
        if self.autocommit:
            await self.session.commit()

    async def create(self, **kwargs) -> T:
        obj = self.model(**kwargs)
        self.session.add(obj)
        if self.autocommit:
            await self.session.commit()
            await self.session.refresh(obj)
        return obj

    async def find(self, **kwargs) -> list[T]:
        result = await self.session.scalars(Select(self.model).filter_by(**kwargs))
        return result.all()

    async def find_one(self, **kwargs) -> T | None:
        result = await self.find(**kwargs)
        if len(result) > 0:
            return result[0]
    
    async def get_by_id(self, id:int) -> T | None:
        return await self.session.get(self.model, id)

    async def delete(self, obj:T) -> None:
        await self.session.delete(obj)
        if self.autocommit:
            await self.session.commit()