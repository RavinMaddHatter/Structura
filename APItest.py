from structura_core import structura
import os
files_to_conver={
        
        "gems":{"file":"test_structures/All Blocks World/gems and redstone.mcstructure",
                "offset":[0,0,0]},
        "stone":{"file":"test_structures/All Blocks World/Stones.mcstructure",
                 "offset":[0,0,0]},
        "wood":{"file":"test_structures/All Blocks World/wood.mcstructure",
                "offset":[0,0,0]},
        "decor":{"file":"test_structures/All Blocks World/decorative.mcstructure",
                 "offset":[0,0,0]}}

structura_base=structura("tmp/all_blocks")
structura_base.set_opacity(20)
for name_tag, info in files_to_conver.items():
    print(f'{name_tag}, {info}')
    
    structura_base.add_model(name_tag,info["file"])
    structura_base.set_model_offset(name_tag,info["offset"])
structura_base.generate_nametag_file()
structura_base.generate_with_nametags()
structura_base.compile_pack()
