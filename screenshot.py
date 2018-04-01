#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import re
from threading import Thread
from multiprocessing import Queue

str_queue = Queue()

try:
    import pyocr
    from PIL import Image
    import pyautogui
except ImportError:
    print('[!] Import error, start install')
    os.system('pip3 install python3-xlib pyautogui pyocr')
    os.system(
        'apt-get install scrot python-tk python3-dev python-imaging tesseract-ocr')

tools = pyocr.get_available_tools()[:]
print('[*] ocr using: {}'.format(tools[0].get_name()))


class CaptureMousePic(Thread):
    def __init__(self):
        super().__init__()
        self.thread_stop = False
        self.left, self.top = None, None

    def run(self):
        while not self.thread_stop:
            self.left, self.top = pyautogui.position()
            time.sleep(2)
            self.capture()

    def stop(self):
        self.thread_stop = True

    def capture(self):
        left_, top_ = pyautogui.position()  # return mouse position
        if self.left == left_ and self.top == top_:
            return
        left, top = left_, top_
        pic = pyautogui.screenshot()
        try:
            tmp = pic.crop((left - 200, top - 30, left, top))
        except:
            return
        tmp = tmp.resize((800, 120), Image.ANTIALIAS)  # for orc work well
        string = tools[0].image_to_string(tmp, lang='eng')
        str_list = list(filter(lambda s: s and s.strip(),
                               re.split('[^a-zA-Z]\s*', string)))
        if len(str_list) == 0:
            return
        string = str_list[-1]
        if len(string) <= 3:
            return
        # print(string)
        str_queue.put(string)
