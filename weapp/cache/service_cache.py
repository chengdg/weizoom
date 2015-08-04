# -*- coding: utf-8 -*-
"""@package cache.service_cache
服务 状态, 响应，性能，　剖析　数据　缓存／存储　接口

BDD feature: `user_center_cache.feature`

"""

__author__ = 'abael'

import logging,re, redis
from django.conf import settings
from django.core.cache import parse_backend_conf

log = logging.getLogger('weapp.service_cache')

redis_loc = None
redis_args = []

# 获取配置中 Redis 访问Client
try:
    cls, location, args = parse_backend_conf('redis')
    if location and location.lower().find('redis')>-1:
        redis_loc = location
        redis_args = args
except:
    try:
        cls, location, args = parse_backend_conf('default')
        if location and location.lower().find('redis')>-1:
            redis_loc = location
            redis_args = args
    except:
        pass
# 没有找到
if redis_loc is None:
    log.error('Redis required for service caching !')
    sys.exit(-1)

locdic = (lambda s: s and s.groupdict() or None)(re.match('((?P<scheme>redis)\:\/\/)?(?P<host>[^\:]{5,})(:(?P<port>[0-9]+)?)', redis_loc, re.I))
if locdic is None or not locdic.has_key('host'): 
    log.error('Redis location invalid !')
    sys.exit(-1)

sredis = redis.StrictRedis(host=locdic['host'], port= (locdic.has_key('port') and int(locdic['port']) or  6379))


def set_service_time(url, time_pair):
    p = sredis.pipeline()
    p.lpush(url, time_pair)
    p.ltrim(url, 0, 1000)
    p.execute()


def get_service_time(url, start, end):
    p = sredis.pipeline()
    p.lrange(url, start, end)
    p.execute()

def get_service_urls(pattern):
    urls = p.keys(pattern)
    return urls
