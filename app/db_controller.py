from typing import List, Optional
from sqlalchemy import ForeignKey, String, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from model.weather_event import WeatherEvent


class DB(DeclarativeBase):
    pass


# metadata_obj = MetaData()
DB.metadata.create_all()

