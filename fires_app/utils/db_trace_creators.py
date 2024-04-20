import pandas as pd
import shapely
import plotly.express as px
from fires_app.services import fire_service


def create_fires_trace(uid, date_start, date_end):
    """Создаёт слой данных с пожарами, в соответствии с условиями."""
    fires = fire_service.get_fires_limited_data(date_start, date_end)

    fires_df = pd.DataFrame([t._asdict() for t in fires]
                            )
    lat = []
    lon = []
    if len(fires) > 0:

        for g in fires_df['coords']:
            lat.append(shapely.from_wkb(str(g)).y)
            lon.append(shapely.from_wkb(str(g)).x)

    fires_df.insert(0, 'lat', lat)
    fires_df.insert(0, 'lon', lon)

    return px.scatter_mapbox(fires_df,
                             lat='lat',
                             lon='lon',
                             opacity=1,
                             color_discrete_sequence=['red']
                             ).update_traces(uid=uid,
                                             name='Пожары',
                                             showlegend=True).data[0]
