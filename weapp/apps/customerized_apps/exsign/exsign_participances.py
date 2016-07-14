# -*- coding: utf-8 -*-
import json
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from core import resource
from core import paginator
from core.jsonresponse import create_response
from mall.promotion.models import Coupon
from modules.member import models as member_models
import models as app_models
import export
from modules.member.models import Member
from utils.string_util import hex_to_byte, byte_to_hex

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

class exSignParticipances(resource.Resource):
	app = 'apps/exsign'
	resource = 'exsign_participances'

	@staticmethod
	def get_datas(request):
		sort_attr = request.GET.get('sort_attr', '-latest_date')
		participant_name = request.GET.get('participant_name', '')
		webapp_id = request.user_profile.webapp_id

		datas = app_models.exSignParticipance.objects(belong_to=request.GET['id'])

		if participant_name != '':
			hexstr = byte_to_hex(participant_name)
			members = member_models.Member.objects.filter(webapp_id=webapp_id,username_hexstr__contains=hexstr)
			temp_ids = [member.id for member in members]
			member_ids = temp_ids  if temp_ids else [-1]
			datas = datas.filter(member_id__in=member_ids)

		if 'total_integral' in sort_attr:
			datas = sorted(datas, lambda x,y: cmp(x.prize['integral'], y.prize['integral']), reverse=True if '-' in sort_attr else False)
		elif 'total_coupon' in sort_attr:
			datas = sorted(datas, lambda x,y: cmp(len(x.prize['coupon'].split(',')), len(y.prize['coupon'].split(','))), reverse=True if '-' in sort_attr else False)
		else:
			datas = datas.order_by(sort_attr)
		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		return pageinfo, datas

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		sort_attr = request.GET.get('sort_attr', '-latest_date')
		pageinfo, datas = exSignParticipances.get_datas(request)

		member_ids = []
		for data in datas:
			member_ids.append(data.member_id)
		members = member_models.Member.objects.filter(id__in=member_ids)
		member_id2member = {member.id: member for member in members}

		items = []
		for data in datas:
			coupon_count = 0
			if data.prize['coupon']:
				coupon_count = len(data.prize['coupon'].split(','))
			items.append({
				'id': str(data.id),
				'belong_to': data.belong_to,
				'member_id': data.member_id,
				'participant_name': member_id2member[data.member_id].username_for_html if member_id2member.get(data.member_id) else u'未知',
				'participant_icon': member_id2member[data.member_id].user_icon if member_id2member.get(data.member_id) else '/static/img/user-1.jpg',
				'created_at': data.created_at.strftime("%Y/%m/%d %H:%M:%S"),
				'latest_date': data.latest_date.strftime("%Y/%m/%d %H:%M:%S") if data.latest_date else "",
				'latest_date_f': data.latest_date.strftime("%Y-%m-%d %H:%M:%S") if data.latest_date else "",
				'total_count': data.total_count,
				'serial_count': data.serial_count,
				'top_serial_count': data.top_serial_count,
				'total_integral': data.prize['integral'],
				'coupon_count': coupon_count
			})
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': sort_attr,
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()

class SignParticipancesDetail(resource.Resource):
	'''
	签到详情
	'''
	app = 'apps/sign'
	resource = 'sign_participance_detail'
	def get(request):
		"""
		响应GET
		"""
		member_id = request.GET.get('member_id', None)
		belong_to = request.GET.get('belong_to', None)
		if member_id and belong_to:
			items = app_models.SignDetails.objects(belong_to=belong_to, member_id=int(member_id)).order_by('-created_at')
			sign_member_ids = [item.member_id for item in items]
			member_id2info = {m.id: {'is_subscribed': m.is_subscribed, 'member_name': m.username_for_html} for m in Member.objects.filter(id__in=sign_member_ids)}
			returnDataList = []
			for t in items:
				prize_str = u''
				if t['prize'].get('integral', None):
					prize_str += u'积分奖励: %s <br>' % str(t['prize']['integral'])
				if t['prize'].get('coupon', None):
					prize_str += u'优惠券奖励: %s' % str(t['prize']['coupon']['name'])
				returnDataDict = {
					"member_id": t.member_id,
					"member_name": member_id2info[t.member_id]['member_name'],
					"created_at": t.created_at.strftime("%Y/%m/%d %H:%M"),
					"type": t.type,
					"prize": prize_str
				}
				returnDataList.append(returnDataDict)
			c = RequestContext(request, {
				'items': returnDataList,
				'errMsg': None
			})
		else:
			c = RequestContext(request, {
				'items': None,
				'errMsg': u'member_id或者belong_to不存在'
			})
		return render_to_response('exsign/templates/editor/exsign_participance_detail.html', c)


from apps.customerized_apps.mysql_models import ConsumeCouponLog
from mall.models import *
def get_member_coupons_for_exsign(member, user, project_id, status=-1):
	"""
	得到通过专项签到获得的优惠券信息
	"""
	sign = app_models.exSign.objects.get(related_page_id=project_id)
	consume_doupon_logs = ConsumeCouponLog.objects.filter(member_id=member.id, app_name='exsign', user_id=user.id, app_id="%s"%sign.id)
	consume_doupon_log_ids = [consume_doupon_log.coupon_id for consume_doupon_log in consume_doupon_logs]

	orders = Order.objects.filter(webapp_user_id__in=member.get_webapp_user_ids, coupon_id__gt=1).filter(status__in=[ORDER_STATUS_NOT, ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED])
	coupon_ids = [order.coupon_id for order in orders]

	if status == -1:
		member_coupons = Coupon.objects.filter(Q(member_id=member.id)| Q(id__in=coupon_ids)).filter(id__in=consume_doupon_log_ids).order_by('-provided_time', '-coupon_record_id', '-id')
	else:
		member_coupons = Coupon.objects.filter(Q(member_id=member.id)| Q(id__in=coupon_ids)).filter(id__in=consume_doupon_log_ids).filter(status=status).order_by('-provided_time', '-coupon_record_id', '-id')

	return member_coupons
