"""Сервис для типов территорий в БД."""

from fires_app.models.territory_type import TerritoryType

from fires_app import db, flask_app


def get_all_territory_types():
    """Возвращает из БД все типы территорий."""
    with flask_app.app_context():
        query = db.Query(TerritoryType)
        res = db.session.execute(query).scalars().all()
        return res
