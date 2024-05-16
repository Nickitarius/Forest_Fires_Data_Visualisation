"""Содержит функции для работы с данными карты."""

from datetime import date

import dash_bootstrap_components as dbc
import geopandas as gpd
from dash import Patch, dcc, html
from geoalchemy2 import shape
from shapely import geometry

from fires_app.services import fire_service, fire_status_service, forestry_service
from fires_app.utils import db_trace_creators


def replace_trace_by_uid(fig, patch, uid, new_trace):
    """Заменяет слой данных в графике с данным uid на новый слой."""
    old_trace = [item for item in fig["data"] if item["uid"] == uid]
    if len(old_trace) > 0:
        patch["data"].remove(old_trace[0])

    patch["data"].append(new_trace)
    return patch


def patch_main_layer(
    fig,
    layer,
    trace_uid,
    date_start,
    date_end,
    forestries=None,
    fire_statuses=None,
    fire_area_min=0,
    fire_area_max=1000,
):
    """Меняет главный слой в данных графика."""
    patch = Patch()
    match layer:
        case "fires":
            new_trace = db_trace_creators.create_fires_trace(
                trace_uid,
                date_start,
                date_end,
                forestries,
                fire_statuses,
                fire_area_min,
                fire_area_max,
            )

    patch = replace_trace_by_uid(fig, patch, trace_uid, new_trace)
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


def get_fire_statuses_options():
    """Возвращает списки имён и"""
    statuses = fire_status_service.get_all_fire_statuses()
    options = []
    for f in statuses:
        option = {"value": f.id, "label": f.name}
        options.append(option)

    return options


def get_fire_info_DOM(fire_id):
    """Возвращает DOM с описанием объекта."""
    fire = fire_service.get_fire(fire_id)
    coords = shape.to_shape(fire.coords)

    if fire.fire_status.id == 10:
        status_color = "green"
    elif fire.fire_status.id == 11:
        status_color = "orange"
    else:
        status_color = "green"

    duration_days = (fire.date_end - fire.date_start).days + 1
    res = html.Div(
        id="object_info",
        children=[
            html.H5("Пожар", className="display-6"),
            html.H6("Код"),
            html.P(fire.code),
            html.H6("Статус"),
            html.P(fire.fire_status.name, style={"color": status_color}),
            html.H6("Координаты"),
            html.P(f"{round(coords.y, 4)} N; {round(coords.x, 4)} E"),
            html.H6("Дата начала"),
            html.P(str(fire.date_start)),
            html.H6("Дата окончания"),
            html.P(str(fire.date_end)),
            html.H6("Продолжительность, дней"),
            html.P(duration_days),
            html.H6("Лесничество"),
            html.P(fire.forestry.name_ru),
            html.H6("Площадь общая, кв. км."),
            html.P(fire.area_all),
            html.H6("Площадь леса, кв. км."),
            html.P(fire.area_forest),
            html.H6("Площадь лесофонда общая, кв. км."),
            html.P(fire.area_lesofond_all),
            html.H6("Площадь лесофонда — лес, кв. км."),
            html.P(fire.area_lesofond_forest),
            html.H6("Площадь регистровая, кв. км."),
            html.P(fire.area_registr),
        ],
    )

    return res
