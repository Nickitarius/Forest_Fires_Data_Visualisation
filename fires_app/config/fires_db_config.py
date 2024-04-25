from flask_sqlalchemy import SQLAlchemy as Flask_SQLAlchemy
from sqlalchemy import Column, ForeignKey, Table, create_engine
from sqlalchemy.orm import sessionmaker

from .fires_db import FiresDB

# ПОРЯДОК ИМПОРТА ВАЖЕН!!!
# При его нарушении связи в БД рушатся.
from ..models.weather_event import WeatherEvent
from ..models.meteo_record import MeteoRecord
from ..models.meteo_station import MeteoStation
from ..models.forest_quarter import ForestQuarter
from ..models.uch_forestry import UchForestry
from ..models.dacha import Dacha
from ..models.forest_seed_zoning_zone import ForestSeedZoningZone
from ..models.foresst_zone import ForestZone
from ..models.forestry import Forestry
from ..models.fire_status import FireStatus
from ..models.territory_type import TerritoryType
from ..models.fire import Fire
from ..models.weather_event_type import WeatherEventType

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

__engine = create_engine(DB_URL, echo=False)#echo=True)
FiresDB.metadata.create_all(bind=__engine)
db = Flask_SQLAlchemy(model_class=FiresDB)

session_factory = sessionmaker(bind=__engine)
