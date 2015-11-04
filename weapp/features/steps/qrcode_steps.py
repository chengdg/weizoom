# -*- coding: utf-8 -*-

import json
import time
import random
from datetime import datetime

from behave import *
from django.test.client import Client

from test import bdd_util
from features.testenv.model_factory import *

from mall.promotion.models import CouponRule
from modules.member.models import Member, MemberGrade, MemberTag
from weixin2.models import Material, News
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeBingMember, ChannelQrcodeHasMember
from market_tools.tools.channel_qrcode.channel_qrcode_util import create_channel_qrcode_has_memeber, create_channel_qrcode_has_memeber_restructure
from utils.string_util import byte_to_hex


def _add_or_update_qrcode(context, data, method, setting_id=0):
    if method == 'put':
        url = "/new_weixin/api/qrcode/?_method=put"
        post_data = {'setting_id': 0}
    else:
        url = "/new_weixin/api/qrcode/?_method=post"
        post_data = {'setting_id': setting_id}
    post_data['name'] = data['code_name']
    if data['prize_type'] == "无奖励":
        post_data['prize_info'] = '{"id":-1,"name":"non-prize","type":"无奖励"}'
    elif data['prize_type'] == "积分":
        post_data['prize_info'] = '{"id":' + str(data['integral']) + ',"name":"_score-prize_","type":"积分"}'
    elif data['prize_type'] == "优惠券":
        coupon_name = data['coupon']
        coupon_id = CouponRule.objects.get(owner_id=context.webapp_owner_id, name=coupon_name).id
        post_data['prize_info'] = '{"id":'+ str(coupon_id) +',"name":"'+ coupon_name +'","type":"优惠券"}'

    grade_id = MemberGrade.objects.get(webapp_id=context.webapp_id, name=data['member_rank']).id
    tag_id = MemberTag.objects.get(webapp_id=context.webapp_id, name=data['tags']).id

    post_data['grade_id'] = grade_id
    post_data['tag_id'] = tag_id
    post_data['remark'] = data['remarks']
    post_data['re_old_member'] = 1 if data['is_attention_in'] == 'true' else 0

    post_data['is_bing_member'] = data['is_relation_member']
    member_name = data.get('relation_member', '')
    if member_name:
        query_hex = byte_to_hex(member_name)
        member_id = Member.objects.get(webapp_id=context.webapp_id, username_hexstr=query_hex).id
        post_data['bing_member_id'] = member_id
        post_data['bing_member_title'] = data.get('title', "")
        post_data['qrcode_desc'] = data.get('code_description', "")

    if data['reply_type'] == "文字":
        post_data['reply_type'] = 1
        post_data['reply_detail'] = data['scan_code_reply']
        post_data['reply_material_id'] = 0
    else:
        post_data['reply_type'] = 2
        post_data['reply_detail'] = ''

        material_ids = Material.objects.filter(owner_id=context.webapp_owner_id, is_deleted=False).values_list('id', flat=True)
        material_id = News.objects.get(material_id__in=material_ids, title=data['scan_code_reply']).material_id
        post_data['reply_material_id'] = material_id

    response = context.client.post(url, post_data)
    bdd_util.assert_api_call_success(response)
    if setting_id:
        qrcode = ChannelQrcodeSettings.objects.get(id=setting_id)
    else:
        qrcode = ChannelQrcodeSettings.objects.filter(owner_id=context.webapp_owner_id).order_by('-id')[0]

    if data['create_time'] == '今天':
        qrcode.created_at = qrcode.created_at.strftime('%Y-%m-%d')
    else:
        qrcode.created_at = datetime.strptime(data['create_time'], '%Y-%m-%d %H:%M:%S')
    qrcode.ticket = __create_random_ticket()
    qrcode.save()

    if data['is_relation_member'] == "true":
        bing_member_record = ChannelQrcodeBingMember.objects.get(channel_qrcode=qrcode, member_id=member_id)
        if data['create_time'] == '今天':
            bing_member_record.created_at = bing_member_record.created_at.strftime('%Y-%m-%d')
        else:
            bing_member_record.created_at = datetime.strptime(data['relation_time'], '%Y-%m-%d %H:%M:%S')
        bing_member_record.save()

