# from models.fire import Fire
from dash import Dash, Input, Output, callback, dash_table, dcc, html, Patch
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
# import plotly
import plotly.graph_objects as go
import plotly.express as px
import shapely
# import shapely.geometry as geometry
# from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy

from fires_app import flask_app
# import config.db_config as db_config
# from fires_app.config import flask_app
# import flask_app

MY_DATA_PATH = '../MY data/'


def pd_to_gpd_w_geom(df):
    """Transforms Pandas DF to Geopandas DF, reading geometry stored as WKB from 'geom' field"""
    geoms = []
    for shape in df['geom']:
        geoms.append(shapely.from_wkb(shape))

    gdf = gpd.GeoDataFrame(df, geometry=geoms, crs="EPSG:4326")
    return gdf


def repalce_geometry_with_wkb(gdf):
    """Recieves GeoPandas DF, deletes geometry, writes WKB based on it instead"""
    wkb = gdf.geometry.to_wkb(hex=True)
    gdf.drop(columns=['geometry'], inplace=True)
    gdf.rename(columns={'poly': 'geom'}, inplace=True)
    gdf['geom'] = wkb
    return gdf


def get_coords_linestring(gdf):
    """Get coords from a GeoPandas DF"""
    lats = []
    lons = []
    for i in gdf['geometry']:
        lons = lons+i.coords.xy[0].tolist()
        lats = lats+i.coords.xy[1].tolist()
        lons.append(None)
        lats.append(None)

    return lats, lons


def load_geo_from_geojson(file_name):
    """Загружает географические данные из GEOJSON."""
    path_to_json = MY_DATA_PATH + file_name
    df = gpd.read_file(path_to_json)
    return df


def load_geo_from_json(file_name):
    """Загружает географические данные из обычного JSON."""
    path_to_json = MY_DATA_PATH + file_name
    df = pd_to_gpd_w_geom(pd.read_json(path_to_json))
    return df


# DBS = db_config.get_session_factory()

# DBS.select(Fire)

# db_session = db_config.get_session()
# db = db_config.get_db()
# db = SQLAlchemy(model_class=db_config.FiresDB)

# Map options
map_background_options = ["open-street-map",
                          "carto-positron", "carto-darkmatter"]
map_options = {'map_center_start': {"lat": 52.25, "lon": 104.3},
               'map_zoom_start': 6, 'opacity': 0.25,
               'mapbox_style': map_background_options[1],
               'width': 1500, 'height': 800}


def create_map_loc_trace():
    df_loc = load_geo_from_geojson("geodata/localities_Irk_obl.geojson")
    return px.choropleth_mapbox(df_loc,
                                geojson=df_loc.geometry,
                                locations=df_loc.index,
                                opacity=map_options['opacity'],
                                labels={'type': 'Тип'},
                                hover_name='name',
                                hover_data=['type'],
                                color_discrete_sequence=['yellow']
                                ).update_traces(uid="map_loc",
                                                name='Населённые пункты').data[0]


def create_map_rail_trace():
    df_rail = load_geo_from_geojson("geodata/zhd_roads.geojson")
    lats, lons = get_coords_linestring(df_rail)
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
    df_rivers = load_geo_from_geojson("geodata/rivers.geojson")
    lats, lons = get_coords_linestring(df_rivers)
    return px.line_mapbox(df_rivers,
                          lat=lats,
                          lon=lons,
                          color_discrete_sequence=['blue'],
                          ).update_traces(uid="map_rivers",
                                          name='Реки',
                                          line={'width': 1},
                                          hovertemplate=None,
                                          hoverinfo='skip',
                                          showlegend=True).data[0]


def create_map_roads_trace():
    df_roads = load_geo_from_geojson("geodata/auto_roads.geojson")
    lats, lons = get_coords_linestring(df_roads)
    return px.line_mapbox(df_roads,
                          lat=lats,
                          lon=lons,
                          color_discrete_sequence=['orange'],
                          ).update_traces(name="Дороги",
                                               line={'width': 2},
                                               hovertemplate=None,
                                               hoverinfo='skip',
                                               uid='map_roads',
                                               showlegend=True).data[0]


