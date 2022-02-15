import pyautogui
import time
import random
import pygame
from threading import Thread
from queue import Queue
from my_scripts.coords_and_img import *
from my_scripts import misc_func as mf

V_LC = 'v0.41'
pygame.mixer.init()
SAVE_FILE = 'save.txt'
q = Queue()


class MainLocalCheck:

    def __init__(self, save_file, starter, threads, queue=None):
        self.save_file = save_file
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
        self.pull_num = 1

    '''
    information block
    '''

    def info(self, text):
        if not self.threads:
            for key in text.keys():
                print(f'{key} = {text[key]}')
        else:
            text['pull_num'] = self.pull_num
            self.queue.put(text)
            self.pull_num += 1

    def information_text(self):
        if not self.threads:

            self.info({'info': f''''time = {time.ctime()}
                            ore = {self.ore}, status = {self.status}, cargo = {self.cargo}, 
                            first belt status = {self.status_belt_1}, minus = {self.minus}, neutal = {self.neutral}'''})
        else:
            if self.ore < 1000000:
                calc = str(round(self.ore // 1000))
                ore = f'{calc} k'
            else:
                calc = str(round(self.ore / 1000000, 2))
                ore = f'{calc} kk'
            self.info({'status': self.status})
            self.info({'minus': self.minus})
            self.info({'neutral': self.neutral})
            self.info({'first_belt': self.status_belt_1})
            self.info({'cargo': self.cargo})
            self.info({'drill_status': self.drill_status})
            self.info({'ore': ore})

    '''
    save-load block
    '''

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
                self.information_text()
        except FileNotFoundError:
            self.info({'info': 'NO SAVE'})
            with open('save.txt', encoding='utf-8', mode='x') as _:
                pass
            self.data_save()

    '''
    actions block
    '''

    def drill_on(self):
        self.status = 'mine'
        self.drill_status = True
        self.info({'drill_status': self.drill_status})
        self.time_start = time.time()
        self.data_save()
        mf.click_queue([DREEL_1, DREEL_2, DREEL_3])

    def neutral_minus_check(self):
        if self.status == 'warp_to_dock':
            return
        if pyautogui.locateOnScreen(NEW_LOCAL_ZERO, region=NEW_LOCAL_RELATIONS_MINUS, confidence=0.75,
                                    grayscale=True) is None:
            self.minus = True
            self.info({'minus': self.minus})
            self.data_save()
            return
        else:
            self.minus = False
        if pyautogui.locateOnScreen(NEW_LOCAL_ZERO, region=NEW_LOCAL_RELATIONS_NEUTRAL, confidence=0.75,
                                    grayscale=True) is None:
            self.neutral = True
            self.info({'neutral': self.neutral})
            self.data_save()
            return
        else:
            self.neutral = False

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

    '''
    logic block
    '''

    def in_station(self):
        if pyautogui.locateOnScreen(STATION, region=STATION_SCREEN, confidence=0.8) is not None:
            time.sleep(4)
            self.status = 'dock'
            self.over = False
            time.sleep(5)
            if self.cargo == 'fool':
                time_ = round(self.time_stop - self.time_start)
                ore_mined = 3 * (time_ * 29.53 + time_ * 30.59)
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
            self.neutral_minus_check()
            while self.neutral or self.minus:
                time.sleep(3)
                self.neutral_minus_check()
                self.data_save()
                self.information_text()
            if self.cargo == 'empty':
                mf.click_queue([UNDOCK])
                time.sleep(random.randint(18, 20))
                self.status = 'idle'
                self.neutral_minus_check()
                if self.minus or self.neutral:
                    self.to_dock()

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
                time.sleep(random.randint(60, 61))
                self.drill_on()
                self.info({'status': self.status})

                self.data_save()

        if self.status == 'idle' and not self.minus:
            self.neutral_minus_check()
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
            time.sleep(random.randint(60, 61))
            self.neutral_minus_check()
            if self.minus or self.neutral:
                self.to_dock()
                self.data_save()
            self.drill_on()
            self.data_save()

    '''
    assembly block
    '''

    def local_check(self):
        while True:
            status_previous = self.status
            minus_previous = self.minus
            neutral_previous = self.neutral
            drill_previous = self.drill_status
            if self.starter:
                self.start_check()
            while self.status in ['dock', 'warp_to_dock']:
                self.in_station()

            while self.status in ['warp_to_mine', 'mine', 'idle']:
                self.in_space_check()
            if status_previous != self.status or minus_previous != self.minus or neutral_previous != self.neutral or \
                    drill_previous != self.drill_status:
                self.information_text()

    def func_for_tread(self):
        self.starter = False
        while not self.starter:
            time.sleep(1)
        self.local_check()


class process(Thread):
    def __init__(self, check, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check = check

    def run(self):
        while True:
            try:
                self.check.local_check()
            except OSError as err:
                print(f'system restart... : {err}')
                self.run()


if __name__ == '__main__':
    check = MainLocalCheck(save_file=SAVE_FILE, starter=True, threads=False)
    start = process(check)
    start.run()
