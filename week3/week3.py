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