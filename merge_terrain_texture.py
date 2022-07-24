import json
oldblocksFile = "Vanilla_Resource_Pack\\blocks.json"
newblocksFile = "Vanilla_Resource_Pack\\blocks17.json"
oldTerrainTexture="Vanilla_Resource_Pack\\textures\\terrain_texture.json"
newTerrainTexture="Vanilla_Resource_Pack\\textures\\terrain_texture17.json"
oldDefsFile="lookups\\block_definition.json"
with open(oldTerrainTexture) as file:
    oldData=json.load(file)
with open(newTerrainTexture) as file:
    newData=json.load(file)
with open(oldDefsFile) as file:
    blockDef=json.load(file)

with open(oldblocksFile) as file:
    oldBlocks=json.load(file)
with open(newblocksFile) as file:
    newBlocks=json.load(file)

oldKeys=list(oldData["texture_data"].keys())
newKeys=list(newData["texture_data"].keys())
oldDefs=list(blockDef.keys())

newBlockskeys = list(filter(lambda i: i not in oldBlocks, newBlocks))
newTextures = list(filter(lambda i: i not in oldKeys, newKeys))
newDefinitions = list(filter(lambda i: i not in oldDefs, newKeys))
for key in newTextures:
    oldData["texture_data"][key]=newData["texture_data"][key]
for key in newBlockskeys:
    blockDef[key]="cube"
    oldBlocks[key]=newBlocks[key]
    print(key)


with open(oldTerrainTexture,"w+") as file:
    json.dump(oldData,file, indent=4)
with open(oldDefsFile, "w+") as file:
    json.dump(blockDef,file, indent=4)
with open(oldblocksFile, "w+") as file:
    json.dump(oldBlocks,file, indent=4)
