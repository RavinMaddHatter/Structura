import json
from PIL import Image
import numpy as np
import copy
import os

debug=False
class armorstandgeo:
    def __init__(self, name, alpha = 0.8,offsets=[9,0,0], size=[64, 64, 64], ref_pack="Vanilla_Resource_Pack"):
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
        with open("lookups/block_definition.json") as f:
            self.defs = json.load(f)
        with open("lookups/block_shapes.json") as f:
            self.block_shapes = json.load(f)
        with open("lookups/block_uv.json") as f:
            self.block_uv = json.load(f)
        self.name = name.replace(" ","_").lower()
        self.stand = {}
        self.offsets = offsets
        self.alpha=alpha
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

        
        ## these blocks are either not needed, or cause issue. Grass is banned because the terrian_texture.json has a biome map in it. If someone wants to fix we can un-bann it
        self.excluded = ["air", "structure_block"]

    def export(self, pack_folder):
        ## This exporter just packs up the armorstand json files and dumps them where it should go. as well as exports the UV file
        self.add_blocks_to_bones()
        self.geometry["description"]["texture_height"] = len(
            self.uv_map.keys())
        self.stand["minecraft:geometry"] = [self.geometry] ## this is insuring the geometries are imported, there is an implied refference other places.
        path_to_geo = "{}/models/entity/armor_stand.ghost_blocks_{}.geo.json".format(
            pack_folder,self.name)
        os.makedirs(os.path.dirname(path_to_geo), exist_ok=True)
        i=0
        for index in range(len(self.stand["minecraft:geometry"][0]["bones"])):
            if "name" not in self.stand["minecraft:geometry"][0]["bones"][index].keys():
                self.stand["minecraft:geometry"][0]["bones"][index]["name"]="empty_row+{}".format(i)
                self.stand["minecraft:geometry"][0]["bones"][index]["parent"]="ghost_blocks"
                self.stand["minecraft:geometry"][0]["bones"][index]["pivot"]=[0.5,0.5,0.5]
                i+=1
            
        with open(path_to_geo, "w+") as json_file:
            json.dump(self.stand, json_file, indent=2)
        texture_name = "{}/textures/entity/ghost_blocks_{}.png".format(
            pack_folder,self.name)
        os.makedirs(os.path.dirname(texture_name), exist_ok=True)
        self.save_uv(texture_name)


    def make_layer(self, y):
        # sets up a layer for us to refference in the animation controller later. Layers are moved during the poses 
        layer_name = "layer_{}".format(y)
        self.geometry["bones"].append(
            {"name": layer_name, "pivot": [-8, 0, 8], "parent": "ghost_blocks"})

    def make_block(self, x, y, z, block_name, rot=None, top=False,data=0, trap_open=False, parent=None,variant=None):
        # make_block handles all the block processing, This function does need cleanup and probably should be broken into other helperfunctions for ledgiblity.
        block_type = self.defs[block_name]
        if block_type!="ignore":
            if debug:
                print(block_name)
            ghost_block_name = "block_{}_{}_{}".format(x, y, z)
            self.blocks[ghost_block_name] = {}
            block_type = self.defs[block_name]
            ## hardcoded to true for now, but this is when the variants will be called
            shape_variant="default"
            if block_type == "hopper" and rot!=0:
                shape_variant="side"
            elif block_type == "trapdoor" and trap_open:
                shape_variant = "open"
            elif top:
                shape_variant = "top"

            if data!=0:
                print(data)

            block_shapes = self.block_shapes[block_type][shape_variant]
            block_uv = self.block_uv[block_type]["default"]
            if shape_variant in self.block_uv[block_type].keys():
                block_uv = self.block_uv[block_type][shape_variant]
            if str(data) in self.block_uv[block_type].keys():
                shape_variant=str(data)
            if str(data) in self.block_shapes[block_type].keys():
                block_shapes = self.block_shapes[block_type][str(data)]
                print(block_shapes)
            if block_type in self.block_rotations.keys():
                rotation = self.block_rotations[block_type][str(rot)]
            else:
                rotation = [0, 0, 0]
                if debug:
                    print("no rotation for block type {} found".format(block_type))
            self.blocks[ghost_block_name]["cubes"] = []
            uv_idx=0
            
            for i in range(len(block_shapes["size"])):
                uv = self.block_name_to_uv(block_name,variant=variant,shape_variant=shape_variant,index=i)
                block={}
                if len(block_uv["uv_sizes"]["up"])>i:
                    uv_idx=i
                xoff = 0
                yoff = 0
                zoff = 0
                if "offsets" in block_shapes.keys():
                    xoff = block_shapes["offsets"][i][0]
                    yoff = block_shapes["offsets"][i][1]
                    zoff = block_shapes["offsets"][i][2]
                block["origin"] = [-1*(x + self.offsets[0]) + xoff, y + yoff + self.offsets[1], z + zoff + self.offsets[2]]
                block["size"] = block_shapes["size"][i]
                block["inflate"] = -0.03
                block["pivot"]=[-1*(x + self.offsets[0]) + 0.5, y + 0.5 + self.offsets[1], z + 0.5 + self.offsets[2]]
                block["rotation"]=rotation
                
                blockUV=dict(uv)
                blockUV["up"]["uv"][0] += block_uv["offset"]["up"][uv_idx][0]
                blockUV["up"]["uv"][1] += block_uv["offset"]["up"][uv_idx][1]
                blockUV["down"]["uv"][0] += block_uv["offset"]["down"][uv_idx][0]
                blockUV["down"]["uv"][1] += block_uv["offset"]["down"][uv_idx][1]
                blockUV["east"]["uv"][0] += block_uv["offset"]["east"][uv_idx][0]
                blockUV["east"]["uv"][1] += block_uv["offset"]["east"][uv_idx][1]
                blockUV["west"]["uv"][0] += block_uv["offset"]["west"][uv_idx][0]
                blockUV["west"]["uv"][1] += block_uv["offset"]["west"][uv_idx][1]
                blockUV["north"]["uv"][0] += block_uv["offset"]["north"][uv_idx][0]
                blockUV["north"]["uv"][1] += block_uv["offset"]["north"][uv_idx][1]
                blockUV["south"]["uv"][0] += block_uv["offset"]["south"][uv_idx][0]
                blockUV["south"]["uv"][1] += block_uv["offset"]["south"][uv_idx][1]
                blockUV["up"]["uv_size"] = block_uv["uv_sizes"]["up"][uv_idx]
                blockUV["down"]["uv_size"] = block_uv["uv_sizes"]["down"][uv_idx]
                blockUV["east"]["uv_size"] = block_uv["uv_sizes"]["east"][uv_idx]
                blockUV["west"]["uv_size"] = block_uv["uv_sizes"]["west"][uv_idx]
                blockUV["north"]["uv_size"] = block_uv["uv_sizes"]["north"][uv_idx]
                blockUV["south"]["uv_size"] = block_uv["uv_sizes"]["south"][uv_idx]
                
                block["uv"]=blockUV
                self.blocks[ghost_block_name]["cubes"].append(block)
            

            
            self.blocks[ghost_block_name]["name"] = ghost_block_name
            self.blocks[ghost_block_name]["parent"] = "layer_{}".format(y)
            self.blocks[ghost_block_name]["pivot"] = block_shapes["center"]
        
    def save_uv(self, name):
        # saves the texture file where you tell it to
        im = Image.fromarray(self.uv_array)
        im.save(name)

    def stand_init(self):
        # helper function to initialize the dictionary that will be exported as the json object
        self.stand["format_version"] = "1.12.0"
        self.geometry["description"] = {
            "identifier": "geometry.armor_stand.ghost_blocks_{}".format(self.name)}
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
                                    {"name": "ghost_blocks",
                                     "pivot": [-8, 0, 8]}]

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
        image_array[:, :, 3] = image_array[:, :, 3] * self.alpha
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

    def block_name_to_uv(self, block_name, variant = "",shape_variant="default",index=0,data=0):
        
        # helper function maps the the section of the uv file to the side of the block
        temp_uv = {}
        if block_name not in self.excluded:  # if you dont want a block to be rendered, exclude the UV

            block_type = self.defs[block_name]
            
            texture_files = self.get_block_texture_paths(block_name, variant = variant)

            corrected_textures={}
            if shape_variant in self.block_uv[block_type].keys():
                if "overwrite" in self.block_uv[block_type][shape_variant].keys():
                    corrected_textures = self.block_uv[block_type][shape_variant]["overwrite"]
            else:
                if "overwrite" in self.block_uv[block_type]["default"].keys():
                    corrected_textures = self.block_uv[block_type]["default"]["overwrite"]
            
            for side in corrected_textures.keys():
                if len(corrected_textures[side])>index:
                    if corrected_textures[side][index] != "default":
                        texture_files[side]=corrected_textures[side][index]
                        if debug:
                            print("{}: {}".format(side,texture_files[side]))
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
