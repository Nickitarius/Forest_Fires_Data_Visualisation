"""Данные конфигурации приложения."""
# Импорт производится для fires_db_config именно здесь, так как иначе будет рекурсивный импорт

# from fires_app.models import *

# ПОРЯДОК ИМПОРТА ВАЖЕН!!!
# При его нарушении связи в БД рушатся.
from fires_app.models.weather_event import WeatherEvent
from fires_app.models.meteo_record import MeteoRecord
from fires_app.models.meteo_station import MeteoStation
from fires_app.models.forest_quarter import ForestQuarter
from fires_app.models.uch_forestry import UchForestry
from fires_app.models.dacha import Dacha
from fires_app.models.forest_seed_zoning_zone import ForestSeedZoningZone
from fires_app.models.foresst_zone import ForestZone
from fires_app.models.forestry import Forestry
from fires_app.models.fire_status import FireStatus
from fires_app.models.territory_type import TerritoryType
from fires_app.models.fire import Fire
