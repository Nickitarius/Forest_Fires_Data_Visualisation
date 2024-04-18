"""Основное приложение. """

from flask_sqlalchemy import SQLAlchemy
import flask
import sys

from .config.fires_db_config import db, DB_URL

sys.path.append(".")

flask_app = flask.Flask(__name__)

# flask_app.debug = True

# fires_db_config.DB_URL  # db_url

flask_app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
db.init_app(flask_app)

MY_DATA_PATH = '../MY data/'

print("s")
