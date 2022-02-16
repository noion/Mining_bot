import unittest
import random
import time
from my_scripts import misc_func as mf
from unittest.mock import MagicMock
from unittest.mock import patch


class TestMiscFunc(unittest.TestCase):

    def test_rand_cords_3(self):
        # given
        random.seed(0)  # disable random
        # when
        coords = mf.rand_cords([10, 20, 40])
        # then
        self.assertEqual(2, len(coords))
        self.assertEqual(22, coords[0])
        self.assertEqual(37, coords[1])

    def test_rand_cords_4_equal_3(self):
        # given
        random.seed(0)  # disable random
        # when
        coords = mf.rand_cords([10, 20, 40, 40])
        # then
        self.assertEqual(2, len(coords))
        self.assertEqual(22, coords[0])
        self.assertEqual(37, coords[1])

    def test_rand_cords_4(self):
        # given
        random.seed(0)  # disable random
        # when
        coords = mf.rand_cords([10, 20, 40, 35])
        # then
        self.assertEqual(2, len(coords))
        self.assertEqual(22, coords[0])
        self.assertEqual(36, coords[1])

    def test_click_queue(self):
        # given
        with patch('my_scripts.misc_func.rand_cords', MagicMock(return_value=[3, 4])) as rand_cords_mock, \
                patch('pyautogui.leftClick', MagicMock()) as left_click_mock, \
                patch('time.sleep', MagicMock()) as sleep_mock:
            # when
            mf.click_queue([[1, 2, 3]])
            # then
            rand_cords_mock.assert_called_once_with([1, 2, 3])
            left_click_mock.assert_called_once_with(3, 4)
            sleep_mock.assert_called_once_with(2)
