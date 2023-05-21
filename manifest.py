import json
import os
import uuid


def export(pack_name):
    manifest = {
        "format_version": 2,
        "header": {
            "name": pack_name.replace("/tmp/",""),
            "description": "Structura block overlay pack, created by  \u00a7o\u00a75DrAv0011\u00a7r, \u00a7o\u00a79 FondUnicycle\u00a7r and\u00a7o\u00a75 RavinMaddHatter\u00a7r",
            "uuid": str(uuid.uuid4()),
            "version": [
                0,
                0,
                1
            ],
            "min_engine_version": [
                1,
                16,
                0
            ]
        },
        "modules": [
            {
                "type": "resources",
                "uuid": str(uuid.uuid4()),
                        "version": [
                    0, 0, 1]}]}


    path_to_ani = "{}/manifest.json".format(pack_name)
    os.makedirs(os.path.dirname(path_to_ani), exist_ok=True)

    with open(path_to_ani, "w+") as json_file:
        json.dump(manifest, json_file, indent=2)
