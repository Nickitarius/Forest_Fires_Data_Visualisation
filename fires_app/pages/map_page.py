"""Интерактивная карта. Доступна всем пользователям. """

import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import MATCH, Input, Output, Patch, State, callback, dcc, html

from fires_app.utils import db_trace_creators, json_trace_creators, map_utils

MAP_BACKGROUND_OPTIONS = ["open-street-map", "carto-positron", "carto-darkmatter"]
# Опции карты по-умолчанию, в т.ч. опции input'ов
DEFAULT_MAP_OPTIONS = {
    "map_center_start": {"lat": 52.25, "lon": 104.3},
    "map_zoom_start": 6,
    "opacity": 25,
    "mapbox_style": MAP_BACKGROUND_OPTIONS[0],
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
    value=DEFAULT_MAP_OPTIONS["opacity"],
)

# Выбор основного слоя
dom_main_layer_select = dbc.Select(
    id="main_layer_select",
    options=[
        {"label": "Пожары", "value": "fires"},
        {"label": "Риски пожаров", "value": "fire_risks"},
    ],
    value="fires",
)

# Выбор дат
dom_dates_input = html.Div(
    id="dates_choice",
    children=[
        dbc.Label("Период"),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Начало"),
                dbc.Input(
                    id="date_start",
                    value="2017-01-01",
                    type="date",
                ),
            ],
            class_name="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Конец"),
                dbc.Input(
                    id="date_end",
                    value="2021-12-31",
                    type="date",
                ),
            ],
            class_name="mb-3",
        ),
    ],
)

# Выбор лесничества
forestry_options = map_utils.get_forestry_options()
dom_forestries_dropdown = html.Div(
    children=[
        dcc.Dropdown(
            id={"type": "dropdown_w_all", "index": "forestries"},
            options=forestry_options,
            value=forestry_options[0]["value"],
            multi=True,
            placeholder="Выбор...",
            # className="form-control",
            className="dbc",
        )
    ],
)
# Кнопка выбора всех лесничеств для dom_forestries_dropdown
dom_select_all_forestries = html.Div(
    dbc.Button(
        # id="select_all_forestries",
        id={"type": "select_all_button", "index": "forestries"},
        children="Выбрать все",
        color="secondary",
        outline=True,
        class_name="mb-3",
        size="sm",
        # type="select_all_button",
        # inde
    )
)

# Выбор статусов пожаров
fire_statuses = map_utils.get_fire_status_options()
dom_fire_statuses_dropdown = dcc.Dropdown(
    id="fire_statuses_dropdown",
    # id={"type": "dropdown_w_all", "index": "fire_statuses"},
    options=fire_statuses,
    value=fire_statuses[0]["value"],
    multi=True,
    placeholder="Выбор...",
)

# Площадь пожаров - макс/мин
dom_area_input = html.Div(
    [
        dbc.Label("Площадь пожаров, кв. км.:"),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Мин."),
                dbc.Input(id="min_area_input", type="number", min=0, value=0),
            ],
            class_name="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Макс."),
                dbc.Input(id="max_area_input", type="number", min=0, value=1000),
            ],
            class_name="mb-3",
        ),
    ],
    id="area_input",
)

# Выбор типов территорий
territory_types = map_utils.get_territory_type_options()
dom_territory_types_dropdown = dcc.Dropdown(
    id={"type": "dropdown_w_all", "index": "territory_types"},
    options=territory_types,
    value=territory_types[0]["value"],
    multi=True,
    placeholder="Выбор...",
)
dom_select_all_territory_types = html.Div(
    dbc.Button(
        # id="select_all_territory_types",
        id={"type": "select_all_button", "index": "territory_types"},
        children="Выбрать все",
        color="secondary",
        outline=True,
        class_name="mb-3",
        size="sm",
    )
)

# Базовые функции панели управления
dom_basic_controls = html.Div(
    id="basic_controls",
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
    ],
)

# Элементы для фильтрации пожаров
dom_fires_controls = html.Div(
    id="fires_controls",
    children=[
        dom_dates_input,
        html.Hr(),
        dbc.Label("Выбор лесничеств", html_for="forestry_dropdown"),
        dom_select_all_forestries,
        dom_forestries_dropdown,
        html.Hr(),
        dbc.Label("Выбор статуса пожаров", html_for="fire_statuses_dropdown"),
        dom_fire_statuses_dropdown,
        html.Hr(),
        dom_area_input,
        html.Hr(),
        dbc.Label("Выбор типов территорий"),
        dom_select_all_territory_types,
        dom_territory_types_dropdown,
    ],
)

dom_fire_risks_controls = html.Div(id="fire_risks_controls")

# Панель управления
dom_control_panel = html.Div(
    id="map-control-panel",
    children=[
        dom_basic_controls,
        html.Hr(),
        html.Div(id="layer_control"),
    ],
    style={
        "padding": 10,
    },
    className="col-sm-2",
)

# Карта
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
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
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
        "width": "100%",
    },
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

