from infrastructure.loggers.create_logger import logger #todo разобраться с импортом
from config.settings import Config
import asyncpg
from asyncpg.pool import Pool


class JobDb():
    '''Класс реализации работы базы данных'''
    __pool = dict()

    def __init__(self):
        self.user: str = Config.PSQL_DB_USER
        self.password: str = Config.PSQL_DB_PASSWORD
        self.db_name: str = Config.PSQL_DB_NAME
        self.host: str = Config.PSQL_DB_HOST
        self.port: str = Config.PSQL_DB_PORT
        self.pool = None
        self.cursor = None

    async def __aenter__(self) -> Pool:
        if self.pool:
            return self.pool
        self.cursor = await asyncpg.connect(user=self.user,
                                            password=self.password,
                                            database=self.db_name,
                                            host=self.host,
                                            port=self.port)
        return self.cursor

    async def __aexit__(self, exc_type, exc, tb):
        if self.cursor:
            await self.cursor.close()

    async def create_pool(self):
        try:
            name = 'root'
            self.pool: Pool = await asyncpg.create_pool(user=self.user,
                                                        password=self.password,
                                                        database=self.db_name,
                                                        host=self.host,
                                                        port=self.port)
            JobDb.__pool[name] = self.pool
            logger.info(f"База данных успешно подключена")
        except Exception as e:
            logger.exception(f"При подключении базы данных получено исключение {e}")

    async def close_pool(self):
        try:
            for name in JobDb.__pool.keys():
                await JobDb.__pool[name].close()
            logger.info(f"База данных успешно отключена")
        except Exception as e:
            logger.exception(f"При отключении базы данных получено исключение {e}")
