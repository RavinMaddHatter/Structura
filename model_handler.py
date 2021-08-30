import os
import json
from PIL import Image


model = ""
uvlock = False
x_rot = 0
y_rot = 0
z_rot = 0
blockstates_directory = 'Vanilla_Java_Resource_Pack/blockstates'
models_directory = 'Vanilla_Java_Resource_Pack/models'
textures_directory = 'Vanilla_Java_Resource_Pack/textures'
textures_list = []


def asign_model(block_matrix):
    global model, uvlock, x_rot, y_rot, z_rot, blockstates_directory, models_directory

    for x in range(len(block_matrix)):
        for y in range(len(block_matrix[0])):
            for z in range(len(block_matrix[0][0])):
                model = ""
                uvlock = False
                x_rot = 0
                y_rot = 0
                z_rot = 0
                for blockstate_file_name in os.listdir(blockstates_directory):
                    # Get the block id without variants
                    if block_matrix[x][y][z] == None:
                        break
                    java_id_nv = block_matrix[x][y][z].java_id.split("[")[0]
                    try:
                        if blockstate_file_name.replace(".json", "") == java_id_nv.replace("minecraft:", ""):
                            file = open(blockstates_directory +
                                        "/" + blockstate_file_name, 'r')
                            file_contents = json.load(file)
                            file.close()

                            if "variants" in file_contents:
                                # Get the block variants
                                try:
                                    java_variants = block_matrix[x][y][z].java_id.split("[")[
                                        1][:-1]
                                except IndexError:
                                    java_variants = ""
                                for variant in file_contents["variants"]:
                                    if variant == java_variants:
                                        assign_values(file_contents,
                                                      variant, block_matrix[x][y][z].java_id)
                                        break
                            elif "multipart" in file_contents:
                                # TODO Handle Multipart later
                                print(
                                    "Block with id: \"" + block_matrix[x][y][z].be_id + "\" is a multipart block which is not supported yet. Skipping.")
                                raise(MultipartException)

                            block_matrix[x][y][z].cubes = java_to_be_model(
                                model, x, y, z, [])

                            block_matrix[x][y][z].rotation = [
                                x_rot, y_rot, z_rot]

                            break

                    except NoModelException:
                        pass
                    except MultipartException:
                        pass


def assign_values(file_contents, variant, block_id):
    global model, uvlock, x_rot, y_rot, z_rot
    # Some blocks which display a random texture rotation have multiple blockstates for a same variant, we choose only first
    if type(variant) == list or type(variant) == tuple:
        value = variant[0]
    else:
        value = variant
    if file_contents["variants"][value]["model"] == None or file_contents["variants"][value]["model"] == "":
        print(
            "Block with id: \"" + block_id + "\" has no model")
        raise(NoModelException)
    else:
        model = file_contents["variants"][value]["model"]
    if "uv_lock" in file_contents["variants"][value]:
        uvlock = file_contents["variants"][value]["uvlock"]
    if "x" in file_contents["variants"][value]:
        x_rot = file_contents["variants"][value]["x"]
    if "y" in file_contents["variants"][value]:
        y_rot = file_contents["variants"][value]["y"]
    if "z" in file_contents["variants"][value]:
        z_rot = file_contents["variants"][value]["z"]


