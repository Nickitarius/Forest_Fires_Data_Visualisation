import datetime
from typing import Optional

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.fires_db_config import FiresDB


class RiskForecast(FiresDB):
    """Оценки рисков лесных пожаров в определённой точке."""

    __tablename__ = "risk_forecasts"
    id: Mapped[int] = mapped_column(primary_key=True)

    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    risk_class_value: Mapped[float] = mapped_column(nullable=False)

    # Many-to-One GeoPoint
    geo_point_id: Mapped[Optional[int]] = mapped_column(ForeignKey("geo_points.id"))
    geo_point: Mapped[Optional["GeoPoint"]] = relationship(
        back_populates="risk_forecasts"
    )
