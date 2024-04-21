from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.fires_db_config import FiresDB


class TerritoryType(FiresDB):
    """Тип территории, подвергнувшейся пожару."""

    __tablename__ = "territory_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(20, collation="utf8mb4_general_ci"), nullable=False
    )

    # One-to-Many fires
    fires: Mapped[List["Fire"]] = relationship(back_populates="territory_type")
