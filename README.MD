# Structura

This tool is inspired by Litematica. It is a tool that generates Resource packs from .mcstructure files. In this resource pack the armor stands were modified to render when off screen, and have all the blocks from your structure file as bones in their model. Thes "ghost blocks" are used to show the user where to place the real blocks. 


## Structura Rewrite

This is an attempt to use Java Blockstates and Models to render the ghost blocks to provide more accuracy on their shape without needing to define each model by hand.

## Notes 

It is an alpha version. It does not contain support for all the features right now available on **Structura**.<br/>
It does not have ane executable yet<br/>
Pipeline (not in order):<br/>
-All Vanilla blocks support<br/>
-Support for all features available right now on Structura<br/>
--Layered animations<br/>
--Multiple structures in one pack (by renaming armor_stand)<br/>
--Transparency changer<br/>
--Offsets<br/>
-Make app into a web<br/>
-Support for custom blocks from addons(?)<br/>
-Optimize app speed<br/>

## How to use

First you need to have installed Python 3.9.x on your device<br/>
Open Terminal in the Structura Rewrite folder and run the following command to install the needed modules:<br/>
`pip install pillow nbtlib numpy`<br/>
Once that is completed the app is ready to use<br/>

To use it run the next command:<br/>
`structura.py <path_to_mcstructure_file> <pack_name>`<br/>
and it will generate an .mcpack with the structure on it.<br/>
