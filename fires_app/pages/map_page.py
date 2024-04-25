"""Интерактивная карта. Доступна всем пользователям. """

import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import MATCH, Dash, Input, Output, Patch, State, callback, dcc, html

from fires_app.services import fire_status_service, forestry_service
from fires_app.utils import db_trace_creators, json_trace_creators, map_utils


MAP_BACKGROUND_OPTIONS = ["open-street-map", "carto-positron", "carto-darkmatter"]
# Опции карты по-умолчанию, в т.ч. опции input'ов
DEFAULT_MAP_OPTIONS = {
    "map_center_start": {"lat": 52.25, "lon": 104.3},
    "map_zoom_start": 6,
    "opacity": 0.25,
    "mapbox_style": MAP_BACKGROUND_OPTIONS[1],
    "width": 1500,
    "height": 800,
}
# uid главного слоя данных на карте.
MAIN_TRACE_UID = "main_trace"


dash.register_page(__name__, path="/map", name="Карта")

# DOM Elements

# Выбор подложки
dom_select_background = dbc.Select(
    id="select_background",
    options=[
        {"label": "Open Street Map", "value": MAP_BACKGROUND_OPTIONS[0]},
        {"label": "Positron светлый", "value": MAP_BACKGROUND_OPTIONS[1]},
        {"label": "Positron тёмный", "value": MAP_BACKGROUND_OPTIONS[2]},
    ],
    value=DEFAULT_MAP_OPTIONS["mapbox_style"],
)

# Выбор фоновых слоёв
background_layers_ids = ["map_loc", "map_roads", "map_rail", "map_rivers"]
dom_backgound_layers_checklist = dbc.Checklist(
    id="checklist_layers",
    options=[
        {"label": "Населённые пункты", "value": "map_loc"},
        {"label": "Дороги", "value": "map_roads"},
        {"label": "Железные дороги", "value": "map_rail"},
        {"label": "Реки", "value": "map_rivers"},
    ],
    value="",
    switch=True,
)

# Панель фоновых слоёв
background_layers_panel = html.Div(
    children=[
        dbc.Label("Фоновые слои", html_for="checklist_layers"),
        # Выбор слоёв
        dom_backgound_layers_checklist,
        dbc.Label("Подложка", html_for="select_background"),
        dom_select_background,
    ]
)

# Настройка прозрачности слоёв
dom_opacity_slider = dcc.Slider(
    id="opacity_slider",
    min=0,
    max=100,
    # marks={str(i) for i in range(0, 101, 20)},
    value=50,
)

# Выбор основного слоя
dom_main_layer_select = dbc.Select(
    id="main_layer_select",
    options=[
        {"label": "Пожары", "value": "fires"},
        {"label": "Риски пожаров", "value": MAP_BACKGROUND_OPTIONS[1]},
    ],
    value="fires",
)
# responsive=True)

# Выбор дат
dom_dates_input = html.Div(
    id="dates_choice",
    children=[
        dbc.Label("Начало периода"),
        dbc.Input(
            id="date_start",
            value="2017-01-01",
            type="date",
        ),
        dbc.Label("Конец периода"),
        dbc.Input(
            id="date_end",
            value="2021-12-31",
            type="date",
        ),
    ],
)

# Выбор лесничества
forestry_options = map_utils.get_forestries_options()
dom_forestries_dropdown = dcc.Dropdown(
    id="forestries_dropdown",
    options=forestry_options,
    value=forestry_options[0]["value"],
    multi=True,
    placeholder="Выбор...",
)
# Кнопка выбора/отмены выбора всех лесничеств для dom_forestries_dropdown

dom_select_deselct_all_forestries = html.Div(
    dbc.Button(
        id="select_deselct_all_button",
        children="Выбрать все",
        color="secondary",
        outline=True,
        class_name="mb-3",
        size="sm",
    )
)

# Выбор статусов пожаров
fire_statuses = map_utils.get_fire_statuses_options()
dom_fire_statuses_dropdown = dcc.Dropdown(
    id="fire_statuses_dropdown",
    options=fire_statuses,
    value=fire_statuses[0]["value"],
    multi=True,
    placeholder="Выбор...",
)

# Панель управления
dom_control_panel = html.Div(
    id="map-control-panel",
    children=[
        # Фоновые слои
        background_layers_panel,
        html.Hr(),
        html.Div(
            children=[
                dbc.Label("Слой данных", html_for="main_layer_select"),
                dom_main_layer_select,
                dbc.Label("Прозрачность", html_for="opacity_slider"),
                dom_opacity_slider,
            ]
        ),
        html.Hr(),
        dom_dates_input,
        html.Hr(),
        dbc.Label("Выбор лесничеств", html_for="forestry_dropdown"),
        dom_select_deselct_all_forestries,
        dom_forestries_dropdown,
        html.Hr(),
        dbc.Label("Выбор статуса пожаров", html_for="fire_statuses_dropdown"),
        dom_fire_statuses_dropdown,
    ],
    style={
        "padding": 10,
        # "flex-direction": "column"
    },
    className="col-sm-2",
)

map_fig = go.Figure()
default_trace = db_trace_creators.create_fires_trace(
    MAIN_TRACE_UID,
    "2017-01-01",
    "2021-12-31",
    forestry_options[0]["value"],
    # [option["value"] for option in forestry_options],
)
map_fig.add_trace(default_trace)
map_fig.update_layout(
    margin={"r": 5, "t": 1, "l": 5, "b": 1},
    # width=1500,
    # height=800,
    legend={"yanchor": "top", "y": 0.95, "xanchor": "left", "x": 0.85},
    mapbox={
        "center": DEFAULT_MAP_OPTIONS["map_center_start"],
        "zoom": DEFAULT_MAP_OPTIONS["map_zoom_start"],
        "style": DEFAULT_MAP_OPTIONS["mapbox_style"],
    },
    clickmode="event+select",
)

# Карта
dom_graph = dcc.Graph(
    id="map",
    figure=map_fig,
    style={
        # "maxWidth": "70%",
        "height": "90vh",
        "width": "100%",
        "padding-left": "5px",
    },
    # className="col-xl"
)

# Панель информации о выбранном объекте.
dom_object_info_panel = html.Div(
    id="object_info_panel",
    children=[],
    style={
        "padding": 10,
        # "flex-direction": "column"
    },
    className="col-sm-2",
)

layout = html.Div(
    id="map_app",
    children=[
        dom_control_panel,
        html.Div(className="vr"),
        dom_graph,
        html.Div(className="vr"),
        dom_object_info_panel,
    ],
    style={
        "margin": 10,
        # "maxWidth": "100%",
        # "height": "90vh",
        "display": "flex",
        "flexDirection": "row",
    },
)
