import unittest
from my_scripts import misc_func as mf


class TestMiscFunc(unittest.TestCase):

    def test_get_coords_1(self):
        self.assertRaises(IndexError, mf.get_coords, [1])

    def test_get_coords_2(self):
        coords = mf.get_coords([1, 2])
        self.assertTrue(len(coords), 2)
        self.assertTrue(coords[0], 1)
        self.assertTrue(coords[1], 2)

    def test_get_coords_3(self):
        coords = mf.get_coords([1, 2, 3])
        self.assertTrue(len(coords), 2)
        self.assertTrue(coords[0], 2)
        self.assertTrue(coords[1], 2)
