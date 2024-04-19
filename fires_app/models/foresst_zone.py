from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from ..config.fires_db_config import FiresDB


class ForestZone(FiresDB):
    """Лесная зона. """
    __tablename__ = "forest_zones"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(20, collation="utf8mb4_general_ci"), nullable=False)

    # One-to-Many dachas
    dachas: Mapped[List["Dacha"]] = relationship(back_populates="forest_zone")
