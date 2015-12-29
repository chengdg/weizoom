# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

from django.template import RequestContext
from django.shortcuts import render_to_response

from core import resource

import models as app_models
from mall.models import Product, OrderHasProduct, Order, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED, \
	ORDER_STATUS_PAYED_NOT_SHIP
from modules.member.models import WebAppUser
from termite2 import pagecreater
from termite import pagestore as pagestore_manager
from webapp.models import WebApp
from weixin.user.module_api import get_mp_qrcode_img

SHORTCUTS_TEXT={
	'phone': u'手机',
	'name': u'姓名',
	'email': u'邮箱',
	'qq':u'QQ号',
	'job':u'职位',
	'addr':u'地址'
}
class Msurvey(resource.Resource):
	app = 'apps/exsurvey'
	resource = 'm_exsurvey'
	
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			id = request.GET['id']
			isPC = request.GET.get('isPC',0)
			isMember = False
			qrcode_url = None
			permission = ''
			share_page_desc = ''
			thumbnails_url = '/static_v2/img/thumbnails_survey.png'
			product_id2product_name = []
			if not isPC:
				isMember = request.member and request.member.is_subscribed
				if not isMember:
					if hasattr(request, "webapp_owner_info") and request.webapp_owner_info and hasattr(request.webapp_owner_info, "qrcode_img") :
						qrcode_url = request.webapp_owner_info.qrcode_img
					else:
						qrcode_url = get_mp_qrcode_img(request.webapp_owner_id)

			participance_data_count = 0
			if 'new_app:' in id:
				project_id = id
				activity_status = u"未开始"
			else:
				#termite类型数据
				try:
					record = app_models.exsurvey.objects.get(id=id)
				except:
					c = RequestContext(request,{
						'is_deleted_data': True
					})
					return render_to_response('workbench/wepage_webapp_page.html', c)
				activity_status = record.status_text
				share_page_desc =record.name
				now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
				data_start_time = record.start_time.strftime('%Y-%m-%d %H:%M')
				data_end_time = record.end_time.strftime('%Y-%m-%d %H:%M')
				if record.status <= 1:
					if data_start_time <= now_time and now_time < data_end_time:
						record.update(set__status=app_models.STATUS_RUNNING)
						activity_status = u'进行中'
					elif now_time >= data_end_time:
						record.update(set__status=app_models.STATUS_STOPED)
						activity_status = u'已结束'

				project_id = 'new_app:exsurvey:%s' % record.related_page_id

			# 	if request.member:
			# 		participance_data_count = app_models.exsurveyParticipance.objects(belong_to=id, member_id=request.member.id).count()
            #
			# 	pagestore = pagestore_manager.get_pagestore('mongo')
			# 	page = pagestore.get_page(record.related_page_id, 1)
			# 	permission = page['component']['components'][0]['model']['permission']
			# is_already_participanted = (participance_data_count > 0)
			# if  is_already_participanted:
			# 	member_id = request.member.id
			# 	try:
			# 		exsurvey_detail,result_list = get_result(id,member_id)
			# 	except:
			# 		c = RequestContext(request,{
			# 			'is_deleted_data': True
			# 		})
			# 		return render_to_response('exsurvey/templates/webapp/result_exsurvey.html', c)
			# 	c = RequestContext(request, {
			# 		'exsurvey_detail': exsurvey_detail,
			# 		'record_id': id,
			# 		'page_title': '用户调研',
			# 		'app_name': "exsurvey",
			# 		'resource': "exsurvey",
			# 		'q_survey': result_list,
			# 		'hide_non_member_cover': True, #非会员也可使用该页面
			# 		'isMember': isMember,
			# 		'qrcode_url': qrcode_url
			# 	})
			# 	return render_to_response('exsurvey/templates/webapp/result_exsurvey.html', c)
			# else:
				pagestore = pagestore_manager.get_pagestore('mongo')
				page = pagestore.get_page(record.related_page_id, 1)
				permission = page['component']['components'][0]['model']['permission']
			participance_datas = None
			member_id = 0
			orderhasproduct_ids = []
			webapp_owner_id = 0
			if not isPC:
				webapp_owner_id = request.GET['webapp_owner_id']
			if request.member:
				member_id = request.member.id
				participance_datas = app_models.exsurveyParticipance.objects(member_id=request.member.id)
				if participance_datas:
					for p in participance_datas:
						termite_data = p.termite_data
						for title,value in termite_data.items():
							if value['type'] == 'appkit.dropdownbox':
								orderhasproduct_ids.append(value['value']['orderhasproduct_id'])
				webappusers =  WebAppUser.objects.filter(member_id=member_id)
				webapp_user_ids = [wau.id for wau in webappusers]
				#获取上个月的时间
				curr_time = datetime.now()
				for m in range(1, 2):
					curr_time = (curr_time.replace(day=1) - timedelta(1)).replace(day=curr_time.day)
				start_date = curr_time.strftime('%Y-%m-%d 00:00:00')
				#现在的时间
				end_date = datetime.now().strftime('%Y-%m-%d 23:59:59')

				#获取当前会员一个月内所下单已发货和已完成的id
				orders = Order.objects.filter(webapp_user_id__in=webapp_user_ids,created_at__gte=start_date, created_at__lte=end_date,status__in=[ORDER_STATUS_PAYED_SHIPED,ORDER_STATUS_SUCCESSED,ORDER_STATUS_PAYED_NOT_SHIP])
				webapp = WebApp.objects.filter(owner_id=webapp_owner_id)
				if webapp.count()>0:
					orders.filter(webapp_id=webapp[0].appid)

				order_ids = [order.id for order in orders]

				#根据订单id获取商品id的dict
				product_id2product = {ohp.product_id:ohp for ohp in OrderHasProduct.objects.filter(order_id__in=order_ids).exclude(id__in=orderhasproduct_ids).order_by('-created_at')}
				#根据商品id获取到商品名称
				for p in Product.objects.filter(id__in=product_id2product.keys()):
					product_id2product_name.append({
						"orderhasproduct_id": product_id2product[p.id].id,
						"product_id": p.id,
						"product_name": p.name,
						"product_supplier_id": p.supplier,
						"product_owner_id": p.owner_id
					})
				product_id2product_name = sorted(product_id2product_name,key= lambda product:product['orderhasproduct_id'])
			request.GET._mutable = True
			request.GET.update({"project_id": project_id})
			request.GET._mutable = False
			html = pagecreater.create_page(request, return_html_snippet=True)
			c = RequestContext(request, {
				'record_id': id,
				'activity_status': activity_status,
				'is_already_participanted': False,
				'page_title': '用户反馈',
				'page_html_content': html,
				'app_name': "exsurvey",
				'resource': "exsurvey",
				'hide_non_member_cover': True, #非会员也可使用该页面
				'isPC': False if request.member else True,
				'isMember': isMember,
				'qrcode_url': qrcode_url,
				'permission': permission,
				'share_page_desc': share_page_desc,
				'share_img_url': thumbnails_url,
				'product_dict': product_id2product_name
			})

			return render_to_response('exsurvey/templates/webapp/m_exsurvey.html', c)
		else:
			record = None
			c = RequestContext(request, {
				'record': record
			})
			return render_to_response('exsurvey/templates/webapp/m_survey.html', c)

