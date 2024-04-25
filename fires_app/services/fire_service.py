"""Функции для работы с таблицей Fire в БД."""

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy.orm import joinedload, load_only

from fires_app import db, flask_app
from fires_app.models.fire import Fire


def get_fires_by_dates_range(date_start, date_end):
    """Получает пожары из БД."""
    with flask_app.app_context():
        query = db.select(Fire).where(
            and_(Fire.date_start <= date_end, date_start <= Fire.date_end)
        )
        res = db.session.execute(query).scalars().all()
        return res


def get_fires_limited_data(date_start, date_end, forestries=None):
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
        query = query.where(dates_fit_condition)

        if forestries is not None:
            # Если есть список лесничеств
            if isinstance(forestries, list):  # and len(forestries) > 0:
                # Если список лесничеств не пустой
                if len(forestries) > 0:
                    forestries_condition = and_(
                        Fire.forestry_id.in_(forestries),
                    )
                    query = query.where(forestries_condition)

                # Если список лесничеств пустой
                else:
                    pass
            # forestries_condition = and_(
            #     Fire.date_start <= date_end, date_start <= Fire.date_end
            # )

            # Если лесничество есть, и оно одно
            else:
                forestries_condition = and_(
                    Fire.forestry_id == forestries,
                )
                query = query.where(forestries_condition)

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
        # query = query.options(joinedload(Fire.forestry))
        # query = query.options(joinedload(Fire.territory_type))
        res = db.session.execute(query).scalar_one()
        return res
