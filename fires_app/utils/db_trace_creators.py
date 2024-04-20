"""Содержит функции, создающие слои данных для карты с помощью данных из БД."""
import pandas as pd
import shapely
import plotly.express as px
from fires_app.services import fire_service


def create_fires_trace(uid, date_start, date_end):
    """Создаёт слой данных с пожарами, в соответствии с условиями."""
    fires = fire_service.get_fires_limited_data(date_start, date_end)
    fires_df = pd.DataFrame([t.tuple()[0].__dict__ for t in fires]
                            ).drop(columns="_sa_instance_state")

    lat = []
    lon = []
    if len(fires) > 0:
        for g in fires_df['coords']:
            lat.append(shapely.from_wkb(str(g)).y)
            lon.append(shapely.from_wkb(str(g)).x)

    hover_template = "<b>%{customdata[0]}<b><br>" +\
        "Начало: {customdata[1]}<br>" +\
        "Конец: {customdata[2]}<br>" +\
        "Статус: {customdata[3].name}"

    fires_df.insert(0, 'lat', lat)
    fires_df.insert(0, 'lon', lon)
    return px.scatter_mapbox(fires_df,
                             lat='lat',
                             lon='lon',
                             opacity=1,
                             color_discrete_sequence=['red'],
                             custom_data=['code',
                                          'date_start',
                                          'date_end',
                                          'fire_status']
                             ).update_traces(uid=uid,
                                             name='Пожары',
                                             showlegend=True,
                                             hovertemplate=hover_template
                                             ).data[0]
