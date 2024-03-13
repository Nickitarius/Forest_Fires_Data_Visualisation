from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from geoalchemy2 import Geometry
from typing import List
from config.db import DB


class ForestQuarter(DB):
    """Лесной квартал."""
    __tablename__ = "forest_quarters"
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(nullable=False)
    geom: Mapped[Geometry] = mapped_column(
        Geometry('MULTIPOLYGON'), nullable=False)

    # Many-to-One nearest_meteo_station
    nearest_meteo_station_id: Mapped[int] = mapped_column(ForeignKey("meteo_stations.id"))
    nearest_meteo_station: Mapped["MeteoStation"] = relationship(
        back_populates="forest_quarters_nearest")

    # Many-to-Many MeteoStation
    meteo_stations_all: Mapped[List["ForestQuartersMeteoStations"]] = relationship(
        back_populates="forest_quarter")
