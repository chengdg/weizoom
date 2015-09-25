# -*- coding: utf-8 -*-

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_info, watchdog_warning
from market_tools.tools.template_message import models as template_message_model
from market_tools.tools.template_message import module_api as template_message_api
from celery import task

@task
def send_message_to_member(rule, member_id):
    #给用户发优惠券提示
    try:
        model_data = {
            "coupon_name": u'%s' % rule.name,
            "invalid_date": u'%s至%s有效' % (rule.start_date.strftime("%Y-%m-%d"), rule.end_date.strftime("%Y-%m-%d"))
        }
        template_message_api.send_weixin_template_message(rule.owner_id, member_id, model_data, template_message_model.COUPON_ARRIVAL_NOTIFY)
    except:
        alert_message = u"ship_order 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
        watchdog_warning(alert_message)