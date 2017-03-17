from pyproj import Proj, transform
import xlrd
import geohash




inProj = Proj(init="epsg:3646", preserve_units=True) # NAD 1983 HARN StatePlane Oregon North FIPS 3601 Feet Intl
outProj = Proj(init="epsg:4326") # google map

x,y = 7637348, 708028
lng, lat = transform(inProj, outProj, x,y)

for i in range(1,13):
    hashcode = geohash.encode(lat, lng, i)
    print(hashcode)


file = "/home/tianxiaopian/Desktop/022817_Data/NIJ2017_FEB28.xlsx"
#
# workbook = xlrd.open_workbook(file).sheet_by_index(0)
#
# xy = []
# for i, row in enumerate(range(workbook.nrows)):
#     if i<=0:
#         continue
#     r = []
#     r.append(workbook.cell_value(i,5))
#     r.append(workbook.cell_value(i,6))
#     xy.append(r)
#
# file = "/home/tianxiaopian/Documents/cs536/course_project/project_data/crime_data/2015/NIJ2015_JAN01_DEC31.xlsx"
#
# workbook = xlrd.open_workbook(file).sheet_by_index(0)
# list = []
# for i, row in enumerate(range(workbook.nrows)):
#     if i<=0:
#         continue
#     list.append(workbook.cell_value(i,7))



