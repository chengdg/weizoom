# -*- coding: utf-8 -*-
__author__ = 'guoliyan'
import json
import time
from test import bdd_util
from market_tools.tools.activity.models import *

#######################################################################
# __supplement_activity: 补足一个活动的数据
#######################################################################
def __supplement_activity(activity):
    activity_prototype = {
        "name": u"活动报名",
        "start_date": u"2014-06-16",
        "end_date": u"2014-06-19",
        "detail": u"<p>343434<br/></p>",
        "is_non_member": u"非会员可参与",
        "is_enable_offline_sign": u"启用线下签到",
        "prize_source": u"500",
        "prize_type": u"3",
        "item_text_data_100000": u"",
        "item_text_data_99999": u"",
        "item_text_mandatory_100000": u"必填",
        "item_text_mandatory_99999": u"必填",
        "item_text_title_100000": u"手机号",
        "item_text_title_99999": u"姓名"
    }

    activity_prototype.update(activity)
    return activity_prototype


#######################################################################
# __add_activity: 添加一个活动
#######################################################################
def __add_activity(context, activity):
    activity = __supplement_activity(activity)
    __process_activity_data(activity)
    context.client.post("/market_tools/activity/activity/create/", activity)


#######################################################################
# __process_activity_data: 转换一个报名的数据
#######################################################################
def __process_activity_data(activity):
    if activity['is_non_member'] == u'非会员可参与':
        activity['is_non_member'] = 1
    else:
         activity['is_non_member'] = 0

    if activity['is_enable_offline_sign'] == u'启用线下签到':
        activity['is_enable_offline_sign'] = 1
    else:
         activity['is_enable_offline_sign'] = 0

    if activity['item_text_mandatory_100000'] == u'必填':
        activity['item_text_mandatory_100000'] = 1
    else:
         activity['item_text_mandatory_100000'] = 0



@when(u"{user}添加活动报名")
def step_impl(context, user):
    client = context.client
    context.activities = json.loads(context.text)
    for activity in context.activities:
        __add_activity(context, activity)


@then(u"{user}能获取活动列表")
def step_impl(context, user):
    context.client = bdd_util.login(user)
    client = context.client
    response = client.get('/market_tools/activity/')
    actual_activities = response.context['activities']
    actual_data = []
    for activity in actual_activities:
        actual_data.append({
            "name": activity.name
        })

    expected = json.loads(context.text)

    bdd_util.assert_list(expected, actual_data)


@given(u"{user}已添加'活动报名'")
def step_impl(context, user):
    if hasattr(context, 'client'):
        context.client.logout()
    context.client = bdd_util.login(user)

    context.activities = json.loads(context.text)
    for activity in context.activities:
        __add_activity(context, activity)


@when(u"{user}删除活动报名'{activity_name}'")
def step_impl(context, user, activity_name):
    activity = Activity.objects.get(name=activity_name)
    url = '/market_tools/activity/activity/delete/%d/' % activity.id
    context.client.get(url, HTTP_REFERER='/market_tools/activity/')


