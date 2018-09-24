import folium
import branca
import numpy as np
from geopandas import GeoDataFrame, GeoSeries

class InconsistantGeometry(Exception):
    pass

class InputError(Exception):
    pass


def attach_points(dataframe, foliumMap, color_field=None, size_field=None, color='red',size=3, cm=branca.colormap.linear.YlGnBu, sm=[1,6], svr=None, weight=1):
    if color_field:
        vmin = dataframe[color_field].min()
        vmax = dataframe[color_field].max()
        colorscale = cm.scale(vmin, vmax)
    if size_field:
        if svr:
            sizescale = svr
        else:
            smin = dataframe[size_field].min()
            smax = dataframe[size_field].max()
            sizescale = [smin, smax]
    if isinstance(dataframe, GeoDataFrame) and not dataframe.geometry.empty:
        geom_name = dataframe.geometry.name
        for index, row in dataframe.iterrows():
            geom = row[geom_name]
            c = colorscale(row[color_field]) if color_field else color
            s = np.interp(row[size_field], sizescale, sm) if size_field else size
            if geom.geom_type == 'Point':
                marker = folium.CircleMarker([geom.y, geom.x], radius=s, fill=True, fill_color=c, fill_opacity=0.7,
                                             weight=0)
                marker.add_to(foliumMap)
            else:
                raise InconsistantGeometry('Geometry should be point feature')
    elif isinstance(dataframe, GeoSeries):
        for geom in dataframe:
            if geom.geom_type == 'Point':
                marker = folium.CircleMarker([geom.y, geom.x], radius=size, fill=True, fill_color=color, fill_opacity=0.7, weight=0)
                marker.add_to(foliumMap)
            else:
                raise InconsistantGeometry('Geometry should be point feature')
    else:
        raise InputError('Data input should be pandas geo table')
    return foliumMap

def attach_lines(dataframe, foliumMap, color_field=None, size_field=None, color='red',size=3, cm=branca.colormap.linear.YlGnBu, sm=[1,6], svr=None,weight=1):
    if color_field:
        vmin = dataframe[color_field].min()
        vmax = dataframe[color_field].max()
        colorscale = cm.scale(vmin, vmax)
    if size_field:
        if svr:
            sizescale = svr
        else:
            smin = dataframe[size_field].min()
            smax = dataframe[size_field].max()
            sizescale = [smin, smax]
    if isinstance(dataframe, GeoDataFrame) and not dataframe.geometry.empty:
        geom_name = dataframe.geometry.name
        for index, row in dataframe.iterrows():
            geom = row[geom_name]
            c = colorscale(row[color_field]) if color_field else color
            s = np.interp(row[size_field], sizescale, sm) if size_field else size
            if geom.geom_type == 'LineString':
                xs = list(geom.coords.xy[0])
                ys = list(geom.coords.xy[1])
                polyline = folium.PolyLine([list(zip(ys, xs))], color=c, weight=s)
                polyline.add_to(foliumMap)
            else:
                raise InconsistantGeometry('Geometry should be line feature')
    elif isinstance(dataframe, GeoSeries):
        for geom in dataframe:
            if geom.geom_type == 'LineString':
                xs = list(geom.coords.xy[0])
                ys = list(geom.coords.xy[1])
                polyline = folium.PolyLine([list(zip(ys, xs))], color=color, weight=weight)
                polyline.add_to(foliumMap)
            else:
                raise InconsistantGeometry('Geometry should be line feature')
    else:
        raise InputError('Data input should be pandas geo table')

