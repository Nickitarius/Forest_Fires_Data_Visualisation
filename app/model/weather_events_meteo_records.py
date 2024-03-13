from typing import Optional
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from config.db import DB


class WeatherEventsMeteoRecords(DB):
    __tablename__ = "weather_events_meteo_records"
    weather_event: Mapped[int] = mapped_column(
        ForeignKey("weather_events.id"), primary_key=True)
    meteo_record: Mapped[int] = mapped_column(
        ForeignKey("meteo_records.id"), primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)