import rebrick
import json
from ImageSelector import acquireImage
import ColorProcessing
from key import API_KEY
import options

def hex_to_rgb(value):
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv // 3))

if __name__ == "__main__":

    OK_TO_CONNECT = True

    # Select an image file
    file_path = acquireImage()

    print(file_path)
    print()


    if(OK_TO_CONNECT):
        # init Rebrick tool
        rb = rebrick.Rebrick(api_key=API_KEY)
        

        response = None
        color_dict = None
        if (options.UPDATE_COLOR_LIST):
            data = rb.get_part(options.PART_ID)
            print(data)

            response = rb.get_part_colors(options.PART_ID)

            color_dict = {}
            for i, color in enumerate(response):
                color_dict[color.name] = hex_to_rgb(color.rgb)
        
            with open("color_cache.json", 'w', encoding='utf-8') as f:
                json.dump(color_dict, f, ensure_ascii=False, indent=4)
        
        else:
            with open("color_cache.json", 'r') as f:
                color_dict = json.load(f)

        print("Total colors:", len(color_dict))

        result = ColorProcessing.convertImageToLegoColors(file_path, color_dict)        
        
        save = input("Would you like to save this image? Y/N: ")
        if save == "Y":
            #save file
            sindex = file_path.rfind("/")
            dindex = file_path.find(".")
            
            result.save("output/" + file_path[sindex+1:dindex] + "_conv" + file_path[dindex:])
            print("File saved in 'output'.")
        else:
            #don't save
            print("File not saved")
            
    else:
        print("Not currently using Rebrick tool.")

