from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from config.db import DB
from geoalchemy2 import Geometry as Geometry


class MeteoStation(DB):
    __tablename__ = "meteo_stations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    coords: Mapped[Geometry] = mapped_column(
        Geometry('POINT'), nullable=False)

    # One-to-Many MeteoRecord
    meteo_record: Mapped[List["MeteoRecord"]] = relationship(
        back_populates="meteo_record")

    # Many-to-Many ForestQuarters
    forest_quarters: Mapped[List["ForestQuartersMeteoStations"]] = relationship(
        back_populates="nearest_meteo_station_id")

    # One-to-Many ForestQuarter
    forest_quarters_nearest: Mapped[List["ForestQuarter"]] = relationship(
        back_populates="nearest_meteo_station")
