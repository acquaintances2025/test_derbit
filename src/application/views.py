import json

from datetime import datetime, date

from fastapi.responses import JSONResponse


from infrastructure import JobDb, GET_RANGE_COURSES, GET_ALL_COURSES, GET_END_COURSES
from infrastructure.loggers.create_logger import logger



class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


async def all_courses(ticker: str) -> JSONResponse:
    try:
        async with JobDb() as connector:
            courses = await connector.fetch(GET_ALL_COURSES, ticker)
            result_list = [
                {
                    **course,
                    'last_price': f"{float(course['last_price']):,.2f}",
                    'best_ask_price': f"{float(course['best_ask_price']):,.2f}",
                    'best_bid_price': f"{float(course['best_bid_price']):,.2f}"
                }
                for course in courses
            ]
            logger.info(f"Общий список курсов по параметру {ticker} отправлен.")
            return JSONResponse(status_code=200,
                                content=json.loads(json.dumps({"answer": result_list}, cls=DateTimeEncoder)))
    except Exception as e:
        logger.error(f"В процессе получения списка курсов произошла ошибка {e}")
        return JSONResponse(status_code=500, content={"message": "Ошибка исполнения процесса."})


async def end_courses(ticker: str) -> JSONResponse:
    try:
        async with JobDb() as connector:
            courses = await connector.fetch(GET_END_COURSES, ticker)
            result_list = [
                {
                    **course,
                    'last_price': f"{float(course['last_price']):,.2f}",
                    'best_ask_price': f"{float(course['best_ask_price']):,.2f}",
                    'best_bid_price': f"{float(course['best_bid_price']):,.2f}"
                }
                for course in courses
            ]
        logger.info(f"Крайний курс по параметру {ticker} отправлен.")
        return JSONResponse(status_code=200, content=json.loads(json.dumps({"answer": result_list}, cls=DateTimeEncoder)))
    except Exception as e:
        logger.error(f"В процессе получения списка курсов произошла ошибка {e}")
        return JSONResponse(status_code=500, content={"message": "Ошибка исполнения процесса."})

async def date_courses(ticker: str,date_start: datetime, date_end: datetime) -> JSONResponse:
    try:
        async with JobDb() as connector:
            courses = await connector.fetch(GET_RANGE_COURSES, ticker, date_start, date_end)
            result_list = [
                {
                    **course,
                    'last_price': f"{float(course['last_price']):,.2f}",
                    'best_ask_price': f"{float(course['best_ask_price']):,.2f}",
                    'best_bid_price': f"{float(course['best_bid_price']):,.2f}"
                }
                for course in courses
            ]
        logger.info(f"Список курсов по параметру {ticker} в диапазоне дат от {date_start} до {date_end} отправлен.")
        return JSONResponse(status_code=200, content=json.loads(json.dumps({"answer": result_list}, cls=DateTimeEncoder)))
    except Exception as e:
        logger.error(f"В процессе получения списка курсов произошла ошибка {e}")
        return JSONResponse(status_code=500, content={"message": "Ошибка исполнения процесса."})