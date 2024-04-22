"""Основное приложение. """

import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import (
    MATCH,
    Dash,
    Input,
    Output,
    Patch,
    State,
    clientside_callback,
    dcc,
    html,
)

from fires_app import flask_app
from fires_app.services import fire_status_service, forestry_service
from fires_app.utils import db_trace_creators, json_trace_creators, map_utils

MAIN_TRACE_UID = "main_trace"

# HTML app
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
        dbc.icons.BOOTSTRAP,
    ],
    server=flask_app,
    use_pages=True,
)

# Ссылки на страницы
nav_items = [
    dbc.NavItem(dbc.NavLink(page["name"], href=page["relative_path"]))
    for page in dash.page_registry.values()
]

color_mode_switch = html.Span(
    [
        dbc.Label(className="bi bi-moon-fill", html_for="color_mode_switch"),
        dbc.Switch(
            id="color_mode_switch",
            value=True,
            className="d-inline-block ms-1",
            persistence=True,
            style={"padding-y": "-8px"},
        ),
        dbc.Label(className="bi bi-sun", html_for="color_mode_switch"),
    ],
    className="d-inline-flex",
    style={"padding-y": "-8px"},
)

nav_items.append(color_mode_switch)

navbar = dbc.NavbarSimple(
    children=nav_items,
    brand="Fires Data Visualiser",
    brand_href="#",
    color="dark",
    dark=True,
    # light=True,
)

app.layout = dbc.Container(
    id="dash_app_container",
    children=[
        navbar,
        dash.page_container,
    ],
    # class_name="container-xxl",
    fluid=True,
    style={"padding": 0},
)

clientside_callback(
    """
    (switchOn) => {
       switchOn
         ? document.documentElement.setAttribute('data-bs-theme', 'light')
         : document.documentElement.setAttribute('data-bs-theme', 'dark')
       return window.dash_clientside.no_update
    }
    """,
    Output("color_mode_switch", "id"),
    Input("color_mode_switch", "value"),
)

# Callbacks

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
