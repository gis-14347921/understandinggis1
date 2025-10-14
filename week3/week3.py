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