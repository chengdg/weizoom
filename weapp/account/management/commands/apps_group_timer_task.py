# -*- coding: utf-8 -*-

import time
from datetime import timedelta,datetime

from django.core.management.base import BaseCommand, CommandError
from core.exceptionutil import unicode_full_stack

from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning
from apps.customerized_apps.group import models as app_models
from modules.member.models import Member
from mall.order.util import update_order_status_by_group_status

class Command(BaseCommand):
	help = 'start group stats task'
	args = ''

	def handle(self, *args, **options):
		"""
		"""
		try:
			print 'group timer task start...'
			start_time = time.time()

			"""
			所有已到时间还未完成的团购，置为团购失败
			"""
			all_running_group_relations = app_models.GroupRelations.objects(group_status=app_models.GROUP_RUNNING)
			for group_relation in all_running_group_relations:
				timing = (group_relation.created_at + timedelta(days=int(group_relation.group_days)) - datetime.today()).total_seconds()
				if timing <= 0:
					group_relation.update(set__group_status=app_models.GROUP_FAILURE)
					update_order_status_by_group_status(group_relation.id,'failure')

			"""
			所有已到15分钟还未开团成功的团购，删除团购记录
			"""
			all_not_start_group_relations = app_models.GroupRelations.objects(group_status=app_models.GROUP_NOT_START)
			for group_relation in all_not_start_group_relations:
				timing_minutes = (datetime.today() - group_relation.created_at).total_seconds() / 60
				if timing_minutes >= 15 :
					group_relation.delete()

			"""
			所有已到15分钟还未完成支付的参与他人团购，删除团购参与记录
			"""
			all_unpaid_group_details = app_models.GroupDetail.objects(is_already_paid=False)
			for group_detail in all_unpaid_group_details:
				timing_minutes = (datetime.today() - group_detail.created_at).total_seconds() / 60
				if timing_minutes >= 15 :
					all_running_group_relations.get(id=group_detail.relation_belong_to).update(
						dec__grouped_number=1,
						pop__grouped_member_ids=group_detail.grouped_member_id
					)
					group_detail.delete()

			end_time = time.time()
			diff = (end_time-start_time)*1000
			print 'group timer task end...expend %s' % diff
		except:
			notify_msg = u"处理失败团购错误，cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_msg)