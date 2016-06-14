# -*- coding: utf-8 -*-
from core import api_resource, dateutil
from wapi.decorators import param_required
from wapi.wapi_utils import get_webapp_id_via_username
from datetime import timedelta, datetime
import json

import stats.util as stats_util
from core.charts_apis import create_line_chart_response

class MemberIncreasement(api_resource.ApiResource):
	"""
	获取购买趋势的接口
	"""
	app = 'stats'
	resource = 'member_increasement'

	@param_required(['un'])
	def get(args):
		"""
		获取微品牌价值

		@param un username
		@param sd 起始日期(可选参数)
		@param ed 结束日期(可选参数)
		"""
		username = args.get('un')
		start_date = args.get('sd', None)
		end_date = args.get('ed', None)

		date_fmt = "%Y-%m-%d"
		if type(start_date) == unicode:
			start_date = datetime.strptime(start_date, date_fmt)
		if type(end_date) == unicode:
			end_date = datetime.strptime(end_date, date_fmt)

		webapp_id = get_webapp_id_via_username(username)

		date_formatter = stats_util.TYPE2FORMATTER['day']
		if not end_date:
			#默认显示最近7天的日期
			end_date = datetime.strptime(dateutil.get_today(), date_fmt)

		if not start_date:
			start_date = datetime.strptime(dateutil.get_previous_date('today', 6), date_fmt) #获取7天前日期

		date_range = dateutil.get_date_range_list(start_date, end_date)


		#新增会员数
		date2new_member_count = stats_util.get_date2new_member_count(webapp_id, start_date, end_date)

		#下单会员数
		date2bought_member_count = stats_util.get_date2bought_member_count(webapp_id, start_date, end_date)

		#绑定手机会员数
		date2binding_phone_member_count = stats_util.get_date2binding_phone_member_count(webapp_id, start_date, end_date)

		formatted_date_list = stats_util.get_formatted_date_list(date_range, date_formatter)

		#准备X轴日期数据
		x_values = formatted_date_list

		#准备Y轴数据
		new_member_count_list = []
		bought_member_count_list = []
		binding_phone_member_count_list = []

		for date in formatted_date_list:
			new_member_count = 0  #新增会员数
			if date2new_member_count.has_key(date):
				new_member_count = date2new_member_count[date]

			new_member_count_list.append(new_member_count)

			bought_member_count = 0  #下单会员数
			if date2bought_member_count.has_key(date):
				bought_member_count = date2bought_member_count[date]

			bought_member_count_list.append(bought_member_count)

			binding_phone_member_count = 0  #绑定手机会员数
			if date2binding_phone_member_count.has_key(date):
				binding_phone_member_count = date2binding_phone_member_count[date]

			binding_phone_member_count_list.append(binding_phone_member_count)

		y_values = [
			{
				"name": "新增会员数",
				"values" : new_member_count_list,
			},{
				"name": "下单会员数",
				"values" : bought_member_count_list,
			# },{
			# 	"name": "绑定手机会员数",
			# 	"values" : binding_phone_member_count_list,
			}
		]
		response = create_line_chart_response('', '', x_values, y_values)
		data = json.loads(response.content)['data']

		return data
