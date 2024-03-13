from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from config.db import DB


class UchForestry(DB):
    __tablename__ = "uch_forestries"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_en: Mapped[str] = mapped_column(String(50), nullable=False)
    name_ru: Mapped[str] = mapped_column(String(50), nullable=False)

    # One-to-Many forest_quarter
    forest_quarters: Mapped[List["ForestQuarter"]
                            ] = relationship(back_populates="uch_forestry")

    # One-to-Many dachas
    dachas: Mapped[List["Dacha"]] = relationship(back_populates="uch_forestry")
