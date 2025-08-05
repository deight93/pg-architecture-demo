import os
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_NAME = os.environ["DB_NAME"]
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_HOST_MASTER = os.environ["DB_HOST_MASTER"]
DB_HOST_REPLICA = os.environ["DB_HOST_REPLICA"]

DATABASE_URL_MASTER = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST_MASTER}:{DB_PORT}/{DB_NAME}"
DATABASE_URL_REPLICA = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST_REPLICA}:{DB_PORT}/{DB_NAME}"

engine_master = create_async_engine(DATABASE_URL_MASTER, echo=True)
engine_replica = create_async_engine(DATABASE_URL_REPLICA, echo=True)

SessionMaster = sessionmaker(bind=engine_master, class_=AsyncSession, expire_on_commit=False)
SessionReplica = sessionmaker(bind=engine_replica, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()

@app.get("/master")
async def read_master():
    async with SessionMaster() as session:
        result = await session.execute(text("SELECT * FROM test_table"))
        rows = result.fetchall()
        return {"master_data": [dict(row._mapping) for row in rows]}

@app.get("/replica")
async def read_replica():
    async with SessionReplica() as session:
        result = await session.execute(text("SELECT * FROM test_table"))
        rows = result.fetchall()
        return {"replica_data": [dict(row._mapping) for row in rows]}

@app.post("/master")
async def write_master(value: str):
    async with SessionMaster() as session:
        await session.execute(text("INSERT INTO test_table (value) VALUES (:v)"), {"v": value})
        await session.commit()
    return {"result": "inserted into master"}
