import nbtlib
import numpy as np

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
        self.mins = np.array(list(map(int,self.NBTfile["structure_world_origin"])))
        self.maxs = self.mins + np.array(self.size)-1
        self.get_blockmap()
    def get_blockmap(self):
        self.cube = np.zeros(self.size, int)
        i = 0
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    self.cube[x][y][z] = self.blocks[i]
                    i += 1

    def get_block(self, x, y, z):
        index = self.cube[x, y, z]
        return self.palette[int(index)]

    def get_size(self):
        return self.size

    def get_block_list(self, ignored_blocks=[]):
        block_counter = {}
        for block_id in self.blocks:
            if self.palette[block_id]["name"] not in ignored_blocks:
                block_name = self.palette[block_id]["name"]
                if block_name in block_counter.keys():
                    block_counter[block_name] += 1
                else:
                    block_counter[block_name] = 1
        return block_counter
class combined_structures:
    def __init__(self,file_list,exclude_list=[]):
        self.structs={}
        self.maxs = np.array([-2147483647,-2147483647,-2147483647],dtype=np.int32)
        self.mins = np.array([2147483647,2147483647,2147483647],dtype=np.int32)
        palette_size=0
        self.palette=[{"name":"minecraft:air","states":[],"version":"17959425"}]
        
        for file in file_list:
            self.structs[file] = {}
            self.structs[file]["nbt"] = nbtlib.load(file, byteorder='little')
            if "" in self.structs[file]["nbt"].keys():
                self.structs[file]["nbt"] = self.NBTfile[""]
            
            self.structs[file]["blocks"] = np.array(list(map(int, self.structs[file]["nbt"]["structure"]["block_indices"][0])))
            
            self.structs[file]["size"] = np.array(list(map(int, self.structs[file]["nbt"]["size"])))
            self.structs[file]["palette"] = self.structs[file]["nbt"]["structure"]["palette"]["default"]["block_palette"]
            self.structs[file]["mins"] = np.array(list(map(int,self.structs[file]["nbt"]["structure_world_origin"])))
            self.structs[file]["maxs"] = self.structs[file]["mins"] + self.structs[file]["size"]
            self.maxs=np.maximum(self.maxs, self.structs[file]["maxs"])
            self.mins=np.minimum(self.mins, self.structs[file]["mins"])
            self.structs[file]["blocks"] = self.structs[file]["blocks"].reshape(self.structs[file]["size"])
            self.structs[file]["blocks"] = self.structs[file]["blocks"]+len(self.palette)
            self.palette += self.structs[file]["palette"]
        self.size = self.maxs-self.mins
        self.blocks = np.zeros(self.size, int)
        for file in file_list:
            embed(self.structs[file]["blocks"],self.blocks,self.structs[file]["mins"]-self.mins)
    def get_block(self, x, y, z):
        index = self.cube[x, y, z]
        return self.palette[int(index)]
    def get_size(self):
        return self.size
    def get_block_list(self, ignored_blocks=[]):
        block_counter = {}
        for block_id in self.blocks.ravel():
            if self.palette[block_id]["name"] not in ignored_blocks:
                block_name = self.palette[block_id]["name"]
                if block_name in block_counter.keys():
                    block_counter[block_name] += 1
                else:
                    block_counter[block_name] = 1
        return block_counter
        
    
if __name__ == "__main__":
    testFileNameArray=[]
    testFileNameArray.append("test_structures\\BigHatter\\1.mcstructure")
    testFileNameArray.append("test_structures\\BigHatter\\2.mcstructure")
    testFileNameArray.append("test_structures\\BigHatter\\3.mcstructure")
    testFileNameArray.append("test_structures\\BigHatter\\4.mcstructure")
    testFileName="BigHatter\\1.mcstructure"
    excludedBlocks=["minecraft:structure_block","minecraft:air"]
    #test=process_structure(testFileName)
    #block_count=test.get_block_list(excludedBlocks)
    t=combined_structures(testFileNameArray)
    print(t.size)
    print(t.get_block_list(ignored_blocks=excludedBlocks))

