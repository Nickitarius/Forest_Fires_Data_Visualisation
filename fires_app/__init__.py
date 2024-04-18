"""Основное приложение. """

from flask_sqlalchemy import SQLAlchemy
import flask

# from config.fires_db_config import db, DB_URL

flask_app = flask.Flask(__name__)

# db = SQLAlchemy(model_class=fires_db_config.db)
# fires_db_config.DB_URL  # db_url

# flask_app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
# db.init_app(flask_app)

MY_DATA_PATH = '../MY data/'
D = 1

# print(db_config.get_db().metadata)
