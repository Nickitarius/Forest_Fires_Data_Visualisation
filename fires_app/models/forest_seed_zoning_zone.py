from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..config.fires_db_config import FiresDB


class ForestSeedZoningZone(FiresDB):
    """Зона лесосеменного районирования."""

    __tablename__ = "forest_seed_zoning_zones"
    id: Mapped[int] = mapped_column(primary_key=True)
    pine: Mapped[int] = mapped_column(nullable=False)  # Сосна
    spruce: Mapped[int] = mapped_column(nullable=False)  # Ель
    larch: Mapped[int] = mapped_column(nullable=False)  # Лиственница
    cedar: Mapped[int] = mapped_column(nullable=False)  # Кедр

    # One-to-One dacha
    dacha_id: Mapped[int] = mapped_column(ForeignKey("dachas.id"))
    dacha: Mapped["Dacha"] = relationship(back_populates="forest_seed_zoning_zone")