map_loc = create_map_loc_trace()

# df_loc_buf = load_geo_from_json("MY buffers/localities_buffers.json")
# map_loc_buf = px.choropleth_mapbox(df_loc_buf,
#                                    geojson=df_loc_buf.geometry,
#                                    locations=df_loc_buf.index,
#                                    opacity=0.5,
#                                    labels={'type': 'Тип'},
#                                    color_discrete_sequence=['orange'],
#                                    ).update_traces(uid="map_loc_buf",
#                                                    visible=False).data[0]


# df_road_buf = load_geo_from_json("MY buffers/roads_buffers.json")
# map_roads_buf = px.choropleth_mapbox(df_road_buf,
#                                      geojson=df_road_buf.geometry,
#                                      locations=df_road_buf.index,
#                                      opacity=0.5,
#                                      labels={'type': 'Тип'},
#                                      color_discrete_sequence=['yellow'],
#                                      ).update_traces(uid="map_roads_buf",
#                                                      visible=False).data[0]

# df_rivers_buf = load_geo_from_json("MY buffers/rivers_buffers.json")
# map_rivers_buf = px.choropleth_mapbox(df_rivers_buf,
#                                       geojson=df_rivers_buf.geometry,
#                                       locations=df_rivers_buf.index,
#                                       opacity=0.5,
#                                       labels={'type': 'Тип'},
#                                       color_discrete_sequence=['yellow']
#                                       ).update_traces(uid="map_rivers_buf",
#                                                       visible=False,
#                                                       showlegend=True).data[0]

comb_fig = go.Figure(map_loc)
comb_fig.update_layout(
    margin={"r": 5, "t": 0, "l": 5, "b": 0},
    width=1500,
    height=800,
    legend=dict(
        yanchor="top",
        y=0.95,
        xanchor="left",
        x=0.85
    ),
    mapbox=dict(center=map_options['map_center_start'],
                zoom=map_options['map_zoom_start'])
)


# def create_fires_df():
#     fires = select(Fire)
#     fires = sf.scalars(fires).all()

#     fires_df = pd.DataFrame([t.__dict__ for t in fires]
#                             ).drop(columns={'_sa_instance_state'})

#     lat = []
#     lon = []
#     for g in fires_df['coords']:
#         lat.append(shapely.from_wkb(str(g)).y)
#         lon.append(shapely.from_wkb(str(g)).x)

#     fires_df.insert(2, 'lat', lat)
#     fires_df.insert(2, 'lon', lon)

#     # geom = []
#     # for g in fires_df['coords']:
#     #     geom.append(shapely.from_wkb(str(g)))

#     # fires_gpd = gpd.GeoDataFrame(fires_df, geometry=geom)

#     return px.scatter_mapbox(fires_df,
#                              lat='lat',
#                              lon='lon',
#                              opacity=1,
#                              color_discrete_sequence=['red']
#                              ).update_traces(uid="map_fires",
#                                              name='Пожары',
#                                              showlegend=True).data[0]


# map_fires = create_fires_df()
# comb_fig.add_trace(map_fires)

print('S')

# comb_fig.add_trace(map_loc_buf)
# comb_fig.add_trace(map_roads_buf)
# comb_fig.add_trace(map_rivers_buf)

# comb_fig.update_traces(visible=False, selector={})

# DOM Elements

# Выбор подложки
dom_select_background = dbc.Select(id="select_background",
                                   options=[{"label": "Open Street Map",
                                             "value": map_background_options[0]},
                                            {"label": "Positron светлый",
                                                "value": map_background_options[1]},
                                            {"label": "Positron тёмный",
                                             "value": map_background_options[2]},],
                                   value=map_options['mapbox_style'])
