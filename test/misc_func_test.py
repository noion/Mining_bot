import unittest
from my_scripts import misc_func as mf
import random


class TestMiscFunc(unittest.TestCase):

    def test_rand_cords_3(self):
        # disable random
        random.seed(0)
        coords = mf.rand_cords([10, 20, 40])
        self.assertEqual(len(coords), 2)
        self.assertEqual(coords[0], 22)
        self.assertEqual(coords[1], 37)

    def test_rand_cords_4_equal_3(self):
        # disable random
        random.seed(0)
        coords = mf.rand_cords([10, 20, 40, 40])
        self.assertEqual(len(coords), 2)
        self.assertEqual(coords[0], 22)
        self.assertEqual(coords[1], 37)

    def test_rand_cords_4(self):
        # disable random
        random.seed(0)
        coords = mf.rand_cords([10, 20, 40, 35])
        self.assertEqual(len(coords), 2)
        self.assertEqual(coords[0], 22)
        self.assertEqual(coords[1], 36)
