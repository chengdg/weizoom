#coding: utf8
"""
数据统计(BI)之销售订单分析的BDD steps

"""

__author__ = 'victor'

import json
#import time
from test import bdd_util
from core import dateutil
from market_tools.tools.activity.models import *
from modules.member.models import Member, MemberGrade, MemberTag, MemberHasTag, SOURCE_SELF_SUB, SOURCE_MEMBER_QRCODE, SOURCE_BY_URL
from behave import *
#from features.testenv.model_factory import *
from django.test.client import Client
#from market_tools.tools.delivery_plan.models import *

from core import dateutil
#from util import dateutil as util_dateutil

@when(u'{user}批量获取微信用户关注')
def step_impl(context, user):
	for row in context.table:
		context.execute_steps(u"when %s关注%s的公众号" % (row['member_name'], user))
		# 因没有可用的API处理Member相关的source字段, 暂时直接操作Member对象
		tmp_member = Member.objects.all().order_by('-id')[0]
		tmp_member.created_at = row['attention_time']
		tmp_source = None
		if row['member_source'] == u'直接关注':
			tmp_source = SOURCE_SELF_SUB
		elif row['member_source'] == u'推广扫码':
			tmp_source = SOURCE_MEMBER_QRCODE
		elif row['member_source'] == u'会员分享':
			tmp_source = SOURCE_BY_URL

		if tmp_source:
			tmp_member.source = tmp_source
		if row.get('grade'):
			grade_id = MemberGrade.objects.get(webapp_id=context.webapp_id, name=row['grade']).id
			tmp_member.grade_id = grade_id

		tmp_member.save()

		if row.get('tags'):
			tags_list = row['tags'].split(',')
			for tag in tags_list:
				tag_id = MemberTag.objects.get(webapp_id=context.webapp_id, name=tag).id
				MemberHasTag.objects.create(member_id=tmp_member.id, member_tag_id=tag_id)

@when(u'{user}查询订单概况统计')
def step_impl(context, user):
	start_date = None
	end_date = None

	if context.date_dict:
		start_date = context.date_dict['start_date']
		end_date = context.date_dict['end_date']
		start_date = bdd_util.get_date_str(start_date)
		end_date = bdd_util.get_date_str(end_date)
	else:
		today = dateutil.get_today()
		start_date = dateutil.get_previous_date(today, 6)
		end_date = today

	start_time = start_date + ' 00:00:00'
	end_time = end_date + ' 23:59:59'

	url = '/stats/api/order_summary/?start_time=%s&end_time=%s' % (start_time, end_time)
	response = context.client.get(url)
	bdd_util.assert_api_call_success(response)

	result = json.loads(response.content)
	context.stats_data = result['data']

@then(u'{user}获得订单概况统计数据')
def step_impl(context, user):
	expected = json.loads(context.text)
	# if not expected.get(u'客单价', None):
	#	expected[u'客单价'] = str(expected[u'客单价'])
	actual = {}
	data = context.stats_data
	order_num = data['order_num']
	paid_amount = data['paid_amount']
	if order_num > 0:
		unit_price = '%.2f' % float(float(paid_amount) / float(order_num))
	else:
		unit_price = '0.00'

	actual[u'成交订单'] = order_num
	actual[u'成交金额'] = paid_amount
	actual[u'客单价'] = unit_price
	actual[u'成交商品'] = data['product_num']
	actual[u'优惠抵扣'] = '%.2f' % float(data['discount_amount'])
	actual[u'总运费'] = '%.2f' % float(data['postage_amount'])
	actual[u'在线支付订单'] = data['online_order_num']
	actual[u'在线支付金额'] = '%.2f' % float(data['online_paid_amount'])
	actual[u'货到付款订单'] = data['cod_order_num']
	actual[u'货到付款金额'] = '%.2f' % float(data['cod_amount'])

	bdd_util.assert_dict(expected, actual)

@then(u'{user}获得订单趋势统计数据')
def step_impl(context, user):
	expected = json.loads(context.text)
	actual = {}
	data = context.stats_data['order_trend_stats']
	actual[u'待发货'] = data['not_shipped_num']
	actual[u'已发货'] = data['shipped_num']
	actual[u'已完成'] = data['succeeded_num']

	bdd_util.assert_dict(expected, actual)

