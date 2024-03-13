from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from config.db import DB


class WeatherEvent(DB):
    __tablename__ = "weather_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int] = mapped_column(nullable=False)
    description_ru: Mapped[str] = mapped_column(String(20), nullable=False)

    meteo_records: Mapped[List["WeatherEventsMeteoRecords"]] = relationship()
    # def __repr__(self) -> str:
    #     return f"Weather event(id={self.id!r}, code={self.code!r}, description_ru={self.description_ru!r})"
