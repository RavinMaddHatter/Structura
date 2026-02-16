import os
import argparse
import sys
import updater
import json
import lang_parse

from numpy import array, int32, minimum
import nbtlib
from tkinter import (
    filedialog,
    messagebox,
    OptionMenu,
    Scale,
    DoubleVar,
    HORIZONTAL,
    IntVar,
    Listbox,
    ANCHOR,
    StringVar,
    Button,
    Label,
    Entry,
    Tk,
    Checkbutton,
    END,
    ACTIVE,
)

from structura_core import structura

structura_update_version = "Structura1-7"

if not(os.path.exists("lookups")):
    print("getting files")
    updater.update("https://update.structuralab.com/structuraUpdate",structura_update_version,"")
settings={"lang":"English"}
if os.path.exists("settings.json"):
    with open("settings.json") as file:
        settings = json.load(file)
else:
    with open("settings.json","w+") as file:
        json.dump(settings,file)
langs = lang_parse.parse()
lang = langs[settings["lang"]]

# CLI Args
parser = argparse.ArgumentParser(description="Structura app that generates Resource packs from .mcstructure files.")
parser.add_argument("--structure", type=str, help=".mcstructure file")
parser.add_argument("--pack_name", type=str, help="Name of pack")
parser.add_argument("--opacity", type=int, help="Opacity of blocks")
parser.add_argument("--icon", type=str, help="Icon for pack")
parser.add_argument("--offset", type=str, help="X, Y, X")
parser.add_argument("--overwrite", type=bool, help="Overwrite the output file.")
parser.add_argument("--debug", "-db", action='store_true', help='Enable debug mode')
parser.add_argument("--update", action='store_true', help='Run updater')
args = parser.parse_args()

def browseStruct():
    #browse for a structure file.
    FileGUI.set(filedialog.askopenfilename(filetypes=(
        ("Structure File", "*.mcstructure *.MCSTRUCTURE"), )))
def browseIcon():
    #browse for a structure file.
    icon_var.set(filedialog.askopenfilename(filetypes=(
        ("Icon File", "*.png *.PNG"), )))
def update():
    with open(r"lookups\lookup_version.json") as file:
        version_data = json.load(file)
    updated = updater.update(version_data["update_url"],structura_update_version,version_data["version"])
    if updated:
        with open(r"lookups\lookup_version.json") as file:
            version_data = json.load(file)
        messagebox.showinfo("Updated!", version_data["notes"])
    else:
        messagebox.showinfo("Status", "You are currently up to date.")

if args.update:
    update()

def box_checked():
    r = 0
    title_text.grid(row=r, column=0, columnspan=2)
    updateButton.grid(row=r, column=2)
    if check_var.get()==0:
        modle_name_entry.grid_forget()
        modle_name_lb.grid_forget()
        deleteButton.grid_forget()
        cord_lb_big.grid_forget()
        listbox.grid_forget()
        saveButton.grid_forget()
        modelButton.grid_forget()
        cord_lb.grid_forget()
        r +=1
        file_lb.grid(row=r, column=0)
        file_entry.grid(row=r, column=1)
        packButton.grid(row=r, column=2)
        r += 1
        icon_lb.grid(row=r, column=0)
        icon_entry.grid(row=r, column=1)
        IconButton.grid(row=r, column=2)
        r += 1

        packName_lb.grid(row=r, column=0)
        packName_entry.grid(row=r, column=1)
        r += 1
        cord_lb.grid_forget()
        x_entry.grid_forget()
        y_entry.grid_forget()
        z_entry.grid_forget()
        big_build_check.grid_forget()
        transparency_lb.grid_forget()
        transparency_entry.grid_forget()
        get_cords_button.grid_forget()
        advanced_check.grid(row=r, column=0)
        export_check.grid(row=r, column=1)
        saveButton.grid(row=r, column=2)
        
    else:
        saveButton.grid_forget()
        get_cords_button.grid_forget()
        cord_lb.grid_forget()
        cord_lb_big.grid_forget()
        modle_name_entry.grid_forget()
        modle_name_lb.grid_forget()
        modelButton.grid_forget()
        r +=1 
        file_lb.grid(row=r, column=0)
        file_entry.grid(row=r, column=1)
        packButton.grid(row=r, column=2)
        r += 1
        icon_lb.grid(row=r, column=0)
        icon_entry.grid(row=r, column=1)
        IconButton.grid(row=r, column=2)
        r += 1
        packName_lb.grid(row=r, column=0)
        packName_entry.grid(row=r, column=1)
        r += 1
        if big_build.get()==0:
            
            modle_name_entry.grid(row=r, column=1)
            modle_name_lb.grid(row=r, column=0)
        else:
            get_cords_button.grid(row=r, column=0,columnspan=2)
        modelButton.grid(row=r, column=2)
        r += 1
        offsetLbLoc=r
        if big_build.get()==0:
            cord_lb.grid(row=r, column=0,columnspan=3)
        else:
            cord_lb_big.grid(row=r, column=0,columnspan=3)
        r += 1
        x_entry.grid(row=r, column=0)
        y_entry.grid(row=r, column=1)
        z_entry.grid(row=r, column=2)
        r += 1
        transparency_lb.grid(row=r, column=0)
        transparency_entry.grid(row=r, column=1,columnspan=2)
        r += 1
        listbox.grid(row=r,column=1, rowspan=3)
        deleteButton.grid(row=r,column=2)
        r += 4
        advanced_check.grid(row=r, column=0)
        export_check.grid(row=r, column=1)
        saveButton.grid(row=r, column=2)
        r +=1
        big_build_check.grid(row=r, column=0,columnspan=2)   
