import datetime
from typing import Optional

from geoalchemy2 import Geometry
from sqlalchemy import Boolean, Date, Double, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.fires_db_config import FiresDB


class Fire(FiresDB):
    __tablename__ = "fires"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(
        String(20, collation="utf8mb4_general_ci"), nullable=False
    )
    # Центр пожара
    coords: Mapped[Geometry] = mapped_column(Geometry("POINT"), nullable=False)
    date_start: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    date_end: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    is_forest: Mapped[bool] = mapped_column(Boolean, nullable=False)
    # geometry: Mapped[Geometry] = mapped_column(
    #     Geometry('MULTIPOLYGON'), nullable=False)

    area_all: Mapped[float] = mapped_column(Double, nullable=False)
    area_forest: Mapped[float] = mapped_column(Double, nullable=False)
    area_lesofond_all: Mapped[float] = mapped_column(Double, nullable=False)
    area_lesofond_forest: Mapped[float] = mapped_column(Double, nullable=False)
    area_union: Mapped[float] = mapped_column(Double, nullable=False)
    area_registr: Mapped[float] = mapped_column(Double, nullable=False)

    # Many-to-One forestries
    forestry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("forestries.id"))
    forestry: Mapped[Optional["Forestry"]] = relationship(back_populates="fires")

    # Many-to-one fire_statuses
    fire_status_id: Mapped[int] = mapped_column(ForeignKey("fire_statuses.id"))
    fire_status: Mapped["FireStatus"] = relationship(back_populates="fires")

    # status_change_date: Mapped[datetime.date] = mapped_column(
    #     Date, nullable=False)

    # Many-to-One territory_types
    territory_type_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("territory_types.id")
    )
    territory_type: Mapped[Optional["TerritoryType"]] = relationship(
        back_populates="fires"
    )
