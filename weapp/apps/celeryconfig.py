#coding:utf8
import logging
from django.conf import settings
# This will cause your tasks to be called immediately at the point you say "task.delay(...)", so you can test the whole path (without any asynchronous behavior).
#if settings.MODE == 'develop':
# 如果需要在开发环境用同步模式，将CELERY_ALWAYS_EAGER置为True
if settings.MODE == 'develop':
	# 如果需要在开发环境用同步模式，将CELERY_ALWAYS_EAGER置为True
	CELERY_ALWAYS_EAGER = True
	BROKER_URL = 'redis://redis.weapp.com//'
	# 置为True之后，会看到worker的异常，适合调试模式
	CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
else:
	CELERY_ALWAYS_EAGER = False
	CELERY_EAGER_PROPAGATES_EXCEPTIONS = False
	BROKER_URL = 'amqp://rmq.weapp.com//'

CELERY_RESULT_BACKEND = 'redis://redis.weapp.com/3/'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
CELERYD_CONCURRENCY =  8
CELERYD_TASK_TIME_LIMIT = 60

if CELERY_ALWAYS_EAGER:
	logging.info("develop mode, no celery asynchronous behaviors")
