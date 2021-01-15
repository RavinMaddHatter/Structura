import json
from PIL import Image
import numpy as np
import copy
import os


class armorstand:
    def __init__(self, size=[64, 64, 64], ref_pack="Vanilla_Resource_Pack"):
        self.ref_resource_pack = ref_pack
        with open("{}/blocks.json".format(self.ref_resource_pack)) as f:
            self.blocks_def = json.load(f)
        with open("{}/textures/terrain_texture.json".format(self.ref_resource_pack)) as f:
            self.terrain_texture = json.load(f)
        with open("block_rotation.json") as f:
            self.block_rotations = json.load(f)
        self.stand = {}
        self.texture_list = []
        self.geometry = {}
        self.stand_init()
        self.uv_map = {}
        self.blocks = {}
        self.size = []
        self.bones = []
        self.uv_array = None
        self.lower_objects = ["powered_repeater", "unpowered_repeater", "unpowered_comparator", "activator_rail", "detector_rail",
                              "golden_rail", "rail", "powered_comparator", "spruce_pressure_plate", "stone_pressure_plate", "redstone_wire", "frame", "carpet"]
        self.excluded = ["air", "grass", "structure_block"]

    def export(self, pack_folder):
        self.add_blocks_to_bones()
        self.geometry["description"]["texture_height"] = len(
            self.uv_map.keys())
        self.stand["minecraft:geometry"] = [self.geometry]
        path_to_geo = "{}/models/entity/armor_stand.ghost_blocks.geo.json".format(
            pack_folder)

        os.makedirs(os.path.dirname(path_to_geo), exist_ok=True)
        with open(path_to_geo, "w+") as json_file:
            json.dump(self.stand, json_file, indent=2)
        texture_name = "{}/textures/entity/ghost_blocks.png".format(
            pack_folder)
        os.makedirs(os.path.dirname(texture_name), exist_ok=True)
        self.save_uv(texture_name)


    def make_layer(self, y):
        # sets up a layer for us to refference in the animation controller later.
        layer_name = "layer_{}".format(y)
        self.geometry["bones"].append(
            {"name": layer_name, "pivot": [-8, 0, 8], "parent": "ghost_blocks"})

    def make_block(self, x, y, z, block_name, rot=None, top=False, trap_open=False, parent=None):
        # call this to add a block to the a bar of blocks that will be rendered
        if block_name not in self.excluded:
            slab = "slab" in block_name and "double" not in block_name
            wall = "wall" in block_name
            trapdoor = "trapdoor" in block_name or block_name in self.lower_objects
            uv = self.block_name_to_uv(block_name)
            if rot is not None:

                if block_name in self.block_rotations.keys():
                    piv = self.block_rotations[block_name][str(int(rot))]

                else:
                    piv = [0, 0, 0]
                    print("no rotation for {} found".format(block_name))
            else:
                piv = [0, 0, 0]
            if slab:
                size = [1, .5, 1]
                if top:
                    origin = [-1*(x+9), y+.5, z]
                else:
                    origin = [-1*(x+9), y, z]
            elif trapdoor:
                if trap_open:
                    size = [1, 2/16, 1]
                else:
                    size = [1, 2/16, 1]
                if top:
                    origin = [-1*(x+9), y+14/2, z]
                else:
                    origin = [-1*(x+9), y, z]
            elif wall:
                size = [.5, 1, .5]
                origin = [-1*(x+9)+.25, y, z+.25]
            else:
                origin = [-1*(x+9), y, z]
                size = [1, 1, 1]
            block_name = "block_{}_{}_{}".format(x, y, z)

            self.blocks[block_name] = {}
            self.blocks[block_name]["name"] = block_name
            self.blocks[block_name]["parent"] = "layer_{}".format(y)
            self.blocks[block_name]["pivot"] = [0, 0, 0]
            self.blocks[block_name]["cubes"] = []
            self.blocks[block_name]["cubes"].append(
                {"origin": origin, "size": size, "rotation": piv, "uv": uv, "inflate": -0.03})

    def rotate_observer_like(self, rot):
        if rot == 0:
            piv = [90, 0, 0]
        elif rot == 1:
            piv = [270, 0, 0]
        elif rot == 2:
            piv = [0, 0, 0]
        elif rot == 3:
            piv = [0, 180, 0]
        elif rot == 4:
            piv = [0, 270, 0]
        elif rot == 5:
            piv = [0, 90, 0]
        else:
            piv = [0, 0, 0]
        return piv

    def save_uv(self, name):
        # saves the texture file where you tell it to

        im = Image.fromarray(self.uv_array)
        im.save(name)

    def stand_init(self):
        # helper function to initialize the dictionary that will be exported as the json object
        self.stand["format_version"] = "1.12.0"
        self.geometry["description"] = {
            "identifier": "geometry.armor_stand.ghost_blocks"}
        self.geometry["description"]["texture_width"] = 1
        self.geometry["description"]["visible_bounds_offset"] = [
            0.0, 1.5, 0.0]
        # Changed render distance of the block geometry
        self.geometry["description"]["visible_bounds_width"] = 5120
        # Changed render distance of the block geometry
        self.geometry["description"]["visible_bounds_height"] = 5120
        self.geometry["bones"] = []
        self.stand["minecraft:geometry"] = [self.geometry]
        self.geometry["bones"] = [
            {"name": "ghost_blocks", "pivot": [-8, 0, 8]}]

    def extend_uv_image(self, new_image_filename):
        # helper function that just appends to the uv array to make things
        image = Image.open(new_image_filename)
        impt = np.array(image)
        image_array = np.ones([impt.shape[0], impt.shape[1], 4])*255
        image_array[0:impt.shape[0], 0:impt.shape[1], 0:impt.shape[2]] = impt
        image_array[:, :, 3] = image_array[:, :, 3]*.8
        if type(self.uv_array) is type(None):
            self.uv_array = image_array
        else:
            startshape = list(self.uv_array.shape)
            endshape = startshape.copy()
            endshape[0] += image_array.shape[0]
            temp_new = np.zeros(endshape, np.uint8)
            temp_new[0:startshape[0], :, :] = self.uv_array
            temp_new[startshape[0]:, :, :] = image_array
            self.uv_array = temp_new

    def block_name_to_uv(self, block_name, variant=0):
        # hellper function maps the the section of the uv file to the side of the block
        temp_uv = {}
        if block_name not in self.excluded:  # if you dont want a block to be rendered, exclude the UV
            texture_files = self.get_block_texture_paths(block_name, variant=0)
            if block_name == "sticky_piston":
                texture_files["up"] = "textures/blocks/piston_top_sticky"
            if block_name == "piston":
                texture_files["up"] = "textures/blocks/piston_top_normal"
            for key in texture_files.keys():
                if texture_files[key] not in self.uv_map.keys():
                    self.extend_uv_image(
                        "{}/{}.png".format(self.ref_resource_pack, texture_files[key]))
                    self.uv_map[texture_files[key]] = len(self.uv_map.keys())
                temp_uv[key] = {
                    "uv": [0, self.uv_map[texture_files[key]]], "uv_size": [1, 1]}

        return temp_uv

    def add_blocks_to_bones(self):
        # helper function for adding all of the bars, this is called during the writing step
        for key in self.blocks.keys():
            self.geometry["bones"].append(self.blocks[key])

    def get_block_texture_paths(self, blockName, variant=0):
        # helper function for getting the texture locations from the vanilla files.
        textureLayout = self.blocks_def[blockName]["textures"]
        texturedata = self.terrain_texture["texture_data"]
        textures = {}

        if type(textureLayout) is dict:
            if "side" in textureLayout.keys():
                textures["east"] = textureLayout["side"]
                textures["west"] = textureLayout["side"]
                textures["north"] = textureLayout["side"]
                textures["south"] = textureLayout["side"]
            if "east" in textureLayout.keys():
                textures["east"] = textureLayout["east"]
            if "west" in textureLayout.keys():
                textures["west"] = textureLayout["west"]
            if "north" in textureLayout.keys():
                textures["north"] = textureLayout["north"]
            if "south" in textureLayout.keys():
                textures["south"] = textureLayout["south"]
            if "down" in textureLayout.keys():
                textures["down"] = textureLayout["down"]
            if "up" in textureLayout.keys():
                textures["up"] = textureLayout["up"]
        elif type(textureLayout) is str:
            textures["east"] = textureLayout
            textures["west"] = textureLayout
            textures["north"] = textureLayout
            textures["south"] = textureLayout
            textures["up"] = textureLayout
            textures["down"] = textureLayout
        for key in textures.keys():
            if type(texturedata[textures[key]]["textures"]) is str:
                textures[key] = texturedata[textures[key]]["textures"]
            elif type(texturedata[textures[key]]["textures"]) is list:
                textures[key] = texturedata[textures[key]]["textures"][variant]
        return textures

    def loadbasefile(self, pathtofile):
        # unused function for loading an armorstand.
        with open(pathtofile) as f:
            self.stand = json.load(f)
        self.geometry = self.stand["minecraft:geometry"][0]
        self.stand["minecraft:geometry"] = [self.geometry]
