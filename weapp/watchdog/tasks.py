#coding:utf8
from __future__ import absolute_import

from django.conf import settings
from core.exceptionutil import full_stack

from weapp.celery import task
from .models import Message, WeappMessage
from .models import WATCHDOG_ALERT,WATCHDOG_DEBUG,WATCHDOG_EMERGENCY,WATCHDOG_ERROR,WATCHDOG_FATAL,WATCHDOG_INFO,WATCHDOG_NOTICE,WATCHDOG_WARNING
import logging

# 可以在settings中设定WATCHDOG_CONFIG，配置watchdog
CONFIG = getattr(settings, 'WATCHDOG_CONFIG', {})
TASK_CONFIG = {
	'name': 'watchdog.send'
}
TASK_CONFIG.update(CONFIG)

def _watchdog(type, message, severity=WATCHDOG_INFO, user_id='0', db_name='default'):
	"""
	watchdog : 向日志记录表添加一条日志信息
	"""
	try:
		if isinstance(user_id, int):
			user_id = str(user_id)

		if settings.WATCH_DOG_DEVICE == 'console':
			if severity == WATCHDOG_DEBUG:
				severity = 'DEBUG'
			elif severity == WATCHDOG_INFO:
				severity = 'INFO'
			elif severity == WATCHDOG_NOTICE:
				severity = 'NOTICE'
			elif severity == WATCHDOG_WARNING:
				severity = 'WARNING'
			elif severity == WATCHDOG_ERROR:
				severity = 'ERROR'
			elif severity == WATCHDOG_FATAL:
				severity = 'FATAL'
			elif severity == WATCHDOG_ALERT:
				severity = 'ALERT'
			elif severity == WATCHDOG_EMERGENCY:
				severity = 'EMERGENCY'
			else:
				severity = 'UNKNOWN'
			if not settings.IS_UNDER_BDD:
				logging.info("[%s] [%s] : %s" % (severity, type, message))
		else:
			try:
				if not settings.IS_UNDER_BDD:
					logging.info("[%s] [%s] : %s" % (severity, type, message))
				WeappMessage.objects.using(settings.WATCHDOG_DB).create(type=type, message=message, severity=severity, user_id=user_id)
				print('here111111111111111111111111111111111111111111111111111')
			except:
				print('here2222222')

				logging.error(u'>>>>>>>>>>>>>>>>> not connection operation databases settings.WATCHDOG_DB={}'.format(settings.WATCHDOG_DB))
				logging.error("Cause:\n{}".format(full_stack()))
				print 'error message==============', message
				Message.objects.create(type=type, message=message, severity=severity, user_id=user_id)
	except:
		#TODO, 通过监控和心跳来发现
		try:
			logging.error("Failed to save watchdog, type:{}, message:{}".format(type, message))
			logging.error("Cause:\n{}".format(full_stack()))
		except:
			pass


@task(**TASK_CONFIG)
def send_watchdog(level, message, severity=WATCHDOG_INFO, user_id='0', db_name='default'):
	try:
		if not settings.IS_UNDER_BDD:
			logging.info('received watchdog message: [%s] [%s]' % (level, message))
		_watchdog(level, message, severity, user_id, db_name)
	except Exception, e:
		logging.error("Failed to send watchdog message, retrying...")
		send_watchdog.retry(exc=e)
	return 'OK'
