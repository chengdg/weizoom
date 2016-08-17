# -*- coding: utf-8 -*-

#import json
from core import dateutil
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import Sum

from stats import export
from core import resource
from core import paginator
from core.jsonresponse import create_response

import stats.util as stats_util
from modules.member.models import Member, MemberSharedUrlInfo,MemberFollowRelation
from market_tools.tools.member_qrcode.models import MemberQrcode, MemberQrcodeLog
from core.charts_apis import create_line_chart_response

FIRST_NAV = export.STATS_HOME_FIRST_NAV
DEFAULT_COUNT_PER_PAGE = 20


class MemberSummary(resource.Resource):
	"""
	会员概况分析
	"""
	app = 'stats'
	resource = 'member_summary'

	#@mp_required
	@login_required
	def get(request):
		"""
		显示营销活动分析的页面
		"""
		#默认显示最近7天的日期
		end_date = dateutil.get_today()
		start_date = dateutil.get_previous_date(end_date, 6) #获取7天前日期

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_stats_second_navs(request),
			'second_nav_name': export.STATS_MEMBER_SECOND_NAV,
			'third_nav_name': export.MEMBER_SUMMARY_NAV,
			'start_date': start_date,
			'end_date': end_date,

		})
		return render_to_response('member/member_summary.html', c)

	@login_required
	def api_get(request):
		"""
		会员概况分析API，获取基础数据和会员来源12项数据
		"""
		# 时间区间
		low_date, high_date, date_range = stats_util.get_date_range(request)
		webapp_id = request.user_profile.webapp_id

		#会员总数
		total_member_count = stats_util.get_total_member_count(webapp_id)
		#新增会员
		new_member_count = stats_util.get_new_member_count(webapp_id, low_date, high_date)
		#新增手机绑定
		binding_phone_member_count = stats_util.get_binding_phone_member_count(webapp_id, low_date, high_date)
		#关注会员
		subscribed_member_count = stats_util.get_subscribed_member_count(webapp_id)
		#下单会员
		bought_member_count = stats_util.get_bought_member_count(webapp_id, low_date, high_date)
		#会员复购率
		repeat_buying_member_count = stats_util.get_repeat_buying_member_count(webapp_id, low_date, high_date)
		repeat_buying_member_rate = '0.00%'
		if bought_member_count > 0:
			repeat_buying_member_rate = str(round(((repeat_buying_member_count + 0.0) / bought_member_count) * 100, 2)) + '%'
			if str(repeat_buying_member_rate) == '0.0%':
				repeat_buying_member_rate = '0.00%'
		#发起扫码会员和扫码新增会员
		ori_qrcode_member_count, member_from_qrcode_count = stats_util.get_ori_qrcode_member_count(webapp_id, low_date, high_date)
		#发起链接会员
		share_url_member_count = stats_util.get_share_url_member_count(webapp_id, low_date, high_date)
		#直接关注会员
		self_follow_member_count = stats_util.get_self_follow_member_count(webapp_id, low_date, high_date)
		#分享链接新增会员
		member_from_share_url_count = stats_util.get_member_from_share_url_count(webapp_id, low_date, high_date)
		#会员推荐率
		member_recommend_rate = '0.00%'
		_total_member_count = stats_util.get_total_member_count(webapp_id, high_date)
		if _total_member_count > 0:
			member_recommend_rate = str(round(((share_url_member_count + ori_qrcode_member_count + 0.0) / _total_member_count) * 100, 2)) + '%'
			if str(member_recommend_rate) == '0.0%':
				member_recommend_rate = '0.00%'

		item = {
			'total_member_count': total_member_count,
			'subscribed_member_count': subscribed_member_count,
			'new_member_count': new_member_count,
			'binding_phone_member_count': binding_phone_member_count,
			'bought_member_count': bought_member_count,
			'repeat_buying_member_rate': repeat_buying_member_rate,
			'ori_qrcode_member_count': ori_qrcode_member_count,
			'share_url_member_count': share_url_member_count,
			'member_from_qrcode_count': member_from_qrcode_count,
			'self_follow_member_count': self_follow_member_count,
			'member_from_share_url_count': member_from_share_url_count,
			'member_recommend_rate': member_recommend_rate
		}
		response = create_response(200)
		response.data = {
			'items': item,
			'sortAttr': ''
		}

		return response.get_response()

