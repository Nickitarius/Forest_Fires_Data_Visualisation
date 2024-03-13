from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from config.db import DB


class Dacha(DB):
    """Лесная дача."""
    __tablename__ = "dachas"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_en: Mapped[str] = mapped_column(String(50))
    name_ru: Mapped[str] = mapped_column(String(50), nullable=False)

    # Many-To-One uch_forestries
    uch_forestry_id: Mapped[int] = mapped_column(ForeignKey("uch_forestries.id"))
    uch_forestry: Mapped["UchForestry"] = relationship(back_populates="children")

    #One-to-Many forestr_quarters
    forest_quarters: Mapped[List["ForestQuarter"]] = relationship(back_populates="dacha")

    #One-to-One forest_seed_zoning_zones
    forest_seed_zoning_zone: Mapped["ForestSeedZoningZone"] = relationship(back_populates="dacha")
