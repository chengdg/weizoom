# -*- coding: utf-8 -*-

__author__ = 'chuter'


import os
import sys
import gevent
from gevent.event import Event
from gevent.queue import Queue, Empty

from threading import Thread

from task import Task
from defer import Deferred, TaskExecuteCallbackError

from core.exceptionutil import unicode_full_stack
from utils.classes_util import singleton
from watchdog.utils import watchdog_alert

class AlreadyStartError(Exception):
    pass

class AlreadyStopError(Exception):
	pass

@singleton
class Executors(object):
	has_started = False
	has_stopped = False
	is_running = False

	pending_tasks_event = Event()

	def __init__(self):
		self.deferred_queue = Queue()

	@property
	def executors_count(self):
		if not hasattr(self, '_executors_count'):
			try:
				import multiprocessing
				self._executors_count = multiprocessing.cpu_count() * 2
			except:
				self._executors_count = 4

		return self._executors_count

	def append_task(self, task):
		deferred = Deferred(task)
		self.deferred_queue.put_nowait(deferred)

		self.pending_tasks_event.set()
		return deferred

	def run_task(self, deferred):
		try:
			deferred.execute_task()
		except:
			deferred.errback()
		else:
			try:
				deferred.callback()	
			except:
				raise TaskExecuteCallbackError(u"cause:\n\t{}".format(unicode_full_stack()))

	def __executor(self, executor_id):
		while self.is_running:
			try:
				deferred = self.deferred_queue.get(timeout=1)
				print('Worker %s got task %s' % (executor_id, deferred))

				if deferred.is_canceled():
					print(deferred, ' is canceled')
					continue
					
				self.run_task(deferred)
				gevent.sleep(0)
			except Empty:
				print('waiting for task!')

				self.pending_tasks_event.clear()
				self.pending_tasks_event.wait()
			except TaskExecuteCallbackError:
				alert_msg = u"执行任务:{}失败, cause:\n{}".format(
						deferred.task.__str__(),
						unicode_full_stack()
					)
				watchdog_alert(alert_msg)

	def __run_executors(self):
		self.__executors = [
				gevent.spawn(self.__executor, "__executor{}__".format(i)) \
				for i in xrange(self.executors_count)
			]

		gevent.joinall(self.__executors)
		print 'quitting'

	def __start_executors(self):
		self.main_loop = Thread(target=self.__run_executors)
		self.main_loop.start()

	def start(self):
		if self.has_started:
			raise AlreadyStartError()

		self.is_running = True
		self.__start_executors()
		self.has_started = True

	def stop(self, graceful=True):
		if self.has_stopped:
			return
			# raise AlreadyStopError()

		self.is_running = False
		#唤醒所有等待的worker
		self.pending_tasks_event.set()
		#TODO 确保关闭

		if not graceful:
			gevent.killall(self.__executors)

		self.has_stopped = True

executors = Executors()

def stop_executors_signal_hand(*args, **kw):
	graceful = kw.get('graceful', True)
	executors.stop(graceful=graceful)
	#http://thushw.blogspot.com/2010/12/python-dont-use-sysexit-inside-signal.html
	os._exit(0)

import signal
gevent.signal(signal.SIGTERM, stop_executors_signal_hand)
gevent.signal(signal.SIGINT, stop_executors_signal_hand)

executors.start()