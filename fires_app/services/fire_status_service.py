from sqlalchemy import and_
from sqlalchemy.orm import joinedload, load_only

from fires_app import db, flask_app
from fires_app.models.fire_status import FireStatus


def get_all_fire_statuses():
    """Получает пожары из БД."""
    with flask_app.app_context():
        query = db.select(FireStatus)
        res = db.session.execute(query).scalars().all()
        return res
