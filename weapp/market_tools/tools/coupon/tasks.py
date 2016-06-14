# -*- coding: utf-8 -*-

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_info, watchdog_warning
from market_tools.tools.template_message import models as template_message_model
from market_tools.tools.template_message import module_api as template_message_api
from celery import task

@task
def send_message_to_member(rule, member_id, first_text=None):
    #给用户发优惠券提示
    try:
        model_data = {
            "coupon_name": u'%s' % rule.name,
            "invalid_date": u'%s至%s有效' % (rule.start_date.strftime("%Y-%m-%d"), rule.end_date.strftime("%Y-%m-%d"))
        }
        template_message_api.send_weixin_template_message(rule.owner_id, member_id, model_data, template_message_model.COUPON_ARRIVAL_NOTIFY, first_text)
    except:
        alert_message = u"ship_order 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
        watchdog_warning(alert_message)


@task
def send_message_to_member_for_weizoom(owner_id, member_id, template_id, template_url, first_text, remark_text):
    #给用户发审核未通过的提示
    try:
        detail_data = {}
        detail_data["keyword1"] = {"value" : u'未采纳', "color" : "#173177"}
        detail_data["keyword2"] = {"value" : u'反馈内容需进一步完善丰富', "color" : "#173177"}
        detail_data["first"] = {"value" : first_text, "color" : "#000000"}
        detail_data["remark"] = {"value" : remark_text, "color" : "#000000"}
        
        template_data = dict()
        template_data['template_id'] = template_id
        template_data['topcolor'] = "#FF0000"
        template_data['url'] = template_url
        template_data['data'] = detail_data

        template_message_api.send_template_message_for_weizoom(owner_id, member_id, template_data)
    except:
        alert_message = u"ship_order 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
        watchdog_warning(alert_message)