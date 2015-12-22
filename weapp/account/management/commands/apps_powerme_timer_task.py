# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils.importlib import import_module

from apps.customerized_apps.powerme import models as app_models
from modules.member.models import Member


class Command(BaseCommand):
	help = 'start powerme stats task'
	args = ''
	
	def handle(self, **options):
		print 'powerme timer task start...'
		for powerme in app_models.PowerMe.objects():
			record_id = powerme.id
			power_logs = app_models.PowerLog.objects(belong_to=record_id)
			power_member_ids = [p.power_member_id for p in power_logs]
			member_id2subscribe = {m.id: m.is_subscribed for m in Member.objects.filter(id__in=power_member_ids)}
			power_logs = [p for p in power_logs if member_id2subscribe[p.power_member_id]]
			power_log_ids = [p.id for p in power_logs]
			need_power_member_ids = [p.be_powered_member_id for p in power_logs]
			#计算助力值
			need_power_member_id2power = {}
			for m_id in need_power_member_ids:
				if not need_power_member_id2power.has_key(m_id):
					need_power_member_id2power[m_id] = 1
				else:
					need_power_member_id2power[m_id] += 1
			for m_id in need_power_member_id2power.keys():
				app_models.PowerMeParticipance.objects(belong_to=record_id,member_id=m_id).update(inc__power=need_power_member_id2power[m_id])
			#更新已关注会员的助力详情记录
			detail_power_member_ids = [p.power_member_id for p in power_logs]
			app_models.PoweredDetail.objects(belong_to=record_id, power_member_id__in=detail_power_member_ids).update(set__has_powered=True)
			#删除计算过的log
			app_models.PowerLog.objects(id__in=power_log_ids).delete()

		print 'powerme timer task end...'