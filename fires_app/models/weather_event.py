from typing import List, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.fires_db_config import FiresDB


class WeatherEvent(FiresDB):
    """Погодное явление."""

    __tablename__ = "weather_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int] = mapped_column(nullable=False)
    description_ru: Mapped[str] = mapped_column(String(300), nullable=False)

    # Many-to-Many
    meteo_records: Mapped[List["MeteoRecord"]] = relationship(
        secondary="weather_events_meteo_records", back_populates="weather_events"
    )

    # Many-to-One weather_event_types
    weather_event_type_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("weather_event_types.id")
    )
    weather_event_type: Mapped[Optional["WeatherEventType"]] = relationship(
        back_populates="weather_events"
    )
