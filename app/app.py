from dash import Dash, Input, Output, callback, dash_table, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
import plotly
import plotly.graph_objects as go
import plotly.express as px
import shapely
import shapely.geometry as geometry
import config.db_config as db_config

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


sf = db_config.get_session_factory()
# sf

# Map options
map_background_options = ["carto-positron",
                          "open-street-map", "carto-darkmatter"]
map_options = {'map_center_start': {"lat": 52.25, "lon": 104.3},
               'map_zoom_start': 6, 'opacity': 0.15,
               'mapbox_style': map_background_options[0],
               'width': 1900, 'height': 800}


df_loc = load_geo_from_geojson("geodata/localities_Irk_obl.geojson")
map_loc = px.choropleth_mapbox(df_loc, geojson=df_loc.geometry, locations=df_loc.index,
                               mapbox_style=map_options['mapbox_style'],
                               opacity=map_options['opacity'],
                               center=map_options['map_center_start'],
                               zoom=map_options['map_zoom_start'],
                               labels={'type': 'Тип'},
                               hover_name='name',
                               hover_data=['type'],
                               color_discrete_sequence=['yellow']
                               ).update_traces(uid="map_loc", name='Населённые пункты')
map_loc.update_layout(
    margin={"r": 2, "t": 0, "l": 2, "b": 0},
    width=1500,
    height=800,
    legend=dict(
        yanchor="top",
        y=0.95,
        xanchor="left",
        x=0.95
    )
)

df_rail = load_geo_from_geojson("geodata/zhd_roads.geojson")
lats, lons = get_coords_linestring(df_rail)
map_rail = px.line_mapbox(df_rail, lat=lats, lon=lons,
                          color_discrete_sequence=['black'],
                          ).update_traces(name="Железные дороги",
                                          hovertemplate=None,
                                          hoverinfo='skip',
                                          uid='map_rail'
                                          ).data[0]

df_rivers = load_geo_from_geojson("geodata/rivers.geojson")
lats, lons = get_coords_linestring(df_rivers)
map_rivers = px.line_mapbox(df_rivers, lat=lats, lon=lons,
                            color_discrete_sequence=['blue'],
                            ).update_traces(uid="map_rivers", name='Реки', line={'width': 1},
                                            hovertemplate=None, hoverinfo='skip',).data[0]

df_roads = load_geo_from_geojson("geodata/auto_roads.geojson")
lats, lons = get_coords_linestring(df_roads)
map_roads = px.line_mapbox(df_roads, lat=lats, lon=lons,
                           color_discrete_sequence=['orange'],
                           ).update_traces(name="Дороги", line={'width': 2},
                                           hovertemplate=None, hoverinfo='skip', uid='map_roads').data[0]

df_loc_buf = load_geo_from_json("MY buffers/localities_buffers.json")
map_loc_buf = px.choropleth_mapbox(df_loc_buf, geojson=df_loc_buf.geometry,
                                   locations=df_loc_buf.index,
                                   opacity=0.5,
                                   labels={'type': 'Тип'},
                                   color_discrete_sequence=['orange'],
                                   ).update_traces(uid="map_loc_buf", visible=False).data[0]


df_road_buf = load_geo_from_json("MY buffers/roads_buffers.json")
map_roads_buf = px.choropleth_mapbox(df_road_buf, geojson=df_road_buf.geometry,
                                     locations=df_road_buf.index,
                                     opacity=0.5,
                                     labels={'type': 'Тип'},
                                     color_discrete_sequence=['yellow'],
                                     ).update_traces(uid="map_roads_buf", visible=False).data[0]

df_rivers_buf = load_geo_from_json("MY buffers/rivers_buffers.json")
map_rivers_buf = px.choropleth_mapbox(df_rivers_buf, geojson=df_rivers_buf.geometry,
                                      locations=df_rivers_buf.index,
                                      opacity=0.5,
                                      labels={'type': 'Тип'},
                                      color_discrete_sequence=['yellow'],
                                      ).update_traces(uid="map_rivers_buf", visible=False).data[0]

