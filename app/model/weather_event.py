from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from config.db import DB


class WeatherEvent(DB):
    __tablename__ = "weather_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int] = mapped_column(nullable=False)
    description_ru: Mapped[str] = mapped_column(String(20), nullable=False)

    # Many-to-Many
    meteo_records: Mapped[List["WeatherEventsMeteoRecords"]] = relationship(
        back_populates="weather_event")
