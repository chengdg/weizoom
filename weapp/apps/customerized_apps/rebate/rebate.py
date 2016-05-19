# -*- coding: utf-8 -*-

import json
import random
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.conf import settings

from core import resource
from core import paginator
from core import emotion
from core.jsonresponse import create_response
from utils.cache_util import delete_cache
from weixin2.models import News
import models as app_models
from apps.models import AppsWeizoomCard
import export
from apps import request_util
from mall import export as mall_export
from modules.member import integral as integral_api
import termite.pagestore as pagestore_manager
from core.wxapi import get_weixin_api
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from core.wxapi.api_create_qrcode_ticket import QrcodeTicket
from market_tools.tools.weizoom_card import models as card_models
from mall.promotion.string_util import byte_to_hex, hex_to_byte
from mall.promotion import models as promotion_models
from excel_response import ExcelResponse
import os
import xlrd

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class Rebate(resource.Resource):
	app = 'apps/rebate'
	resource = 'rebate'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		rebate = None
		if 'id' in request.GET:
			try:
				rebate = app_models.Rebate.objects.get(id=request.GET['id'])
			except:
				c = RequestContext(request, {
					'first_nav_name': FIRST_NAV,
					'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
					'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
					'third_nav_name': mall_export.MALL_APPS_REBATE_NAV,
					'is_deleted_data': True,
				})
				return render_to_response('rebate/templates/editor/create_rebate_rule.html', c)
			answer_content = {}
			if rebate.reply_type == 2:
				answer_content['type'] = 'news'
				answer_content['newses'] = []
				answer_content['content'] = rebate.reply_material_id
				newses = News.get_news_by_material_id(rebate.reply_material_id)
				for news in newses:
					news_dict = {}
					news_dict['id'] = news.id
					news_dict['title'] = news.title
					answer_content['newses'].append(news_dict)
			else:
				answer_content['type'] = 'text'
				answer_content['content'] = emotion.change_emotion_to_img(rebate.reply_detail)
			jsons = [{
				"name": "qrcode_answer",
				"content": answer_content
			}]
			card_stock = AppsWeizoomCard.objects(belong_to=request.GET['id'],status=0).count()
			c = RequestContext(request, {
				'first_nav_name': FIRST_NAV,
				'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
				'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
				'third_nav_name': mall_export.MALL_APPS_REBATE_NAV,
				'rebate_rule': rebate,
				'card_stock': card_stock,
				'jsons': jsons
			})
			return render_to_response('rebate/templates/editor/create_rebate_rule.html', c)
		else:
			c = RequestContext(request, {
				'first_nav_name': FIRST_NAV,
				'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
				'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
				'third_nav_name': mall_export.MALL_APPS_REBATE_NAV,
				'rebate_rule': rebate
			})
			return render_to_response('rebate/templates/editor/create_rebate_rule.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应PUT
		"""
		data = request_util.get_fields_to_be_save(request)
		data['permission'] = True if data['permission']=='1' else False
		data['is_limit_first_buy'] = True if data['is_limit_first_buy']=='1' else False
		data['is_limit_cash'] = True if data['is_limit_cash']=='1' else False
		weizoom_card_ids = data['weizoom_card_ids'].split(',')
		weizoom_card_passwords = data['weizoom_card_passwords'].split(',')
		rebate = app_models.Rebate(**data)
		ticket_id = app_models.Rebate.objects.all().count() + 10001 #ID从1W开始计算，为了防止跟带参数二维码重复
		rebate.ticket_id = ticket_id
		rebate.save()
		data = json.loads(rebate.to_json())
		data['id'] = data['_id']['$oid']
		index = 0
		for weizoom_card_id in weizoom_card_ids:
			weizoom_card_info = AppsWeizoomCard(
				owner_id = request.manager.id,
				belong_to = data['id'],
				weizoom_card_id = weizoom_card_id,
				weizoom_card_password = weizoom_card_passwords[index]
			)
			weizoom_card_info.save()
			index += 1

		if settings.MODE != 'develop':
			mp_user = get_binding_weixin_mpuser(request.manager)
			mpuser_access_token = get_mpuser_accesstoken(mp_user)
			weixin_api = get_weixin_api(mpuser_access_token)
			try:
				qrcode_ticket = weixin_api.create_qrcode_ticket(ticket_id, QrcodeTicket.PERMANENT)
				ticket = qrcode_ticket.ticket
			except Exception, e:
				print 'get qrcode_ticket fail:', e
				ticket = ''
		else:
			ticket = ''
		rebate.ticket = ticket
		rebate.save()
		response = create_response(200)
		response.data = data
		return response.get_response()
	
	@login_required
	def api_post(request):
		"""
		响应POST
		"""
		data = request_util.get_fields_to_be_save(request)
		data['permission'] = True if data['permission']=='1' else False
		data['is_limit_first_buy'] = True if data['is_limit_first_buy']=='1' else False
		data['is_limit_cash'] = True if data['is_limit_cash']=='1' else False

		update_data = {}
		update_fields = set(['name', 'start_time', 'end_time', 'permission', 'is_limit_first_buy', 'is_limit_cash', 'rebate_order_price', 'rebate_money', 'weizoom_card_id_from', 'weizoom_card_id_to', 'reply_type', 'reply_detail', 'reply_material_id'])
		for key, value in data.items():
			if key in update_fields:
				update_data['set__'+key] = value

		app_models.Rebate.objects(id=request.POST['id']).update(**update_data)

		weizoom_card_ids = data['weizoom_card_ids'].split(',')
		weizoom_card_passwords = data['weizoom_card_passwords'].split(',')

		cur_weizoom_cards = AppsWeizoomCard.objects(belong_to=request.POST['id'])
		cur_weizoom_card_ids = [cur_weizoom_card.weizoom_card_id for cur_weizoom_card in cur_weizoom_cards]
		need_add_weizoom_card_ids =  [ i for i in weizoom_card_ids if i not in cur_weizoom_card_ids ]

		if need_add_weizoom_card_ids != []:
			weizoom_card_id2password = {}
			index = 0
			for weizoom_card_id in weizoom_card_ids:
				if not weizoom_card_id2password.has_key(weizoom_card_id):
					weizoom_card_id2password[weizoom_card_id] = weizoom_card_passwords[index]
				else:
					weizoom_card_id2password[weizoom_card_id].append(weizoom_card_passwords[index])
				index += 1
			print(weizoom_card_id2password)
			for need_add_weizoom_card_id in need_add_weizoom_card_ids:
				weizoom_card_info = AppsWeizoomCard(
					belong_to = data['id'],
					weizoom_card_id = need_add_weizoom_card_id,
					weizoom_card_password = weizoom_card_id2password[need_add_weizoom_card_id]
				)
				weizoom_card_info.save()

		#更新后清除缓存
		# cache_key = 'apps_rebate_%s_html' % request.POST['id']
		# delete_cache(cache_key)
		response = create_response(200)
		return response.get_response()
	
	@login_required
	def api_delete(request):
		"""
		响应DELETE
		"""
		app_models.Rebate.objects(id=request.POST['id']).update(is_deleted=True)
		
		response = create_response(200)
		return response.get_response()

class RebateCardDetails(resource.Resource):
	app = 'apps/rebate'
	resource = 'card_details'

	@login_required
	def get(request):
		"""
		卡兑换详情页
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': mall_export.MALL_APPS_REBATE_NAV,
			'record_id': request.GET['id']
		})
		return render_to_response('rebate/templates/editor/card_rebate_details.html', c)

	@login_required
	def api_get(request):
		"""
		查看微众卡使用详情
		"""
		cur_page = int(request.GET.get('page',1))
		count_per_page = int(request.GET.get('count_per_page',10))

		rebate_cards = RebateCardDetails.get_rebate_cards(request)
		pageinfo, rebate_cards = paginator.paginate(rebate_cards, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		rebate_cards_list = []
		for card in rebate_cards:
			try:
				rebate_cards_list.append({
					'card_number': card.card_number,
					'card_password': card.card_password,
					'member_name': hex_to_byte(card.member_name)
				})
			except Exception,e:
				print(e)
				response = create_response(500)
				return response.get_response()

		response = create_response(200)
		response.data.items = rebate_cards_list
		response.data.pageinfo = paginator.to_dict(pageinfo)
		return response.get_response()

	@staticmethod
	def get_rebate_cards(request):
		card_number = request.GET.get('cardNumber',None)
		card_user = request.GET.get('cardUser',None)
		#查询
		rebate_rule_id = request.GET.get('record_id','')
		rebate_cards = promotion_models.MemberHasWeizoomCard.objects.filter(source=promotion_models.WEIZOOM_CARD_SOURCE_REBATE,relation_id=rebate_rule_id).order_by('-created_at')
		if card_number:
			rebate_cards = rebate_cards.filter(card_number__in=card_number)
		if card_user:
			rebate_cards = rebate_cards.filter(member_name__contains=byte_to_hex(card_user))

		return rebate_cards

class CardRebateDetailExport(resource.Resource):
	app = 'apps/rebate'
	resource = 'export_card_rebate_details'

	@login_required
	def api_get(request):
		"""
		微众卡兑换详情导出
		"""
		cards = card_models.WeizoomCard.objects.all()
		exchanged_cards = RebateCardDetails.get_rebate_cards(request,cards)
		card_rules = card_models.WeizoomCardRule.objects.all()

		members_info = [
			[u'卡号', u'面值',u'卡内余额',u'使用金额',u'使用者']
		]

		for card in exchanged_cards:
			card_id = card.card_id
			try:
				cur_card = cards.get(id = card_id)
				weizoom_card_id = cur_card.weizoom_card_id
				weizoom_card_rule_id = cur_card.weizoom_card_rule_id
				cur_card_rule = card_rules.get(id = weizoom_card_rule_id)
				money = cur_card_rule.money
				remainder = cur_card.money
				user = hex_to_byte(card.owner_name)
				used_money = money - remainder
				info_list = [
					weizoom_card_id,
					'%.2f' % money,
					'%.2f' % remainder,
					'%.2f' % used_money,
					user
				]
				members_info.append(info_list)
			except:
				pass

		filename = u'微众卡返利详情'
		return ExcelResponse(members_info, output_name=filename.encode('utf8'), force_csv=False)

class RebateUpload(resource.Resource):
	app = 'apps/rebate'
	resource = 'upload_file'

	def api_post(request):
		"""
		上传文件
		"""
		upload_file = request.FILES.get('Filedata', None)
		owner_id = request.POST.get('owner_id', None)
		has_file = request.POST.get('has_file', None)
		belong_to = request.POST.get('belong_to', '')

		weizoom_card_ids = []
		weizoom_card_passwords = []
		response = create_response(500)
		if upload_file:
			try:
				now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
				upload_file.name = now + upload_file.name
				file_path = RebateUpload.__save_file(upload_file, owner_id)
			except Exception, e:
				print(e)
				response.errMsg = u'保存文件出错'
				return response.get_response()
			try:
				file_name_dir = '%s/owner_id%s/%s' % (settings.UPLOAD_DIR,owner_id,upload_file.name)
				data = xlrd.open_workbook(file_name_dir)
				table = data.sheet_by_index(0)
				nrows = table.nrows   #行数
				# ncols = table.ncols   #列数
				# data = table.cell(0, 1).value
				for i in range(1,nrows):
					table_content=table.cell(i,0).value
					weizoom_card_ids.append(str(table_content))
				for i in range(1,nrows):
					table_content=table.cell(i,1).value
					weizoom_card_passwords.append(str(table_content))
			except Exception, e:
				print(e)
				response.errMsg = u'上传文件错误'
				return response.get_response()
			if not has_file:
				card_stock = len(weizoom_card_ids)
			else:
				cur_weizoom_cards = AppsWeizoomCard.objects(belong_to=belong_to, status=0)
				cur_weizoom_card_ids = [cur_weizoom_card.weizoom_card_id for cur_weizoom_card in cur_weizoom_cards]
				need_add_weizoom_card_ids =  [ i for i in weizoom_card_ids if i not in cur_weizoom_card_ids ]
				card_stock = len(cur_weizoom_cards) + len(need_add_weizoom_card_ids)
			response = create_response(200)
			response.data = {
				'file_path': file_path,
				'weizoom_card_ids': weizoom_card_ids,
				'weizoom_card_passwords': weizoom_card_passwords,
				'card_stock': card_stock
			}
		else:
			response.errMsg = u'文件错误'
		return response.get_response()

	@staticmethod
	def __save_file(file, owner_id):
		"""
		@param file: 文件
		@param owner_id: webapp_owner_id
		@return: 文件保存路径
		"""
		content = []
		curr_dir = os.path.dirname(os.path.abspath(__file__))
		if file:
			for chunk in file.chunks():
				content.append(chunk)

		dir_path = os.path.join(curr_dir, '../../../','static', 'upload', 'owner_id'+owner_id)
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		file_path = os.path.join(dir_path, file.name)

		dst_file = open(file_path, 'wb')
		print >> dst_file, ''.join(content)
		dst_file.close()
		file_path = os.path.join('\standard_static', 'upload', 'owner_id'+owner_id, file.name).replace('\\','/')
		return file_path