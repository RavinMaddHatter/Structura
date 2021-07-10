import nbtlib
import numpy as np
import stringcase

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
        # load translations from vanilla minecraft resource pack
        translations = {}
        with open('Vanilla_Resource_Pack/en_US.lang') as translation_file:
            for line in translation_file:
                name, var = line.partition("=")[::2]
                translations[name.strip()] = var.strip()

        block_counter = {}
        translated_block_counter = {}

        for block_id in self.blocks:
            if self.palette[block_id]["name"] not in ignored_blocks:
                block_name = self.palette[block_id]["name"]
                block_name = block_name.replace('minecraft:', '')

                # We will ignore these states when checking for additional data
                ignored_state_types = ["upside_down_bit", "top_slot_bit", "direction", "facing_direction", "deprecated",
                                       "wall_connection_type_east", "rail_data_bit", "age", "rail_direction",
                                       "redstone_signal",
                                       "torch_facing_direction", "lever_direction", "covered_bit", "growing_plant_age",
                                       "dripstone_thickness", "moisturized_amount", "growth", "pillar_axis",
                                       "attached_bit", "composter_fill_level", "update_bit", "infiniburn_bit",
                                       "allow_underwater_bit", "explode_bit", "brewing_stand_slot_a_bit",
                                       "brewing_stand_slot_b_bit",
                                       "brewing_stand_slot_c_bit", "ground_sign_direction", "stability",
                                       "stability_check",
                                       "hanging", "multi_face_direction_bits", "cluster_count", "dead_bit",
                                       "bamboo_leaf_size",
                                       "bamboo_stalk_thickness", "twisting_vines_age", "vine_direction_bits",
                                       "bite_counter"]

                ignored_state_types = []

                # We will check these states for additional data about the blocks
                state_types = ["color", "dirt_type", "stone_slab_type_4", "stone_slab_type", "wall_block_type",
                               "old_leaf_type", "chisel_type", "huge_mushroom_bits", "wood_type", "flower_type",
                               "double_plant_type", "coral_color", "tall_grass_type", "sapling_type", "cauldron_liquid",
                               "sand_type", "stone_brick_type", "stone_type", "sponge_type", "cracked_state",
                               "sand_stone_type", "respawn_anchor_charge",
                               "monster_egg_stone_type", "prismarine_block_type", "new_log_type", "stone_slab_type_2",
                               "old_log_type", "stone_slab_type_3", "new_leaf_type"]

                # Parsing the respective states

                #if block_name == 'skull':
                #    print(self.palette[block_id]["states"])

                # Fix log type
                if (block_name == 'log2'):
                    block_name = 'log'

                # Handle glazed terracotta types
                if (block_name == 'magenta_glazed_terracotta'):
                    block_name = 'glazedTerracotta.magenta'

                if (block_name == 'purple_glazed_terracotta'):
                    block_name = 'glazedTerracotta.purple'

                if (block_name == 'blue_glazed_terracotta'):
                    block_name = 'glazedTerracotta.blue'

                if (block_name == 'light_blue_glazed_terracotta'):
                    block_name = 'glazedTerracotta.light_blue'

                if (block_name == 'cyan_glazed_terracotta'):
                    block_name = 'glazedTerracotta.cyan'

                if (block_name == 'green_glazed_terracotta'):
                    block_name = 'glazedTerracotta.green'

                if (block_name == 'lime_glazed_terracotta'):
                    block_name = 'glazedTerracotta.lime'

                if (block_name == 'yellow_glazed_terracotta'):
                    block_name = 'glazedTerracotta.yellow'

                if (block_name == 'orange_glazed_terracotta'):
                    block_name = 'glazedTerracotta.orange'

                if (block_name == 'red_glazed_terracotta'):
                    block_name = 'glazedTerracotta.red'

                if (block_name == 'brown_glazed_terracotta'):
                    block_name = 'glazedTerracotta.brown'

                if (block_name == 'black_glazed_terracotta'):
                    block_name = 'glazedTerracotta.black'

                if (block_name == 'gray_glazed_terracotta'):
                    block_name = 'glazedTerracotta.gray'

                if (block_name == 'silver_glazed_terracotta'):
                    block_name = 'glazedTerracotta.silver'

                if (block_name == 'white_glazed_terracotta'):
                    block_name = 'glazedTerracotta.white'

                if (block_name == 'pink_glazed_terracotta'):
                    block_name = 'glazedTerracotta.pink'

                # Handle warped and crimson roots
                if (block_name == 'warped_roots'):
                    block_name += '.warpedRoots'

                if (block_name == 'crimson_roots'):
                    block_name += '.crimsonRoots'

                # Handle repeaters, comparators and daylight detectors
                if (block_name == 'unpowered_repeater'):
                    block_name = 'repeater'

                if (block_name == 'unpowered_comparator'):
                    block_name = 'comparator'

                if (block_name == 'daylight_detector_inverted'):
                    block_name = 'daylight_detector'

                # Handle undyed shulker boxes
                if (block_name == 'undyed_shulker_box'):
                    block_name = 'shulkerBox'

                # Handle dirt types
                if ("dirt_type" in self.palette[block_id]["states"]):
                    if (self.palette[block_id]["states"]["dirt_type"] == 'normal'):
                        block_name += '.default'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["dirt_type"]


                # Handle colors
                if ("color" in self.palette[block_id]["states"]):
                    # Handle shulker boxes
                    if (block_name == 'shulker_box'):
                        block_name = stringcase.camelcase('shulker_box_' + self.palette[block_id]["states"]["color"])
                    elif (block_name == 'concrete' and self.palette[block_id]["states"]["color"] == 'light_blue'):
                        block_name += '.lightBlue'
                    elif (block_name == 'concretePowder' and self.palette[block_id]["states"]["color"] == 'light_blue'):
                        block_name += '.lightBlue'
                    elif (block_name == 'carpet' and self.palette[block_id]["states"]["color"] == 'light_blue'):
                        block_name += '.lightBlue'
                    elif (block_name == 'wool' and self.palette[block_id]["states"]["color"] == 'light_blue'):
                        block_name += '.lightBlue'
                    elif (block_name == 'stained_hardened_clay' and self.palette[block_id]["states"]["color"] == 'light_blue'):
                        block_name += '.lightBlue'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["color"]
                if ("stone_slab_type_4" in self.palette[block_id]["states"]):
                    block_name += '.' + self.palette[block_id]["states"]["stone_slab_type_4"]
                if ("stone_slab_type" in self.palette[block_id]["states"]):
                    type = self.palette[block_id]["states"]["stone_slab_type"]
                    if (type == 'sandstone'):
                        block_name += '.sand'
                    elif (type == 'stone_brick'):
                        block_name += '.brick'
                    elif (type == 'cobblestone'):
                        block_name += '.cobble'
                    elif (type == 'smooth_stone'):
                        block_name += '.stone'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["stone_slab_type"]
                if ("wall_block_type" in self.palette[block_id]["states"]):
                    type = self.palette[block_id]["states"]["wall_block_type"]
                    if (type == 'cobblestone'):
                        block_name += '.normal'
                    elif (type == 'mossy_cobblestone'):
                        block_name += '.mossy'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["wall_block_type"]
                if ("new_log_type" in self.palette[block_id]["states"]):
                    # Handle dark oak planks
                    if (block_name == 'log' and self.palette[block_id]["states"]["new_log_type"] == 'dark_oak'):
                        block_name += '.big_oak'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["new_log_type"]
                if ("old_log_type" in self.palette[block_id]["states"]):
                    block_name += '.' + self.palette[block_id]["states"]["old_log_type"]
                if ("old_leaf_type" in self.palette[block_id]["states"]):
                    block_name += '.' + self.palette[block_id]["states"]["old_leaf_type"]
                if ("chisel_type" in self.palette[block_id]["states"]):
                    block_name += '.' + self.palette[block_id]["states"]["chisel_type"]
                if ("wood_type" in self.palette[block_id]["states"]):
                    # Handle dark oak planks
                    if (block_name == 'planks' and self.palette[block_id]["states"]["wood_type"] == 'dark_oak'):
                        block_name += '.big_oak'
                    elif (block_name == 'fence'):
                        type = self.palette[block_id]["states"]["wood_type"]
                        if (type == 'oak'):
                            # do nothing
                            block_name = block_name
                        else:
                            block_name = stringcase.camelcase(type + '_fence')
                    elif (block_name == 'wooden_slab'):
                        block_name += '.big_oak'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["wood_type"]
                if ("flower_type" in self.palette[block_id]["states"]):
                    # Handle blue orchid
                    if (self.palette[block_id]["states"]["flower_type"] == 'orchid'):
                        block_name += '.blueOrchid'
                    elif (self.palette[block_id]["states"]["flower_type"] == 'oxeye'):
                        block_name += '.oxeyeDaisy'
                    else:
                        block_name += '.' + stringcase.camelcase(self.palette[block_id]["states"]["flower_type"])
                if ("double_plant_type" in self.palette[block_id]["states"]):
                    block_name += '.' + self.palette[block_id]["states"]["double_plant_type"]
                if ("coral_color" in self.palette[block_id]["states"]):
                    if (block_name == 'coral_fan_dead'):
                        block_name += '.'+self.palette[block_id]["states"]["coral_color"]+'_fan'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["coral_color"]
                if ("tall_grass_type" in self.palette[block_id]["states"]):
                    if (block_name == 'tallgrass'):
                        block_name = 'double_plant.grass'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["tall_grass_type"]

                if ("sapling_type" in self.palette[block_id]["states"]):
                    if (self.palette[block_id]["states"]["sapling_type"] == 'dark_oak'):
                        block_name += '.big_oak'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["sapling_type"]
                if ("sand_type" in self.palette[block_id]["states"]):
                    if (self.palette[block_id]["states"]["sand_type"] == 'normal'):
                        # do nothing
                        block_name = block_name
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["sand_type"]
                if ("stone_brick_type" in self.palette[block_id]["states"]):
                    block_name += '.' + self.palette[block_id]["states"]["stone_brick_type"]
                if ("stone_type" in self.palette[block_id]["states"]):
                    type = self.palette[block_id]["states"]["stone_type"]
                    if (type == 'andesite_smooth'):
                        block_name += '.andesiteSmooth'
                    elif (type == 'granite_smooth'):
                        block_name += '.graniteSmooth'
                    elif (type == 'diorite_smooth'):
                        block_name += '.dioriteSmooth'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["stone_type"]
                if ("sponge_type" in self.palette[block_id]["states"]):
                    block_name += '.' + self.palette[block_id]["states"]["sponge_type"]
                if ("sand_stone_type" in self.palette[block_id]["states"]):
                    if (self.palette[block_id]["states"]["sand_stone_type"] == 'heiroglyphs'):
                        block_name += '.chiseled'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["sand_stone_type"]
                if ("moster_egg_stone_type" in self.palette[block_id]["states"]):
                    block_name += '.' + self.palette[block_id]["states"]["moster_egg_stone_type"]
                if ("prismarine_block_type" in self.palette[block_id]["states"]):
                    if (self.palette[block_id]["states"]["prismarine_block_type"] == 'default'):
                        block_name += '.rough'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["prismarine_block_type"]
                if ("stone_slab_type_2" in self.palette[block_id]["states"]):
                    # Handle prismarine types
                    type = self.palette[block_id]["states"]["stone_slab_type_2"]
                    if (type == 'prismarine_rough'):
                        block_name += '.prismarine.rough'
                    elif (type == 'prismarine_dark'):
                        block_name += '.prismarine.dark'
                    elif (type == 'prismarine_brick'):
                        block_name += '.prismarine.bricks'
                    elif (type == 'smooth_sandstone'):
                        block_name += '.sandstone.smooth'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["stone_slab_type_2"]

                if ("stone_slab_type_3" in self.palette[block_id]["states"]):
                    type = self.palette[block_id]["states"]["stone_slab_type_3"]
                    if (type == 'end_stone_brick'):
                        block_name += '.end_brick'
                    elif (type == 'polished_andesite'):
                        block_name += '.andesite.smooth'
                    elif (type == 'polished_diorite'):
                        block_name += '.diorite.smooth'
                    elif (type == 'polished_granite'):
                        block_name += '.granite.smooth'
                    elif (type == 'smooth_red_sandstone'):
                        block_name += '.red_sandstone.smooth'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["stone_slab_type_3"]
                if ("new_leaf_type" in self.palette[block_id]["states"]):
                    if (self.palette[block_id]["states"]["new_leaf_type"] == 'dark_oak'):
                        block_name += '.big_oak'
                    else:
                        block_name += '.' + self.palette[block_id]["states"]["new_leaf_type"]
                # Mushroom stems have an integer value of 15
                if ("huge_mushroom_bits" in self.palette[block_id]["states"]):
                    if (self.palette[block_id]["states"]["huge_mushroom_bits"] == 15):
                        block_name += '.stem'
                    elif (block_name == 'brown_mushroom_block'):
                        block_name += '.cap'

                # print states that we haven't parsed yet (DEBUG)
                # found = False
                # total_state_types = ignored_state_types + state_types

                # for state_type in total_state_types:
                #    if (state_type in self.palette[block_id]["states"]):
                #        found = True

                # if not found and len(self.palette[block_id]["states"]) > 0:
                #    print(self.palette[block_id]["states"])

                if block_name in block_counter.keys():
                    block_counter[block_name] += 1
                else:
                    block_counter[block_name] = 1

                if ('tile.' + block_name + '.name' in translations):
                    translated_block_name = translations['tile.' + block_name + '.name']
                elif ('item.' + block_name + '.name' in translations):
                    translated_block_name = translations['item.' + block_name + '.name']
                else:
                    translated_block_name = "TRANSLATION_MISSING " + block_name

                if translated_block_name in translated_block_counter.keys():
                    translated_block_counter[translated_block_name] += 1
                else:
                    translated_block_counter[translated_block_name] = 1

        return translated_block_counter


testFileName = "allblocks.mcstructure"
excludedBlocks = ["minecraft:structure_block", "minecraft:air"]
test = process_structure(testFileName)
block_count = test.get_block_list(excludedBlocks)
print("BLOCK LIST")
total_blocks = 0
for i in block_count.keys():
    print("{}: {}".format(i, block_count[i]))
    total_blocks += block_count[i]
print("TOTAL NUMBER OF BLOCKS ", total_blocks)