# Выбор фоновых слоёв
background_layers_ids = ['map_loc', 'map_roads', 'map_rail', 'map_rivers']
dom_backgound_layers_checklist = dbc.Checklist(id="checklist_layers",
                                               options=[{'label': 'Населённые пункты',
                                                         'value': 'map_loc'},
                                                        {'label': 'Дороги',
                                                         'value': 'map_roads'},
                                                        {'label': 'Железные дороги',
                                                         'value': 'map_rail'},
                                                        {'label': 'Реки',
                                                         'value': 'map_rivers'}],
                                               value=['map_loc'],
                                               switch=True)

# Настройка прозрачности слоёв
dom_opacity_slider = dcc.Slider(id="opacity_slider",
                                min=0,
                                max=100,
                                # marks={str(i) for i in range(0, 101, 20)},
                                value=50,)
# Карта
dom_graph = dcc.Graph(id="map",
                      figure=comb_fig,
                      style={"maxWidth": "70%"},)

dom_select_main_layer = dbc.Select(id="select_main_layer",
                                   options=[{"label": "Пожары",
                                             "value": 'fires'},
                                            {"label": "Риски пожаров",
                                                "value": map_background_options[1]},
                                            ],
                                   value='fires')
# responsive=True)

# HTML app
map_app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=flask_app)
map_app.layout = html.Div(
    id="map-app",
    children=[
        # Панель управления
        html.Div(
            id="map-control-panel",
            children=[
                # Слои
                html.Div(children=[  # dbc.Label('Слои'),
                    # Выбор слоёв
                    dom_backgound_layers_checklist,
                    html.Br(),
                    dbc.Label('Прозрачность.'),
                    dom_opacity_slider,]),
                dbc.Label('Подложка'),
                dom_select_background,
                dbc.Label('Слой данных'),
                dom_select_main_layer,
            ],

            style={'padding': 10,
                   # 'flex': 1,
                   'width': '15%',
                   'minWidth': 150}
        ),
        html.Div(className="vr"),
        dom_graph
    ],
    style={"margin": 10,
           "maxWidth": "100%",
           "height": "90vh",
           'display': 'flex',
           'flexDirection': 'row'},
)

# Callbacks


@map_app.callback(Output("map", "figure"),
                  Input("select_background", "value"),)
def set_mapbox_background(background_name):
    """Устанавливает подложку карты. """
    patched_fig = Patch()
    patched_fig['layout']['mapbox']['style'] = background_name
    return patched_fig


@map_app.callback(Output("map", "figure", allow_duplicate=True),
                  Input("checklist_layers", "value"),
                  Input("map", "figure"),
                  prevent_initial_call=True)
def set_background_layers(layers_ids, fig):
    """Устанавливает фоновые слои карты. """
    patched_fig = Patch()
    # back_layers_existing = fig.select_traces(
    #     lambda x: x.uid in background_layers_ids)
    for l in background_layers_ids:
        g = [item for item in fig['data'] if item['uid'] == l]
        if len(g) == 0:
            if (l in layers_ids):
                match l:
                    case "map_rivers":
                        patched_fig['data'].append(create_map_rivers_trace())
                    case "map_roads":
                        patched_fig['data'].append(create_map_roads_trace())
                    case "map_rail":
                        patched_fig['data'].append(create_map_rail_trace())
                    case "map_loc":
                        patched_fig['data'].append(create_map_loc_trace())
        else:
            patched_fig['data'].remove(g[0])

    return patched_fig


# DB connection data
DB_DIALECT = "mysql"
DB_ENGINE = "pymysql"
DB_USERNAME = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "weather_risks_app"
DB_CHARSET = "utf8mb4"

db_url = DB_DIALECT + "+" + DB_ENGINE + "://" + DB_USERNAME + ":" + \
    DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME + "?charset=" + DB_CHARSET
map_app.server.config["SQLALCHEMY_DATABASE_URI"] = db_url
# db_session.init_app(app)
db.init_app(map_app.server)

if __name__ == '__main__':
    map_app.run(host='0.0.0.0', port=8050, debug=False)
