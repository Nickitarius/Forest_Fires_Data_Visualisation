from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import DB


class WeatherEventsMeteoRecords(DB):
    __tablename__ = "weather_events_meteo_records"

    weather_event_id: Mapped[int] = mapped_column(
        ForeignKey("weather_events.id"), primary_key=True)
    meteo_record_id: Mapped[int] = mapped_column(
        ForeignKey("meteo_records.id"), primary_key=True)

    id: Mapped[int] = mapped_column(primary_key=True)

    meteo_record: Mapped["MeteoRecord"] = relationship(
        back_populates="weather_events")
    weather_event: Mapped["WeatherEvent"] = relationship(
        back_populates="meteo_records")
