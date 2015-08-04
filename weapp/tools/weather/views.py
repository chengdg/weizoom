# -*- coding: utf-8 -*-

__author__ = "liupeiyu"

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q
import httplib

from core.jsonresponse import JsonResponse, create_response, decode_json_str
from core import dateutil
from core.exceptionutil import full_stack

from tools.models import *
from watchdog.utils import watchdog_fatal

WATCHDOG_TYPE = 'WHETHER_API'

########################################################################
# get_weather_info: 获得天气信息
########################################################################
def get_weather_info(request):
	weathers = Weather.objects.all()
	response = create_response(200)
	city_code = "101180801"
	morning_time = 6    # 早晨时间
	night_time = 18     # 晚上时间

	today_date = datetime.now()
	try:
		if weathers.count() == 0:
			weather_info, weather = __get_weather_info(city_code)
		else:
			weather = weathers[0]
			if __is_out_time_span(weather.update_time, weather.update_span):
				weather_info, weather = __get_weather_info(city_code, weather_id=weather.id)
			else:
				weather_info = json.loads(weather.info)

		response.data.weather_info = weather_info
		response.data.today_date = today_date.strftime("%Y年%m月%d日")
		response.data.create_time = weather.update_time.strftime("%Y年%m月%d日 %H:%M")

		# 计算白天还是晚上，True为白天，False为晚上
		hour = int(weather.update_time.strftime("%H"))
		if morning_time <= hour and hour < night_time:
			response.data.is_daytime = True
		else:
			response.data.is_daytime = False

		# 当前温度
		response.data.current_temp = __get_current_temp(city_code)
	except:
		response = create_response(500)
		response.errMsg = u'获取失败'
		response.innerErrMsg = full_stack()
		watchdog_fatal(u'代码错误！%s' % response.innerErrMsg, WATCHDOG_TYPE)

	return response.get_response()


########################################################################
# __get_weather_info: 获取近6天气信息
########################################################################
def __get_weather_info(city_code, weather_id = 0):
	data_str, error_info = __get_http_response_data("m.weather.com.cn", "/data/%s.html" % city_code)
	weather_info = []
	weather = None
	if data_str:
		info_json = decode_json_str(data_str)
		weather_json = info_json['weatherinfo']

		# 计算周几
		weeks = [u'一', u'二', u'三', u'四', u'五', u'六', u'日']
		week_index = __get_week_index(weeks, weather_json['week'])

		# 获取今天日期
		today_date = datetime.now()
		total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), '6', 6)
		date_list = dateutil.get_date_range_list(datetime.date(today_date), high_date)

		for i in range(1,7):
			data = dict()
			data['date'] = date_list[i-1].strftime("%Y年%m月%d日")
			data['weather'] = weather_json['weather%d' % i]
			data['temp'] = weather_json['temp%d' % i]
			data['week'] = u'周%s' % weeks[week_index]
			# 给week赋值下标
			week_index = week_index + 1 if week_index + 1 < len(weeks) else 0
			weather_info.append(data)

		# 判断是否已经添加过数据，如果添加过就修改
		if weather_id:
			weather = Weather.objects.get(id=weather_id)
			weather.info = json.dumps(weather_info)
			weather.update_time = today_date
			weather.save()
		else:
			weather = Weather.objects.create(info=json.dumps(weather_info), city_code = city_code)
	else:
		if weather_id:
			weather = Weather.objects.get(id=weather_id)
			weather_info = json.loads(weather.info)
			# print u'更新数据,天气的api不可用！'
			watchdog_fatal(u'更新数据,天气的api不可用！%s' % error_info, WATCHDOG_TYPE)
		else:
			# print u'首次获取数据,天气的api不可用！'
			watchdog_fatal(u'首次获取数据,天气的api不可用！%s' % error_info, WATCHDOG_TYPE)
	return weather_info, weather


########################################################################
# __get_current_temp: 获取当前天气温度
########################################################################
def __get_current_temp(city_code):
	data_str, error_info = __get_http_response_data("www.weather.com.cn", "/data/sk/%s.html" % city_code)
	temp = ''
	if data_str:
		info_json = decode_json_str(data_str)
		# 当前温度
		temp = info_json['weatherinfo']['temp']
	else:
		# print u'获取当前天气温度,天气的api不可用！'
		watchdog_fatal(u'获取当前天气温度,发送请求失败！%s' % error_info, WATCHDOG_TYPE)
	return temp


########################################################################
# __is_out_time_span: 判断时间是否超出时间间隔
########################################################################
def __is_out_time_span(update_time, update_span):
	update_span = update_span * 60 * 1000
	create_time = long(time.mktime(update_time.timetuple()))*1000
	now = long(time.time()) * 1000
	if now-create_time > update_span:
		return True
	else:
		return False


########################################################################
# __get_http_response_data: 发送http请求，返回数据
########################################################################
def __get_http_response_data(domain, url, method="GET"):
	error_info = None
	conn = httplib.HTTPConnection(domain)
	try:
		conn.request(method, url)
		r1 = conn.getresponse()
		print r1.status
		if r1.status is not 200:
			error_info = r1.read()
			data_str = None
		else:
			data_str = r1.read()
	except:
		data_str = None
		error_info = full_stack()
	finally:
		conn.close()
	return data_str, error_info


########################################################################
# __get_week_index: 获取周期下标
########################################################################
def __get_week_index(weeks, string):
	string = string[-1:]
	for i in range(len(weeks)):
		if weeks[i] == string:
			return i