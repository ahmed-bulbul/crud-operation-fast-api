from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.v1.endpoints import users
from app.db.base import Base
from app.db.session import engine
from app.core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(title="FastAPI Starter Project", lifespan=lifespan)

# Routers
app.include_router(users.router)

# ✅ Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Unhandled error: {exc} | Path: {request.url.path}",
        exc_info=True  # prints full traceback
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error. Please try again later."},
    )
