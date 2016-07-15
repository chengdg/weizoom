# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from apps.customerized_apps.exsign import models as exsign_models
from apps.customerized_apps.mysql_models import ConsumeCouponLog

from apps.customerized_apps.sign import models as sign_models
class Command(BaseCommand):
	help = 'start exsign stats task'
	args = ''

	def handle(self, **options):
		"""
		"""
		user = User.objects.filter(username='weshop')
		if user.count() > 0:
			user = user[0]
			sign = sign_models.Sign.objects(owner_id=user.id)
			if sign.count() > 0:
				exsign = exsign_models.exSign.objects(owner_id=user.id)
				exsign_id = None
				if exsign.count() > 0:
					exsign_id = exsign[0].id
				exsign_models.exSignParticipance.objects(belong_to=str(exsign_id)).delete()
				exsign_models.exSignDetails.objects(belong_to=str(exsign_id)).delete()
				signparticipances = sign_models.SignParticipance.objects(belong_to=str(sign[0].id))
				for participance in signparticipances:
					exsign_models.exSignParticipance(
						webapp_user_id=participance.webapp_user_id,
						member_id=participance.member_id,
						belong_to=str(exsign_id) if exsign_id else participance.belong_to,
						tel=participance.tel,
						prize=participance.prize,
						created_at=participance.created_at,
						latest_date=participance.latest_date,
						total_count=participance.total_count,
						serial_count=participance.serial_count,
						top_serial_count=participance.top_serial_count,
					).save()

				signdetails = sign_models.SignDetails.objects(belong_to=str(sign[0].id))
				for detail in signdetails:
					if detail.prize["coupon"]:
						if detail.prize["coupon"]["id"]:
							detail.prize["coupon"] = [detail.prize["coupon"]]
						else:
							detail.prize["coupon"]["id"] = 0
							detail.prize["coupon"] = [detail.prize["coupon"]]
					exsign_models.exSignDetails(
						member_id=detail.member_id,
						belong_to=str(exsign_id) if exsign_id else detail.belong_to,
						created_at=detail.created_at,
						prize=detail.prize,
						type=detail.type
					).save()

				logs = ConsumeCouponLog.objects(user_id=user.id, app_name=u'sign', app_id=str(sign[0].id))
				for log in logs:
					ConsumeCouponLog(
						user_id=log.user_id,
						app_name=u'exsign',
						app_id=str(exsign_id) if exsign_id else log.app_id,
						member_id=log.member_id,
						coupon_id=log.coupon_id,
						coupon_msg=log.coupon_msg,
						created_at=log.created_at,
					).save()
		else:
			print u"没有weshop帐号"