# def get_result(id,member_id):
# 	survey_detail ={}
# 	survey_survey = app_models.exsurvey.objects.get(id=id)
# 	survey_detail['name'] = survey_survey['name']
# 	survey_detail['start_time'] = survey_survey['start_time'].strftime('%Y-%m-%d %H:%M')
# 	survey_detail['end_time'] = survey_survey['end_time'].strftime('%Y-%m-%d %H:%M')
#
# 	member_survey_termite = app_models.exsurveyParticipance.objects.filter(belong_to=id,member_id=member_id).order_by('-created_at').first().termite_data
# 	result_list = []
#
# 	for title in sorted(member_survey_termite.keys()):
# 		title_type = member_survey_termite[title]['type']
# 		result = {}
# 		title_name = title.split('_')[1]
# 		if title_type in['appkit.textlist', 'appkit.shortcuts']:
# 			if title_name in SHORTCUTS_TEXT:
# 				title_name = SHORTCUTS_TEXT[title_name]
# 		result['title'] = title_name
# 		result['type'] = title_type
# 		values = member_survey_termite[title]['value']
#
# 		if title_type == 'appkit.selection':
# 			select_values = []
# 			for select_title in sorted(values.keys()):
# 				select_value = {}
# 				select_value['name'] = select_title.split('_')[1]
# 				select_value['type'] = values[select_title]['type']
# 				select_value['isSelect'] = values[select_title]['isSelect']
# 				select_values.append(select_value)
# 			values = select_values
# 		result['values'] = values
#
# 		if title_type == 'appkit.uploadimg':
# 			print member_survey_termite[title]['value']
# 			result['att_urls'] = member_survey_termite[title]['value']
# 		result_list.append(result)
#
#
# 	related_page_id = survey_survey.related_page_id
#
# 	pagestore = pagestore_manager.get_pagestore('mongo')
# 	page = pagestore.get_page(related_page_id, 1)
# 	page_info = page['component']['components'][0]['model']
# 	survey_detail['subtitle'] = page_info['subtitle']
# 	survey_detail['description'] = page_info['description']
# 	prize_type = page_info['prize']['type']
# 	survey_detail['prize_type'] = prize_type
# 	if prize_type == 'coupon':
# 		prize_data = page_info['prize']['data']['name']
# 	else:
# 		prize_data = page_info['prize']['data']
# 	survey_detail['prize_data'] = prize_data
#
# 	return survey_detail,result_list