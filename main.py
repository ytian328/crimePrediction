from DataPreprocess.hash import Hash
import os
import geohash
from osgeo import ogr
my_hash = Hash()

directory = "/home/tianxiaopian/Documents/cs536/course_project/project_data/crime_data/unzipped"
# for root, dirs, files in os.walk(directory):
#     for name in dirs:
#         file = directory + '/' + name + '/' + name + '.shp'
#         my_hash.add_geohash(file, 6)
#         my_hash.add_crime_tag(file)
#         print("done")



# decode each hash value
hash_file = "./areas.txt"
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

output = open('./areas grid', 'w')
for key in geo_dict:
    lat = geo_dict[key][0]
    lng = geo_dict[key][1]
    output.write(key)
    output.write('\t')
    output.write(str(latitude.index(lat)))
    output.write('\t')
    output.write(str(longitude.index(lng)))
    output.write('\n')

