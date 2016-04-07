# -*- coding: utf-8 -*-

import json
from datetime import datetime
from core import dateutil
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
import time
from core.charts_apis import *
from stats import export
from core import resource
from mall.models import Order, belong_to
from mall import models
from modules.member.models import Member, WebAppUser, SOURCE_SELF_SUB, SOURCE_MEMBER_QRCODE, SOURCE_BY_URL
from core.jsonresponse import create_response
from django.db.models import Max
import pandas as pd
from decimal import *

FIRST_NAV = export.STATS_HOME_FIRST_NAV


class RepeatBuyAnalysis(resource.Resource):
	"""
	会员分析-复购分析
	"""
	app = 'stats'
	resource = 'repeat_buy_analysis'
	
	@login_required
	def get(request):
		"""
		显示复购分析页面
		"""

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'app_name': 'stats',
			'second_navs': export.get_stats_second_navs(request),
			'second_nav_name': export.STATS_MEMBER_SECOND_NAV,
			'third_nav_name': export.REPEAT_BUY_ANALISIS_NAV
		})

		return render_to_response('member/repeat_buy_analysis.html', c)


	@login_required
	def api_get(request):
		"""
		复购会员分析数据	
		"""
		webapp_id = request.user_profile.webapp_id
		# all 全部， 1 关注 0 取消关注
		is_subscribed = request.GET.get('is_subscribed','all') # 会员是否关注
		search_pay_list = request.GET.get('search_pay_list','')
		if search_pay_list!='':
			search_pay_list = search_pay_list.split(',')
		else:
			search_pay_list = []

		# 校验数据是否正确 [1,2,3,4,5,6]
		if is_subscribed == 'all':
			is_subscribed = [0,1]
		elif is_subscribed == '1':
			is_subscribed = [1]
		elif is_subscribed == '0':
			is_subscribed = [0]

		print "zl---------------------",search_pay_list
		if len(search_pay_list)>0:
			if not RepeatBuyAnalysis._check_pay_money(search_pay_list):
				response = create_response(201)

				response.data = {
					"error":True
				}
				return response.get_response()
			rebuy_fans = Member.objects.filter(webapp_id=webapp_id, is_for_test=False,pay_times__gte=2,is_subscribed__in=is_subscribed,status__in=[0,1])
			rebuy_fans_1 = rebuy_fans.filter(pay_money__gte=search_pay_list[0],pay_money__lt=search_pay_list[1]).count()
			rebuy_fans_2 = rebuy_fans.filter(pay_money__gte=search_pay_list[2],pay_money__lt=search_pay_list[3]).count()
			rebuy_fans_3 = rebuy_fans.filter(pay_money__gte=search_pay_list[4],pay_money__lt=search_pay_list[5]).count()
			other_rebug_fans = rebuy_fans.count()-rebuy_fans_1-rebuy_fans_2-rebuy_fans_3
			all_rebuy_fans = rebuy_fans.count()
			return create_pie_chart_response('',
				{
					u"消费金额:{}-{}\n人数:{}\n占比:{}".format(search_pay_list[0],search_pay_list[1],rebuy_fans_1,format( float(Decimal(rebuy_fans_1)/Decimal(all_rebuy_fans)),'.2%') if all_rebuy_fans!=0 else '0%'): rebuy_fans_1,
					u"消费金额:{}-{}\n人数:{}\n占比:{}".format(search_pay_list[2],search_pay_list[3],rebuy_fans_2,format( float(Decimal(rebuy_fans_2)/Decimal(all_rebuy_fans)),'.2%') if all_rebuy_fans!=0 else '0%'): rebuy_fans_2,
					u"消费金额:{}-{}\n人数:{}\n占比:{}".format(search_pay_list[4],search_pay_list[5],rebuy_fans_3,format( float(Decimal(rebuy_fans_3)/Decimal(all_rebuy_fans)),'.2%') if all_rebuy_fans!=0 else '0%'): rebuy_fans_3,
					u"其他\n人数:{}\n占比:{}".format(other_rebug_fans,format( float(Decimal(other_rebug_fans)/Decimal(all_rebuy_fans)),'.2%') if all_rebuy_fans!=0 else '0%'): other_rebug_fans
				}
			)
		else:
			rebuy_fans = Member.objects.filter(webapp_id=webapp_id, is_for_test=False,pay_times__gte=2,is_subscribed__in=is_subscribed,status__in=[0,1])
			max_pay_money = rebuy_fans.aggregate(Max('pay_money'))
			count = rebuy_fans.count()
			return create_pie_chart_response('',
				{
					u"消费金额:0-{}\n人数:{}\n占比:100%".format(max_pay_money['pay_money__max'],count): count,
				}
			)




	@staticmethod
	def _check_pay_money(pay_money_list):
		_len = len(pay_money_list)
		if _len !=6:
			return False
		for i in range(0, _len - 2):
			if int(pay_money_list[i+1]) - int(pay_money_list[i]) <0:
				return False
		return True


