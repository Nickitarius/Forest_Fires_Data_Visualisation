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


def load_localities():
    file_name = "localities_Irk_obl.geojson"
    path_to_json = my_data_path + file_name
    df = gpd.read_file(path_to_json)
    return df


def load_rail():
    file_name = "zhd_roads.geojson"
    path_to_json = my_data_path + "/metadata/" + file_name
    df = gpd.read_file(path_to_json)
    return df


def load_rivers():
    file_name = 'rivers.geojson'
    path_to_json = my_data_path + "/metadata/" + file_name
    df = gpd.read_file(path_to_json)
    return df


def load_roads():
    file_name = 'auto_roads.geojson'
    path_to_json = my_data_path + "/metadata/" + file_name
    df = gpd.read_file(path_to_json)
    return df


def load_loc_buffers():
    file_name = 'localities_buffers.json'
    path_to_json = my_data_path + "/MY buffers/" + file_name
    df = pd_to_gpd_w_geom(pd.read_json(path_to_json))
    return df


def load_road_buffers():
    file_name = 'roads_buffers.json'
    path_to_json = my_data_path + "/MY buffers/" + file_name
    df = pd_to_gpd_w_geom(pd.read_json(path_to_json))
    return df


def load_river_buffers():
    file_name = 'rivers_buffers.json'
    path_to_json = my_data_path + "/MY buffers/" + file_name
    df = pd_to_gpd_w_geom(pd.read_json(path_to_json))
    return df


my_data_path = '../../MY data/'
# Map options
map_background_options = ["carto-positron", "open-street-map"]
map_options = {'map_center_start': {"lat": 52.25, "lon": 104.3},
               'map_zoom_start': 6, 'opacity': 0.15,
               'mapbox_style': map_background_options[0],
               'width': 1900, 'height': 800}


df_loc = load_localities()
map_loc = px.choropleth_mapbox(df_loc, geojson=df_loc.geometry, locations=df_loc.index,
                               mapbox_style=map_options['mapbox_style'],
                               opacity=map_options['opacity'],
                               center=map_options['map_center_start'],
                               zoom=map_options['map_zoom_start'],
                               labels={'type': 'Тип'},
                               hover_name='name',
                               #    hover_data={'type'},
                               color_discrete_sequence=['yellow']
                               ).update_traces(name="map_loc")
map_loc.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, width=1900,
                      height=800)

df_rail = load_rail()
lats, lons = get_coords_linestring(df_rail)
map_rail = px.line_mapbox(df_rail, lat=lats, lon=lons,
                          color_discrete_sequence=['black'],
                          ).update_traces(name="map_rail", hovertemplate=None, hoverinfo='skip',).data[0]

df_rivers = load_rivers()
lats, lons = get_coords_linestring(df_rivers)
map_rivers = px.line_mapbox(df_rivers, lat=lats, lon=lons,
                            color_discrete_sequence=['blue'],
                            ).update_traces(name="map_rivers", line={'width': 1}, hovertemplate=None, hoverinfo='skip',).data[0]

df_roads = load_roads()
lats, lons = get_coords_linestring(df_roads)
map_roads = px.line_mapbox(df_roads, lat=lats, lon=lons,
                           color_discrete_sequence=['orange'],
                           ).update_traces(name="map_roads", line={'width': 2}, hovertemplate=None, hoverinfo='skip',).data[0]


df_loc_buf = load_loc_buffers()
map_loc_buf = px.choropleth_mapbox(df_loc_buf, geojson=df_loc_buf.geometry, locations=df_loc_buf.index,
                                   opacity=0.5,
                                   labels={'type': 'Тип'},
                                   #    hover_name='name',
                                   #    hover_data={'type'},
                                   color_discrete_sequence=['orange'],
                                   ).update_traces(name="map_loc_buf", visible=False).data[0]


df_road_buf = load_road_buffers()
map_roads_buf = px.choropleth_mapbox(df_road_buf, geojson=df_road_buf.geometry,
                                     locations=df_road_buf.index,
                                     opacity=0.5,
                                     labels={'type': 'Тип'},
                                     #    hover_name='name',
                                     #    hover_data={'type'},
                                     color_discrete_sequence=['yellow'],
                                     ).update_traces(name="map_roads_buf", visible=False).data[0]

df_rivers_buf = load_river_buffers()
map_rivers_buf = px.choropleth_mapbox(df_rivers_buf, geojson=df_rivers_buf.geometry,
                                      locations=df_rivers_buf.index,
                                      opacity=0.5,
                                      labels={'type': 'Тип'},
                                      #    hover_name='name',
                                      #    hover_data={'type'},
                                      color_discrete_sequence=['yellow'],
                                      ).update_traces(name="map_rivers_buf", visible=False).data[0]

comb_fig = go.Figure(map_loc)  # 0
comb_fig.add_trace(map_rivers)  # 1
comb_fig.add_trace(map_rail)  # 2
comb_fig.add_trace(map_roads)  # 3

# comb_fig.add_trace(map_loc_buf)  # 4
# comb_fig.add_trace(map_roads_buf)  # 5
# comb_fig.add_trace(map_rivers_buf)  # 6

# comb_fig.update_traces(visible=False, selector={})

app = Dash()
app.layout = html.Div([
    dcc.Graph(id="map", figure=comb_fig,)
],
    style={"margin": 10, "maxWidth": "100%", "height": "90vh"}
)

app.run_server(host='0.0.0.0', debug=True)
