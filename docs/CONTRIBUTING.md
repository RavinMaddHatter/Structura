#Contributing
Thank you for being intersed in contributing, strucutra is a program uses several ways and there is a few things you should understand before Contributing. 
##Usecases

###Desktop application
Structura was orginally only a desktop application, this comes with some bagage and some down sides. But support for using it with the gui needs to remain in place. To make this easier, the application was pulled out of the gui and mostly lives in "structura_core.py" the structura.py file is just a wrapper/gui.
###Structura Discord bot/ Structura lab
As mobile users were unable to use the desktop application, structura core was made to allow me to make an API that doesnt rely on CLI. The Discord bot (maddhatters discord bot, not availible to the public) runs in AWS lambda. that means it is a read only file system. for that reason structura_core.py and all dependencies must not rely on writing files to any directory except tmp. Any pull request that break this cannot be merged.
####Structura CLI
The CLI was added by contributors that wanted to make their own web services. This is allowed. Structura is MIT licensed and anyone can do anything with structura. This CLI is kept in but not highly tested (unless someone wants to take that on.
##Blocks Definitions
Minecraft is a giant mess when it comes to naming, versioning, and block definitions. But becase structura dates back to 2020 and posted files still refference old block names, we need to be careful when updating blocks. In 2020 an effort was made to remove all hard coded block defintions. At this point, blocks are defined in 2 locations. Vanilla_Resource_pack, where the textures and texture locations are saved in a similar way to the default texture pack from minecraft, and in lookups, where all the block geometry and nbt is defined.
###Editing Vanilla_Resource_pack 
When adding new blocks, do not remove old block defintions. Due to the project mojang ran between 2020 and 2024 renaming all the blocks, old structures will be broken if the terrain_texture.json and blocks.json is simply copied from the new version. Instead the old and new terrain textures must be merged. This is a bit painful, but it is what it is.
###Adding geometry
In 2025 when Vibrant Visuals was added, the CPU cost of rendering a bone became 50-100x more expensive. For that reason, when making new geometries, we need to be respectful of cube count. excessive use of cubes will cause excessive lag.

#Recognition
In the beginning i added the first 2 people who contributed to the manifest.json of every pack. If you stick around and help more then a few months, i may choose to do that in the future. If you fix things you will get credit in the release notes and likely in a video covering that release.