class BuyPercent(resource.Resource):
	"""
	会员购买占比
	"""
	app = 'stats'
	resource = 'buy_percent'

	@login_required
	def api_get(request):
		"""
		会员购买占比数据
		默认会员分为1、2、3-5、5以上 几个阶段 显示人数、占比
		, pay_times__gte=2
		"""

		webapp_id = request.user_profile.webapp_id
		# all 全部， 1 关注 0 取消关注
		is_subscribed = request.GET.get('is_subscribed','all') # 会员是否关注

		if is_subscribed == 'all':
			is_subscribed = [0,1]
		elif is_subscribed == '1':
			is_subscribed = [1]
		elif is_subscribed == '0':
			is_subscribed = [0]
		buy_fans = Member.objects.filter(webapp_id=webapp_id, is_for_test=False,is_subscribed__in=is_subscribed,status__in=[0,1])
		bought_fans_1 = buy_fans.filter(pay_times=1).count()
		bought_fans_2 = buy_fans.filter(pay_times=2).count()
		bought_fans_3_5 = buy_fans.filter(pay_times__gte=3,pay_times__lte=5).count()
		bought_fans_5_after = buy_fans.filter(pay_times__gt=5).count()
		all_buy_fnas = bought_fans_1+bought_fans_2+bought_fans_3_5+bought_fans_5_after
		return create_pie_chart_response('',
				{
					u"购买1次的会员\n人数:{}\n占比:{}".format(bought_fans_1,format( float(Decimal(bought_fans_1)/Decimal(all_buy_fnas)),'.2%') if all_buy_fnas!=0 else '0%'):bought_fans_1,
					u"购买2次的会员\n人数:{}\n占比:{}".format(bought_fans_2,format(float(Decimal(bought_fans_2)/Decimal(all_buy_fnas)),'.2%') if all_buy_fnas!=0 else '0%'):bought_fans_2,
					u"购买3-5次的会员\n人数:{}\n占比:{}".format(bought_fans_3_5,format(float(Decimal(bought_fans_3_5)/Decimal(all_buy_fnas)),'.2%') if all_buy_fnas!=0 else '0%'):bought_fans_3_5,
					u"购买5次以上的会员\n人数:{}\n占比:{}".format(bought_fans_5_after,format(float(Decimal(bought_fans_5_after)/Decimal(all_buy_fnas)),'.2%') if all_buy_fnas!=0 else '0%'):bought_fans_5_after
				}
			)

class UserAnalysis(resource.Resource):
	"""
	会员购买占比
	"""
	app = 'stats'
	resource = 'user_analysis'

	@login_required
	def api_get(request):
		"""
		会员购买占比数据
		默认会员分为1、2、3-5、5以上 几个阶段 显示人数、占比
		, pay_times__gte=2
		"""

		webapp_id = request.user_profile.webapp_id
		# all 全部， 1 关注 0 取消关注
		is_subscribed = request.GET.get('is_subscribed','all') # 会员是否关注
		pay_times = request.GET.get('pay_times','') # 会员是否关注
		pay_money = request.GET.get('pay_money','') # 会员是否关注

		if is_subscribed == 'all':
			is_subscribed = [0,1]
		elif is_subscribed == '1':
			is_subscribed = [1]
		elif is_subscribed == '0':
			is_subscribed = [0]
		buy_fans_ = Member.objects.filter(webapp_id=webapp_id, is_for_test=False,is_subscribed__in=is_subscribed,status__in=[0,1])
		if pay_times !='':
			pay_times_arr = pay_times.split(',')
			buy_fans_ = buy_fans_.filter(pay_times__gte=pay_times_arr[0],pay_times__lte=pay_times_arr[1])
		if pay_money!='':
			pay_money_arr = pay_money.split(',')
			buy_fans_ =buy_fans_.filter(pay_money__gte=pay_money_arr[0],pay_money__lte=pay_money_arr[1])
		if  pay_times =='' and pay_money=='':
			buy_fans_ = buy_fans_.filter(pay_times__gte=1)
		buy_fans_count = buy_fans_.count()

		response = create_response(200)
		response.data = {
			"fans_num":buy_fans_count
		}
		return response.get_response()


