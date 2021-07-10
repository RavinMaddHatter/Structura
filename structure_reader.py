import nbtlib
import numpy as np


class process_structure:
    def __init__(self, file):
        if type(file) is dict:
            self.NBTfile = file
        else:
            self.NBTfile = nbtlib.load(file, byteorder='little')
        self.blocks = list(
            map(int, self.NBTfile[""]["structure"]["block_indices"][0]))
        self.size = list(map(int, self.NBTfile[""]["size"]))
        self.palette = self.NBTfile[""]["structure"]["palette"]["default"]["block_palette"]
        self.get_blockmap()

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

    def get_block_list(self, ignored_blocks=[]):
        block_counter = {}
        for block_id in self.blocks:
            if self.palette[block_id]["name"] not in ignored_blocks:
                block_name = self.palette[block_id]["name"]

                # We will ignore these states when checking for additional data
                ignored_state_types = ["upside_down_bit", "top_slot_bit", "direction", "facing_direction", "deprecated",
                                       "wall_connection_type_east", "rail_data_bit", "age", "rail_direction",
                                       "redstone_signal",
                                       "torch_facing_direction", "lever_direction", "covered_bit", "growing_plant_age",
                                       "dripstone_thickness", "moisturized_amount", "growth", "pillar_axis",
                                       "attached_bit", "composter_fill_level", "update_bit"]

                # We will check these states for additional data about the blocks
                state_types = ["color", "dirt_type", "stone_slab_type_4", "stone_slab_type", "wall_block_type",
                               "old_leaf_type", "chisel_type", "huge_mushroom_bits", "wood_type", "flower_type",
                               "double_plant_type", "coral_color", "tall_grass_type", "sapling_type", "cauldron_liquid",
                               "sand_type", "stone_brick_type", "stone_type"]

                # Parsing the respective states
                if ("dirt_type" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["dirt_type"]
                if ("color" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["color"]
                if ("stone_slab_type_4" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["stone_slab_type_4"]
                if ("stone_slab_type" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["stone_slab_type"]
                if ("wall_block_type" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["wall_block_type"]
                if ("old_leaf_type" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["old_leaf_type"]
                if ("chisel_type" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["chisel_type"]
                if ("wood_type" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["wood_type"]
                if ("flower_type" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["flower_type"]
                if ("double_plant_type" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["double_plant_type"]
                if ("coral_color" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["coral_color"]
                if ("tall_grass_type" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["tall_grass_type"]
                if ("sapling_type" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["sapling_type"]
                if ("cauldron_liquid" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["cauldron_liquid"]
                if ("sand_type" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["sand_type"]
                if ("stone_brick_type" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["stone_brick_type"]
                if ("stone_type" in self.palette[block_id]["states"]):
                    block_name += ':' + self.palette[block_id]["states"]["stone_type"]
                # Mushroom stems have an integer value of 15
                if ("huge_mushroom_bits" in self.palette[block_id]["states"]):
                    if (self.palette[block_id]["states"]["huge_mushroom_bits"] == 15):
                        block_name += ':stem'
                    else:
                        block_name += ':' + self.palette[block_id]["states"]["huge_mushroom_bits"]

                # print states that we haven't parsed yet (DEBUG)
                #found = False
                #total_state_types = ignored_state_types + state_types

                #for state_type in total_state_types:
                #    if (state_type in self.palette[block_id]["states"]):
                #        found = True

                #if not found and len(self.palette[block_id]["states"]) > 0:
                #    print(self.palette[block_id]["states"])

                if block_name in block_counter.keys():
                    block_counter[block_name] += 1
                else:
                    block_counter[block_name] = 1
        return block_counter

#testFileName="test_structures/minecart multi item sorter.mcstructure"
#excludedBlocks=["minecraft:structure_block","minecraft:air"]
#test=process_structure(testFileName)
#block_count=test.get_block_list(excludedBlocks)
#print("BLOCK LIST")
#total_blocks = 0
#for i in block_count.keys():
#   total_blocks += block_count[i]
#   print("{}: {}".format(i,block_count[i]))
#print("TOTAL NUMBER OF BLOCKS ", total_blocks)
