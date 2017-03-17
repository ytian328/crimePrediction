from pyproj import Proj, transform
import geohash
from osgeo import ogr


def xy_to_coord(x, y):
    inProj = Proj(init="epsg:3646", preserve_units=True)  # NAD 1983 HARN StatePlane Oregon North FIPS 3601 Feet Intl
    outProj = Proj(init="epsg:4326")  # google map
    lng, lat = transform(inProj, outProj, x, y)
    return lng, lat


def encode(x, y, precision = 12):
    lng, lat = xy_to_coord(x,y)
    return geohash.encode(lat, lng, precision)


def add_geohash(file, precision=12):
    # add geohash field to file if geohash field does not exist
    source = ogr.Open(file, update=True)
    layer = source.GetLayer()
    if layer.FindFieldIndex('geohash', True) == -1:
        new_field = ogr.FieldDefn('geohash', ogr.OFTString)
        layer.CreateField(new_field)
    # set geohash for each entry according to x,y coordinates
    feature = layer.GetNextFeature()
    i = 0
    while feature:
        x = layer[i].GetField('x_coordina')
        y = layer[i].GetField('y_coordina')
        i=i+1
        hashcode = encode(x, y, precision)
        feature.SetField('geohash', hashcode)
        layer.SetFeature(feature)
        feature = layer.GetNextFeature()
    return


def delete_field(file, field_name):
    source = ogr.Open(file, update=True)
    layer = source.GetLayer()
    index = layer.FindFieldIndex(field_name, True)
    if index == -1:
        print('field does not exist')
        return -1
    layer.DeleteField(index)
    print('field is deleted')
    return 0


def print_fields(file):
    source = ogr.Open(file, update=False)
    layer = source.GetLayer()
    layer_defn = layer.GetLayerDefn()
    field_names = []
    for i in range(layer_defn.GetFieldCount()):
        field_names.append(layer_defn.GetFieldDefn(i).GetName())
    print(field_names)
    return


def add_field(file, field_name, field_type = ogr.OFTString):
    source = ogr.Open(file, update=True)
    layer = source.GetLayer()
    if layer.FindFieldIndex(field_name, True) == -1:
        new_field = ogr.FieldDefn(field_name, field_type)
        layer.CreateField(new_field)
        print("new field is added")
        return 0
    print("field already exist, no new field is added")
    return -1


file = '/home/tianxiaopian/Documents/cs536/course_project/project_data/crime_data/2016/NIJ2016_JAN01_JUL31.shp'


add_geohash(file,6)



