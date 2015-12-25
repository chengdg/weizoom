# -*- coding: utf-8 -*-
import json

from behave import *

from test import bdd_util
from utils import cache_util

import account.models as account_models

ORDER_NOTIFY_STATUS_TEXT2_STATUS_ID = {
    u'下单时': account_models.PLACE_ORDER,
    u'付款时': account_models.PAY_ORDER,
    u'发货时': account_models.SHIP_ORDER,
    u'完成时': account_models.SUCCESSED_ORDER,
    u'取消时': account_models.CANCEL_ORDER
}


@given(u'{user}初始化邮件通知')
def step_impl(context, user):
    context.client.get('/mall2/email_notify_list/')


@when(u"{user}配置'{status}'邮件通知")
def step_impl(context, user, status):
    status = ORDER_NOTIFY_STATUS_TEXT2_STATUS_ID[status]
    url = '/mall2/email_notify/' + '?status=' + str(status)
    data = json.loads(context.text)
    data['status'] = status
    context.client.post(url, data)

@when(u"{user}启用'{status}'邮件通知")
def step_impl(context, user, status):


    url = '/mall2/api/email_notify/?_method=put'
    status = ORDER_NOTIFY_STATUS_TEXT2_STATUS_ID[status]
    user_id = bdd_util.get_user_id_for(user)
    id = account_models.UserOrderNotifySettings.objects.get(status=status, user_id=user_id).id

    data = {
        'id': id,
        'status': '1'
    }

    res = context.client.post(url, data)

