# -*- coding: utf-8 -*-

import json
import os
import re

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.conf.urls.static import static
from django.conf.urls import patterns
from django.template.loader import get_template

from core.jsonresponse import JsonResponse, create_response
from momus import views as momus_views
from momus.store import store

class Command(object):
	name2class = dict()

	def __init__(self, cmd_content, cmd_data):
		self.type = 'command'
		self.content = cmd_content
		if cmd_data:
			self.raw_data_str = ''.join(cmd_data)
			try:
				self.data = json.loads(''.join(cmd_data))
			except:
				raise RuntimeError('invalid json data')
		else:
			self.raw_data_str = ''
			self.data = None

	def is_request(self):
		return False

	def get_query_options(self, request):
		condition = self.data.get('condition', None)
		if condition:
			filter = {}
			for key, value in condition.items():
				if key == 'id':
					key = '_id'
				
				if value.startswith('GET.'):
					qs_key = value[4:]
					value = request.GET[qs_key]
				elif value.startswith('POST.'):
					qs_key = value[5:]
					value = request.POST[qs_key]

				value = str(value)

				filter[key] = value
			options = {"filter":filter}
		else:
			options = {}

		return options

	def __str__(self):
		if self.data:
			data = self.data
		else:
			data = 'None'
		return '***** COMMAND(%s) *****\ncontent: %s\ndata: %s' % (self.type, self.content, str(data))

	@staticmethod
	def create_from(lines):
		if type(lines) == list:
			line_index = lines[0].index
			momus_file = lines[0].file
			cmd_line = lines[0].content
			data = ''.join([line.content for line in lines[1:]])
		else:
			line_index = lines.index
			momus_file = lines.file
			cmd_line = lines.content
			data = None

		cmd_items = cmd_line.split(' ')
		if len(cmd_items) > 2:
			cmd_type = cmd_items[0]
			cmd_content = ' '.join(cmd_items[1:])
		elif len(cmd_items) == 2:
			cmd_type, cmd_content = cmd_items
		else:
			cmd_type = cmd_items[0]
			cmd_content = 'None'
		cmd_type = cmd_type.strip().lower()
		cmd_content = cmd_content.strip()

		return Command.create_command(momus_file, line_index, cmd_type, cmd_content, data)

	@staticmethod
	def register(cmd_name, cmd_class, *extra_classes):
		if extra_classes:
			classes = [cmd_class]
			classes.extend(*extra_classes)
			Command.name2class[cmd_name] = classes
		else:
			Command.name2class[cmd_name] = cmd_class


	@staticmethod
	def create_command(momus_file, line_index, cmd_type, cmd_content, data):
		cls = Command.name2class.get(cmd_type, None)
		if not cls:
			raise RuntimeError('[%s:%d]: no class for command : %s' % (momus_file, line_index, cmd_type))

		try:
			if type(cls) == list:
				cls_list = cls
				commands = []
				for cls in cls_list:
					commands.append(cls(cmd_content, data))
				return commands
			else:
				return cls(cmd_content, data)
		except Exception, e:
			import sys
			message = '[%s:%d] when process command "%s": %s' % (momus_file, line_index, cmd_type, e.message)
			raise type(e), type(e)(message), sys.exc_info()[2]


def command(cmd_name, *extra_classes):
	def inner_func(cmd_class):
		if extra_classes:
			Command.register(cmd_name, cmd_class, extra_classes)
		else:
			Command.register(cmd_name, cmd_class)
	return inner_func


@command('return')
class Return(Command):
	def __init__(self, cmd_content, cmd_data):
		Command.__init__(self, cmd_content, cmd_data)
		self.type = 'Return'

	def create_context_data(self, default_context, exec_context):
		context_data = dict()
		context_data.update(default_context)

		if '${' in self.raw_data_str:
			#替换context_data中的变量
			tmpl = re.sub(r'"\${([^}]+)}"', r'%(\1)s', self.raw_data_str)
			variables = exec_context['variables']
			for key in variables:
				variables[key] = json.dumps(variables[key])
			real_cmd_data = json.loads(tmpl % variables)

			context_data.update(real_cmd_data.get('data', {}))
		else:
			context_data.update(self.data.get('data', {}))

		return context_data

	def __call__(self, request, default_context, last_command_result, exec_context):
		response_type = self.data['type']
		if response_type == 'html':
			template_path = self.data['template']
			context_data = self.create_context_data(default_context, exec_context)
			print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
			print request.path
			print template_path

			if template_path == '$url_list':
				template_path = 'momus/momus_urls.html'
				context_data = self.create_context_data(default_context, exec_context)
				from momus.loader import ALL_URLS
				context_data.update({
					'url_infos': ALL_URLS
				})

			print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
			print template_path
				
			template = get_template(template_path)
			if 'request_data' in context_data:
				for key, value in context_data['request_data'].items():
					setattr(request, key, value)
			context = RequestContext(request, context_data)
			return HttpResponse(template.render(context))
		else:
			data = self.data['data']
			response = create_response(200)
			response.data = self.data['data']
			return response.get_response()