class MemberIncreasement(resource.Resource):
	"""
	会员增长趋势
	"""
	app = 'stats'
	resource = 'member_increasement'

	@login_required
	def api_get(request):
		low_date, high_date, date_range = stats_util.get_date_range(request)
		webapp_id = request.user_profile.webapp_id
		date_formatter = stats_util.TYPE2FORMATTER['day']

		#新增会员数
		date2new_member_count = stats_util.get_date2new_member_count(webapp_id, low_date, high_date)

		#下单会员数
		date2bought_member_count = stats_util.get_date2bought_member_count(webapp_id, low_date, high_date)

		#绑定手机会员数
		date2binding_phone_member_count = stats_util.get_date2binding_phone_member_count(webapp_id, low_date, high_date)

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
		return create_line_chart_response('', '', x_values, y_values)

class MemberShareUrlRank(resource.Resource):
	"""
	分享链接排行
	"""
	app = 'stats'
	resource = 'member_share_url_rank'

	@login_required
	def api_get(request):
		low_date, high_date, date_range = stats_util.get_date_range(request)
		webapp_id = request.user_profile.webapp_id

		rank_list = _get_member_share_url_rank(webapp_id, low_date, high_date)

		response = create_response(200)
		response.data = {
			'items': rank_list,
			'sortAttr': ''
		}

		return response.get_response()

class MemberQrcodeRank(resource.Resource):
	"""
	会员扫码排行
	"""
	app = 'stats'
	resource = 'member_qrcode_rank'

	@login_required
	def api_get(request):
		low_date, high_date, date_range = stats_util.get_date_range(request)
		webapp_id = request.user_profile.webapp_id

		rank_list = _get_member_qrcode_rank(webapp_id, low_date, high_date)

		response = create_response(200)
		response.data = {
			'items': rank_list,
			'sortAttr': ''
		}

		return response.get_response()

class MemberDetailData(resource.Resource):
	"""
	会员详细数据
	"""
	app = 'stats'
	resource = 'member_detail_data'

	@login_required
	def api_get(request):
		low_date, high_date, date_range = stats_util.get_date_range(request)
		date_formatter = stats_util.TYPE2FORMATTER['day']
		formatted_date_list = stats_util.get_formatted_date_list(date_range, date_formatter)
		formatted_date_list.reverse()  #反转日期列表，使之按日期倒序

		#获取当前页数
		cur_page = int(request.GET.get('page', '1'))
		#获取每页个数
		count_per_page = int(request.GET.get('count_per_page', 10))
		#先根据日期进行分页，避免全部查询出来的时候再分页，浪费时间降低效率
		pageinfo, formatted_date_list = paginator.paginate(formatted_date_list, cur_page, count_per_page, None)

		#根据当页的日期再获取一次low_date和high_date
		low_date, high_date, date_range = stats_util.get_date_range_for_data(request, formatted_date_list[-1], formatted_date_list[0])

		webapp_id = request.user_profile.webapp_id

		#新增会员
		date2new_member_count = stats_util.get_date2new_member_count(webapp_id, low_date, high_date)
		#手机绑定会员
		date2binding_phone_member_count = stats_util.get_date2binding_phone_member_count(webapp_id, low_date, high_date)
		#发起分享链接
		date2share_url_member_count = stats_util.get_date2share_url_member_count(webapp_id, low_date, high_date)
		#发起链接新增
		date2member_from_share_url_count = stats_util.get_date2member_from_share_url_count(webapp_id, low_date, high_date)
		#发起扫码和扫码新增
		date2qrcode_member_count = stats_util.get_date2ori_qrcode_member_count(webapp_id, low_date, high_date)
		#下单会员
		date2bought_member_count = stats_util.get_date2bought_member_count(webapp_id, low_date, high_date)



		items = []
		for date in formatted_date_list:
			new_member_count = 0
			if date2new_member_count.has_key(date):
				new_member_count = date2new_member_count[date]

			binding_phone_member_count = 0
			if date2binding_phone_member_count.has_key(date):
				binding_phone_member_count = date2binding_phone_member_count[date]

			share_url_member_count = 0
			if date2share_url_member_count.has_key(date):
				share_url_member_count = date2share_url_member_count[date]

			member_from_share_url_count = 0
			if date2member_from_share_url_count.has_key(date):
				member_from_share_url_count = date2member_from_share_url_count[date]

			ori_qrcode_member_count = 0
			member_from_qrcode_count = 0
			if date2qrcode_member_count.has_key(date):
				if date2qrcode_member_count[date].has_key('ori_qrcode_member_count'):
					ori_qrcode_member_count = date2qrcode_member_count[date]['ori_qrcode_member_count']
				if date2qrcode_member_count[date].has_key('member_from_qrcode_count'):
					member_from_qrcode_count = date2qrcode_member_count[date]['member_from_qrcode_count']

			bought_member_count = 0
			if date2bought_member_count.has_key(date):
				bought_member_count = date2bought_member_count[date]

			items.append({
				'date': date,
				'new_member_count': new_member_count,
				'binding_phone_member_count': binding_phone_member_count,
				'share_url_member_count': share_url_member_count,
				'member_from_share_url_count': member_from_share_url_count,
				'ori_qrcode_member_count': ori_qrcode_member_count,
				'member_from_qrcode_count': member_from_qrcode_count,
				'bought_member_count': bought_member_count
			})

		# #获取当前页数
		# cur_page = int(request.GET.get('page', '1'))
		# #获取每页个数
		# count_per_page = int(request.GET.get('count_per_page', 10))

		# pageinfo, items = paginator.paginate(items, cur_page, count_per_page, None)


		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': ''
		}

		return response.get_response()


