# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from modules.member.models import *
from mall.promotion.models import CouponRule
from utils.string_util import byte_to_hex, hex_to_byte
from tools.regional import views as regional_util

@when(u"{user}访问'{member}'会员详情")
def step_impl(context, user, member):
    # query_hex = byte_to_hex(member)
    # member_id = Member.objects.get(webapp_id=context.webapp_id, username_hexstr=query_hex).id
    # url = "/member/member_detail/edit/?id=%s" % str(member_id)
    # response = context.client.get(url)
    # context.member_id = member_id
    pass

def _get_member_info(context, member):
    query_hex = byte_to_hex(member)
    member_id = Member.objects.get(webapp_id=context.webapp_id, username_hexstr=query_hex).id
    context.member_id = member_id
    url = "/member/detail/?id=%s" % str(member_id)
    response = context.client.get(url)
    return response

@then(u"{user}获得'{member}'会员详情")
def step_impl(context, user, member):
    response = _get_member_info(context, member)
    expected = json.loads(context.text)
    show_member = response.context['show_member'].to_dict()
    show_member_info = response.context['show_member_info']
    show_member_info = show_member_info.to_dict() if show_member_info else None
    member_has_tags = response.context['member_has_tags']
    grades = response.context['grades']
    grade_id = show_member['grade_id']
    grade_name = ""

    for g in grades:
        if g.id == grade_id:
            grade_name = g.name

    if show_member_info:
        if show_member_info['sex'] == 1:
            sex = "男"
        elif show_member_info['sex'] == 2:
            sex = "女"
        elif show_member_info['sex'] == 0:
            sex = "未知"
    else:
        sex = "未知"

    actual = {}
    actual['member_name'] = hex_to_byte(show_member['username_hexstr'])
    actual['attention_time'] = show_member['created_at'].strftime("%Y-%m-%d")
    actual['remarks'] = show_member_info['member_remarks'] if show_member_info else ""
    actual['name'] = show_member_info['name'] if show_member_info else ""
    actual['sex'] = sex
    actual['phone'] = show_member_info['phone_number'] if show_member_info else ""
    actual['last_buy_time'] = "今天" if show_member['last_pay_time'] else ""
    actual['tags'] = [tag.member_tag.name for tag in member_has_tags]
    actual['grade'] = grade_name
    actual['integral'] = show_member['integral']
    actual['friend_count'] = show_member['friend_count']

    bdd_util.assert_dict(actual, expected)

@when(u'{user}修改会员详情')
def step_impl(context, user):
    data = json.loads(context.text)
    grade_name = data['grade']
    grade_id = MemberGrade.objects.get(webapp_id=context.webapp_id, name=grade_name).id
    tag_ids = []
    if data.has_key('tags'):
        for tag_name in data['tags']:
            tag_ids.append(str(MemberTag.objects.get(webapp_id=context.webapp_id, name=tag_name).id))
    if data.has_key('sex'):
        if data['sex'] == '未知':
            sex = 0
        elif data['sex'] == '男':
            sex = 1
        elif data['sex'] == '女':
            sex = 2
    else:
        sex = 0
    args = {
        'member_id': context.member_id,
        'grade_id': grade_id,
        'member_remarks': data['remarks'],
        'name': data['name'],
        'sex': sex,
        'phone_number': data['phone'],
        'tag_ids': '_'.join(tag_ids)
    }

    response = context.client.post('/member/api/detail/', args)
    bdd_util.assert_api_call_success(response)

@then(u"{user}获得'积分明细'列表")
def step_impl(context, user):
    url = '/member/api/integral_logs/'
    response = context.client.get(url, {'member_id': context.member_id})
    expected = json.loads(context.text)
    for data in expected:
        if data['date'] == '今天':
            data.pop("date")
            data['created_at'] = datetime.today().strftime("%Y/%m/%d")

    actual = json.loads(response.content)['data']['items']
    for data in actual:
        data['created_at'] = data['created_at'].split(" ")[0]
    bdd_util.assert_list(actual, expected)

