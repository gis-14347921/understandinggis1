from geopandas import read_file

world = read_file("C:/Users/14256/Documents/GitHub/data/natural-earth/ne_50m_admin_0_countries.shp")

print(world.head())