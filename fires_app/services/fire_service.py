"""Функции для работы с таблицей Fire в БД."""

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
        print(forestries)
        if forestries is not None:
            # Если есть список лесничеств и он не пустой
            if isinstance(forestries, list):
                if len(forestries) > 0:
                    and_expression = and_(
                        Fire.date_start <= date_end,
                        date_start <= Fire.date_end,
                        Fire.forestry_id.in_(forestries),
                    )
                else:
                    and_expression = and_(
                        Fire.date_start <= date_end, date_start <= Fire.date_end
                    )
            # Если лесничество есть, и оно одно
            else:
                and_expression = and_(
                    Fire.date_start <= date_end,
                    date_start <= Fire.date_end,
                    Fire.forestry_id == forestries,
                )
        # Если лесничества не выбраны, то возвращаем все лесничества сразу
        else:
            and_expression = and_(
                Fire.date_start <= date_end, date_start <= Fire.date_end
            )

        query = db.select(Fire).where(and_expression)
        load_only_option = load_only(
            Fire.id, Fire.coords, Fire.date_start, Fire.date_end, Fire.code
        )
        # query = query.where()

        joined_load_option = joinedload(Fire.fire_status)
        query = query.options(load_only_option, joined_load_option)
        res = db.session.execute(query).scalars().all()
        return res


def get_fire(id):
    """Получает пожар из БД."""
    with flask_app.app_context():
        res = db.session.execute(db.get_or_404(Fire, id))
        return res
