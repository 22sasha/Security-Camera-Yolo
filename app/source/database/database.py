from pydantic import PostgresDsn
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncIterator
from .settings import get_db_settings

Base = declarative_base()

DB_SCHEME = "postgresql+asyncpg"
DB_SETTINGS = get_db_settings()

DATABASE_URL = PostgresDsn.build(
    scheme=DB_SCHEME,
    username=DB_SETTINGS.user,
    password=DB_SETTINGS.password,
    host=DB_SETTINGS.host,
    port=int(DB_SETTINGS.port),
    path=f"{DB_SETTINGS.db_name}",
)

ENGINE = create_async_engine(str(DATABASE_URL), pool_pre_ping=True,
                             future=True)


async def init_db():
    async with ENGINE.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    async_session = sessionmaker(
        bind=ENGINE,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
