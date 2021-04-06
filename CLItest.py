import structura
import os
models={"":"test structures/test partial blocks 1.mcstructure"}
offsets={"":[0,0,0]}
if os.path.isfile("{}.mcpack".format("testMe")):
    os.remove("testMe.mcpack")
structura.generate_pack("testMe",50,1,models,offsets)
