from math import cos, sin, radians

def compute_offset(origin, distance, direction):
    """
    Compute the location of a point at a given distance and direction 
    from a specified location using trigonometry.
    """
    x1, y1 = origin
    theta = radians(direction)   # convert degrees to radians
    offset_x = x1 + cos(theta) * distance
    offset_y = y1 + sin(theta) * distance
    return (offset_x, offset_y)

# this code tests whether your function works correctly
origin = (345678, 456789)
destination = compute_offset(origin, 1011, 123)  # move 1011m in a direction of 123 degrees
print("CORRECT!!" if (int(destination[0]), int(destination[1])) == (345127, 457636) 
      else f"INCORRECT!! Error: {(int(destination[0])-345127, int(destination[1])-457636)}")

import geopandas as gpd  # Import GeoPandas

# Load the world countries shapefile
world = gpd.read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")

# Extract the row for Iceland (ISO_A3 == "ISL")
iceland = world[world["ISO_A3"] == "ISL"]

# Load the land cover shapefile for Iceland
land_cover = gpd.read_file("../../data/iceland/gis_osm_natural_a_free_1.shp")

# Extract only the glacier features
ice = land_cover[land_cover["fclass"] == "glacier"]

# Get the bounds of Iceland
minx, miny, maxx, maxy = iceland.total_bounds

# Print the bounds to verify
print(minx, miny, maxx, maxy)

from pyproj import Geod  # import pyproj for geodesic calculations

# Define the geographic CRS (geodesic model)
geo_string = "+proj=longlat +datum=WGS84 +no_defs"

# Initialise a Geod object with the WGS84 ellipsoid
g = Geod(ellps='WGS84')

# Create a list of projections to evaluate for distortion
projections = [
    {
        'name': "Web Mercator",
        'description': "Global Conformal",
        'proj': "+proj=merc +datum=WGS84 +no_defs"
    },
    {
        'name': "Eckert IV",
        'description': "Global Equal Area",
        'proj': "+proj=eck4 +datum=WGS84 +no_defs"
    },
    {
        'name': "Iceland Albers Equal Area",
        'description': "Local Equal Area",
        # Local equal-area projection centered on Iceland — created using Projection Wizard
        # (approx. settings: lat_1=63, lat_2=67, lat_0=65, lon_0=-19)
        'proj': "+proj=aea +lat_1=63 +lat_2=67 +lat_0=65 +lon_0=-19 +datum=WGS84 +units=m +no_defs"
    }
]

