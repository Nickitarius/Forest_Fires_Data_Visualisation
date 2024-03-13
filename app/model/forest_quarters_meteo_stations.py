from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import DB


class ForestQuartersMeteoStations(DB):
    """Таблица связи Many-to-Many между лесными кварталами и метеостанциями, которые их покрывают."""
    __tablename__ = "forest_quarters_meteo_stations"

    forest_quarter_id: Mapped[int] = mapped_column(
        ForeignKey("forest_quarters.id"), primary_key=True)
    meteo_station_id: Mapped[int] = mapped_column(
        ForeignKey("meteo_stations.id"), primary_key=True)

    id: Mapped[int] = mapped_column(primary_key=True)

    forest_quarter: Mapped["ForestQuarter"] = relationship(back_populates="meteo_stations_all")
    meteo_station: Mapped["MeteoStations"] = relationship(back_populates="forest_quarters")
