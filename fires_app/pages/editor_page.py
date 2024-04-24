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
                html.Div(
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        dbc.InputGroup(
                                            children=[
                                                dbc.InputGroupText(
                                                    "Тип редактируемых данных "
                                                ),
                                                dbc.Select(
                                                    id="data_type_select",
                                                    options=[
                                                        {
                                                            "value": "fires",
                                                            "label": "Пожары",
                                                        }
                                                    ],
                                                    value="fires",
                                                    # class_name="",
                                                ),
                                            ],
                                            # className="sm-3",
                                        )
                                    ],
                                    # className="sm-3",
                                ),
                                dbc.Col(
                                    children=[
                                        dbc.Button(
                                            "Добавить",
                                            color="secondary",
                                            # class_name=" btn-sm",
                                        ),
                                    ],
                                ),
                                dbc.Col(
                                    children=[
                                        dbc.Button(
                                            "Очистить",
                                            color="warning",
                                            # class_name=" btn-sm",
                                        ),
                                    ],
                                ),
                                dbc.Col(
                                    children=[
                                        dbc.Button(
                                            "Сохранить",
                                            color="primary",
                                            # class_name=" btn-sm",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                    className="mb-3",
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
                dcc.Upload(
                    id="datatable-upload",
                    children=html.Div(
                        ["Загрузите файл для ", html.A("предварительного просмотра.")]
                    ),
                    style={
                        "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                    },
                ),
            ],
            style={"padding": 50},
        )
    ]
)
