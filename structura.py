import structure_reader
import model_handler
import armor_stand_geo_gen
import sys
import json
import shutil
import os
import uuid


def main():
    args = sys.argv[1:]

    structure_file = args[0]
    pack_name = args[1]

    # Excluded blocks should use bedrock id's not java ones
    excluded_blocks = ["minecraft:air",
                       "minecraft:structure_block", "minecraft:barrier"]

    print("Reading Structure")
    structure = structure_reader.StructureReader(
        structure_file, excluded_blocks)
    print("Generating block models")
    model_handler.asign_model(structure.matrix)
    print("Generating textures")
    model_handler.add_uv_textures()
    print("Writing Structura geometry")
    armor_geo = armor_stand_geo_gen.generate_geometry(
        structure.matrix, excluded_blocks, len(model_handler.textures_list) * 16)

    print("Saving geo")
    file = open("pack/models/entity/structura.geo.json", 'w+')
    file.write(json.dumps(armor_geo))
    file.close()

    print("Generating Manifest")
    manifest_file = open("utilities/manifest.json", 'r')
    manifest = manifest_file.read()
    manifest_file.close()

    manifest = manifest.replace("#pack_name", pack_name)
    manifest = manifest.replace("#UUID1", str(uuid.uuid4()))
    manifest = manifest.replace("#UUID2", str(uuid.uuid4()))
    
    manifest_file = open("pack/manifest.json", 'w+')
    manifest_file.write(manifest)
    manifest_file.close()

    print("Generating pack")
    shutil.make_archive(pack_name, 'zip', "pack")
    # os.rename(pack_name+".zip", pack_name+".mcpack")


if __name__ == "__main__":
    main()
