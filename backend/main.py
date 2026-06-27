from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.session import engine, Base
from app.api.api_v1 import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # For development only: create tables on startup. 
    # In production, Alembic migrations should be used.
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"⚠️ Could not connect to PostgreSQL database during startup: {e}")
        print("⚠️ Genesis Engine REST APIs will still function, but Database APIs may fail.")
    yield
    try:
        await engine.dispose()
    except Exception:
        pass

app = FastAPI(
    title="GenesisWeb AI",
    description="Autonomous Software Development Platform API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
