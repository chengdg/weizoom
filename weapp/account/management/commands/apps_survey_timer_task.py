# -*- coding: utf-8 -*-

import time
from datetime import timedelta,datetime

from django.core.management.base import BaseCommand, CommandError
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning
from apps.customerized_apps.survey import models as app_models
from modules.member.models import *


class Command(BaseCommand):
	help = 'start survey timer task'
	args = ''

	def handle(self, *args, **options):
		"""
		"""
		try:
			print ('survey timer task start...')
			start_time = time.time()

			"""
			所有未关注的会员参与调研之后，如果之后关注了，就会被分配到设定的指定分组中
			"""
			survey_log = app_models.surveyParticipanceLog.objects.all()
			survey_member_ids = [s.member_id for s in survey_log]
			members = Member.objects.filter(id__in=survey_member_ids)
			member_id2subscribe = {m.id: m.is_subscribed for m in members}
			need_clear_logs = [s for s in survey_log if member_id2subscribe[s.member_id]]
			survey_record_ids = [l.belong_to for l in need_clear_logs]
			survey_records = app_models.survey.objects.filter(id__in=survey_record_ids)
			survey_id2tag_id = {str(s.id): s.tag_id for s in survey_records}

			need_clear_log_ids = []
			for log in need_clear_logs:
				need_clear_log_ids.append(log.id)
				member = members.get(id=log.member_id)
				MemberHasTag.add_tag_member_relation(member, [survey_id2tag_id[log.belong_to]])
				if MemberHasTag.objects.filter(member=member, member_tag__name="未分组").count() > 0:
					MemberHasTag.objects.filter(member=member, member_tag__name="未分组").delete()

			#删除分组过的log
			app_models.surveyParticipanceLog.objects(id__in=need_clear_log_ids).delete()

			end_time = time.time()
			diff = (end_time-start_time)*1000
			print ('survey timer task end...expend %s' % diff)

		except Exception, e:
			print(e)
			print (u'------百宝箱调研定时任务出错--------------------------------')
			notify_msg = u"百宝箱调研定时任务出错,cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_msg)
			print (u'------百宝箱调研定时任务出错--------------------------------')