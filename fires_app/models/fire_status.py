from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from ..config.fires_db_config import FiresDB


class FireStatus(FiresDB):
    """Статус пожара."""

    __tablename__ = "fire_statuses"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(20, collation="utf8mb4_general_ci"), nullable=False
    )

    # One-to-Many fires
    fires: Mapped[List["Fire"]] = relationship(back_populates="fire_status")
