"""Функции для загрузки геоданных из файлов json/geojson."""

import plotly.express as px

from . import geodata_utils


def create_map_loc_trace():
    """Возвразает слой данных с полигонами, означающими населённые пункты."""
    df_loc = geodata_utils.load_geo_from_geojson(
        "geodata/localities_Irk_obl.geojson"
    ).drop(columns=["poly", "address"])
    hover_tempalte = "<b>%{customdata[0]}</b><br>Тип: %{customdata[1]}"
    return (
        px.choropleth_mapbox(
            df_loc,
            geojson=df_loc["geometry"],
            locations=df_loc.index,
            labels={"type": "Тип"},
            color_discrete_sequence=["yellow"],
            opacity=0.5,
            custom_data=["name", "type"],
        )
        .update_traces(
            name="Населённые пункты",
            uid="map_loc",
            hovertemplate=hover_tempalte,
        )
        .data[0]
    )


def create_map_rail_trace():
    """Возвращает слой с картой железных дорог."""
    df_rail = geodata_utils.load_geo_from_geojson("geodata/zhd_roads.geojson").drop(
        columns=["geom:1"]
    )
    lats, lons = geodata_utils.get_coords_linestring(df_rail)
    return (
        px.line_mapbox(
            lat=lats,
            lon=lons,
            color_discrete_sequence=["black"],
        )
        .update_traces(
            name="Железные дороги",
            hovertemplate=None,
            hoverinfo="skip",
            uid="map_rail",
            showlegend=True,
        )
        .data[0]
    )


def create_map_rivers_trace():
    """Возвращает слой с картой рек."""
    df_rivers = geodata_utils.load_geo_from_geojson("geodata/rivers.geojson")
    lats, lons = geodata_utils.get_coords_linestring(df_rivers)
    return (
        px.line_mapbox(
            lat=lats,
            lon=lons,
            color_discrete_sequence=["blue"],
        )
        .update_traces(
            uid="map_rivers",
            name="Реки",
            line={"width": 1},
            hovertemplate=None,
            hoverinfo="skip",
            showlegend=True,
        )
        .data[0]
    )


def create_map_roads_trace():
    """Возвразает слой слой данных с картой дорог."""
    df_roads = geodata_utils.load_geo_from_geojson("geodata/auto_roads.geojson")
    lats, lons = geodata_utils.get_coords_linestring(df_roads)
    return (
        px.line_mapbox(
            lat=lats,
            lon=lons,
            color_discrete_sequence=["orange"],
        )
        .update_traces(
            name="Дороги",
            line={"width": 2},
            hovertemplate=None,
            hoverinfo="skip",
            uid="map_roads",
            showlegend=True,
        )
        .data[0]
    )


def create_loc_buf_trace():
    """Возвращает слой данных с областями, находящимися в определённых радиусах от
    населённых пунктов."""
    df_loc_buf = geodata_utils.load_geo_from_json("MY buffers/localities_buffers.json")
    return (
        px.choropleth_mapbox(
            df_loc_buf,
            geojson=df_loc_buf.geometry,
            locations=df_loc_buf.index,
            opacity=0.5,
            labels={"type": "Тип"},
            color_discrete_sequence=["orange"],
        )
        .update_traces(uid="map_loc_buf", visible=False)
        .data[0]
    )


def create_road_buf_trace():
    """Возвращает слой данных с областями, находящимися в определённых радиусах от дорог."""
    df_road_buf = geodata_utils.load_geo_from_json("MY buffers/roads_buffers.json")
    return (
        px.choropleth_mapbox(
            df_road_buf,
            geojson=df_road_buf.geometry,
            locations=df_road_buf.index,
            opacity=0.5,
            labels={"type": "Тип"},
            color_discrete_sequence=["yellow"],
        )
        .update_traces(uid="map_roads_buf", visible=False)
        .data[0]
    )


def create_rivers_buf_trace():
    """Возвращает слой данных с областями, находящимися в определённых радиусах от рек."""
    df_rivers_buf = geodata_utils.load_geo_from_json("MY buffers/rivers_buffers.json")
    return (
        px.choropleth_mapbox(
            df_rivers_buf,
            geojson=df_rivers_buf.geometry,
            locations=df_rivers_buf.index,
            opacity=0.5,
            labels={"type": "Тип"},
            color_discrete_sequence=["yellow"],
        )
        .update_traces(uid="map_rivers_buf", visible=False, showlegend=True)
        .data[0]
    )
