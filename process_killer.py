#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import exit
from time import sleep
from os import getpid, kill, remove
from signal import SIGTERM
import signal
from pathlib import Path
from threading import Thread

pid_file_path = '/tmp/youdao_translater.pid'


class ProcessKiller(Thread):
    def __init__(self, time=5):
        super().__init__()
        self.waitting = time

    def run(self):
        sleep(self.waitting)
        print('[*] trying to kill myself (pid: %s)' % getpid())
        kill(getpid(), SIGTERM)

    @staticmethod
    def _backup_code():
        pid_file = Path(pid_file_path)
        if pid_file.is_file():
            pid = open(pid_file_path).read()
            pid = int(pid)
            remove(pid_file_path)
            print('[*] trying to kill process %s' % pid)
            try:
                kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                print('[*] kill process %s fialed')
                pass
            finally:
                exit()
        else:
            print('[*] pid file do not exist')
            print('[*] start GUI')
            pid = getpid()
            with open(pid_file_path, 'w') as f:
                f.write(str(pid))
