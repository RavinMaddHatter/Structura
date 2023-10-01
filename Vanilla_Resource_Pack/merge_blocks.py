import json


with open("blocks.json") as file:
    oldData=json.load(file)
with open("blocks20-20.json") as file:
    newData=json.load(file)

oldKeys=list(oldData.keys())
newKeys=list(newData.keys())

newBlocks = list(filter(lambda i: i not in oldKeys, newKeys))
for key in newBlocks:
    oldData[key]=newData[key]

with open("blocks.json","w+") as file:
    oldData=json.dump(oldData,file, indent=2)
