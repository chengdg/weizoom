#coding:utf8
# bdd server相关的step

import json
import time
import base64
from datetime import datetime, timedelta
from wsgiref.simple_server import WSGIRequestHandler, make_server
from wsgiref.util import setup_testing_defaults
from cgi import parse_qs, escape

from behave import *
from test import bdd_util

from features import environment

class BDDRequestHandler(WSGIRequestHandler):
	def handle(self):
		WSGIRequestHandler.handle(self)

		if 'shutdown=1' in self.raw_requestline:
			import threading
			threading.Thread(target = self.shutdown_server()).start()

	def shutdown_server(self):
		server = self.server
		def inner_shutdown():
			server.shutdown()
			server.server_close()
			print('[bdd server] server is shutdown now!')

		return inner_shutdown


@given(u'启动BDD Server')
def step_impl(context):
	# A relatively simple WSGI application. It's going to print(out the)
	# environment dictionary after being updated by setup_testing_defaults
	def simple_app(environ, start_response):
		setup_testing_defaults(environ)

		status = '200 OK'
		headers = [('Content-type', 'text/plain')]

		start_response(status, headers)

		# the environment variable CONTENT_LENGTH may be empty or missing
		try:
			request_body_size = int(environ.get('CONTENT_LENGTH', 0))
		except (ValueError):
			request_body_size = 0

		# When the method is POST the query string will be sent
		# in the HTTP request body which is passed by the WSGI server
		# in the file like wsgi.input environment variable.
		request_body = environ['wsgi.input'].read(request_body_size)
		post = parse_qs(request_body)
		step_data = json.loads(post['data'][0])
		step = step_data['step'].strip()
		if step == '__reset__':
			print('*********************** run step **********************')
			print(u'重置bdd环境')
			environment.after_scenario(context, context.scenario)
			environment.before_scenario(context, context.scenario)
			return base64.b64encode('success')
		else:
			step = u'%s\n"""\n%s\n"""' % (step_data['step'], step_data['context'])
			print('*********************** run step **********************')
			print(step)

			try:
				context.execute_steps(u'%s\n"""\n%s\n"""' % (step_data['step'], step_data['context']))

				raw_context_kvs = context._stack[0]
				context_kvs = {}
				for k,v in raw_context_kvs.items():
					if isinstance(v, (basestring, int, float, list, dict, bool)):
						context_kvs[k] = v
				context_kvs['__is_success'] = True
			except:
				from core.exceptionutil import full_stack
				print('*********************** exception **********************')
				stacktrace = full_stack()
				print(stacktrace.decode('utf-8'))
				return base64.b64encode(stacktrace)

		# return base64.b64encode('success')

			return base64.b64encode(json.dumps(context_kvs))

	httpd = make_server('', 8170, simple_app, handler_class=BDDRequestHandler)
	print("[bdd server] Serving on port 8170...")
	httpd.serve_forever()


