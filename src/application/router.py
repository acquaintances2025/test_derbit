from fastapi import APIRouter, Query

from datetime import datetime

from .path import ALL_COURSES, END_COURSES, DATE_COURSES
from .views import all_courses, end_courses, date_courses
courses_router = APIRouter()

@courses_router.get(ALL_COURSES)
async def get_all_courses(ticker: str = Query(description="Валюта запроса")):
    result = await all_courses(ticker)
    return result

@courses_router.get(END_COURSES)
async def get_all_courses(ticker: str = Query(description="Валюта запроса")):
    result = await end_courses(ticker)
    return result

@courses_router.get(DATE_COURSES)
async def get_all_courses(ticker: str = Query(description="Валюта запроса"),
                          date_start: datetime = Query(default=None, description="Дата начала выборки"),
                          date_end: datetime = Query(default=None, description="Дата окончания выборки")):
    result = await date_courses(ticker, date_start, date_end)
    return result