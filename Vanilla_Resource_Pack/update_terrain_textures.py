import json
import os

with open("textures/terrain_texture.json") as file:
    terrain_texture = json.load(file)

textures = []

for (dirpath, dirnames, filenames) in os.walk("textures/blocks"):
    textures.extend(filenames)
    break

for texture in textures:
    if texture.endswith(".tga"):
        print(f"TGA found: {texture}")
        continue
    texture_name = texture.split(".png")[0]
    if not texture_name in terrain_texture["texture_data"]:
        terrain_texture["texture_data"][texture_name] = {"textures": f"textures/blocks/{texture_name}"}

with open("textures/terrain_texture.json","w") as file:
    json.dump(terrain_texture, file, indent=2)