def __create_random_ticket():
    ticket = time.strftime("%Y%m%d%H%M%S", time.localtime())
    ticket = '%s%03d' % (ticket, random.randint(1, 999))

    if ChannelQrcodeSettings.objects.filter(ticket=ticket).count() > 0:
        return __create_random_ticket()
    else:
        return ticket

@when(u"{user}添加带参数二维码")
def step_impl(context, user):
    qrcode_data = json.loads(context.text)
    for data in qrcode_data:
        _add_or_update_qrcode(context, data, 'put')


@then(u"{user}获得带参数二维码'{qrcode_name}'")
def step_impl(context, user, qrcode_name):
    qrcode_id = ChannelQrcodeSettings.objects.get(owner_id=context.webapp_owner_id, name=qrcode_name).id
    url = '/new_weixin/qrcode/?setting_id=%s' % str(qrcode_id)
    response = context.client.get(url)

    qrcode_info = response.context['qrcode']
    actual = {}
    actual['code_name'] = qrcode_info.name
    actual['create_time'] = datetime.strftime(qrcode_info.created_at, '%Y-%m-%d %H:%M:%S')
    award_prize_info = json.loads(qrcode_info.award_prize_info)
    if award_prize_info['type'] == '无奖励':
        actual['prize_type'] = '无奖励'
    if award_prize_info['type'] == '积分':
        actual['prize_type'] = '积分'
        actual['integral'] = award_prize_info['id']
    if award_prize_info['type'] == '优惠券':
        actual['prize_type'] = '优惠券'
        actual['coupon'] = award_prize_info['name']

    grade_name = MemberGrade.objects.get(id=qrcode_info.grade_id).name
    tag_name = MemberTag.objects.get(id=qrcode_info.tag_id).name
    actual['member_rank'] = grade_name
    actual['tags'] = tag_name
    actual['is_attention_in'] = 'true' if qrcode_info.re_old_member else 'false'
    actual['remarks'] = qrcode_info.remark
    actual['is_relation_member'] = 'true' if qrcode_info.bing_member_id else 'false'
    if qrcode_info.bing_member_id:
        member = Member.objects.get(id=qrcode_info.bing_member_id)
        actual['relation_member'] = member.username
        actual['title'] = qrcode_info.bing_member_title
        actual['code_description'] = qrcode_info.qrcode_desc
    if qrcode_info.reply_type == 1:
        actual['reply_type'] = "文字"
        actual['scan_code_reply'] = qrcode_info.reply_detail
    if qrcode_info.reply_type == 2:
        actual['reply_type'] = "图文"
        actual['scan_code_reply'] = response.context['jsons'][0]['content']['newses'][0]['title']


    expected = json.loads(context.text)
    if expected['create_time'] == "今天":
        expected['create_time'] = datetime.now().strftime('%Y-%m-%d')
        actual['create_time'] = qrcode_info.created_at.strftime('%Y-%m-%d')
    bdd_util.assert_dict(expected, actual)

@when(u"{user}更新带参数二维码'{qrcode_name}'")
def step_impl(context, user, qrcode_name):
    data = json.loads(context.text)
    qrcode_id = ChannelQrcodeSettings.objects.get(owner_id=context.webapp_owner_id, name=qrcode_name).id
    _add_or_update_qrcode(context, data, 'post', setting_id=qrcode_id)

@when(u"{user}设置带参数二维码查询条件")
def step_impl(context, user):
    query = json.loads(context.text)
    context.query = query['code_name']

@then(u"{user}获得带参数二维码列表")
def step_impl(context, user):
    if hasattr(context, 'query'):
        query = context.query
    else:
        query = ""
    url = "/new_weixin/api/qrcodes/?query=%s" % query
    if hasattr(context, 'count_per_page'):
        url += '&count_per_page=' + str(context.count_per_page)
    if hasattr(context, 'page_number'):
        url += '&page=' + str(context.page_number)
    response = context.client.get(url)

    items = json.loads(response.content)['data']['items']

    actual = []
    for item in items:
        actual_tmpl = {}
        actual_tmpl['code_name'] = item['name']
        actual_tmpl['attention_number'] = item['count']
        actual_tmpl['order_money'] = item['total_final_price']
        actual_tmpl['prize'] = item['cur_prize']
        actual_tmpl['create_time'] = '今天' if item['created_at'].split(" ")[0] == datetime.now().strftime('%Y-%m-%d') else item['created_at']
        actual_tmpl['remarks'] = item['remark']
        actual_tmpl['relation_member'] = item['bing_member_name']
        actual_tmpl['relation_time'] = '今天' if item['bing_time'].split(" ")[0] == datetime.now().strftime('%Y-%m-%d') else item['bing_time']
        actual_tmpl['cancel_related_time'] = '今天' if item['cancel_time'].split(" ")[0] == datetime.now().strftime('%Y-%m-%d') else item['cancel_time']

        actual.append(actual_tmpl)

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)

