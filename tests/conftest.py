import asyncio
from typing import Generator, AsyncGenerator

import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from db.models import Base
from db.session import get_db
from main import app

from settings import POSTGRES_URL_TEST

engine_test = create_async_engine(
    POSTGRES_URL_TEST,
    future=True,
    echo=True,
    execution_options={"isolation_level": "READ COMMITTED"},
)

async_session = sessionmaker(
    engine_test,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base.metadata.bind = engine_test


async def override_get_db() -> Generator:
    async with async_session() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope='session')
async def prepare_database() -> None:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with engine_test.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all())


@pytest.fixture(scope='session')
def event_loop(request) -> None:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        yield ac
