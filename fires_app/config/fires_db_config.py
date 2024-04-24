from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Table, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .fires_db import FiresDB

# ПОРЯДОК ИМПОРТА ВАЖЕН!!!
# При его нарушении связи в БД рушатся.
from fires_app.models.weather_event import WeatherEvent
from fires_app.models.meteo_record import MeteoRecord
from fires_app.models.meteo_station import MeteoStation
from fires_app.models.forest_quarter import ForestQuarter
from fires_app.models.uch_forestry import UchForestry
from fires_app.models.dacha import Dacha
from fires_app.models.forest_seed_zoning_zone import ForestSeedZoningZone
from fires_app.models.foresst_zone import ForestZone
from fires_app.models.forestry import Forestry
from fires_app.models.fire_status import FireStatus
from fires_app.models.territory_type import TerritoryType
from fires_app.models.fire import Fire

# MySQL
# DB_DIALECT = "mysql"
# DB_ENGINE = "pymysql"
# DB_USERNAME = "root"
# DB_PASSWORD = ""
# DB_CHARSET = "utf8mb4"
# DB_NAME = "fire_risks_app"


# PostgreSQL
DB_DIALECT = "postgresql"
DB_ENGINE = "psycopg"
DB_USERNAME = "postgres"
DB_PASSWORD = "pass"
DB_NAME = "fires_app_test"

DB_HOST = "localhost"
DB_URL = (
    DB_DIALECT
    + "+"
    + DB_ENGINE
    + "://"
    + DB_USERNAME
    + ":"
    + DB_PASSWORD
    + "@"
    + DB_HOST
    + "/"
    + DB_NAME
    # + "?charset="
    # + DB_CHARSET
)

# class FiresDB(DeclarativeBase):
#     """База данных приложения."""


# Assotiation tables


# Many-to-Many association
weather_events_meteo_records = Table(
    "weather_events_meteo_records",
    FiresDB.metadata,
    Column("weather_event_id", ForeignKey("weather_events.id"), primary_key=True),
    Column("meteo_record_id", ForeignKey("meteo_records.id"), primary_key=True),
)

# Many-to-Many association
forest_quarters_meteo_stations = Table(
    "forest_quarters_meteo_stations",
    FiresDB.metadata,
    Column("forest_quarter_id", ForeignKey("forest_quarters.id"), primary_key=True),
    Column("meteo_station_id", ForeignKey("meteo_stations.id"), primary_key=True),
)

engine = create_engine(DB_URL, echo=True)
FiresDB.metadata.create_all(bind=engine)
db = SQLAlchemy(model_class=FiresDB)
# db.init_app(flask_app)

session_factory = sessionmaker(bind=engine)
