# -*- coding: utf-8 -*-

import os
import subprocess
import shutil

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

in_dump_mode = False

class Block(object):
	def __init__(self):
		self.type = None
		self.lines = []

	def add(self, line):
		self.lines.append(line)


class TextBlock(Block):
	def __init__(self):
		Block.__init__(self)
		self.type = 'text'
		self.name = 'unknown_text'

	def dump(self):
		if in_dump_mode:
			print '[# TEXT'
		for line in self.lines:
			print line
		if in_dump_mode:
			print 'TEXT #]'

class TermiteBlock(Block):
	def __init__(self):
		Block.__init__(self)
		self.type = 'termite'
		self.blocks = []
		self.name = 'unknown_termite'
		self.name2block = {}

	def parse(self):
		block = None
		for line in self.lines:
			if 'Termite GENERATED' in line:
				continue

			if '# MODULE START:' in line:
				block = ModuleBlock()
				block.termite_block = self
				block.add(line)
			elif '# MODULE END:' in line:
				block.name = line.split(':')[1].strip()
				block.add(line)
				self.blocks.append(block)
			else:
				if block:
					block.add(line)

		for block in self.blocks:
			self.name2block[block.name] = block

	def get_module_blocks(self):
		return self.blocks

	def add_module(self, module_block):
		self.blocks.append(module_block)

	def remove_module(self, module_name):
		for block in self.blocks:
			if block.name == module_name:
				print 'remove module ', module_name
				self.blocks.remove(block)

	def dump(self):
		if in_dump_mode:
			print '[[# TERMITE'
		print self.lines[0]
		for block in self.blocks:
			block.dump()
		print self.lines[-1]
		if in_dump_mode:
			print 'TERMITE #]]'


class ModuleBlock(Block):
	def __init__(self):
		Block.__init__(self)
		self.type = 'module'
		self.termite_block = None
		self.name = 'unknown_module'

	def get_parent_termite_name(self):
		return self.termite_block.name

	def dump(self):
		if in_dump_mode:
			print '[[[# MODULE %s(%s)' % (self.name, self.termite_block.name)
		print '\n'
		for line in self.lines:
			print line
		if in_dump_mode:
			print 'MODULE %s(%s) #]]]' % (self.name, self.termite_block.name)


class SourceFile(object):
	def __init__(self, file_path):
		self.file_path = file_path
		self.blocks = self.__parse_file()
		self.name2block = dict([(block.name, block) for block in self.blocks])

	def dump(self, blocks=None):
		global in_dump_mode
		in_dump_mode = True
		if not blocks:
			blocks = self.blocks
		if in_dump_mode:
			print '\n=============== source file %s ===============' % self.file_path
		for block in blocks:
			block.dump()
		in_dump_mode = False

	def save(self):
		global in_dump_mode
		in_dump_mode = False
		f = open(self.file_path, 'wb')
		import sys
		old_stdout = sys.stdout
		sys.stdout = f
		for block in self.blocks:
			block.dump()
		sys.stdout = old_stdout
		f.close()

	def __parse_file(self):
		f = open(self.file_path)
		in_module = False
		blocks = []
		block = TextBlock()
		for line in f:
			line = line.rstrip()
			if '# Termite GENERATED START:' in line:
				blocks.append(block)
				block = TermiteBlock()
				block.add(line)
			elif '# Termite GENERATED END:' in line:
				block.add(line)
				block.name = line.split(':')[1].strip()
				blocks.append(block)
				block = TextBlock()
			else:
				block.add(line)
		f.close()

		for block in blocks:
			if block.type == 'termite':
				block.parse()

		return blocks

	def get_module_blocks(self):
		module_blocks = []
		for block in self.blocks:
			if block.type == 'termite':
				module_blocks.extend(block.get_module_blocks())

		return module_blocks

	def add_module(self, module_block):
		termite_block = self.name2block[module_block.get_parent_termite_name()]
		termite_block.add_module(module_block)

	def add_modules(self, module_blocks):
		for module in module_blocks:
			self.add_module(module)

	def remove_module(self, module):
		print 'remove module from ', self.file_path
		for block in self.blocks:
			if block.type == 'termite':
				block.remove_module(module)


class SourceFileManager(object):
	def __init__(self, app, viper_path):
		self.app = app
		self.app_dir = app
		self.viper_dir = viper_path
		self.viper_app_dir = os.path.join(viper_path, app)

	def __get_plural_name(self, name):
		if name[-1] == 's':
			return '%ses' % name
		elif name[-1] == 'y':
			return '%sies' % name[:-1]
		else:
			return '%ss' % name

	def merge_file(self, file_path):
		src = os.path.join(self.app_dir, file_path)
		dst = os.path.join(self.viper_app_dir, file_path)
		if not os.path.exists(dst):
			#直接拷贝
			print 'COPY %s to %s' % (src, dst)
			shutil.copyfile(src, dst)
		else:
			print 'merge %s to %s' % (src, dst)
			src_py = SourceFile(src)

			dst_py = SourceFile(dst)

			dst_py.add_modules(src_py.get_module_blocks())
			dst_py.save()

	def remove_module_from_file(self, file_path, module):
		dst = os.path.join(self.viper_app_dir, file_path)
		dst_py = SourceFile(dst)
		dst_py.remove_module(module)
		dst_py.save()

	def merge_python_files(self):
		self.merge_file('urls.py')
		self.merge_file('models.py')
		self.merge_file('views.py')
		self.merge_file('api_views.py')
		self.merge_file('mobile_urls.py')
		self.merge_file('mobile_views.py')

	def copy_html_files(self):
		for dirpath, dirnames, filenames in os.walk('./%s/templates' % self.app_dir):
			for filename in filenames:
				src_path = os.path.join(dirpath, filename)
				dst_path = os.path.join(self.viper_dir, dirpath, filename)

				dst_dir = os.path.dirname(dst_path)
				if not os.path.exists(dst_dir):
					os.makedirs(dst_dir)

				print 'copy file from %s to %s' % (src_path, dst_path)
				shutil.copyfile(src_path, dst_path)

	def remove_module_from_python_files(self, module):
		self.remove_module_from_file('urls.py', module)
		self.remove_module_from_file('models.py', module)
		self.remove_module_from_file('views.py', module)
		self.remove_module_from_file('api_views.py', module)
		self.remove_module_from_file('mobile_urls.py', module)
		self.remove_module_from_file('mobile_views.py', module)

	def remove_module_html_files(self, module):
		module_plural_name = self.__get_plural_name(module)
		for file_path in [
				os.path.join(self.viper_app_dir, 'templates', self.app, '%s_detail.html' % module),
				os.path.join(self.viper_app_dir, 'templates', self.app, '%s.html' % module_plural_name),
				os.path.join(self.viper_app_dir, 'templates', self.app, 'editor', '%s.html' % module_plural_name),
				os.path.join(self.viper_app_dir, 'templates', self.app, 'editor', 'edit_%s.html' % module)
			]:
			if os.path.exists(file_path):
				print 'remove html file ', file_path
				os.remove(file_path)
			else:
				print '[WARNING] no file exists: ', file_path
