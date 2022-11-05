from turtle import color
import armor_stand_geo_class_2 as asgc
import armor_stand_class ,structure_reader ,animation_class ,manifest ,os ,glob ,json ,shutil ,updater
import render_controller_class as rcc
from shutil import copyfile
from zipfile import ZIP_DEFLATED, ZipFile

debug=True

with open("lookups/nbt_defs.json") as f:
    nbt_def = json.load(f)
class structura:
    def __init__(self,pack_name):
        self.pack_name=pack_name
        self.structure_files={}
        self.rc=rcc.render_controller()
        self.armorstand_entity = armor_stand_class.armorstand()
        visual_name=pack_name
        manifest.export(visual_name)
        self.animation = animation_class.animations()
        self.exclude_list=["minecraft:structure_block","minecraft:air"]
        self.opacity=0.8
        self.longestY=0
        self.unsupported_blocks=[]
        self.all_blocks={}
        self.icon="lookups/pack_icon.png"
    def set_icon(self,icon):
        self.icon=icon
    def set_opacity(self,opacity):
        self.opacity=opacity
    def add_model(self,name,file_name):
        self.structure_files[name]={}
        self.structure_files[name]["file"]=file_name
        self.structure_files[name]["offsets"]=None
    def set_model_offset(self,name,offset):
        self.structure_files[name]["offsets"]=offset
    def generate_nametag_file(self):
        ## temp folder would be a good idea
        name_tags=self.structure_files.keys()
        fileName="{} Nametags.txt".format(self.pack_name)
        with open(fileName,"w+") as text_file:
            text_file.write("These are the nametags used in this file\n")
            for name in name_tags:
                text_file.write("{}\n".format(name))
    def make_big_model(self):
        names= list(self.structure_files.keys())
        struct2make=structure_reader.combined_structures(names,exclude_list=self.exclude_list)
        self.rc.add_model("")
        self.armorstand_entity.add_model("")
        blocks=self._add_blocks_to_geo(struct2make,"")
        ## condier temp folder
        self.armorstand_entity.export(self.pack_name)
    def generate_with_nametags(self):
        update_animation=True
        for model_name in self.structure_files.keys():
            if self.structure_files[model_name]["offsets"] is None:
                offset=[0,0,0]
            else:
                offset=self.structure_files[model_name]["offsets"]
            self.rc.add_model(model_name)
            self.armorstand_entity.add_model(model_name)
            ## temp folder would be a good idea
            print(self.structure_files[model_name]["file"])
            copyfile(self.structure_files[model_name]["file"], "{}/{}.mcstructure".format(self.pack_name,model_name))
            if debug:
                print(self.structure_files[model_name]['offsets'])
            struct2make = structure_reader.process_structure(self.structure_files[model_name]["file"])
            
            blocks=self._add_blocks_to_geo(struct2make,model_name)
            self.structure_files[model_name]["block_list"]=blocks
            ##consider temp folder
            self.armorstand_entity.export(self.pack_name)## this may be in the wrong spot, but transfered from 1.5
    def make_nametag_block_lists(self):
        ## consider temp file
        for model_name in self.structure_files.keys():
            file_name="{}-{} block list.txt".format(visual_name,model_name)
            all_blocks=self.structure_files[model_name]["block_list"]
            with open(file_name,"w+") as text_file:
                text_file.write("This is a list of blocks, there is a known issue with variants, all variants are counted together\n")
                for name in all_blocks.keys():
                    commonName = name.replace("minecraft:","")
                    text_file.write("{}: {}\n".format(commonName,all_blocks[name]))
    def make_big_blocklist(self):
        ## consider temp file
        file_name="{} block list.txt".format(self.pack_name)
        with open(file_name,"w+") as text_file:
            text_file.write("This is a list of blocks, there is a known issue with variants, all variants are counted together\n")
            for name in self.all_blocks.keys():
                commonName = name.replace("minecraft:","")
                text_file.write("{}: {}\n".format(commonName,self.all_blocks[name]))
    def _add_blocks_to_geo(self,struct2make,model_name):
        armorstand = asgc.armorstandgeo(model_name,alpha = self.opacity, offsets=self.structure_files[model_name]['offsets'])
        [xlen, ylen, zlen] = struct2make.get_size()
        if ylen > self.longestY:
            update_animation=True
            longestY = ylen
        else:
            update_animation=False
        for y in range(ylen):
            if debug:
                print(range(ylen))
                print("layer "+str(y)+" of "+ str(ylen))
            #creates the layer for controlling. Note there is implied formating here
            #for layer names
            armorstand.make_layer(y)
            #adds links the layer name to an animation
            if update_animation:
                self.animation.insert_layer(y)
            for x in range(xlen):
                for z in range(zlen):
                    block = struct2make.get_block(x, y, z)
                    blk_name=block["name"].replace("minecraft:", "")
                    blockProp=self._process_block(block)
                    rot = blockProp[0]
                    top = blockProp[1]
                    variant = blockProp[2]
                    open_bit = blockProp[3]
                    data = blockProp[4]
                    skip = blockProp[5]
                    if debug:
                        #print(blk_name)
                        pass
                    if debug and False:
                        if not skip:
                            armorstand.make_block(x, y, z, blk_name, rot = rot, top = top,variant = variant, trap_open=open_bit, data=data)
                    else:
                        try:
                            if not skip:
                                armorstand.make_block(x, y, z, blk_name, rot = rot, top = top,variant = variant, trap_open=open_bit, data=data)
                        except:
                            self.unsupported_blocks.append("x:{} Y:{} Z:{}, Block:{}, Variant: {}".format(x,y,z,block["name"],variant))
                            print("There is an unsuported block in this world and it was skipped")
                            print("x:{} Y:{} Z:{}, Block:{}, Variant: {}".format(x,y,z,block["name"],variant))
            ## consider temp file
            armorstand.export(self.pack_name)
            self.animation.export(self.pack_name)
        return struct2make.get_block_list()
    def compile_pack(self):
        ## consider temp file
        copyfile(self.icon, "{}/pack_icon.png".format(self.pack_name))
        larger_render = "lookups/armor_stand.larger_render.geo.json"
        larger_render_path = "{}/models/entity/{}".format(self.pack_name, "armor_stand.larger_render.geo.json")
        copyfile(larger_render, larger_render_path)
        self.rc.export(self.pack_name)
        file_paths = []
        for directory,_,_ in os.walk(self.pack_name):
            file_paths.extend(glob.glob(os.path.join(directory, "*.*")))
        ## add all files to the mcpack file  
        with ZipFile("{}.mcpack".format(self.pack_name), 'x',ZIP_DEFLATED) as zip: ## add compression
            # writing each file one by one 

            for file in file_paths:
                print(file)
                zip.write(file)
        ## delete all the extra files.
        shutil.rmtree(self.pack_name)
        print("Pack Making Completed")
    def _process_block(self,block):
        rot = None
        top = False
        open_bit = False
        data=0
        skip=False
        variant="Default"

        for key in nbt_def.keys():
            if nbt_def[key]== "variant" and key in block["states"].keys():
                variant = [key,block["states"][key]]
            if nbt_def[key]== "rot" and key in block["states"].keys():
                try:
                    rot = int(block["states"][key])
                except:
                    rot = str(block["states"][key])
                
            if nbt_def[key]== "top" and key in block["states"].keys():
                top = bool(block["states"][key])
            if nbt_def[key]== "open_bit" and "open_bit" in block["states"].keys():
                open_bit = bool(block["states"][key])
            if nbt_def[key]== "data" and key in block["states"].keys():
                data = int(block["states"][key])

        if "wood_type" in block["states"].keys():
            variant = ["wood_type",block["states"]["wood_type"]]
            if block["name"] == "minecraft:wood":
                keys = block["states"]["wood_type"]
                if bool(block["states"]["stripped_bit"]):
                    keys+="_stripped"
                variant = ["wood",keys]
        #if debug:
        #    print([rot, top, variant, open_bit, data, skip])
        return [rot, top, variant, open_bit, data, skip]
