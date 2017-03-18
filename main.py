from DataPreprocess.hash import hash

my_hash = hash()

# directory = "/home/tianxiaopian/Documents/cs536/course_project/project_data/crime_data/unzipped"
# for root, dirs, files in os.walk(directory):
#     for name in dirs:
#         file = directory + '/' + name + '/' + name + '.shp'
#         my_hash.add_geohash(file, 6)
#         my_hash.day_geo_type(file, './' + name + '.txt')


file = "/home/tianxiaopian/Desktop/NIJ2017_FEB28/NIJ2017_FEB28.shp"
my_hash.add_geohash(file,6)

