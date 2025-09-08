from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.endpoints import users
from app.db.base import Base
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(title="FastAPI Starter Project", lifespan=lifespan)

# Include Routers
app.include_router(users.router)
