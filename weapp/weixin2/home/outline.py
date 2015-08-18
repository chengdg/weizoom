# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from datetime import timedelta
from weixin2 import export
from core.exceptionutil import unicode_full_stack
from core import resource
#from core import paginator
from core.jsonresponse import create_response
from core import dateutil
from modules.member.models import *
from weixin2.models import Session, MessageAnalysis, KeywordCount, KeywordHistory
from weixin.user.models import get_system_user_binded_mpuser
from core.charts_apis import *
from django.db.models import Sum
from weixin.mp_decorators import mp_required
from core import paginator

FIRST_NAV = export.HOME_FIRST_NAV

class Outline(resource.Resource):
	app = 'new_weixin'
	resource = 'outline'

	@login_required
	@mp_required
	def get(request):
		"""
		微信概况
		"""
		owner_id = request.user.id
		webapp_id = request.user_profile.webapp_id

		member_count = Member.count(webapp_id)

		yesterday_added_count, yesterday_net_count = _get_yesterday_count(owner_id)

		unread_message_count = _get_unread_message_count(request.user)
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_home_second_navs(request),
			'second_nav_name': export.HOME_OUTLINE_NAV,
			'member_count': member_count,
			'yesterday_added_count': yesterday_added_count,
			'yesterday_net_count': yesterday_net_count,
			'unread_message_count': unread_message_count
		})
		return render_to_response('weixin/home/outline.html', c)

	@login_required
	def api_get(request):
		unread_message_count = _get_unread_message_count(request.user)
		try:
			response = create_response(200)
			response.data = {
				'unread_realtime_count': unread_message_count,
				}
			#watchdog_debug("response.data={}".format(response.data))
		except:
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()

def _get_yesterday_count(owner_id):
	yesterday_added_count, yesterday_net_count = 0, 0
	yesterday_str = dateutil.get_yesterday_str('today')
	analysis = MemberAnalysis.get_analysis_by_date(owner_id, yesterday_str)

	if analysis:
		yesterday_added_count = analysis.new_user
		yesterday_net_count = analysis.cancel_user

	return yesterday_added_count, yesterday_net_count

def _get_unread_message_count(user):
	unread_message_count = 0
	mpuser = get_system_user_binded_mpuser(user)
	sessions = Session.objects.select_related().filter(mpuser=mpuser, is_show=True).exclude(member_latest_created_at="").aggregate(Sum("unread_count"))

	if sessions["unread_count__sum"] is not None:
		unread_message_count = sessions["unread_count__sum"]

	return unread_message_count;