@when(u"{user}访问带参数二维码列表第'{page_number}'页")
def step_impl(context, user, page_number):
    context.page_number = page_number

@when(u"{user}访问带参数二维码列表下一页")
def step_impl(context, user):
    context.page_number = str(int(context.page_number) + 1)

@when(u"{user}访问带参数二维码列表上一页")
def step_impl(context, user):
    context.page_number = str(int(context.page_number) - 1)

@when(u"{user}导出带参数二维码列表")
def step_impl(context, user):
    if hasattr(context, 'query'):
        query = context.query
    else:
        query = ""
    url = "/new_weixin/qrcode_export/?query=%s" % query
    response = context.client.get(url)

    from cStringIO import StringIO
    import csv

    reader = csv.reader(StringIO(response.content))
    context.reader = reader

@then(u"{user}获得带参数二维码列表导出结果")
def step_impl(context, user):
    csv_items = [row for row in context.reader]
    actual = []
    for item in csv_items[1:]:
        code_name, attention_number, total_final_price, cash_money, weizoom_card_money, prize, create_time = item
        actual.append(dict(
                code_name=code_name,
                attention_number=attention_number,
                total_final_price=total_final_price,
                cash_money=cash_money,
                weizoom_card_money=weizoom_card_money,
                prize=prize,
                create_time=create_time
            ))

    expected = json.loads(context.text)
    for item in expected:
        if item['create_time'] == "今天":
            item['create_time'] = datetime.now().strftime('%Y-%m-%d') + " 00:00:00"
    bdd_util.assert_list(expected, actual)

@when(u'{user}扫描带参数二维码"qrcode_name"')
def step_impl(context, user, qrcode_name):
    channel_setting = bdd_util.get_channel_qrcode_setting(qrcode_name)

#扫码关注任务
@when(u'{webapp_user_name}扫描带参数二维码"{channel_qrcode_name}"')
def step_impl(context, webapp_user_name, channel_qrcode_name):
    channel_setting = bdd_util.get_channel_qrcode_setting(channel_qrcode_name)
    assert channel_setting is not None
    owner_id = channel_setting.owner_id
    owner = User.objects.get(id=owner_id)
    webapp_id = bdd_util.get_webapp_id_via_owner_id(owner_id)
    member = bdd_util.get_member_by_username(webapp_user_name, webapp_id)

    context.user_profile = UserProfile.objects.get(user_id=owner_id)
    ticket = channel_setting.ticket
    # 模拟收到的消息
    openid = '%s_%s' % (webapp_user_name, owner.username)
    url = '/simulator/api/mp_user/qr_subscribe/?version=2'
    data = {
        "timestamp": "1402211023857",
        "webapp_id": webapp_id,
        "ticket": ticket,
        "from_user": openid
    }
    response = context.client.post(url, data)
    response_data = json.loads(response.content)
    context.qa_result = response_data

@when(u'{webapp_user_name}扫描带参数二维码"{channel_qrcode_name}"于{scan_qrcode_time}')
def step_impl(context, webapp_user_name, channel_qrcode_name, scan_qrcode_time):
    context.execute_steps(u'when %s扫描带参数二维码"%s"' % (webapp_user_name, channel_qrcode_name))
    scan_qrcode_time = bdd_util.get_date(scan_qrcode_time)
    relation = ChannelQrcodeHasMember.objects.all().order_by('-id')[0]
    relation.created_at = scan_qrcode_time
    relation.save()
    if relation.is_new:
        relation.member.created_at = scan_qrcode_time
        relation.member.save()

@then(u"{jobs}获得带参数二维码关注会员查询条件")
def step_impl(context, user):
    pass

