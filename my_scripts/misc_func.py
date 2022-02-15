import random
import time
import pyautogui
import my_scripts.coords_and_img as ci


def rand_coords(coords):
    x, y, max_x, max_y = coords[0], coords[1], coords[2], coords[3]
    point_x = random.randint(x, x + round(max_x / 2))
    point_y = random.randint(y, y + round(max_y / 2))
    return point_x, point_y


def get_coords(coords):
    if len(coords) < 2:
        raise IndexError
    if len(coords) == 2:
        return coords[0], coords[1]
    x, y, max_x = coords[0], coords[1], coords[2]
    if len(coords) > 3:
        max_y = coords[3]
    else:
        max_y = max_x
    return rand_coords([x, y, max_x, max_y])


def click_queue(queue_list):
    for coords in queue_list:
        try:
            x, y = get_coords(coords)
        except IndexError:
            print('Incorrect coordinates', coords)
        pyautogui.leftClick(x, y)
        time.sleep(2)


def screen_shot():
    img = pyautogui.screenshot(region=ci.RIGHT_PART_SCREEN)
    img.save(r'img/target_img.png')
