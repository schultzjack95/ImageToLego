import argparse
import json
import os.path
import sys

import rebrick

import ColorProcessing
import data.key
import data.options
from ImageSelector import acquireImage


def hex_to_rgb(value):
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv // 3))


def save_image(result, file_path):
    sindex = file_path.rfind("/")
    dindex = file_path.find(".")
            
    result.save("output/" + file_path[sindex+1:dindex] + "_conv" + file_path[dindex:])
    print("Image file saved in 'output/'.")

def save_parts_list(parts, file_path):
    sindex = file_path.rfind('/')
    dindex = file_path.find('.')

    with open("output/parts_list_for_" + file_path[sindex+1:dindex] + ".txt", 'w', encoding='utf-8') as f:
        total = sum(a[1] for a in parts.values())
        print("A total of", total, "pieces of part id", data.options.PART_ID, ".", file=f)
        print(file=f)
        for color, (name, count) in sorted(parts.items(), key=lambda x:x[1][1], reverse=True):
            print(f'{count} pieces of {name}.', file=f)
    print("Parts list saved in 'output/'.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog="ImageToLego",
            description="Recreates the given image in a limited palette of LEGO Brick colors.")
    #file -s SAVE -v VIEW -p
    parser.add_argument("file", help="File to be converted")
    parser.add_argument("-s", "--save", help="Y/y to save result, N/n to discard after viewing", choices=['Y', 'y', 'N', 'n'])
    parser.add_argument("-v", "--view", help="Displays the result on-screen when enabled", action="store_true")
    parser.add_argument("-p", "--parts", help="-[p|pp|ppp]. Computes the necessary pieces of each color needed to physically craft the result. If excluded, do not compute total. -p: print total on screen. -pp: save the results to a file. -ppp: both display and save the total", action="count", default=0)
    args = parser.parse_args()
    
    # If command line file path was provided
    if os.path.isfile(args.file):
        file_path = args.file
    else:
        # Select an image file from file system window
        file_path = acquireImage()

    print(file_path)
    print()

    response = None
    color_dict = None
    
    if (data.options.UPDATE_COLOR_LIST):
        # init Rebrick tool
        rb = rebrick.Rebrick(api_key=data.key.API_KEY)
        
        # Display part information from Rebrickable
        data = rb.get_part(data.options.PART_ID)
        print(data)
        
        # Retrieve part colors from Rebrickable
        response = rb.get_part_colors(data.options.PART_ID)

        color_dict = {}
        for color in response:
            color_dict[color.name] = hex_to_rgb(color.rgb)
        
        # Store updated color list
        with open("data/color_cache.json", 'w', encoding='utf-8') as f:
            json.dump(color_dict, f, ensure_ascii=False, indent=4)
        
    else:
        # Use cached color list
        with open("data/color_cache.json", 'r') as f:
            color_dict = json.load(f)

    print("Total valid target colors:", len(color_dict))

    result, best_matches = ColorProcessing.convertImageToLegoColors(file_path, color_dict)        
    
    # If --view flag enabled, display resultant image
    if args.view:
        result.show()
    

    # If --parts is enabled, calculate the parts needed of each color and link the official color names
    if args.parts > 0:
        # parts_list = [ [color, name, count]
        parts_list = {}
        for color, count in best_matches.values():
            if color in parts_list:
                parts_list[color][1] += count
            else:
                parts_list[color] = ["unnamed", count]

        # parts_list now has the color values and the number of parts. Now find the right names.
        for color, value in parts_list.items():
            for name, rgb in color_dict.items():
                if tuple(rgb) == color:
                    value[0] = name
                    break
        
        if args.parts == 1 or args.parts >= 3:
            print("Total pieces needed:", sum(a[1] for a in parts_list.values()))
            print("Different colors used:", len(parts_list))
            for color, (name, count) in sorted(parts_list.items(), key=lambda x:x[1][1], reverse=True):
                print(f'{count} pieces of {name}.')

        if args.parts >= 2:
            save_parts_list(parts_list, file_path)

    # If -s Y, save automatically, if -s n, discard automatically, else ask user
    if args.save:
        if args.save.upper() == "Y":
            save_image(result, file_path)
        elif args.save.upper() == "N":
            #discard
            print("Image file not saved.")
    else:
        #ask user
        save = input("Would you like to save this image? Y/N: ")
        if save.upper() == "Y":
            save_image(result, file_path)
        else:
            #don't save
            print("Image file not saved.")
