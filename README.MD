# Structura

This tool is inspired by Litematica. It is a tool that generates Resource packs from .mcstructure files. In this resource pack the armor stands were modified to render when off screen, and have all the blocks from your structure file as bones in their model. Thes "ghost blocks" are used to show the user where to place the real blocks. 


## Structura Rewrite

This is an attempt to use Java Blockstates and Models to render the ghost blocks to provide more accuracy on their shape without needing to define each model by hand.

## Notes 

It is an alpha version. It does not contain support for all the features right now available on **Structura**.
It does not have ane executable yet
Pipeline (not in order):
-All Vanilla blocks support
-Support for all features available right now on Structura
--Layered animations
--Multiple structures in one pack (by renaming armor_stand)
--Transparency changer
--Offsets
-Make app into a web
-Support for custom blocks from addons(?)
-Optimize app speed

## How to use

First you need to have installed Python 3.9.x on your device
Open Terminal in the Structura Rewrite folder and run the following command to install the needed modules
`pip install pillow nbtlib numpy`
Once that is completed the app is ready to use

To use it run the next command
`structura.py <path_to_mcstructure_file> <pack_name>`
and it will generate an .mcpack with the structure on it