@then(u'{user}获得复购率统计数据')
def step_impl(context, user):
	expected = json.loads(context.text)
	actual = {}
	data = context.stats_data
	actual[u'初次购买'] = data['order_num'] - data['repeated_num']
	actual[u'重复购买'] = data['repeated_num']

	bdd_util.assert_dict(expected, actual)

@then(u'{user}获得买家来源统计数据')
def step_impl(context, user):
	expected = json.loads(context.text)
	actual = {}
	data = context.stats_data['buyer_source_stats']
	actual[u'直接关注购买'] = data['sub_source_num']
	actual[u'推广扫码关注购买'] = data['qrcode_source_num']
	actual[u'分享链接关注购买'] = data['url_source_num']
	actual[u'其他'] = data['other_source_num']

	bdd_util.assert_dict(expected, actual)

@then(u'{user}获得支付金额统计数据')
def step_impl(context, user):
	expected = json.loads(context.text)
	actual = {}
	data = context.stats_data
	actual[u'支付宝'] = '%.2f' % float(data['alipay_amount'])
	actual[u'微信支付'] = '%.2f' % float(data['weixinpay_amount'])
	actual[u'货到付款'] = '%.2f' % float(data['cod_amount'])
	actual[u'微众卡支付'] = '%.2f' % float(data['wezoom_card_amount'])

	bdd_util.assert_dict(expected, actual)

@then(u'{user}获得优惠抵扣统计数据')
def step_impl(context, user):
	expected = json.loads(context.text)
	actual = {}
	data = context.stats_data['discount_stats']
	actual[u'微众卡支付.单量'] = data['wezoom_num']
	actual[u'微众卡支付.金额'] = '%.2f' % float(data['wezoom_amount'])
	actual[u'积分抵扣.单量'] = data['integral_num']
	actual[u'积分抵扣.金额'] = '%.2f' % float(data['integral_amount'])
	actual[u'优惠券.单量'] = data['coupon_num']
	actual[u'优惠券.金额'] = '%.2f' % float(data['coupon_amount'])
	actual[u'微众卡+积分.单量'] = data['wezoom_integral_num']
	actual[u'微众卡+积分.金额'] = '%.2f' % float(data['wezoom_integral_amount'])
	actual[u'微众卡+优惠券.单量'] = data['wezoom_coupon_num']
	actual[u'微众卡+优惠券.金额'] = '%.2f' % float(data['wezoom_coupon_amount'])
	actual[u'优惠抵扣订单总数'] = data['discount_order_num']

	bdd_util.assert_dict(expected, actual)

@when(u"浏览'销售分析-订单概况'页面")
def step_impl(context):
	client = context.client
	context.response = client.get("/stats/order_summary/")
	data = context.response.context['jsons'] # 与render_to_response的Response对应
	print("data: {}".format(data))


@then(u"页面上的'筛选日期'")
def step_impl(context):
	print("text: {}".format(context.text))
	expected = json.loads(context.text)
	real = context.response.context['jsons'][0]['content'] # 实际数据

	expected['begin_time'] = bdd_util.escape_date_string(expected['begin_time'])
	context.tc.assertEquals(expected['begin_time'], real['start_time'])

	expected['end_time'] = bdd_util.escape_date_string(expected['end_time'])
	context.tc.assertEquals(expected['end_time'], real['end_time'])


@when(u"已有一批微信用户关注{webapp_user}")
def step_impl(context, webapp_user):
	"""
	确保用户批量关注webapp_user
	"""
	for row in context.table:
		member_name = row['member_name']
		source = row['member_source']
		if source == u'直接关注':
			context.execute_steps(u"When %s关注%s的公众号" % (member_name, webapp_user))
		elif source == u'推广扫码':
			extra = row['extra']
			context.execute_steps(u"When %s通过扫描'%s'二维码关注" % (member_name, extra))
		elif source == u'会员分享':
			extra = row['extra']
			context.execute_steps(u"When %s通过%s分享链接关注%s的公众号'" % (member_name, extra, webapp_user))