def __get_args(context, qrcode_name):
    channel_setting = bdd_util.get_channel_qrcode_setting(qrcode_name)
    assert channel_setting is not None
    setting_id = channel_setting.id

    data = {
        "setting_id": setting_id,
        "is_show": 1
    }

    if hasattr(context, 'is_show'):
        data['is_show'] = context.is_show
    if hasattr(context, 'start_time'):
        data['start_date'] = context.start_time
    if hasattr(context, 'end_time'):
        data['end_date'] = context.end_time
    if hasattr(context, 'page_num'):
        data['page'] = context.page_num
    if hasattr(context, 'count_per_page'):
        data['count_per_page'] = context.count_per_page

    return data

@then(u"{user}获得'{qrcode_name}'关注会员列表")
def step_impl(context, user, qrcode_name):
    data = __get_args(context, qrcode_name)

    url = "/new_weixin/api/qrcode_member/"
    response = context.client.get(url, data)
    response_data = json.loads(response.content)
    actual = []
    for item in response_data['data']['items']:
        actual.append(dict(
                member_name=item['username'],
                status= '已关注' if item['is_subscribed'] else '取消关注',
                pay_times=item['pay_times'],
                integral=item['integral'],
                pay_money=item['pay_money'],
                member_rank=item['grade_name'],
                attention_time=item['follow_time']
            ))
    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@when(u"{user}设置带参数二维码关注会员查询条件")
def step_impl(context, user):
    data = json.loads(context.text)
    context.start_time = bdd_util.get_date(data['start_time']) if '天' in data['start_time'] else data['start_time']
    context.end_time = bdd_util.get_date(data['end_time']) if '天' in data['end_time'] else data['end_time']
    context.is_show = 1 if data['is_new_attention_member'] == 'true' else 0

@when(u"{user}访问'{qrcode_name}'关注会员列表第'{page_num}'页")
def step_impl(context, user, qrcode_name, page_num):
    context.page_num = page_num

@when(u"{user}访问'带参数二维码-默认设置'关注会员列表下一页")
def step_impl(context, user):
     context.page_num = str(int(context.page_num) + 1)

@when(u"{user}访问'带参数二维码-默认设置'关注会员列表上一页")
def step_impl(context, user):
     context.page_num = str(int(context.page_num) - 1)

@then(u"{user}获得'{qrcode_name}'交易订单列表汇总")
def step_impl(context, user, qrcode_name):
    data = __get_args(context, qrcode_name)

    url = "/new_weixin/api/qrcode_order/"
    response = context.client.get(url, data)
    response_data = json.loads(response.content)
    actual = {}
    actual['cash'] = response_data['data']['final_price']
    actual['weizoom_card'] = response_data['data']['weizoom_card_money']
    expected = json.loads(context.text)
    bdd_util.assert_dict(actual, expected)

@then(u"{user}获得'{qrcode_name}'交易订单列表")
def step_impl(context, user, qrcode_name):
    data = __get_args(context, qrcode_name)

    url = "/new_weixin/api/qrcode_order/"
    response = context.client.get(url, data)
    response_data = json.loads(response.content)

    actual = []
    for item in response_data['data']['items']:
        order_info = {}
        order_info['order_no'] = item['order_id']
        order_info['order_time'] = '今天' if item['created_at'].split(" ")[0] == datetime.now().strftime('%Y-%m-%d') else item['created_at'].split(" ")[0]
        order_info['payment_time'] = '今天' if item['payment_time'].split(" ")[0] == datetime.now().strftime('%Y-%m-%d') else item['payment_time'].split(" ")[0]
        order_info['consumer'] = item['buyer_name']
        for product in item['products']:
            product_info = []
            product_info.append(product['name'])
            if product['custom_model_properties']:
                product_info.append(" ".join([property['property_value'] for property in product['custom_model_properties']]))
            product_info.append(str(product['count']))
        order_info['product'] = ",".join(product_info)
        order_info['price'] = item['products'][0]['price']
        order_info['pay_type'] = item['pay_interface_name']
        order_info['postage'] = item['postage']
        order_info['discount_amount'] = item['save_money']
        order_info['paid_amount'] = item['pay_money']
        order_info['order_status'] = item['status']
        actual.append(order_info)
    actual = sorted(actual, key=lambda order: order['order_no'], reverse=True)
    if context.table:
        expected = []
        for order in context.table:
            order = order.as_dict()
            expected.append(dict(order))

    bdd_util.assert_list(actual, expected)


