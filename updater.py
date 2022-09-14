import pooch
import os
cwd = os.getcwd()

os.environ["PATH_TO_STRUCTURA_LOOKUP"] = os.path.join(cwd,"lookups")
def_files_to_update=["block_definition.json",
                 "block_shapes.json",
                 "block_uv.json",
                 "variants.json",
                 "armor_stand.larger_render.geo.json",
                 "block_rotation.json",
                 "nbt_defs.json"]

def getLatest():

    
    registry={}
    for file in def_files_to_update:
        try:
            os.remove(os.path.join(cwd,"lookups",file))
        except:
            print("failed to delete:" +file)
            pass
        registry[file]=None


    definitions = pooch.create(
        # Use the default cache folder for the operating system
        path=pooch.os_cache("plumbus"),
        # The remote data is on Github
        base_url="https://github.com/RavinMaddHatter/Structura/tree/main/lookups",
        # If this is a development version, get the data from the "main" branch
        registry=registry,
        env="PATH_TO_STRUCTURA_LOOKUP",
    )
    for file in registry.keys():
        test=definitions.fetch(file)


