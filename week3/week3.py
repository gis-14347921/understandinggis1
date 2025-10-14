from math import sqrt

def distance(x1, y1, x2, y2):
    """
    * Use Pythagoras' theorem to measure the distance. This is acceptable in this case because:
    *	 - the CRS of the data is a local projection
    *	 - the distances are short
    *  - computational efficiency is important (as we are making many measurements)
    """
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Test the function with the given coordinates
result = distance(345678, 456789, 445678, 556789)
print(f"{result:.2f}")

from geopandas import read_file

# read in shapefiles, ensure that they all have the same CRS
pop_points = read_file("C:/Users/14256/Documents/GitHub/data/gulu/pop_points.shp")
water_points = read_file("C:/Users/14256/Documents/GitHub/data/gulu/water_points.shp")
gulu_district = read_file("C:/Users/14256/Documents/GitHub/data/gulu/district.shp")

print(pop_points.crs.to_epsg())
print(water_points.crs.to_epsg())
print(gulu_district.crs.to_epsg())

# read in the `water_points` dataset AND transform it the the same CRS as `pop_points`
water_points = read_file("C:/Users/14256/Documents/GitHub/data/gulu/water_points.shp").to_crs(pop_points.crs)

print(f"population points: {len(pop_points.index)}")
print(f"Initial wells: {len(water_points.index)}")

from shapely import STRtree

# get the geometries from the water points geodataframe as a list
geoms = water_points.geometry.to_list()

# initialise an instance of an STRtree using the geometries
idx = STRtree(geoms)

# get the one and only polygon from the district dataset
polygon = gulu_district.geometry.iloc[0]

# how many rows are we starting with?
print(f"Initial wells: {len(water_points.index)}")

# get the indexes of wells that intersect bounds of the district
possible_matches_index = idx.query(polygon)

# use those indexes to extract the possible matches from the GeoDataFrame
possible_matches = water_points.iloc[possible_matches_index]

# how many rows are left now? 
print(f"Potential wells: {len(possible_matches.index)}")

precise_matches = possible_matches.loc[possible_matches.within(polygon)]

print(f"Filtered wells: {len(precise_matches.index)}")
