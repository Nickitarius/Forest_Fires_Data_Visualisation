from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.fires_db_config import FiresDB


class AdmTerUnitType(FiresDB):
    """Тип АТО."""

    __tablename__ = "adm_ter_unit_types"
    id: Mapped[int] = mapped_column(primary_key=True)

    name_ru: Mapped[str] = mapped_column(String(50), nullable=False)

    # One-to-Many AdmTerUnit
    adm_ter_units: Mapped[List["AdmTerUnit"]] = relationship(
        back_populates="adm_ter_unit_type"
    )
