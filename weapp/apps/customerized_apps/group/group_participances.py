# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime,timedelta,date
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from core import resource
from core import paginator
from core.jsonresponse import create_response
from modules.member import models as member_models
import models as app_models
import export
from mall import export as mall_export
from utils.string_util import byte_to_hex
from weapp import settings

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 12

class GroupParticipances(resource.Resource):
	app = 'apps/group'
	resource = 'group_participances'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.GroupRelations.objects(belong_to=request.GET['id']).count()

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': "groups",
			'has_data': has_data,

			'activity_id': request.GET['id']
		});

		return render_to_response('group/templates/editor/group_participances.html', c)

	@staticmethod
	def get_datas(request):
		webapp_id = request.user_profile.webapp_id#user_id
		id = request.GET.get('id',0)#relation id

		#导出
		export_id = request.GET.get('export_id',0)#export relation id
		if id:
			belong_to = id
		else:
			belong_to = export_id


		#Relation表		  需求状态
		# 0未生效，1进行中	 进行中
		# 2成功				成功
		# 3失败				退款中
		#  未知
		# -1 全部			   全部
		filter_status = request.GET.get('status', 'all')
		filter_group_leader_name = request.GET.get('group_leader_name', '')
		filter_start_time = request.GET.get('start_time', '')
		filter_end_time = request.GET.get('end_time', '')


		params = {'belong_to':belong_to}
		datas_datas = app_models.GroupRelations.objects(**params).order_by('-created_at')
		if filter_group_leader_name:
			params['group_leader_name__icontains'] = filter_group_leader_name
		if filter_status == "all":
			pass
		elif filter_status == 'ing':
			params['group_status__in'] = [0,1]
		elif filter_status == 'success':
			params['group_status'] = 2
		elif filter_status == 'fail':
			params['group_status'] = 3

		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		datas = app_models.GroupRelations.objects(**params).order_by('-created_at')#.order_by('group_days')

		### 过滤支付 start
		r_id2pay_memebers = {}
		r_ids = [ str(data.id) for data in datas]
		all_details = app_models.GroupDetail.objects.filter(relation_belong_to__in=r_ids)
		for a_detail in all_details:
			r_id_tmp = str(a_detail.relation_belong_to)
			is_pay = a_detail.is_already_paid
			if is_pay:
				if r_id_tmp in r_id2pay_memebers:
					r_id2pay_memebers[r_id_tmp].append(a_detail.grouped_member_id)
				else:
					r_id2pay_memebers[r_id_tmp] = [a_detail.grouped_member_id]

		### 过滤支付 end
		items = []
		for data in datas:
			pass_tag = True
			success_time = data.success_time
			created_at = data.created_at
			group_days = data.group_days
			rest_days = 0

			if data.status_text == u'团购成功' and data.success_time:
				start_time_date = data.created_at.strftime('%Y/%m/%d')
				start_time_time = data.created_at.strftime('%H:%M')
				end_time_date = data.success_time.strftime('%Y/%m/%d')
				end_time_time = data.success_time.strftime('%H:%M')
				rest_days = (success_time - created_at).days

				start_time = data.created_at.strftime('%Y-%m-%d %H:%M')
				end_time = data.success_time.strftime('%Y-%m-%d %H:%M')

			else:
				start_time_date = data.created_at.strftime('%Y/%m/%d')
				start_time_time = data.created_at.strftime('%H:%M')

				group_end_time = data.created_at+timedelta(days=int(group_days))
				end_time_date = group_end_time.strftime('%Y/%m/%d')
				end_time_time = group_end_time.strftime('%H:%M')

				rest_days = int(group_days)

				start_time = data.created_at.strftime('%Y-%m-%d %H:%M')
				end_time = group_end_time.strftime('%Y-%m-%d %H:%M')

			if filter_start_time and (filter_start_time>start_time):
				pass_tag = False
			if filter_end_time and (filter_end_time<end_time):
				pass_tag = False
			if pass_tag:
				members_count = "0"
				if r_id2pay_memebers:
					members_count = '%d/%s'%(len(r_id2pay_memebers[str(data.id)]),data.group_type)


				items.append({
					'id': str(data.id),
					'group_leader_name':data.group_leader_name,
					'rest_days':rest_days,
					'start_time_date': start_time_date,
					'start_time_time': start_time_time,
					'start_time':start_time,
					'end_time_date': end_time_date,
					'end_time_time': end_time_time,
					'end_time':end_time,
					'status':data.status_text,
					'members_count':members_count,
					'member_id':str(data.member_id)
				})

		#排序
		status_ing = []
		status_fail = []
		status_success = []
		status_others = []
		for item in items:
			if item['status'] == u'团购未生效':
				# status_ing.append(item)
				pass
			elif item['status']==u'团购进行中':
				status_ing.append(item)
			else:
				status_others.append(item)
		status_ing.sort(key=lambda item:item['rest_days'])
		items = status_ing+status_others #+status_fail+status_success

		pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		if export_id:
			return items
		else:
			return pageinfo, items

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""

		pageinfo, datas = GroupParticipances.get_datas(request)

		items = []
		for data in datas:
			items.append({
				'id': data['id'],
				'group_leader_name':data['group_leader_name'],
				'rest_days':data['rest_days'],
				'start_time_date': data['start_time_date'],
				'start_time_time': data['start_time_time'],
				'end_time_date': data['end_time_date'],
				'end_time_time': data['end_time_time'],
				'status':data['status'],
				'members_count':data['members_count'],
				'member_id':data['member_id']
			})

		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()




