"""Основное приложение. """

import dash
import dash_bootstrap_components as dbc
from dash import MATCH, Dash, Input, Output, clientside_callback, html

from fires_app import flask_app

MAIN_TRACE_UID = "main_trace"

# HTML app
dash_app = Dash(
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

color_mode_switch = html.Div(
    [
        dbc.Label(className="bi bi-moon", html_for="color_mode_switch", color="light"),
        dbc.Switch(
            id="color_mode_switch",
            value=False,
            class_name="d-inline-block ms-1",
            persistence=True,
            style={"padding-y": "-8px"},
        ),
        dbc.Label(class_name="bi bi-sun", html_for="color_mode_switch", color="light"),
    ],
    className="form-check form-check-inline",
    style={"padding-top": "0.5em"},
)


nav_items.append(color_mode_switch)

nav_items.append(
    dbc.Button(
        id="log_in_button_nav", color="warning", outline=True, children=["Войти"]
    )
)

navbar = dbc.NavbarSimple(
    children=nav_items,
    brand="Fires Data Visualiser",
    brand_href="#",
    color="dark",
    dark=True,
    # light=True,
)

dash_app.layout = dbc.Container(
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
    dash_app.run(host="0.0.0.0", port=8050, debug=True)
