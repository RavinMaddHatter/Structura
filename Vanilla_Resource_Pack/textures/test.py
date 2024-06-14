import json
with open("item_texture.json") as file:
    oldData=json.load(file)
with open("easyItems.txt","w+") as file:
    for key in oldData["texture_data"].keys():
        file.write(key)
        file.write("\n")
