#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
import time

from django.core.management.base import BaseCommand, CommandError

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning
from mall.promotion import models as promotion_models
from weixin.user.models import ComponentAuthedAppid
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
        for component in ComponentAuthedAppid.objects.all():
            user_ids.append(component.user_id)

        now = datetime.now()
        expired_time_g = datetime.now() + timedelta(hours=35)
        expired_time_l = datetime.now() + timedelta(hours=38)

        coupons = promotion_models.Coupon.objects.filter(
            owner_id__in=user_ids,
            expired_time__gte=expired_time_g,
            expired_time__lt=expired_time_l,
            status=promotion_models.COUPON_STATUS_UNUSED
            )

        for coupon in coupons:
            try:
                model_data = {
                    "coupon_store": u'下单即可使用',
                    "coupon_rule": u'%S至%s有效' % (coupon.coupon_rule.start_date.strftime("%Y-%m-%d"), coupon.coupon_rule.end_date.strftime("%Y-%m-%d"))
                }
                if rule.valid_restrictions > -1:
                    model_data["coupon_store"] = u"满%s元即可使用" % str(coupon.coupon_rule.valid_restrictions)

                template_message_api.send_weixin_template_message(coupon.owner_id, coupon.member_id, model_data, template_message_model.COUPON_EXPIRED_REMIND)
            except:
                alert_message = u"ship_order 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
                watchdog_warning(alert_message)

        return u"Succeed in sending a hint message to members who have a coupon will expire!"