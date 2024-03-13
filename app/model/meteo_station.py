from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from config.db import DB
from geoalchemy2 import Geometry as GAGeometry


class MeteoStation(DB):
    __tablename__ = "meteo_stations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    coords: Mapped[GAGeometry] = mapped_column(
        GAGeometry('POINT'), nullable=False)

    meteo_record: Mapped[List["MeteoRecord"]] = relationship(
        back_populates="meteo_record")
