# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random
import shutil
try:
    import Image
except:
    from PIL import Image
import copy
from hashlib import md5

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib import auth


VIEWFUNC2FEATURES = {}
ID2FEATURE = {}


######################################################################
# __create_feature: 创建一个feature
######################################################################
def __create_feature(features, buf):
	if (len(buf) >= 2) and ('Feature:' in buf[1]):
		feature_line = buf[1]
		feature_name = feature_line[len('Feature:'):]
		view_function = buf[0]
		id_str = (u'%s_%s' % (view_function, feature_name)).encode('utf-8')
		id = md5(id_str).hexdigest()
		buf.append('\n')

		feature = {
			"id": id,
			"name": feature_name,
			"view_function": buf[0],
			"feature_content":  '\n'.join(buf)
		}

		features.append(feature)
		ID2FEATURE[id] = feature


######################################################################
# __parse_feature_file: 读取并解析feature文件
######################################################################
def __parse_feature_file(feature_file_path):
	feature_file = open(feature_file_path, 'rb')
	lines = []
	for line in feature_file:
		lines.append(line.rstrip().decode('utf-8'))
	feature_file.close()

	features = []
	buf = []
	for line in lines:
		if 'Feature:' in line:
			#从前一个buf中获取view_function
			if len(buf) >= 1:
				view_function_line = buf[-1] #line的前一行应该是@func:行，如果不是，该Feature不处理
			else:
				view_function_line = ''
			if '@func:' in view_function_line:
				view_function = view_function_line[len('@func:'):]
				buf = buf[:-1]
			else:
				view_function = 'unknown'

			#创建feature
			__create_feature(features, buf)

			#重建buf，用于记录新的feature
			buf = []
			buf.append(view_function)

		buf.append(line)

	if len(buf) > 0:
		__create_feature(features, buf)

	return features


######################################################################
# __load_features: 加载feature文件
######################################################################
def __load_features():
	global VIEWFUNC2FEATURES
	global ID2FEATURE
	VIEWFUNC2FEATURES = {}
	ID2FEATURE = {}

	features_dir = os.path.join(settings.PROJECT_HOME, '..', 'features')
	feature_files = []
	for root, dirs, files in os.walk(features_dir):
		for file in files:
			if not file.endswith('.feature'):
				continue

			feature_files.append({
				'path': os.path.abspath(os.path.join(root, file))
			})

	for feature_file in feature_files:
		for feature in __parse_feature_file(feature_file['path']):
			VIEWFUNC2FEATURES.setdefault(feature['view_function'], []).append(feature)


######################################################################
# get_features_for_page: 获得page_id对应的feature集合
######################################################################
def get_features_for_page(page_id):
	if settings.MODE == 'develop':
		__load_features()
	else:
		if len(ID2FEATURE) == 0:
			__load_features()

	result = []
	for feature in VIEWFUNC2FEATURES.get(page_id, []):
		result.append({
			"id": feature['id'],
			"name": feature['name']
		})
	return result


######################################################################
# get_feature_content: 获得feature对应的content
######################################################################
def get_feature_content(feature_id):
	a = ID2FEATURE
	content = ID2FEATURE[feature_id]['feature_content']
	content = content.replace('<', '&lt;')\
				.replace('>', '&gt;')\
				.replace('\n', '<br/>')\
				.replace(' ', '&nbsp;')\
				.replace('\t', '&nbsp'*4)\
				.replace('Feature:', '<span class="red">Feature:</span>')\
				.replace('Background:', '<span class="red">Background:</span>')\
				.replace('Scenario:', '<span class="red">Scenario:</span>')\
				.replace('Scenario&nbsp;Outline:', '<span class="red">Scenario&nbsp;Outline:</span>')\
				.replace('Examples:', '<span class="red">Examples:</span>')\
				.replace('When', '<span class="red">When</span>')\
				.replace('Then', '<span class="red">Then</span>')\
				.replace('Given', '<span class="red">Given</span>')\
				.replace('And', '<span class="red">And</span>')
	return content;


######################################################################
# get_all_features: 获得feature对应的content
######################################################################
def get_all_features():
	viewfunc2features = {}
	for viewfunc, features in VIEWFUNC2FEATURES.items():
		for feature in features:
			obj = {
				"id": feature['id'],
				"name": feature['name']
			}
		if viewfunc in viewfunc2features:
			viewfunc2features[viewfunc].append(obj)
		else:
			viewfunc2features[viewfunc] = [obj]

	id2feature = {}
	for id, feature in ID2FEATURE.items():
		id2feature[id] = {"name": feature['name'], "view_function": feature['view_function']}

	return {
		"viewfunc2features": viewfunc2features,
		"id2feature": id2feature
	}
