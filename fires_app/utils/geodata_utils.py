"""Функции для работы с геоданными в json/geojson и датафреймах pandas и geopandas."""

import geopandas as gpd
import pandas as pd
import shapely

from fires_app import DATA_PATH


def pd_to_gpd_w_geom(df):
    """
    Transforms Pandas DF to Geopandas DF,
    reading geometry stored as WKB from 'geom' field.
    """
    geoms = []
    for shape in df["geom"]:
        geoms.append(shapely.from_wkb(shape))

    gdf = gpd.GeoDataFrame(df, geometry=geoms, crs="EPSG:4326")
    return gdf


def repalce_geometry_with_wkb(gdf):
    """
    Recieves GeoPandas DF, deletes geometry,
    writes WKB based on it instead.
    """
    wkb = gdf.geometry.to_wkb(hex=True)
    gdf.drop(columns=["geometry"], inplace=True)
    gdf.rename(columns={"poly": "geom"}, inplace=True)
    gdf["geom"] = wkb
    return gdf


def get_coords_linestring(gdf):
    """Get coords from a GeoPandas DF."""
    lats = []
    lons = []
    for i in gdf["geometry"]:
        lons = lons + i.coords.xy[0].tolist()
        lats = lats + i.coords.xy[1].tolist()
        # Так надо для разделения координат разных фигур
        lons.append(None)
        lats.append(None)

    return lats, lons


def load_geo_from_geojson(file_name):
    """Загружает географические данные из GEOJSON."""
    path_to_json = DATA_PATH + file_name
    df = gpd.read_file(path_to_json)
    return df


def load_geo_from_json(file_name):
    """Загружает географические данные из обычного JSON."""
    path_to_json = DATA_PATH + file_name
    df = pd_to_gpd_w_geom(pd.read_json(path_to_json))
    return df
