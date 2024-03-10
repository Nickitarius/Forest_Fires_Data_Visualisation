from dash import Dash, Input, Output, callback, dash_table, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
import plotly
import plotly.graph_objects as go
import plotly.express as px
import shapely
import shapely.geometry as geometry


def pd_to_gpd_w_geom(df):
    """Transforms Pandas DF to Geopandas DF, reading geometry stored as WKB from 'geom' field"""
    geoms = []
    for shape in df['geom']:
        geoms.append(shapely.from_wkb(shape))

    gdf = gpd.GeoDataFrame(df, geometry=geoms, crs="EPSG:4326")
    return gdf


def repalce_geometry_with_wkb(gdf):
    """Recieves GeoPandas DF, deletes geometry, writes WKB based on it instead"""
    wkb = gdf.geometry.to_wkb(hex=True)
    gdf.drop(columns=['geometry'], inplace=True)
    gdf.rename(columns={'poly': 'geom'}, inplace=True)
    gdf['geom'] = wkb
    return gdf


def get_coords_linestring(gdf):
    """Get coords from a GeoPandas DF"""
    lats = []
    lons = []
    for i in gdf['geometry']:
        lons = lons+i.coords.xy[0].tolist()
        lats = lats+i.coords.xy[1].tolist()
        lons.append(None)
        lats.append(None)

    return lats, lons


def load_forest_quarters():
    """Loads forest quarters from JSON"""
    file_name = "user_schema.lesnye_kv_3051.json"
    path_to_json = my_data_path + "Лесные кварталы/" + file_name
    quaters_df = pd_to_gpd_w_geom(pd.read_json(path_to_json))
    return quaters_df
    # quarter_map_trace = px.choropleth_mapbox(quaters_df, geojson=quaters_df.geometry,
    #                                          locations=quaters_df.index, mapbox_style="carto-positron",
    #                                          center=quaters_df, zoom=quaters_df, opacity=0.25,
    #                                          color_discrete_sequence=px.colors.qualitative.Set1
    #                                          #    color=gdf_valid['name_in'],
    #                                          #    labels={'name_in': 'name'}
    #                                          ).data[0]
    # return quarter_map_trace


def load_localities():
    file_name = "localities_Irk_obl.geojson"
    path_to_json = my_data_path + file_name
    df = gpd.read_file(path_to_json)
    return df


my_data_path = '../MY data/'
# Map options
map_background_options = ["carto-positron", "open-street-map"]
map_options = {'map_center_start': {"lat": 52.25, "lon": 104.3},
               'map_zoom_start': 6,
               'opacity': 0.15,
               'mapbox_style': map_background_options[0]}


df_loc = load_localities()
map_fig = px.choropleth_mapbox(df_loc, geojson=df_loc.geometry, locations=df_loc.index,
                               mapbox_style=map_options['mapbox_style'],
                               opacity=map_options['opacity'],
                               center=map_options['map_center_start'],
                               zoom=map_options['map_zoom_start'],
                               labels={'type': 'Тип'},
                               hover_name='name',
                               #    hover_data={'type'},
                               color_discrete_sequence=['yellow']
                               )

map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
map_fig.show()

# Incorporate data
# df = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
# )

# Initialize the app - incorporate a Dash Bootstrap theme
# external_stylesheets = [dbc.themes.CERULEAN]
# app = Dash(__name__, external_stylesheets=external_stylesheets)

# # App layout
# app.layout = dbc.Container(
#     [
#         dbc.Row(
#             [
#                 html.Div(
#                     "My First App with Data, Graph, and Controls",
#                     className="text-primary text-center fs-3",
#                 )
#             ]
#         ),
#         dbc.Row(
#             [
#                 dbc.RadioItems(
#                     options=[
#                         {"label": x, "value": x}
#                         for x in ["pop", "lifeExp", "gdpPercap"]
#                     ],
#                     value="lifeExp",
#                     inline=True,
#                     id="radio-buttons-final",
#                 )
#             ]
#         ),
#         dbc.Row(
#             [
#                 dbc.Col(
#                     [
#                         dash_table.DataTable(
#                             data=df.to_dict("records"),
#                             page_size=12,
#                             style_table={"overflowX": "auto"},
#                         )
#                     ],
#                     width=6,
#                 ),
#                 dbc.Col([dcc.Graph(figure={}, id="my-first-graph-final")], width=6),
#             ]
#         ),
#     ],
#     fluid=True,
# )


# # Add controls to build the interaction
# @callback(
#     Output(component_id="my-first-graph-final", component_property="figure"),
#     Input(component_id="radio-buttons-final", component_property="value"),
# )
# def update_graph(col_chosen):
#     fig = px.histogram(df, x="continent", y=col_chosen, histfunc="avg")
#     return fig


# # Run the app
# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=False)
