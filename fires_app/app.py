"""Файл с приложением-интерактивной картой."""

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html, Patch
from fires_app.services.forestry_service import get_all_forestries

from fires_app import flask_app
from fires_app.utils import json_trace_creators, db_trace_creators

# Map options
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


def replace_trace_by_uid(fig, patch, uid, new_trace):
    """
    Заменяет слой данных в графике с данным uid
    на новый слой.
    """
    old_trace = [item for item in fig["data"] if item["uid"] == uid]
    if len(old_trace) > 0:
        patch["data"].remove(old_trace[0])

    patch["data"].append(new_trace)
    return patch


def patch_main_trace(fig, trace, patch, date_start, date_end):
    """Меняет главный слой в данных графика."""
    patch = Patch()
    match trace:
        case "fires":
            new_trace = db_trace_creators.create_fires_trace(
                MAIN_TRACE_UID, date_start, date_end
            )

    patch = replace_trace_by_uid(fig, patch, MAIN_TRACE_UID, new_trace)
    return patch


# print(get_all_forestries())


map_fig = go.Figure()
default_trace = db_trace_creators.create_fires_trace(
    MAIN_TRACE_UID, "2017-01-01", "2021-12-31"
)
map_fig.add_trace(default_trace)
map_fig.update_layout(
    margin={"r": 5, "t": 0, "l": 5, "b": 0},
    width=1500,
    height=800,
    legend={"yanchor": "top", "y": 0.95, "xanchor": "left", "x": 0.85},
    mapbox={
        "center": DEFAULT_MAP_OPTIONS["map_center_start"],
        "zoom": DEFAULT_MAP_OPTIONS["map_zoom_start"],
        "style": DEFAULT_MAP_OPTIONS["mapbox_style"],
    },
    clickmode="event+select",
)


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

# Настройка прозрачности слоёв
dom_opacity_slider = dcc.Slider(
    id="opacity_slider",
    min=0,
    max=100,
    # marks={str(i) for i in range(0, 101, 20)},
    value=50,
)
# Карта
dom_graph = dcc.Graph(
    id="map",
    figure=map_fig,
    style={
        "maxWidth": "70%",
    },
)

# Выбор основного слоя
dom_select_main_layer = dbc.Select(
    id="select_main_layer",
    options=[
        {"label": "Пожары", "value": "fires"},
        {"label": "Риски пожаров", "value": MAP_BACKGROUND_OPTIONS[1]},
    ],
    value="fires",
)
# responsive=True)

# Выбор дат
dom_date_choice = html.Div(
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
                html.Div(
                    children=[
                        dbc.Label("Фоновые слои", html_for="checklist_layers"),
                        # Выбор слоёв
                        dom_backgound_layers_checklist,
                        dbc.Label("Подложка", html_for="select_background"),
                        dom_select_background,
                    ]
                ),
                html.Hr(),
                html.Div(
                    children=[
                        dbc.Label("Слой данных", html_for="select_main_layer"),
                        dom_select_main_layer,
                        dbc.Label("Прозрачность", html_for="opacity_slider"),
                        dom_opacity_slider,
                    ]
                ),
                html.Hr(),
                dom_date_choice,
                html.Hr(),
            ],
            style={
                "padding": 10,
            },
        ),
        html.Div(className="vr"),
        dom_graph,
    ],
    style={
        "margin": 10,
        # "maxWidth": "100%",
        # "height": "90vh",
        "display": "flex",
        "flexDirection": "row",
    },
)+


# Callbacks


@map_app.callback(
    Output("map", "figure"),
    Input("select_background", "value"),
    prevent_initial_call=True,
)
def set_mapbox_background(background_name):
    """Устанавливает подложку карты."""
    patched_fig = Patch()
    patched_fig["layout"]["mapbox"]["style"] = background_name
    return patched_fig


@map_app.callback(
    Output("map", "figure", allow_duplicate=True),
    Input("checklist_layers", "value"),
    Input("map", "figure"),
    prevent_initial_call=True,
)
def set_background_layers(layers_ids, fig):
    """Устанавливает фоновые слои карты."""
    patched_fig = Patch()
    for l in background_layers_ids:
        # Выбор поиск выбранного слоя в текущих данных карты
        layer = [item for item in fig["data"] if item["uid"] == l]
        # Слоя нет на карте И он содержится в списке выбранных?
        if (len(layer) == 0) and (l in layers_ids):
            match l:
                case "map_rivers":
                    patched_fig["data"].append(
                        json_trace_creators.create_map_rivers_trace()
                    )
                case "map_roads":
                    patched_fig["data"].append(
                        json_trace_creators.create_map_roads_trace()
                    )
                case "map_rail":
                    patched_fig["data"].append(
                        json_trace_creators.create_map_rail_trace()
                    )
                case "map_loc":
                    patched_fig["data"].append(
                        json_trace_creators.create_map_loc_trace()
                    )
        # Слой есть на карте И его нет в списке выбранных?
        elif (len(layer) > 0) and not (l in layers_ids):
            patched_fig["data"].remove(layer[0])

    return patched_fig


@map_app.callback(
    Output("date_end", "min"),
    Output("date_start", "max"),
    Output("map", "figure", allow_duplicate=True),
    Input("date_start", "value"),
    Input("date_end", "value"),
    Input("select_main_layer", "value"),
    Input("map", "figure"),
    prevent_initial_call=True,
)
def adjust_min_end_date(date_start, date_end, selected_trace, fig):
    """Устанавливает минимальное значение конца выбранного периода равным началу периода."""
    patched_fig = Patch()
    patched_fig = patch_main_trace(
        fig, selected_trace, patched_fig, date_start, date_end
    )
    return date_start, date_end, patched_fig


if __name__ == "__main__":
    map_app.run(host="0.0.0.0", port=8050, debug=True)
