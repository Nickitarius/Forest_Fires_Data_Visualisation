from typing import List, Optional

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.fires_db_config import FiresDB


class GeoPoint(FiresDB):
    """Точки на карте, к которым привзяаны свойства ландшафта."""

    __tablename__ = "geo_points"
    id: Mapped[int] = mapped_column(primary_key=True)

    dist_to_river: Mapped[float] = mapped_column()
    dist_to_road: Mapped[float] = mapped_column()
    dist_to_set: Mapped[float] = mapped_column()
    elevation: Mapped[float] = mapped_column()
    aspect: Mapped[float] = mapped_column()
    slope: Mapped[float] = mapped_column()
    vegetation: Mapped[float] = mapped_column()

    coords: Mapped[Geometry] = mapped_column(Geometry("POINT"), nullable=False)

    # Many-to-One MeteoStation
    # Ближайшкая метеостанция
    nearest_meteo_station_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("meteo_stations.id")
    )
    nearest_meteo_station: Mapped[Optional["MeteoStation"]] = relationship(
        back_populates="geo_points_nearest"
    )

    # One-to-Many RiskForecast
    risk_forecasts: Mapped[List["RiskForecast"]] = relationship(
        back_populates="geo_point"
    )

    # WW_code не нужен, он получается из таблицы с записями о погоде
    # для соответствующей метеостанции и даты

    # class_cbr =
