# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import os
import logging
logger = logging.getLogger('util')



def get_js_files(path):
	shouldRecord = False
	js_files = []
	for line in open(path, 'rb'):
		if '*start develop js*' in line:
			shouldRecord = True
			continue

		if '*finish develop js*' in line:
			shouldRecord = False
			continue

		if shouldRecord:
			if '<!--' in line:
				continue
				
			line = line.strip()
			if line:
				if 'src="' in line:
					beg = line.find('src="')+5
					end = line.find('"', beg)
				else:
					beg = line.find("src='")+5
					end = line.find("'", beg)
				if beg == 4 or end == -1:
					logger.warn("invalid js: %s", line)
					continue

				js = line[beg:end][1:] #去掉开始的/
				js_files.append(js)

	return js_files