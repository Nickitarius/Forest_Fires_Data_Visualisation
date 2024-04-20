"""Функции для работы с таблицей Fire в БД."""
from sqlalchemy import and_
from sqlalchemy.orm import joinedload, load_only
from fires_app import db, flask_app
from fires_app.models.fire import Fire


def get_fires(date_start, date_end):
    """Получает пожары из БД. """
    with flask_app.app_context():
        query = db.select(Fire).where(
            and_(Fire.date_start <= date_end, date_start <= Fire.date_end)
        )
        res = db.session.execute(query).scalars().all()
        return res


def get_fires_limited_data(date_start, date_end):
    """Получает пожары из БД. """
    with flask_app.app_context():
        query = db.select(Fire).where(
            and_(Fire.date_start <= date_end,
                 date_start <= Fire.date_end)).options(
                     load_only(Fire.id, Fire.coords, Fire.date_start,
                               Fire.date_end, Fire.code), joinedload(Fire.fire_status))
        res = db.session.execute(query).fetchall()
        return res


def get_fire(id):
    """Получает пожар из БД. """
    with flask_app.app_context():
        res = db.session.execute(db.get_or_404(Fire, id))
        return res
