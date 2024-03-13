from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db_controller import DB


class WeatherEvent(DB):
    __tablename__ = "weather_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int] = mapped_column()
    description_ru: Mapped[str] = mapped_column(String(20))
