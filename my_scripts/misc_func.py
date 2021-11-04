import random
import win32api, win32con
import time
import pyautogui
import cv2 as cv
import my_scripts.coords_and_img as ci


def rand_cords(range):
    x, y, max_x = range[0], range[1], range[2]
    try:
        max_y = range[3]
    except IndexError:
        max_y = max_x
    point_x = random.randint(x, x + round(max_x / 2))
    point_y = random.randint(y + 4, y + round(max_y / 2))
    return point_x, point_y


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def click_queue(queue_list):
    for cords in queue_list:
        x, y = rand_cords(cords)
        click(x, y)
        time.sleep(random.randint(1, 2))


def screen_shot():
    img = pyautogui.screenshot(region=ci.RIGHT_PART_SCREEN)
    img.save(r'img/target_img.png')
