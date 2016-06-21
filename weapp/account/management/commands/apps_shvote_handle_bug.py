# -*- coding: utf-8 -*-

import time

from django.core.management.base import BaseCommand

from apps.customerized_apps.shvote import models as app_models
from mall import models as mall_models


class Command(BaseCommand):
	help = ''
	args = ''
	
	def handle(self, *args, **options):
		"""
		处理由于投票活动结束后任然可以继续投票导致的数据问题
		处理方案：将details记录中超出活动截止日期的投票除去
		@param args:
		@param options:
		@return:
		"""
		print 'handle bug start...'
		start_time = time.time()
		records = app_models.Shvote.objects(status=app_models.STATUS_STOPED)
		records_id2endtime = {str(r.id): r.end_time for r in records}
		record_ids = records_id2endtime.keys()
		need_mins = dict()
		details = app_models.ShvoteDetail.objects(belong_to__in=record_ids)
		for detail in details:
			record_id = detail.belong_to
			member_id = detail.vote_to_member_id
			record_end_time = records_id2endtime.get(record_id)
			if detail.created_at > record_end_time:
				if not need_mins.has_key(record_id):
					need_mins[record_id] = {
						member_id: 1
					}
				else:
					if not need_mins[record_id].has_key(member_id):
						need_mins[record_id][member_id] += 1
					else:
						need_mins[record_id][member_id] = 1

		member_infos = app_models.ShvoteParticipance.objects(belong_to__in=record_ids, is_use=True, status=1)
		for member_info in member_infos:
			belong_to = member_info.belong_to
			member_id = str(member_info.id)
			if need_mins.get(belong_to, None) and need_mins[belong_to].get(member_id, None):
				print 'need handle: %s'
				member_info.count -= need_mins[belong_to].get(member_id, 0)
				member_info.save()
		end_time = time.time()
		diff = (end_time-start_time)*1000
		print 'handle bug  end...expend %s' % diff