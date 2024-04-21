from fires_app.models.forestry import Forestry
from fires_app import db, flask_app


def get_all_forestries():
    with flask_app.app_context():
        query = db.Query(Forestry)
        res = db.session.execute(query).scalars().all()
        print(res[0])
        return res
