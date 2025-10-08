# here is your list of numbers
numbers = [1,2,3,4,5,6,7,8,9,10,15,30]

# this variable will hold your result, start it at 0
total = 0

# MISSING LINE HERE
# loop through the list
for num in numbers:
    # INCOMPLETE LINE HERE
    # add each number to the total
    total += num

# print the result
print(total)

from geopandas import read_file, GeoSeries

# load the shapefile of countries - this gives a table of 12 columns and 246 rows (one per country)
world = read_file("C:/Users/14256/Documents/GitHub/data/natural-earth/ne_10m_admin_0_countries.shp")

# print a list of all of the columns in the shapefile
print(world.columns)

# extract the country rows as a GeoDataFrame object with 1 row
usa = world.loc[(world.ISO_A3 == 'USA')]

print(type(usa))

# extract the geometry columns as a GeoSeries object
usa_col = usa.geometry

print(type(usa_col))

# extract the geometry objects themselves from the GeoSeries
usa_geom = usa_col.iloc[0]

print(type(usa_geom))

# extract the country rows as a GeoDataFrame object with 1 row
mex = world.loc[(world.ISO_A3 == 'MEX')]

print(type(mex))

# extract the geometry columns as a GeoSeries object
mex_col = mex.geometry

print(type(mex_col))

# extract the geometry objects themselves from the GeoSeries
mex_geom = mex_col.iloc[0]

print(type(mex_geom))

# calculate the intersection of the geometry objects
border = usa_geom.intersection(mex_geom)

from matplotlib.pyplot import subplots, savefig, title

# create map axis object
my_fig, my_ax = subplots(1, 1, figsize=(16, 10))

# remove axes
my_ax.axis('off')

# plot the border
GeoSeries(border).plot(
  ax = my_ax
	)

# save the image
savefig('C:/Users/14256/Documents/GitHub/understandinggis1/week2/out/first-border.png')

from pyproj import Geod

# set which ellipsoid you would like to use
g = Geod(ellps='WGS84')

print(border)

# loop through each segment in the line and print the coordinates
for segment in border.geoms:
	print(f"from:{segment.coords[0]}\tto:{segment.coords[1]}")
    
# initialise a variable to hold the cumulative length
cumulative_length = 0

# loop through each segment in the line
for segment in border.geoms:
    # Extract coordinates of start and end points
    start_lon, start_lat = segment.coords[0]  # Start point coordinates
    end_lon, end_lat = segment.coords[1]      # End point coordinates
    
    # Calculate the ellipsoidal distance between two points (get only the distance value, index 2)
    distance = g.inv(start_lon, start_lat, end_lon, end_lat)[2]


	# add the distance to our cumulative total
    cumulative_length += distance
    
    print(cumulative_length)
   
    