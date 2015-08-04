# -*- coding: utf-8 -*-

__author__ = 'chuter'

from core import dateutil

from models import *


class PvUvCount(object):
	def __init__(self, key, uv=0, pv=0):
		self.key = key
		self.uv = uv
		self.pv = pv

	def increment_pv(self):
		self.pv += 1

	def increment_uv(self):
		self.uv += 1

		
def count_visit_daily_pv_uv(webapp_id, day_date):
	#获取指定日期的当天所有访问日志信息
	visit_logs = PageVisitLog.objects.filter(webapp_id=webapp_id, create_date=day_date)

	#进行统计
	app_to_pv_uv_count = {}
	url_to_pv_uv_count = {}
	has_counted_user = {}

	for visit_log in visit_logs:
		if visit_log.webapp_id is None or visit_log.webapp_id == '':
			continue

		if app_to_pv_uv_count.has_key(visit_log.webapp_id):
			app_pv_uv_count = app_to_pv_uv_count.get(visit_log.webapp_id)
		else:
			app_pv_uv_count = PvUvCount(visit_log.webapp_id)
			app_to_pv_uv_count[visit_log.webapp_id] = app_pv_uv_count

		if url_to_pv_uv_count.has_key(visit_log.url):
			url_pv_uv_count = url_to_pv_uv_count.get(visit_log.url)
		else:
			url_pv_uv_count = PvUvCount(visit_log.url)
			url_pv_uv_count.webapp_id = visit_log.webapp_id
			url_to_pv_uv_count[visit_log.url] = url_pv_uv_count

		app_pv_uv_count.increment_pv()
		url_pv_uv_count.increment_pv()

		visit_user_token = visit_log.token
		if visit_user_token:
			uv_for_app_key = u"{}-{}".format(visit_log.webapp_id, visit_user_token)
			if not has_counted_user.has_key(uv_for_app_key):
				app_pv_uv_count.increment_uv()
				has_counted_user[uv_for_app_key] = 1

			uv_for_url_key = u"{}-{}".format(visit_log.url, visit_user_token)
			if not has_counted_user.has_key(uv_for_url_key):
				url_pv_uv_count.increment_uv()
				has_counted_user[uv_for_url_key] = 1

	#写入数据库
	for webapp_id in app_to_pv_uv_count.keys():
		statistics_record = PageVisitDailyStatistics.objects.create(
			webapp_id = webapp_id,
			url_type = URL_TYPE_ALL,
			pv_count = app_to_pv_uv_count[webapp_id].pv,
			uv_count = app_to_pv_uv_count[webapp_id].uv,
			data_date = day_date
		)

	for url in url_to_pv_uv_count.keys():
		statistics_record = PageVisitDailyStatistics.objects.create(
			webapp_id = url_to_pv_uv_count[url].webapp_id,
			url_type = URL_TYPE_SPECIFIC,
			url = url,
			pv_count = url_to_pv_uv_count[url].pv,
			uv_count = url_to_pv_uv_count[url].uv,
			data_date = day_date
		)