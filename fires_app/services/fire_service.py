"""Функции для работы с таблицей Fire в БД."""

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy.orm import joinedload, load_only

from fires_app import db, flask_app
from fires_app.models.fire import Fire
from fires_app.models.fire_status import FireStatus


def set_forestries_condition(query, forestries):
    print(forestries)
    # Если есть список лесничеств
    if isinstance(forestries, list):
        # Если список лесничеств не пустой
        forestries_condition = and_(
            Fire.forestry_id.in_(forestries),
        )
    # Если лесничество есть, и оно одно
    else:
        forestries_condition = and_(
            Fire.forestry_id == forestries,
        )

    query = query.where(forestries_condition)

    return query


def set_area_condition(query, statuses):
    if statuses is not None:
        # Если есть список лесничеств
        is_list = isinstance(statuses, list)
        if is_list and len(statuses) > 0:
            # Если список лесничеств не пустой
            statuses_condition = and_(
                Fire.fire_status_id.in_(statuses),
            )
            query = query.where(statuses_condition)
        # Если лесничество есть, и оно одно
        elif not is_list:
            statuses_condition = and_(
                Fire.fire_status_id == statuses,
            )
            query = query.where(statuses_condition)

    return query


def get_fires_limited_data(
    date_start,
    date_end,
    forestries=None,
    statuses=None,
    fire_area_min=0,
    fire_area_max=1000,
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