def _get_member_qrcode_rank(webapp_id, low_date, high_date):
	"""
	获取会员扫码效果排行（按带来的会员数排名）
	"""
	member_qrcodes = MemberQrcode.objects.filter(
						member__webapp_id=webapp_id,
						# member__is_subscribed=True,
						member__is_for_test=False,
						created_at__range=(low_date, high_date)
					)
	qrcode_id2member_id = {}
	qrcode_ids = []
	for member_qrcode in member_qrcodes:
		qrcode_id2member_id[member_qrcode.id] = member_qrcode.member_id
		qrcode_ids.append(member_qrcode.id)

	member_qrcode_logs = MemberQrcodeLog.objects.filter(member_qrcode_id__in = qrcode_ids)

	member_id2count = {}  #发起会员扫码的会员带来的会员个数
	member_id2follower_member_id = {}
	#处理通过扫码新增的用户列表
	for log in member_qrcode_logs:
		#已经取消关注的也计算在内
		member_id = qrcode_id2member_id[log.member_qrcode_id]
		if not member_id2follower_member_id.has_key(member_id):
			member_id2follower_member_id[member_id] = []
		member_id2follower_member_id[member_id].append(log.member_id)
	for member_id, values in member_id2follower_member_id.items():
		fans_count = MemberFollowRelation.objects.filter(member_id=member_id, follower_member_id__in=values, is_fans=True).count()
		member_id2count[member_id] = fans_count
	#按带来的会员个数倒序
	sorted_member_id2count = sorted(member_id2count.items(), key=lambda d:d[1], reverse = True)

	#收集数据
	rank_list = []
	i = 1
	for item in sorted_member_id2count:
		username = '-'
		member_id = item[0]
		try:
			member = Member.objects.get(id=member_id)
			username = member.username_for_html
		except:
			pass

		rank_list.append({
			'rank': i,
			'member_id': member_id,
			'username': username,
			'followers': item[1]
		})

		i += 1
		if i > 10:
			break

	return rank_list


def _get_member_share_url_rank(webapp_id, low_date, high_date):
	"""
	获取分享链接效果排行（按带来的会员数排名）
	"""
	share_url_members = MemberSharedUrlInfo.objects.filter(
							created_at__range=(low_date, high_date),
							member__webapp_id=webapp_id,
							# member__is_subscribed=True,
							member__is_for_test=False
						)#.values('member_id').annotate(total_followers=Sum('followers')).order_by('-total_followers')

	member_id2followers = {}
	for share_url_member in share_url_members:
		if not member_id2followers.has_key(share_url_member.member_id):
			member_id2followers[share_url_member.member_id] = 0
			fans_count = MemberFollowRelation.get_follow_members_for(share_url_member.member_id, '1')
			qrcode_friends = 0
			if fans_count:
				qrcode_friends = fans_count.filter(source=1).count()

			member_id2followers[share_url_member.member_id] = fans_count.count() - qrcode_friends

	#按粉丝数量倒序
	sorted_member_id2followers = sorted(member_id2followers.items(), key=lambda d:d[1], reverse = True)

	#收集数据
	rank_list = []
	i = 1
	for item in sorted_member_id2followers:
		username = '-'
		member_id = item[0]
		followers = item[1]
		if followers == 0:
			continue
		try:
			member = Member.objects.get(id=member_id)
			username = member.username_for_html
		except:
			pass

		rank_list.append({
			'rank': i,
			'member_id': member_id,
			'username': username,
			'followers': followers
		})

		i += 1
		if i> 10:
			break

	return rank_list