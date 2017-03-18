from pyproj import Proj, transform
import geohash
from osgeo import ogr
from datetime import datetime

class hash:
    def __init__(self):
        self.neighbor = [['p0r21436x8zb9dcf5h7kjnmqesgutwvy', 'bc01fg45238967deuvhjyznpkmstqrwx'],
                    ['14365h7k9dcfesgujnmqp0r2twvyx8zb', '238967debc01fg45kmstqrwxuvhjyznp'],
                    ['bc01fg45238967deuvhjyznpkmstqrwx', 'p0r21436x8zb9dcf5h7kjnmqesgutwvy'],
                    ['238967debc01fg45kmstqrwxuvhjyznp', '14365h7k9dcfesgujnmqp0r2twvyx8zb']]

        self.border = [['prxz', 'bcfguvyz'],
                  ['028b', '0145hjnp'],
                  ['bcfguvyz', 'prxz'],
                  ['0145hjnp', '028b']]

        self.base = '0123456789bcdefghjkmnpqrstuvwxyz'
        return


    def xy_to_coord(self, x, y):
        """
        project x, y coordinate to google map coordinate
        :param x: x coordinate, NAD 1983 HARN StatePlane Oregon North FIPS 3601 Feet Intl
        :param y: y coordinate, NAD 1983 HARN StatePlane Oregon North FIPS 3601 Feet Intl
        :return: longitude, latitude
        """
        inProj = Proj(init="epsg:3646", preserve_units=True)  # NAD 1983 HARN StatePlane Oregon North FIPS 3601 Feet Intl
        outProj = Proj(init="epsg:4326")  # google map
        lng, lat = transform(inProj, outProj, x, y)
        return lng, lat


    def encode(self, x, y, precision = 12):
        """
        generate geohash value from x,y cooridnate, NAD 1983 HARN StatePlane Oregon North FIPS 3601 Feet Intl
        :param x: x coordinate, NAD 1983 HARN StatePlane Oregon North FIPS 3601 Feet Intl
        :param y: y coordinate, NAD 1983 HARN StatePlane Oregon North FIPS 3601 Feet Intl
        :param precision: geohash grid size
        :return: geohash value
        """
        lng, lat = self.xy_to_coord(x,y)
        return geohash.encode(lat, lng, precision)


    def add_geohash(self, file, precision=12):
        """
        set geohash for each feature in shapefile
        :param file: shapefile name
        :param precision: geohash grid size
        :return: 0
        """
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
            hashcode = self.encode(x, y, precision)
            feature.SetField('geohash', hashcode)
            layer.SetFeature(feature)
            feature = layer.GetNextFeature()
        return 0


    def delete_field(self, file, field_name):
        """
        delete specified field from shapefile, if exists
        :param file: shape filename
        :param field_name: field name
        :return: 0 if delete successful, -1 otherwise
        """
        source = ogr.Open(file, update=True)
        layer = source.GetLayer()
        index = layer.FindFieldIndex(field_name, True)
        if index == -1:
            print('field does not exist')
            return -1
        layer.DeleteField(index)
        print('field is deleted')
        return 0


    def print_fields(self, file):
        """
        print all field names of the specified shapefile
        :param file: shapefile name
        :return: 0
        """
        source = ogr.Open(file, update=False)
        layer = source.GetLayer()
        layer_defn = layer.GetLayerDefn()
        field_names = []
        for i in range(layer_defn.GetFieldCount()):
            field_names.append(layer_defn.GetFieldDefn(i).GetName())
        print(field_names)
        return 0


    def add_field(self, file, field_name, field_type = ogr.OFTString):
        """
        add specified field to shape file
        :param file: shapefile, str
        :param field_name: new field name to be added, str
        :param field_type: field type, ogr defined types
        :return: 0 if add successfully, -1 otherwise
        """
        source = ogr.Open(file, update=True)
        layer = source.GetLayer()
        if layer.FindFieldIndex(field_name, True) == -1:
            new_field = ogr.FieldDefn(field_name, field_type)
            layer.CreateField(new_field)
            print("new field is added")
            return 0
        print("field already exist, no new field is added")
        return -1


    def days_diff(self, d1, d2):
        """
        calculate date difference
        :param d1: date string with format m/d/Y
        :param d2: date string with format m/d/Y
        :return: date difference between d1 and d2, int
        """
        d1 = datetime.strptime(d1, '%m/%d/%Y')
        d2 = datetime.strptime(d2, '%m/%d/%Y')
        return (d1-d2).days


    def date_geo_type(self, shapefile, textfile):
        source = ogr.Open(shapefile, update=False)
        layer = source.GetLayer()
        if layer.FindFieldIndex('geohash', True) == -1:
            return -1
        if layer.FindFieldIndex('occ_date', True) == -1:
            return -2
        if layer.FindFieldIndex('final_case', True) == -1:
            print("fields are missing. fail to generate text file")
            return -3

        out_put = open(textfile, 'w')

        for line in layer:
            out_put.write(line.GetField('occ_date'))
            out_put.write('_')
            out_put.write(line.GetField('geohash'))
            out_put.write('_')
            type = line.GetField('final_case')
            if len(type) >= 4:
                out_put.write(type[:4])
            else:
                out_put.write(type)
            out_put.write('\n')
        out_put.close()
        return 0

    def geo_neighbor(self, geohash, direction):
        """
        calculate the neighbor of geohash on direction
        :param geohash: lower case geohash code, str
        :param direction: str, valid values: 'n', 'e', 'w', 's'
        :return: neighbor geohash
        """
        directions = {'n':0, 's':1, 'e':2, 'w':3}
        dir = directions[direction]

        lastCh = geohash[-1]
        parent = geohash[:-1]

        type = len(geohash) % 2

        # check for edge-case which does not share common prefix
        if lastCh not in self.border[dir][type] and parent != '':
            parent = self.geo_neighbor(parent, direction)

        # append letter for direction to parent
        return parent + self.base[self.neighbor[dir][type].index(lastCh)]



my_hash = hash()
file = "/home/tianxiaopian/Desktop/NIJ2017_FEB28/NIJ2017_FEB28.shp"
my_hash.add_geohash(file,6)
