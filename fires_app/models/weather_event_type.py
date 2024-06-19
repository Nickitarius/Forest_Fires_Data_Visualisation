from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.fires_db_config import FiresDB


class WeatherEventType(FiresDB):
    """Тип погодного явления."""

    __tablename__ = "weather_event_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_ru: Mapped[str] = mapped_column(String(20), nullable=False)

    # One-to-Many weather_events
    weather_events: Mapped[List["WeatherEvent"]] = relationship(
        back_populates="weather_event_type"
    )
