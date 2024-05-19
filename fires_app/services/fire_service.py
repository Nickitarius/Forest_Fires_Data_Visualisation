"""Функции для работы с таблицей Fire в БД."""

import sqlalchemy
from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload, load_only

from fires_app import db, flask_app
from fires_app.models.fire import Fire
from fires_app.models.fire_status import FireStatus


def set_forestries_condition(query, forestries):
    # Если есть список лесничеств
    if isinstance(forestries, list):
        query = query.where(Fire.forestry_id.in_(forestries))
    # Если лесничество есть, и оно одно
    else:
        query = query.where(Fire.forestry_id == forestries)
    return query


def set_area_condition(query, statuses):
    # Если есть список лесничеств
    if isinstance(statuses, list):
        query = query.where(Fire.fire_status_id.in_(statuses))
    # Если статус есть, и он один
    else:
        query = query.where(Fire.fire_status_id == statuses)

    return query


def set_territory_type_condition(query, territory_types):
    # Если есть список территорий
    if isinstance(territory_types, list):
        # Если среди типов территорий есть вариант "Нет"
        if 0 in territory_types:
            query = query.where(
                or_(
                    Fire.territory_type_id.in_(territory_types),
                    Fire.territory_type_id.is_(None),
                )
            )
        else:
            query = query.where(Fire.territory_type_id.in_(territory_types))
    # Если тип территории есть, и он один
    else:
        query = query.where(Fire.territory_type_id == territory_types)

    return query


def get_fires_limited_data(
    date_start,
    date_end,
    forestries=None,
    statuses=None,
    fire_area_min=0,
    fire_area_max=1000,
    territory_types=None,
):
    """Получает пожары из БД."""
    with flask_app.app_context():
        query = db.select(Fire)
        load_only_option = load_only(
            Fire.id, Fire.coords, Fire.date_start, Fire.date_end, Fire.code
        )
        joined_load_option = joinedload(Fire.fire_status)
        query = query.options(load_only_option)
        query = query.options(joined_load_option)

        # Период действия пожара пересекатся с заданным периодом времени
        dates_fit_condition = and_(
            sqlalchemy.cast(Fire.date_start, sqlalchemy.Date)
            <= sqlalchemy.cast(date_end, sqlalchemy.Date),
            sqlalchemy.cast(date_start, sqlalchemy.Date)
            <= sqlalchemy.cast(Fire.date_end, sqlalchemy.Date),
        )
        area_condition = and_(
            Fire.area_all >= fire_area_min, Fire.area_all <= fire_area_max
        )

        query = query.where(dates_fit_condition)
        query = query.where(area_condition)
        query = set_area_condition(query, statuses)
        query = set_forestries_condition(query, forestries)
        query = set_territory_type_condition(query, territory_types)

        res = db.session.execute(query).scalars().all()
        return res


def get_fire(id):
    """Получает пожар из БД."""
    with flask_app.app_context():
        query = db.select(Fire).where(Fire.id == id)
        query = query.options(
            joinedload(Fire.fire_status),
            joinedload(Fire.forestry),
            joinedload(Fire.territory_type),
        )
        res = db.session.execute(query).scalar_one()
        return res
