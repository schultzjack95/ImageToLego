import rebrick
import json

# init Rebrick tool
rb = rebrick.Rebrick(api_key="15b882fd571ffae85bdd8cf05d7ab057")

# part id 3005 is the basic 1x1 brick
part_id = 3005

data = rb.get_part(part_id)
print(data)

response = rb.get_part_colors(part_id)

print("Total colors:", len(response))
for i, color in enumerate(response):
    print(i, color)
