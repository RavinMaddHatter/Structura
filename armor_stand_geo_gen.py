import json


def generate_geometry(block_matrix, excluded_blocks, texture_width):
    bones = []
    bones.append({"name": "ghost_blocks", "pivot": [-8, 0, -8]})
    # We generate the layer bones
    for y in range(len(block_matrix[0])):
        layer_name = "layer_" + str(y)
        bones.append(
            {"name": layer_name, "pivot": [-8, 0, -8], "parent": "ghost_blocks"})

    # We append each cube
    for x in range(len(block_matrix)):
        for y in range(len(block_matrix[0])):
            for z in range(len(block_matrix[0][0])):
                if block_matrix[x][y][z] != None and block_matrix[x][y][z].be_id not in excluded_blocks:
                    block_name = "block_" + \
                        str(x) + "_" + str(y) + "_" + str(z)
                    parent_name = "layer_" + str(y)
                    cubes = block_matrix[x][y][z].cubes
                    pivot = [-16*x, 8 + 16*y, 16*z]
                    rotation = block_matrix[x][y][z].rotation
                    if cubes != None and cubes != []:
                        for cube in cubes:
                            #We reset the rotation and reaply it later to not deal with inverted axis while moving the cube
                            [x_rot_cube, y_rot_cube, z_rot_cube] = cube["rotation"]
                            cube["rotation"] = [0, 0, 0]
                            cube["origin"][0] = cube["origin"][0] - 16*x
                            cube["origin"][1] = cube["origin"][1] + 16*y
                            cube["origin"][2] = cube["origin"][2] + 16*z
                            cube["rotation"] = [x_rot_cube, y_rot_cube, z_rot_cube]
                        cube["inflate"] = -0.03
                            
                        bones.append({"name": block_name, "parent": parent_name,
                                    "pivot": pivot, "rotation": rotation, "cubes": cubes})
                        
    
    geometry = json.loads("""
{
    "format_version": "1.16.0",
    "minecraft:geometry": [
        {
            "description": {
                "identifier": "geometry.armor_stand.structura",
                "texture_width": 1,
                "texture_height": 16,
                "visible_bounds_offset": [0.0, 1.5, 0.0],
                "visible_bounds_width": 5120,
                "visible_bounds_height": 5120
            }
        }
    ]
}
""")

    geometry["minecraft:geometry"][0]["bones"] = bones
    geometry["minecraft:geometry"][0]["description"]["texture_width"] = texture_width

    return geometry
