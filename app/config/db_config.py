from sqlalchemy import create_engine, Table, Column, ForeignKey
from sqlalchemy.orm import sessionmaker
from config.db import DB

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

# Many-to-Many association
weather_events_meteo_records = Table(
    "weather_events_meteo_records",
    DB.metadata,
    Column("weather_event_id", ForeignKey(
        "weather_events.id"), primary_key=True),
    Column("meteo_record_id", ForeignKey(
        "meteo_records.id"), primary_key=True),
)

# Many-to-Many association
forest_quarters_meteo_stations = Table(
    "forest_quarters_meteo_stations",
    DB.metadata,
    Column("forest_quarter_id", ForeignKey(
        "forest_quarters.id"), primary_key=True),
    Column("meteo_station_id", ForeignKey(
        "meteo_stations.id"), primary_key=True),
)


def get_session_factory():
    """Возвращает сессию БД."""
    session_factory = sessionmaker(bind=engine)
    DB.metadata.create_all(bind=engine)
    print(f'metadata: {DB.metadata.tables}')
    return session_factory()
