import json


with open("terrain_texture_old.json") as file:
    oldData=json.load(file)
with open("terrain_texture_new.json") as file:
    newData=json.load(file)

oldKeys=list(oldData["texture_data"].keys())
newKeys=list(newData["texture_data"].keys())

newBlocks = list(filter(lambda i: i not in oldKeys, newKeys))
for key in newBlocks:
    oldData["texture_data"][key]=newData["texture_data"][key]

with open("terrain_texture.json","w+") as file:
    oldData=json.dump(oldData,file, indent=2)
