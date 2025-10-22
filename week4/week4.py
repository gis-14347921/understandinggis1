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

# set the percentage of nodes that you want to remove
SIMPLIFICATION_PERC = 98

# how many nodes do we need?
n_nodes = int(len(coord_list) / 100.0 * (100 - SIMPLIFICATION_PERC))

# ensure that there are at least 3 nodes (minimum for a polygon)
if n_nodes < 3:
	n_nodes = 3 
    
from math import sqrt

# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def distance(x1, y1, x2, y2):
    """
    Calculate the straight-line (Euclidean) distance between two points.
    """
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


def get_effective_area(a, b, c):
    """
    Calculate the area of a triangle made from the points a, b and c using Heron's formula.
    https://en.wikipedia.org/wiki/Heron%27s_formula
    Parameters:
        a, b, c : tuples/lists of (x, y)
    Returns:
        float : area of the triangle
    """
    # calculate the length of each side
    side_a = distance(b[0], b[1], c[0], c[1])
    side_b = distance(a[0], a[1], c[0], c[1])
    side_c = distance(a[0], a[1], b[0], b[1])

    # calculate semi-perimeter of the triangle (perimeter / 2)
    s = (side_a + side_b + side_c) / 2

    # apply Heron's formula and return
    return sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))

def visvalingam_whyatt(node_list, n_nodes):
    """
    Simplify a line using the Visvalingam-Whyatt algorithm.
    node_list : list of coordinate pairs [(x, y), (x, y), ...]
    n_nodes : number of nodes to keep
    """

    # loop through each node, excluding the end points
    areas = []
    for i in range(1, len(node_list) - 1):

        # get the effective area using the nodes to the left and right
        area = get_effective_area(node_list[i - 1], node_list[i], node_list[i + 1])  # ✅ COMPLETED LINE

        # append the node and effective area to the list
        areas.append({"point": node_list[i], "area": area})

    # add the end points back in at the start (0) and end (len(areas))
    areas.insert(0, {"point": node_list[0], "area": 0})
    areas.insert(len(areas), {"point": node_list[len(node_list) - 1], "area": 0})

    # quick test - compare the number of nodes and the number of areas
    print(f"Number of original nodes: {len(node_list)}")
    print(f"Number of areas calculated: {len(areas)}")

    # (for now we don't return anything yet)
    return

# test call (no simplification yet, just to check your setup)
simplified_nodes = visvalingam_whyatt(coord_list, n_nodes)

def visvalingam_whyatt(node_list, n_nodes):
    """
    Simplify a line using the Visvalingam-Whyatt algorithm.
    node_list : list of coordinate pairs [(x, y), (x, y), ...]
    n_nodes   : desired number of nodes to keep
    """

    # Calculate initial effective areas for each node
    areas = []
    for i in range(1, len(node_list) - 1):
        area = get_effective_area(node_list[i - 1], node_list[i], node_list[i + 1])
        areas.append({"point": node_list[i], "area": area})

    # Add endpoints (with fake area = 0)
    areas.insert(0, {"point": node_list[0], "area": 0})
    areas.insert(len(areas), {"point": node_list[len(node_list) - 1], "area": 0})

    # Sanity check
    print(f"Initial node count: {len(node_list)} | Initial areas count: {len(areas)}")

    # Make a shallow copy so we don’t modify the original
    nodes = areas.copy()

    # Keep going as long as we have more nodes than desired
    while len(nodes) > n_nodes:

        # --- Find the node with the smallest effective area ---
        min_area = float("inf")
        node_to_delete = None

        for i in range(1, len(nodes) - 1):  # ignore endpoints
            if nodes[i]['area'] < min_area:
                min_area = nodes[i]['area']
                node_to_delete = i

        # --- Remove that node from the list ---
        nodes.pop(node_to_delete)

        # --- Recalculate effective areas for its neighbours ---
        # Left neighbour
        nodes[node_to_delete - 1]['area'] = get_effective_area(
            nodes[node_to_delete - 2]['point'],   # point to the left of left neighbour
            nodes[node_to_delete - 1]['point'],   # left neighbour
            nodes[node_to_delete]['point']        # right neighbour (current)
        )

        # Right neighbour (only if we didn’t delete the last node)
        if node_to_delete < len(nodes) - 1:
            nodes[node_to_delete]['area'] = get_effective_area(
                nodes[node_to_delete - 1]['point'],  # left
                nodes[node_to_delete]['point'],      # middle (right neighbour)
                nodes[node_to_delete + 1]['point']   # right of right neighbour
            )

        # Optional: progress check
        print(f"Nodes remaining: {len(nodes)}")

    # Extract only the coordinates and return them
    return [node['point'] for node in nodes]

from shapely.geometry import LineString 

# run your simplification
simplified_nodes = visvalingam_whyatt(coord_list, n_nodes)

# check that the number of points matches what we asked for
print(f" Simplified node count check: {len(simplified_nodes)} (target was {n_nodes})\n")

# make LineStrings before and after simplification
before_line = LineString(coord_list)
after_line = LineString(simplified_nodes)

# print out node counts and lengths
print(f"original node count: {len(coord_list)}")
print(f"original length: {before_line.length / 1000:.2f} km\n")

print(f"simplified node count: {len(simplified_nodes)}")
print(f"simplified length: {after_line.length / 1000:.2f} km\n")

from geopandas import GeoSeries  # can be combined with other imports
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.pyplot import subplots, savefig, subplots_adjust
import os

# if not already defined
SIMPLIFICATION_PERC = round(100 * len(simplified_nodes) / len(coord_list), 1)
osgb = "EPSG:27700"  # example CRS (adjust if your data uses a different one)

# create map figure with two side-by-side axes
fig, my_axs = subplots(1, 2, figsize=(16, 10))

# set overall title and individual subplot titles
fig.suptitle("The Length of the Coastline of Mainland Great Britain\n", fontsize=16)
my_axs[0].set_title(f"Original: {before_line.length / 1000:.0f} km, {len(coord_list)} nodes.")
my_axs[1].set_title(f"{SIMPLIFICATION_PERC}% Simplified: {after_line.length / 1000:.0f} km, {len(simplified_nodes)} nodes.")

# reduce gap between maps
subplots_adjust(wspace=0)

# plot the original coastline in blue
GeoSeries(before_line, crs=osgb).plot(
    ax=my_axs[0],
    color='blue',
    linewidth=0.6,
)

# plot the simplified coastline in red
GeoSeries(after_line, crs=osgb).plot(
    ax=my_axs[1],
    color='red',
    linewidth=0.6,
)

# edit each axis
for my_ax in my_axs:
    # remove default axes
    my_ax.axis('off')

    # add north arrow
    x, y, arrow_length = 0.95, 0.99, 0.1
    my_ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
                   arrowprops=dict(facecolor='black', width=5, headwidth=15),
                   ha='center', va='center', fontsize=20, xycoords=my_ax.transAxes)

    # add scalebar (in metres)
    my_ax.add_artist(ScaleBar(dx=1, units="m", location="lower right"))

# make sure the 'out' folder exists
os.makedirs("out", exist_ok=True)

SIMPLIFICATION_PERC = 20

# save the result as a PNG
savefig('out/4.png', bbox_inches='tight')
print(" done! Saved map as out/4.png")
