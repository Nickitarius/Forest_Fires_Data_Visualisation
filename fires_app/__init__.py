"""Основное приложение. """

import flask

from .config.fires_db_config import DB_URL, db

DATA_PATH = "../data/"

flask_app = flask.Flask(__name__)
flask_app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL

# with flask_app.app_context():
db.init_app(flask_app)
