import datetime
from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from config.fires_db_config import FiresDB


class MeteoRecord(FiresDB):
    """Усреднённые погодные показатели за день. """
    __tablename__ = "meteo_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    precipitation_mm: Mapped[float] = mapped_column(nullable=False)
    temp_celsius: Mapped[float] = mapped_column(nullable=False)
    wind_speed_ms: Mapped[float] = mapped_column(nullable=False)
    atm_pres_mmhg: Mapped[float] = mapped_column(nullable=False)
    hor_visibility_km: Mapped[float] = mapped_column(nullable=False)
    rel_wetness_perc: Mapped[float] = mapped_column(nullable=False)

    # Many-to-One meteo_stations
    meteo_station_id: Mapped[int] = mapped_column(
        ForeignKey("meteo_stations.id"), nullable=False)
    meteo_station: Mapped["MeteoStation"] = relationship(
        back_populates="meteo_records")

    # Many-to-Many WeatherEvents
    weather_events: Mapped[List["WeatherEvent"]] = relationship(
        secondary="weather_events_meteo_records",
        back_populates="meteo_records")
