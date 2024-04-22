"""Содержит функции для взаимодействия с БД по классу Forestry."""

from fires_app import db, flask_app
from fires_app.models.forestry import Forestry


def get_all_forestries():
    """Возвращает из БД все лесничества."""
    with flask_app.app_context():
        query = db.Query(Forestry)
        res = db.session.execute(query).scalars().all()
        return res
