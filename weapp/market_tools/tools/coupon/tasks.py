# -*- coding: utf-8 -*-

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_info
from market_tools.tools.template_message import models as template_message_model
from market_tools.tools.template_message import module_api as template_message_api
from celery import task

@task
def send_message_to_member(rule, member_id):
    #给用户发优惠券提示
    try:
        model_data = {
            "coupon_store": u'全部可用',
            "coupon_rule": u'不限'
        }
        if rule.limit_product:
            model_data["coupon_store"] = u'单个商品可用'
        if rule.valid_restrictions > -1:
            model_data["coupon_rule"] = "每笔订单满%s元即可使用本券" % str(rule.valid_restrictions)
        template_message_api.send_weixin_template_message(rule.owner_id, member_id, model_data, template_message_model.COUPON_ARRIVAL_NOTIFY)
    except:
        alert_message = u"ship_order 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
        watchdog_warning(alert_message)