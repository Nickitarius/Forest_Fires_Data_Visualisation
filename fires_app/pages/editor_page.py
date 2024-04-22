"""Страница для редактирования данных в БД. Доступна только авторизованным администраторам. """

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(__name__, path="/editor")


layout = html.Div(dbc.Badge("Editor page"))
