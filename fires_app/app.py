# from models.fire import Fire
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import plotly.express as px
import shapely
from dash import Dash, Input, Output, callback, dash_table, dcc, html, Patch
# import dash_mantine_components
# import plotly

from fires_app import flask_app
from fires_app.config.fires_db_config import db
from fires_app.utils import geodata_utils, json_trace_creators
from fires_app.services import fire_service

# Map options
MAP_BACKGROUND_OPTIONS = ["open-street-map",
                          "carto-positron",
                          "carto-darkmatter"]
DEFAULT_MAP_OPTIONS = {'map_center_start': {"lat": 52.25, "lon": 104.3},
                       'map_zoom_start': 6,
                       'opacity': 0.25,
                       'mapbox_style': MAP_BACKGROUND_OPTIONS[1],
                       'width': 1500,
                       'height': 800}


def create_fires_df():
    fires = fire_service.get_fires()
    fires_df = pd.DataFrame([t.__dict__ for t in fires]
                            ).drop(columns={'_sa_instance_state'})
    lat = []
    lon = []
    for g in fires_df['coords']:
        lat.append(shapely.from_wkb(str(g)).y)
        lon.append(shapely.from_wkb(str(g)).x)

    fires_df.insert(2, 'lat', lat)
    fires_df.insert(2, 'lon', lon)

    return px.scatter_mapbox(fires_df,
                             lat='lat',
                             lon='lon',
                             opacity=1,
                             color_discrete_sequence=['red']
                             ).update_traces(uid="map_fires",
                                             name='Пожары',
                                             showlegend=True).data[0]


comb_fig = go.Figure()
comb_fig.update_layout(
    margin={"r": 5, "t": 0, "l": 5, "b": 0},
    width=1500,
    height=800,
    legend={
        "yanchor": "top",
        "y": 0.95,
        "xanchor": "left",
        "x": 0.85
    },
    mapbox={"center": DEFAULT_MAP_OPTIONS['map_center_start'],
            "zoom": DEFAULT_MAP_OPTIONS['map_zoom_start']}
)
comb_fig.add_trace(create_fires_df())


# DOM Elements

# Выбор подложки
dom_select_background = dbc.Select(id="select_background",
                                   options=[
                                       {"label": "Open Street Map",
                                        "value": MAP_BACKGROUND_OPTIONS[0]},
                                       {"label": "Positron светлый",
                                        "value": MAP_BACKGROUND_OPTIONS[1]},
                                       {"label": "Positron тёмный",
                                        "value": MAP_BACKGROUND_OPTIONS[2]}],
                                   value=DEFAULT_MAP_OPTIONS['mapbox_style'])

# Выбор фоновых слоёв
background_layers_ids = ['map_loc', 'map_roads', 'map_rail', 'map_rivers']
dom_backgound_layers_checklist = dbc.Checklist(id="checklist_layers",
                                               options=[
                                                   {'label': 'Населённые пункты',
                                                    'value': 'map_loc'},
                                                   {'label': 'Дороги',
                                                    'value': 'map_roads'},
                                                   {'label': 'Железные дороги',
                                                    'value': 'map_rail'},
                                                   {'label': 'Реки',
                                                    'value': 'map_rivers'}],
                                               value=['map_loc'],
                                               switch=True)

# Выбор дат
dom_date_choice = html.Div(id="dates_choice",
                           children=[
                               dbc.Label("Начало периода"),
                               dbc.Input(id="date_start",
                                         #  value="",
                                         type="date",),
                               dbc.Label("Конец периода"),
                               dbc.Input(id="date_end",
                                         type="date")
                           ])

# Настройка прозрачности слоёв
dom_opacity_slider = dcc.Slider(id="opacity_slider",
                                min=0,
                                max=100,
                                # marks={str(i) for i in range(0, 101, 20)},
                                value=50)
# Карта
dom_graph = dcc.Graph(id="map",
                      figure=comb_fig,
                      style={"maxWidth": "70%"},)

dom_select_main_layer = dbc.Select(id="select_main_layer",
                                   options=[
                                       {"label": "Пожары",
                                        "value": 'fires'},
                                       {"label": "Риски пожаров",
                                        "value": MAP_BACKGROUND_OPTIONS[1]},
                                   ],
                                   value='fires')
# responsive=True)


# HTML app

map_app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=flask_app)

map_app.layout = html.Div(
    id="map_app",

    children=[
        # Панель управления
        html.Div(
            id="map-control-panel",
            children=[
                # Слои
                html.Div(children=[
                    dbc.Label('Фоновые слои', html_for="checklist_layers"),
                    # Выбор слоёв
                    dom_backgound_layers_checklist,
                    html.Br(),
                    dbc.Label('Прозрачность', html_for="opacity_slider"),
                    dom_opacity_slider,]),
                dbc.Label('Подложка', html_for="select_background"),
                dom_select_background,
                dbc.Label('Слой данных', html_for="select_main_layer"),
                dom_select_main_layer,
                dom_date_choice,
            ],
            style={'padding': 10}
        ),
        html.Div(className="vr"),
        dom_graph
    ],

    style={
        "margin": 10,
        # "maxWidth": "100%",
        # "height": "90vh",
        'display': 'flex',
        'flexDirection': 'row'},
)


# Callbacks
@ map_app.callback(Output("map", "figure"),
                   Input("select_background", "value"),)
def set_mapbox_background(background_name):
    """Устанавливает подложку карты."""
    patched_fig = Patch()
    patched_fig['layout']['mapbox']['style'] = background_name
    return patched_fig


@ map_app.callback(Output("map", "figure", allow_duplicate=True),
                   Input("checklist_layers", "value"),
                   Input("map", "figure"),
                   prevent_initial_call=True)
def set_background_layers(layers_ids, fig):
    """Устанавливает фоновые слои карты."""
    patched_fig = Patch()
    # back_layers_existing = fig.select_traces(
    #     lambda x: x.uid in background_layers_ids)
    for l in background_layers_ids:
        # Выбор поиск выбранного слоя в текущих данных карты
        layer = [item for item in fig['data'] if item['uid'] == l]
        # Слоя нет на карте И он содержится в списке выбранных?
        if (len(layer) == 0) and (l in layers_ids):
            match l:
                case "map_rivers":
                    patched_fig['data'].append(
                        json_trace_creators.create_map_rivers_trace())
                case "map_roads":
                    patched_fig['data'].append(
                        json_trace_creators.create_map_roads_trace())
                case "map_rail":
                    patched_fig['data'].append(
                        json_trace_creators.create_map_rail_trace())
                case "map_loc":
                    patched_fig['data'].append(
                        json_trace_creators.create_map_loc_trace())
        # Слой есть на карте И его нет в списке выбранных?
        elif (len(layer) > 0) and not (l in layers_ids):
            patched_fig['data'].remove(layer[0])

    return patched_fig


@map_app.callback(Output("date_end", "min"),
                  Input("date_start", "value"))
def adjust_min_end_date(date):
    """Устанавливает минимальное значение конца выбранного периода равным началу периода."""
    return date


@map_app.callback(Output("date_start", "max"),
                  Input("date_end", "value"))
def adjust_max_start_date(date):
    """Устанавливает максимальное значение начала выбранного периода равным концу периода."""
    return date


if __name__ == '__main__':
    map_app.run(host='0.0.0.0', port=8050, debug=True)
