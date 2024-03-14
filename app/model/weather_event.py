from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from config.db import DB


class WeatherEvent(DB):
    __tablename__ = "weather_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int] = mapped_column(nullable=False)
    description_ru: Mapped[str] = mapped_column(
        String(20, collation="utf8mb4_general_ci"), nullable=False)

    # Many-to-Many
    meteo_records: Mapped[List["MeteoRecord"]] = relationship(
        secondary="weather_events_meteo_records",
        back_populates="weather_events")
