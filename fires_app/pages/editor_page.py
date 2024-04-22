"""Страница для редактирования данных в БД. Доступна только авторизованным администраторам. """

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, dcc, html

from fires_app.services import fire_service
from fires_app.utils import db_trace_creators

dash.register_page(__name__, path="/editor", name="Редактор данных")

forestries = 1
# fires = fire_service.get_fires_limited_data("2017-01-01", "2021-01-01", forestries)
fires_df = db_trace_creators.create_fires_df("2017-01-01", "2021-01-01", forestries)

print(fires_df)

fires_df.rename(
    columns={
        "lat": "Широта",
        "lon": "Долгота",
        "code": "Код",
        "date_start": "Дата начала",
        "date_end": "Дата окончания",
        "fire_status": "Статус",
    },
    inplace=True,
)

layout = dbc.Container(
    children=[
        html.Div(
            children=[
                dbc.InputGroup(
                    children=[
                        dbc.InputGroupText("Тип редактируемых данных "),
                        dbc.Select(
                            id="data_type_select",
                            options=[{"value": "fires", "label": "Пожары"}],
                            value="fires",
                            # class_name="",
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    children=[
                        dbc.InputGroup(
                            children=[
                                dbc.InputGroupText("Начало периода"),
                                dbc.Input(
                                    id="date_start",
                                    value="2017-01-01",
                                    type="date",
                                ),
                            ],
                            className="col mb-3",
                        ),
                        dbc.InputGroup(
                            children=[
                                dbc.InputGroupText("Конец периода"),
                                dbc.Input(
                                    id="date_end",
                                    value="2021-12-31",
                                    type="date",
                                ),
                            ],
                            className="col mb-3",
                        ),
                    ],
                    class_name="",
                ),
                dash_table.DataTable(
                    id="table",
                    data=fires_df.to_dict("records"),
                    columns=[{"name": i, "id": i} for i in fires_df.columns],
                    editable=True,
                    row_deletable=True,
                    sort_action="native",
                    filter_action="native",
                    row_selectable="multi",
                    page_action="native",
                    page_current=0,
                    page_size=20,
                ),
            ],
            style={"padding": 50},
        )
    ]
)
