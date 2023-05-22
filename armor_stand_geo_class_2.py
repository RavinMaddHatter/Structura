try:
    import ujson as json
except:
    print("using built in json, but that is much slower, consider installing ujson")
    import json
from PIL import Image
from numpy import array, ones, uint8, zeros
import copy
import os
import time

debug=False


class armorstandgeo:
    def __init__(self, name, alpha = 0.8,offsets=[0,0,0], size=[64, 64, 64], ref_pack="Vanilla_Resource_Pack"):
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
        self.offsets[0]+=8
        self.offsets[2]+=7
        self.alpha=alpha
        self.texture_list = []
        self.geometry = {}
        self.stand_init()
        self.uv_map = {}
        self.blocks = {}
        self.size = size
        self.bones = []
        self.errors={}
        self.layers=[]
        self.uv_array = None
        self.pre_gen_blocks={}
        ## The stuff below is a horrible cludge that should get cleaned up. +1 karma to whomever has a better plan for this.
        # this is how i determine if something should be thin. it is ugly, but kinda works

        
        ## these blocks are either not needed, or cause issue. Grass is banned because the terrian_texture.json has a biome map in it. If someone wants to fix we can un-bann it
        self.excluded = ["air", "structure_block"]

    def export(self, pack_folder):
        start = time.time()
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
        start=time.time()
        with open(path_to_geo, "w+") as json_file:
            json.dump(self.stand, json_file)
        texture_name = "{}/textures/entity/ghost_blocks_{}.png".format(
            pack_folder,self.name)
        os.makedirs(os.path.dirname(texture_name), exist_ok=True)
        self.save_uv(texture_name)
        
    def export_big(self, pack_folder):
        ## This exporter just packs up the armorstand json files and dumps them where it should go. as well as exports the UV file
        self.stand["minecraft:geometry"] = []
        size=list(map(int,self.size))
        offset=[-size[0]//2,0,-size[2]//2]
        geometries={}
        geometries["default"]={}
        geometries["default"]["description"]={}
        geometries["default"]["description"]["identifier"] = "geometry.armor_stand.default"
        geometries["default"]["description"]["texture_width"] = 1
        geometries["default"]["description"]["texture_height"] = 1
        geometries["default"]["description"]["visible_bounds_width"] = 5120
        geometries["default"]["description"]["visible_bounds_height"] = 5120
        geometries["default"]["description"]["visible_bounds_offset"] = [0, 1.5, 0]     
        geometries["default"]["bones"]=[{"name":"ghost_blocks","pivot": [-8, 0, 8],"origin":[0,0,0]}]
        default_geo=[{"origin": offset,"size": size,
                        "uv": {
                                "north": {"uv": [0, 0], "uv_size": [1, 1]},
                                "east": {"uv": [0, 0], "uv_size": [1, 1]},
                                "south": {"uv": [0, 0], "uv_size": [1, 1]},
                                "west": {"uv": [0, 0], "uv_size": [1, 1]},
                                "up": {"uv": [1, 1], "uv_size": [-1, -1]},
                                "down": {"uv": [1, 1], "uv_size": [-1, -1]}
                        }},
                     {"origin": offset,
                        "size": size,
                        "uv": {
                                "north": {"uv": [0, 3], "uv_size": [1, -1]},
                                "east": {"uv": [0, 3], "uv_size": [1, -1]},
                                "south": {"uv": [0, 3], "uv_size": [1, -1]},
                                "west": {"uv": [0, 3], "uv_size": [1, -1]},
                                "up": {"uv": [0, 1], "uv_size": [1, -1]},
                                "down": {"uv": [0, 3], "uv_size": [1, -1]}
                        }}]
        geometries["default"]["bones"][0]["cubes"]=default_geo
        for i in range(len(self.layers)):
            layer_name=self.layers[i]
            geometries[layer_name] = {}
            geometries[layer_name]["description"] = {}
            geometries[layer_name]["description"]["identifier"] = "geometry.armor_stand.ghost_blocks_{}".format(i)
            geometries[layer_name]["description"]["texture_width"] = 1
            geometries[layer_name]["description"]["texture_height"] = len(self.uv_map.keys())
            geometries[layer_name]["description"]["visible_bounds_width"] = 5120
            geometries[layer_name]["description"]["visible_bounds_height"] = 5120
            geometries[layer_name]["description"]["visible_bounds_offset"] = [0, 1.5, 0]
            geometries[layer_name]["bones"]=[{"name": "ghost_blocks","pivot": [-8, 0, 8]},## i am not sure this should be this value for pivot
                                             {"name": "layer_"+str(i),"parent": "ghost_blocks","pivot": [-8, 0, 8]}]## i am not sure this should be this value for pivot
        
        
        for key in self.blocks.keys():
            layer_name = self.blocks[key]["parent"]
            geometries[layer_name]["bones"].append(self.blocks[key])
        self.stand["minecraft:geometry"].append(geometries["default"])
        for layer_name in self.layers:
            self.stand["minecraft:geometry"].append(geometries[layer_name])
            
        path_to_geo = "{}/models/entity/armor_stand.ghost_blocks_{}.geo.json".format(pack_folder,self.name)
        os.makedirs(os.path.dirname(path_to_geo), exist_ok=True)            
        with open(path_to_geo, "w+") as json_file:
            json.dump(self.stand, json_file, indent=2)
        
        
        for i in range(len(self.layers)):
            texture_name = "{}/textures/entity/ghost_blocks_{}.png".format(pack_folder,i)
            os.makedirs(os.path.dirname(texture_name), exist_ok=True)
            self.save_uv(texture_name)

    
    def make_layer(self, y):
        # sets up a layer for us to refference in the animation controller later. Layers are moved during the poses 
        layer_name = "layer_{}".format(y)
        self.geometry["bones"].append(
            {"name": layer_name, "parent": "ghost_blocks"})#, "pivot": [-8, 0, 8]})

    def make_block(self, x, y, z, block_name, rot=None, top=False,data=0, trap_open=False, parent=None,variant="default"):
        # make_block handles all the block processing, This function does need cleanup and probably should be broken into other helperfunctions for ledgiblity.
        block_type = self.defs[block_name]
        if block_type!="ignore":
            ghost_block_name = "block_{}_{}_{}".format(x, y, z)
            self.blocks[ghost_block_name] = {}
            self.blocks[ghost_block_name]["name"] = ghost_block_name
            layer_name = "layer_{}".format(y % (12))
            if layer_name not in self.layers:
                self.layers.append(layer_name)
            self.blocks[ghost_block_name]["parent"] = layer_name
            block_type = self.defs[block_name]
            ## hardcoded to true for now, but this is when the variants will be called
            shape_variant="default"
            if block_type == "hopper" and rot!=0:
                shape_variant="side"
            elif block_type == "trapdoor" and trap_open:
                shape_variant = "open"
            elif block_type == "lever" and trap_open:
                shape_variant = "on"
            elif top:
                shape_variant = "top"

            if data!=0 and debug:
                print(data)
            

            block_shapes = self.block_shapes[block_type][shape_variant]
            self.blocks[ghost_block_name]["pivot"] = [block_shapes["center"][0] - (x + self.offsets[0]),
                                                      y + block_shapes["center"][1] + self.offsets[1],
                                                      z + block_shapes["center"][2] + self.offsets[2]]
            self.blocks[ghost_block_name]["inflate"] = -0.03

            block_uv = self.block_uv[block_type]["default"]
            if shape_variant in self.block_uv[block_type].keys():
                block_uv = self.block_uv[block_type][shape_variant]
            if str(data) in self.block_uv[block_type].keys():
                shape_variant=str(data)
            if str(data) in self.block_shapes[block_type].keys():
                block_shapes = self.block_shapes[block_type][str(data)]
            if block_type in self.block_rotations.keys() and rot is not None:
                self.blocks[ghost_block_name]["rotation"] = self.block_rotations[block_type][str(rot)]
            else:
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

                if "rotation" in block_shapes.keys():
                    block["rotation"] = block_shapes["rotation"][i]

                blockUV=dict(uv)
                for dir in ["up", "down", "east", "west", "north", "south"]:
                    blockUV[dir]["uv"][0] += block_uv["offset"][dir][uv_idx][0]
                    blockUV[dir]["uv"][1] += block_uv["offset"][dir][uv_idx][1]
                    blockUV[dir]["uv_size"] = block_uv["uv_sizes"][dir][uv_idx]

                block["uv"] = blockUV
                self.blocks[ghost_block_name]["cubes"].append(block)

    def save_uv(self, name):
        # saves the texture file where you tell it to
        if self.uv_array is None:
            print("No Blocks Were found")
        else:
            im = Image.fromarray(self.uv_array)
            im.save(name)

    def stand_init(self):
        # helper function to initialize the dictionary that will be exported as the json object
        self.stand["format_version"] = "1.16.0"
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
        impt = array(image)
        shape=list(impt.shape)
        if shape[0]>16:
            shape[0]=16
            impt=impt[0:16,:,:]
        if shape[1]>16:
            shape[1]=16
            impt=impt[:,0:16,:]
        image_array = ones([16, 16, 4],uint8)*255
        image_array[0:shape[0], 0:shape[1], 0:impt.shape[2]] = impt
        image_array[:, :, 3] = image_array[:, :, 3] * self.alpha
        if type(self.uv_array) is type(None):
            self.uv_array = image_array
        else:
            startshape = list(self.uv_array.shape)
            endshape = startshape.copy()
            endshape[0] += image_array.shape[0]
            temp_new = zeros(endshape, uint8)
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
                if debug:
                    print(index)
                    print(key)
                    print(texturedata[textures[key]]["textures"])
                    print(texturedata[textures[key]]["textures"][index])
                textures[key] = texturedata[textures[key]]["textures"][index]

            
        return textures
