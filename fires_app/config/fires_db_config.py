from sqlalchemy import create_engine, Table, Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
# from config.fires_db import FiresDB
# from fires_app import flask_app

DB_DIALECT = "mysql"
DB_ENGINE = "pymysql"
DB_USERNAME = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "weather_risks_app"
DB_CHARSET = "utf8mb4"
DB_URL = DB_DIALECT + "+" + DB_ENGINE + "://" + DB_USERNAME + ":" + \
    DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME + "?charset=" + DB_CHARSET


class FiresDB(DeclarativeBase):
    """База данных приложения."""


# Many-to-Many association
weather_events_meteo_records = Table(
    "weather_events_meteo_records",
    FiresDB.metadata,
    Column("weather_event_id", ForeignKey(
        "weather_events.id"), primary_key=True),
    Column("meteo_record_id", ForeignKey(
        "meteo_records.id"), primary_key=True),
)

# Many-to-Many association
forest_quarters_meteo_stations = Table(
    "forest_quarters_meteo_stations",
    FiresDB.metadata,
    Column("forest_quarter_id", ForeignKey(
        "forest_quarters.id"), primary_key=True),
    Column("meteo_station_id", ForeignKey(
        "meteo_stations.id"), primary_key=True),
)

engine = create_engine(DB_URL, echo=True)
FiresDB.metadata.create_all(bind=engine)
db = SQLAlchemy(model_class=FiresDB)
# db.init_app(flask_app)

# session_factory = sessionmaker(bind=engine)

# def get_session():
#     """Возвращает сессию БД."""
#     return session_factory()


# def get_db():
#     """Возвращает экземпляр ДБ."""
#     db = SQLAlchemy(model_class=FiresDB)
#     # # app = Flask(__name__)
#     # # with app.app_context():
#     # #     db.create_all()
#     return db
#     # return FiresDB
