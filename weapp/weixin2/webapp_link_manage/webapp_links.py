# -*- coding: utf-8 -*-
from datetime import datetime
from mall.promotion.models import CouponRule

__author__ = 'liupeiyu'

import os
import json
import requests

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import F
from django.conf import settings

from weixin2 import export
import weixin2.models as weixin_models
from core import resource
from core import paginator
from core.jsonresponse import create_response
import utils as webapp_link_utils
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error


COUNT_PER_PAGE = 20
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV


class WebappLinkMenus(resource.Resource):
	"""
	webapp链接Menu资源
	"""
	app = 'new_weixin'
	resource = 'webapp_link_menus'

	@login_required
	def api_get(request):
		"""
		获取链接的menu集合的json表示
		"""
		memus = webapp_link_utils.get_webapp_link_menu_objectes(request)

		#用户反馈只在指定的帐号下显示
		titles = memus['marketPage']['title']
		for title in titles:
			if title['type'] in ['exsurvey', 'shvote'] and not request.manager.username in title['users']:
				memus['marketPage']['title'].remove(title)

		response = create_response(200)
		response.data = memus
		return response.get_response()


class WebappItemLinks(resource.Resource):
	"""
	webapp链接资源
	"""
	app = 'new_weixin'
	resource = 'webapp_item_links'

	LOTTER_TYPE = [u'刮刮卡', u'砸金蛋', u'大转盘']

	@login_required
	def api_get(request):
		"""
		获取链接集合的json表示
		"""
		query = request.GET.get('query', None)
		link_type = request.GET.get('type', None)
		menu_type = request.GET.get('menu_type', '')
		selected_link_target = request.GET.get('selected_link_target', '')
		order_by = request.GET.get('sort_attr', '-id')

		selected_id = 0
		# 根据link_target获取已选的id跟type
		selected_id, is_selected_type = webapp_link_utils.get_selected_by_link_target(request, menu_type, link_type, selected_link_target)
		request.selected_id = selected_id

		URL = "http://%s/apps/export/api/get_app_items/?webapp_owner_id=%s&link_type=%s&query=%s" % (settings.MARKETAPP_DOMAIN, str(request.manager.id), link_type, query)


		try:
			api_resp_text = requests.get(URL).text
			print URL, 'marketapp get_app_items===============>>>', api_resp_text
			api_resp = json.loads(api_resp_text)
		except:
			api_resp = {}
			notify_message = u"api request marketapp get_app_link failed:::: ".format(unicode_full_stack())
			watchdog_error(notify_message)

		if api_resp.get('data', None):
			api_data = api_resp['data']
			link_targets = api_data['link_targets']
			pageinfo = api_data['pageinfo']
			response = create_response(200)
			response.data = {
				'items': link_targets,
				'pageinfo': pageinfo,
				'sortAttr': order_by,
				'data': {},
				'type': link_type
			}
		elif api_resp.get('errMsg', None) and 'invalid' == api_resp['errMsg']:
			objects, menu_item = webapp_link_utils.get_webapp_link_objectes_for_type(request, link_type, query, order_by)

			if link_type == "shengjing_app":
				items = []
				for item in objects[0]['data']:
					shengjing = {}
					shengjing['id'] = item['id']
					shengjing['name'] = item['text']
					shengjing['link'] = item['link'].format(item['id'])
					shengjing['isChecked'] = True if is_selected_type and item['id'] == selected_id else False
					items.append(shengjing)
				response = create_response(200)
				response.data = {
					'items':items,
					'type': link_type
				}

			else:
				count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
				cur_page = int(request.GET.get('page', '1'))
				pageinfo, objects = paginator.paginate(objects, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
				items = []
				for item in objects:
					data = dict()
					if link_type == 'red_envelope':
						items.append(item)
					else:
						data['id'] = item.id
						data['created_at'] = item.created_at if isinstance(item.created_at, str) else item.created_at.strftime('%Y-%m-%d %H:%M:%S')
						data['name'] = item.name
						data['link'] = menu_item['link_template'].format(item.id)
						data['isChecked'] = True if is_selected_type and item.id == selected_id else False
						if link_type == 'webappPage':
							# 微页面
							data['name'] = item.site_title

						if link_type == 'lottery':
							# 抽奖
							data['type'] = WebappItemLinks.LOTTER_TYPE[item.type]
							data['valid'] = u'{} 至 {}'.format(item.start_at.strftime("%Y-%m-%d"), item.end_at.strftime("%Y-%m-%d"))

						if link_type == 'coupon':
							# 优惠券
							data['type'] = '多商品劵' if item.detail['limit_product'] else '通用劵'
							data['end_date'] = item.end_date if isinstance(item.end_date, str) else item.end_date.strftime('%Y-%m-%d %H:%M')
							data['created_at'] = data['created_at'][:16] if len(data['created_at']) > 16 else data['created_at']
							data['end_date'] = data['end_date'][:16] if len(data['end_date']) > 16 else data['end_date']
							data['valid'] = u'{} 至 {}'.format(data['created_at'], data['end_date'])
							data['link'] = menu_item['link_template'].format(item.detail['id'])

						if link_type == 'activity':
							# 活动
							data['valid'] = u'{} 至 {}'.format(item.start_date, item.end_date)
						items.append(data)

				response = create_response(200)
				response.data = {
					'items': items,
					'pageinfo': paginator.to_dict(pageinfo),
					'sortAttr': order_by,
					'data': {},
					'type': link_type
				}
		else:
			response = create_response(500)
			response.errMsg = 'get %s datas failed' % link_type
		return response.get_response()
