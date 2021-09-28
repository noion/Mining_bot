import pyautogui
import time
import random
import win32api
import win32con
import pygame
from threading import Thread
from queue import Queue
from my_scripts.coords_and_img import *
from my_scripts import misc_func as mf

V_LC = 'v0.34'
pygame.mixer.init()
SAVE_FILE = 'save.txt'
q = Queue()


class MainLocalCheck:

    def __init__(self, save_file, starter, threads, queue=None):
        self.save_file = save_file
        self.windows = 0
        self.recheck = False
        self.starter = starter
        self.over = False
        self.status_belt_1 = True
        self.minus = False
        self.neutral = False
        self.drill_status = False
        self.status = ''
        self.cargo = 'empty'
        self.ore = 0
        self.time_start = 0
        self.time_stop = 0
        self.threads = threads
        self.queue = queue
        self.neutral_cord_y = None

    def info(self, text):
        if not self.threads:
            for key in text.keys():
                print(f'{key} = {text[key]}')
        else:
            self.queue.put(text)

    def inforamtion_text(self):
        if not self.threads:

            self.info({'info': f''''time = {time.ctime()}
                            ore = {self.ore}, status = {self.status}, cargo = {self.cargo}, 
                            first belt status = {self.status_belt_1}, minus = {self.minus}, neutal = {self.neutral}'''})
        else:
            if self.ore < 1000000:
                calc = str(round(self.ore // 1000))
                ore = (f'{calc} k')
            else:
                calc = str(round(self.ore / 1000000, 2))
                ore = (f'{calc} kk')
            self.info({'status': self.status})
            self.info({'minus': self.minus})
            self.info({'neutral': self.neutral})
            self.info({'first_belt': self.status_belt_1})
            self.info({'cargo': self.cargo})
            self.info({'drill_status': self.drill_status})
            self.info({'ore': ore})
            self.info({'neutral_y': self.neutral_cord_y})

    def data_save(self):
        data = {'time_start': self.time_start, 'time_stop': self.time_stop, 'ore': self.ore, 'status': self.status,
                'cargo': self.cargo, 'first_belt_status': self.status_belt_1, 'minus': self.minus,
                'neutal': self.neutral, 'dreel_status': self.drill_status}
        with open('save.txt', encoding='utf-8', mode='w') as save:
            for key, value in data.items():
                save.write(f'{key} {value} ')

    def data_load(self):
        ore_mined = None
        try:
            with open('save.txt', encoding='utf-8', mode='r') as save:
                data = save.read().split(' ')
                self.time_start = float(data[1])
                self.time_stop = float(data[3])
                self.status = data[7]
                self.cargo = data[9]
                self.ore = float(data[5])
                if data[11] == 'True':
                    self.status_belt_1 = True
                else:
                    self.status_belt_1 = False
                if data[17] == 'True':
                    self.drill_status = True
                else:
                    self.drill_status = False
                if self.time_start == '' or self.time_start < self.time_stop and self.cargo == 'empty':
                    pass
                else:
                    self.info({'info': 'loading data...'})
                    if self.cargo == 'fool':
                        time_ = round(self.time_stop - self.time_start)
                        ore_mined = 3 * (time_ * 21.91 + time_ * 26.415)
                    if ore_mined is not None:
                        self.ore += ore_mined
                        self.extraction()
                        self.data_save()
                self.inforamtion_text()
        except FileNotFoundError:
            self.info({'info': 'NO SAVE'})
            with open('save.txt', encoding='utf-8', mode='x') as save:
                pass
            self.data_save()

    def drill_on(self):
        self.status = 'mine'
        self.drill_status = True
        self.info({'drill_status': self.drill_status})
        self.time_start = time.time()
        self.data_save()
        mf.click_queue([DREEL_1, DREEL_2, DREEL_3])

    def neutral_minus_check(self):
        try:
            if self.status == 'warp_to_dock':
                pass
            if pyautogui.locateOnScreen(RED_MINUS, region=RIGHT_LOCAL_RELATION, confidence=0.75) is not None:
                self.minus = True
                self.info({'minus': self.minus})
                return
            else:
                self.minus = False
            neutral = pyautogui.locateOnScreen(NEUTRAL_GRAYSCALE, region=RIGHT_LOCAL_RELATION, confidence=0.75,
                                               grayscale=True)
            if neutral is not None:
                x, y = pyautogui.center(neutral)
                self.neutral_cord_y = y
                neut_check = []
                for i in range(2):
                    if pyautogui.locateOnScreen(LOCAL_ME, region=(1057, y - 10, 140, 25), confidence=0.75) is not None \
                            or pyautogui.locateOnScreen(LOCAL_EMPTY_GRAYSCALE, region=(1045, y - 10, 140, 30),
                                                        confidence=0.75, grayscale=True) is not None:
                        neut_check.append(False)
                    else:
                        neut_check.append(True)
                    time.sleep(2)
                    print(neut_check)
                if False not in neut_check:
                    self.neutral = True
                    self.info({'neutral': self.neutral})
                    self.info({'neutral_y': self.neutral_cord_y})
                    pyautogui.screenshot(region=(1057, y - 10, 140, 25)).save('img/i_see.png')

                    return
                else:
                    self.neutral = False
                    self.neutral_cords = None
            else:
                self.neutral = False
                self.neutral_cords = None
        except Exception as err:
            print(err)

    def local_scroll(self):
        local_allert = False
        x = random.randint(1090, 1120)
        y = random.randint(300, 340)
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -150)
        time.sleep(3)
        self.neutral_minus_check()
        if self.neutral or self.minus:
            local_allert = True
        return local_allert

    def recheck_local(self, scroll_up=True, on_undock=False):
        flag = True
        self.recheck = False
        if self.minus or self.neutral:
            self.info({'info': "still minus, let's wait..."})
            time.sleep(20)
        if scroll_up:
            mf.local_scroll_up()
        while flag:
            local_allert = self.local_scroll()
            if local_allert:
                self.recheck = True
            if local_allert:
                if self.status == 'idle':
                    return
                while self.neutral or self.minus:
                    self.neutral_minus_check()
            if pyautogui.locateOnScreen(LOCAL_PREW, region=RIGHT_LOCAL, confidence=0.7) is not None:
                if local_allert:
                    self.recheck = True
                flag = False
            pyautogui.screenshot(region=RIGHT_LOCAL).save(r'img/local_prew.png')

    def start_check(self):
        self.data_load()
        if pyautogui.locateOnScreen(STATION, region=STATION_SCREEN, confidence=0.7) is not None:
            self.status = 'dock'
        else:
            self.status = 'mine'
            self.time_start = time.time()
        if self.starter:
            self.starter = False

    def to_dock(self):
        if self.status == 'idle':
            if not self.over:
                self.over = True
                mf.click_queue([OVER_BUTTON, VUE])
                mf.click_queue([OVER_STATION, GO_DOCK])
                self.status = 'dock'
        else:
            self.time_stop = time.time()
            self.drill_status = False
            self.info({'drill_status': self.drill_status})
            self.status = 'warp_to_dock'
            pygame.mixer.music.load("audio/Минус.mp3")
            pygame.mixer.music.play()
            mf.click_queue([OVER_SELECTOR, OVER_SELECTOR_STATION, OVER_STATION, GO_DOCK, INTERA_1, INTERA_2])

    def extraction(self):
        if self.cargo == 'fool' and self.status == 'dock':
            mf.click_queue([CARGO_SPAN])
            time.sleep(random.randint(5, 7))
            mf.click_queue(
                [MY_STORAGE_CLOSE, STATION_STORAGE_ORE, SELECT_ALL, MOVE_CARGO_TO, MOVE_TO_STATION,
                 CLOSE_WINDOW])
            self.cargo = 'empty'

    def in_station(self):
        if pyautogui.locateOnScreen(STATION, region=STATION_SCREEN, confidence=0.8) is not None:
            time.sleep(4)
            self.status = 'dock'
            self.over = False
            time.sleep(5)
            if self.cargo == 'fool':
                time_ = round(self.time_stop - self.time_start)
                ore_mined = 3 * (time_ * 21.91 + time_ * 26.415)
                self.ore += ore_mined
                if self.ore < 1000000:
                    calc = str(round(self.ore // 1000))
                    ore = f'{calc} k'
                else:
                    calc = str(round(self.ore / 1000000, 2))
                    ore = f'{calc} kk'
                self.info({'ore': ore})
                self.info({'info': f'Now mined {round(ore_mined, 2)} ore'})
                self.extraction()
                self.data_save()
            self.recheck_local(scroll_up=False, on_undock=True)
            self.inforamtion_text()
            if self.cargo == 'empty' and not self.recheck:
                x, y = mf.rand_cords(UNDOCK)
                mf.click(x, y)
                time.sleep(random.randint(20, 30))
                self.status = 'idle'
                self.recheck_local(scroll_up=False)
                if self.minus or self.neutral:
                    self.to_dock()
            else:
                mf.local_scroll_up()

    def in_space_check(self):
        self.neutral_minus_check()
        if self.status != 'warp_to_dock':
            if self.minus or self.neutral:
                self.to_dock()
                self.cargo = 'fool'
                self.data_save()

            if pyautogui.locateOnScreen(FOOL_CARGO_WORDS, region=ALL_SCREEN, confidence=0.7) is not None:
                self.time_stop = time.time()
                self.drill_status = False
                self.info({'drill_status': self.drill_status})
                self.status = 'warp_to_dock'
                self.cargo = 'fool'
                pygame.mixer.music.load("audio/Полное_карго.mp3")
                pygame.mixer.music.play()
                mf.click_queue([OVER_SELECTOR, OVER_SELECTOR_STATION, OVER_STATION, GO_DOCK, INTERA_1, INTERA_2])
                self.data_save()

            if pyautogui.locateOnScreen(EMPTY_BELT, region=ALL_SCREEN, confidence=0.7) is not None:
                self.time_stop = time.time()
                self.drill_status = False
                self.info({'drill_status': self.drill_status})
                time_ = round(self.time_stop - self.time_start)
                ore_mined = 3 * (time_ * 21.91 + time_ * 26.415)
                self.ore += ore_mined
                if not self.status_belt_1:
                    self.status_belt_1 = True
                    self.info({'first_belt': self.status_belt_1})
                else:
                    self.status_belt_1 = False
                    self.info({'first_belt': self.status_belt_1})
                pygame.mixer.music.load("audio/Нет_минералов.mp3")
                pygame.mixer.music.play()
                mf.click_queue([OVER_REWARP_BELT, WARP_TO_2_POSITION])
                time.sleep(random.randint(60, 70))
                self.drill_on()
                self.status = 'mine'
                self.info({'status': self.status})

                self.data_save()

        if self.status == 'idle' and not self.minus:
            self.recheck_local(scroll_up=False, on_undock=True)
            self.status = 'warp_to_mine'
            if not self.over:
                self.over = True
                mf.click_queue([OVER_BUTTON, VUE])
            if self.status_belt_1:
                queue = [OVER_SELECTOR, OVER_SELECTOR_BELT, OVER_STATION, WARP_TO_1_POSITION]
            else:
                queue = [OVER_SELECTOR, OVER_SELECTOR_BELT, OVER_REWARP_BELT, WARP_TO_2_POSITION]
            mf.click_queue(queue)

        if self.status == 'warp_to_mine':
            time.sleep(random.randint(60, 70))
            self.neutral_minus_check()
            if self.minus or self.neutral:
                self.to_dock()
                self.data_save()
            self.drill_on()
            self.data_save()

    def local_check(self):
        while True:
            status_prew = self.status
            minus_prew = self.minus
            neutral_prew = self.neutral
            drill = self.drill_status
            if self.starter:
                self.start_check()
            while self.status in ['dock', 'warp_to_dock']:
                self.in_station()

            while self.status in ['warp_to_mine', 'mine', 'idle']:
                self.in_space_check()
            if status_prew != self.status or minus_prew != self.minus or neutral_prew != self.neutral or drill != self.drill_status:
                self.inforamtion_text()

    def func_for_tread(self):
        self.starter = False
        while not self.starter:
            time.sleep(1)
        self.local_check()


class pocess(Thread):

    def __init__(self, check, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check = check

    def run(self):
        while True:
            try:
                self.check.local_check()
            except OSError as err:
                print(f'sistem restart... : {err}')
                self.run()


if __name__ == '__main__':
    check = MainLocalCheck(save_file=SAVE_FILE, starter=True, threads=False)
    start = pocess(check)
    start.run()
