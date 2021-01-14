import armor_stand_class
import structure_reader
import animation_class
from tkinter import StringVar, Button, Label, Entry, Tk
from tkinter import filedialog
import manifest
from shutil import copyfile
import os
from zipfile import ZipFile
import glob


def generate_pack(struct_name, pack_name):
    manifest.export(pack_name)
    struct2make = structure_reader.process_structure(struct_name)
    armorstand = armor_stand_class.armorstand()
    animation = animation_class.animations()
    [xlen, ylen, zlen] = struct2make.get_size()
    for y in range(ylen):
        armorstand.make_layer(y)
        animation.insert_layer(y)
        for x in range(xlen):
            for z in range(zlen):
                block = struct2make.get_block(x, y, z)
                rot = None
                top = False
                if "facing_direction" in block["states"].keys():
                    rot = block["states"]["facing_direction"]

                if "direction" in block["states"].keys():
                    rot = block["states"]["direction"]
                if "top_slot_bit" in block["states"].keys():
                    top = bool(block["states"]["top_slot_bit"])
                    print(top)

                armorstand.make_block(x, y, z, block["name"].replace(
                    "minecraft:", ""), rot=rot, top=top)

    armorstand.export(pack_name)
    animation.export(pack_name)
    copyfile("pack_icon.png", "{}/pack_icon.png".format(pack_name))
    os.makedirs(os.path.dirname(
        "{}/entity/armor_stand.entity.json".format(pack_name)), exist_ok=True)
    copyfile("armor_stand.entity.json",
             "{}/entity/armor_stand.entity.json".format(pack_name))

    # Adds to zip file a modified armor stand geometry to enlarge the render area of the entity
    larger_render = "armor_stand.larger_render.geo.json"
    larger_render_path = "{}/models/entity/{}".format(pack_name, larger_render)
    copyfile(larger_render, larger_render_path)

    rc = "armor_stand.ghost_blocks.render_controllers.json"
    rcpath = "{}/render_controllers/{}".format(pack_name, rc)
    os.makedirs(os.path.dirname(rcpath))
    copyfile(rc, rcpath)
    file_paths = []
    for directory, _, _ in os.walk(pack_name):
        file_paths.extend(glob.glob(os.path.join(directory, "*.*")))
    with ZipFile("{}.mcpack".format(pack_name), 'x') as zip:
        # writing each file one by one
        for file in file_paths:
            print(file)
            zip.write(file)


def runFromGui():
    FileGUI
    generate_pack(FileGUI.get(), packName.get())


def browseStruct():
    FileGUI.set(filedialog.askopenfilename(filetypes=(
        ("Structure File", "*.mcstructure *.MCSTRUCTURE"), )))


root = Tk()
root.title("Bedrock Litematica Maker")


FileGUI = StringVar()
packName = StringVar()
file_entry = Entry(root, textvariable=FileGUI)
packName_entry = Entry(root, textvariable=packName)
file_lb = Label(root, text="Structure file")
packName_lb = Label(root, text="Pack Name")
packButton = Button(root, text="Browse", command=browseStruct)

saveButton = Button(root, text="Make Pack", command=runFromGui)
r = 0
file_lb.grid(row=r, column=0)
file_entry.grid(row=r, column=1)
packButton.grid(row=r, column=2)
r += 1
packName_lb.grid(row=r, column=0)
packName_entry.grid(row=r, column=1)
r += 1
saveButton.grid(row=r, column=2)


root.mainloop()