class AssertPostData(Command):
	def __init__(self, cmd_content, cmd_data):
		Command.__init__(self, cmd_content, cmd_data)
		self.type = 'AssertPostData'

	def __call__(self, request, default_context, last_command_result, exec_context):
		for key in self.data:
			if not key in request.POST:
				raise RuntimeError('"%s" must be in request.POST' % key)

		return None


@command('save')
class Save(Command):
	def __init__(self, cmd_content, cmd_data):
		Command.__init__(self, cmd_content, cmd_data)
		self.type = 'Save'
		#table的格式为T{products}，要获取products, 需要[2:-1]
		hint = '\nInvalid Save command. \nCommand Format: \nSave to T{table}'
		try:
			_, table = cmd_content.split(' ')
			if not 'T{' in table:
				raise
			self.table = str(cmd_content.split(' ')[1][2:-1])
		except:
			raise RuntimeError(hint)

	def __call__(self, request, default_context, last_command_result, exec_context):
		data = {}
		for key, value in request.POST.items():
			data[key] = value

		store.save_record(self.table, request.user.id, data)


@command('readmany')
class ReadMany(Command):
	def __init__(self, cmd_content, cmd_data):
		Command.__init__(self, cmd_content, cmd_data)
		self.type = 'ReadMany'
		#命令格式为: ReadMany from T{products} to ${products}
		hint = '\nInvalid ReadMany command. \nCommand Format: \nReadMany from T{table} to ${variable}\n\t"""\n\t{"default":"..."}\n\t"""'
		try:
			_, table, _, variable = cmd_content.split(' ')
			if (not 'T{' in table) or (not '${' in variable):
				raise RuntimeError(hint)
			self.table = table[2:-1]
			self.variable = variable[2:-1]
		except:
			raise RuntimeError(hint)

		if (not self.data) or (not self.data.get('default', None)):
			raise RuntimeError(hint)

	def __call__(self, request, default_context, last_command_result, exec_context):
		total_count, records = store.get_records(self.table, request.user.id, self.get_query_options(request))
		if not records:
			records = self.data.get('default', [])
		exec_context.setdefault('variables', dict())[self.variable] = records


@command('read')
class Read(Command):
	def __init__(self, cmd_content, cmd_data):
		Command.__init__(self, cmd_content, cmd_data)
		self.type = 'Read'
		#命令格式为: Read from T{products} to ${products}
		hint = '\nInvalid Read command. \nCommand Format: \nReadMany from T{table} to ${variable}\n\t"""\n\t{"condition":"...", "default":"..."}\n\t"""'
		try:
			_, table, _, variable = cmd_content.split(' ')
			if (not 'T{' in table) or (not '${' in variable):
				raise RuntimeError(hint)
			self.table = table[2:-1]
			self.variable = variable[2:-1]
		except:
			raise RuntimeError(hint)

		if (not self.data) or (not self.data.get('condition', None)) or (not self.data.get('default', None)):
			raise RuntimeError(hint)

	def __call__(self, request, default_context, last_command_result, exec_context):
		total_count, records = store.get_records(self.table, request.user.id, self.get_query_options(request))
		if not records:
			records = [self.data.get('default', []),]
		exec_context.setdefault('variables', dict())[self.variable] = records[0]


@command('delete')
class Delete(Command):
	def __init__(self, cmd_content, cmd_data):
		Command.__init__(self, cmd_content, cmd_data)
		self.type = 'Delete'
		#命令格式为: Read from T{products}
		hint = '\nInvalid Delete command. \nCommand Format: \nDelete from T{table}\n\t"""\n\t{"condition":"..."}\n\t"""'
		try:
			_, table = cmd_content.split(' ')
			if (not 'T{' in table):
				raise
			self.table = table[2:-1]
		except:
			raise RuntimeError(hint)

		if (not self.data) or (not self.data.get('condition', None)):
			raise RuntimeError(hint)

	def __call__(self, request, default_context, last_command_result, exec_context):
		options = self.get_query_options(request)
		record_id = options['filter']['_id']
		store.remove_record(self.table, record_id)


@command('redirect')
class Redirect(Command):
	def __init__(self, cmd_content, cmd_data):
		Command.__init__(self, cmd_content, cmd_data)
		self.type = 'Redirect'
		self.url = cmd_content

	def __call__(self, request, default_context, last_command_result, exec_context):
		return HttpResponseRedirect(self.url)


class Request(Command):
	def __init__(self):
		self.type = 'Request'

	def is_request(self):
		return True

	def is_get(self):
		return False


@command('get')
class Get(Request):
	def __init__(self, cmd_content, cmd_data):
		Command.__init__(self, cmd_content, cmd_data)
		self.type = 'Get'
		self.url = cmd_content.split('?')[0][1:]

	def is_get(self):
		return True


@command('post', AssertPostData)
class Post(Request):
	def __init__(self, cmd_content, cmd_data):
		Command.__init__(self, cmd_content, cmd_data)
		self.type = 'Post'
		self.url = cmd_content[1:]