def java_to_be_model(model_file_name, x, y, z, block_textures_list):
    global model, textures_list
    if model_file_name.replace("minecraft:", "") == "block/air" or model_file_name.replace("minecraft:", "") == "":
        return []

    file = open(models_directory + "/" +
                model_file_name.replace("minecraft:", "") + ".json", 'r')
    file_contents = json.load(file)
    file.close()

    # Manage the textures (we first work out the textures as is needed to set the propper uv later)
    if "textures" in file_contents:
        for texture in file_contents["textures"]:
            if file_contents["textures"][texture][0] == "#":
                for block_texture in block_textures_list:
                    for value in block_texture:
                        if value == file_contents["textures"][texture].replace("#", ""):
                            file_contents["textures"][texture] = block_textures_list[block_textures_list.index(
                                block_texture)][value].replace("minecraft:", "")

            texture_path = file_contents["textures"][texture].replace(
                "minecraft:", "")
            if texture_path not in textures_list:
                textures_list.append(texture_path)
            block_textures_list.append(
                {texture: file_contents["textures"][texture]})

    # Manage the model
    if "parent" in file_contents and "elements" not in file_contents:
        return java_to_be_model(file_contents["parent"], x, y, z, block_textures_list)
    elif "elements" not in file_contents:
        print("Block with id: \"" + model_file_name + "\" has no model")
        raise(NoModelException)
    else:
        for element in file_contents["elements"]:
            # Get cube size
            element["size"] = [0, 0, 0]
            element["size"][0] = element["to"][0] - element["from"][0]
            element["size"][1] = element["to"][1] - element["from"][1]
            element["size"][2] = element["to"][2] - element["from"][2]

            # Move origin x and z -8 to center block and delete unnecesary keys
            element["origin"] = element.pop("from")
            element["origin"][0] = element["origin"][0] - 8
            element["origin"][2] = element["origin"][2] - 8
            element.pop("to")

            # Convert faces
            element["uv"] = {}
            for face in element["faces"]:
                element["uv"][face] = {}
                try:
                    element["uv"][face]["uv_size"] = [element["faces"][face]["uv"][2] - element["faces"]
                                                      [face]["uv"][0], element["faces"][face]["uv"][3] - element["faces"][face]["uv"][1]]
                    element["uv"][face]["uv"] = [element["faces"][face]
                                                 ["uv"][0], element["faces"][face]["uv"][1]]
                except KeyError:
                    element["uv"][face]["uv_size"] = [16, 16]
                    element["uv"][face]["uv"] = [0, 0]

                # If texture is top or bottom and size is 16x16 rotate it 180 
                if abs(element["uv"][face]["uv_size"][0]) == 16 and abs(element["uv"][face]["uv_size"][1]) == 16:
                    if face == "up" or face == "down":
                        element["uv"][face]["uv_size"][0] = -element["uv"][face]["uv_size"][0]
                        element["uv"][face]["uv"][0] = element["uv"][face]["uv"][0] + 16
                        element["uv"][face]["uv_size"][1] = -element["uv"][face]["uv_size"][1]
                        element["uv"][face]["uv"][1] = (0 if element["uv"][face]["uv"][1] == 16 else 16)

                try:
                    cube_face_texture = element["faces"][face]["texture"]
                    for texture in block_textures_list:
                        for value in texture:
                            if cube_face_texture.replace("#", "") == value:
                                texture_offset = textures_list.index(texture[value].replace("minecraft:", ""))
                                element["uv"][face]["uv"][0] = element["uv"][face]["uv"][0] + \
                                    texture_offset * 16
                                break
                except:
                    pass

                try:
                    element["uv"][face].pop("cullface")
                except:
                    pass
                try:
                    element.pop("__comment")
                except:
                    pass
                try:
                    element.pop("shade")
                except:
                    pass

            if "rotation" in element:
                # Apply cube rotation
                element["pivot"] = element["rotation"]["origin"]
                element["pivot"][0] = element["pivot"][0] - 16*x - 8
                element["pivot"][1] = element["pivot"][1] + 16*y
                element["pivot"][2] = element["pivot"][2] + 16*z - 8
                angle = element["rotation"]["angle"]
                if element["rotation"]["axis"] == "x":
                    element["rotation"] = [-angle, 0, 0]
                elif element["rotation"]["axis"] == "y":
                    element["rotation"] = [0, angle, 0]
                elif element["rotation"]["axis"] == "z":
                    element["rotation"] = [0, 0, angle]
            else:
                # Apply general rotation
                element["rotation"] = [0, 0, 0]
                element["pivot"] = [-16*x - 8, 16*y, 16*z - 8]
            element.pop("faces")

        cubes = file_contents.pop("elements")

    # We only return the cubes as it will be part of a custom bone in the armor_stand geo
    return cubes


def add_uv_textures():
    armor_stand_texture = Image.new('RGBA', (0, 16), color='white')
    for texture in textures_list:
        image = Image.open(textures_directory + "/" + texture + ".png")
        enlarged_image = Image.new(
            'RGBA', (armor_stand_texture.size[0]+16, armor_stand_texture.size[1]))
        enlarged_image.paste(armor_stand_texture)
        enlarged_image.paste(image, (armor_stand_texture.size[0], 0))
        armor_stand_texture = enlarged_image
    armor_stand_texture.putalpha(180)
    armor_stand_texture.save("pack/textures/entity/structura.png")


class NoModelException(Exception):
    pass


class MultipartException(Exception):
    pass
