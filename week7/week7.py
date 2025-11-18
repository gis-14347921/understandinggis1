from rasterio import open as rio_open
from rasterio.transform import rowcol

def coord_2_img(transform, x, y):
    """ 
    Convert from coordinate space to image space using the 
    Affine transform object from a rasterio dataset
    
    Note that rowcol() returns floats so they need to be 
    converted to integers to be used as cell references
    """
    r, c = rowcol(transform, x, y)
    return (int(r), int(c))

def main():
    # Open the raster dataset using a with statement
    with rio_open('C:/Users/14256/Documents/GitHub/data/helvellyn/Helvellyn-50.tif') as dem:
        
        # Print dataset profile information
        print("Dataset Profile:")
        print(dem.profile)
        print("\n" + "="*50 + "\n")
        
        # Read the single band (elevation data)
        dem_data = dem.read(1)
        
        # Coordinates for the summit of Helvellyn
        summit_x = 334170
        summit_y = 515165
        
        # Convert coordinates to image space
        row, col = coord_2_img(dem.transform, summit_x, summit_y)
        
        # Get elevation value at summit coordinates
        elevation = dem_data[row][col]
        
        # Print the result
        print(f"Helvellyn Summit Information:")
        print(f"Coordinates: ({summit_x}, {summit_y})")
        print(f"Image space position: (row {row}, column {col})")
        print(f"Elevation: {elevation:.0f}m")
        
        # Alternative method using tuple indexing
        alt_elevation = dem_data[coord_2_img(dem.transform, summit_x, summit_y)]
        print(f"Alternative method result: {alt_elevation:.0f}m")

if __name__ == "__main__":
    main()