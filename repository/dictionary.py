from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.models import Dictionary

class DictionaryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_category_id_by_name(self, name: str) -> int | None:
        stmt = select(Dictionary.id).where(Dictionary.name == name)
        result = await self.session.execute(stmt)
        category = result.scalar_one_or_none()
        return category if category else None
    
    async def get_category_name_by_id(self, id: int) -> str | None:
        stmt = select(Dictionary.name).where(Dictionary.id == id)
        result = await self.session.execute(stmt)
        category = result.scalar_one_or_none()
        return category if category else None


