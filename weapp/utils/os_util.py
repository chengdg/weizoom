# -*- coding: utf-8 -*-

__author__ = 'chuter'


import platform

def is_windows():
    return 'Windows' == platform.system()

def is_linux():
    return 'Linux' == platform.system()