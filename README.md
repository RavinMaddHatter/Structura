# Structura

This tool is inspired by Litematica. It is a tool that generates Resource packs from .mcstructure files. In this resource pack the armor stands were modified to render when off screen, and have all the blocks from your structure file as bones in their model. Thes "ghost blocks" are used to show the user where to place the real blocks. 


[![Intro to Structura video](https://img.youtube.com/vi/IdKT925LKMM/0.jpg)](https://www.youtube.com/watch?v=IdKT925LKMM)



## Generating an .mcstrucutre file

First you must get a structure block, as this is typically done from a creative copy with cheats enabled, simply execute /give @s structure_block to get a structure block 
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/give_structure.png?raw=true)
Next configure the structure using the GUI, selecte every block you wish to have in your armor stand. Note the larges size suported by a signel structure block is 64x64x64
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/select_structure.PNG?raw=true)
Next click the export button at the bottom to produce a save prompt, this will allow you to save the structure to a file. Name it whatever you want and not the location, you will need it later.
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/export_structure.PNG?raw=true)

## Converting a structure into a .mcpack file
First you will need to download the current release of Structura. Extract the zip file, and launch executable. once it is launched you should see something like the image below.
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/launch_structura.PNG?raw=true)
Next bows for your exported structure from earlier using browse button, or type the path in manually.
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/browse_file.PNG?raw=true)
Enter a name for you structura pack.
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/name.PNG?raw=true)
** if you mistakenly name two files the same it will show you the prompt below to rename it
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/already_exists.PNG?raw=true)
If everything worked you should now have an mcpack file 
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/pack_made.PNG?raw=true)

## Using the pack
This pack is like any texture pack. To use it you must make sure it is active, enabling it in your global resources works well.
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/make_pack_active.PNG?raw=true)
The structure will appear around every armor stand in the worlds you load. It is how we are able to make it work on any world. So get out an armor stand and place it down to see your structure.
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/example_full.png?raw=true)
You can go through a structure layer by layer if you like by shift right clicking on the stand. This will minimize all layers except the "active" ones. I cant add poses without adding a behavior pack so for large structures there will be mutiple layers displayed at a time (12 blocks apart)
![alt text](https://github.com/RavinMaddHatter/Structura/blob/main/docs/example_layer.png?raw=true)







