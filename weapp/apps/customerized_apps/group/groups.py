# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from eaglet.utils.resource_client import Resource

from apps.models import UserHasTemplateMessages, UserappHasTemplateMessages
from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as app_models
import export
from datetime import datetime
from mall import export as mall_export
from mall.order.util import update_order_status_by_group_status
from apps.customerized_apps.group.group_participance import send_group_template_message

import weixin2.models as weixin_models

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 10

class Groups(resource.Resource):
	app = 'apps/group'
	resource = 'groups'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.Group.objects.count()
		#从数据库中获取模板配置
		templates = weixin_models.UserHasTemplateMessages.objects.filter(owner_id=request.manager.id)
		um = weixin_models.UserTemplateSettings.objects.filter(owner_id=request.manager.id, usage__in=[1,2])
		control_data = dict()
		tem_list = []
		if um.count() > 0:
			for u in um:
				if u.usage == 1:
					control_data['success'] = {
						'template_id': u.template_id,
						'first': u.first
					}
				elif u.usage == 2:
					control_data['fail'] = {
						'template_id': u.template_id,
						'first': u.first
					}
		for t in templates:
			tem_list.append({
				"template_id": t.template_id,
				"template_title": t.title
			})
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': "groups",
			'has_data': has_data,
			'template_data': json.dumps({"hasData": 0 if len(tem_list) <= 0 else 1, "templates": tem_list, "control_data": control_data})
		})

		return render_to_response('group/templates/editor/groups.html', c)

	@staticmethod
	def get_datas(request):
		group_name = request.GET.get('group_name', '')
		product_name = request.GET.get('product_name', '')
		status = int(request.GET.get('status', -1))
		handle_status = int(request.GET.get('handle_status', 0))
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')

		now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
		params = {'owner_id':request.manager.id}
		datas_datas = app_models.Group.objects(**params)
		for data_data in datas_datas:
			data_start_time = data_data.start_time.strftime('%Y-%m-%d %H:%M')
			data_end_time = data_data.end_time.strftime('%Y-%m-%d %H:%M')
			handle_status = int(data_data.handle_status)#手动开启状态
			if handle_status == 0:#手动关闭(默认)
				pass
			elif handle_status == 1:#手动开启
				if data_start_time <= now_time and now_time < data_end_time:
					data_data.update(set__status=app_models.STATUS_RUNNING)
			if now_time >= data_end_time:
				data_data.update(set__status=app_models.STATUS_STOPED)
				#活动已结束，所有进行中的小团置为失败
				running_group_relations = app_models.GroupRelations.objects(belong_to=data_data.id,group_status=app_models.GROUP_RUNNING)
				for group_relation in running_group_relations:
					group_relation.update(group_status=app_models.GROUP_FAILURE)
					group_relation_id = group_relation.id
					# update_order_status_by_group_status(group_relation_id,'failure')
					resp = Resource.use('zeus').post({
						'resource': 'mall.group_update_order',
						'data': {
							'group_id': group_relation_id,
							'status': 'failure',
							'is_test': 1 if request.GET.get('is_test', False) else 0
						}
					})
					if resp and resp['code'] == 200:
						#发送拼团失败模板消息
						try:
							group_details = app_models.GroupDetail.objects(relation_belong_to=str(group_relation_id))
							owner_id = data_data.owner_id
							product_name = data_data.product_name
							miss = int(group_relation.group_type)-group_details.count()
							activity_info = {
								"owner_id": str(owner_id),
								"record_id": str(request.POST['id']),
								"group_id": str(group_relation_id),
								"fid": str(group_relation.member_id),
								"price": '%.2f' % group_relation.group_price,
								"product_name": product_name,
								"status" : 'fail',
								"miss": str(miss)
							}
							member_info_list = [{"member_id": group_detail.grouped_member_id, "order_id": group_detail.order_id} for group_detail in group_details]
							send_group_template_message(activity_info, member_info_list)
						except Exception, e:
							print(u'发送拼团失败模板消息失败')
							print 'template----------------------------------'
							print e
							print 'template----------------------------------'

		if group_name:
			params['name__icontains'] = group_name
		if product_name:
			params['product_name__icontains'] = product_name
		if status != -1:
			params['status'] = status
		if start_time:
			params['start_time__gte'] = start_time
		if end_time:
			params['end_time__lte'] = end_time
		params['is_use'] = app_models.IS_USE_YES
		datas = app_models.Group.objects(**params).order_by('-created_at')

		#goup 一个大团活动
		#relation 一个用户开启的团，belong_to 一个group
		#details描述一个团圆的信息，有很多个 belong_to 一个 relation
		group_ids = [unicode(p.id) for p in datas]


		id2relation = {}
		all_relations = app_models.GroupRelations.objects(belong_to__in=group_ids)
		if all_relations:
			for relation in all_relations:
				group_id = relation.belong_to
				if group_id in id2relation:
					id2relation[group_id].append(relation)
				else:
					id2relation[group_id] = [relation]

		r_id2details = {}
		relation_ids = [unicode(r.id) for r in all_relations]
		all_details =  app_models.GroupDetail.objects(relation_belong_to__in=relation_ids)
		if all_details:
			for detail in all_details:
				r_id = unicode(detail.relation_belong_to)
				if r_id in r_id2details:
					r_id2details[r_id].append(detail)
				else:
					r_id2details[r_id]=[detail]
		##### 开团支付个数 start ################
		g_id2details = {}
		for g_id in group_ids:
			detail_list = []
			if g_id in id2relation:
				relations = id2relation[g_id]
				r_ids = [str(r.id) for r in relations]
				for r_id in r_ids:
					if r_id in r_id2details:
						details = r_id2details[r_id]
						detail_list = detail_list+details
			if g_id in g_id2details:
				g_id2details[g_id] = g_id2details[g_id]+detail_list
			else:
				g_id2details[g_id] = []+detail_list

		g_id2pay = {}
		for g_id in group_ids:
			pay_num = 0
			if g_id in g_id2details:
				details = g_id2details[g_id]
				for detail in details:
					if detail.is_already_paid and (detail.owner_id==detail.grouped_member_id):
						pay_num += 1
			if g_id in g_id2pay:
				g_id2pay[g_id] = pay_num
			else:
				g_id2pay[g_id] = pay_num
		###### 开团支付个数 end #################

		for data in datas:
			g_id = unicode(data.id)
			open_group_num = 0
			group_customer_num = 0
			if g_id in id2relation:
				relation_list = id2relation[g_id]
				if g_id in g_id2pay:
					open_group_num = g_id2pay[g_id]
				for relation in relation_list:
					r_id = unicode(relation.id)
					if relation.status_text == '团购成功':
						group_customer_num += int(relation.group_type)

				data.static_info = {'open_group_num':open_group_num,
										'group_customer_num':group_customer_num,
										}
			else:
				data.static_info = {'open_group_num':open_group_num,
										'group_customer_num':group_customer_num,
										}

		items = []
		for data in datas:
			items.append({
				'id': str(data.id),
				'name': data.name,
				'product_id':data.product_id,
				'product_img':data.product_img,
				'product_name':data.product_name,
				'start_time': data.start_time,
				'end_time': data.end_time,
				'group_item_count':data.static_info['open_group_num'],
				'group_customer_count':data.static_info['group_customer_num'],
				'group_visitor_count':len(data.visited_member),
				'related_page_id': data.related_page_id,
				'status': data.status_text,
				'handle_status':data.handle_status,
				'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S")
			})

		#排序
		status_0 = []
		status_1 = []
		status_2 = []
		for item in items:
			if item['status'] == u'未开启':
				status_0.append(item)
			elif item['status'] == u'进行中':
				status_1.append(item)
			elif item['status'] == u'已结束':
				status_2.append(item)
		items = status_1+status_0+status_2

		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, items = paginator.paginate(items, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		return pageinfo, items

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		pageinfo, datas = Groups.get_datas(request)
		#goup 一个大团活动
		#relation 一个用户开启的团，belong_to 一个group
		#details描述一个团圆的信息，有很多个 belong_to 一个 relation



		items = []
		for data in datas:
			items.append({
				'id': data['id'],
				'name': data['name'],
				'product_id':data['product_id'],
				'product_img':data['product_img'],
				'product_name':data['product_name'],
				# 'start_time': data.start_time.strftime('%Y-%m-%d %H:%M'),
				'start_time_date': data['start_time'].strftime('%Y/%m/%d'),
				'start_time_time': data['start_time'].strftime('%H:%M'),
				# 'end_time': data.end_time.strftime('%Y-%m-%d %H:%M'),
				'end_time_date': data['end_time'].strftime('%Y/%m/%d'),
				'end_time_time': data['end_time'].strftime('%H:%M'),
				'group_item_count':data['group_item_count'],
				'group_customer_count':data['group_customer_count'],
				'group_visitor_count':data['group_visitor_count'],
				'related_page_id': data['related_page_id'],
				'status': data['status'],
				'handle_status':data['handle_status'],
				'created_at': data['created_at']})

		#排序
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()