@when(u"{user}设置带参数二维码交易订单列表查询条件")
def step_impl(context, user):
    data = json.loads(context.text)
    context.start_time = datetime.now().strftime("%Y-%m-%d") if '今天' in data['start_time'] else data['start_time']
    context.end_time = datetime.now().strftime("%Y-%m-%d") if '今天' in data['end_time'] else data['end_time']
    context.is_show = 1 if data['is_after_code_order'] == 'true' else 0

@when(u"{user}访问'{qrcode_name}'交易订单列表第'{page_num}'页")
def step_impl(context, user, qrcode_name, page_num):
    context.page_num = page_num

@when(u"{user}访问交易订单列表下一页")
def step_impl(context, user):
    context.page_num = str(int(context.page_num) + 1)

@when(u"{user}访问交易订单列表上一页")
def step_impl(context, user):
    context.page_num = str(int(context.page_num) - 1)

@then(u"{user}获得代言人二维码页")
def step_impl(context, user):
    response = _get_setting_data(context)

    actual = {}
    actual['member_name'] = response.context['member'].user_name
    actual['title'] = response.context['setting'].bing_member_title
    actual['code_description'] = response.context['setting'].qrcode_desc
    actual['recommended_number'] = response.context['setting'].count

    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, actual)

def _get_setting_data(context):
    url = "/termite/workbench/jqm/preview/?module=market_tool:channel_qrcode&model=settings&action=get&webapp_owner_id=%s&project_id=0&workspace_id=market_tool:channel_qrcode" % context.webapp_owner_id
    response = context.client.get(bdd_util.nginx(url))
    while response.status_code == 302:
        response = context.client.get(bdd_util.nginx(response['Location']))
    return response

@then(u"{user}获得推荐详情页")
def step_impl(context, user):
    response = _get_setting_data(context)
    url = "/termite/workbench/jqm/preview/?module=market_tool:channel_qrcode&model=settings_detail&action=get&webapp_owner_id=%s&project_id=0&workspace_id=market_tool:channel_qrcode&sid=%s&fmt=%s" % (context.webapp_owner_id, response.context['setting'].id, response.context['member'].token)
    data = context.client.get(bdd_util.nginx(url))
    actual = {}
    actual['recommended_number'] = data.context['channel_qrcode_members_count']
    members = []
    for ralation in data.context['channel_qrcode_members']:
        members.append(dict(
                member_name = ralation.member.username_for_html,
                status = '已关注' if ralation.member.is_subscribed else '已跑路'
            ))
    actual['members'] = members
    actual['pay_member_number'] = data.context['payed_count']
    actual['order_money'] = data.context['pay_money']


    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, actual)

@then(u"{user}获得选择关联会员列表")
def step_impl(context, user):
    url = "/member/api/member_list/?status=1"
    filter_value = "&filter_value="
    if hasattr(context, 'name'):
        filter_value += ('name:' + context.name + '|')
        del context.name
    if hasattr(context, 'tag_id'):
        filter_value += ('tag_id:' + str(context.tag_id) + '|')
        del context.tag_id
    if hasattr(context, 'grade_id'):
        filter_value += ('grade_id:' + str(context.grade_id) + '|')
        del context.grade_id
    filter_value += "status:1"
    response = context.client.get(url+filter_value)
    response_data = json.loads(response.content)
    actual = []
    for data in response_data['data']['items']:
        actual.append(dict(
                member_name = data['username_truncated'],
                member_rank = data['grade_name'],
                pay_money = float(data['pay_money']),
                average_pay_money = float(data['unit_price']),
                pay_times = data['pay_times'],
                integral = data['integral']
            ))

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@When(u"{user}设置选择关联会员列表查询条件")
def step_impl(context, user):
    data = json.loads(context.text)
    if "member_name" in data:
        context.name = data['member_name']
    if "tags" in data:
        if data['tags'] == '全部':
            pass
        else:
            tag_id = MemberTag.objects.get(webapp_id=context.webapp_id, name=data['tags']).id
            context.tag_id = tag_id
    if "member_rank" in data:
        if data['member_rank'] == '全部':
            pass
        else:
            grade_id = MemberGrade.objects.get(webapp_id=context.webapp_id, name=data['member_rank']).id
            context.grade_id = grade_id