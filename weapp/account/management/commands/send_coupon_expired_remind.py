#-*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_warning
from mall.promotion import models as promotion_models
from modules.member import module_api as member_model_api
from utils import send_mns_message as mns_utils
from weapp import settings
from weixin.user.models import ComponentAuthedAppid, ComponentAuthedAppidInfo
from market_tools.tools.template_message import models as template_message_model
from market_tools.tools.template_message import module_api as template_message_api

class Command(BaseCommand):
	help = "send coupon expired remained"
	args = ''

	def handle(self, **options):
		"""
		优惠券到期前36小时提醒用户有优惠券即将过期。
		"""
		user_ids = []
		owner_id2ahth_appid = dict()
		for component in ComponentAuthedAppid.objects.all():
			user_ids.append(component.user_id)
			owner_id2ahth_appid[component.user_id] = component

		expired_time_g = datetime.now() + timedelta(hours=36)
		expired_time_l = datetime.now() + timedelta(hours=37)

		coupons = promotion_models.Coupon.objects.filter(
			owner_id__in=user_ids,
			expired_time__gte=expired_time_g,
			expired_time__lt=expired_time_l,
			status=promotion_models.COUPON_STATUS_UNUSED
			)
		print 'has{} to be handled'.format(coupons.count())
		for coupon in coupons:
			try:
				model_data = {
					"coupon_store": u'下单即可使用',
					"coupon_rule": u'%s至%s有效' % (coupon.coupon_rule.start_date.strftime("%Y-%m-%d"), coupon.coupon_rule.end_date.strftime("%Y-%m-%d"))
				}
				if coupon.coupon_rule.valid_restrictions > -1:
					model_data["coupon_store"] = u"满%s元即可使用" % str(coupon.coupon_rule.valid_restrictions)

				print u"给用户{}发优惠券过期提醒！".format(coupon.member_id)
				new_tmpl_name = u'过期提醒'
				if mns_utils.has_new_tmpl(coupon.owner_id, new_tmpl_name):
					print 'use mns----------------'
					mp_info = ComponentAuthedAppidInfo.objects.get(auth_appid=owner_id2ahth_appid[coupon.owner_id])
					member = member_model_api.get_member_by_id(coupon.member_id)
					mns_utils.send_weixin_template_msg({
						'user_id': coupon.owner_id,
						'member_id': coupon.member_id,
						'name': new_tmpl_name,
						'url': u'{}/mall/my_coupons/?woid={}&fmt={}'.format(settings.H5_HOST, coupon.owner_id, member.token),
						'items': {
							'keyword1': mp_info.nick_name,
							'keyword2': coupon.expired_time.strftime('%Y-%m-%d %H:%M:%S')
						}
					})
				else:
					print 'use celery----------------'
					template_message_api.send_weixin_template_message(coupon.owner_id, coupon.member_id, model_data, template_message_model.COUPON_EXPIRED_REMIND)
			except:
				print unicode_full_stack()
				alert_message = u"ship_order 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
				watchdog_warning(alert_message)

		return u"Succeed in sending a hint message to members who have a coupon will expire!"