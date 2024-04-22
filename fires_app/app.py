"""Файл с приложением-интерактивной картой."""

import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import MATCH, Dash, Input, Output, Patch, State, dcc, html

from fires_app import flask_app
from fires_app.services import fire_status_service, forestry_service
from fires_app.utils import db_trace_creators, json_trace_creators, map_utils

MAIN_TRACE_UID = "main_trace"

# HTML app
map_app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    server=flask_app,
    use_pages=True,
)
map_app.layout = html.Div(
    id="dsah_app_container",
    children=[
        html.Div(
            [
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}", href=page["relative_path"]
                    )
                )
                for page in dash.page_registry.values()
            ]
        ),
        dash.page_container,
    ],
)

# Callbacks

if __name__ == "__main__":
    map_app.run(host="0.0.0.0", port=8050, debug=True)
