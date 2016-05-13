# -*- coding: utf-8 -*-
import json

from datetime import date, datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
# from apps.customerized_apps.red_packet.m_red_packet import reset_member_helper_info,reset_re_subscribed_member_helper_info
from core import resource
from core import paginator
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from modules.member import models as member_models
import models as app_models
import export
from mall import export as mall_export
from modules.member.models import Member
from utils.string_util import byte_to_hex
import os

from watchdog.utils import watchdog_error
from weapp import settings
from mall import models as mall_models

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class RebateParticipances(resource.Resource):
	app = 'apps/rebate'
	resource = 'rebate_participances'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.RebateParticipance.objects(belong_to=request.GET['id']).count()

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': mall_export.MALL_APPS_REBATE_NAV,
			'has_data': has_data,
			'record_id': request.GET['id']
		})

		return render_to_response('rebate/templates/editor/rebate_participances.html', c)

	@staticmethod
	def get_datas(request,export_id=0):
		sort_attr = request.GET.get('sort_attr', '-created_at')
		webapp_id = request.user_profile.webapp_id
		record_id = request.GET.get('record_id', 0)
		is_show = request.GET.get('is_show', '0')

		datas = app_models.RebateParticipance.objects(belong_to=record_id).order_by('-created_at')

		member_ids = [d.member_id for d in datas]

		if is_show == '1':
			all_members = member_models.Member.objects.filter(id__in=member_ids)
			member_id2created_at = {m.id: m.created_at for m in all_members}
			member_ids = []
			for data in datas:
				participent_time = data.created_at
				member_id = data.member_id
				subscribe_time = member_id2created_at.get(member_id, None)
				if subscribe_time:
					if subscribe_time >= participent_time:
						member_ids.append(data.member_id)

		#查询
		member_status = int(request.GET.get('status', '-1'))
		start_date = request.GET.get('start_date', '')
		end_date = request.GET.get('end_date', '')
		params = {'status__in':[0,1]}
		if member_status != -1:
			params['status__in'] = [member_status]
		if start_date:
			params['created_at__gte'] = start_date
		if end_date:
			params['created_at__lte'] = end_date

		params['id__in'] = member_ids

		members = member_models.Member.objects.filter(**params).order_by(sort_attr)

		# 进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		if not export_id:
			pageinfo, members = paginator.paginate(members, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		items = []
		for member in members:
			try:
				name = member.username_for_html
			except:
				name = u'未知'
			if member.status != member_models.NOT_SUBSCRIBED:
				items.append({
					'id': member.id,
					'username': name,
					'participant_icon': member.user_icon,
					'follow_time': member.created_at.strftime("%Y-%m-%d %H:%M:%S"),
					'integral': member.integral,
					'pay_times': member.pay_times,
					'pay_money': '%.2f' % member.pay_money,
					'is_subscribed': member.status
				})

		if not export_id:
			return pageinfo, items
		else:
			return items

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		pageinfo, items = RebateParticipances.get_datas(request)
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': request.GET.get('sort_attr', '-created_at'),
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()

class RebateParticipances_Export(resource.Resource):
	'''
	批量导出
	'''
	app = 'apps/rebate'
	resource = 'rebate_participances_export'

	@login_required
	def api_get(request):
		"""
		分析导出
		"""
		export_id = request.GET.get('export_id',0)
		download_excel_file_name = u'返利活动关注会员.xls'
		excel_file_name = 'rebate_participances_'+datetime.now().strftime('%H_%M_%S')+'.xls'
		dir_path_suffix = '%d_%s' % (request.user.id, date.today())
		dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		export_file_path = os.path.join(dir_path,excel_file_name)
		#Excel Process Part
		try:
			import xlwt
			datas =RebateParticipances.get_datas(request,export_id)
			fields_pure = []
			export_data = []

			#from sample to get fields4excel_file
			# fields_pure.append(u'会员id')
			fields_pure.append(u'用户名')
			fields_pure.append(u'购买次数')
			fields_pure.append(u'积分')
			fields_pure.append(u'消费总额')
			fields_pure.append(u'参与时间')

			#processing data
			num = 0
			for data in datas:
				export_record = []
				# member_id = data["member_id"]
				participant_name = data["username"]
				pay_times = data["pay_times"]
				integral = data["integral"]
				pay_money = data["pay_money"]
				follow_time = data["follow_time"]

				# export_record.append(member_id)
				export_record.append(participant_name)
				export_record.append(pay_times)
				export_record.append(integral)
				export_record.append(pay_money)
				export_record.append(follow_time)
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
