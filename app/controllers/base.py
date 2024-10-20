from typing import Generic, TypeVar
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import ASYNC_SCOPED_SESSION

T = TypeVar('T')
class Controller(Generic[T]):

    def __init__(self, model:T, session:AsyncSession=None, autocommit=False):
        self.model = model
        self.autocommit = autocommit
        if session is None:
            self.session:AsyncSession = ASYNC_SCOPED_SESSION()
        else:
            self.session = session

    async def create(self, **kwargs) -> T:
        obj = self.model(**kwargs)
        self.session.add(obj)
        if self.autocommit:
            await self.session.commit()
        return obj

    async def find(self, **kwargs) -> list[T]:
        result = await self.session.scalars(Select(self.model).filter_by(**kwargs))
        return result.all()
    
    async def get_by_id(self, id:int) -> T:
        await self.session.get(self.model, id)

    async def delete(self, obj:T):
        await self.session.delete(obj)
        if self.autocommit:
            await self.session.commit()