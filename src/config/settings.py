import os

from dotenv import load_dotenv
load_dotenv()

class Config:
    #db
    PSQL_DB_USER = os.environ.get("PSQL_DB_USER")
    PSQL_DB_PASSWORD = os.environ.get("PSQL_DB_PASSWORD")
    PSQL_DB_NAME= os.environ.get("PSQL_DB_NAME")
    PSQL_DB_HOST = os.environ.get("PSQL_DB_HOST")
    PSQL_DB_PORT = os.environ.get("PSQL_DB_PORT")

    #app
    HOST = os.environ.get("HOST")
    PORT = os.environ.get("PORT")

    #proxy
    DERIBIT_API = os.environ.get("DERIBIT_API")