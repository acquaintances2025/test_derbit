from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from typing import Any

from application import courses_router
from infrastructure.course_parser.get_course import courses
from infrastructure import COURSES_TABLE, JobDb

scheduler = AsyncIOScheduler()

scheduler.add_job(courses, 'interval', seconds=60)


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        scheduler.start()
        await JobDb().create_pool()
        async with JobDb() as pool:
            await pool.execute(COURSES_TABLE)
        yield
        await JobDb().close_pool()

    app = FastAPI(
        lifespan=lifespan,
        title="Test",
        version="0.0.1"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["DNT", "X-CustomHeader", "Keep-Alive", "User-Agent", "X-Requested-With",
                       "If-Modified-Since", "Cache-Control", "Content-Type", "x-tz-offset", "Authorization"],
    )

    async def default_exception_handler(request: Request, exc: Any) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"message": "Ошибка исполнения процесса."}
        )

    app.default_exception_handler = default_exception_handler

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc) -> JSONResponse:
        if hasattr(exc, "body") and exc.body is None:
            return JSONResponse(status_code=400,
                                content={"message": "Отсутствуют параметры запроса"})
        return JSONResponse(status_code=400,
                            content={"message": "Параметры входа не соответствуют верным"})

    app.include_router(courses_router)

    return  app