# Страница в целом
layout = dbc.Card(
    id="map_app",
    children=[
        dbc.CardBody(
            children=[
                dom_control_panel,
                html.Div(className="vr"),
                dom_graph,
                html.Div(className="vr"),
                dom_object_info_panel,
            ],
            style={
                "display": "flex",
                "flexDirection": "row",
            },
        ),
    ],
)


@callback(Output("layer_control", "children"), Input("main_layer_select", "value"))
def set_main_layer_controls(layer_name):
    "Создаёт элементы управления для выбранного слоя."
    match layer_name:
        case "fires":
            return dom_fires_controls
        case "fire_risks":
            return dom_fire_risks_controls


@callback(
    Output("map", "figure"),
    Input("select_background", "value"),
    prevent_initial_call=True,
)
def set_mapbox_background(background_name):
    """Устанавливает подложку карты."""
    patched_fig = Patch()
    patched_fig["layout"]["mapbox"]["style"] = background_name
    return patched_fig


@callback(
    Output("map", "figure", allow_duplicate=True),
    Input("checklist_layers", "value"),
    State("map", "figure"),
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


@callback(
    Output("date_end", "min"),
    Output("date_start", "max"),
    Input("date_start", "value"),
    Input("date_end", "value"),
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


@callback(
    Output("map", "figure", allow_duplicate=True),
    State("map", "figure"),
    # Пожар
    Input("date_start", "value"),
    Input("date_end", "value"),
    Input("main_layer_select", "value"),
    Input({"type": "dropdown_w_all", "index": "forestries"}, "value"),
    Input(dom_fire_statuses_dropdown, "value"),
    Input("min_area_input", "value"),
    Input("max_area_input", "value"),
    Input({"type": "dropdown_w_all", "index": "territory_types"}, "value"),
    Input("opacity_slider", "value"),
    prevent_initial_call=True,
)
def patch_main_layer(
    fig,
    date_start,
    date_end,
    selected_trace,
    forestries,
    fire_statuses,
    min_area,
    max_area,
    territory_types,
    opacity,
):
    """
    Устанавливает гланый слой данных на карте
    в соответствии с input'ами.
    """
    patched_fig = map_utils.patch_main_layer(
        fig,
        selected_trace,
        MAIN_TRACE_UID,
        date_start,
        date_end,
        forestries,
        fire_statuses,
        min_area,
        max_area,
        territory_types,
        opacity=opacity / 100,
    )
    return patched_fig


@callback(
    Output({"type": "dropdown_w_all", "index": MATCH}, "value"),
    Input({"type": "select_all_button", "index": MATCH}, "n_clicks"),
    State({"type": "dropdown_w_all", "index": MATCH}, "value"),
    State({"type": "dropdown_w_all", "index": MATCH}, "options"),
    prevent_initial_call=True,
)
def select_deselect_all(n_clicks, selected_values, options):
    """Выбирает или удаляет все объекты из dropdown'а."""
    all_options = [option["value"] for option in options]
    # Если выбран только один вариант, то вместо списка значение будет просто строкой/числом
    if isinstance(selected_values, list):
        if len(selected_values) == len(all_options):
            return []

    return all_options


@callback(
    Output({"type": "select_all_button", "index": MATCH}, "children"),
    Input({"type": "dropdown_w_all", "index": MATCH}, "value"),
    State({"type": "dropdown_w_all", "index": MATCH}, "options"),
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


@callback(
    Output("object_info_panel", "children"),
    Input("map", "clickData"),
    State("main_layer_select", "value"),
    prevent_initial_call=True,
)
def display_clicked_object_data(click_data, selected_layer):
    """Отображает данные о выбранном объекте в панели."""
    clicked_object_id = click_data["points"][0]["customdata"][0]
    match selected_layer:
        case "fires":
            patch = map_utils.get_fire_info_DOM(clicked_object_id)
        case _:
            patch = html.Div()

    patch = map_utils.get_fire_info_DOM(clicked_object_id)
    return patch


@callback(
    Output("map", "figure", allow_duplicate=True),
    Input("opacity_slider", "value"),
    State("map", "figure"),
    prevent_initial_call=True,
)
def set_opacity(value, fig):
    """Устанавливает прозрачность слоя данных."""
    patched_fig = Patch()
    # Значение делится на 100, т.к. в слайдере задаётся процент от 0 до 100,
    # который нужно перевести в дробь
    # layer = [item for item in fig["data"] if item["uid"] == MAIN_TRACE_UID][0]
    # patched_fig["data"].remove(layer)
    # print(layer)
    trace = map_utils.find_trace_by_uid(fig, MAIN_TRACE_UID)
    new_trace = trace
    new_trace["marker"]["opacity"] = value / 100
    print(trace)
    patched_fig = map_utils.replace_trace_by_uid(
        fig, patched_fig, MAIN_TRACE_UID, new_trace
    )
    # patched_fig["data"].append(new_layer)
    return patched_fig