@then(u"{user}获得'{member}'的收货信息")
def step_impl(context, user, member):
    expected = json.load(context.text)
    response = _get_member_info(context, member)
    actual = []
    for ship_info in response.context['ship_infos']:
        ship = {}
        ship['address'] = ship_info.province + " " + ship_info.city + " " + ship_info.village + " " + ship_info.ship_address
        ship['ship_name'] = ship_info.ship_name
        ship['ship_tel'] = ship_info.ship_tel
        actual.append(ship)
    bdd_util.assert_list(actual, expected)

@then(u"{user}获得'{member}'的购买信息")
def step_impl(context, user, member):
    response = _get_member_info(context, member)
    expected = json.loads(context.text)
    show_member = response.context['show_member'].to_dict()
    actual = {}
    actual['purchase_amount'] = show_member["pay_money"]
    actual['purchase_number'] = show_member["pay_times"]
    actual['customer_price'] = show_member["unit_price"]

    bdd_util.assert_dict(actual, expected)


@then(u"{user}获得'{member}'的订单列表")
def step_impl(context, user, member):
    response = _get_member_info(context, member)
    orders = response.context['orders']
    actual = []
    for order in orders:
        actual.append(dict(
                order_id = order.order_id,
                order_amount = "%.2f" % order.final_price,
                date = order.created_at.strftime("%Y-%m-%d"),
                order_status = STATUS2TEXT[order.status]
            ))
    if context.table:
        expected = []
        for order in context.table:
            order = order.as_dict()
            expected.append(dict(order))

    bdd_util.assert_list(actual, expected)

@when(u"{webapp_user_name}访问{share_member}分享{webapp_owner_name}的微站链接")
def step_impl(context, webapp_user_name, share_member, webapp_owner_name):
    context.execute_steps(u"When %s访问%s的webapp" % (webapp_user_name, webapp_owner_name))

@then(u"{user}获得'{member}'的传播能力")
def step_impl(context, user, member):
    response = _get_member_info(context, member)
    expected = json.loads(context.text)
    shared_url_infos = response.context['shared_url_infos']
    shared_url_lead_number = response.context['shared_url_lead_number']
    qrcode_friends = response.context['qrcode_friends']
    actual = {}
    share_detailed_data = []
    actual['scan_qrcode_new_member'] = qrcode_friends
    actual['share_link_new_member'] = shared_url_lead_number
    for info in shared_url_infos:
        share_detailed_data.append(
            dict(
                click_number = info.pv,
                new_member = info.followers,
                order = info.leadto_buy_count
            )
        )
    actual['share_detailed_data'] = share_detailed_data
    print("actual:",actual)
    print("expected:",expected)

    bdd_util.assert_dict(expected, actual)

@then(u"{user}获得'{member}'的浏览轨迹")
def step_impl(context, user, member):
    url = '/member/api/member_browse_record/?id='+member.id
    response = context.client.get(bdd_util.nginx(url))
    items = json.loads(response.content)['data']['items']
    expected = json.loads(context.text)

    actual = []
    for record in items:
        actual.append(dict(
            date_time = record['create_at'].strftime("%Y-%m-%d"),
            link = record['tittle']
        ))

    for item in expected:
        item['date_time'] = "{}".format(bdd_util.get_date_str(item['date_time']))

    bdd_util.assert_list(actual, expected)


@When(u"{user}访问'{webapp_user}'{spreadPath}引流会员好友列表")
def step_impl(context, user, webapp_user, spreadPath):
    spreadPath = spreadMethod(spreadPath)
    url = '/member/api/member_list/?design_mode=0&version=1&status=1&enable_paginate=1'
    response = context.client.get(bdd_util.nginx(url))
    items = json.loads(response.content)['data']['items']
    for member_item in items:
        if webapp_user == member_item['username']:
            context.user_id = member_item['id']
            break
    if hasattr(context, 'user_id'):
        context.page = 1
        context.url = '/member/api/follow_relations/?design_mode=0&'\
        'version=1&data_value=%s&member_id=%s&sort_attr=-created_at&count_per_page=%s&page=%s'\
        '&enable_paginate=1' %(spreadPath, context.user_id, context.count_per_page, context.page)

