# -*- coding: utf-8 -*-

__author__ = 'chuter'


#dummy callback
def passthru(*arg, **kw):
	return arg, kw

class TaskExecuteCallbackError(Exception):
	pass

class TaskResult(object):
	def __init__(self):
		self._is_failed = False
		self._is_successful = True
		self._result = None

	def is_failed(self):
		return self._is_failed

	def is_successful(self):
		return self._is_successful

	@property
	def result(self):
		return self._result

	def __str__(self):
		return self._result.__str__()

	__repr__ = __str__

from core.exceptionutil import unicode_full_stack
class Failure(TaskResult):
	def __init__(self):
		super(Failure, self).__init__()
		self._is_failed = True
		self._result = unicode_full_stack()


class Success(TaskResult):
	def __init__(self, result):
		super(Success, self).__init__()
		self._is_successful = True
		self._result = result


from watchdog.utils import watchdog_fatal

#
#TODO 需要创建单独的IO Thread
#把任何的IO操作都创建为对应的Deferred然后注册
#到该IO Thread?
#
class Deferred(object):
	def __init__(self, task, canceller=None):
		if canceller is not None:
			assert callable(canceller)

		self.task = task
		self.callbacks = []
		self.err_callbacks = []
		self._canceller = canceller
		self.executed = False
		self._is_canceled = False

	def add_callbacks(self, callback, errback=None,
					callback_args=None, callback_kw=None,
					errback_args=None, errback_kw=None):
		assert callable(callback)
		assert errback == None or callable(errback)

		_callback = (callback, callback_args, callback_kw)
		_err_callback = (errback or (passthru), errback_args, errback_kw)

		if self.executed:
			if self._result.is_failed():
				self._run_errback([_err_callback])
			else:
				self._run_callback([_callback])
		else:
			self.callbacks.append(_callback)
			self.err_callbacks.append(_err_callback)

		return self

	def add_callback(self, callback, *args, **kw):
		return self.add_callbacks(callback, callback_args=args,
								 callback_kw=kw)

	def cancel(self, is_force=False):
		if this._canceller is not None:
			if is_force:
				#如果是强制取消，那么无论取消操作是否成功
				#都会进行后续的操作（认为该认为已经被取消）
				try:
					this._canceller()
				except:
					err_msg = u"取消任务({})失败，cause:\n{}".format(self.task, unicode_full_stack())
					watchdog_fatal(err_msg)
			else:
				this._canceller()

		this._is_canceled = True

	def execute_task(self):
		try:
			task_execute_result = self.task.execute()
		except:
			self._result = Failure()
		else:
			self._result = Success(task_execute_result)

		self.executed = True
		return self._result

	def is_finished(self):
		return self.executed

	def is_canceled(self):
		return self._is_canceled

	def callback(self):
		self._run_callback(self.callbacks)

	def errback(self):
		self._run_errback(self.err_callbacks)

	@property
	def result(self):
		return self._result

	def __makesure_finished(self):
		if not self.is_finished():
			raise Exception('the task not finished yet')

	def _run_callback(self, callbacks):
		self.__makesure_finished()

		for callback in callbacks:
			callback[0](self.task, self.result, callback[1], callback[2])

	def _run_errback(self, err_callbacks):
		self.__makesure_finished()

		for err_callback in err_callbacks:
			err_callback[0](self.task, self.result, err_callback[1], err_callback[2])