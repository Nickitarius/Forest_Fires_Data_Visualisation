"""Файл с приложением-интерактивной картой."""

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Dash, Input, Output, Patch, State, dcc, html

from fires_app import flask_app
from fires_app.services import forestry_service
from fires_app.utils import db_trace_creators, json_trace_creators

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
    """Заменяет слой данных в графике с данным uid на новый слой."""
    old_trace = [item for item in fig["data"] if item["uid"] == uid]
    if len(old_trace) > 0:
        patch["data"].remove(old_trace[0])

    patch["data"].append(new_trace)
    return patch


def patch_main_layer(fig, layer, date_start, date_end, forestries=None):
    """Меняет главный слой в данных графика."""
    patch = Patch()
    match layer:
        case "fires":
            new_trace = db_trace_creators.create_fires_trace(
                MAIN_TRACE_UID, date_start, date_end, forestries
            )

    patch = replace_trace_by_uid(fig, patch, MAIN_TRACE_UID, new_trace)
    return patch


def get_forestries_options(lang="ru"):
    """Возвращает списки имён и"""
    forestries = forestry_service.get_all_forestries()
    options = []
    if lang == "ru":
        for f in forestries:
            option = {"value": f.id, "label": f.name_ru}
            options.append(option)

    elif lang == "en":
        for f in forestries:
            option = {"value": f.id, "label": f.name_en}
            options.append(option)

    return options


map_fig = go.Figure()
default_trace = db_trace_creators.create_fires_trace(
    MAIN_TRACE_UID, "2017-01-01", "2021-12-31"
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

# Выбор основного слоя
dom_main_layer_select = dbc.Select(
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

# Выбор лесничества
forestry_options = get_forestries_options()
dom_forestries_dropdown = dcc.Dropdown(
    id="forestries_dropdown",
    options=forestry_options,
    value=forestry_options[0]["value"],
    multi=True,
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
        value="select",
    )
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
                dbc.Label("Слой данных", html_for="select_main_layer"),
                dom_main_layer_select,
                dbc.Label("Прозрачность", html_for="opacity_slider"),
                dom_opacity_slider,
            ]
        ),
        html.Hr(),
        dom_date_choice,
        html.Hr(),
        dbc.Label("Выбор лесничеств", html_for="forestry_dropdown"),
        dom_select_deselct_all_forestries,
        dom_forestries_dropdown,
    ],
    style={
        "padding": 10,
        # "flex-direction": "column"
    },
    className="col-sm-2",
)

# HTML app
map_app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=flask_app)
map_app.layout = html.Div(
    id="map_app",
    children=[
        dom_control_panel,
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
)


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
    Input("date_start", "value"),
    Input("date_end", "value"),
    prevent_initial_call=True,
)
def adjust_min_end_date(date_start, date_end):
    """
    Устанавливает минимальное значение конца выбранного периода
    равным началу периода.
    """
    return (
        date_start,
        date_end,
    )


@map_app.callback(
    Output("map", "figure", allow_duplicate=True),
    Input("map", "figure"),
    Input("date_start", "value"),
    Input("date_end", "value"),
    Input("select_main_layer", "value"),
    Input("forestries_dropdown", "value"),
    prevent_initial_call=True,
)
def set_main_layer(
    fig,
    date_start,
    date_end,
    selected_trace,
    forestries,
):
    """
    Устанавливает гланый слой данных на карте
    в соответствии с input'ами.
    """
    patched_fig = patch_main_layer(
        fig, selected_trace, date_start, date_end, forestries
    )
    return patched_fig


@map_app.callback(
    Output("forestries_dropdown", "value"),
    Input("select_deselct_all_button", "n_clicks"),
    State("forestries_dropdown", "value"),
    State("forestries_dropdown", "options"),
    prevent_initial_call=True,
)
def select_deselect_all_forestries(selected_values, options):
    """Выбирает или удаляет все объекты из dropdown'а."""
    all_options = [option["value"] for option in options]
    # Если выбран только один вариант, то вместо списка значение будет просто строкой/числом
    if isinstance(selected_values, list):
        if len(selected_values) == len(all_options):
            return []

    return all_options


@map_app.callback(
    Output("select_deselct_all_button", "children"),
    Input("forestries_dropdown", "value"),
    State("forestries_dropdown", "options"),
    prevent_initial_call=True,
)
def set_select_deselct_button_text(selected_values, options):
    """
    Устанавливает текст кнопки в зависимости от значений
    соответствующего dropdown'a.
    """
    all_options = [option["value"] for option in options]
    # Если выбран только один вариант, то вместо списка значение будет просто строкой/числом
    if isinstance(selected_values, list):
        if len(selected_values) == len(all_options):
            return "Удалить все"

    return "Выбрать все"


if __name__ == "__main__":
    map_app.run(host="0.0.0.0", port=8050, debug=True)
