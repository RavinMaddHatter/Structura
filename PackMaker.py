import armor_stand_class
import structure_reader
from tkinter import StringVar, Button,Label,Entry,Tk
from tkinter import filedialog




def generate_pack(struct_name,pack_name):
    struct2make=structure_reader.process_structure(struct_name)
    armorstand=armor_stand_class.armorstand()
    [xlen,ylen,zlen]=struct2make.get_size()
    for y in range(ylen):
        armorstand.make_layer(y)
        for x in range(xlen):
            for z in range(zlen):
                block=struct2make.get_block(x,y,z)
                armorstand.make_block(x,y,z,block["name"].replace("minecraft:",""))

    armorstand.export(pack_name)

def runFromGui():
    FileGUI
    generate_pack(FileGUI.get(),packName.get())
def browseStruct():
    FileGUI.set(filedialog.askopenfilename(filetypes = (("Structure File", "*.mcstructure *.MCSTRUCTURE"), )))



root = Tk()
root.title("Bedrock Litematica Maker")


FileGUI=StringVar()
packName=StringVar()
file_entry = Entry(root,textvariable=FileGUI)
packName_entry = Entry(root,textvariable=packName)
file_lb=Label(root, text="Structure file")
packName_lb=Label(root, text="Pack Name")
packButton=Button(root,text="Browse",command=browseStruct)

saveButton=Button(root,text="Make Pack",command=runFromGui)
r=0
file_lb.grid(row=r,column=0)
file_entry.grid(row=r,column=1)
packButton.grid(row=r,column=2)
r+=1
packName_lb.grid(row=r,column=0)
packName_entry.grid(row=r,column=1)
r+=1
saveButton.grid(row=r,column=2)


root.mainloop() 
