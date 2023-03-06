import structura_core  
import os
structura_core.debug=True
files_to_conver={
        
        "":{"file":"test_structures/BigHatter/1.mcstructure",
                "offset":[-32,0,-32]}}


if os.path.exists("tmp/speed.mcpack"):
    os.remove("tmp/speed.mcpack")
if os.path.exists("tmp/speed Nametags.txt"):
    os.remove("tmp/speed Nametags.txt")

structura_base=structura_core.structura("tmp/speed")
structura_base.set_opacity(20)
for name_tag, info in files_to_conver.items():
    print(f'{name_tag}, {info}')
    
    structura_base.add_model(name_tag,info["file"])
    structura_base.set_model_offset(name_tag,info["offset"])


structura_base.generate_nametag_file()
structura_base.generate_with_nametags()

structura_base.compile_pack()
print(structura_base.timers["total"])
for key, value in structura_base.timers.items():
    print(f"{key}-{value}")
