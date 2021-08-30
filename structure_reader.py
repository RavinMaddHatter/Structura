import nbtlib
import block as block_class
import numpy as np


class StructureReader:
    def __init__(self, file, excluded_blocks):
        if type(file) is dict:
            self.NBTfile = file
        else:
            self.NBTfile = nbtlib.load(file, byteorder='little')
        self.blocks = list(
            map(int, self.NBTfile[""]["structure"]["block_indices"][0]))
        self.size = list(map(int, self.NBTfile[""]["size"]))
        self.palette = self.NBTfile[""]["structure"]["palette"]["default"]["block_palette"]
        self.get_blockmap()
        self.matrix = self.process_blocks(excluded_blocks)

    def get_blockmap(self):
        self.cube = np.zeros(self.size, np.int)
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

    def get_block_list(self, excluded_blocks):
        block_counter = {}
        for block_id in self.blocks:
            if self.palette[block_id]["name"] not in excluded_blocks:
                block_name = self.palette[block_id]["name"]
                if block_name in block_counter.keys():
                    block_counter[block_name] += 1
                else:
                    block_counter[block_name] = 1

        return block_counter

    # Creates a matrix equivalent to the structure containing the block info
    def process_blocks(self, excluded_blocks):
        structure_matrix = []
        # Create the matrix for the blocks
        for x in range(self.size[0]):
            structure_matrix.append([])
            for y in range(self.size[1]):
                structure_matrix[x].append([])
                for z in range(self.size[2]):
                    structure_matrix[x][y].append(None)

        # Fill the matrix with the structure blocks
        # We create first the matrix and then fill it by y layers to fix the top door direction_bit issue (in block.py)
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                for z in range(self.size[2]):
                    if self.get_block(x, y, z)["name"] in excluded_blocks:
                        structure_matrix[x][y][z] = None
                    else:
                        try:
                            # We also send the block_nbt from underneath to fix top door issue
                            if y != 0:
                                block = block_class.Block(self.get_block(
                                    x, y, z), self.get_block(x, y-1, z))
                            else:
                                block = block_class.Block(self.get_block(
                                    x, y, z), None)
                            structure_matrix[x][y][z] = block
                        except block_class.NotJavaBlockException:
                            pass
        return structure_matrix


# testFileName="test_structures/partial_blocks.mcstructure"
# excludedBlocks=["minecraft:structure_block","minecraft:air"]
# test=StructureReader(testFileName)
