from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, habits, analytics
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # For development only! In production, use Alembic.
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="TimeTrack API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(habits.router)
app.include_router(analytics.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to TimeTrack API"}
