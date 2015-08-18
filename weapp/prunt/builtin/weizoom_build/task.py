# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import os
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

import logging
logger = logging.getLogger('weizoom-build')

from prunt.decorator import register_task
from prunt.util import template_util
import prunt

from utils import resource_util

class Block(object):
	def __init__(self):
		self.lines = []

	def add_line(self, line):
		self.lines.append(line)

	def generate(self):
		return '\n'.join(self.lines)

	def dump(self):
		raise RuntimeError('subclass must implement dump method')


class TextBlock(Block):
	def dump(self):
		print '===== text block ====='


class PruntTaskBlock(Block):
	def __init__(self):
		Block.__init__(self)
		self.task_name = ''
		self.conf_dict = {}

	def set_task(self, task_name, conf_dict):
		self.task_name = task_name
		self.conf_dict = conf_dict

	def extract_file_path(self):
		paths = []
		for line in self.lines:
			line = line.strip()
			if '<!--' in line:
				continue
			if not line:
				continue

			if '.js' in line:
				if 'src="' in line:
					beg = line.find('src="')+5
					end = line.find('"', beg)
				else:
					beg = line.find("src='")+5
					end = line.find("'", beg)
				if beg == 4 or end == -1:
					logger.warn("invalid js: %s", line)
			elif '.css' in line:
				if 'href="' in line:
					beg = line.find('href="')+6
					end = line.find('"', beg)
				else:
					beg = line.find("href='")+6
					end = line.find("'", beg)
				if beg == 5 or end == -1:
					logger.warn("invalid css: %s", line)

			path = line[beg:end][1:] #去掉开始的/
			paths.append(path)
		return paths

	def generate(self):
		if self.task_name == 'weizoom-merge':
			paths = self.extract_file_path()
			self.conf_dict['files'] = {
				"src": paths
			}

		if prunt.run_task(self.task_name, self.conf_dict):
			if self.task_name == 'weizoom-merge':
				if '.js' in self.conf_dict['dest']:
					dest = '<script type="text/javascript" src="/%s"></script>' % prunt.get_last_result()
					return dest.decode('utf-8').encode('utf-8')
				elif '.css' in self.conf_dict['dest']:
					dest = '<link type="text/css" rel="stylesheet" media="all" href="/%s">' % prunt.get_last_result()
					return dest.decode('utf-8').encode('utf-8')
			elif self.task_name == 'weizoom-merge-views-dialogs':
				result = prunt.get_last_result()
				template_content = ''
				with open(result['template'], 'rb') as src_file:
					template_content = src_file.read().decode('utf-8')

				dest = u'%s\n<script type="text/javascript" src="/%s"></script>' % (template_content, result['js'].decode('utf-8'))
				return dest.encode('utf-8')
			elif self.task_name == 'weizoom-generate-component-front-template':
				dest = u'<script type="text/x-handlebar-template" id="componentTemplates">\n%s\n</script>' % prunt.get_last_result().decode('utf-8')
				return dest.encode('utf-8')
		else:
			logger.error('run task "%s" failed!!!', self.task_name)
			return ''
		
	def dump(self):
		print '===== prunt task block ====='
		print 'name: ', self.task_name
		print 'conf_dict: ', self.conf_dict


def parse_prunt_task(lines):
	items = []
	while True:
		line = lines.pop(0)
		if line.strip() == '-->':
			break
		else:
			items.append(line)

	task_info = json.loads(''.join(items))
	return task_info['task'], task_info.get('args', {})


def build(path):
	lines = []
	with open(path, 'rb') as src_file:
		for line in src_file:
			lines.append(line.rstrip())

	PRUNT_BEG_TAG = "<!-- *start_prunt_task* -->"
	PRUNT_END_TAG = "<!-- *end_prunt_task* -->"
	mode = 'text'
	blocks = []
	cur_block = TextBlock()
	while len(lines) > 0:
		line = lines.pop(0)
		stripped_line = line.strip()
		if stripped_line == PRUNT_BEG_TAG and mode == 'text':
			blocks.append(cur_block)
			cur_block = PruntTaskBlock()
			mode = 'prunt_task'
		elif stripped_line == PRUNT_END_TAG and mode == 'prunt_task':
			blocks.append(cur_block)
			cur_block = TextBlock()
			mode = 'text'
		else:
			if '[prunt_task]' in line:
				task_name, task_config_dict = parse_prunt_task(lines)
				cur_block.set_task(task_name, task_config_dict)
			else:
				cur_block.add_line(line)
	blocks.append(cur_block)

	#为每个block生成代码
	items = []
	for block in blocks:
		items.append(block.generate())
	with open('%s.result' % path, 'wb') as dst_file:
		print >> dst_file, '\n'.join(items)
	logger.info('build %s', path)


@register_task('weizoom-build')
def buildFile(prunt):
	u"""
	解析文件，执行其中定义的task
	"""
	prunt.config.require('files')
	files = prunt.config['files']
	paths = files['src'] if type(files['src']) == list else [files['src']]

	prunt.run_task('prunt-replace', {
		"files": {
			"src": "static_v2/js/termite/component/common/Component.js"
		},
		"rules": [{
			"pattern": 'default:',
			"replacement": '"default":'
		}]
	})

	for path in paths:
		build(path)
