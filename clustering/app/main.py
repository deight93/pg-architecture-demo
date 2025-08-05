from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()

@app.get("/users")
async def read_users():
    async with SessionLocal() as session:
        result = await session.execute(text("SELECT * FROM users LIMIT 10"))
        users = result.fetchall()
        return {"users": [dict(row._mapping) for row in users]}

@app.post("/cluster")
async def cluster_table():
    async with SessionLocal() as session:
        # 인덱스 기준 클러스터링
        await session.execute(text("CLUSTER users USING idx_users_email;"))
        await session.commit()
        return {"result": "Clustered users table by idx_users_email"}
