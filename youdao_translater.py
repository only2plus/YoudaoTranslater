#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
import tkinter as tk
from tkinter import ttk, font
from screenshot import CaptureMousePic, str_queue
import re
from process_killer import ProcessKiller
from clipboard import Clipboard
from youdao import Youdao


class GUI(Thread):
    def __init__(self, text):
        super().__init__()
        self.result_text = text
        self.c = None

    def run(self):
        self.init()

    def init(self):
        root = tk.Tk()
        root.wm_title('Hello PY!')
        root.wm_attributes('-topmost', 1)  # top window
        default_font = font.nametofont('TkDefaultFont')
        default_font.configure(size=17, family='sans-serif')
        root.option_add('*font', default_font)

        button = ttk.Button(root, text='Send', width=4,
                            command=lambda: send_word())
        button.grid(row=0, column=1, sticky='W', padx=5, pady=5)

        # is_capture.get enable -> 1, disable -> 0
        is_capture = tk.IntVar()
        check = tk.Checkbutton(root, text="⊙", variable=is_capture, command=lambda: mouse_wait_capture())
        check.grid(row=0, column=2, sticky='W', padx=5, pady=5)

        input_entry = ttk.Entry(root, width=12, textvariable=tk.StringVar())
        input_entry.grid(row=0, column=0, sticky='W', padx=5)
        input_entry.focus_set()

        text = tk.StringVar()
        text.set(self.result_text)
        result_label = tk.Label(root, textvariable=text)
        result_label.grid(row=1, columnspan=3)

        c = [CaptureMousePic()]
        def mouse_wait_capture(*args):
            if is_capture.get() == 1:
                c[0].start()
                Thread(target=capture).start()
            else:
                c[0].stop()
                c[0] = CaptureMousePic()

        def capture():
            while True:
                if c[0].isAlive():
                    result = Youdao().request(str_queue.get())
                    text.set(result)
                else:
                    break

        def send_word(*args):
            button['state'] = 'disabled'
            word = input_entry.get()
            if len(word) > 0:
                result = Youdao().request(word)
                text.set(result)
            button['state'] = 'normal'

        def move_window(event):
            width, height, x, y = [
                int(i) for i in re.findall(r'\d+', root.geometry())]
            if event.keysym == 'Up':
                y = int(y - height)
            elif event.keysym == 'Down':
                y = int(y + height)
            elif event.keysym == 'Left':
                x = int(x - width / 2)
            elif event.keysym == 'Right':
                x = int(x + width / 2)
            root.geometry('+%d+%d' % (x, y))

        def _quit(*args):
            root.quit()

        root.bind(sequence='<Control-s>', func=send_word)
        root.bind(sequence='<Control-q>', func=_quit)
        root.bind(sequence='<Return>', func=send_word)
        root.bind(sequence='<Down>', func=move_window)
        root.bind(sequence='<Up>', func=move_window)
        root.bind(sequence='<Left>', func=move_window)
        root.bind(sequence='<Right>', func=move_window)
        root.mainloop()


def main():
    origin = Clipboard().paste()
    # origin = 'world'
    if origin == '':
        result = '[!] Get text from clipboard failed.'
    else:
        result = Youdao().request(origin)
    print(result)
    GUI(result).start()


if __name__ == '__main__':
    main()
