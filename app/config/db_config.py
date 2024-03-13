from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.db import DB
# from model.weather_event import WeatherEvent

DB_DIALECT = "mysql"
DB_ENGINE = "pymysql"
DB_USERNAME = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "test"
DB_CHARSET = "utf8mb4"

db_url = DB_DIALECT + "+" + DB_ENGINE + "://" + DB_USERNAME + ":" + \
    DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME + "?charset=" + DB_CHARSET
engine = create_engine(db_url, echo=True)
session_factory = sessionmaker(bind=engine)


def get_session_factory():
    DB.metadata.create_all(bind=engine)
    print(f'metadata: {DB.metadata.tables}')
    return session_factory()
