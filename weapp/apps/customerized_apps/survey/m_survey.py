# -*- coding: utf-8 -*-

from datetime import datetime
from django.template import RequestContext
from django.shortcuts import render_to_response
from core import resource
import models as app_models
from modules.member.models import Member
from termite2 import pagecreater
from termite import pagestore as pagestore_manager
from utils.string_util import byte_to_hex
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
	app = 'apps/survey'
	resource = 'm_survey'
	
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			id = request.GET['id']
			isPC = request.GET.get('isPC',0)
			print isPC,"isPC"
			isMember = False
			qrcode_url = None
			permission = ''
			share_page_desc = ''
			thumbnails_url = '/static_v2/img/thumbnails_survey.png'
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
					record = app_models.survey.objects.get(id=id)
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

				project_id = 'new_app:survey:%s' % record.related_page_id

				if request.member:
					participance_data_count = app_models.surveyParticipance.objects(belong_to=id, member_id=request.member.id).count()

				pagestore = pagestore_manager.get_pagestore('mongo')
				page = pagestore.get_page(record.related_page_id, 1)
				permission = page['component']['components'][0]['model']['permission']
			is_already_participanted = (participance_data_count > 0)
			if  is_already_participanted:
				try:
					survey_detail,result_list = Msurvey.get_result(request)
				except:
					c = RequestContext(request,{
						'is_deleted_data': True
					})
					return render_to_response('survey/templates/webapp/result_survey.html', c)
				c = RequestContext(request, {
					'survey_detail': survey_detail,
					'record_id': id,
					'page_title': '用户调研',
					'app_name': "survey",
					'resource': "survey",
					'q_survey': result_list,
					'hide_non_member_cover': True, #非会员也可使用该页面
					'isMember': isMember,
					'qrcode_url': qrcode_url
				})
				return render_to_response('survey/templates/webapp/result_survey.html', c)
			else:
				request.GET._mutable = True
				request.GET.update({"project_id": project_id})
				request.GET._mutable = False
				html = pagecreater.create_page(request, return_html_snippet=True)
				c = RequestContext(request, {
					'record_id': id,
					'activity_status': activity_status,
					'is_already_participanted': (participance_data_count > 0),
					'page_title': '用户调研',
					'page_html_content': html,
					'app_name': "survey",
					'resource': "survey",
					'hide_non_member_cover': True, #非会员也可使用该页面
					'isPC': False if request.member else True,
					'isMember': isMember,
					'qrcode_url': qrcode_url,
					'permission': permission,
					'share_page_desc': share_page_desc,
					'share_img_url': thumbnails_url
				})

				return render_to_response('workbench/wepage_webapp_page.html', c)
		else:
			record = None
			c = RequestContext(request, {
				'record': record
			})
			return render_to_response('survey/templates/webapp/m_survey.html', c)


	@staticmethod
	def get_result(request):
		survey_detail ={}
		survey_survey = app_models.survey.objects.get(id=request.GET['id'])
		survey_detail['name'] = survey_survey['name']
		survey_detail['start_time'] = survey_survey['start_time'].strftime('%Y-%m-%d %H:%M')
		survey_detail['end_time'] = survey_survey['end_time'].strftime('%Y-%m-%d %H:%M')
		related_page_id = survey_survey.related_page_id

		pagestore = pagestore_manager.get_pagestore('mongo')
		page = pagestore.get_page(related_page_id, 1)
		page_info = page['component']['components'][0]['model']
		survey_detail['subtitle'] = page_info['subtitle']
		survey_detail['description'] = page_info['description']
		prize_type = page_info['prize']['type']
		survey_detail['prize_type'] = prize_type
		if prize_type == 'coupon':
			prize_data = page_info['prize']['data']['name']
		else:
			prize_data = page_info['prize']['data']
		survey_detail['prize_data'] = prize_data

		result_list = Msurvey.get_surveyparticipance_datas(request)

		return survey_detail,result_list

	@staticmethod
	def get_surveyparticipance_datas(request):
		id = request.GET.get('id','')
		export_id = request.GET.get('export_id','')
		#判断是否是手机端
		if hasattr(request,'member'):
			member_id = request.member.id
			survey_participances = app_models.surveyParticipance.objects.filter(belong_to=id,member_id=member_id).order_by('-created_at')
		elif export_id:
			name = request.GET.get('participant_name', '')
			webapp_id = request.user_profile.webapp_id
			member_ids = []
			if name:
				hexstr = byte_to_hex(name)
				members = Member.objects.filter(webapp_id=webapp_id,username_hexstr__contains=hexstr)
				temp_ids = [member.id for member in members]
				member_ids = temp_ids  if temp_ids else [-1]
			start_time = request.GET.get('start_time', '')
			end_time = request.GET.get('end_time', '')
			params = {'belong_to':export_id}
			if member_ids:
				params['member_id__in'] = member_ids
			if start_time:
				params['created_at__gte'] = start_time
			if end_time:
				params['created_at__lte'] = end_time
			survey_participances = app_models.surveyParticipance.objects(**params).order_by('-id')
		else:
			survey_participances = app_models.surveyParticipance.objects.filter(id=id).order_by('-created_at')
		member_ids = []
		for record in survey_participances:
			member_ids.append(record['member_id'])
		members = Member.objects.filter(id__in=member_ids)
		member_id2member = {member.id: member for member in members}
		termite_data_list = []
		for survey_participance in survey_participances:
			result_list = []
			cur_member = member_id2member.get(survey_participance['member_id'], None)
			if cur_member:
				try:
					name = cur_member.username.decode('utf8')
				except:
					name = cur_member.username_hexstr
				username_for_title = cur_member.username_for_title
			else:
				name = username_for_title = u'未知'
			created_at = survey_participance['created_at'].strftime("%Y-%m-%d %H:%M:%S")
			termite_data = survey_participance['termite_data']
			for title in sorted(termite_data.keys()):
				title_type = termite_data[title]['type']
				result = {}
				title_name = title.split('_')[1]
				if title_type in['appkit.textlist', 'appkit.shortcuts']:
					if title_name in SHORTCUTS_TEXT:
						title_name = SHORTCUTS_TEXT[title_name]
				result['title'] = title_name
				result['type'] = title_type
				values = termite_data[title]['value']

				if title_type == 'appkit.selection':
					select_values = []
					for select_title in sorted(values.keys()):
						select_value = {}
						select_value['name'] = select_title.split('_')[1]
						select_value['type'] = values[select_title]['type']
						select_value['isSelect'] = values[select_title]['isSelect']
						select_values.append(select_value)
					values = select_values
				result['values'] = values

				if title_type == 'appkit.uploadimg':
					result['att_urls'] = termite_data[title]['value']
				result_list.append(result)

			if hasattr(request,'member'):
				termite_data_list = result_list
			else:
				items_data_list = []
				if result_list:
					for item in result_list:
						items_data ={}
						if item['type'] != 'appkit.uploadimg':
							items_data['type'] = item['type']
						items_data['item_name'] = item['title']
						if item['type'] == 'appkit.uploadimg':
							items_data['item_value'] = []
							for value in item['values']:
								items_data['item_value'].append(value)
						else:
							if type(item['values']) == list:
								items_data['item_value'] = []
								for value in item['values']:
									if value['isSelect']:
										items_data['item_value'].append(value['name'])
							else:
								items_data['item_value'] = item['values']
						items_data_list.append(items_data)
					termite_data_list.append({
						'id': str(survey_participance.id),
						'member_id': survey_participance.member_id,
						'name': name,
						'username_for_title': username_for_title,
						'items': items_data_list,
						'created_at': created_at
					})
		return termite_data_list