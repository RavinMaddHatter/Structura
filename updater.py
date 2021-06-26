import pooch
import os
cwd = os.getcwd()

os.environ["PATH_TO_STRUCTURA_LOOKUP"] = os.path.join(cwd,"lookups")


def getUpdates():
    registry={
            "block_definition.json": None,
            "block_shapes.json": None,
            "block_uv.json": None,
            "variants.json": None,
            "armor_stand.larger_render.geo.json": None,
            "block_rotation.json": None
        }
    definitions = pooch.create(
        # Use the default cache folder for the operating system
        path=pooch.os_cache("plumbus"),
        # The remote data is on Github
        base_url="https://github.com/RavinMaddHatter/Structura/tree/1.4-development/lookups/",
        # If this is a development version, get the data from the "main" branch
        registry=registry,
        env="PATH_TO_STRUCTURA_LOOKUP",
    )
    for file in registry.keys():
        test=definitions.fetch(file)

    