def add_model():
    valid=True
    if big_build.get()==1:
        model_name_var.set(os.path.basename(FileGUI.get()))

    if len(FileGUI.get()) == 0:
        valid=False
        messagebox.showinfo(lang["Error"], lang["browse file"])
    if model_name_var.get() in list(models.keys()):
        messagebox.showinfo(lang["Error"], lang["unique tag"])
        valid=False

    if valid:
        name_tag=model_name_var.get()
        opacity=(100-sliderVar.get())/100
        models[name_tag] = {}
        models[name_tag]["offsets"] = [xvar.get(),yvar.get(),zvar.get()]
        models[name_tag]["opacity"] = opacity
        models[name_tag]["structure"] = FileGUI.get()
        listbox.insert(END,model_name_var.get())
            
def get_global_cords():
    mins = array([2147483647,2147483647,2147483647],dtype=int32)
    for name in models.keys():
        file = models[name]["structure"]
        struct = {}
        struct["nbt"] = nbtlib.load(file, byteorder='little')
        if "" in struct["nbt"].keys():
            struct["nbt"] = struct["nbt"][""]
        struct["mins"] = array(list(map(int,struct["nbt"]["structure_world_origin"])))
        mins = minimum(mins, struct["mins"])
        xvar.set(mins[0])
        yvar.set(mins[1])
        zvar.set(mins[2])

        
def delete_model():
    items = listbox.curselection()
    if len(items)>0:
        models.pop(listbox.get(ACTIVE))
    listbox.delete(ANCHOR)

def runFromGui():
    ##wrapper for a gui.
    global models, offsets
    stop = False
    if os.path.isfile("{}.mcpack".format(packName.get())):
        stop = True
        messagebox.showinfo(lang["Error"], lang["pack name error"])
        ## could be fixed if temp files were used.
    if check_var.get()==0:
        if len(FileGUI.get()) == 0:
            stop = True
            messagebox.showinfo(lang["Error"], lang["unique tag"])
    if len(packName.get()) == 0:
        stop = True
        messagebox.showinfo(lang["Error"], lang["no pack name"])
    else:
        if len(list(models.keys()))==0 and check_var.get():
            stop = True
            messagebox.showinfo(lang["Error"], lang["no structure files"])

    if not stop:
        structura_base=structura(packName.get())
        structura_base.set_opacity(sliderVar.get())
        if len(icon_var.get())>0:
            structura_base.set_icon(icon_var.get())

        
        if not(check_var.get()):
            structura_base.add_model("",FileGUI.get())
            offset=[xvar.get(),yvar.get(),zvar.get()]
            structura_base.set_model_offset("",offset)
            structura_base.generate_with_nametags()
            if (export_list.get()==1):
                structura_base.make_nametag_block_lists()
            structura_base.compile_pack()
        elif big_build.get():
            for name_tag in models.keys():
                structura_base.add_model(name_tag,models[name_tag]["structure"])
            structura_base.make_big_model([xvar.get(),yvar.get(),zvar.get()])
            if (export_list.get()==1):
                structura_base.make_big_blocklist()
            structura_base.compile_pack()
        else:
            for name_tag in models.keys():
                structura_base.add_model(name_tag,models[name_tag]["structure"])
                structura_base.set_model_offset(name_tag,models[name_tag]["offsets"].copy())
            structura_base.generate_with_nametags()
            if (export_list.get()==1):
                structura_base.make_nametag_block_lists()
            structura_base.generate_nametag_file()
            structura_base.compile_pack()

