# How to edit blocks for Structura
This page covers the process of editing a block to add support. This is broken into sections of adding support for rotation, changing the shape of a of a block, editing the textures for the block. This was added in Structura 1.3.
## find the block common name
Blocks that contain the same type but different names are linked in the file lookups/block_definitions.json. This allows several blocks to use the same type of rotations, block shape, and texture layout. These are strings, the entry name is as minecraft calls it internally, the value is a string that can be wahtever the writer wants it to be. however this needs to match exactly the entries in the other files.

## block roations 
The most common edit required is the rotation definition. The block rotation is contained in lookups/block_rotation.json. To support a common group of blocks you add an entry to the block_rotations.json matching the common name from the block_defintions.json. This entry must contain a dictionary with a key for each rotation state. All keys are strings in this document. The rotation states must contain a list of 3 numbers that denote the rotations around the X, Y, Z respectively.
### Example:
```json
"repeater": {
        "0": [0,180,0],
        "1": [0,-90,0],
        "2": [0,0,0],
        "3": [0,90,0]
    },
```
## Block Shapes
The second most frequently edited item is the lookups/block_shapes.json. This file defines the physical dimientions of the block as well as where it is located internally if needed. Again this is based upon "Common names" to prevent duplicated code. Common names can be looked up in the block_definitions.json file. each common name contains a dictionary, where each entry is a block state if needed, and each block state is a dictionary of sizes, and block centers. The block center is where the rotation is applied from the rotations function.
### Block states
 Block additions are supported in the python code. This needs to be moved out to become data drive, however this work has not been comlpleted yet.

Each block state must have a dictionary containting a size entry and a center entry. it may also contain an "offsets" entry
### size
Each size entry must be an array of arrays, Each sub array must contain 3 number representing the X, Y, Z dimentions of the compoent in question. The units are in percentage of full blocks, Each size entry must have at least 1 set of dimentions, but may optionally have many more cubes as the maker desires.
### Center
Each block state must contain 1 center definition, this is a array of 3 numbers. these number define where in the X, Y, Z that the rotation will be applied.
### Offsets (optional)
Each offset entry must be an array of arrays, each sub array must have 3 numbers to repersent an X, Y, Z offset in precentage of a full block. There must be 1 entry here for each size in the size entry
### Example
```json
"repeater":{"default":{
				"size":[[1,0.125,1],[0.1875,0.4375,0.1875],[0.1875,0.4375,0.1875]],"offsets":[[0,0,0],[0.4125,0,0.7125],[0.4125,0,0.4875]],"center":[0.5,0.5,0.5]},
				"0":{"size":[[1,0.125,1],[0.1875,0.4375,0.1875],[0.1875,0.4375,0.1875]],"offsets":[[0,0,0],[0.4125,0,0.7125],[0.4125,0,0.4875]],"center":[0.5,0.5,0.5]},
				"1":{"size":[[1,0.125,1],[0.1875,0.4375,0.1875],[0.1875,0.4375,0.1875]],"offsets":[[0,0,0],[0.4125,0,0.7125],[0.4125,0,0.375]],"center":[0.5,0.5,0.5]},
				"2":{"size":[[1,0.125,1],[0.1875,0.4375,0.1875],[0.1875,0.4375,0.1875]],"offsets":[[0,0,0],[0.4125,0,0.7125],[0.4125,0,0.25]],"center":[0.5,0.5,0.5]},
				"3":{"size":[[1,0.125,1],[0.1875,0.4375,0.1875],[0.1875,0.4375,0.1875]],"offsets":[[0,0,0],[0.4125,0,0.7125],[0.4125,0,0.125]],"center":[0.5,0.5,0.5]}},
```
## Block UV definitions
For a small portion of blocks the UV defintions must be changed. To do this you must change the common name entry in lookups/block_uv.json. Like the shape file, this is a dictionary of block states. if there is not a block state to represent the one in the file a default blcok state is chosen.
### block states 
 Block additions are supported in the python code. This needs to be moved out to become data drive, however this work has not been comlpleted yet.

Each block state must have a dictionary containting a uv_sizes entry and a offset entry. it may also contain an "overwrite" entry.
### uv_sizes
UV sizes must contain 6 entries, one for each directions ("up", "down", "north", "south", "east", "west"). These must contain a UV for each shape defined in the size in the block_shapes.json. Each direction must contain an array of arrays. The sub array needs to have 2 numbers, the size in the X, and Y. The size is the percentage of the texture size. 
### offset
Offset must contain 6 entries, one for each directions ("up", "down", "north", "south", "east", "west"). These must contain a Offset for each shape defined in the size in the block_shapes.json. Each direction must contain an array of arrays. The sub array needs to have 2 numbers, the Offset in the X, and Y. The Offset is the percentage of the texture size. Offsets start in the upper left hand corner.
## overwrite (optional)
If you need to select the texture directly, this is the mechanism for that. overwrite must contain 6 entries, one for each directions ("up", "down", "north", "south", "east", "west"). These must contain a overwrite for each shape defined in the size in the block_shapes.json. Each direction must contain an array. The  array needs to have a string for each texture. Default can be used if you want it to use the default for 1 or more of the sides.
