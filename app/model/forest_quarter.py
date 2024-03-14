from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from typing import List, Optional
from config.db import DB


class ForestQuarter(DB):
    """Лесной квартал."""
    __tablename__ = "forest_quarters"
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(nullable=False)
    geom: Mapped[Geometry] = mapped_column(
        Geometry('MULTIPOLYGON'), nullable=False)

    # Many-to-One nearest_meteo_station
    nearest_meteo_station_id: Mapped[int] = mapped_column(
        ForeignKey("meteo_stations.id"))
    nearest_meteo_station: Mapped["MeteoStation"] = relationship(
        back_populates="forest_quarters_nearest")

    # Many-to-Many meteostations
    meteo_stations: Mapped[List["MeteoStation"]] = relationship(
        secondary="forest_quarters_meteo_stations",
        back_populates="forest_quarters")

    # Many-to-One uch_forestries
    uch_forestry_id: Mapped[int] = mapped_column(
        ForeignKey("uch_forestries.id"))
    uch_forestry: Mapped["UchForestry"] = relationship(
        back_populates="forest_quarters")

    # Many-to-One dachas
    dacha_id: Mapped[Optional[int]] = mapped_column( ForeignKey("dachas.id"))
    dacha: Mapped[Optional["Dacha"]] = relationship(back_populates="forest_quarters")
