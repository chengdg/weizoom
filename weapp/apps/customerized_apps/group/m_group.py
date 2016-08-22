# -*- coding: utf-8 -*-

import json
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from eaglet.utils.resource_client import Resource

from core import resource

import models as app_models
from core.jsonresponse import create_response
from termite2 import pagecreater
from utils import url_helper
from utils.cache_util import GET_CACHE, SET_CACHE
from modules.member.models import Member
from mall.models import *
from weapp import settings
from mall.order.util import update_order_status_by_group_status
from apps.customerized_apps.group.group_participance import send_group_template_message

from watchdog.utils import watchdog_alert, watchdog_info
from core.exceptionutil import unicode_full_stack

class MGroup(resource.Resource):
	app = 'apps/group'
	resource = 'm_group'

	def api_get(request):
		response = create_response(500)
		record_id = request.GET.get('id', None)
		if not record_id:
			response.errMsg = u'活动信息出错'
			return response.get_response()
		group_relation_id = request.GET.get('group_relation_id', None)
		member = request.member
		isMember = False
		timing = 0
		is_group_leader = False
		remain_days = 0 #开团时间剩余天数
		is_helped = False
		self_page = False
		group_status = ''
		group_type = ''
		product_original_price = 0
		product_group_price = 0
		product_mysql_name = ''
		pic_url = ''
		page_owner_name = ''
		page_owner_icon = ''
		page_owner_member_id = 0
		grouped_member_info_list = []
		order_id = ''
		is_from_pay_result = request.GET.get('from', None)
		is_helper_unpaid = False
		if is_from_pay_result == 'pay_result':
			is_from_pay_result = True
		else:
			is_from_pay_result = False

		webapp_owner_id = int(request.GET.get('webapp_owner_id', 0))
		watchdog_info(u'团购流程日志：request.GET[webapp_owner_id]=={}'.format(webapp_owner_id))
		record = app_models.Group.objects(id=record_id, owner_id=webapp_owner_id)
		if record.count() <= 0:
			response.errMsg = 'is_deleted'
			return response.get_response()

		record = record.first()
		#获取活动状态
		activity_status = record.status_text
		if activity_status == u'已结束':
			record.update(set__status=app_models.STATUS_STOPED)
		#开团时间不足一天
		remain_days = (record.end_time-datetime.today()).total_seconds() / (60*60*24)

		try:
			product_id = record.product_id
			product_original_price = ProductModel.objects.get(product_id=product_id,is_standard=True).price
			product = Product.objects.get(id=product_id)
			product_mysql_name = product.name
			pic_url = product.thumbnails_url
			if product_mysql_name != record.product_name:#如果商品被改名了
				record.update(set__product_name=product_mysql_name)
				record.reload()
			if pic_url != record.product_img:
				record.update(set__product_img=pic_url)
				record.reload()
		except:
			response.errMsg = u'团购商品已不存在！'
			return response.get_response()
		if member:
			member_id = member.id
			fid = request.GET.get('fid')
			if fid == 'null':
				fid = member_id
			isMember =member.is_subscribed
			if activity_status in [u"进行中", u'已结束']:
				if not group_relation_id:
					group_relation = app_models.GroupRelations.objects(belong_to=record_id,member_id=str(member_id))
					if group_relation.count() > 0:
						group_relation_id = group_relation.first().id
				if group_relation_id:
					# 已经开过团
					try:
						group_relation_info = app_models.GroupRelations.objects.get(id=group_relation_id)
						group_status = group_relation_info.status_text
						group_type = group_relation_info.group_type
						product_group_price = group_relation_info.group_price
						timing = (group_relation_info.created_at + timedelta(days=int(group_relation_info.group_days)) - datetime.today()).total_seconds()
						if timing <= 0 and group_relation_info.group_status == app_models.GROUP_RUNNING:
							group_relation_info.update(set__group_status=app_models.GROUP_FAILURE)
							# update_order_status_by_group_status(group_relation_info.id,'failure')
							resp = Resource.use('zeus').post({
								'resource': 'mall.group_update_order',
								'data': {
									'group_id': group_relation_info.id,
									'status': 'failure',
									'is_test': 1 if request.GET.get('is_test', False) else 0
								}
							})
							if resp and resp['code'] == 200:
								#发送拼团失败模板消息
								try:
									group_details = app_models.GroupDetail.objects(relation_belong_to=str(group_relation_id))
									owner_id = record.owner_id
									product_name = record.product_name
									miss = int(group_relation_info.group_type)-group_details.count()
									activity_info = {
										"owner_id": str(owner_id),
										"record_id": str(record_id),
										"group_id": str(group_relation_id),
										"fid": str(group_relation_info.member_id),
										"price": '%.2f' % group_relation_info.group_price,
										"product_name": product_name,
										"status" : 'fail',
										"miss": str(miss)
									}

									member_info_list = [{"member_id": group_detail.grouped_member_id, "order_id": group_detail.order_id} for group_detail in group_details]
									send_group_template_message(activity_info, member_info_list)
								except:
									watchdog_alert(u'发送团购失败模版消息失败， cause：\n{}'.format(unicode_full_stack()))

						# 获取该主页帮助者列表
						helpers = app_models.GroupDetail.objects(relation_belong_to=str(group_relation_id), owner_id=fid, order_id__ne='').order_by('created_at')
						member_ids = [h.grouped_member_id for h in helpers]
						member_id2member = {m.id: m for m in Member.objects.filter(id__in=member_ids)}
						for h in helpers:
							temp_dict = {
								'member_id': h.grouped_member_id,
								'user_icon': member_id2member[h.grouped_member_id].user_icon,
								'username': member_id2member[h.grouped_member_id].username_size_ten
							}
							grouped_member_info_list.append(temp_dict)

						#判断分享页是否自己的主页
						if fid is None or str(fid) == str(member_id):
							is_group_leader = True if (group_relation_info.member_id == str(member_id) and group_relation_info.group_status != app_models.GROUP_NOT_START) else False
						else:
							try:
								group_detail = app_models.GroupDetail.objects.get(relation_belong_to=str(group_relation_id),owner_id=fid,grouped_member_id=member_id)
								if ( group_detail.is_already_paid and (member_id in member_ids)):
									is_helped = True
							except:
								pass
						try:
							group_detail = app_models.GroupDetail.objects.get(relation_belong_to=str(group_relation_id),owner_id=fid,grouped_member_id=member_id)
							order_id = group_detail.order_id
							if not group_detail.is_already_paid:
								if order_id!='':
									is_helper_unpaid = True
						except:
							pass
					except:
						watchdog_alert(u'该团购已不存在！cause: \n{}'.format(unicode_full_stack()))
						response = create_response(500)
						response.errMsg = u'该团购已不存在！'
						return response.get_response()
			if group_relation_id:#已开过团
				#判断分享页是否自己的主页
				if fid is None or str(fid) == str(member_id):
					page_owner_name = member.username_size_ten
					page_owner_icon = member.user_icon
					page_owner_member_id = member_id
					self_page = True
				else:
					page_owner = Member.objects.get(id=fid)
					page_owner_name = page_owner.username_size_ten
					page_owner_icon = page_owner.user_icon
					page_owner_member_id = fid
			else:#没开过团
				page_owner_name = member.username_size_ten
				page_owner_icon = member.user_icon
				page_owner_member_id = member_id
				self_page = True

		member_info = {
			'isMember': isMember,
			'timing': timing,
			'self_page': self_page,
			'is_helped': is_helped,
			'is_group_leader': is_group_leader,
			'page_owner_name': page_owner_name,
			'page_owner_icon': page_owner_icon,
			'page_owner_member_id': page_owner_member_id,
			'activity_status': activity_status,
			'group_status': group_status, #小团购状态
			'group_type': int(group_type) if group_type !='' else '',
			'grouped_number': len(grouped_member_info_list),
			'member_id': member_id if member else '',
			'remain_days': remain_days,
			'product_original_price': product_original_price,
			'product_mysql_name': product_mysql_name,
			'pic_url': pic_url,
			'product_group_price': product_group_price,
			'order_id': order_id,
			'is_from_pay_result': is_from_pay_result,
			'is_helper_unpaid': is_helper_unpaid,
			'group_relation_id': str(group_relation_id) if group_relation_id else ''
		}

		response = create_response(200)
		response.data = {
			'member_info': member_info,
			'helpers_info': grouped_member_info_list
		}
		return response.get_response()

	def get(request):
		"""
		响应GET
		"""
		try:
			record_id = request.GET.get('id','id')
			mpUserPreviewName = ''
			activity_status = u"未开始"
			member = request.member
			fid = 0
			group_relation_id = None
			product_id = None

			if 'new_app:' in record_id:
				project_id = record_id
				record_id = 0
				record = None
			elif member:
				member_id = member.id
				fid = request.GET.get('fid', None)
				group_relation_id = request.GET.get('group_relation_id', None)

				#判断分享页是否自己的主页
				# if not fid:
				# 	new_url = url_helper.add_query_part_to_request_url(request.get_full_path(), 'fid', member_id)
				# 	response = HttpResponseRedirect(new_url)
				# 	response.set_cookie('fid', member_id, max_age=60*60*24*365)
				# 	return response

				if not group_relation_id:
					group_relation = app_models.GroupRelations.objects(belong_to=record_id, member_id=str(member_id))
					if group_relation.count() > 0:
						group_relation = group_relation.first()
						group_detail = app_models.GroupDetail.objects(
							relation_belong_to = str(group_relation.id),
							owner_id = str(member_id),
							grouped_member_id = str(member_id),
						)
						if group_detail.count() > 0: #已成功开团
							if group_relation.group_status != app_models.GROUP_NOT_START:
								new_url_1 = url_helper.add_query_part_to_request_url(request.get_full_path(), 'group_relation_id', str(group_relation.id))
								new_url = url_helper.add_query_part_to_request_url(new_url_1, 'fid', member_id)
								response = HttpResponseRedirect(new_url)
								response.set_cookie('group_relation_id', str(group_relation.id), max_age=60*60*24*365)
								return response

				# cache_key = 'apps_group_%s_html' % record_id
				# # 从redis缓存获取静态页面
				# cache_data = GET_CACHE(cache_key)
				# if cache_data:
				# 	print 'redis---return'
				# 	return HttpResponse(cache_data)

				webapp_owner_id = int(request.GET.get('webapp_owner_id', 0))
				watchdog_info(u'团购流程日志：request.GET[webapp_owner_id]=={}'.format(webapp_owner_id))
				record = app_models.Group.objects(id=record_id, owner_id=webapp_owner_id)
				if record.count() > 0:
					record = record.first()
					record.update(add_to_set__visited_member=member_id)
					#获取公众号昵称
					mpUserPreviewName = request.webapp_owner_info.auth_appid_info.nick_name
					#获取活动状态
					activity_status = record.status_text
					if activity_status == u'已结束':
						record.update(set__status=app_models.STATUS_STOPED)
					product_id = record.product_id
					project_id = 'new_app:group:%s' % record.related_page_id
				else:
					c = RequestContext(request, {
						'is_deleted_data': True
					})
					return render_to_response('group/templates/webapp/m_group.html', c)

			else:
				record = app_models.Group.objects(id=record_id)
				if record.count() >0:
					record = record.first()
					#获取活动状态
					activity_status = record.status_text
					if activity_status == u'已结束':
						record.update(set__status=app_models.STATUS_STOPED)
					project_id = 'new_app:group:%s' % record.related_page_id
				else:
					c = RequestContext(request, {
						'is_deleted_data': True
					})
					return render_to_response('group/templates/webapp/m_group.html', c)

			request.GET._mutable = True
			request.GET.update({"project_id": project_id})
			request.GET._mutable = False
			html = pagecreater.create_page(request, return_html_snippet=True)

			c = RequestContext(request, {
				'record_id': record_id,
				'group_relation_id': group_relation_id, #小团购id，如不存在则为None
				'product_id': product_id, #产品id，如不存在则为None
				'activity_status': activity_status,
				'page_title': record.name if record else u"团购",
				'page_html_content': html,
				'app_name': "group",
				'resource': "group",
				'hide_non_member_cover': True, #非会员也可使用该页面
				'isPC': False if request.member else True,
				'share_page_title': mpUserPreviewName,
				'share_img_url': record.material_image if record else '',
				'share_page_desc': record.share_description.replace('<br>', ' ') if record else u"团购",
				'share_to_timeline_use_desc': True,  #分享到朋友圈的时候信息变成分享给朋友的描述
				'settings_domain': settings.APPS_H5_DOMAIN
			})
			response = render_to_string('group/templates/webapp/m_group.html', c)
			# if request.member:
			# 	SET_CACHE(cache_key, response)
			return HttpResponse(response)
		except:
			watchdog_alert(u'团购页面跳转失败，cause:\n{}'.format(unicode_full_stack()))
			c = RequestContext(request, {
				'is_deleted_data': True
			})
			return render_to_response('group/templates/webapp/m_group.html', c)

class GetProductDetail(resource.Resource):
	app = 'apps/group'
	resource = 'get_product_detail'

	def api_get(request):
		product_detail = ''
		product_id = request.GET.get('product_id')
		try:
			product_detail = Product.objects.get(id=product_id).detail
		except:
			pass
		response = create_response(200)
		response.data = {
			'product_detail': product_detail
		}
		return response.get_response()