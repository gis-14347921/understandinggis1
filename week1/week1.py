from geopandas import read_file

world = read_file("C:/Users/14256/Documents/GitHub/data/natural-earth/ne_50m_admin_0_countries.shp")

print(world.head())

from matplotlib.pyplot import subplots, savefig
# create map axis object
my_fig, my_ax = subplots(1, 1, figsize=(16, 10))

# plot the countries onto ax
world.plot(ax = my_ax)

# save the result
savefig('out/1.png')
print("done!")

# turn off the visible axes on the map
my_ax.axis('off')

graticule = read_file("C:/Users/14256/Documents/GitHub/data/natural-earth/ne_110m_graticules_15.shp")
bbox = read_file("C:/Users/14256/Documents/GitHub/data/natural-earth/ne_110m_wgs84_bounding_box.shp")


ea_proj = "+proj=eqearth +lon_0=0 +datum=WGS84 +units=m +no_defs"

# reproject all three layers to equal earth
world = world.to_crs(ea_proj)
graticule = graticule.to_crs(ea_proj)
bbox = bbox.to_crs(ea_proj)

world['pop_density'] = world['POP_EST'] / (world.area / 1000000)

my_ax.set(title="Population Density: <WGS84> Coordinate Reference System")

# add bounding box and graticule layers
bbox.plot(
    ax = my_ax,
    color = 'lightgray',
    linewidth = 0,
    )

# plot the countries
world.plot(
    ax = my_ax,
    color = 'black',
    linewidth = 0.5,
    )

# plot the graticule
graticule.plot(
    ax = my_ax,
    color = 'white',
    linewidth = 0.5,
    )

print(world.columns)



# plot the countries
world.plot(								
# plot the world dataset
    ax = my_ax,						
# specify the axis object to draw it to
    column = 'pop_density',		
# specify the column used to style the dataset
    cmap = 'OrRd',				
# specify the colour map used to style the dataset based on POP_EST
    scheme = 'quantiles',	
# specify how the colour map will be mapped to the values in POP_EST
    linewidth = 0.5,			
# specify the line width for the country outlines
    edgecolor = 'gray',		
# specify the line colour for the country outlines
legend = True,
legend_kwds = {
    'loc': 'lower left',
    'title': 'Population Density'    
    }
)

#GDP
# 1. Read data --------------------------------------------------------------
world = read_file("C:/Users/14256/Documents/GitHub/data/natural-earth/ne_50m_admin_0_countries.shp")
graticule = read_file("C:/Users/14256/Documents/GitHub/data/natural-earth/ne_110m_graticules_15.shp")
bbox = read_file("C:/Users/14256/Documents/GitHub/data/natural-earth/ne_110m_wgs84_bounding_box.shp")

# 3. Define Equal Earth projection string -----------------------------------------
ea_proj = '+proj=eqearth +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'

# 4. Reproject --------------------------------------------------------------
world = world.to_crs(ea_proj)
graticule = graticule.to_crs(ea_proj)
bbox = bbox.to_crs(ea_proj)

# 5. Calculate GDP per capita (GDP / population) -----------------------------------------
# Natural Earth provides GDP_MD_EST (GDP in million USD) and POP_EST (population)
world['gdp_per_capita'] = (world['GDP_MD_EST'] * 1e6) / world['POP_EST']   # USD per capita

# 6. Create canvas ------------------------------------------------------------
my_fig, my_ax = subplots(1, 1, figsize=(16, 10))

# 7. Draw base map elements --------------------------------------------------------
bbox.plot(ax=my_ax, color='lightgray', linewidth=0)
graticule.plot(ax=my_ax, color='white', linewidth=0.5)

# 8. Draw choropleth map of GDP per capita ---------------------------------------------
world.plot(
    ax=my_ax,
    column='gdp_per_capita',
    cmap='OrRd',              # Orange-Red colormap for GDP per capita
    scheme='quantiles',       # Quantile classification
    linewidth=0.5,
    edgecolor='gray',
    legend=True,
    legend_kwds={
        'loc': 'lower left',
        'title': 'GDP per capita (USD)'
    }
)

# 9. Title and details ----------------------------------------------------------
my_ax.set(title="GDP per Capita: Equal Earth Coordinate Reference System")
my_ax.axis('off')

# 10. Save result -----------------------------------------------------------
savefig('out/gdp_per_capita.png', dpi=300, bbox_inches='tight')
print("done! → out/gdp_per_capita.png")