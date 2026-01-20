import httpx

from datetime import datetime

from sqlalchemy.dialects.postgresql.psycopg import logger

from infrastructure.proxy.proxy_client import DeribitClient
from infrastructure import JobDb, ADD_COURSES

async def add_db(name: str, last_price: float, best_bid_price: float, best_ask_price: float, date: datetime):
    async with JobDb() as connector:
        await connector.fetch(ADD_COURSES, name, last_price, best_bid_price, best_ask_price, date)
        return True

async def get_instruments(params: dict[str, str]) -> dict[str, str]:
    try:
        async with DeribitClient() as client:
            get_instrument = await client.request(
                "GET",
                "/public/get_instruments",
                params=params,
            )
            return get_instrument.json().get('result', [])
    except Exception as e:
        logger.error(f"В процессе поиска инструмента произошла ошибка {e}")


async def check_answer(instruments: dict[str: str],base :str, quote: str):
    try:
        btc_usd_instrument = None
        for instrument in instruments:
            if (instrument['base_currency'] == base and
                    instrument['quote_currency'] == quote and
                    instrument['kind'] == 'future'):
                logger.info(f"Найден инструмент: {instrument['instrument_name']} - {instrument['expiration_timestamp']}")
                btc_usd_instrument = instrument
                break
        return btc_usd_instrument
    except Exception as e:
        logger.error(f"В процессе проверки инструмента произошла ошибка {e}")


async def get_prise(params: str) -> dict[str, str] | None:
    try:
        async with DeribitClient() as client:
            ticker_data = await client.request(
                "GET",
                "/public/ticker",
                params={"instrument_name": params},
            )
            return ticker_data.json()
    except httpx.RequestError as e:
        logger.error(f"Ошибка запроса к параметру {params}: {e}")
        return None

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP ошибка для {params}: {e.response.status_code} - {e.response.text}")
        return None

async def courses():
    try:
        instrument_bts_usd = await get_instruments({"currency": "BTC", "kind": "future"})
        check_instrument_bts_usd = await check_answer(instrument_bts_usd, "BTC", "USD")
        prise_bts_usd = await get_prise(check_instrument_bts_usd["instrument_name"])
        if prise_bts_usd is not None:
            if prise_bts_usd and 'result' in prise_bts_usd:
                date_bts_usd = prise_bts_usd['result']
                await add_db("btc_usd", float(date_bts_usd["last_price"]), float(date_bts_usd["best_bid_price"]), float(date_bts_usd["best_ask_price"]), datetime.utcfromtimestamp(date_bts_usd['timestamp'] / 1000))
                logger.info(f"Курсы btc_usd и успешно записаны в базу данных")
    except Exception as e:
        logger.error(f"В работе по поиску курсов btc_usd и записи его в базу данных произошла ошибка {e}")

    try:
        instrument_eth_usd = await get_instruments({"currency": "ETH", "kind": "future"})
        check_instrument_eth_usd = await check_answer(instrument_eth_usd, "ETH", "USD")
        prise_eth_usd = await get_prise(check_instrument_eth_usd['instrument_name'])
        if prise_eth_usd is not None:
            if prise_eth_usd and 'result' in prise_eth_usd:
                date_eth_usd = prise_eth_usd['result']
                await add_db("eth_usd", float(date_eth_usd["last_price"]), float(date_eth_usd["best_bid_price"]), float(date_eth_usd["best_ask_price"]), datetime.utcfromtimestamp(date_eth_usd['timestamp'] / 1000))
                logger.info(f"Курсы eth_usd и успешно записаны в базу данных")
    except Exception as e:
        logger.error(f"В работы по поиску курсов eth_usd и записи его в базу данных произошла ошибка {e}")

