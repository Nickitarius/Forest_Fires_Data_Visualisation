from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from config.db import DB


class ForestZone(DB):
    """Лесная зона. """
    __tablename__ = "forest_zones"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    #One-to-Many dachas
    dachas: Mapped[List["Dacha"]] = relationship(back_populates="forest_zone")
