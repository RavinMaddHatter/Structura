import json
from PIL import Image
import numpy as np
import copy
import os


class armorstand:
    def __init__(self, size=[64, 64, 64], ref_pack="Vanilla_Resource_Pack"):
        self.ref_resource_pack = ref_pack
        ## we load all of these items containing the mapping of blocks to the some property that is either hidden, implied or just not clear
        with open("{}/blocks.json".format(self.ref_resource_pack)) as f:
            ## defines the blocks from the NBT name tells us sides vs textures
            self.blocks_def = json.load(f)
        with open("{}/textures/terrain_texture.json".format(self.ref_resource_pack)) as f:
            ##maps textures names to texture files.
            self.terrain_texture = json.load(f)
        with open("lookups/block_rotation.json") as f:
            ## custom look up table i wrote to help with rotations, error messages dump if somehting has undefined rotations 
            self.block_rotations = json.load(f)
        with open("lookups/variants.json") as f:
            ## custom lookup table mapping the assume array location in the terrian texture to the relevant blocks IE log2 index 2 implies a specific wood type not captured anywhere
            self.block_variants = json.load(f)
        self.stand = {}
        self.texture_list = []
        self.geometry = {}
        self.stand_init()
        self.uv_map = {}
        self.blocks = {}
        self.size = []
        self.bones = []
        self.errors={}
        self.uv_array = None
        ## The stuff below is a horrible cludge that should get cleaned up. +1 karma to whomever has a better plan for this.
        # this is how i determine if something should be thin. it is ugly, but kinda works
        self.lower_objects = ["powered_repeater", "unpowered_repeater", "unpowered_comparator", "activator_rail", "detector_rail",
                              "golden_rail", "rail", "powered_comparator", "spruce_pressure_plate", "stone_pressure_plate", "redstone_wire", "frame", "carpet"]
        ## these blocks are either not needed, or cause issue. Grass is banned because the terrian_texture.json has a biome map in it. If someone wants to fix we can un-bann it
        self.excluded = ["air", "grass", "structure_block"]

    def export(self, pack_folder):
        ## This exporter just packs up the armorstand json files and dumps them where it should go. as well as exports the UV file
        self.add_blocks_to_bones()
        self.geometry["description"]["texture_height"] = len(
            self.uv_map.keys())
        self.stand["minecraft:geometry"] = [self.geometry] ## this is insuring the geometries are imported, there is an implied refference other places.
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
        # sets up a layer for us to refference in the animation controller later. Layers are moved during the poses 
        layer_name = "layer_{}".format(y)
        self.geometry["bones"].append(
            {"name": layer_name, "pivot": [-8, 0, 8], "parent": "ghost_blocks"})

    def make_block(self, x, y, z, block_name, rot=None, top=False, trap_open=False, parent=None,variant=None):
        # make_block handles all the block processing, This function does need cleanup and probably should be broken into other helperfunctions for ledgiblity.
        if block_name not in self.excluded:
            slab = "slab" in block_name and "double" not in block_name
            wall = "wall" in block_name
            torch = "torch" in block_name
            lantern = "lantern" in block_name
            stair = "stair" in block_name
            hopper = "hopper" in block_name
            trapdoor = "trapdoor" in block_name or block_name in self.lower_objects
            uv = self.block_name_to_uv(block_name,variant=variant)
            non_block=False
            if rot is not None and not stair and not hopper:
                if "trapdoor" in block_name:
                    rot_name = "trapdoor"
                else:
                    rot_name = block_name
                if rot_name in self.block_rotations.keys():
                    piv = self.block_rotations[rot_name][str(int(rot))]

                else:
                    piv = [0, 0, 0]
                    print("no rotation for {} found".format(block_name))
            else:
                piv = [0, 0, 0]
            pivot_point = None
            #the section below is the hardcoded block geometries. This likely should be broken into helper functions. It will make it easier to maintain....
            if slab:
                size = [1, .5, 1]
                uv["east"]["uv_size"][1] = 0.5
                uv["west"]["uv_size"][1] = 0.5
                uv["north"]["uv_size"][1] = 0.5
                uv["south"]["uv_size"][1] = 0.5
                if top:
                    origin = [-1*(x+9), y+.5, z]
                else:
                    origin = [-1*(x+9), y, z]
            elif trapdoor:
                if top and not trap_open:
                    origin = [-1*(x+9), y+14/16, z]
                else:
                    origin = [-1*(x+9), y, z]
                
                if trap_open:
                    pivot_point=[-1*(x+9)+.5, y+.5, z+.5]
                    size = [1, 1, 2/16]
                else:
                    size = [1, 2/16, 1]
            elif wall:
                size = [.5, 1, .5]
                origin = [-1*(x+9)+.25, y, z+.25]
                uv["east"]["uv_size"] = [0.5, 1]
                uv["west"]["uv_size"] = [0.5, 1]
                uv["north"]["uv_size"] = [0.5, 1]
                uv["south"]["uv_size"] = [0.5, 1]
            elif torch:
                size = [3/16, 10/16, 3/16]
                origin = [-1*(x+9) + (16-2)/32, y, z + (16-2)/32]
                uv["east"]["uv"] = [7/16, uv["east"]["uv"][1]+6/16]
                uv["east"]["uv_size"] = [2/16, 10/16]
                uv["west"]["uv"] = [7/16, uv["west"]["uv"][1]+6/16]
                uv["west"]["uv_size"] = [2/16, 10/16]
                uv["north"]["uv"] = [7/16, uv["north"]["uv"][1]+6/16]
                uv["north"]["uv_size"] = [2/16, 10/16]
                uv["south"]["uv"] = [7/16, uv["south"]["uv"][1]+6/16]
                uv["south"]["uv_size"] = [2/16, 10/16]
                uv["up"]["uv"] = [7/16, uv["up"]["uv"][1]+6/16]
                uv["up"]["uv_size"] = [2/16, 2/16]
                uv["down"]["uv"] = [7/16, uv["down"]["uv"][1]+14/16]
                uv["down"]["uv_size"] = [2/16,2/16]
            elif lantern:
                size = [6/16, 7/16, 6/16]
                origin = [-1*(x+9) + (16-6)/32, y + (16-7)/32, z + (16-6)/32]
                uv["east"]["uv"] = [0, uv["east"]["uv"][1]+2/16]
                uv["east"]["uv_size"] = [6/16, 7/16]
                uv["west"]["uv"] = [0, uv["west"]["uv"][1]+2/16]
                uv["west"]["uv_size"] = [6/16, 7/16]
                uv["north"]["uv"] = [0, uv["north"]["uv"][1]+2/16]
                uv["north"]["uv_size"] = [6/16, 7/16]
                uv["south"]["uv"] = [0, uv["south"]["uv"][1]+2/16]
                uv["south"]["uv_size"] = [6/16, 7/16]
                uv["up"]["uv"] = [0, uv["up"]["uv"][1]+9/16]
                uv["up"]["uv_size"] = [6/16, 6/16]
                uv["down"]["uv"] = [0, uv["down"]["uv"][1]+9/16]
                uv["down"]["uv_size"] = [6/16, 6/16]
            elif stair:
                self.stair(x, y, z, block_name,uv, rot, top)
                non_block=True
            elif hopper:
                self.make_hopper(x, y, z, block_name,uv, rot)
                non_block=True
            else:
                origin = [-1*(x+9), y, z]
                size = [1, 1, 1]
            ## the code below assumes 1 cube, the helper functions for hoppers and stairs handle proper blocks,
            ## Probably should just move all this to helper functions for each block geo
                
            if not non_block:
                block_name = "block_{}_{}_{}".format(x, y, z)

                self.blocks[block_name] = {}
                self.blocks[block_name]["name"] = block_name
                self.blocks[block_name]["parent"] = "layer_{}".format(y)
                self.blocks[block_name]["pivot"] = [0, 0, 0]
                self.blocks[block_name]["cubes"] = []
                if pivot_point is not None:
                    self.blocks[block_name]["cubes"].append(
                        {"origin": origin, "size": size, "rotation": piv, "uv": uv, "inflate": -0.03,"pivot":pivot_point})
                else:
                    self.blocks[block_name]["cubes"].append(
                        {"origin": origin, "size": size, "rotation": piv, "uv": uv, "inflate": -0.03})
                
                    
                
    def make_hopper(self, x, y, z, block_name,uv, rot=None):
        ## helper function for hoppers. it is a bit ugly, but it works
        block_name = "block_{}_{}_{}".format(x, y, z)
        block1 = {}
        block1["origin"] = [-1*(x+9), y+9/16, z]
        block1["size"] = [1, 7/16, 1]
        block1["inflate"] = -0.03
        block1uv=dict(uv)
        block1uv["east"]["uv_size"] = [1, 6/16]
        block1uv["west"]["uv_size"] = [1, 6/16]
        block1uv["north"]["uv_size"] = [1, 6/16]
        block1uv["south"]["uv_size"] = [1, 6/16]
        block1["uv"]=block1uv
        block2={}
        block2["origin"] = [-1*(x+9) + 0.25, y+4/16, z + 0.25]
        block2["size"] = [.5, 6/16, 0.5]
        block2["inflate"] = -0.03
        block2uv=dict(uv)
        block2uv["east"]["uv_size"] = [0.5, 6/16]
        block2uv["west"]["uv_size"] = [0.5, 6/16]
        block2uv["north"]["uv_size"] = [0.5, 6/16]
        block2uv["south"]["uv_size"] = [0.5, 6/16]
        block2["uv"]=block2uv
        
        block3={}
        
        block3["size"] = [4/16, 4/16, 4/16]
        block3["inflate"] = -0.03
        block3uv=dict(uv)
        block3uv["east"]["uv_size"] = [4/16, 4/16]
        block3uv["west"]["uv_size"] = [4/16, 4/16]
        block3uv["north"]["uv_size"] = [4/16, 4/16]
        block3uv["south"]["uv_size"] = [4/16, 4/16]
        block3["uv"]=block2uv
        if rot == 0:
            block3["origin"] = [-1*(x+9) + 6/16, y+1/16, z + 6/16]
        elif rot == 5:
            block3["origin"] = [-1*(x+9) + 1/16, y + 5/16, z + 6/16]
        elif rot == 2:
            block3["origin"] = [-1*(x+9) + 6/16, y + 5/16, z + 1/16]
        elif rot == 3:
            block3["origin"] = [-1*(x+9) + 6/16, y + 5/16, z + 1 - 6/16]
        elif rot == 4:
            block3["origin"] = [-1*(x+9) + 1 - 6/16, y + 5/16, z + 6/16]
            
        self.blocks[block_name] = {}
        self.blocks[block_name]["name"] = block_name
        self.blocks[block_name]["parent"] = "layer_{}".format(y)
        self.blocks[block_name]["pivot"] = [0, 0, 0]
        self.blocks[block_name]["cubes"] = [block1]
        self.blocks[block_name]["cubes"].append(block2)
        self.blocks[block_name]["cubes"].append(block3)
    def stair(self, x, y, z, block_name,uv, rot=None,top=None):
        ##helper function for stair creation. currently does not support corner stairs. 
        block_name = "block_{}_{}_{}".format(x, y, z)
        block1 = {}
        offset = 0
        if top:
            offset = 7/16
        block1["origin"] = [-1*(x+9), y + offset, z]
        block1["size"] = [1, 0.5, 1]
        block1["inflate"] = -0.03
        block1uv=dict(uv)
        block1uv["east"]["uv_size"] = [1, 0.5]
        block1uv["west"]["uv_size"] = [1, 0.5]
        block1uv["north"]["uv_size"] = [1, 0.5]
        block1uv["south"]["uv_size"] = [1, 0.5]
        block1["uv"]=block1uv
        if rot == 0:
            rotation = [0, 90, 0]
        elif rot == 1:
            rotation = [0, -90, 0]
        elif rot == 2:
            rotation = [0, 180, 0]
        elif rot == 3:
            rotation = [0, 0, 0]

        
        block2={}
        block2["origin"] = [-1*(x+9), y + 7/16 - offset, z]
        block2["size"] = [1, 0.5, 0.5]
        block2["rotation"]=rotation
        block2["pivot"]=[-1*(x+9) + 0.5, y + 0.5 - offset, z + 0.5]
        block2["inflate"] = -0.03
        block2uv=dict(uv)
        block2uv["east"]["uv_size"] = [1, 1]
        block2uv["west"]["uv_size"] = [1, 1]
        block2uv["north"]["uv_size"] = [1, 1]
        block2uv["south"]["uv_size"] = [1, 1]
        block2uv["up"]["uv_size"] = [1, 1]
        block2uv["down"]["uv_size"] = [1, 1]
        block2["uv"]=block2uv
            
        self.blocks[block_name] = {}
        self.blocks[block_name]["name"] = block_name
        self.blocks[block_name]["parent"] = "layer_{}".format(y)
        self.blocks[block_name]["pivot"] = [0.5, 0.5, 0.5]
        self.blocks[block_name]["cubes"] = [block1]
        self.blocks[block_name]["cubes"].append(block2)
        
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
        shape=list(impt.shape)
        if shape[0]>16:
            shape[0]=16
            impt=impt[0:16,:,:]
        if shape[1]>16:
            shape[1]=16
            impt=impt[:,0:16,:]
        image_array = np.ones([16, 16, 4],np.uint8)*255
        image_array[0:shape[0], 0:shape[1], 0:impt.shape[2]] = impt
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

    def block_name_to_uv(self, block_name, variant = ""):
        
        # helper function maps the the section of the uv file to the side of the block
        temp_uv = {}
        if block_name not in self.excluded:  # if you dont want a block to be rendered, exclude the UV
            texture_files = self.get_block_texture_paths(block_name, variant = variant)
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

    def get_block_texture_paths(self, blockName, variant = ""):
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
                index=0
                if variant[0] in self.block_variants.keys():
                    index=self.block_variants[variant[0]][variant[1] ]
                textures[key] = texturedata[textures[key]]["textures"][index]

            
        return textures
