from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeMeta

from core.config import Settings
from typing import AsyncGenerator

settings = Settings()

engine = create_async_engine(
    url=settings.database_url,
    echo=True
)

Maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Maker() as session:
        yield session