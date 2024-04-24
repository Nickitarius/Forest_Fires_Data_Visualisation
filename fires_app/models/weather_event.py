from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.fires_db_config import FiresDB


class WeatherEvent(FiresDB):
    __tablename__ = "weather_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int] = mapped_column(nullable=False)
    description_ru: Mapped[str] = mapped_column(
        # String(20, collation="utf8mb4_general_ci"), nullable=False
        String(20),
        nullable=False,
    )

    # Many-to-Many
    meteo_records: Mapped[List["MeteoRecord"]] = relationship(
        secondary="weather_events_meteo_records", back_populates="weather_events"
    )
