#coding:utf8
"""@package services.daily_page_visit_statistic_service.tasks
每日凌晨调用，计算上一天的pv和uv的统计值

@args: 消息中指定的日期
"""

from celery import task

#@task(name="daily_page_visit_statistic_service")
@task
def daily_page_visit_statistic_service(request0, args):
	"""
	计算上一天的pv和uv的统计值的异步task
	
	@param args string类型，指定日期
	"""
	from webapp import statistics_util
	from account import models as account_models
	date = args
	for user_profile in account_models.UserProfile.objects.all():
		if not user_profile.is_active:
			continue
		statistics_util.count_visit_daily_pv_uv(user_profile.webapp_id, date)
	return "OK"
