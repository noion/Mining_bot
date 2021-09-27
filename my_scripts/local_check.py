import pyautogui
import time
import random
import win32api, win32con
import pygame
from my_scripts.coords_and_img import *

pygame.mixer.init()


class MainLocalCheck:

    def __init__(self):
        self.starter = True
        self.status = ''
        self.cargo = ''
        self.over = False
        self.status_belt_1 = True
        self.minus = False
        self.ore = 0
        self.time_start = 0
        self.time_stop = 0

    def starter_text(self):
        print('_' * 10)
        print('LOADING...')
        print('_' * 10)
        time.sleep(1)
        print('ANALIZING...')
        time.sleep(1)
        print('STATUS...OK')
        time.sleep(1)
        print('CARGO...OK')
        time.sleep(1)
        print('LOCAL...OK')
        time.sleep(1)
        print('READY')

    def rand_cords(self, range):
        x, y, max_x = range[0], range[1], range[2]
        try:
            max_y = range[3]
        except IndexError:
            max_y = max_x
        point_x = random.randint(x, x + max_x)
        point_y = random.randint(y, y + max_y)
        return point_x, point_y

    def click(self, x, y):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def click_queue(self, queue_list):
        for cords in queue_list:
            x, y = self.rand_cords(cords)
            self.click(x, y)
            time.sleep(random.randint(2, 3))

    def activate_cloack(self):
        s_x, s_y = self.rand_cords(CLOACK)
        self.click(s_x, s_y)
        pygame.mixer.music.load("../audio/Минус.mp3")
        pygame.mixer.music.play()
        time.sleep(2)

    def local_scroll_up(self):
        x = random.randint(1050, 1170)
        y = random.randint(300, 340)
        win32api.SetCursorPos((x, y))
        for _ in range(3):
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, random.randint(300, 400))
            time.sleep(1)
        time.sleep(random.randint(1,3))

    def local_scroll(self):
        x = random.randint(1050, 1170)
        y = random.randint(300, 340)
        win32api.SetCursorPos((x, y))
        for _ in range(3):
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, random.randint(-400, -300))
            time.sleep(1)
            if pyautogui.locateOnScreen(RED_MINUS, region=RIGHT_LOCAL, confidence=0.8) is not None:
                self.minus = True
            else:
                self.minus = False
        time.sleep(random.randint(3, 6))

    def start_check(self):
        self.local_scroll()
        if pyautogui.locateOnScreen(FOOL_CARGO, region=CARGO_CHECK, confidence=0.71):
            self.cargo = 'fool'
        else:
            self.cargo = 'empty'
        if pyautogui.locateOnScreen(STATION, region=STATION_SCREEN, confidence=0.7) != None:
            self.status = 'idle'
        else:
            self.status = 'mine'
            self.time_start = time.time()
        if pyautogui.locateOnScreen(RED_MINUS, region=RIGHT_LOCAL, confidence=0.8) is not None:
            self.minus = True
            if self.status == 'idle':
                print('wating minus')
                while self.minus:
                    time.sleep(5)
                    if pyautogui.locateOnScreen(RED_MINUS, region=RIGHT_LOCAL, confidence=0.8) is None:
                        self.minus = False
                        print(self.minus)
            elif not self.minus:
                queue_list = [OVER_SELECTOR, OVER_SELECTOR_STATION, OVER_STATION, GO_DOCK]
                self.click_queue(queue_list)

    def recheck_local(self):
        if self.minus:
            while self.minus:
                print("still minus, let's wait...")
                time.sleep(20)
                if pyautogui.locateOnScreen(RED_MINUS, region=RIGHT_LOCAL, confidence=0.8) is not None:
                    pass
                else:
                    self.local_scroll_up()
                    self.local_scroll()

    def check_screen(self):
        if self.starter:
            self.starter_text()
            self.starter = False
            self.start_check()

            print(f''''time = {time.ctime()}
status = {self.status}, cargo = {self.cargo}, first belt status = {self.status_belt_1}, minus = {self.minus}''')
            self.recheck_local()

        if pyautogui.locateOnScreen(STATION, region=STATION_SCREEN, confidence=0.7) != None:
            ore_mined = None
            if self.status == 'dock' or self.status == 'empty_belt':
                time_ = round(self.time_stop - self.time_start)
                ore_mined = 3 * (time_ * 21.91 + time_ * 26.415)
            self.recheck_local()
            time.sleep(7)
            self.over = False
            if self.cargo == 'fool':
                print('start extracting...')
                queue = [CARGO_SPAN]
                self.click_queue(queue)
                time.sleep(random.randint(7, 10))
                queue = [MY_STORAGE_CLOSE, STATION_STORAGE_ORE, SELECT_ALL, MOVE_CARGO_TO, MOVE_TO_STATION, CLOSE_WINDOW]
                self.click_queue(queue)
                if ore_mined is not None:
                    self.ore += ore_mined
                print(f'you mined {round(self.ore, 2)} ore for this launch.... Approximately')
                self.cargo = 'empty'
            if self.cargo == 'empty':
                x, y = self.rand_cords(UNDOCK)
                self.click(x, y)
                time.sleep(random.randint(20, 30))
            self.status = 'idle'
            print(self.status)

            if self.status == 'idle':
                self.status = 'warp to mine'
                print(self.status)
                if not self.over:
                    self.local_scroll()
                    self.over = True
                    queue = [OVER_BUTTON, VUE]
                    self.click_queue(queue)
                    time.sleep(random.randint(2, 4))
                if self.status_belt_1:
                    queue = [OVER_SELECTOR, OVER_SELECTOR_BELT, OVER_STATION, WARP_TO_1_POSITION]
                else:
                    queue = [OVER_SELECTOR, OVER_SELECTOR_BELT, OVER_REWARP_BELT, WARP_TO_2_POSITION]
                self.click_queue(queue)

            if self.status == 'warp to mine':
                time.sleep(random.randint(60, 70))
                self.status = 'mine'
                print(self.status)
                queue = [DREEL_1, DREEL_2, DREEL_3]
                self.time_start = time.time()
                self.click_queue(queue)

        if pyautogui.locateOnScreen(RED_MINUS, region=RIGHT_LOCAL,
                                    confidence=0.8) is not None and self.status != 'dock':
            self.minus = True
            print(self.minus)
            self.time_stop = time.time()
            self.status = 'dock'
            print(self.status)
            self.cargo = 'fool'
            pygame.mixer.music.load("../audio/Минус.mp3")
            pygame.mixer.music.play()
            queue_list = [OVER_SELECTOR, OVER_SELECTOR_STATION, OVER_STATION, GO_DOCK]
            self.click_queue(queue_list)
        #     if self.status != 'cloack':
        #         self.status = 'cloack'
        #         self.activate_cloack()
        # else:
        #     if self.status == 'cloack':
        #         self.activate_cloack()
        #         self.status = 'mine'
        #     time.sleep(0.5)
        elif not self.minus:
            self.minus = False


        if pyautogui.locateOnScreen(FOOL_CARGO_WORDS, region=ALL_SCREEN,
                                    confidence=0.8) is not None and self.status != 'dock':
            self.time_stop = time.time()
            self.status = 'dock'
            print(self.status)
            self.cargo = 'fool'
            pygame.mixer.music.load("../audio/Полное_карго.mp3")
            pygame.mixer.music.play()
            queue_list = [OVER_SELECTOR, OVER_SELECTOR_STATION, OVER_STATION, GO_DOCK]
            self.click_queue(queue_list)

        if pyautogui.locateOnScreen(EMPTY_BELT, region=ALL_SCREEN,
                                    confidence=0.8) is not None and self.status != 'empty_belt':
            if self.status == 'dock':
                pass
            else:
                self.time_stop = time.time()
                time_ = round(self.time_stop - self.time_start)
                ore_mined = 3 * (time_ * 21.91 + time_ * 26.415)
                self.ore += ore_mined
                self.time_start = time.time()
                if not self.status_belt_1:
                    self.status_belt_1 = True
                    print(self.status_belt_1)
                    queue = [OVER_STATION, WARP_TO_1_POSITION]
                    self.click_queue(queue)
                else:
                    self.status_belt_1 = False
                    print(self.status_belt_1)
                    pygame.mixer.music.load("../audio/Нет_минералов.mp3")
                    pygame.mixer.music.play()
                    queue = [OVER_REWARP_BELT, WARP_TO_2_POSITION]
                    self.click_queue(queue)
                time.sleep(random.randint(60, 70))
                self.status = 'mine'
                print(self.status)
                queue = [DREEL_1, DREEL_2, DREEL_3]
                self.click_queue(queue)
            self.status = 'empty_belt'
            print(self.status)


check = MainLocalCheck()
while True:
    check.check_screen()
