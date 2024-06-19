from typing import List, Optional

from geoalchemy2 import Geometry

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.fires_db_config import FiresDB


class MeteoStation(FiresDB):
    """Метеорологическая станция."""

    __tablename__ = "meteo_stations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    code: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
    coords: Mapped[Geometry] = mapped_column(Geometry("POINT"), nullable=False)

    # One-to-Many MeteoRecord
    meteo_records: Mapped[List["MeteoRecord"]] = relationship(
        back_populates="meteo_station"
    )

    # Many-to-Many ForestQuarters
    forest_quarters: Mapped[List["ForestQuarter"]] = relationship(
        secondary="forest_quarters_meteo_stations", back_populates="meteo_stations"
    )

    # One-to-Many ForestQuarter
    forest_quarters_nearest: Mapped[List["ForestQuarter"]] = relationship(
        back_populates="nearest_meteo_station"
    )

    # One-to-Many GeoPoint
    geo_points_nearest: Mapped[List["GeoPoint"]] = relationship(
        back_populates="nearest_meteo_station"
    )
