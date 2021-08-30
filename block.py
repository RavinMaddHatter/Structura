import json

# We use string which is going to be inside the block we want to avoid so we do not need to list all trapdoors for example
invalid_variants = {
    "triggered=false": ["any"],
    "triggered=true": ["any"],
    "distance=0": ["any"],
    "distance=1": ["any"],
    "distance=2": ["any"],
    "distance=3": ["any"],
    "distance=4": ["any"],
    "distance=5": ["any"],
    "distance=6": ["any"],
    "distance=7": ["any"],
    "persistent=true": ["any"],
    "persistent=false": ["any"],
    # Custom value for leaves
    "update_bit=true": ["any"],
    "waterlogged=true": ["any"],
    "waterlogged=false": ["any"],
    "powered=true": ["trapdoor", "door", "fence_gate", "bell"],
    "powered=false": ["trapdoor", "door", "fence_gate", "bell"],
    "enabled=true": ["hopper"],
    "enabled=false": ["hopper"],
    "facing=north": ["chest"],
    "facing=east": ["chest"],
    "facing=south": ["chest"],
    "facing=west": ["chest"],
    "type=single": ["chest"],
    "type=left": ["chest"],
    "type=right": ["chest"],
    "level=1": ["cauldron"],
    "level=2": ["cauldron"],
    "level=3": ["cauldron"]
}

mappings_file = open('utilities/block_mappings.json', 'r')
mappings = json.load(mappings_file)
mappings_file.close()

class Block:
    def __init__(self, block_nbt, under_block_nbt):
        global mappings
        # Save valueable information about the block
        self.nbt = block_nbt
        self.be_id = block_nbt["name"]
        self.be_states = block_nbt["states"]
        self.java_id = None
        self.cubes = None
        self.rotation = [0, 0, 0]

        # Fix for top door block if there is block underneath
        # if there is no block underneath (structure cut and only contains upper door part) we leave as is
        if "door" in self.be_id and under_block_nbt != None:
            # We separate conditions as python checks the whole condition and if the block is not a door it will not have the next state and crash
            if self.be_states["upper_block_bit"] == 1:
                self.be_states["direction"] = under_block_nbt["states"]["direction"]
                self.be_states["open_bit"] = under_block_nbt["states"]["open_bit"]
                self.be_states["door_hinge_bit"] = under_block_nbt["states"]["door_hinge_bit"]

        # Look for java equivalent block
        for block in mappings:
            if mappings[block]["bedrock_identifier"] == self.be_id and self.check_states(block):
                self.java_id = block
                break

        if self.java_id == None:
            print("Block with Bedrock ID: \"" + str(self.be_id) +
                  "\" does not have a java equivalent. Skipping.")
            raise NotJavaBlockException()
        else:
            # Remove invalid variants
            for invalid_variant in invalid_variants:
                for block in invalid_variants[invalid_variant]:
                    if block == "any" or block in self.be_id:
                        self.java_id = self.java_id.replace(
                            invalid_variant, "")
                        # Easier than convert string to list/dict and back
                        self.java_id = self.java_id.replace(
                            "[,", "[")
                        self.java_id = self.java_id.replace(
                            ",]", "]")
                        self.java_id = self.java_id.replace(
                            ",,", ",")

    # Compare the Java and the Bedrock blockstates to see if they match
    def check_states(self, block):
        state_amount = 0
        state_equal = 0
        for be_state in self.be_states:
            state_amount += 1
            for map_state in mappings[block]["bedrock_states"]:
                be_state_value = self.be_states[be_state]

                if be_state == map_state and be_state_value == mappings[block]["bedrock_states"][map_state]:
                    state_equal += 1
                    break

        return state_amount == state_equal


class NotJavaBlockException(Exception):
    pass
