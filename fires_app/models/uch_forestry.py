from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.fires_db_config import FiresDB


class UchForestry(FiresDB):
    __tablename__ = "uch_forestries"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_en: Mapped[str] = mapped_column(
        String(
            50,
            # collation="utf8mb4_general_ci"
        )
    )
    name_ru: Mapped[str] = mapped_column(
        String(
            50,
            #    collation="utf8mb4_general_ci"
        ),
        nullable=False,
    )

    # One-to-Many forest_quarter
    forest_quarters: Mapped[List["ForestQuarter"]] = relationship(
        back_populates="uch_forestry"
    )

    # One-to-Many dachas
    dachas: Mapped[List["Dacha"]] = relationship(back_populates="uch_forestry")

    # Many-to-One forestries
    forestry_id: Mapped[int] = mapped_column(ForeignKey("forestries.id"))
    forestry: Mapped["Forestry"] = relationship(back_populates="uch_forestries")
