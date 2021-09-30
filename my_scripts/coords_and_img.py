import pyautogui

STATION = 'img/station.png'
STORAGE = 'img/station_storage.png'
STORAGE_P = 'img/station_storage_p.png'
RED_MINUS = 'img/red.png'
NEUTRAL_GRAYSCALE = 'img/neutral_gray.png'
FOOL_CARGO = 'img/cargo.jpg'
FOOL_CARGO_WORDS = 'img/fool_cargo.bmp'
EMPTY_BELT = 'img/empty_belt.bmp'
SPEED_MAX = 'img/speed_check_max.png'
SPEED_MIN = 'img/speed_check_min.png'
MINERAL = 'img/miniral.png'
LOCAL_ME = 'img/me_remove.png'
LOCAL_EMPTY_GRAYSCALE = 'img/empty_local_gray.png'
LOCAL_PREW = 'img/local_prew.png'
LOCAL_UP_PREW = 'img/local_up_prew.png'
ALL_SCREEN = (0, 0, 1830, 510)
RIGHT_LOCAL = (1045, 200, 180, 200)
RIGHT_LOCAL_NAME = (1045, 200, 140, 200)
RIGHT_LOCAL_RELATION = (1195, 200, 30, 200)
RIGHT_PART_SCREEN = (915, 0, 990, 600)
MY_OVER =(1840, 330, 20, 20)
OVER_SELECTOR = (1670,45,120,35)
OVER_SELECTOR_STATION = (1670,220,120,35)
OVER_STATION = (1660,85,120,35)
STATION_STORAGE_ORE = (965,260,170,50)
GO_DOCK = (1520,85,120,40)
STATION_SCREEN = (1730, 200, 150, 80)
UNDOCK = (1730,200,150,50)
RIGHT_CARGO = (955,110,68,30)
MY_STORAGE = (955, 150, 150, 50)
MY_STORAGE_CLOSE = (960, 100, 150, 30)
SELECT_ALL = (1640, 490, 65, 65)
MOVE_CARGO_TO = (965, 120, 180, 60)
MOVE_TO_STATION = (1200, 130, 180, 60)
OVER_SELECTOR_BELT = (1670, 430, 120, 35)
OVER_REWARP_BELT = (1660, 140, 120, 35)
WARP_TO_1_POSITION = (1520, 140, 120, 50)
SPEED_CHECK = (1385, 495, 60, 40)
CARGO_CHECK = (953, 108, 73, 38)
DREEL_1 = (1540, 510, 40, 40)
DREEL_2 = (1600, 510, 40, 40)
DREEL_3 = (1660, 510, 40, 40)
INTERA_1 = (1720, 510, 40, 40)
INTERA_2 = (1780, 510, 40, 40)
CLOSE_WINDOW = (1839, 63, 20, 20)
VUE = (1400, 480, 30, 30)
OVER_ONLY_BELTS = (1850, 80, 35, 35)
MINS_CHECK = (1660, 80, 15, 35)
WARP_TO_2_POSITION = (1520, 190, 120, 50)
CARGO_SPAN = (980, 120, 30, 10)
CLOACK = (1830, 510, 40)
OVER_BUTTON = (1840, 330, 20)

# if __name__ == '__main__':
#     img = pyautogui.screenshot(region=SPEED_CHECK)
#     img.save(r"../img/speed_check.png")
#     img = cv.imread(r"../img/speed_check.png")
#     img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#     cv.imwrite(r"../img/speed_check.png", img)