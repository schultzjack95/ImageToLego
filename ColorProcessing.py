from math import sqrt

from PIL import Image
from tqdm.contrib import itertools

# COLORS[name] = (r,g,b)
COLORS = {}

# BEST_MATCHES[original_color] = [(r,g,b) of closest match, count]
BEST_MATCHES = {}


def convertImageToLegoColors(image, colors):
    with Image.open(image) as im:
        px = im.load()
    result = im.copy()
    
    global COLORS
    COLORS = colors

    for x, y in itertools.product(range(im.width), range(im.height), desc="Progress"):
        result.putpixel((x, y), identifyNewPixelColor(im.getpixel((x, y)), colors))
    #result = result.point(pickNearestColor)

    return result, BEST_MATCHES

def identifyNewPixelColor(old_color, color_dict):
    '''
    Takes the original pixel color and chooses the closest from the provided list of options.
    Returns a 3-tuple containing the rgb of the selected color.
    '''
    global BEST_MATCHES
    if old_color in BEST_MATCHES:
        BEST_MATCHES[old_color][1] += 1
        return BEST_MATCHES[old_color][0]
    
    # Not found in cache, do it the hard way
    (r1, g1, b1) = old_color
    minimum_distance = float("inf")
    closest_match = (0, 0, 0)

    for key, value in color_dict.items():
        (r2, g2, b2) = value
        distance = sqrt((r2-r1)**2 + (g2-g1)**2 + (b2-b1)**2)
        if distance < minimum_distance:
            minimum_distance = distance
            closest_match = (r2, g2, b2)

    # Update cache
    BEST_MATCHES[old_color] = [closest_match, 1]

    return closest_match

def pickNearestColor(rgb):
    r1, g1, b1 = rgb
    min_dist = float("inf")
    closest_match = (0, 0, 0)

    for key, value in COLORS.items():
        (r2, g2, b2) = value
        distance = sqrt((r2-r1)**2 + (g2-g1)**2 + (b2-b1)**2)
        if distance < minimum_distance:
            minimum_distance = distance
            closest_match = (r2, g2, b2)

    return closest_match

if __name__ == "__main__":
    convertImageToLegoColorsTest()
