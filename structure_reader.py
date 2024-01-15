import nbtlib
from numpy import array, argwhere , int32, maximum, minimum, zeros, count_nonzero, flip
import json
loaded={}
def embed( small_array, big_array, loc):
    """Overwrites values in big_array starting at big_index with those in small_array"""
    xstart=loc[0]
    ystart=loc[1]
    zstart=loc[2]
    xstop=xstart+small_array.shape[0]
    ystop=ystart+small_array.shape[1]
    zstop=zstart+small_array.shape[2]
    big_array[xstart:xstop,ystart:ystop,zstart:zstop]=small_array
class process_structure:
    def __init__(self, file):
        global loaded
        with open("lookups/nbt_defs.json") as nbt_file:
            self.nbt_defs=json.load(nbt_file)
            
        with open("lookups/material_list_names.json") as nbt_file:
            self.block_names=json.load(nbt_file)
        if type(file) is dict:
            self.NBTfile = file
        else:
            self.NBTfile = nbtlib.load(file, byteorder='little')
        loaded=self.NBTfile
        
        if "" in self.NBTfile.keys():
            self.NBTfile=self.NBTfile[""]

        self.blocks = list(map(int, self.NBTfile["structure"]["block_indices"][0]))
        self.size = list(map(int, self.NBTfile["size"]))
        self.palette = self.NBTfile["structure"]["palette"]["default"]["block_palette"]
        self.mins = array(list(map(int,self.NBTfile["structure_world_origin"])))
        self.maxs = self.mins + array(self.size)-1
        self.origin = array(list(map(int,self.NBTfile["structure_world_origin"])))
        self.get_blockmap()
    def get_layer_blocks(self,y):
        lb=self.cube[:,y,:]
        return argwhere(lb > 0)
    def get_blockmap(self):
        index_of_air = 0
        for i in range(len(self.palette)):
            if self.palette[i]["name"] == "minecraft:air":
                index_of_air = i
                break
        self.cube = array(self.blocks)
        self.cube += 1
        self.palette = [{"name":"minecraft:air","states":[]}] + self.palette
        self.cube[self.cube==index_of_air+1]=0
        self.cube=self.cube.reshape(self.size)

    def get_block(self, x, y, z):
        index = self.cube[x, y, z]
        return self.palette[int(index)]

    def get_size(self):
        return self.size

    def get_block_list(self, ignored_blocks=["minecraft:air","minecraft:structure_block"]):
        block_counter = {}
        i=-2
        block_array=array(self.blocks)
        for block in self.palette:
            i+=1
            name=block["name"]
            if not(name in ignored_blocks):
                
                if name in self.block_names.keys():
                    variant="default"
                    for state in block["states"].keys():
                        if state in self.nbt_defs.keys():
                            if self.nbt_defs[state] == "variant":
                                if block["states"][state] in self.block_names[name].keys():
                                    variant=block["states"][state]
                    try:
                        name=self.block_names[name][variant]
                    except:
                        print(name,variant)
                if name not in block_counter.keys():
                    block_counter[name]=0
                
                block_counter[name]+=count_nonzero(block_array==i)
            
        return block_counter
