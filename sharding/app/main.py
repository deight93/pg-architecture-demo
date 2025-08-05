import os
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_NAME = os.environ["DB_NAME"]
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_HOST_SHARD1 = os.environ["DB_HOST_SHARD1"]
DB_HOST_SHARD2 = os.environ["DB_HOST_SHARD2"]

DATABASE_URL_SHARD1 = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST_SHARD1}:{DB_PORT}/{DB_NAME}"
DATABASE_URL_SHARD2 = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST_SHARD2}:{DB_PORT}/{DB_NAME}"

engine_shard1 = create_async_engine(DATABASE_URL_SHARD1, echo=True)
engine_shard2 = create_async_engine(DATABASE_URL_SHARD2, echo=True)

SessionShard1 = sessionmaker(bind=engine_shard1, class_=AsyncSession, expire_on_commit=False)
SessionShard2 = sessionmaker(bind=engine_shard2, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()


def get_shard_session(user_id: int):
    return SessionShard1 if user_id % 2 == 0 else SessionShard2

@app.post("/users")
async def create_user(user_id: int, name: str):
    Session = get_shard_session(user_id)
    async with Session() as session:
        await session.execute(
            text("INSERT INTO users (user_id, name) VALUES (:user_id, :name)"),
            {"user_id": user_id, "name": name}
        )
        await session.commit()
    return {"result": "inserted", "shard": 1 if user_id % 2 == 0 else 2}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    Session = get_shard_session(user_id)
    async with Session() as session:
        result = await session.execute(
            text("SELECT * FROM users WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        row = result.fetchone()
        if row:
            return dict(row._mapping)
        return {"error": "not found"}

@app.get("/all")
async def all_users():
    users = []
    for Session in (SessionShard1, SessionShard2):
        async with Session() as session:
            result = await session.execute(text("SELECT * FROM users"))
            users += [dict(r._mapping) for r in result.fetchall()]
    return {"users": users}
