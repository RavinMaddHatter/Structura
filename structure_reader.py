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

                # debug output for states
#                if block_name == 'smooth_stone':
#                    print(self.palette[block_id]["states"])

                # Parsing the respective states

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
                if (block_name == 'unpowered_repeater' or block_name == 'powered_repeater'):
                    block_name = 'repeater'

                if (block_name == 'unpowered_comparator' or block_name == 'powered_comparator'):
                    block_name = 'comparator'

                if (block_name == 'daylight_detector_inverted'):
                    block_name = 'daylight_detector'

                if (block_name == 'lit_redstone_lamp'):
                    block_name = 'redstone_lamp'

                if (block_name == 'wall_sign'):
                    block_name = 'sign'

                if (block_name == 'birch_wall_sign'):
                    block_name = 'birch_sign'

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
                    if (block_name == 'coral_fan_dead' or block_name == 'coral_fan'):
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

                # DEPRECATED this is no longer necessary and will be removed in the future
                if block_name in block_counter.keys():
                    # Fix double slabs
                    if ("double_" in block_name and "slab" in block_name):
                        block_counter[block_name] += 2
                    else:
                        block_counter[block_name] += 1
                else:
                    # Fix double slabs
                    if ("double_" in block_name and "slab" in block_name):
                        block_counter[block_name] = 2
                    else:
                        block_counter[block_name] = 1

                # Fix double slabs for translations
                fixed_block_name = block_name
                if ("double_" in block_name and "slab" in block_name):
                    fixed_block_name = block_name.replace('double_', '')

                if ('tile.' + fixed_block_name + '.name' in translations):
                    translated_block_name = translations['tile.' + fixed_block_name + '.name']
                elif ('item.' + fixed_block_name + '.name' in translations):
                    translated_block_name = translations['item.' + fixed_block_name + '.name']
                else:
                    translated_block_name = "TRANSLATION_MISSING " + fixed_block_name

                if translated_block_name in translated_block_counter.keys():
                    if ("double_" in block_name and "slab" in block_name):
                        translated_block_counter[translated_block_name] += 2
                    else:
                        translated_block_counter[translated_block_name] += 1
                else:
                    if ("double_" in block_name and "slab" in block_name):
                        translated_block_counter[translated_block_name] = 2
                    else:
                        translated_block_counter[translated_block_name] = 1

        # sort alphabetically
        sorted_items = dict(sorted(translated_block_counter.items()))

        return sorted_items

#testFileName = "Post_office.mcstructure"
#excludedBlocks = ["minecraft:structure_block", "minecraft:air"]
#test = process_structure(testFileName)
#block_count = test.get_block_list(excludedBlocks)
#print("BLOCK LIST")
#total_blocks = 0
#for i in block_count.keys():
#    #if ("TRANSLATION_MISSING" in i):
#    print("{}: {}".format(i, block_count[i]))
#
#    total_blocks += block_count[i]
#print("TOTAL NUMBER OF BLOCKS ", total_blocks)
