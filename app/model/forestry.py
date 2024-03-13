from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from config.db import DB


class Forestry(DB):
    __tablename__ = "forestries"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_en: Mapped[str] = mapped_column(String(50), nullable=False)
    name_ru: Mapped[str] = mapped_column(String(50), nullable=False)

    # One-to-Many uch_forestries
    uch_forestries: Mapped[List["UchForestry"]
                           ] = relationship(back_populates="forestry")

    # One-to-Many fires
    fires: Mapped[List["Fire"]] = relationship(back_populates="forestry")
