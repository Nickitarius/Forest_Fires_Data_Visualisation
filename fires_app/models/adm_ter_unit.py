from typing import Optional

from geoalchemy2 import Geometry
from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.fires_db_config import FiresDB


class AdmTerUnit(FiresDB):
    """Административно-территориальное образование."""

    __tablename__ = "adm_ter_units"
    id: Mapped[int] = mapped_column(primary_key=True)

    name_ru: Mapped[str] = mapped_column(String(50), nullable=False)

    geom: Mapped[Geometry] = mapped_column(Geometry("MULTIPOLYGON"), nullable=False)

    # Many-to-One AdmTerUnitType
    adm_ter_unit_type_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("adm_ter_unit_types.id")
    )
    adm_ter_unit_type: Mapped[Optional["AdmTerUnitType"]] = relationship(
        back_populates="adm_ter_units"
    )
