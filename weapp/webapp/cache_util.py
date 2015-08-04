# -*- coding: utf-8 -*-

__author__ = 'bert'

from django.core.cache import cache
from models import *
from utils import cache_util

def get_webapp_by_appid(appid):
	key = 'webapp_appid_%s' % appid
	return cache_util.get_from_cache(key, get_webapp_from_db(appid=appid))

def get_webapp_from_db(**kwargs):
	def inner_func():
		try:
			webapp = WebApp.objects.get(**kwargs)
			return {
				'keys': [
					'webapp_appid_%s' % webapp.appid
				],
				'value': webapp
			}
		except:
			return None
	return inner_func

