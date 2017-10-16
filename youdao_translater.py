#!/usr/bin/env python3
# TODO: None

from threading import Thread
import sys

class GUI(Thread):
    def __init__(self, text):
        self.result_text = text
        super().__init__()
    def run(self):
        self.initGUI()
    def initGUI(self):
        import tkinter as tk
        from tkinter import ttk
        from tkinter import font    
        root = tk.Tk()
        root.style = ttk.Style()
        root.wm_title('Hello, world!')
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size = 20)
        default_font.configure(family="sans-serif")
        root.option_add("*font" , default_font)
        strvar = tk.StringVar()
        strvar.set('')
        
        
        label = ttk.Label(root, text = 'Input: ')
        label.grid(row = 1, column = 1, sticky = 'nsew')
        
        input_entry = ttk.Entry(root)
        input_entry.grid(row = 1, column = 2)
        input_entry.focus_set()
        
        result_label = ttk.Label(root, text = self.result_text)
        self.result_label = strvar
        result_label.grid(row = 2, column = 2)
        
        button = ttk.Button(root, text = 'Send to web', command = lambda: showWord())
        button.grid(row = 2, column = 1)
        
        def showWord(event):
            from time import sleep
            word = input_entry.get()
            if word != '':
                if self.thread == None or self.thread.isAlive() == False:
                    t = WebRequestThread(word, root, strvar)
                    self.thread = t
                    print('thread starting')
                    t.start()
                else:
                    root.destroy()
                    import sys
                    import os
                    os.remove(pid_file_path)
                    sys.exit()
        def moveWindow(event):
            import re
            width, height, x, y = [int(i) for i in re.findall(r'\d+', root.geometry())]
            if event.keysym == 'Up':
                y = int(y - height)
            elif event.keysym == 'Down':
                y = int(y + height)
            elif event.keysym == 'Left':
                x = int(x - width / 2)
            elif event.keysym == 'Right':
                x = int(x + width / 2)
                            
            root.geometry('+%d+%d' % (x, y))
            
        root.bind(sequence= '<Control-j>', func= showWord)
        root.bind(sequence= '<Return>', func= showWord)
        root.bind(sequence= '<Down>', func= moveWindow)
        root.bind(sequence= '<Up>', func= moveWindow)
        root.bind(sequence= '<Left>', func= moveWindow)
        root.bind(sequence= '<Right>', func= moveWindow)
        root.mainloop()

class ProcessKiller(Thread):
    def __init__(self, time):
        self.waitting = time
        super().__init__()
    def run(self):
        from time import sleep
        from os import getpid, kill
        from signal import SIGTERM
        sleep(self.waitting)
        print("trying kill myself (pid: %s)" % getpid())
        kill(getpid(), SIGTERM)
        
    def _backupCode(self):
        
        import os
        import os
        import signal
        from pathlib import Path
        from sys import exit
        
        pid_file = Path(pid_file_path)
        if pid_file.is_file():
            pid = open(pid_file_path).read()
            pid = int(pid)
            os.remove(pid_file_path)
            print("trying kill process %s" % pid)
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                print('kill process %s fialed')
                pass
            finally:
                exit()
        else:
            print('pid file do not exist')
            print('start GUI')
            pid = os.getpid()
            with open(pid_file_path, 'w') as f:
                f.write(str(pid))    
                 

class Clipboard():
    
    def _copy_xclip(self, text):
        import subprocess
        p = subprocess.Popen(['xclip', '-selection', 'primary', '-in'],
                             stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=text.encode('utf-8'))

    def _paste_xclip(self):
        import subprocess
        p = subprocess.Popen(['xclip', '-selection', 'primary', '-out'],
                             stdout=subprocess.PIPE, close_fds=True)
        stdout, stderr = p.communicate()
        return stdout.decode('utf-8')
    
    def copy(self, text):
        self._copy_xclip(text)
        
    def paste(self):
        return self._paste_xclip()

class Youdao:
    def __init__(self, url, key, sec):
        self.API_URL = url
        self.APP_KEY = key
        self.APP_SEC = sec
    
    def request(self, q):
        from hashlib import md5
        from random import randint
        from requests import get

        salt = str(randint(1, 100))
        appKey = self.APP_KEY
        secret = self.APP_SEC
        sign = md5((appKey + q + salt + secret).encode()).hexdigest().upper()
        
        payload = {
            'q': q,
            'from': 'auto',
            'to': 'auto',
            'appKey': appKey,
            'salt': salt,
            'sign': sign,
        }
        
        r = get(self.API_URL, params= payload)
        reval = r.json()
        
        
        if(reval['errorCode'] != '0'):
            text = '[!] API return error: %s' % reval['errorCode']
        elif 'basic' not in reval:
            text = '[!] query: %s\n' % reval['query']+ 'There has no translation for this'
        
        else: 
            text = '[*] query: %s\n' % reval['query']+ '\n'.join(reval['basic']['explains'])
            
        return text

def main():
    from sys import exit
    from time import sleep
    youdao = Youdao(API_URL, APP_KEY, APP_SEC)
    origin = Clipboard().paste()
    #origin = 'world'
    if origin == '':
        result = '[!] Get text from clipboard failed.'
    else:
        result = youdao.request(origin)
    print(result)
    ProcessKiller(wait_seconds_before_close_window).start()
    GUI(result).start()
    
    
pid_file_path = '/tmp/youdao_trasnlate.pid'
API_URL = 'http://openapi.youdao.com/api'

APP_KEY = 'your key'
APP_SEC = 'your secret'
wait_seconds_before_close_window = 5

if __name__ == '__main__':
    main()
