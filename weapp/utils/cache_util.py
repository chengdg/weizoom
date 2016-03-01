# -*- coding: utf-8 -*-

__author__ = 'bert'

import logging
from time import time
import traceback
import redis
from django.core.cache import cache
from django.conf import settings

from core.exceptionutil import unicode_full_stack
from django.conf import settings


#add by likunlun
#初始化CACHE_QUERIES
try:
	CACHE_QUERIES = CACHE_QUERIES
except:
	CACHE_QUERIES = []

pyredis =redis.Redis(settings.REDIS_HOST,settings.REDIS_PORT,settings.REDIS_CACHES_DB)
def get_trace_back():
	stack_entries = traceback.extract_stack()
	stack_entries = filter(lambda entry: (('weapp' in entry[0]) and (not 'hack_django' in entry[0])), stack_entries)
	buf = []
	for stack_entry in stack_entries:
		filename, line, function_name, text = stack_entry
		formated_stack_entry = "<span>File `%s`, line %s, in %s</span><br/><span>&nbsp;&nbsp;&nbsp;&nbsp;%s</span>" % (filename, line, function_name, text)
		buf.append(formated_stack_entry)
	stack = '<br/>'.join(buf).replace("\\", '/').replace('"', "``").replace("'", '`')
	return stack

def set_cache(key, value, timeout=0):
	cache.set(key, value, timeout)

def get_cache(key):
	return cache.get(key)

def get_many(keys):
	return cache.get_many(keys)

def delete_cache(key):
	cache.delete(key)

	cache.delete("api"+key)
	logging.info("api"+key)

def delete_pattern(key):
	cache.delete_pattern(key)
	cache.delete_pattern("api"+key)
	logging.info("api"+key)


def clear_db():
	cache.clear()

def set_cache_wrapper(key, value, timeout=0):
	start = time()
	try:
		return set_cache(key, value, timeout)
	except:
		if settings.DEBUG:
			raise
		else:
			return None
	finally:
		stop = time()
		duration = stop - start
		value_type = str(type(value)).replace('<', '&lt;').replace('>', '&gt;')
		CACHE_QUERIES.append({
			'sql': 'set `cache`: {`%s`: `%s`)' % (key, value_type),
			'time': "%.3f" % duration,
			'stack': get_trace_back()
		})


def get_cache_wrapper(key):
	start = time()
	success = False
	try:
		value = get_cache(key)
		if value:
			success = True
		return value
	except:
		if settings.DEBUG:
			raise
		else:
			return None
	finally:
		stop = time()
		duration = stop - start
		CACHE_QUERIES.append({
			'sql': 'get `cache`: `%s` =&gt; %s' % (key, 'hit' if success else 'MISS!!'),
			'time': "%.3f" % duration,
			'stack': get_trace_back()
		})


def get_many_wrapper(keys):
	start = time()
	success = False
	try:
		value = get_many(keys)
		if value:
			success = True
		return value
	except:
		if settings.DEBUG:
			raise
		else:
			return None
	finally:
		stop = time()
		duration = stop - start
		CACHE_QUERIES.append({
			'sql': 'get_many from `cache`: `%s` =&gt; %s' % (keys, 'hit' if success else 'MISS!!'),
			'time': "%.3f" % duration,
			'stack': get_trace_back()
		})


def delete_cache_wrapper():
	start = time()
	try:
		return delete_cache()
	except:
		if settings.DEBUG:
			raise
		else:
			return None
	finally:
		stop = time()
		duration = stop - start
		value_type = str(type(value)).replace('<', '&lt;').replace('>', '&gt;')
		CACHE_QUERIES.append({
			'sql': 'delete `cache`: {`%s`: `%s`)' % (key, value_type),
			'time': "%.3f" % duration,
			'stack': get_trace_back()
		})


def delete_pattern_wrapper(pattern):
	start = time()
	try:
		return delete_pattern(pattern)
	except:
		if settings.DEBUG:
			raise
		else:
			return None
	finally:
		stop = time()
		duration = stop - start
		value_type = str(type(value)).replace('<', '&lt;').replace('>', '&gt;')
		CACHE_QUERIES.append({
			'sql': 'delete_pattern from `cache`: `%s`' % pattern,
			'time': "%.3f" % duration,
			'stack': get_trace_back()
		})


if settings.MODE == 'develop':
	SET_CACHE = set_cache_wrapper
	GET_CACHE = get_cache_wrapper
	DELETE_CACHE = delete_cache_wrapper
	DELETE_PATTERN = delete_pattern_wrapper
	GET_MANY = get_many_wrapper
else:
	SET_CACHE = set_cache
	GET_CACHE = get_cache
	DELETE_CACHE = delete_cache
	DELETE_PATTERN = delete_pattern
	GET_MANY = get_many


def get_from_cache(key, on_miss):
	"""
	从cache获取数据，构建对象
	"""
	obj = GET_CACHE(key)
	if obj:
		return obj
	else:
		try:
			fresh_obj = on_miss()
			if not fresh_obj:
				return None
			value = fresh_obj['value']
			SET_CACHE(key, value)
			if 'keys' in fresh_obj:
				for fresh_key in fresh_obj['keys']:
					SET_CACHE(fresh_key, value)
			return value
		except:
			if settings.DEBUG:
				raise
			else:
				print unicode_full_stack()
				return None


def get_many_from_cache(key_infos):
	keys = []
	key2onmiss = {}

	for key_info in key_infos:
		key = key_info['key']
		keys.append(key)
		key2onmiss[key] = key_info['on_miss']

	objs = GET_MANY(keys)
	for key in keys:
		if objs.get(key, None):
			continue

		on_miss = key2onmiss[key]
		if on_miss:
			fresh_obj = on_miss()
			if not fresh_obj:
				value = {}
			else:
				value = fresh_obj['value']
				SET_CACHE(key, value)
			objs[key] = value

	return objs

def get_zset_from_redis(zset_name):
	return pyredis.zrange(zset_name,0,-1)

def add_zdata_to_redis(zset_name,*args):
	return pyredis.zadd(zset_name,*args)

def rem_zset_member_from_redis(zset_name,*args):
	return pyredis.zrem(zset_name,*args)

def get_zset_count_from_redis(zset_name):
	return pyredis.zcard(zset_name)

def get_zrange_from_redis(name,  start =0, end =-1,desc=False, withscores=False,
	               score_cast_func=int):
	return pyredis.zrange(name, start, end, desc, withscores,
				   score_cast_func)

def rem_zset_member_by_patten_from_redis(zset_pattern_name,*args):
	key_list = pyredis.keys(zset_pattern_name)
	if key_list:
		for key_name in key_list:
			result = rem_zset_member_from_redis(key_name,*args)
	else:
		return 0

def rem_set_member_by_patten_from_redis(set_pattern_name,*args):
	key_list = pyredis.keys(set_pattern_name)
	if key_list:
		for key_name in key_list:
			result = rem_set_member_from_redis(key_name,*args)
	else:
		return 0

def get_set_from_redis(set_name):
	return pyredis.smembers(set_name)


def add_set_to_redis(set_name,*args):
	return pyredis.sadd(set_name,*args)

def rem_set_member_from_redis(set_name,*args):
	return pyredis.srem(set_name,*args)

def delete_redis_key(*key_name):
	return pyredis.delete(*key_name)

def add_mhash_to_redis(hash_name,mapping):
	return pyredis.hmset(hash_name,mapping)

def get_mhash_from_redis(hash_name):
	return pyredis.hgetall(hash_name)