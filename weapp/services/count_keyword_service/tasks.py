#coding:utf8
"""@package services.start_promotion_service.tasks
start_promotion_service 的Celery task实现

"""
import time

from celery import task

from core.dateutil import get_previous_date
from core.exceptionutil import unicode_full_stack
from datetime import timedelta
import datetime

from weixin2.models import *


@task
def count_keyword(request, args):
	"""
	统计用户发送的关键词数

	@param request 无用，为了兼容
	@param args dict类型
	"""
	print 'start service count_keyword {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	hour = int(datetime.now().strftime('%M'))
	if hour == 0:
		print 'count yesterday first {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		yesterday = _get_yesterday()
		_count(yesterday)

	print 'count today {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	today = time.strftime("%Y-%m-%d")
	_count(today)
	return 'OK {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def _count(date):
	records = KeywordCount.objects.filter(date=date)

	keyword_histories = KeywordHistory.objects.filter(date=date)
	keyword2user2count = {}
	for keyword_hisyory in keyword_histories:
		keyword = keyword_hisyory.keyword
		user_id = keyword_hisyory.owner_id
		if not keyword2user2count.has_key(keyword):
			keyword2user2count[keyword] = {}

		if not keyword2user2count[keyword].has_key(user_id):
			keyword2user2count[keyword][user_id] = 1
		else:
			keyword2user2count[keyword][user_id] += 1

	#先清空当天旧数据
	KeywordCount.objects.filter(date=date).delete()
	
	for keyword in keyword2user2count:
		for user_id in keyword2user2count[keyword]:
			count = keyword2user2count[keyword][user_id]
			KeywordCount.objects.create(date=date, owner_id=user_id, keyword=keyword, count = count)

def _get_yesterday():
	today = datetime.date.today() 
	oneday = datetime.timedelta(days=1) 
	yesterday = today - oneday  
	return time.strftime("%Y-%m-%d", yesterday)