# Command Line interface
if args.structure and args.pack_name:

    opacity = args.opacity or 20
    offset = [0, 0, 0]
    if args.offset:
        offset = [int(val) for val in args.offset.split(",")]

    pack_file = "{}.mcpack".format(args.pack_name)
    if args.overwrite and os.path.isfile(pack_file):
        os.remove(pack_file)

    structura_base = structura(args.pack_name)
    structura_base.set_opacity(opacity)

    if icon := args.icon:
        structura_base.set_icon(icon)

    structura_base.add_model("", args.structure)
    structura_base.set_model_offset("", offset)
    structura_base.generate_with_nametags()
    structura_base.compile_pack()


    # Exit Script
    sys.exit(0)

offsetLbLoc=4
offsets={}
root = Tk()
root.title(structura_update_version)
models={}
FileGUI = StringVar()
packName = StringVar()
icon_var = StringVar()
icon_var.set("lookups/pack_icon.png")
sliderVar = DoubleVar()
model_name_var = StringVar()
xvar = DoubleVar()
xvar.set(0)
yvar = DoubleVar()
zvar = DoubleVar()
zvar.set(0)
check_var = IntVar()
export_list = IntVar()
big_build = IntVar()
big_build.set(0)
sliderVar.set(20)
listbox=Listbox(root)
title_text = Label(root, text=lang["title"])
file_entry = Entry(root, textvariable=FileGUI)
packName_entry = Entry(root, textvariable=packName)
modle_name_lb = Label(root, text=lang["name tag"])
modle_name_entry = Entry(root, textvariable=model_name_var)
cord_lb = Label(root, text=lang["offset"])
cord_lb_big = Label(root, text=lang["corner"])
x_entry = Entry(root, textvariable=xvar, width=5)
y_entry = Entry(root, textvariable=yvar, width=5)
z_entry = Entry(root, textvariable=zvar, width=5)
icon_lb = Label(root, text=lang["icon"])
icon_entry = Entry(root, textvariable=icon_var)
updateButton = Button(root, text=lang["update"], command=update)
IconButton = Button(root, text=lang["browse"], command=browseIcon)
file_lb = Label(root, text=lang["structurefile"])
packName_lb = Label(root, text=lang["packname"])
packButton = Button(root, text=lang["browse"], command=browseStruct)
advanced_check = Checkbutton(root, text=lang["advance"], variable=check_var, onvalue=1, offvalue=0, command=box_checked)
export_check = Checkbutton(root, text=lang["lists"], variable=export_list, onvalue=1, offvalue=0)
big_build_check = Checkbutton(root, text=lang["bigbuild"], variable=big_build, onvalue=1, offvalue=0, command=box_checked )

deleteButton = Button(root, text=lang["remove"], command=delete_model)
saveButton = Button(root, text=lang["makepack"], command=runFromGui)
modelButton = Button(root, text=lang["addmodel"], command=add_model)
get_cords_button = Button(root, text=lang["getcords"], command=get_global_cords)
transparency_lb = Label(root, text=lang["transparency"])
transparency_entry = Scale(root,variable=sliderVar, length=200, from_=0, to=100,tickinterval=10,orient=HORIZONTAL)

box_checked()

root.resizable(0,0)
root.mainloop()
root.quit()

