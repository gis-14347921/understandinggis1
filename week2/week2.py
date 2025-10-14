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
#print(total)

from geopandas import read_file, GeoSeries

# load the shapefile of countries - this gives a table of 12 columns and 246 rows (one per country)
world = read_file("C:/Users/14256/Documents/GitHub/data/natural-earth/ne_10m_admin_0_countries.shp")

# print a list of all of the columns in the shapefile
#print(world.columns)

# extract the country rows as a GeoDataFrame object with 1 row
usa = world.loc[(world.ISO_A3 == 'USA')]

#print(type(usa))

# extract the geometry columns as a GeoSeries object
usa_col = usa.geometry

#print(type(usa_col))

# extract the geometry objects themselves from the GeoSeries
usa_geom = usa_col.iloc[0]

#print(type(usa_geom))

# extract the country rows as a GeoDataFrame object with 1 row
mex = world.loc[(world.ISO_A3 == 'MEX')]

#print(type(mex))

# extract the geometry columns as a GeoSeries object
mex_col = mex.geometry

#print(type(mex_col))

# extract the geometry objects themselves from the GeoSeries
mex_geom = mex_col.iloc[0]

#print(type(mex_geom))

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
    
    #print(cumulative_length)
   
# open the graticule dataset
graticule = read_file(r"C:/Users/14256/Documents/GitHub/data/natural-earth\ne_110m_graticules_5.shp")
# create map axis object
my_fig, my_ax = subplots(1, 1, figsize=(16, 10))

# remove axes
my_ax.axis('off')

# set title
title(f"Trump's wall would have been {cumulative_length / 1000:.2f} km long.")

lambert_conic = '+proj=lcc +lat_0=30 +lat_1=30 +lon_0=-100 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs'

# project border
border_series = GeoSeries(border, crs=world.crs).to_crs(lambert_conic)

# extract the bounds from the (projected) GeoSeries Object
minx, miny, maxx, maxy = border_series.geometry.iloc[0].bounds

# set bounds (10000m buffer around the border itself, to give us some context)
buffer = 10000
my_ax.set_xlim([minx - buffer, maxx + buffer])
my_ax.set_ylim([miny - buffer, maxy + buffer])

# plot data
usa.to_crs(lambert_conic).plot(
    ax = my_ax,
    color = '#ccebc5',
    edgecolor = '#4daf4a',
    linewidth = 0.5,
    )
mex.to_crs(lambert_conic).plot(
    ax = my_ax,
    color = '#fed9a6',
    edgecolor = '#ff7f00',
    linewidth = 0.5,
    )
border_series.plot(     
# note that this has already been projected above!
    ax = my_ax,
    color = '#984ea3',
    linewidth = 2,
    )
graticule.to_crs(lambert_conic).plot(
    ax=my_ax,
    color='grey',
    linewidth = 1,
    )

# save the result
savefig('out/2.png', bbox_inches='tight')
print("done!")

# add north arrow
x, y, arrow_length = 0.98, 0.99, 0.1
my_ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
	arrowprops=dict(facecolor='black', width=5, headwidth=15),
	ha='center', va='center', fontsize=20, xycoords=my_ax.transAxes)

from matplotlib_scalebar.scalebar import ScaleBar

# add scalebar
my_ax.add_artist(ScaleBar(dx=1, units="m", location="lower left", length_fraction=0.25))