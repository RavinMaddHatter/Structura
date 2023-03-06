try:
    import ujson as json
except:
    print("using built in json, but that is much slower, consider installing ujson")
    import json
import os
import copy
import numpy as np

class render_controller:
    def __init__(self):
        self.rc={"format_version": "1.8.0"}
        self.rc["render_controllers"]={}
        self.rcname = "controller.render.armor_stand.ghost_blocks" 
        self.rc["render_controllers"][self.rcname] = {}
        materials = [{"*": "Material.ghost_blocks"}]
        self.rc["render_controllers"][self.rcname]["materials"]=materials
        self.rc["render_controllers"][self.rcname]["arrays"]={"geometries":{}}
        self.rc["render_controllers"][self.rcname]["arrays"]["geometries"]["array.ghost_geo"]=["geometry.default"]
        self.geometry= "array.ghost_geo[ variable.armor_stand.pose_index ]"
        self.textures = ["variable.armor_stand.pose_index != 0 ? Texture.ghost_blocks_1 : (Texture.default)"]
        self
    def add_geometry(self,name):
        name='geometry.ghost_blocks_{}'.format(name)
        self.rc["render_controllers"][self.rcname]["arrays"]["geometries"]["array.ghost_geo"].append(name)
    def export(self, pack_name):
        
        #self.geometry = self.geometry.format("Geometry.default")
        #self.textures = self.textures.format("Texture.default")
        self.rc["render_controllers"][self.rcname]["geometry"] = self.geometry
        self.rc["render_controllers"][self.rcname]["textures"] = self.textures
        
        rc = "armor_stand.ghost_blocks.render_controllers.json"
        rcpath = "{}/render_controllers/{}".format(pack_name, rc)
        os.makedirs(os.path.dirname(rcpath), exist_ok = True)
        
        with open(rcpath, "w+") as json_file:
            json.dump(self.rc, json_file, indent=2)
        
