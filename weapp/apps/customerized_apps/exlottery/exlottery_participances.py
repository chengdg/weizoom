# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, date
import os

from core import resource
from core import paginator
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from modules.member import models as member_models
import models as app_models
from mall import export
from utils.string_util import hex_to_byte, byte_to_hex
from watchdog.utils import watchdog_error

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class ExlotteryParticipances(resource.Resource):
	app = 'apps/exlottery'
	resource = 'exlottery_participances'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.ExlotteryParticipance.objects(belong_to=request.GET['id']).count()

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_APPS_SECOND_NAV,
            'third_nav_name': export.MALL_APPS_EXLOTTERY_NAV,
			'has_data': has_data,
			'activity_id': request.GET['id']
		})

		return render_to_response('exlottery/templates/editor/exlottery_participances.html', c)

	@staticmethod
	def get_datas(request):
		name = request.GET.get('participant_name', '')
		webapp_id = request.user_profile.webapp_id
		prize_type = request.GET.get('prize_type', '-1')
		status = request.GET.get('status', '-1')
		export_id = request.GET.get('export_id','')
		member_ids = []
		if name:
			hexstr = byte_to_hex(name)
			members = member_models.Member.objects.filter(webapp_id=webapp_id,username_hexstr__contains=hexstr)
			temp_ids = [member.id for member in members]
			member_ids = temp_ids  if temp_ids else [-1]

		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')

		if not export_id:
			belong_to = request.GET['id']
		else:
			belong_to = export_id
		params = {'belong_to':belong_to}
		if name:
			params['member_id__in'] = member_ids
		if start_time:
			params['created_at__gte'] = start_time
		if end_time:
			params['created_at__lte'] = end_time
		if prize_type != '-1':
			params['prize_type'] = prize_type
		if status != '-1':
			params['status'] = True if status == '1' else False
		# datas = app_models.lotteryParticipance.objects(**params).order_by('-id')
		datas = app_models.ExlottoryRecord.objects(**params)
		if not export_id:
			#进行分页
			count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
			cur_page = int(request.GET.get('page', '1'))
			pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
			return pageinfo, datas
		else:
			return datas

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		pageinfo, datas = ExlotteryParticipances.get_datas(request)

		tmp_member_ids = []
		for data in datas:
			tmp_member_ids.append(data.member_id)
		members = member_models.Member.objects.filter(id__in=tmp_member_ids)
		member_id2member = {member.id: member for member in members}

		items = []
		for data in datas:
			items.append({
				'id': str(data.id),
				'participant_name': member_id2member[data.member_id].username_truncated if member_id2member.get(data.member_id) else u'未知',
				'participant_icon': member_id2member[data.member_id].user_icon if member_id2member.get(data.member_id) else '/static/img/user-1.jpg',
				'tel': data.tel,
				'prize_title': data.prize_title,
				'prize_name': data.prize_name,
				'status': data.status,
				'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S")
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
		领取奖品
		"""
		app_models.ExlottoryRecord.objects(id=request.POST['id']).update(set__status=True)
		response = create_response(200)
		return response.get_response()

class ExlotteryParticipances_Export(resource.Resource):
	'''
	批量导出
	'''
	app = 'apps/exlottery'
	resource = 'exlottery_participances-export'
	@login_required
	def api_get(request):
		"""
		详情导出
		"""
		export_id = request.GET.get('export_id','')

		# app_name = lotteryParticipances_Export.app.split('/')[1]
		# excel_file_name = ('%s_id%s_%s.xls') % (app_name,export_id,datetime.now().strftime('%Y%m%d%H%m%M%S'))
		download_excel_file_name = u'微信抽奖详情.xls'
		excel_file_name = 'lottery_details_'+datetime.now().strftime('%H_%M_%S')+'.xls'
		dir_path_suffix = '%d_%s' % (request.user.id, date.today())
		dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		export_file_path = os.path.join(dir_path,excel_file_name)
		#Excel Process Part
		try:
			import xlwt
			datas = ExlotteryParticipances.get_datas(request)
			fields_raw = []
			export_data = []

			#from sample to get fields4excel_file
			fields_raw.append(u'编号')
			fields_raw.append(u'用户名')
			fields_raw.append(u'会员ID')
			fields_raw.append(u'手机号')
			fields_raw.append(u'获奖等级')
			fields_raw.append(u'奖品名称')
			fields_raw.append(u'抽奖时间')
			fields_raw.append(u'领取状态')

			member_ids = []
			for record in datas:
				member_ids.append(record['member_id'])
			members = member_models.Member.objects.filter(id__in=member_ids)
			member_id2member = {member.id: member for member in members}

			#processing data
			num = 0
			for record in datas:
				export_record = []
				num = num+1
				cur_member = member_id2member.get(record['member_id'], None)
				if cur_member:
					try:
						name = cur_member.username.decode('utf8')
					except:
						name = cur_member.username_hexstr
				else:
					name = u'未知'
				tel = record['tel']
				prize_title = record['prize_title']
				prize_name = record['prize_name']
				created_at = record['created_at'].strftime("%Y-%m-%d %H:%M:%S")
				if record['status']:
					status = u'已领取'
				else:
					status = u'未领取'

				export_record.append(num)
				export_record.append(name)
				export_record.append(cur_member.id)
				export_record.append(tel)
				export_record.append(prize_title)
				export_record.append(prize_name)
				export_record.append(created_at)
				export_record.append(status)

				export_data.append(export_record)
			#workbook/sheet
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet('id%s'%export_id)
			header_style = xlwt.XFStyle()

			##write fields
			row = col = 0
			for h in fields_raw:
				ws.write(row,col,h)
				col += 1

			##write data
			if export_data:
				row = 0
				lens = len(export_data[0])
				for record in export_data:
					row +=1
					for col in range(lens):
						try:
							ws.write(row,col,record[col])
						except:
							#'编码问题，不予导出'
							print record
							pass
				try:
					wb.save(export_file_path)
				except:
					print 'EXPORT EXCEL FILE SAVE ERROR'
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
