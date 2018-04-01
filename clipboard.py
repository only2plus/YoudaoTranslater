#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess


class Clipboard:
    @staticmethod
    def _copy_xclip(text):
        p = subprocess.Popen(['xclip', '-selection', 'primary',
                              '-in'], stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=text.encode('utf-8'))

    @staticmethod
    def _paste_xclip():
        p = subprocess.Popen(['xclip', '-selection', 'primary',
                              '-out'], stdout=subprocess.PIPE, close_fds=True)
        stdout, stderr = p.communicate()
        return stdout.decode('utf-8')

    def copy(self, text):
        self._copy_xclip(text)

    def paste(self):
        return self._paste_xclip()
