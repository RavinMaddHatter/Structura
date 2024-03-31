import os
import updater
if not(os.path.exists("lookups")):
    print("downloading lookup files")
    updater.update("https://update.structuralab.com/structuraUpdate","Structura1-6","")
    
import json
from structura_core import structura
from turtle import color
from numpy import array, int32, minimum
import nbtlib

from tkinter import ttk,filedialog,messagebox
from tkinter import StringVar, Button, Label, Entry, Tk, Checkbutton, END, ACTIVE
from tkinter import filedialog, Scale,DoubleVar,HORIZONTAL,IntVar,Listbox, ANCHOR
debug = False


def browseStruct():
    #browse for a structure file.
    FileGUI.set(filedialog.askopenfilename(filetypes=(
        ("Structure File", "*.mcstructure *.MCSTRUCTURE"), )))
def browseIcon():
    #browse for a structure file.
    icon_var.set(filedialog.askopenfilename(filetypes=(
        ("Icon File", "*.png *.PNG"), )))
def update():
    with open("lookups\lookup_version.json") as file:
        version_data = json.load(file)
        print(version_data["version"])
    updated = updater.update(version_data["update_url"],"Structura1-6",version_data["version"])
    if updated:
        with open("lookups\lookup_version.json") as file:
            version_data = json.load(file)
        messagebox.showinfo("Updated!", version_data["notes"])
    else:
        messagebox.showinfo("Status", "You are currently up to date.")
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
        messagebox.showinfo("Error", "You need to browse for a structure file!")
    if model_name_var.get() in list(models.keys()):
        messagebox.showinfo("Error", "The Name Tag mut be unique")
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
        messagebox.showinfo("Error", "pack already exists or pack name is empty")
        ## could be fixed if temp files were used.
    if check_var.get()==0:
        if len(FileGUI.get()) == 0:
            stop = True
            messagebox.showinfo("Error", "You need to browse for a structure file!")
    if len(packName.get()) == 0:
        stop = True
        messagebox.showinfo("Error", "You need a Name")
    else:
        if len(list(models.keys()))==0 and check_var.get():
            stop = True
            messagebox.showinfo("Error", "You need to add some structures")
    if len(icon_var.get())>0:
        pack_icon=icon_var.get()
    if not stop:
        
        structura_base=structura(packName.get())
        structura_base.set_opacity(sliderVar.get())
        if debug:
            print(models)
        
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

offsetLbLoc=4
offsets={}
root = Tk()
root.title("Structura")
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
title_text = Label(root, text="Structura")
file_entry = Entry(root, textvariable=FileGUI)
packName_entry = Entry(root, textvariable=packName)
modle_name_lb = Label(root, text="Name Tag")
modle_name_entry = Entry(root, textvariable=model_name_var)
cord_lb = Label(root, text="Offset")
cord_lb_big = Label(root, text="Corner")
x_entry = Entry(root, textvariable=xvar, width=5)
y_entry = Entry(root, textvariable=yvar, width=5)
z_entry = Entry(root, textvariable=zvar, width=5)
icon_lb = Label(root, text="Icon file")
icon_entry = Entry(root, textvariable=icon_var)
updateButton = Button(root, text="Update", command=update)
IconButton = Button(root, text="Browse", command=browseIcon)
file_lb = Label(root, text="Structure file")
packName_lb = Label(root, text="Pack Name")
if debug:
    debug_lb = Label(root, text="Debug Mode",fg='Red').place(x=285,y=70)
packButton = Button(root, text="Browse", command=browseStruct)
advanced_check = Checkbutton(root, text="advanced", variable=check_var, onvalue=1, offvalue=0, command=box_checked)
export_check = Checkbutton(root, text="make lists", variable=export_list, onvalue=1, offvalue=0)
big_build_check = Checkbutton(root, text="Big Build mode", variable=big_build, onvalue=1, offvalue=0, command=box_checked )

deleteButton = Button(root, text="Remove Model", command=delete_model)
saveButton = Button(root, text="Make Pack", command=runFromGui)
modelButton = Button(root, text="Add Model", command=add_model)
get_cords_button = Button(root, text="Get Global Cords", command=get_global_cords)
transparency_lb = Label(root, text="Transparency")
transparency_entry = Scale(root,variable=sliderVar, length=200, from_=0, to=100,tickinterval=10,orient=HORIZONTAL)

box_checked()

root.resizable(0,0)
root.mainloop()
root.quit()
