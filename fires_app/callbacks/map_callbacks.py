from dash import Input, Output, Patch, State, callback, html

from fires_app.utils import db_trace_creators, json_trace_creators, map_utils

from fires_app.pages.map_page import MAIN_TRACE_UID, background_layers_ids


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


@callback(
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


@callback(
    Output("map", "figure", allow_duplicate=True),
    Input("map", "figure"),
    Input("date_start", "value"),
    Input("date_end", "value"),
    Input("main_layer_select", "value"),
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
    patched_fig = map_utils.patch_main_layer(
        fig, selected_trace, MAIN_TRACE_UID, date_start, date_end, forestries
    )
    return patched_fig


@callback(
    Output("forestries_dropdown", "value"),
    Input("select_deselct_all_button", "n_clicks"),
    State("forestries_dropdown", "value"),
    State("forestries_dropdown", "options"),
    prevent_initial_call=True,
)
def select_deselect_all_forestries(n_clicks, selected_values, options):
    """Выбирает или удаляет все объекты из dropdown'а."""
    all_options = [option["value"] for option in options]
    # Если выбран только один вариант, то вместо списка значение будет просто строкой/числом
    if isinstance(selected_values, list):
        if len(selected_values) == len(all_options):
            return []

    return all_options


@callback(
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


@callback(
    Output("object_info_panel", "children"),
    Input("map", "clickData"),
    State("main_layer_select", "value"),
    prevent_initial_call=True,
)
def display_clicked_object_data(click_data, selected_layer):
    """Отображает данные о выбранном объекте в панели."""
    clicked_object_id = click_data["points"][0]["customdata"][0]
    patch = Patch()
    # new_el = html.Div(clicked_object_id)
    match selected_layer:
        case "fires":
            patch = map_utils.get_fire_info_DOM(clicked_object_id)
        case _:
            patch = html.Div()

    patch = map_utils.get_fire_info_DOM(clicked_object_id)
    return patch
