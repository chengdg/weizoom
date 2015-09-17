# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
import sys
import upyun
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

import wapi as resource

product = resource.get('mall', 'product', {
	"id": 100
})
print product

product = resource.get('mall', 'product', {
	
})
print product
