"""Основное приложение. """
import flask

from fires_app.config.fires_db_config import db, DB_URL

MY_DATA_PATH = '../MY data/'

# flask_app = flask.Flask(__name__)

# # flask_app.debug = True

# flask_app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
# db.init_app(flask_app)

print("init")
