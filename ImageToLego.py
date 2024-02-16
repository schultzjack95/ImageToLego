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
    print("File saved in 'output'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog="ImageToLego",
            description="Recreates the given image in a limited palette of LEGO Brick colors.")
    #file -s SAVE -v VIEW
    parser.add_argument("file", help="File to be converted")
    parser.add_argument("-s", "--save", help="Y/y to save result, N/n to discard after viewing", choices=['Y', 'y', 'N', 'n'])
    parser.add_argument("-v", "--view", help="Displays the result on-screen when enabled", action="store_true")
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
        for i, color in enumerate(response):
            color_dict[color.name] = hex_to_rgb(color.rgb)
        
        # Store updated color list
        with open("data/color_cache.json", 'w', encoding='utf-8') as f:
            json.dump(color_dict, f, ensure_ascii=False, indent=4)
        
    else:
        # Use cached color list
        with open("data/color_cache.json", 'r') as f:
            color_dict = json.load(f)

    print("Total valid target colors:", len(color_dict))

    result = ColorProcessing.convertImageToLegoColors(file_path, color_dict)        
    
    # If --view flag enabled, display resultant image
    if args.view:
        result.show()
    
    # If -s Y, save automatically, if -s n, discard automatically, else ask user
    if args.save:
        if args.save.upper() == "Y":
            save_image(result, file_path)
        elif args.save.upper() == "N":
            #discard
            print("File not saved")
    else:
        #ask user
        save = input("Would you like to save this image? Y/N: ")
        if save.upper() == "Y":
            save_image(result, file_path)
        else:
            #don't save
            print("File not saved")