class ReactTest(resource.Resource):
	app = 'new_weixin'
	resource = 'react_test'

	def get(request):
		"""
		测试React
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_home_second_navs(request),
			'second_nav_name': export.HOME_NAV,
		})
		return render_to_response('weixin/home/react_test.html', c)


class UserAnalysis(resource.Resource):
	app = 'new_weixin'
	resource = 'user_analysis'

	@login_required
	def api_get(request):
		"""
		用户分析
		"""
		days = request.GET.get('days', 7)
		try:
			owner_id = request.user.id
			total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
			date_list = [date.strftime("%Y-%m-%d") for date in dateutil.get_date_range_list(low_date, high_date)]
			display_date_list = [date.strftime("%m.%d") for date in dateutil.get_date_range_list(low_date, high_date)]

			analysis = MemberAnalysis.objects.filter(owner_id=owner_id, date_time__range=(low_date, (high_date+timedelta(days=1)))).order_by('date_time')

			date2added = dict()
			date2cancel = dict()
			date2net = dict()
			date2total = dict()

			for analys in analysis:
				date = analys.date_time
				date2added[date] = analys.new_user
				date2cancel[date] = analys.cancel_user
				date2net[date] = analys.net_growth
				date2total[date] = analys.cumulate_user

			added_trend_values = []
			cancel_trend_values = []
			net_trend_values = []
			total_trend_values = []
			for date in date_list:
				added_trend_values.append(date2added.get(date, 0))
				cancel_trend_values.append(date2cancel.get(date, 0))
				net_trend_values.append(date2net.get(date, 0))
				total_trend_values.append(date2total.get(date, 0))

			return create_line_chart_response(
				'',
				'',
				display_date_list,
				[{
					"name": "新增人数",
					"values" : added_trend_values
				}, {
					"name": "跑路人数",
					"values" : cancel_trend_values
				}, {
					"name": "净增人数",
					"values" : net_trend_values
				}, {
					"name": "累计人数",
					"values" : total_trend_values
				}],
				["#11ca64", "#e2bf91", "#ca117e", "#00a2ff"]
			)
		except:
			if settings.DEBUG:
				raise
			else:
				response = create_response(500)
				response.innerErrMsg = unicode_full_stack()
				return response.get_response()


class PageTrackAnalysis(resource.Resource):
	app = 'new_weixin'
	resource = 'page_track_analysis'

	@login_required
	def api_get(request):
		"""
		页面访问
		"""
		days = request.GET.get('days', 7)
		try:
			owner_id = request.user.id
			total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
			date_list = [date.strftime("%Y-%m-%d") for date in dateutil.get_date_range_list(low_date, high_date)]
			display_date_list = [date.strftime("%m.%d") for date in dateutil.get_date_range_list(low_date, high_date)]

			analysis = MessageAnalysis.objects.filter(owner_id=owner_id, date_time__range=(low_date, (high_date+timedelta(days=1)))).order_by('date_time')

			date2receive = dict()
			date2send = dict()
			date2interaction_user = dict()
			date2interaction = dict()

			for analys in analysis:
				date = analys.date_time.strftime("%Y-%m-%d")
				date2receive[date] = analys.receive_count
				date2send[date] = analys.send_count
				date2interaction_user[date] = analys.interaction_user_count
				date2interaction[date] = analys.interaction_count

			receive_count_values = []
			send_count_values = []
			interaction_user_count_values = []
			interaction_count_values = []
			for date in date_list:
				receive_count_values.append(date2receive.get(date, 0))
				send_count_values.append(date2send.get(date, 0))
				interaction_user_count_values.append(date2interaction_user.get(date, 0))
				interaction_count_values.append(date2interaction.get(date, 0))

			return create_line_chart_response(
				'',
				'',
				display_date_list,
				[{
					"name": "接收消息数",
					"values" : receive_count_values
				}, {
					"name": "发送消息数",
					"values" : send_count_values
				}, {
					"name": "互动人数",
					"values" : interaction_user_count_values
				}, {
					"name": "互动次数",
					"values" : interaction_count_values
				}],
				["#11ca64", "#ca117e", "#00a2ff", "#ff9600"]
			)
		except:
			if settings.DEBUG:
				raise
			else:
				response = create_response(500)
				response.innerErrMsg = unicode_full_stack()
				return response.get_response()

class FansAnalysis(resource.Resource):
	app = 'new_weixin'
	resource = 'fans_analysis'

	@login_required
	def api_get(request):
		"""
		会员分析
		"""
		webapp_id = request.user_profile.webapp_id
		subscribed_fans_count = Member.objects.filter(webapp_id=webapp_id, is_subscribed=True, is_for_test=False).count()
		unsubscribed_fans_count = Member.objects.filter(webapp_id=webapp_id, is_subscribed=False, is_for_test=False).count()

		display_date_list = ['取消关注会员', '现有会员']
		try:
			return create_bar_chart_response(
				display_date_list,
				[{
					"name": "现有会员",
					"values" : [
						{'value':unsubscribed_fans_count,'itemStyle': {'normal': {'color': '#B5B5B5'}}},
						{'value':subscribed_fans_count,'itemStyle': {'normal': {'color': '#63B8FF'}}}
					],
					"tooltip" : {
						"trigger" : "item",
						"formatter" : "数量:{c}"
					},
					"barWidth": 40
				}],
				True,
				False
			)
		except:
			if settings.DEBUG:
				raise
			else:
				response = create_response(500)
				response.innerErrMsg = unicode_full_stack()
				return response.get_response()

class BoughtFansAnalysis(resource.Resource):
	app = 'new_weixin'
	resource = 'bought_fans_analysis'

	@login_required
	def api_get(request):
		"""
		购买过会员分析
		"""
		webapp_id = request.user_profile.webapp_id
		bought_fans_count = Member.objects.filter(webapp_id=webapp_id, is_for_test=False, pay_times__gt=0).count()
		not_bought_fans_count = Member.objects.filter(webapp_id=webapp_id, is_for_test=False, pay_times=0).count()
		tooltip = {
					'trigger': 'item',
					'formatter': '{b}</br>人数：{c}</br>占比：{d}%',
					'backgroundColor': '#FFFFFF',
					'textStyle': {'color': '#363636'},
					'borderWidth': 1,
					'borderColor': '#363636'
				}
		try:
			return create_pie_chart_response('',
				{
					"购买过的会员": bought_fans_count,
					"未购买过的会员": not_bought_fans_count
				},
				tooltip
			)
		except:
			if settings.DEBUG:
				raise
			else:
				response = create_response(500)
				response.innerErrMsg = unicode_full_stack()
				return response.get_response()

class KeywordAnalysis(resource.Resource):
	app = 'new_weixin'
	resource = 'keyword_analysis'

	@login_required
	def api_get(request):
		"""
		关键词分析
		"""
		#获取当前页数
		cur_page = int(request.GET.get('page', '1'))
		#获取每页个数
		count_per_page = int(request.GET.get('count_per_page', 10))

		days = request.GET.get('days', '7')
		keyword = request.GET.get('keyword', '')

		owner_id = request.user.id
		total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
		date_list = [date.strftime("%Y-%m-%d") for date in dateutil.get_date_range_list(low_date, high_date)]
		display_date_list = [date.strftime("%m.%d") for date in dateutil.get_date_range_list(low_date, high_date)]

		records = KeywordCount.objects.filter(owner_id=owner_id, date__range=(low_date, high_date), keyword__contains=keyword).annotate(total_count=Sum('count')).order_by('-total_count')
		new_records = {}

		for record in records:
			new_record = {}
			count = record.count
			if new_records.has_key(record.keyword):
				count += new_records[record.keyword]
			new_records[record.keyword] = count

		new_records = sorted(new_records.items(), key=lambda d:d[1], reverse = True)

		pageinfo, new_records = paginator.paginate(new_records, cur_page, count_per_page, None)

		items = []
		num = 1 #计算排行id使用
		for record in new_records:
			record_item = {}
			record_item['id'] = (cur_page - 1) * count_per_page + num
			num += 1
			record_item['keyword'] = record[0]
			record_item['count'] = record[1]

			items.append(record_item)

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': ''
		}

		return response.get_response()