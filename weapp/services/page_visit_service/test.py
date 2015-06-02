# -*- coding: utf-8 -*-

import os
import sys


#from core.exceptionutil import unicode_full_stack
#from watchdog.utils import watchdog_fatal, watchdog_notice, watchdog_warning,watchdog_error

import redis
REDIS_HOST = 'redis.weapp.com'
REDIS_PORT = 6379
REDIS_SERVICE_DB = 2

redis_cli = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_SERVICE_DB)

os.environ['DJANGO_SETTINGS_MODULE'] = 'weapp.settings'
#SERVICES_DIR = os.path.abspath(os.path.join(os.getcwd(), '..'))
WEAPP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, WEAPP_DIR)

if __name__=="__main__":
	# 构造request和args
	pass