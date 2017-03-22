from pyproj import Proj, transform
import geohash
from osgeo import ogr
from datetime import datetime
import os


class Hash:
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

        self.burglary = {'BURGP','PROWLP'}

        self.street_crime = {'ASSLTP','ASSLTW','DISTP','DISTW','GANG','ROBP','ROBW','SHOOTW','SHOTS','STABW','THRETP','THRETW','VICE'}

        self.auto_theft = {'RSTLN','VEHSTP','VEHREC'}
        return 0

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

    def decode(self, value):
        """
        decode geohash value to latitude, longitude
        :param value: geohash value to be decoded
        :return: latitude, longitude pair for the center of the given geohash
        """
        return geohash.decode(value)

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
            i += 1
            hashcode = self.encode(x, y, precision)
            feature.SetField('geohash', hashcode)
            layer.SetFeature(feature)
            feature = layer.GetNextFeature()
        return 0

    @staticmethod
    def add_crime_tag(self, file):
        source = ogr.Open(file, update=True)
        layer = source.GetLayer()
        if layer.FindFieldIndex('crime_tag', True) == -1:
            new_field = ogr.FieldDefn('crime_tag', ogr.OFTString)
            layer.CreateField(new_field)
        feature = layer.GetNextFeature()
        i = 0
        while feature:
            crime = layer[i].GetField('final_case')
            if crime in self.burglary:
                feature.SetField('crime_tag', 'burglary')
            elif crime in self.auto_theft:
                feature.SetField('crime_tag', 'auto_theft')
            elif crime in self.street_crime:
                feature.SetField('crime_tag', 'street_crime')
            else:
                feature.SetField('crime_tag', 'other')
            layer.SetFeature(feature)
            i += 1
            feature = layer.GetNextFeature()
        return 0

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
            if(line.GetField('occ_date') == None or line.GetField('geohash') == None or line.GetField('final_case') == None):
                continue

            out_put.write(line.GetField('occ_date'))
            out_put.write('_')
            out_put.write(line.GetField('geohash'))
            out_put.write('_')
            type = line.GetField('final_case')
            out_put.write(type)
            out_put.write('\n')
        out_put.close()
        return 0

    @staticmethod
    def crime_type(self, shapefile, textfile):
        source = ogr.Open(shapefile, update=False)
        layer = source.GetLayer()
        if layer.FindFieldIndex('CALL_GROUP', True) == -1:
            return -1
        if layer.FindFieldIndex('CASE_DESC', True) == -1:
            return -2
        if layer.FindFieldIndex('final_case', True) == -1:
            print("fields are missing. fail to generate text file")
            return -3

        out_put = open(textfile, 'w')

        for line in layer:
            if(line.GetField('CALL_GROUP') == None or line.GetField('CASE_DESC') == None or line.GetField('final_case') == None):
                continue

            out_put.write(line.GetField('CALL_GROUP').replace(' ',''))
            out_put.write('_')
            out_put.write(line.GetField('final_case').replace(' ',''))
            out_put.write('_')
            type = line.GetField('CASE_DESC').replace(' ','')
            out_put.write(type)
            out_put.write('\n')
        out_put.close()
        return 0

    @staticmethod
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

    @staticmethod
    def all_area(self, directory, output_file):

        area = set()
        for root, dirs, files in os.walk(directory):
            for name in dirs:
                file = directory + '/' + name + '/' + name + '.shp'
                source = ogr.Open(file, update=True)
                layer = source.GetLayer()
                for line in layer:
                    area.add(line.GetField('geohash'))

        out_put = open(output_file, 'w')
        for element in area:
            out_put.write(element)
            out_put.write('\n')

    @staticmethod
    def geohash_to_grid_point(self, geohash_list_file, output_file):
        hash_file = geohash_list_file
        with open(hash_file) as f:
            content = f.readlines()
        geo_dict = {}
        for i in range(0, len(content)):
            cur_code = content[i][:6]
            geo_dict.update({cur_code: geohash.decode(cur_code)})

        latitude = set()
        longitude = set()
        for key in geo_dict:
            latitude.add(geo_dict[key][0])
            longitude.add(geo_dict[key][1])

        latitude = list(latitude)
        latitude.sort()
        longitude = list(longitude)
        longitude.sort()

        output = open(output_file, 'w')
        for key in geo_dict:
            lat = geo_dict[key][0]
            lng = geo_dict[key][1]
            output.write(key)
            output.write('\t')
            output.write(str(latitude.index(lat)))
            output.write('\t')
            output.write(str(longitude.index(lng)))
            output.write('\n')

        return 0



