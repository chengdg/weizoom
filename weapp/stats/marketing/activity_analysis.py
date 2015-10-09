# -*- coding: utf-8 -*-

import json
#from datetime import datetime
#from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
#from django.db.models import F

from stats import export
from core import resource
from core import paginator
from core.jsonresponse import create_response
#from weixin.mp_decorators import mp_required
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from market_tools.tools.lottery.models import Lottery, LotteryRecord
import utils.dateutil as dateutil
from market_tools.tools.lottery.models import STATUS2TEXT as LOTTERY_STATUS2TEXT

FIRST_NAV = export.STATS_HOME_FIRST_NAV
DEFAULT_COUNT_PER_PAGE = 20


class ActivityAnalysis(resource.Resource):
	"""
	营销活动分析
	"""
	app = 'stats'
	resource = 'activity_analysis'

	#@mp_required
	@login_required
	def get(request):
		"""
		显示营销活动分析的页面
		"""
		activity_type = request.GET.get('type', 'lottery')
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'app_name': 'stats',
			'second_navs': export.get_stats_second_navs(request),
			'second_nav_name': export.STATS_SALES_SECOND_NAV,
			'third_nav_name': export.MARKETING_ACTIVITY_NAV,
			'activity_type': activity_type
		})
		return render_to_response('marketing/activity_analysis.html', c)


	@login_required
	def api_get(request):
		"""
		获取营销活动的列表

		@see  channel_qrcode/api_view.py

		"""
		# 分析活动的类型: qrcode, lottery
		activity_type = request.GET.get('type', 'qrcode')

		# 获取分页数据
		cur_page = int(request.GET.get('page', '1'))
		# 获取每页个数
		count_per_page = int(request.GET.get('count_per_page', DEFAULT_COUNT_PER_PAGE))

		items = []
		if activity_type == 'qrcode':
			# 处理排序
			sort_attr = request.GET.get('sort_attr', '-created_at')
			if sort_attr == '':
				sort_attr = '-created_at'

			# 渠道二维码
			settings = ChannelQrcodeSettings.objects.filter(owner=request.user).order_by(sort_attr)
			#setting_ids = [s.id for s in settings]
			# 分页处理
			pageinfo, settings = paginator.paginate(settings, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
			#  构造items
			for setting in settings:
				# 渠道扫码活动的参与人数
				# TODO: 需要优化
				members = ChannelQrcodeHasMember.objects.filter(channel_qrcode=setting.id)
				participant_times = members.count()
				participant_count = len( set([item['member_id'] for item in  members.values("member_id")]) )
				items.append({
					'id': setting.id,
					'name': setting.name,
					'manager': request.user.username,
					'parti_times': participant_times, # 参与次数
					'parti_person_cnt': participant_count, # 参与人数
					'start_at': dateutil.datetime2string(setting.created_at),
					'end_at': '-',
					'status_text': '已启动',
					'status': 1,
				})
		elif activity_type == 'lottery':
			# 处理排序
			sort_attr = request.GET.get('sort_attr', '-end_at')
			if sort_attr == '':
				sort_attr = '-end_at'

			lotteries = Lottery.objects.filter(owner=request.user, is_deleted=False).order_by(sort_attr)
			# 分页处理
			pageinfo, lotteries = paginator.paginate(lotteries, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
			#  构造items
			for setting in lotteries:
				# 参考: market_tools/tools/lottery/views.py
				# 渠道扫码活动的参与人数
				setting.check_time()
				participant_times = LotteryRecord.objects.filter(lottery=setting).values("id").count() # 参与次数
				# TODO: 需要优化 获取参与人数
				participant_count = len( set([item['member_id'] for item in  LotteryRecord.objects.filter(lottery_id=setting.id).values("member_id")]) )
				item = {
					'id': setting.id,
					'name': setting.name,
					'manager': request.user.username,
					'parti_times': participant_times, # 参与次数
					'parti_person_cnt': participant_count, # 参与人数
					'start_at': dateutil.date2string(setting.start_at),
					'end_at': dateutil.date2string(setting.end_at),
					'status_text': '-',
					'status': setting.status,
				}
				if setting.status < len(LOTTERY_STATUS2TEXT):
					item['status_text'] = LOTTERY_STATUS2TEXT[setting.status]
				items.append(item)
		
		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': sort_attr,
			'data': {},
			'type': activity_type,
		}
		return response.get_response()
