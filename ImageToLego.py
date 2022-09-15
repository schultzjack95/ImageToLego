import rebrick
import json

# init Rebrick tool
rb = rebrick.Rebrick(api_key="15b882fd571ffae85bdd8cf05d7ab057")

# get set info
data = rb.get_set(6608)
print(data)

response = rb.get_colors()

print("Get colors:")
for i, color in enumerate(response):
    print(color, type(color))
