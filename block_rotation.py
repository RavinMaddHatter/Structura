import json

blocks = {}
blocks["observer"] = {}
blocks["observer"]["0"] = [90, 0, 0]
blocks["observer"]["1"] = [270, 0, 0]
blocks["observer"]["2"] = [0, 0, 0]
blocks["observer"]["3"] = [0, 180, 0]
blocks["observer"]["4"] = [0, 270, 0]
blocks["observer"]["5"] = [0, 90, 0]
blocks["dispenser"] = {}
blocks["dispenser"]["0"] = [270, 0, 0]
blocks["dispenser"]["1"] = [90, 0, 0]
blocks["dispenser"]["2"] = [0, 180, 0]
blocks["dispenser"]["3"] = [0, 0, 0]
blocks["dispenser"]["4"] = [0, 90, 0]
blocks["dispenser"]["5"] = [0, 270, 0]
blocks["dropper"] = {}
blocks["dropper"]["0"] = [270, 0, 0]
blocks["dropper"]["1"] = [90, 0, 0]
blocks["dropper"]["2"] = [0, 180, 0]
blocks["dropper"]["3"] = [0, 0, 0]
blocks["dropper"]["4"] = [0, 90, 0]
blocks["dropper"]["5"] = [0, 270, 0]
blocks["sticky_piston"] = {}
blocks["sticky_piston"]["0"] = [180, 0, 0]
blocks["sticky_piston"]["1"] = [0, 0, 0]
blocks["sticky_piston"]["2"] = [-90, 0, 0]
blocks["sticky_piston"]["3"] = [90, 0, 0]
blocks["sticky_piston"]["4"] = [0, 0, -90]
blocks["sticky_piston"]["5"] = [0, 0, 90]
blocks["furnace"] = {}
blocks["furnace"]["0"] = [180, 0, 0]
blocks["furnace"]["1"] = [0, 0, 0]
blocks["furnace"]["2"] = [0, 180, 0]
blocks["furnace"]["3"] = [0, 0, 0]
blocks["furnace"]["4"] = [0, 90, 0]
blocks["furnace"]["5"] = [0, -90, 0]

blocks["unpowered_repeater"] = {}
blocks["unpowered_repeater"]["0"] = [0, 180, 0]
blocks["unpowered_repeater"]["1"] = [0, -90, 0]
blocks["unpowered_repeater"]["2"] = [0, 0, 0]
blocks["unpowered_repeater"]["3"] = [0, 90, 0]

blocks["blast_furnace"] = blocks["furnace"]
blocks["piston"] = blocks["sticky_piston"]
blocks["smoker"] = blocks["furnace"]
blocks["unpowered_comparator"] = blocks["unpowered_repeater"]
blocks["powered_repeater"] = blocks["unpowered_repeater"]
blocks["powered_comparator"] = blocks["unpowered_repeater"]


with open("block_roation.json", "w+") as json_file:
    json.dump(blocks, json_file, indent=2)
