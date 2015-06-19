#coding:utf8
from django.conf import settings
import logging

# This will cause your tasks to be called immediately at the point you say "task.delay(...)", so you can test the whole path (without any asynchronous behavior).
if settings.MODE == 'develop':
	# 如果需要在开发环境用同步模式，将CELERY_ALWAYS_EAGER置为True
	CELERY_ALWAYS_EAGER = True
	BROKER_URL = 'redis://redis.weapp.com//'
	# 置为True之后，会看到worker的异常，适合调试模式
	CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
	
	#from kombu.log import LOG_LEVELS
	#CELERYD_LOG_LEVEL = LOG_LEVELS['DEBUG']
	#BROKER_URL = 'amqp://rmq.weapp.com//'
	#CELERY_ALWAYS_EAGER = False
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
CELERYD_CONCURRENCY =  15


#CELERY_ROUTES = {
#	'tasks.add': 'low-priority',
#}

if CELERY_ALWAYS_EAGER:
	logging.info("develop mode, no celery asynchronous behaviors")

from kombu import Queue, Exchange
#CELERY_DEFAULT_QUEUE = "weapp_default"
#CELERY_DEFAULT_ROUTING_KEY = 'default'


CELERY_QUEUES = (
	#Queue('default', Exchange('default'), routing_key='default'),
	#Queue('services', Exchange('services'), routing_key='services.#'),
	#Queue('watchdog', Exchange('watchdog'), routing_key='watchdog.#')
	Queue('default', Exchange('default'), routing_key='default'),
	Queue('services', routing_key='services.#'),
	Queue('watchdog', routing_key='watchdog.#')
)
CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'default'


"""
CELERY_QUEUE = (
	Queue('default', Exchange('default'), routing_key='default'),
)
"""

"""
CELERY_QUEUES = {
	"weapp_default": {
		"exchange": CELERY_DEFAULT_QUEUE,
		"exchange_type": "direct",
		"routing_key": CELERY_DEFAULT_QUEUE
	},
	"watchdog_queue": {
		"routing_key": "watchdog.#",
		"exchange": "watchdog_queue",
		"exchange_type": "direct",
	}
}
"""
