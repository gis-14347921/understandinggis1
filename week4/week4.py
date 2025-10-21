from geopandas import read_file

# open a dataset of all countries in the world
world = read_file("C:/Users/14256/Documents/GitHub/data/natural-earth/ne_10m_admin_0_countries.shp")

# extract the UK, project, and extract the geometry
uk = world[world["ISO_A3"] == "GBR"].to_crs(epsg=27700).geometry.iloc[0]	# COMPLETE THIS LINE

# report geometry type
print(f"geometry type: {uk.geom_type}")
  
from sys import exit

# quit the analysis if we are dealing with any geometry but a MultiPolygon
if uk.geom_type != 'MultiPolygon':
  print("Geometry is not a MultiPolygon, exiting...")
  exit()
  
# initialise variables to hold the coordinates and area of the largest polygon
biggest_area = 0
coord_list = []

# loop through each polygon in the multipolygon and find the biggest (mainland Great Britain)
for poly in uk.geoms:

	# if it is the biggest so far
    if poly.area > biggest_area:   

        # store the new value for biggest area
        biggest_area = poly.area
        
        # store the coordinates of the polygon
        coord_list = list(poly.boundary.coords)   

# test outputs
print(f"Biggest area: {biggest_area}")
print(f"Number of coordinates in largest polygon: {len(coord_list)}")