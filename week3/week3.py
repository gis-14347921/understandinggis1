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
pop_points = read_file("#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assessment 1 – A Race Around the World!
Find the shortest international border and map it.

Usage: python shortest_border.py
Requires: geopandas, shapely, pyproj, matplotlib
Data: ../data/natural-earth/ne_10m_admin_0_countries.shp
"""
import time, pathlib, sys
import geopandas as gpd
from shapely.geometry import LineString, MultiLineString
from shapely.ops import unary_union
from shapely import make_valid
from pyproj import Geod
import matplotlib.pyplot as plt

# ------------------------- helpers -------------------------
def geodesic_length_wgs84(geom) -> float:
    """Return geodesic length (meters) along WGS84 for LineString/MultiLineString."""
    geod = Geod(ellps="WGS84")
    def seg_len(ls: LineString) -> float:
        x, y = ls.xy
        if len(x) < 2: return 0.0
        return geod.line_length(x, y)
    if isinstance(geom, LineString): return seg_len(geom)
    if isinstance(geom, MultiLineString): return sum(seg_len(ls) for ls in geom.geoms)
    return 0.0

def clean_country_shapes(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Basic cleaning: valid geometries, drop empties, dissolve by ADMIN (avoid slivers)."""
    gdf = gdf[~gdf.geometry.is_empty & gdf.geometry.notnull()].copy()
    gdf["geometry"] = gdf.geometry.apply(lambda g: make_valid(g))
    # Optional: remove Antarctica (no neighbors) to save cycles
    if "ADMIN" in gdf.columns:
        gdf = gdf[gdf["ADMIN"] != "Antarctica"]
    # Dissolve by ADMIN to unify multipart records
    gdf = gdf.dissolve(by="ADMIN", as_index=False)
    return gdf

def shared_border(a, b):
    """Return shared boundary (LineString/MultiLineString) between two polygons; None if only point-touch."""
    inter = a.boundary.intersection(b.boundary)
    if inter.is_empty: return None
    if isinstance(inter, (LineString, MultiLineString)) and inter.length > 0:
        return inter
    return None

# ------------------------- main -------------------------
def main():
    t0 = time.time()
    root = pathlib.Path(__file__).resolve().parent
    shp = root / "../data/natural-earth/ne_10m_admin_0_countries.shp"
    outdir = (root / "outputs"); outdir.mkdir(parents=True, exist_ok=True)
    out_png = outdir / "shortest_border.png"
    out_txt  = outdir / "shortest_border.txt"

    try:
        countries = gpd.read_file(shp)
    except Exception as e:
        sys.exit(f"Error reading shapefile at {shp}:\n{e}")

    # ensure lon/lat for geodesic
    if countries.crs is None:
        countries.set_crs(4326, inplace=True)
    else:
        countries = countries.to_crs(4326)

    countries = clean_country_shapes(countries)[["ADMIN","geometry"]]

    # spatial join (touches) to get candidate neighbors quickly
    # (touches includes line or point touching; we’ll filter to line-only later)
    try:
        nbrs = gpd.sjoin(
            countries, countries,
            how="inner", predicate="touches", lsuffix="a", rsuffix="b"
        )[["ADMIN_a","ADMIN_b","geometry"]]
    except TypeError:
        # GeoPandas <0.10 fallback: predicate='intersects' then post-filter
        cand = gpd.sjoin(countries, countries, how="inner", op="intersects",
                         lsuffix="a", rsuffix="b")
        nbrs = cand[cand["ADMIN_a"] != cand["ADMIN_b"]][["ADMIN_a","ADMIN_b","geometry"]]

    # drop self-pairs and duplicates (A,B) vs (B,A)
    nbrs = nbrs[nbrs["ADMIN_a"] != nbrs["ADMIN_b"]].copy()
    nbrs["key"] = nbrs.apply(lambda r: tuple(sorted((r["ADMIN_a"], r["ADMIN_b"]))), axis=1)
    nbrs = nbrs.drop_duplicates(subset="key")

    # map admin name -> geometry for quick lookup
    geom_map = dict(zip(countries["ADMIN"], countries.geometry))

    best = {"len_m": float("inf"), "a": None, "b": None, "line": None}

    for _, row in nbrs.iterrows():
        a, b = row["ADMIN_a"], row["ADMIN_b"]
        # quick bbox pre-check via sindex is already implicit in sjoin; compute exact shared boundary
        line = shared_border(geom_map[a], geom_map[b])
        if not line: 
            continue  # point-touch only
        L = geodesic_length_wgs84(line)
        if 0 < L < best["len_m"]:
            best.update({"len_m": L, "a": a, "b": b, "line": line})

    if not best["line"]:
        sys.exit("No international borders found (line contacts). Check input data.")

    # ------------------------- map -------------------------
    fig, ax = plt.subplots(figsize=(8, 6), dpi=200)
    # subtle base
    countries.boundary.plot(ax=ax, linewidth=0.3, alpha=0.5)
    # highlight the two countries
    countries[countries["ADMIN"].isin([best["a"], best["b"]])].plot(
        ax=ax, edgecolor="black", linewidth=0.8, alpha=0.4
    )
    # draw the border
    gpd.GeoSeries([best["line"]], crs=4326).plot(ax=ax, linewidth=3)
    ttl = (f"Shortest International Border (WGS84 geodesic): "
           f"{best['a']} — {best['b']} = {best['len_m']:.1f} m")
    ax.set_title(ttl)
    ax.set_axis_off()
    plt.tight_layout()
    fig.savefig(out_png, bbox_inches="tight")
    plt.close(fig)

    # write a tiny text result (handy for automated marking)
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(f"{best['a']},{best['b']},{best['len_m']:.3f}\n")

    print(ttl)
    print(f"Map saved to: {out_png}")
    print(f"Runtime: {time.time()-t0:.2f}s")

if __name__ == "__main__":
    main()
data/gulu/pop_points.shp")
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

# rebuild the spatial index using the new, smaller dataset
geoms = precise_matches.geometry.to_list()
idx = STRtree(geoms)

from shapely.strtree import STRtree

idx = STRtree(water_points.geometry)

distances = []

# loop through each population point
for id, house in pop_points.iterrows():

    # loop through each population point
    nearest_well_index = idx.nearest(house.geometry)

    # use the spatial index to get the closest well object from the original dataset
    nearest_well_geom = water_points.iloc[nearest_well_index].geometry
 
    nearest_point = nearest_well_geom.geoms[0]

    # store the distance to the nearest well
    distances.append(
       distance(house.geometry.x, house.geometry.y,
                nearest_point.x, nearest_point.y)
   )
    
print("Number of distances calculated:", len(distances))

# store distance to nearest well
pop_points['nearest_well'] = distances

mean = sum(distances) / len(distances)

print(f"Minimum distance to water in Gulu District: {min(distances):,.0f}m.")
print(f"Mean distance to water in Gulu District: {mean:,.0f}m.")
print(f"Maximum distance to water in Gulu District: {max(distances):,.0f}m.")

from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.pyplot import subplots, savefig, title

# create map axis object
fig, my_ax = subplots(1, 1, figsize=(16, 10))

# remove axes
my_ax.axis('off')

# add title
title("Distance to Nearest Well, Gulu District, Uganda")

# add the district boundary
gulu_district.plot(
    ax = my_ax,
    color = (0, 0, 0, 0),
    linewidth = 1,
	edgecolor = 'black',		
    )

# plot the locations, coloured by distance to water
pop_points.plot(
    ax = my_ax,
    column = 'nearest_well',
    linewidth = 0,
	markersize = 1,
    cmap = 'RdYlBu_r',
    scheme = 'quantiles',
    legend = 'True',
    legend_kwds = {
        'loc': 'lower right',
        'title': 'Distance to Nearest Well'
        }
    )

# add north arrow
x, y, arrow_length = 0.98, 0.99, 0.1
my_ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
	arrowprops=dict(facecolor='black', width=5, headwidth=15),
	ha='center', va='center', fontsize=20, xycoords=my_ax.transAxes)

