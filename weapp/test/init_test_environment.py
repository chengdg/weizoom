# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'weapp.settings'

import sys
path = os.path.abspath(os.path.join('.', '..'))
sys.path.append(path)
path = os.path.abspath('.')
sys.path.append(path)

import unittest
import time
import selenium
from datetime import datetime

import helper

	
def init():
	print ' start init test environment '.center(100, '*')
	
	
if __name__ == "__main__":
	init()