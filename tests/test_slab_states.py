import unittest

from nbtlib import Byte, String

from structura_core import structura


class SlabStateTests(unittest.TestCase):
    def setUp(self):
        self.processor = structura.__new__(structura)

    def process(self, states):
        block = {
            "name": "minecraft:cut_copper_slab",
            "states": states,
        }
        return self.processor._process_block(block)

    def test_vertical_half_distinguishes_top_and_bottom_slabs(self):
        top = self.process({"minecraft:vertical_half": String("top")})
        bottom = self.process({"minecraft:vertical_half": String("bottom")})

        self.assertIsNone(top[0])
        self.assertTrue(top[1])
        self.assertIsNone(bottom[0])
        self.assertFalse(bottom[1])

    def test_boolean_top_states_still_work(self):
        for state_name in ("top_slot_bit", "upside_down_bit", "upper_block_bit"):
            with self.subTest(state_name=state_name):
                top = self.process({state_name: Byte(1)})
                bottom = self.process({state_name: Byte(0)})

                self.assertTrue(top[1])
                self.assertFalse(bottom[1])


if __name__ == "__main__":
    unittest.main()
