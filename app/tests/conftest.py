import os
from typing import AsyncGenerator
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.models import Base, db_helper
from main import application

from dotenv import load_dotenv

load_dotenv(".env.test")

DATABASE_TEST_URL = os.getenv("APP_CONFIG__DB__URL")

engine_test = create_async_engine(DATABASE_TEST_URL, echo=True)
SessionTest = async_sessionmaker(engine_test, expire_on_commit=False)


@pytest.fixture(scope="session")
async def test_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine_test.dispose()


@pytest.fixture()
async def session(test_db) -> AsyncGenerator[AsyncSession, None]:
    async with SessionTest() as session:
        yield session
        await session.rollback()


@pytest.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session():
        async with SessionTest() as s:
            yield s

    application.dependency_overrides[
        db_helper.session_getter] = override_get_session

    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
