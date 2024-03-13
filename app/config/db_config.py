from typing import List, Optional
from sqlalchemy import ForeignKey, String, MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
# from app import model
from config.db import DB
from model.weather_event import WeatherEvent


DB_DIALECT = "mysql"
DB_ENGINE = "pymysql"
DB_USERNAME = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "test"
DB_CHARSET = "utf8mb4"


# class DB(DeclarativeBase):
#     """База данных приложения."""
#     pass

# DB = declarat

db_url = DB_DIALECT + "+" + DB_ENGINE + "://" + DB_USERNAME + ":" + \
    DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME + "?charset=" + DB_CHARSET
engine = create_engine(db_url, echo=True)
session_factory = sessionmaker(bind=engine)


def get_session_factory():
    # from app.model.weather_event import WeatherEvent

    # create_tables()
    DB.metadata.create_all(bind=engine)
    print(f'metadata: {DB.metadata.tables}')
    return session_factory()


# from app.model.weather_event import WeatherEvent

# def create_session():
#     db_url = DB_DIALECT + "+" + DB_ENGINE + "://" + DB_USERNAME + ":" + \
#         DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME + "?charset=" + DB_CHARSET
#     engine = create_engine(db_url, echo=True)

#     db.DB.metadata.create_all(bind=engine)
#     print(f'metadata: {db.DB.metadata}')
# DB = DeclarativeBase()

# def create_tables():
#     """Создаёт таблицы в БД. Вынесено в отдельную функцию т.к. импорт вне функции приводит к ошибке 'circular import'."""
#     from app.model.weather_event import WeatherEvent
#     DB.metadata.create_all(bind=engine)
#     print(f'metadata: {DB.metadata}')

# # from app.model.weather_event import WeatherEvent
# def create_DB():
#     # from app.model.weather_event import WeatherEvent
#     db_url = DB_DIALECT + "+" + DB_ENGINE + "://" + DB_USERNAME + ":" + \
#         DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME + "?charset=" + DB_CHARSET
#     engine = create_engine(db_url, echo=True)
#     # create_tables()
#     DB.metadata.create_all(bind=engine)
#     print(f'metadata: {DB.metadata}')
