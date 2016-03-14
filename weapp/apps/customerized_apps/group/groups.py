# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as app_models
import export
from datetime import datetime
from mall import export as mall_export

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
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': "groups",
			'has_data': has_data
		});

		return render_to_response('group/templates/editor/groups.html', c)

	@staticmethod
	def get_datas(request):
		product_name = request.GET.get('product_name', '')
		group_name = request.GET.get('group_name', '')
		status = int(request.GET.get('status', -1))
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')

		now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
		params = {'owner_id':request.manager.id}
		datas_datas = app_models.Group.objects(**params)
		for data_data in datas_datas:
			data_start_time = data_data.start_time.strftime('%Y-%m-%d %H:%M')
			data_end_time = data_data.end_time.strftime('%Y-%m-%d %H:%M')
			if data_start_time <= now_time and now_time < data_end_time:
				data_data.update(set__status=app_models.STATUS_RUNNING)
			elif now_time >= data_end_time:
				data_data.update(set__status=app_models.STATUS_STOPED)

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
		datas = app_models.Group.objects(**params).order_by('-created_at')

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
		pageinfo, datas = Groups.get_datas(request)

		#goup 一个大团活动
		#relation 一个用户开启的团，belong_to 一个group
		#details描述一个团圆的信息，有很多个 belong_to 一个 relation
		group_ids = [unicode(p.id) for p in datas]
		print 111111111111111111
		print group_ids

		id2relation = {}
		all_relations = app_models.GroupRelations.objects(belong_to__in=group_ids)
		if all_relations:
			for relation in all_relations:
				group_id = relation.belong_to
				if group_id in id2relation:
					id2relation[group_id].append(relation)
				else:
					id2relation[group_id] = [relation]

		print 22222222222222222222
		print id2relation

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

		print 333333333333333333
		print r_id2details

		g_id2static_info = {}
		if id2relation:
			for g_id in id2relation:
				group_relation_list = id2relation[g_id]
				open_group_num = len(group_relation_list)

				group_customer_num = 0
				for one_relation in group_relation_list:
					r_id = unicode(one_relation.id)
					print '>>>>>>>>'
					print r_id
					print r_id2details
					detail_list = r_id2details[r_id]
					for one_detail in detail_list:
						if one_detail.is_already_paid:
							group_customer_num += 1

				if g_id in g_id2static_info:
					g_id2static_info[g_id]={'open_group_num':open_group_num,
											'group_customer_num':group_customer_num,
											}
				else:
					g_id2static_info[g_id]={'open_group_num':open_group_num,
											'group_customer_num':group_customer_num,
											}

		print 44444444444444444
		print g_id2static_info

		if g_id2static_info:
			for data in datas:
				g_id = str(data.id)
				data.static_info = g_id2static_info[str(g_id)]


		items = []
		for data in datas:
			items.append({
				'id': str(data.id),
				'name': data.name,
				'product_img':data.product_img,
				'product_name':data.product_name,
				# 'start_time': data.start_time.strftime('%Y-%m-%d %H:%M'),
				'start_time_date': data.start_time.strftime('%Y-%m-%d'),
				'start_time_time': data.start_time.strftime('%H:%M'),
				# 'end_time': data.end_time.strftime('%Y-%m-%d %H:%M'),
				'end_time_date': data.end_time.strftime('%Y-%m-%d'),
				'end_time_time': data.end_time.strftime('%H:%M'),
				# 'group_item_count':data.static_info.open_group_num if hasattr(data, 'static_info') else 0,
				# 'group_customer_count':data.static_info.group_customer_num if hasattr(data, 'static_info') else 0,
				'group_item_count': 0,
				'group_customer_count': 0,
				'group_visitor_count':len(data.visited_member),
				'related_page_id': data.related_page_id,
				'status': data.status_text,
				'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S")
			})

		#排序
		status_0 = []
		status_1 = []
		status_2 = []
		for item in items:
			print item
			if item['status'] == u'未开启':
				status_0.append(item)
			elif item['status'] == u'进行中':
				status_1.append(item)
			elif item['status'] == u'已结束':
				status_2.append(item)
		items = status_1+status_0+status_2

		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()

