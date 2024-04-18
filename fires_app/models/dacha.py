from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from config.fires_db_config import FiresDB


class Dacha(FiresDB):
    """Лесная дача."""
    __tablename__ = "dachas"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_en: Mapped[Optional[str]] = mapped_column(
        String(50, collation="utf8mb4_general_ci"), nullable=True)
    name_ru: Mapped[str] = mapped_column(
        String(50, collation="utf8mb4_general_ci"), nullable=False)

    # Many-To-One uch_forestries
    uch_forestry_id: Mapped[int] = mapped_column(
        ForeignKey("uch_forestries.id"))
    uch_forestry: Mapped["UchForestry"] = relationship(back_populates="dachas")

    # One-to-Many forestr_quarters
    forest_quarters: Mapped[List["ForestQuarter"]
                            ] = relationship(back_populates="dacha")

    # One-to-One forest_seed_zoning_zones
    forest_seed_zoning_zone: Mapped[Optional["ForestSeedZoningZone"]] = relationship(
        back_populates="dacha")

    # Many-to-One forest_zones
    forest_zone_id: Mapped[Optional[int]] = mapped_column(ForeignKey("forest_zones.id"))
    forest_zone: Mapped[Optional["ForestZone"]] = relationship(back_populates="dachas")
