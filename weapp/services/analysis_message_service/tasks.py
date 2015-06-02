#coding:utf8
"""@package services.start_promotion_service.tasks
start_promotion_service 的Celery task实现

"""
import time

from celery import task

from core.dateutil import get_previous_date
from core.exceptionutil import unicode_full_stack
from datetime import datetime, timedelta

from weixin2.models import *


@task
def analysis_message(request, args):
	"""
	统计微信消息数据：接收消息数、发送消息数、互动人数、互动次数

	@param request 无用，为了兼容
	@param args dict类型
	"""
	#MessageAnalysis
	print 'start service analysis_message {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	mpuser2user = _get_mpuser2user()
	
	previous_date = get_previous_date('today', 0)
	start_date = previous_date + ' 00:00:00'
	end_date = previous_date + ' 23:59:59'
	
	print 'analysis messages from {} to {}'.format(start_date, end_date)
	messages = Message.objects.filter(weixin_created_at__gte=start_date, weixin_created_at__lte=end_date)
	statistics = {}
	analysised_fans = []
	for message in messages:
		try:
			owner_id = mpuser2user[message.mpuser_id].owner_id
		except:
			print 'get owner_id exception for message {}'.format(message.id)
			continue
		
		analysis_date = message.weixin_created_at.strftime("%Y-%m-%d")
		statistic_key = str(owner_id) + '_' + analysis_date
		if not statistics.has_key(statistic_key):
			statistics[statistic_key] = {'receive_count':0, 'send_count':0, 'interaction_user_count':0}
		date_statistic = statistics[statistic_key]
		
		fans_username = message.from_weixin_user_username
		if message.is_reply:
			date_statistic['send_count'] += 1
		else:
			date_statistic['receive_count'] += 1
			if fans_username not in analysised_fans:
				date_statistic['interaction_user_count'] += 1
				analysised_fans.append(fans_username)
	
	for key in statistics:
		date_statistic = statistics[key]
		date_statistic['interaction_count'] = date_statistic['send_count'] + date_statistic['receive_count']
		try:
			key_items = key.split('_')
			MessageAnalysis.objects.filter(owner_id = key_items[0], date_time = previous_date).delete()
			
			MessageAnalysis.objects.create(owner_id = key_items[0], receive_count = date_statistic['receive_count'],
				send_count = date_statistic['send_count'], interaction_user_count = date_statistic['interaction_user_count'],
				interaction_count = date_statistic['interaction_count'], date_time = key_items[1])
		except:
			pass
	
	print statistics
	return "OK"

def _get_mpuser2user():
	"""获取系统绑定账号mpuser和系统账号user对应关系"""
	mpusers = WeixinMpUser.objects.all()
	mpuser2user = {}
	for mpuser in mpusers:
		mpuser_id = mpuser.id
		if mpuser2user.has_key(mpuser_id):
			continue
		mpuser2user[mpuser_id] = mpuser
	
	return mpuser2user