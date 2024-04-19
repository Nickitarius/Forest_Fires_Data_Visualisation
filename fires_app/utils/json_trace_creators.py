"""Функции для загрузки геоданных из файлов json/geojson."""
import plotly.express as px

from . import geodata_utils


def create_map_loc_trace():
    df_loc = geodata_utils.load_geo_from_geojson(
        "geodata/localities_Irk_obl.geojson")
    return px.choropleth_mapbox(df_loc,
                                geojson=df_loc['geometry'],
                                locations=df_loc.index,
                                labels={'type': 'Тип'},
                                hover_name='name',
                                hover_data=['type'],
                                color_discrete_sequence=['yellow'],
                                opacity=0.25
                                ).update_traces(uid="map_loc",
                                                name='Населённые пункты'
                                                ).data[0]


def create_map_rail_trace():
    df_rail = geodata_utils.load_geo_from_geojson("geodata/zhd_roads.geojson")
    lats, lons = geodata_utils.get_coords_linestring(df_rail)
    return px.line_mapbox(df_rail,
                          lat=lats,
                          lon=lons,
                          color_discrete_sequence=['black'],
                          ).update_traces(name="Железные дороги",
                                          hovertemplate=None,
                                          hoverinfo='skip',
                                          uid='map_rail',
                                          showlegend=True
                                          ).data[0]


def create_map_rivers_trace():
    df_rivers = geodata_utils.load_geo_from_geojson("geodata/rivers.geojson")
    lats, lons = geodata_utils.get_coords_linestring(df_rivers)
    return px.line_mapbox(df_rivers,
                          lat=lats,
                          lon=lons,
                          color_discrete_sequence=['blue'],
                          ).update_traces(uid="map_rivers",
                                          name='Реки',
                                          line={'width': 1},
                                          hovertemplate=None,
                                          hoverinfo='skip',
                                          showlegend=True
                                          ).data[0]


def create_map_roads_trace():
    df_roads = geodata_utils.load_geo_from_geojson(
        "geodata/auto_roads.geojson")
    lats, lons = geodata_utils.get_coords_linestring(df_roads)
    return px.line_mapbox(df_roads,
                          lat=lats,
                          lon=lons,
                          color_discrete_sequence=['orange'],
                          ).update_traces(name="Дороги",
                                               line={'width': 2},
                                               hovertemplate=None,
                                               hoverinfo='skip',
                                               uid='map_roads',
                                               showlegend=True
                                          ).data[0]


# def create_map_loc_trace():
#     df_loc = geodata_utils.load_geo_from_geojson(
#         "geodata/localities_Irk_obl.geojson")
#     return px.choropleth_mapbox(df_loc,
#                                 geojson=df_loc['geometry'],
#                                 locations=df_loc.index,
#                                 # opacity=DEFAULT_MAP_OPTIONS['opacity'],
#                                 labels={'type': 'Тип'},
#                                 hover_name='name',
#                                 hover_data=['type'],
#                                 color_discrete_sequence=['yellow']
#                                 ).update_traces(uid="map_loc",
#                                                 name='Населённые пункты'
#                                                 ).data[0]


def create_loc_buf_trace():
    df_loc_buf = geodata_utils.load_geo_from_json(
        "MY buffers/localities_buffers.json")
    return px.choropleth_mapbox(df_loc_buf,
                                geojson=df_loc_buf.geometry,
                                locations=df_loc_buf.index,
                                opacity=0.5,
                                labels={'type': 'Тип'},
                                color_discrete_sequence=['orange'],
                                ).update_traces(uid="map_loc_buf",
                                                    visible=False).data[0]


def create_road_buf_trace():
    df_road_buf = geodata_utils.load_geo_from_json(
        "MY buffers/roads_buffers.json")
    return px.choropleth_mapbox(df_road_buf,
                                geojson=df_road_buf.geometry,
                                locations=df_road_buf.index,
                                opacity=0.5,
                                labels={'type': 'Тип'},
                                color_discrete_sequence=['yellow'],
                                ).update_traces(uid="map_roads_buf",
                                                visible=False).data[0]


def create_rivers_buf_trace():
    df_rivers_buf = geodata_utils.load_geo_from_json(
        "MY buffers/rivers_buffers.json")
    return px.choropleth_mapbox(df_rivers_buf,
                                geojson=df_rivers_buf.geometry,
                                locations=df_rivers_buf.index,
                                opacity=0.5,
                                labels={'type': 'Тип'},
                                color_discrete_sequence=['yellow']
                                ).update_traces(uid="map_rivers_buf",
                                                visible=False,
                                                showlegend=True).data[0]
