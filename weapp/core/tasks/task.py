# -*- coding: utf-8 -*-

__author__ = 'chuter'


"""
任务的描述
 @param runner 任务的实际执行者
"""
class Task(object):
	task_id = 0
	lock = Lock()

	def __init__(self, runner, *task_args, **task_kw):
		assert callable(runner)

		self.runner = runner
		self.task_args = task_args
		self.task_kw = task_kw

		self.name = self.__generate_name()

	def __generate_name(self):
		from gevent.threading import Lock
		Task.lock.acquire()
		Task.task_id += 1
		_task_id = Task.task_id
		Task.lock.release()

		return "task_{}".format(_task_id)

	def execute(self):
		self.runner(*self.task_args, **self.task_kw)

	def __str__(self):
		return u"task({}) runner:'{}', args:'{}', kw:'{}'"\
			.format(self.name, self.runner.__name__, self.task_args, self.task_kw)