comb_fig = go.Figure(map_loc)  # 0
comb_fig.add_trace(map_rivers)  # 1
comb_fig.add_trace(map_rail)  # 2
comb_fig.add_trace(map_roads)  # 3

# comb_fig.add_trace(map_loc_buf)  # 4
# comb_fig.add_trace(map_roads_buf)  # 5
# comb_fig.add_trace(map_rivers_buf)  # 6

# comb_fig.update_traces(visible=False, selector={})

# DOM Elements

# Выбор подложки
dom_select_background = dbc.Select(
    id="select_background",
    options=[
        {"label": "Positron светлый", "value": map_background_options[0]},
        {"label": "Open Street Map", "value": map_background_options[1]},
        {"label": "Positron тёмный", "value": map_background_options[2]},
    ],
    value=map_background_options[0]
)
# Выбор фоновых слоёв
dom_backgound_layers_checklist = dbc.Checklist(
    id="checklist-layers",
    options=[
        {'label': 'Населённые пункты',
         'value': 'map_loc'},
        {'label': 'Дороги',
         'value': 'map_roads'},
        {'label': 'Железные дороги',
         'value': 'map_rail'},
        {'label': 'Реки',
         'value': 'map_rivers'}
    ],
    value=['map_loc']
)
# Настройка прозрачности слоёв
dom_opacity_slider = dcc.Slider(
    id="opacity-slider",
    min=0,
    max=100,
    # marks={str(i) for i in range(0, 101, 20)},
    value=50,
)
# Карта
dom_graph = dcc.Graph(
    id="map",
    figure=comb_fig,
    style={"maxWidth": "70%"}
)

# App
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(
    id="map-app",
    children=[
        # html.Div(children=[
        #     html.Label('Dropdown'),
        #     dcc.Dropdown(['New York City', 'Montréal',
        #                  'San Francisco'], 'Montréal'),

        #     html.Br(),
        #     html.Label('Multi-Select Dropdown'),
        #     dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
        #                  ['Montréal', 'San Francisco'],
        #                  multi=True),

        # Панель управления
        html.Div(
            id="map-control-panel",
            children=[
                # Слои
                html.Div(
                    children=[dbc.Label('Слои'),
                              # Выбор слоёв
                              dom_backgound_layers_checklist,
                              html.Br(),
                              dbc.Label('Прозрачность.'),
                              dom_opacity_slider,]
                ),
                dbc.Label('Подложка'),
                dom_select_background,
            ],
            style={'padding': 10,
                   # 'flex': 1,
                   'width': '20%',
                   'min-width': 200}
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
# @app.callback(
#     Output("graph", "figure"),
#     Input("x-axis", "value"),
#     Input("y-axis", "value"),
# )
# def generate_chart(x, y):
#     fig = px.box(df, x=x, y=y)
#     return fig


@app.callback(
    Output("map", "figure"),
    Input("select_background", "value"),
)
def set_mapbox_background(background_name):
    """Устанавливает подложку карты. """
    return comb_fig.update_layout(mapbox_style=background_name)

# app.layout = html.Div([
#     html.Div(children=[
#         html.Label('Dropdown'),
#         dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),

#         html.Br(),
#         html.Label('Multi-Select Dropdown'),
#         dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
#                      ['Montréal', 'San Francisco'],
#                      multi=True),

#         html.Br(),
#         html.Label('Radio Items'),
#         dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),
#     ], style={'padding': 10, 'flex': 1}),

#     html.Div(children=[
#         html.Label('Checkboxes'),
#         dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
#                       ['Montréal', 'San Francisco']
#         ),

#         html.Br(),
#         html.Label('Text Input'),
#         dcc.Input(value='MTL', type='text'),

#         html.Br(),
#         html.Label('Slider'),
#         dcc.Slider(
#             min=0,
#             max=9,
#             marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
#             value=5,
#         ),
#     ], style={'padding': 10, 'flex': 1})
# ], style={'display': 'flex', 'flexDirection': 'row'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
