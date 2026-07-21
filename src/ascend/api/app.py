"""ASCEND API — FastAPI application factory.

Middleware stack:
  1. CorrelationMiddleware (X-Correlation-ID)
  2. RequestLogMiddleware (method, path, status, latency)
  3. ErrorHandlerMiddleware (every exception → ASCEND_ERROR)
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ascend.adapter.runtime_adapter import RuntimeAdapter
from ascend.api.middleware.correlation import CorrelationMiddleware
from ascend.api.middleware.error_handler import ErrorHandlerMiddleware
from ascend.api.middleware.logger import RequestLogMiddleware
from ascend.api.routers import auth, builder, demo, health, journey, mission, version

APP_TITLE = "ASCEND API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = (
    "Competency Development Framework — public API boundary layer. "
    "Zero business logic. Routes validate, delegate to RuntimeAdapter, "
    "and serialize."
)


def create_app(db_path: str | None = None) -> FastAPI:
    if db_path is None:
        db_path = os.getenv("ASCEND_DB_PATH", "ascend.db")
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        adapter = RuntimeAdapter(db_path=db_path)
        adapter.initialize_database()
        app.state.adapter = adapter
        yield
        adapter.close()

    app = FastAPI(
        title=APP_TITLE,
        version=APP_VERSION,
        description=APP_DESCRIPTION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(CorrelationMiddleware)
    app.add_middleware(RequestLogMiddleware)
    app.add_middleware(ErrorHandlerMiddleware)

    app.include_router(health.router)
    app.include_router(version.router)
    app.include_router(builder.router)
    app.include_router(auth.router)
    app.include_router(demo.router)
    app.include_router(journey.router)
    app.include_router(mission.router)

    return app
