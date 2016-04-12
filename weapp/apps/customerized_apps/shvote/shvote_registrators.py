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
from apps import request_util
from weapp import settings
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class ShvoteRegistrators(resource.Resource):
	app = 'apps/shvote'
	resource = 'shvote_registrators'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.ShvoteParticipance.objects(belong_to=request.GET['id']).count()#count<->是否有数据

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': "shvotes",
			'has_data': has_data,
			'activity_id': request.GET['id']
		});

		return render_to_response('shvote/templates/editor/shvote_registrators.html', c)

	@staticmethod
	def get_datas(request):
		name = request.GET.get('participant_name', '')#搜索
		status = int(request.GET.get('participant_status', -1))
		webapp_id = request.user_profile.webapp_id
		member_ids = []
		# if name:
		# 	hexstr = byte_to_hex(name)
		# 	members = member_models.Member.objects.filter(webapp_id=webapp_id,username_hexstr__contains=hexstr)#模糊搜索
		# 	member_ids = [member.id for member in members]
		# start_time = request.GET.get('start_time', '')
		# end_time = request.GET.get('end_time', '')

		params = {'belong_to':request.GET['id']}
		if name:
			params['name__icontains'] = name
		if status != -1:
			params['status'] = status
		# if start_time:
		# 	params['created_at__gte'] = start_time
		# if end_time:
		# 	params['created_at__lte'] = end_time
		datas = app_models.ShvoteParticipance.objects(**params).order_by('-id').order_by('status')#筛选后参与者集合

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
		pageinfo, datas = ShvoteRegistrators.get_datas(request)

		tmp_member_ids = []
		# data = one_ShvoteParticipance
		for data in datas:
			tmp_member_ids.append(data.member_id)
		members = member_models.Member.objects.filter(id__in=tmp_member_ids)
		member_id2member = {member.id: member for member in members} #会员

		items = []
		for data in datas:
			items.append({
				'id': str(data.id),
				'icon':data.icon,
				'name':data.name,
				# 'participant_name': member_id2member[data.member_id].username_size_ten if member_id2member.get(data.member_id) else u'未知',
				# 'participant_icon': member_id2member[data.member_id].user_icon if member_id2member.get(data.member_id) else '/static/img/user-1.jpg',
				'count':data.count,
				'serial_number':data.serial_number,
				'status':data.status,
				'created_at': data.created_at.strftime("%Y/%m/%d %H:%M")
				# 'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S")
			})
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		响应POST
		"""
		data = request_util.get_fields_to_be_save(request)
		update_data = {}
		update_data['set__status'] = app_models.MEMBER_STATUS['PASSED']
		if request.POST.get('ids'):
			ids = json.loads(request.POST['ids'])
			app_models.ShvoteParticipance.objects(id__in=ids).update(**update_data)
		elif request.POST.get('id'):
			id = request.POST['id']
			app_models.ShvoteParticipance.objects(id = id).update(**update_data)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		响应DELETE
		"""
		if request.POST.get('ids'):
			ids = json.loads(request.POST['ids'])
			app_models.ShvoteParticipance.objects(id__in=ids).delete()
		elif request.POST.get('id'):
			id = request.POST.get('id')
			app_models.ShvoteParticipance.objects(id=request.POST['id']).delete()

		response = create_response(200)
		return response.get_response()


class ShvoteRegistrators_Export(resource.Resource):
	'''
	批量导出
	'''
	app = 'apps/shvote'
	resource = 'shvote_registrators_export'

	@login_required
	def api_get(request):
		"""
		分析导出
		"""
		export_id = request.GET.get('id',0)
		pageinfo, datas = ShvoteRegistrators.get_datas(request)
		download_excel_file_name = u'上海投票报名详情.xls'
		excel_file_name = 'shvote_registrators_'+datetime.now().strftime('%H_%M_%S')+'.xls'
		dir_path_suffix = '%d_%s' % (request.user.id, date.today())
		dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		export_file_path = os.path.join(dir_path,excel_file_name)
		#Excel Process Part
		try:
			import xlwt
			pageinfo, datas = ShvoteRegistrators.get_datas(request)
			fields_pure = []
			export_data = []

			#from sample to get fields4excel_file
			fields_pure.append(u'id')
			fields_pure.append(u'选手')
			fields_pure.append(u'票数')
			fields_pure.append(u'编号')
			fields_pure.append(u'状态')
			fields_pure.append(u'报名时间')

			#processing data
			num = 0
			for data in datas:
				export_record = []
				num = num+1
				g_id = data["member_id"]
				player_name = data["name"]
				count = data["count"]
				serial_number = data["serial_number"]
				status = data['status']
				status_text = ""
				if status == 0:
					status_text = u"待审核"
				else:
					status_text = u"审核通过"
				created_at = data['created_at'].strftime("%Y/%m/%d %H:%M")

				export_record.append(g_id)
				export_record.append(player_name)
				export_record.append(count)
				export_record.append(serial_number)
				export_record.append(status_text)
				export_record.append(created_at)
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