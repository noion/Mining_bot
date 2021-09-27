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


def local_scroll_up():
    flag = True
    x = random.randint(1050, 1170)
    y = random.randint(300, 340)
    win32api.SetCursorPos((x, y))
    while flag:
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, random.randint(300, 400))
        time.sleep(3)
        if pyautogui.locateOnScreen(ci.LOCAL_UP_PREW, region=ci.RIGHT_LOCAL, confidence=0.7) is not None:
            flag = False
        pyautogui.screenshot(region=ci.RIGHT_LOCAL).save(r'img/local_up_prew.png')
    time.sleep(random.randint(1, 3))

def colibrate_local():
    img = pyautogui.screenshot(region=ci.RIGHT_PART_SCREEN)
    img.save(r'img/target_img.png')
    img_cv = cv.imread(r'img/target_img.png')
    x, y, w, h = ci.RIGHT_PART_SCREEN
    x_r, y_r, w_r, h_r = ci.RIGHT_LOCAL_RELATION
    x_l, y_l, w_l, h_l = ci.RIGHT_LOCAL
    x_cor_r = x_r - x
    y_cor_r = y_r - y
    relation_cv = cv.rectangle(img_cv, (x_cor_r, y_cor_r), (x_cor_r + w_r, y_cor_r + h_r), (0, 0, 255), thickness=1)
    x_cor_l = x_l - x
    y_cor_l = y_l - y
    local_cv = cv.rectangle(relation_cv, (x_cor_l, y_cor_l), (x_cor_l + w_l, y_cor_l + h_l), (0, 255, 0), thickness=1)
    main_window = cv.rectangle(local_cv, (x_cor_l, y_cor_l), (x_cor_l + w_l, y_cor_l + h_l), (0, 255, 0), thickness=1)
    cv.imshow('img', local_cv)