class GroupParticipancesDialog(resource.Resource):
	app = 'apps/group'
	resource = 'group_participances_dialog'

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		#会员来源
		SOURCE_SELF_SUB = 0  # 直接关注
		SOURCE_MEMBER_QRCODE = 1  # 推广扫码
		SOURCE_BY_URL = 2  # 会员分享
		source2name = {
			'-1':"未知",
			'0':u'直接关注',
			'1':u'推广扫码',
			'2':u'会员分享'
		}
		#会员关注状态
		CANCEL_SUBSCRIBED = 0
		SUBSCRIBED = 1
		NOT_SUBSCRIBED = 2
		member_status2name = {
			"0":u"已取消",
			"1":u"关注",
			"2":u"未关注",
			"-1":u"未知"

		}

		relation_id = request.GET['id']

		relation = app_models.GroupRelations.objects(id=relation_id)[0]
		group_price = relation.group_price

		# group_details = app_models.GroupDetail.objects(relation_belong_to = relation_id)
		group_details = app_models.GroupDetail.objects(relation_belong_to = relation_id,is_already_paid=True)### 过滤支付
		tmp_member_ids = [unicode(group_detail.grouped_member_id) for group_detail in group_details]
		members = member_models.Member.objects.filter(id__in=tmp_member_ids)
		member_id2member = {unicode(member.id): member for member in members}

		id2info = {}
		for member_id in tmp_member_ids:
			member = member_id2member[unicode(member_id)]
			integral = member.integral
			source = source2name[str(member.source)]
			member_status = member_status2name[str(member.status)]
			member_grade = member.grade.name
			member_icon = member.user_icon
			id2info[unicode(member_id)]={'integral':integral,
										 'source':source,
										 'member_status':member_status,
										 'member_grade':member_grade,
										 'member_icon':member_icon}

		items = []
		for group_detail in group_details:
			member_id = unicode(group_detail.grouped_member_id)
			money = 0
			if group_detail.is_already_paid:
				money = group_price
			info = id2info[member_id]

			items.append({
				'id':unicode(member.id),
				'name':group_detail.grouped_member_name,
				'money':"%.2f"%float(money),
				'integral':info['integral'],
				'source':info['source'],
				'created_at':group_detail.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				'member_status':info['member_status'],
				'member_grade':info['member_grade'],
				'member_icon':info['member_icon']
				})

		#进行分页
		count_per_page = int(request.GET.get('count_per_page', 1))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, items = paginator.paginate(items, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()


class GroupParticipances_Export(resource.Resource):
	'''
	批量导出
	'''
	app = 'apps/group'
	resource = 'group_participances_export'

	@login_required
	def api_get(request):
		"""
		分析导出
		"""
		export_id = request.GET.get('export_id',0)
		datas = GroupParticipances.get_datas(request)
		download_excel_file_name = u'团购详情.xls'
		excel_file_name = 'group_details_'+datetime.now().strftime('%H_%M_%S')+'.xls'
		dir_path_suffix = '%d_%s' % (request.user.id, date.today())
		dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		export_file_path = os.path.join(dir_path,excel_file_name)
		#Excel Process Part
		try:
			import xlwt
			datas = GroupParticipances.get_datas(request)
			fields_pure = []
			export_data = []

			#from sample to get fields4excel_file
			fields_pure.append(u'id')
			fields_pure.append(u'团长')
			fields_pure.append(u'团购时间')
			fields_pure.append(u'团购开始时间')
			fields_pure.append(u'团购结束时间')
			fields_pure.append(u'团购状态')
			fields_pure.append(u'团购人数')

			#processing data
			num = 0
			for data in datas:
				export_record = []
				num = num+1
				g_id = data["id"]
				group_leader_name = data["group_leader_name"]
				rest_days = data["rest_days"]
				start_time = data["start_time"]
				end_time = data["end_time"]
				status = data['status']
				members_count = data['members_count']

				export_record.append(g_id)
				export_record.append(group_leader_name)
				export_record.append(rest_days)
				export_record.append(start_time)
				export_record.append(end_time)
				export_record.append(status)
				export_record.append(members_count)
				export_data.append(export_record)
			#workbook/sheet
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet('id%s'%export_id)
			header_style = xlwt.XFStyle()

			##write fields
			row = col = 0
			for h in fields_pure:
				ws.write(row,col,h)
				col += 1

			##write data
			if export_data:
				row = 1
				lens = len(export_data[0])
				for record in export_data:
					row_l = []
					for col in range(lens):
						record_col= record[col]
						if type(record_col)==list:
							row_l.append(len(record_col))
							for n in range(len(record_col)):
								data = record_col[n]
								try:
									ws.write(row+n,col,data)
								except:
									#'编码问题，不予导出'
									print record
									pass
						else:
							try:
								ws.write(row,col,record[col])
							except:
								#'编码问题，不予导出'
								print record
								pass
					if row_l:
						row = row + max(row_l)
					else:
						row += 1
				try:
					wb.save(export_file_path)
				except Exception, e:
					print 'EXPORT EXCEL FILE SAVE ERROR'
					print e
					print '/static/upload/%s/%s'%(dir_path_suffix,excel_file_name)
			else:
				ws.write(1,0,'')
				wb.save(export_file_path)
			response = create_response(200)
			response.data = {'download_path':'/static/upload/%s/%s'%(dir_path_suffix,excel_file_name),'filename':download_excel_file_name,'code':200}
		except Exception, e:
			error_msg = u"导出文件失败, cause:\n{}".format(unicode_full_stack())
			watchdog_error(error_msg)
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()

		return response.get_response()