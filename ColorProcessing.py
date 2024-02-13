from PIL import Image
from math import sqrt

def convertImageToLegoColorsTest():
    '''
    Use sample image and very basic color list as PoC.
    '''
    image = "./eevees.png"
    color_dict = {
            "black" : (0,  0, 0),
            "white" : (255, 255, 255),
            "red" : (255, 0, 0),
            "green" : (0, 255, 0),
            "blue" : (0, 0, 255),
            "cyan" : (0, 255, 255),
            "yellow" : (255, 255, 0),
            "magenta" : (255, 0, 255)
            }

    with Image.open(image) as im:
        img = im.load()
    
    result_im = im.copy()
    print(img[im.width // 2, im.height // 2])
    #img.show()
    for x in range(im.width):
        for y in range(im.height):
            result_im.putpixel((x, y), identifyNewPixelColor(img[x, y], color_dict))

    result_im.show()

    return result_im


def convertImageToLegoColors(image, colors):
    with Image.open(image) as im:
        px = im.load()
    result = im.copy()

    for x in range(im.width):
        for y in range(im.height):
            result.putpixel((x, y), identifyNewPixelColor(im.getpixel((x, y)), colors))

    result.show()
    return result

def identifyNewPixelColor(old_color, color_dict):
    '''
    Takes the original pixel color and chooses the closest from the provided list of options.
    Returns a 3-tuple containing the rgb of the selected color.
    '''
    (r1, g1, b1) = old_color
    minimum_distance = float("inf")
    closest_match = (0, 0, 0)

    for key, value in color_dict.items():
        (r2, g2, b2) = value
        distance = sqrt((r2-r1)**2 + (g2-g1)**2 + (b2-b1)**2)
        if distance < minimum_distance:
            minimum_distance = distance
            closest_match = (r2, g2, b2)

    return closest_match

if __name__ == "__main__":
    convertImageToLegoColorsTest()
