import json


with open("Vanilla_Resource_Pack\textures\terrain_texture.json") as file:
    oldData=json.load(file)
with open("Vanilla_Resource_Pack\textures\terrain_texture17.json") as file:
    newData=json.load(file)
with open("lookups\block_definition.json") as file:
    blockDef=json.load(file)

oldKeys=list(oldData["texture_data"].keys())
newKeys=list(newData["texture_data"].keys())
oldDefs=list(blockDef.keys())

newTextures = list(filter(lambda i: i not in oldKeys, newKeys))
newDefinitions = list(filter(lambda i: i not in oldDefs, newKeys))
for key in newBlocks:
    oldData["texture_data"][key]=newData["texture_data"][key]