@Then(u"{user}获得{spreadPath}引流会员好友列表显示共{page_total}页")
def step_impl(context, user, page_total, spreadPath):
    #spreadPath = spreadMethod(spreadPath)
    response = context.client.get(bdd_util.nginx(context.url))
    actual_total = int(json.loads(response.content)['data']['pageinfo']['max_page'])
    page_total = int(page_total)
    assert(page_total, actual_total)

@When(u"{user}浏览{spreadPath}引流会员好友列表'第{page}页'")
def step_impl(context, user, page, spreadPath):
    spreadPath = spreadMethod(spreadPath)
    context.page = page
    context.url = '/member/api/follow_relations/?design_mode=0&'\
        'version=1&data_value=%s&member_id=%s&sort_attr=-created_at&count_per_page=%s&'\
        'page=%s&enable_paginate=1' %(spreadPath, context.user_id, context.count_per_page, context.page)

@Then(u'{user}获得{spreadPath}引流会员好友列表')
def step_impl(context, user, spreadPath):
    source_dict = {0:u'直接关注', 1:u'推广扫码', 2:u'会员分享'}
    response = context.client.get(bdd_util.nginx(context.url))
    items = json.loads(response.content)['data']['items']
    actual_data = []
    for item in items:
        adict = {}
        adict['name'] = item['username']
        adict['member_rank'] = item['grade_name']
        adict['integral'] = item['integral']
        adict['attention_time'] = item['created_at']
        adict['source'] = source_dict[item['source']]
        actual_data.append(adict)

    expected_data = json.loads(context.text)

    for tmp in expected_data:
        if tmp['attention_time'] == u'今天':
            tmp['attention_time'] = time.strftime('%Y-%m-%d')
    bdd_util.assert_list(expected_data, actual_data)

@When(u"{user}浏览{spreadPath}引流会员好友列表'下一页'")
def step_impl(context, user, spreadPath):
    spreadPath = spreadMethod(spreadPath)
    context.page = int(context.page) + 1
    context.url = '/member/api/follow_relations/?design_mode=0&'\
        'version=1&data_value=%s&member_id=%s&sort_attr=-created_at&count_per_page=%s&'\
        'page=%s&enable_paginate=1' %(spreadPath, context.user_id, context.count_per_page, context.page)

@When(u"{user}浏览{spreadPath}引流会员好友列表'上一页'")
def step_impl(context, user, spreadPath):
    spreadPath = spreadMethod(spreadPath)
    if int(context.page) > 1:
        context.page = int(context.page) - 1
    context.url = '/member/api/follow_relations/?design_mode=0&'\
        'version=1&data_value=%s&member_id=%s&sort_attr=-created_at&count_per_page=%s&'\
        'page=%s&enable_paginate=1' %(spreadPath, context.user_id, context.count_per_page, context.page)


def spreadMethod(sMethod):
    if u'分享链接' == sMethod:
        return 'shared'
    elif u'二维码' == sMethod:
        return 'qrcode'

@When(u"休眠1秒")
def step_impl(context):
    time.sleep(1)

@Then(u"{user}获得'{member}'的收货信息列表")
def step_impl(context, user, member):
    expected = json.loads(context.text)
    response = _get_member_info(context, member)
    actual = []
    for ship_info in response.context['ship_infos']:
        ship = {}
        ship['area'] = regional_util.get_str_value_by_string_ids(ship_info.area)
        ship['area'] = ','.join(ship['area'].split())
        ship['ship_address'] = ship_info.ship_address
        ship['ship_name'] = ship_info.ship_name
        ship['ship_tel'] = ship_info.ship_tel
        actual.append(ship)
    bdd_util.assert_list(actual, expected)