class combined_structures:
    def __init__(self,file_list,exclude_list=[]):
        with open("lookups/nbt_defs.json") as nbt_file:
            self.nbt_defs=json.load(nbt_file)
        with open("lookups/material_list_names.json") as nbt_file:
            self.block_names=json.load(nbt_file)
        self.structs={}
        self.maxs = array([-2147483647,-2147483647,-2147483647],dtype=int32)
        self.mins = array([2147483647,2147483647,2147483647],dtype=int32)
        palette_size=0
        self.palette=[{"name":"minecraft:air","states":[],"version":"17959425"}]
        
        for file in file_list:
            self.structs[file] = {}
            self.structs[file]["nbt"] = nbtlib.load(file, byteorder='little')
            if "" in self.structs[file]["nbt"].keys():
                self.structs[file]["nbt"] = self.NBTfile[""]
            
            self.structs[file]["blocks"] = array(list(map(int, self.structs[file]["nbt"]["structure"]["block_indices"][0])))
            
            self.structs[file]["size"] = array(list(map(int, self.structs[file]["nbt"]["size"])))
            self.structs[file]["palette"] = self.structs[file]["nbt"]["structure"]["palette"]["default"]["block_palette"]
            index_of_air = 0
            for i in range(len(self.structs[file]["palette"])):
                if self.structs[file]["palette"][i]["name"] == "minecraft:air":
                    index_of_air = i
            self.structs[file]["mins"] = array(list(map(int,self.structs[file]["nbt"]["structure_world_origin"])))
            self.structs[file]["maxs"] = self.structs[file]["mins"] + self.structs[file]["size"]
            self.maxs=maximum(self.maxs, self.structs[file]["maxs"])
            self.mins=minimum(self.mins, self.structs[file]["mins"])
            self.structs[file]["blocks"] = self.structs[file]["blocks"].reshape(self.structs[file]["size"])
            self.structs[file]["blocks"] = self.structs[file]["blocks"]+len(self.palette)
            self.structs[file]["blocks"][self.structs[file]["blocks"]==index_of_air+len(self.palette)]=0
            
            self.palette += self.structs[file]["palette"]
        self.size = self.maxs-self.mins
        self.blocks = zeros(self.size, int)
        for file in file_list:
            embed(self.structs[file]["blocks"],self.blocks,self.structs[file]["mins"]-self.mins)
        self.blocks = flip(self.blocks,0)
        self.blocks = flip(self.blocks,2)
    def get_layer_blocks(self,y):
        lb=self.blocks[:,y,:]
        return argwhere(lb > 0)
    def get_block(self, x, y, z):
        index = self.blocks[x, y, z]
        return self.palette[int(index)]
    def get_size(self):
        return self.size
    def get_block_list(self, ignored_blocks=["minecraft:air"]):
        block_counter = {}
        i=-2
        block_array=array(self.blocks)
        for block in self.palette:
            i+=1
            name=block["name"]
            if not(name in ignored_blocks):
                
                if name in self.block_names.keys():
                    variant="default"
                    for state in block["states"].keys():
                        if state in self.nbt_defs.keys():
                            if self.nbt_defs[state] == "variant":
                                if block["states"][state] in self.block_names[name].keys():
                                    variant=block["states"][state]
                    try:
                        name=self.block_names[name][variant]
                    except:
                        print(name,variant)
                if name not in block_counter.keys():
                    block_counter[name]=0
                
                block_counter[name]+=count_nonzero(block_array==i)
        return block_counter
        
    
if __name__ == "__main__":
    testFileNameArray=[]
    excludedBlocks=["minecraft:structure_block","minecraft:air"]
    with open("lookups\\material_list_names.json") as name_lookup:
        blocks_def=json.load(name_lookup)
    batchtest=[]
    testFileName="test_structures\\All Blocks World\\gems and redstone.mcstructure"
    batchtest.append(testFileName)
    testFileName="test_structures\\All Blocks World\\decorative.mcstructure"
    batchtest.append(testFileName)
    testFileName="test_structures\\All Blocks World\\wood.mcstructure"
    batchtest.append(testFileName)
    testFileName="test_structures\\All Blocks World\\Stones.mcstructure"
    batchtest.append(testFileName)
##    test=combined_structures(batchtest,excludedBlocks)
    
    test=process_structure(testFileName)
    bllist=test.get_block_list(ignored_blocks=excludedBlocks)
##    for key,value in bllist.items():
##        print(f"{key}:{value}")
    for x in range(test.size[0]):
        for z in range(test.size[2]):
            block=test.get_block(x,0,z)
            if block["name"] not in excludedBlocks:
                variant="default"
                for state in block["states"].keys():
                    
                    if state in test.nbt_defs.keys():
                        if test.nbt_defs[state] == "variant":
                            variant=block["states"][state]
                if block["name"] not in blocks_def.keys():
                    blocks_def[block["name"]]={}
                if variant not in blocks_def[block["name"]].keys():
                    actual_name = input(f"loc: {x+test.origin[0]},{z+test.origin[2]} {block['name']} - {variant}:")
                    blocks_def[block["name"]][variant]=actual_name
    with open("lookups\\material_list_names.json","w+") as name_file:
        json.dump(blocks_def,name_file)
    #print(test.size)
        #input(f"")
    #print(test.size)
    #print(test.get_block_list(ignored_blocks=excludedBlocks))

