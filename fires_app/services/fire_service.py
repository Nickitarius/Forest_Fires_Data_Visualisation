from fires_app import db, flask_app
from fires_app.models.fire import Fire


def get_fires():
    """Получает пожары из БД. """
    with flask_app.app_context():
        res = db.session.execute(db.select(Fire)).scalars().all()
        return res
