# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_v0.1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# pyuic5 -x qt_v0.1_bg -o result.py
# pyinstaller --onefile -w -i "E:\Python\Mining_bot\img\ico.ico" v_local_check.py


V_QT = 'v0.13'

import sys

import pyautogui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from queue import Queue
from PIL import Image, ImageDraw, ImageFont, ImageColor
import cv2 as cv
import local_check as lc
from my_scripts import misc_func as mf
import telegram_bot

SAVE_FILE = 'save.txt'

q = Queue()
q_telegram = Queue()
template_width = 390
template_height = 220


def resiz_bg(width, height):
    im = Image.open('img/background.png')
    w, h = im.size
    im = im.resize((width, height))
    im.save('img/bg.png')


class Worker(QThread):
    progress = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        self.progress.emit(f"Local check START")
        check = lc.MainLocalCheck(save_file=SAVE_FILE, starter=True, threads=True, queue=q)
        while True:
            try:
                check.local_check()
            except OSError as err:
                print(f'sistem restart... : {err}')
                check.local_check()


class WorkerTelegram(QThread):
    progress = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        telegram_bot.bot_process()


class Ui_MainWindow(object):
    def __init__(self):
        self.neutral_cord_y = None
        self.pull_num = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(0, 620, template_width, template_height)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/ico.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        text_style_sheet = ("color: rgb(46, 255, 158);\n"
                            "font-family: arial;\n"
                            "font-size: 12px;\n"
                            "font-weight: bold")

        self.v_local_check = QtWidgets.QLabel(self.centralwidget)
        self.v_local_check.setGeometry(QtCore.QRect(150, 0, 120, 16))
        self.v_local_check.setObjectName("v_local_check")
        self.v_local_check.setStyleSheet(text_style_sheet)
        self.v_qt = QtWidgets.QLabel(self.centralwidget)
        self.v_qt.setGeometry(QtCore.QRect(270, 0, 120, 16))
        self.v_qt.setObjectName("v_qt")
        self.v_qt.setStyleSheet(text_style_sheet)
        self.v_tb = QtWidgets.QLabel(self.centralwidget)
        self.v_tb.setGeometry(QtCore.QRect(270, 20, 120, 16))
        self.v_tb.setObjectName("v_tb")
        self.v_tb.setStyleSheet(text_style_sheet)

        self.label_status = QtWidgets.QLabel(self.centralwidget)
        self.label_status.setGeometry(QtCore.QRect(20, 40, 41, 16))
        self.label_status.setObjectName("label_status")
        self.label_status.setStyleSheet(text_style_sheet)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(300, 140, 71, 23))
        self.start_button.setObjectName("start_button")
        self.start_telegram = QtWidgets.QPushButton(self.centralwidget)
        self.start_telegram.setGeometry(QtCore.QRect(300, 107, 71, 23))
        self.start_telegram.setObjectName("start_telegram")
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(300, 173, 71, 23))
        self.stop_button.setObjectName("start_button")
        self.local_cloib = QtWidgets.QPushButton(self.centralwidget)
        self.local_cloib.setGeometry(QtCore.QRect(225, 140, 71, 23))
        self.local_cloib.setObjectName("local_cloib")
        self.self_remove = QtWidgets.QPushButton(self.centralwidget)
        self.self_remove.setGeometry(QtCore.QRect(225, 173, 71, 23))
        self.self_remove.setObjectName("self_remove")
        self.station_screenshot = QtWidgets.QPushButton(self.centralwidget)
        self.station_screenshot.setGeometry(QtCore.QRect(150, 140, 71, 23))
        self.station_screenshot.setObjectName("dock_button")
        self.status_info = QtWidgets.QLabel(self.centralwidget)
        self.status_info.setGeometry(QtCore.QRect(90, 40, 30, 16))
        self.status_info.setObjectName("status_info")
        self.status_info.setStyleSheet(text_style_sheet)
        self.minus_info = QtWidgets.QLabel(self.centralwidget)
        self.minus_info.setGeometry(QtCore.QRect(90, 70, 30, 16))
        self.minus_info.setObjectName("minus_info")
        self.minus_info.setStyleSheet(text_style_sheet)
        self.minus = QtWidgets.QLabel(self.centralwidget)
        self.minus.setGeometry(QtCore.QRect(20, 70, 41, 16))
        self.minus.setObjectName("minus")
        self.minus.setStyleSheet(text_style_sheet)
        self.neutral_info = QtWidgets.QLabel(self.centralwidget)
        self.neutral_info.setGeometry(QtCore.QRect(90, 100, 30, 16))
        self.neutral_info.setObjectName("neutral_info")
        self.neutral_info.setStyleSheet(text_style_sheet)
        self.neutral = QtWidgets.QLabel(self.centralwidget)
        self.neutral.setGeometry(QtCore.QRect(20, 100, 41, 16))
        self.neutral.setObjectName("neutral")
        self.neutral.setStyleSheet(text_style_sheet)
        self.first_belt_info = QtWidgets.QLabel(self.centralwidget)
        self.first_belt_info.setGeometry(QtCore.QRect(90, 140, 30, 16))
        self.first_belt_info.setObjectName("first_belt_info")
        self.first_belt_info.setStyleSheet(text_style_sheet)
        self.first_belt = QtWidgets.QLabel(self.centralwidget)
        self.first_belt.setGeometry(QtCore.QRect(20, 140, 51, 16))
        self.first_belt.setObjectName("first_belt")
        self.first_belt.setStyleSheet(text_style_sheet)
        self.cargo_info = QtWidgets.QLabel(self.centralwidget)
        self.cargo_info.setGeometry(QtCore.QRect(240, 40, 30, 16))
        self.cargo_info.setObjectName("cargo_info")
        self.cargo_info.setStyleSheet(text_style_sheet)
        self.cargo_status = QtWidgets.QLabel(self.centralwidget)
        self.cargo_status.setGeometry(QtCore.QRect(150, 40, 71, 16))
        self.cargo_status.setObjectName("cargo_status")
        self.cargo_status.setStyleSheet(text_style_sheet)
        self.drill_info = QtWidgets.QLabel(self.centralwidget)
        self.drill_info.setGeometry(QtCore.QRect(240, 70, 30, 16))
        self.drill_info.setObjectName("drill_info")
        self.drill_info.setStyleSheet(text_style_sheet)
        self.drill_status = QtWidgets.QLabel(self.centralwidget)
        self.drill_status.setGeometry(QtCore.QRect(150, 70, 71, 16))
        self.drill_status.setObjectName("drill_status")
        self.drill_status.setStyleSheet(text_style_sheet)
        self.ore_info = QtWidgets.QLabel(self.centralwidget)
        self.ore_info.setGeometry(QtCore.QRect(240, 100, 60, 16))
        self.ore_info.setObjectName("ore_info")
        self.ore_info.setStyleSheet(text_style_sheet)
        self.ore_mined = QtWidgets.QLabel(self.centralwidget)
        self.ore_mined.setGeometry(QtCore.QRect(150, 100, 71, 16))
        self.ore_mined.setObjectName("ore_mined")
        self.ore_mined.setStyleSheet(text_style_sheet)
        self.activity_view = QtWidgets.QLabel(self.centralwidget)
        self.activity_view.setGeometry(QtCore.QRect(20, 180, 220, 16))
        self.activity_view.setObjectName("activity_view")
        self.activity_view.setStyleSheet(text_style_sheet)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 477, 21))
        self.menubar.setObjectName("menubar")
        self.menubar.setStyleSheet(text_style_sheet)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet(text_style_sheet)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setEnabled(False)
        self.frame.setGeometry(QtCore.QRect(0, 0, template_width, template_height))
        self.frame.setToolTipDuration(-1)
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("background-image: url(\"img/bg.png\"); \n"
                                 "background-repeat: no-repeat; \n"
                                 "background-position: center;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.frame.raise_()
        self.v_local_check.raise_()
        self.v_qt.raise_()
        self.v_tb.raise_()

        self.label_status.raise_()
        self.status_info.raise_()
        self.minus_info.raise_()
        self.minus.raise_()
        self.neutral_info.raise_()
        self.neutral.raise_()
        self.first_belt_info.raise_()
        self.first_belt.raise_()
        self.cargo_info.raise_()
        self.cargo_status.raise_()
        self.drill_info.raise_()
        self.drill_status.raise_()
        self.ore_info.raise_()
        self.ore_mined.raise_()
        self.activity_view.raise_()
        self.start_button.raise_()
        self.stop_button.raise_()
        self.station_screenshot.raise_()
        self.local_cloib.raise_()
        self.self_remove.raise_()
        self.start_telegram.raise_()
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.timer = QTimer()
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.add_fuction)
        self.timer.start()

        self.station_screenshot.clicked.connect(self.station_screen)
        self.local_cloib.clicked.connect(mf.colibrate_local)
        self.self_remove.clicked.connect(self.remove_me)

        self.my_thread = Worker()
        self.start_button.clicked.connect(self.start_worker)
        self.stop_button.clicked.connect(self.stop_worker)

        self.telegram_thread = WorkerTelegram()
        self.start_telegram.clicked.connect(self.start_telegram_thread)





    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MinerBot"))

        self.v_local_check.setText((_translate("MainWindow", f"Local check: {lc.V_LC}")))
        self.v_qt.setText((_translate("MainWindow", f"Interface: {V_QT}")))
        self.v_tb.setText((_translate("MainWindow", f"Telegram bot: {telegram_bot.V_TB}")))

        self.label_status.setText(_translate("MainWindow", "Status"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.start_telegram.setText(_translate("MainWindow", "Telegram bot"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))
        self.local_cloib.setText(_translate("MainWindow", "Colibrate"))
        self.self_remove.setText(_translate("MainWindow", "Self remove"))
        self.station_screenshot.setText(_translate("MainWindow", "Station screen"))
        self.status_info.setText(_translate("MainWindow", "None"))
        self.minus_info.setText(_translate("MainWindow", "None"))
        self.minus.setText(_translate("MainWindow", "Minus"))
        self.neutral_info.setText(_translate("MainWindow", "None"))
        self.neutral.setText(_translate("MainWindow", "Neutral"))
        self.first_belt_info.setText(_translate("MainWindow", "None"))
        self.first_belt.setText(_translate("MainWindow", "First belt"))
        self.cargo_info.setText(_translate("MainWindow", "None"))
        self.cargo_status.setText(_translate("MainWindow", "Cargo status"))
        self.drill_info.setText(_translate("MainWindow", "None"))
        self.drill_status.setText(_translate("MainWindow", "Drill status"))
        self.ore_info.setText(_translate("MainWindow", "None"))
        self.ore_mined.setText(_translate("MainWindow", "Ore mined"))
        self.activity_view.setText(_translate("MainWindow", "Local check STOP..."))

    def station_screen(self):
        img = pyautogui.screenshot(region=(1730, 200, 150, 80))
        img.save(r'img/station.png')

    def remove_me(self):
        if self.neutral_cord_y is not None:
            me = pyautogui.screenshot(region=(1057, int(self.neutral_cord_y) - 10, 140, 25))
            me.save(r'img/me_remove.png')
            colib_me = cv.imread(r'img/me_remove.png')
            cv.imshow('Remove neutral', colib_me)
            self.activity_view.setText("Look at screenshot, i remove him")
        else:
            self.activity_view.setText("Don't see you, show me in local")

    def add_fuction(self):
        while len(q.queue) > 0:
            info = q.get()
            if self.pull_num == info['pull_num']:
                pass
            else:
                self.pull_num = info['pull_num']
                keys = list(info.keys())
                name = keys[0]
                value = info[name]
                if name == 'info':
                    self.activity_view.setText(value)
                elif name == 'status':
                    self.status_info.setText(value)
                elif name == 'minus':
                    self.minus_info.setText(str(value))
                elif name == 'neutral':
                    self.neutral_info.setText(str(value))
                elif name == 'first_belt':
                    self.first_belt_info.setText(str(value))
                elif name == 'cargo':
                    self.cargo_info.setText(value)
                elif name == 'drill_status':
                    self.drill_info.setText(str(value))
                elif name == 'ore':
                    self.ore_info.setText(str(value))
                elif name == 'neutral_y':
                    self.neutral_cord_y = value



    def start_worker(self):
        self.my_thread.start()
        self.start_button.setEnabled(False)
        if self.my_thread.isRunning:
            self.activity_view.setText("Local check START...")

    def stop_worker(self):
        self.my_thread.stop()
        self.start_button.setEnabled(True)
        if self.my_thread.isFinished:
            self.activity_view.setText("Local check STOP...")

    def start_telegram_thread(self):
        self.telegram_thread.start()
        self.start_telegram.setEnabled(False)
        if self.telegram_thread.isRunning:
            self.activity_view.setText("Telegram bot START...")


def main():
    resiz_bg(template_width, template_height)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.add_fuction()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