if __name__=="__main__":
    ## this is all the gui stuff that is not needed if you are calling this as a CLI
    
    from tkinter import ttk,filedialog,messagebox
    from tkinter import StringVar, Button, Label, Entry, Tk, Checkbutton, END, ACTIVE
    from tkinter import filedialog, Scale,DoubleVar,HORIZONTAL,IntVar,Listbox, ANCHOR

    def browseStruct():
        #browse for a structure file.
        FileGUI.set(filedialog.askopenfilename(filetypes=(
            ("Structure File", "*.mcstructure *.MCSTRUCTURE"), )))
    def browseIcon():
        #browse for a structure file.
        icon_var.set(filedialog.askopenfilename(filetypes=(
            ("Icon File", "*.png *.PNG"), )))
    def box_checked():
        if check_var.get()==0:
            modle_name_entry.grid_forget()
            modle_name_lb.grid_forget()
            deleteButton.grid_forget()
            listbox.grid_forget()
            saveButton.grid_forget()
            modelButton.grid_forget()
            r = 0
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
            transparency_lb.grid_forget()
            transparency_entry.grid_forget()
            advanced_check.grid(row=r, column=0)
            export_check.grid(row=r, column=1)
            saveButton.grid(row=r, column=2)
            r +=1
            updateButton.grid(row=r, column=2)
        else:
            saveButton.grid_forget()
            r = 0
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
            modle_name_entry.grid(row=r, column=1)
            modle_name_lb.grid(row=r, column=0)
            modelButton.grid(row=r, column=2)
            r += 1
            cord_lb.grid(row=r, column=0,columnspan=3)
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
            updateButton.grid(row=r, column=2)
    def add_model():
        valid=True
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
            if len(list(models.keys()))==0:
                stop = True
                messagebox.showinfo("Error", "You need to add some strucutres")
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
                if (export_list.get()==1):
                    structura_base.generate_nametag_file()
                structura_base.generate_with_nametags()
                structura_base.compile_pack()
            else:
                for name_tag in models.keys():
                    structura_base.add_model(name_tag,models[name_tag]["structure"])
                    structura_base.set_model_offset(name_tag,models[name_tag]["offsets"])
                    structura_base.generate_with_nametags()
                    if (export_list.get()==1):
                        structura_base.generate_nametag_file()
                structura_base.compile_pack()
        

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
    sliderVar.set(20)
    listbox=Listbox(root)
    file_entry = Entry(root, textvariable=FileGUI)
    packName_entry = Entry(root, textvariable=packName)
    modle_name_lb = Label(root, text="Name Tag")
    modle_name_entry = Entry(root, textvariable=model_name_var)
    cord_lb = Label(root, text="offset")
    x_entry = Entry(root, textvariable=xvar, width=5)
    y_entry = Entry(root, textvariable=yvar, width=5)
    z_entry = Entry(root, textvariable=zvar, width=5)
    icon_lb = Label(root, text="Icon file")
    icon_entry = Entry(root, textvariable=icon_var)
    IconButton = Button(root, text="Browse", command=browseIcon)
    file_lb = Label(root, text="Structure file")
    packName_lb = Label(root, text="Pack Name")
    if debug:
        debug_lb = Label(root, text="Debug Mode",fg='Red').place(x=285,y=70)
    packButton = Button(root, text="Browse", command=browseStruct)
    advanced_check = Checkbutton(root, text="advanced", variable=check_var, onvalue=1, offvalue=0, command=box_checked)
    export_check = Checkbutton(root, text="make lists", variable=export_list, onvalue=1, offvalue=0)

    deleteButton = Button(root, text="Remove Model", command=delete_model)
    saveButton = Button(root, text="Make Pack", command=runFromGui)
    modelButton = Button(root, text="Add Model", command=add_model)

    updateButton = Button(root, text="Update Blocks", command=updater.getLatest)
    transparency_lb = Label(root, text="Transparency")
    transparency_entry = Scale(root,variable=sliderVar, length=200, from_=0, to=100,tickinterval=10,orient=HORIZONTAL)

    box_checked()

    root.resizable(0,0)
    root.mainloop()
    root.quit()
