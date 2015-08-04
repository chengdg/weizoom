# -*- coding: utf-8 -*-

import json
import os

from django.conf.urls.static import static
from django.conf.urls import patterns
from momus import views as momus_views
from momus.command import Command

ALL_URLS = []

class Line(object):
	def __init__(self, file, index, content):
		self.file = file
		self.index = index
		self.content = content

	def __unicode__(self):
		return self.content

	def __str__(self):
		return self.content

class Block(object):
	def __init__(self):
		self.lines = []
		self.type = 'block'

	@staticmethod
	def create_from(line):
		if 'Scenario:' in line:
			return Scenario()
		elif 'Context:' in line:
			return Context()
		else:
			return None

	def is_context(self):
		return False

	def add_line(self, line):
		self.lines.append(line)

	def __str__(self):
		print self.type, ' ', type(self.type)
		content = '========== %s ==========\n%s' % (self.type, '\n'.join([line.content for line in self.lines]))
		return content.encode('gbk')

	def parse(self):
		raise RuntimeError('unimplement')


class Context(Block):
	def __init__(self):
		Block.__init__(self)
		self.type = 'context'

	def is_context(self):
		return True

	def parse(self):
		json_str = '\n'.join([line.content for line in self.lines[1:-1]])
		self.data = json.loads(json_str)


class Scenario(Block):
	def __init__(self):
		Block.__init__(self)
		self.type = 'scenario'
		self.commands = []
		self.request = None
		self.process_commands = None

	def parse(self):
		buf = []
		is_enter_data = False
		is_encounter_get_or_post = False
		for line in self.lines:
			line_content = line.content
			if not is_encounter_get_or_post:
				if (not 'Get' in line_content) and (not 'Post' in line_content):
					#略去scenario中的描述
					continue
				else:
					is_encounter_get_or_post = True

			if line_content.strip().startswith('#'):
				#skip comment
				continue

			if line.content == '"""':
				if not is_enter_data:
					is_enter_data = True
					continue
				else:
					is_enter_data = False
					continue

			if is_enter_data:
				buf.append(line)
			else:
				if buf:
					command = Command.create_from(buf)
					if type(command) == list:
						self.commands.extend(command)
					else:					
						if command:
							self.commands.append(command)
					buf = [line]
				else:
					buf.append(line)

		if buf:
			command = Command.create_from(buf)
			if command:
				self.commands.append(command)

		self.request = self.commands[0]
		self.process_commands = self.commands[1:]
		assert self.request.is_request()
		assert len(self.process_commands) > 0


class Loader(object):
	def __init__(self):
		self.is_loaded = False
		self.blocks = []
		pass

	def parse(self):
		urlpatterns = []
		index_page_urlpattern = None
		for f in os.listdir('./momus/'):
			if not f.endswith('.momus'):
				continue

			block = None
			self.blocks = []
			src = open(os.path.join('./momus/', f))
			buf = []
			for index, line in enumerate(src):
				line = line.strip().decode('utf-8')
				if not line:
					continue

				if line.startswith('Scenario:') or \
					line.startswith('Context:'):
						if block:
							self.blocks.append(block)						
						block = Block.create_from(line)
				else:
					if block:
						block.add_line(Line(f, index+1, line))

			if block:
				self.blocks.append(block)

			src.close()

			for block in self.blocks:
				block.parse()

			'''
			收集url2commands
			{
				url: {
					get: get_commands,
					post: post_commands
				}
			}
			'''
			scenarios = [block for block in self.blocks if not block.is_context()]
			url2commands = {}
			for scenario in scenarios:
				url = scenario.request.url
				commands = scenario.process_commands
				if scenario.request.is_get():
					url2commands.setdefault(url, dict())['get'] = commands
				else:
					url2commands.setdefault(url, dict())['post'] = commands

			'''
			根据url2commands构造urlpatterns
			'''
			context = filter(lambda block: True if block.is_context() else False, self.blocks)[0]
			for url, type2command in url2commands.items():
				get_commands = type2command.get('get', [])
				post_commands = type2command.get('post', [])
				if url == 'momus/':
					index_page_urlpattern = (
						r'%s' % url, 
						momus_views.handle_request, 
						{'get_commands':get_commands, 'post_commands':post_commands, 'default_context':context.data}
					)
				else:
					urlpatterns.append((
						r'%s' % url, 
						momus_views.handle_request, 
						{'get_commands':get_commands, 'post_commands':post_commands, 'default_context':context.data}
					))
				ALL_URLS.append({'url':url, 'file':f})
		
		urlpatterns.append(index_page_urlpattern)
		return urlpatterns

	def check(self):
		urlpatterns = self.parse()
		print 'Validate Success! \nURLS:'
		for urlpattern in urlpatterns:
			print '\t%s' % urlpattern[0]

	def load_to(self, urlconf):
		global ALL_URLS
		urlconf_module = __import__(urlconf, {}, {}, ['*',])
		urlpatterns = self.parse()
		urlconf_module.urlpatterns += patterns('', *urlpatterns)

		#对ALL_URLS进行排序
		index_url = filter(lambda url: url['file'] == 'index.momus', ALL_URLS)[0]
		urls = filter(lambda url: url['file'] != 'index.momus', ALL_URLS)

		file2url = {}
		for url in urls:
			file2url.setdefault(url['file'], []).append(url['url'])
		urls = file2url.items()
		urls.sort(lambda x,y: cmp(x[0], y[0]))
		urls.insert(0, (index_url['file'], (index_url['url'],)))
		ALL_URLS = urls

loader = Loader()