# add scalebar
my_ax.add_artist(ScaleBar(dx=1, units="m", location="lower left", length_fraction=0.25))

# save the result
savefig('out/3.png', bbox_inches='tight')
print("done!")

precise_matches = water_points.loc[water_points.within(polygon)]
# initialise an instance of an rtree Index object

print(f"Initial wells: {len(water_points.index)}")
print(f"Potential wells: {len(possible_matches.index)}")
print(f"Filtered wells: {len(precise_matches.index)}")

# ensure that the spatial index has been constructed
water_points.sindex

# report how many wells there are before the operation
print(f"Initial wells: {len(water_points)}")

# get the indexes of wells within the district polygon
precise_matches = water_points.loc[water_points.within(polygon)]

# report how many wells there are after the operation
print(f"Filtered wells: {len(water_points)}")

_, distances = precise_matches.sindex.nearest(pop_points.geometry, return_all=False, return_distance=True)

# origin：
distances = []
for id, house in pop_points.iterrows():
    nearest_well_index = idx.nearest(house.geometry)
    nearest_well = precise_matches.iloc[nearest_well_index].geometry.geoms[0]
    distances.append(distance(house.geometry.x, house.geometry.y, nearest_well.x, nearest_well.y))

# optimization：
nearest_indices, distances = precise_matches.sindex.nearest(
    pop_points.geometry, 
    return_all=False, 
    return_distance=True
)
