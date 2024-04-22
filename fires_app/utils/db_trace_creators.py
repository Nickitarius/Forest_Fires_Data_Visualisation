"""Содержит функции, создающие слои данных для карты с помощью данных из БД."""

import pandas as pd
import plotly.express as px
import shapely

from fires_app.services import fire_service


def create_fires_trace(uid, date_start, date_end, forestries=None):
    """Создаёт слой данных с пожарами, в соответствии с условиями."""
    fires = fire_service.get_fires_limited_data(date_start, date_end, forestries)
    fires_df = pd.DataFrame([t.__dict__ for t in fires])

    # Если по запросу в БД ничего нет — возвращаем пустой график
    if fires is None or len(fires) == 0:
        res = (
            px.scatter_mapbox(fires_df)
            .update_traces(
                uid=uid,
                showlegend=True,
                name="Пожары",
                visibility=False,
            )
            .data[0]
        )
        return res

    lat = []
    lon = []
    fires_df.drop(columns="_sa_instance_state", inplace=True)
    for i in range(len(fires_df)):
        g = fires_df.loc[i]
        lat.append(shapely.from_wkb(str(g["coords"])).y)
        lon.append(shapely.from_wkb(str(g["coords"])).x)
        fires_df.loc[i, "fire_status"] = g["fire_status"].name

    hover_template = (
        "<b>%{customdata[0]}<b><br>"
        + "Начало: %{customdata[1]}<br>"
        + "Конец: %{customdata[2]}<br>"
        + "Статус: %{customdata[3]}"
    )

    fires_df.insert(0, "lat", lat)
    fires_df.insert(0, "lon", lon)
    res = (
        px.scatter_mapbox(
            fires_df,
            lat="lat",
            lon="lon",
            opacity=1,
            color_discrete_sequence=["red"],
            custom_data=["id", "code", "date_start", "date_end", "fire_status"],
        )
        .update_traces(
            uid=uid,
            showlegend=True,
            name="Пожары",
            hovertemplate=hover_template,
            # size=2,
            marker={"size": 10},
        )
        .data[0]
    )
    return res


def create_fires_df(date_start, date_end, forestries=None):
    """Создаёт слой данных с пожарами, в соответствии с условиями."""
    fires = fire_service.get_fires_limited_data(date_start, date_end, forestries)
    fires_df = pd.DataFrame([t.__dict__ for t in fires])

    # Если по запросу в БД ничего нет — возвращаем пустой график
    if fires is None or len(fires) == 0:
        return fires_df

    # for

    lat = []
    lon = []
    fires_df.drop(columns="_sa_instance_state", inplace=True)
    for i in range(len(fires_df)):
        g = fires_df.loc[i]
        lat.append(shapely.from_wkb(str(g["coords"])).y)
        lon.append(shapely.from_wkb(str(g["coords"])).x)
        fires_df.loc[i, "fire_status"] = g["fire_status"].name

    fires_df.drop("coords", axis=1, inplace=True)
    fires_df.insert(0, "lat", lat)
    fires_df.insert(0, "lon", lon)
    return fires_df
