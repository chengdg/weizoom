# -*- coding: utf-8 -*-
from datetime import datetime

from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from weixin.mp_decorators import mp_required
from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect
from weixin2 import export
from core.exceptionutil import unicode_full_stack
from core import resource
from core import paginator
from core import emotion
from core.jsonresponse import JsonResponse, create_response, decode_json_str
from weixin2.models import MessageRemarkMessage,Message,FanCategory,FanHasCategory,Session,News
from modules.member.models import *
from .util import get_members
from .fans_category import DEFAULT_CATEGORY_NAME
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings,ChannelQrcodeHasMember, ChannelQrcodeBingMember
from market_tools.tools.distribution.models import ChannelDistributionQrcodeSettings, ChannelDistributionQrcodeHasMember,\
		ChannelDistributionDetail
from mall.models import Order
from modules.member import models as member_model
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from weixin2.message.util import get_member_groups
from modules.member.models import MemberGrade, MemberTag
from core.wxapi.api_create_qrcode_ticket import QrcodeTicket
import json
from excel_response import ExcelResponse
from modules.member.module_api import get_member_by_id_list, get_member_by_id
from core.wxapi import get_weixin_api
from mall import export as mall_export
from mall.promotion.models import CouponRule
from django.db.models import F

#COUNT_PER_PAGE = 2
COUNT_PER_PAGE = 50
FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV

#DEFAULT_CATEGORY_NAME=u"未分组"

class Qrcodes(resource.Resource):
	app = 'new_weixin'
	resource = 'qrcodes'

	@login_required
	@mp_required
	def get(request):
		"""
		带参数二维码列表页面
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_CHANNEL_QRCODE_SECOND_NAV,
			'third_nav_name': mall_export.ADVANCE_MANAGE_QRCODE_NAV,
		})
		return render_to_response('weixin/advance_manage/qrcodes.html', c)

	@login_required
	@mp_required
	def api_get(request):
		sort_attr = request.GET.get('sort_attr', '-created_at')
		items = _get_qrcode_items(request)

		#进行分页

		if 'created_at' not in  sort_attr:
			if '-' in sort_attr:
				sorter = sort_attr[1:]
				is_reverse = True
			else:
				sorter = sort_attr
				is_reverse = False

			# items = sorted(items, reverse=is_reverse, key=lambda b : getattr(b, sorter))
			items = sorted(items, reverse=is_reverse, key=lambda x:getattr(x, sorter))
		count_per_page = int(request.GET.get('count_per_page', 15))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, items = paginator.paginate(items, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		new_items = []
		for item in items:
			new_items.append(item.__dict__)

		response = create_response(200)
		response.data = {
			'items': new_items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': sort_attr,
			'data': {}
		}
		return response.get_response()

def _get_qrcode_items(request):
	#处理搜索
	from mall.models import *
	query = request.GET.get('query', '').strip()
	sort_attr = request.GET.get('sort_attr', '-created_at')
	created_at = '-created_at'
	if 'created_at' in  sort_attr:
		created_at = sort_attr

	if query:
		settings = ChannelQrcodeSettings.objects.filter(owner=request.manager, name__contains=query).order_by(created_at)
	else:
		settings = ChannelQrcodeSettings.objects.filter(owner=request.manager).order_by(created_at)

	setting_ids = []
	bing_member_ids = []
	setting_id2bing_member_id = {}
	for setting in settings:
		setting_ids.append(setting.id)
		bing_member_ids.append(setting.bing_member_id)
		setting_id2bing_member_id[setting.id] = setting.bing_member_id

	bing_members = get_member_by_id_list(bing_member_ids)
	id2member = dict([(m.id, m) for m in bing_members])

	relations = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id__in=setting_ids)
	setting_id2count = {}
	member_id2setting_id = {}
	member_id2relation = {}
	member_ids = []
	for r in relations:
		member_ids.append(r.member_id)
		member_id2setting_id[r.member_id] = r.channel_qrcode_id
		member_id2relation[r.member_id] = r
		if r.channel_qrcode_id in setting_id2count:
			setting_id2count[r.channel_qrcode_id] += 1
		else:
			setting_id2count[r.channel_qrcode_id] = 1

	relations = ChannelQrcodeBingMember.objects.filter(channel_qrcode_id__in=setting_ids)
	qrcode_id_and_member_id2relation = {}
	for r in relations:
		qrcode_id_and_member_id2relation[(r.channel_qrcode_id, r.member_id)] = r


	webapp_users = member_model.WebAppUser.objects.filter(member_id__in=member_ids)
	webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
	webapp_user_ids = set(webapp_user_id2member_id.keys())

	orders = Order.by_webapp_user_id(webapp_user_ids).filter(status__in=(ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED))

	member_id2total_final_price = {}
	member_id2cash_money = {}
	member_id2weizoom_card_money = {}
	for order in orders:
		member_id = webapp_user_id2member_id[order.webapp_user_id]
		if member_id2relation[member_id].is_new or member_id2relation[member_id].created_at <= order.created_at:
			if member_id in member_id2total_final_price:
				member_id2total_final_price[member_id] += order.final_price + order.weizoom_card_money
				member_id2cash_money[member_id] += order.final_price
				member_id2weizoom_card_money[member_id] += order.weizoom_card_money
			else:
				member_id2total_final_price[member_id] = order.final_price + order.weizoom_card_money
				member_id2cash_money[member_id] = order.final_price
				member_id2weizoom_card_money[member_id] = order.weizoom_card_money

	setting_id2total_final_price = {}
	setting_id2cash_money = {}
	setting_id2weizoom_card_money = {}
	for member_id in member_id2total_final_price.keys():
		final_price = member_id2total_final_price[member_id]
		cash_money = member_id2cash_money[member_id]
		weizoom_card_money = member_id2weizoom_card_money[member_id]
		setting_id = member_id2setting_id[member_id]
		if setting_id in setting_id2total_final_price:
			setting_id2total_final_price[setting_id] += final_price
			setting_id2cash_money[setting_id] += cash_money
			setting_id2weizoom_card_money[setting_id] += weizoom_card_money
		else:
			setting_id2total_final_price[setting_id] = final_price
			setting_id2cash_money[setting_id] = cash_money
			setting_id2weizoom_card_money[setting_id] = weizoom_card_money



	response = create_response(200)
	#response.data.items = []
	items = []

	mp_user = get_binding_weixin_mpuser(request.manager)
	mpuser_access_token = get_mpuser_accesstoken(mp_user)

	for setting in settings:
		current_setting = JsonResponse()
		prize_info = decode_json_str(setting.award_prize_info)
		if prize_info['name'] == '_score-prize_':
			setting.cur_prize = '[%s]%d' % (prize_info['type'], prize_info['id'])
		elif prize_info['name'] == 'non-prize':
			setting.cur_prize = u'无奖励'
			# setting.cur_prize = prize_info['type']
		else:
			setting.cur_prize = '[%s]%s' % (prize_info['type'], prize_info['name'])

		if setting.id in setting_id2count:
			setting.count = setting_id2count[setting.id]
		else:
			setting.count = 0
		if setting.id in setting_id2total_final_price:
			setting.total_final_price = setting_id2total_final_price[setting.id]
			setting.cash_money = setting_id2cash_money[setting.id]
			setting.weizoom_card_money = setting_id2weizoom_card_money[setting.id]
		else:
			setting.total_final_price = 0
			setting.cash_money = 0
			setting.weizoom_card_money = 0


		#获取绑定会员的名称，添加绑定时间和取消绑定的时间
		bing_member_name = ''
		bing_time = ''
		cancel_time = ''
		if setting_id2bing_member_id.has_key(setting.id) and \
		id2member.has_key(setting_id2bing_member_id[setting.id]):
			bing_member_name = id2member[setting_id2bing_member_id[setting.id]].username_truncated
			if qrcode_id_and_member_id2relation.has_key((setting.id, setting.bing_member_id)):
				r = qrcode_id_and_member_id2relation[(setting.id, setting.bing_member_id)]
				bing_time = r.created_at.strftime("%Y-%m-%d %H:%M:%S")
				if (not setting.is_bing_member) and setting.bing_member_id:
					cancel_time = r.cancel_bing_time.strftime("%Y-%m-%d %H:%M:%S")

		#如果没有ticket信息则获取ticket信息
		if not setting.ticket:
			try:
				if mp_user.is_certified and mp_user.is_service and mpuser_access_token.is_active:
					weixin_api = get_weixin_api(mpuser_access_token)
					qrcode_ticket = weixin_api.create_qrcode_ticket(int(setting.id), QrcodeTicket.PERMANENT)

					try:
						ticket = qrcode_ticket.ticket
					except:
						ticket = ''
					setting.ticket = ticket
					setting.save()
			except:
				pass
		current_setting.id = setting.id
		current_setting.name = setting.name
		current_setting.count = setting.count
		current_setting.total_final_price = round(setting.total_final_price,2)
		current_setting.cash_money = round(setting.cash_money, 2)
		current_setting.weizoom_card_money = round(setting.weizoom_card_money, 2)
		current_setting.cur_prize = setting.cur_prize
		current_setting.ticket = setting.ticket
		current_setting.remark = setting.remark
		current_setting.bing_member_id = setting.bing_member_id
		current_setting.bing_member_name = bing_member_name
		current_setting.bing_time = bing_time
		current_setting.cancel_time = cancel_time
		current_setting.created_at = setting.created_at.strftime('%Y-%m-%d %H:%M:%S')

		items.append(current_setting)
	return items



class QrcodeExport(resource.Resource):
	"""
	导出二维码
	"""
	app = "new_weixin"
	resource = 'qrcode_export'

	@login_required
	@mp_required
	def get(request):
		items = _get_qrcode_items(request)

		qrcodes = [
			[u"二维码名称", u"关注数量", u"扫码后成交总金额", u"现金", u"微众卡", u"扫码奖励", u"创建时间"]
		]

		for item in items:
			qrcodes.append([
				item.name,
				item.count,
				item.total_final_price,
				item.cash_money,
				item.weizoom_card_money,
				item.cur_prize,
				item.created_at
			])

		return ExcelResponse(qrcodes,output_name=u'二维码列表'.encode('utf8'),force_csv=False)

class Qrcode(resource.Resource):
	app = 'new_weixin'
	resource = 'qrcode'

	@login_required
	@mp_required
	def get(request):
		"""
		带参数二维码
		"""
		setting_id = int(request.GET.get('setting_id', '-1'))
		setting_ids = request.GET.get('setting_ids', None)
		answer_content = {}
		webapp_id = request.user_profile.webapp_id
		groups = MemberGrade.get_all_grades_list(webapp_id)
		member_tags = MemberTag.get_member_tags(webapp_id)
		#调整排序，将为分组放在最前面
		tags = []
		for tag in member_tags:
			if tag.name == '未分组':
				tags = [tag] + tags
			else:
				tags.append(tag)
		qrcode = None
		#批量修改
		qrcodes = None
		if setting_ids:
			setting_ids = setting_ids.split(',')
			qrcodes = ChannelQrcodeSettings.objects.filter(id__in=setting_ids, owner=request.manager)
		else:
			from mall.promotion.models import CouponRule
			if setting_id > 0:
				try:
					qrcode = ChannelQrcodeSettings.objects.get(id=setting_id, owner=request.manager)
				except Exception, e:
					print 'get qrcode failed,id:',setting_id

				if qrcode:
					#获取优惠券剩余个数
					award_prize_info = qrcode.award_prize_info
					try:
						info_dict = json.loads(award_prize_info)
						if info_dict['type'] == u'优惠券':
							coupon_rule = CouponRule.objects.get(id = info_dict['id'])
							info_dict['remained_count'] = coupon_rule.remained_count
							if coupon_rule.limit_product:
								info_dict['coupon_type'] = u'单品券'
							else:
								info_dict['coupon_type'] = u'全店通用券'
							qrcode.award_prize_info = json.dumps(info_dict)
					except Exception, e:
						print 'qrcode获取优惠券剩余个数失败：', e

					if qrcode.reply_material_id > 0:
						answer_content['type'] = 'news'
						answer_content['newses'] = []
						answer_content['content'] = qrcode.reply_material_id
						newses = News.get_news_by_material_id(qrcode.reply_material_id)

						news_array = []
						for news in newses:
							news_dict = {}
							news_dict['id'] = news.id
							news_dict['title'] = news.title
							answer_content['newses'].append(news_dict)
					else:
						answer_content['type'] = 'text'
						answer_content['content'] = emotion.change_emotion_to_img(qrcode.reply_detail)

					if qrcode.bing_member_id:
						bing_member = get_member_by_id(int(qrcode.bing_member_id))
						qrcode.bing_member_name = bing_member.username_for_html

		settings = ChannelQrcodeSettings.objects.filter(owner=request.manager, bing_member_id__gt=0)
		selectedMemberIds = [setting.bing_member_id for setting in settings]

		jsons = [{
			"name": "qrcode_answer",
			"content": answer_content
		}]
		if not qrcode:
			tag_id = -1
		else:
			tag_id = qrcode.tag_id
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_CHANNEL_QRCODE_SECOND_NAV,
			'third_nav_name': mall_export.ADVANCE_MANAGE_QRCODE_NAV,
			'webapp_id': webapp_id,
			'qrcode': qrcode,
			'groups': groups,
			'tags': tags,
			'tag_is_del': False if MemberTag.objects.filter(id=tag_id).count() > 0 else True,
			'selectedMemberIds': json.dumps(selectedMemberIds),
			'jsons': jsons,
			'qrcodes': qrcodes
		})
		return render_to_response('weixin/advance_manage/edit_qrcode.html', c)

	@login_required
	@mp_required
	def api_put(request):
		cur_setting = None
		name = request.POST["name"]
		award_prize_info = request.POST['prize_info'].strip()
		coupon_id = ''
		try:
			info_dict = json.loads(award_prize_info)
			if info_dict['type'] == u'优惠券':
				coupon_id = str(info_dict['id'])
			if not (info_dict.has_key('id') and info_dict.has_key('name') and info_dict.has_key('type')):
				1/0
		except Exception, e:
			response = create_response(401)
			response.errMsg = u'不合法的award_prize_info：' + award_prize_info
			return response.get_response()

		reply_type = int(request.POST.get("reply_type", 0))
		reply_detail = request.POST.get("reply_detail", '')
		reply_material_id = request.POST.get("reply_material_id", 0)
		remark = request.POST.get("remark", '')
		grade_id = int(request.POST.get("grade_id", -1))
		tag_id = int(request.POST.get("tag_id", -1))
		re_old_member = int(request.POST.get("re_old_member", 0))
		is_bing_member = request.POST.get("is_bing_member", 0)
		bing_member_id = int(request.POST.get("bing_member_id", 0))
		bing_member_title = request.POST.get("bing_member_title", "")
		qrcode_desc = request.POST.get("qrcode_desc", "")

		if reply_type == 0:
			reply_material_id = 0
			reply_detail = ''
		elif reply_type == 1:
			reply_material_id = 0
		elif reply_type == 2:
			reply_detail = ''

		cur_setting = ChannelQrcodeSettings.objects.create(
			owner=request.manager,
			name=name,
			award_prize_info=award_prize_info,
			reply_type=reply_type,
			reply_detail=reply_detail,
			reply_material_id=reply_material_id,
			remark=remark,
			grade_id=grade_id,
			tag_id=tag_id,
			re_old_member=re_old_member,
			is_bing_member=True if is_bing_member == "true" else False,
			bing_member_id=bing_member_id,
			bing_member_title=bing_member_title,
			qrcode_desc=qrcode_desc,
			coupon_ids=coupon_id
		)

		if cur_setting.is_bing_member:
			ChannelQrcodeBingMember.objects.create(
				channel_qrcode=cur_setting,
				member_id=bing_member_id
			)

		if settings.MODE != 'develop':
			mp_user = get_binding_weixin_mpuser(request.manager)
			mpuser_access_token = get_mpuser_accesstoken(mp_user)
			weixin_api = get_weixin_api(mpuser_access_token)

			try:
				qrcode_ticket = weixin_api.create_qrcode_ticket(int(cur_setting.id), QrcodeTicket.PERMANENT)
				ticket = qrcode_ticket.ticket
			except Exception, e:
				print 'get qrcode_ticket fail:', e
				ticket = ''
		else:
			ticket = ''
		cur_setting.ticket = ticket
		cur_setting.save()

		if cur_setting:
			response = create_response(200)
		else:
			response = create_response(400)

		return response.get_response()

	@login_required
	@mp_required
	def api_post(request):
		setting_id = request.POST.get('setting_id', None)
		if not setting_id:
			return create_response(400).get_response()

		name = request.POST["name"]
		award_prize_info = request.POST['prize_info'].strip()
		coupon_id = ''
		try:
			info_dict = json.loads(award_prize_info)
			if info_dict['type'] == u'优惠券':
				coupon_id = info_dict['id']
			if not (info_dict.has_key('id') and info_dict.has_key('name') and info_dict.has_key('type')):
				1/0
		except Exception, e:
			response = create_response(401)
			response.errMsg = u'不合法的award_prize_info：' + award_prize_info
			return response.get_response()
		reply_type = int(request.POST.get("reply_type", 0))
		reply_detail = request.POST.get("reply_detail", '')
		reply_material_id = request.POST.get("reply_material_id", 0)
		remark = request.POST.get("remark", '')
		grade_id = int(request.POST.get("grade_id", -1))
		tag_id = int(request.POST.get("tag_id", -1))
		re_old_member = int(request.POST.get("re_old_member", 0))
		is_bing_member = request.POST.get("is_bing_member", 0)
		bing_member_id = int(request.POST.get("bing_member_id", 0))
		bing_member_title = request.POST.get("bing_member_title", "")
		qrcode_desc = request.POST.get("qrcode_desc", "")

		if reply_type == 0:
			reply_material_id = 0
			reply_detail = ''
		elif reply_type == 1:
			reply_material_id = 0
		elif reply_type == 2:
			reply_detail = ''

		#批量修改
		if len(setting_id.split(',')) > 1:
			settings = ChannelQrcodeSettings.objects.filter(owner=request.manager, id__in=setting_id.split(','))
			for s in settings:
				s.award_prize_info = award_prize_info
				s.reply_type = reply_type
				s.reply_detail = reply_detail
				s.reply_material_id = reply_material_id
				s.remark = remark
				s.grade_id = grade_id
				s.tag_id = tag_id
				s.re_old_member = re_old_member
				s.coupon_ids = s.coupon_ids + ',' + str(coupon_id)
				s.save()
	
			return create_response(200).get_response()

		setting = ChannelQrcodeSettings.objects.filter(owner=request.manager, id=setting_id)
		coupon_ids = setting[0].coupon_ids.split(',')
		coupon_ids.append(str(coupon_id))
		coupon_ids = ','.join(coupon_ids)
		if setting[0].bing_member_id and is_bing_member == 'false':
			#取消关联
			setting.update(
				name=name,
				award_prize_info=award_prize_info,
				reply_type=reply_type,
				reply_detail=reply_detail,
				reply_material_id=reply_material_id,
				remark=remark,
				grade_id=grade_id,
				tag_id=tag_id,
				re_old_member=re_old_member,
				is_bing_member=True if is_bing_member == "true" else False,
				coupon_ids=coupon_ids
			)
			ChannelQrcodeBingMember.objects.filter(channel_qrcode=setting[0]).update(
				cancel_bing_time=datetime.now()
			)
		else:
			if not setting[0].bing_member_id and is_bing_member == 'true':
				ChannelQrcodeBingMember.objects.create(
					channel_qrcode=setting[0],
					member_id=bing_member_id,
				)
			setting.update(
				name=name,
				award_prize_info=award_prize_info,
				reply_type=reply_type,
				reply_detail=reply_detail,
				reply_material_id=reply_material_id,
				remark=remark,
				grade_id=grade_id,
				tag_id=tag_id,
				re_old_member=re_old_member,
				is_bing_member=True if is_bing_member == "true" else False,
				bing_member_id=bing_member_id,
				bing_member_title=bing_member_title,
				qrcode_desc=qrcode_desc,
				coupon_ids=coupon_ids
			)

		return create_response(200).get_response()

class QrcodeMember(resource.Resource):
	app = 'new_weixin'
	resource = 'qrcode_member'

	@login_required
	@mp_required
	def get(request):
		"""
		带参数二维码
		"""
		setting_id = request.GET['setting_id']
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_CHANNEL_QRCODE_SECOND_NAV,
			'third_nav_name': mall_export.ADVANCE_MANAGE_QRCODE_NAV,
			'setting_id': setting_id
		})

		return render_to_response('weixin/advance_manage/qrcode_member.html', c)

	@login_required
	@mp_required
	def api_get(request):
		setting_id = int(request.GET['setting_id'])
		start_date = request.GET.get('start_date', '')
		end_date = request.GET.get('end_date', '')
		member_status = int(request.GET.get('status', -1))
		is_show = request.GET.get('is_show', '0')

		sort_attr = request.GET.get('sort_attr', '-created_at')

		if is_show == '1':
			member_ids = [relation.member_id for relation in \
				ChannelQrcodeHasMember.objects.filter(channel_qrcode=setting_id, is_new=True)]
		else:
			member_ids = [relation.member_id for relation in \
				ChannelQrcodeHasMember.objects.filter(channel_qrcode=setting_id)]

		filter_data_args = {}
		filter_data_args['id__in'] = member_ids

		if start_date:
			filter_data_args['created_at__gte'] = start_date

		if end_date:
			filter_data_args['created_at__lte'] = end_date

		if member_status != -1:
			filter_data_args['status'] = member_status

		channel_members = Member.objects.filter(**filter_data_args).order_by(sort_attr)
		count_per_page = int(request.GET.get('count_per_page', 15))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, channel_members = paginator.paginate(channel_members, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		return_channel_members_json_array = []

		for channel_member in channel_members:
			member_info = member_model.MemberInfo.get_member_info(channel_member.id)
			if member_info:
				channel_member.name = member_info.name
			else:
				channel_member.name = ''

			return_channel_members_json_array.append(build_member_basic_json(channel_member))

		response = create_response(200)
		response.data = {
			'items': return_channel_members_json_array,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': sort_attr,
			'data': {}
		}

		return response.get_response()

def build_member_basic_json(member):
	return {
		'id': member.id,
		'username': member.username_for_html,
		'name': member.name,
		'user_icon': member.user_icon,
		'integral': member.integral,
		'pay_money': '%.2f' % member.pay_money,
		'pay_times': member.pay_times,
		'grade_name': member.grade.name,
		"follow_time": member.created_at.strftime('%Y-%m-%d %H:%M:%S'),
		"is_subscribed": member.is_subscribed
	}

def get_order_status_text(status):
	from mall.models import STATUS2TEXT
	return STATUS2TEXT[status]

class QrcodeOrder(resource.Resource):
	app = 'new_weixin'
	resource = 'qrcode_order'

	@login_required
	@mp_required
	def get(request):
		"""
		带参数二维码
		"""
		setting_id = request.GET.get('setting_id', None)
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_CHANNEL_QRCODE_SECOND_NAV,
			'third_nav_name': mall_export.ADVANCE_MANAGE_QRCODE_NAV,
			'setting_id': setting_id
		})

		return render_to_response('weixin/advance_manage/qrcode_order.html', c)

	@login_required
	@mp_required
	def api_get(request):
		from mall import module_api as mall_api
		from mall.models import *
		channel_qrcode_id = request.GET.get('setting_id', None)
		start_date = request.GET.get('start_date', '')
		end_date = request.GET.get('end_date', '')
		is_show = request.GET.get('is_show', '0')

		filter_data_args = {}

		if start_date:
			filter_data_args['created_at__gte'] = start_date

		if end_date:
			filter_data_args['created_at__lte'] = end_date
		filter_data_args['status__in'] = (ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED)

		relations = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=channel_qrcode_id)
		setting_id2count = {}
		member_id2setting_id = {}
		member_ids = []

		old_member_id2_create_at = {}
		new_member_id2_create_at = {}
		for r in relations:
			member_ids.append(r.member_id)
			member_id2setting_id[r.member_id] = r.channel_qrcode_id
			if r.channel_qrcode_id in setting_id2count:
				setting_id2count[r.channel_qrcode_id] += 1
			else:
				setting_id2count[r.channel_qrcode_id] = 1
			if r.is_new:
				new_member_id2_create_at[r.member_id] = r.created_at
			else:
				old_member_id2_create_at[r.member_id] = r.created_at

		if is_show == '1':
			#获取新会员的webapp_user
			new_webapp_users = WebAppUser.objects.filter(member_id__in=new_member_id2_create_at.keys())
			new_webapp_user_ids = [u.id for u in new_webapp_users]

			#获取old会员的webapp_user
			old_webapp_users = WebAppUser.objects.filter(member_id__in=old_member_id2_create_at.keys())
			old_member_order_ids = []
			for webapp_user in old_webapp_users:
				created_at = old_member_id2_create_at[webapp_user.member_id]
				for order in Order.by_webapp_user_id(webapp_user.id).filter(created_at__gte=created_at):
					old_member_order_ids.append(order.id)

			if new_webapp_user_ids and old_member_order_ids:
				orders = Order.by_webapp_user_id(new_webapp_user_ids, order_id=old_member_order_ids).filter(**filter_data_args).order_by('-created_at')
			elif new_webapp_user_ids:
				orders = Order.by_webapp_user_id(new_webapp_user_ids).filter(**filter_data_args).order_by('-created_at')
			elif old_member_order_ids:
				filter_data_args['id__in'] = old_member_order_ids
				orders = Order.objects.filter(**filter_data_args).order_by('-created_at')
			else:
				orders = []
		else:
			webapp_users = WebAppUser.objects.filter(member_id__in=member_ids)
			webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
			webapp_user_ids = set(webapp_user_id2member_id.keys())
			if webapp_user_ids:
				orders = Order.by_webapp_user_id(webapp_user_ids).filter(**filter_data_args).order_by('-created_at')
			else:
				orders = []


		#add by duhao 2015-06-29 统计微众卡支付总金额和现金支付总金额
		final_price = 0
		weizoom_card_money = 0
		for order in orders:
			final_price += order.final_price
			weizoom_card_money += order.weizoom_card_money


		#进行分页
		count_per_page = int(request.GET.get('count_per_page', 15))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		#获取order对应的会员
		webapp_user_ids = set([order.webapp_user_id for order in orders])
		from modules.member.models import Member
		webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

		#获得order对应的商品数量
		order_ids = [order.id for order in orders]
		order2productcount = {}
		for relation in OrderHasProduct.objects.filter(order_id__in=order_ids):
			order_id = relation.order_id
			if order_id in order2productcount:
				order2productcount[order_id] = order2productcount[order_id] + 1
			else:
				order2productcount[order_id] = 1
		#构造返回的order数据
		items = []
		today = datetime.today()

		for order in  orders:
			 #获取order对应的member的显示名
			 member = webappuser2member.get(order.webapp_user_id, None)
			 if member:
				 order.buyer_name = member.username_for_html
				 order.buyer_id = member.id
			 else:
				 order.buyer_name = u'未知'

			 items.append({
				'id': order.id,
				'source': order.order_source,
				'order_id': order.order_id,
				'status': get_order_status_text(order.status),
				'total_price': order.final_price,
				'ship_name': order.ship_name,
				'buyer_name': order.buyer_name,
				'buyer_id': order.buyer_id,
				'pay_interface_name': PAYTYPE2NAME.get(order.pay_interface_type, u''),
				'created_at': datetime.strftime(order.created_at,'%Y-%m-%d %H:%M'),
				'payment_time':datetime.strftime(order.payment_time,'%Y-%m-%d %H:%M'),
				'product_count': order2productcount.get(order.id, 0),
				'products': mall_api.get_order_products(order),
				'customer_message': order.customer_message,
				'order_status':order.status,
				'express_company_name': order.express_company_name,
				'express_number': order.express_number,
				'leader_name': order.leader_name,
				'remark': order.remark,
				'postage': '%.2f' % order.postage,
				'save_money': '%.2f' % (float(Order.get_order_has_price_number(order)) + float(order.postage) - float(order.final_price) - float(order.weizoom_card_money)),
				'weizoom_card_money': float('%.2f' % order.weizoom_card_money),
				'pay_money': '%.2f' % (order.final_price + order.weizoom_card_money),
				'is_first_order': order.is_first_order
			 })

		response = create_response(200)
		response.data = {
			'items': items,
			'final_price': '%.2f' % final_price,
			'weizoom_card_money': '%.2f' % weizoom_card_money,
			'sortAttr': request.GET.get('sort_attr', '-created_at'),
			'pageinfo': paginator.to_dict(pageinfo),
			'data': {}
		}
		return response.get_response()

class QrcodesFilter(resource.Resource):
	app = 'new_weixin'
	resource = 'qrcodes_filter'

	@login_required
	@mp_required
	def api_get(request):
		sort_attr = request.GET.get('sort_attr', '-created_at')
		items = _get_filter_qrcode_items(request)

		#进行分页

		if 'created_at' not in  sort_attr:
			if '-' in sort_attr:
				sorter = sort_attr[1:]
				is_reverse = True
			else:
				sorter = sort_attr
				is_reverse = False

			# items = sorted(items, reverse=is_reverse, key=lambda b : getattr(b, sorter))
			items = sorted(items, reverse=is_reverse, key=lambda x:getattr(x, sorter))
		count_per_page = int(request.GET.get('count_per_page', 15))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, items = paginator.paginate(items, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		new_items = []
		for item in items:
			new_items.append(item.__dict__)

		response = create_response(200)
		response.data = {
			'items': new_items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': sort_attr,
			'data': {}
		}
		return response.get_response()

def _get_filter_qrcode_items(request):
	#处理搜索
	from mall.models import *
	query = request.GET.get('query', '').strip()
	sort_attr = request.GET.get('sort_attr', '-created_at')
	created_at = '-created_at'
	if 'created_at' in  sort_attr:
		created_at = sort_attr

	if query:
		settings = ChannelQrcodeSettings.objects.filter(owner=request.manager, name__contains=query).order_by(created_at)
	else:
		settings = ChannelQrcodeSettings.objects.filter(owner=request.manager).order_by(created_at)

	items = []

	mp_user = get_binding_weixin_mpuser(request.manager)
	mpuser_access_token = get_mpuser_accesstoken(mp_user)

	for setting in settings:
		current_setting = JsonResponse()
		prize_info = decode_json_str(setting.award_prize_info)
		if prize_info['name'] == '_score-prize_':
			setting.cur_prize = '[%s]%d' % (prize_info['type'], prize_info['id'])
		elif prize_info['name'] == 'non-prize':
			setting.cur_prize = prize_info['type']
		else:
			setting.cur_prize = '[%s]%s' % (prize_info['type'], prize_info['name'])


		#如果没有ticket信息则获取ticket信息
		if not setting.ticket:
			try:
				if mp_user.is_certified and mp_user.is_service and mpuser_access_token.is_active:
					weixin_api = get_weixin_api(mpuser_access_token)
					qrcode_ticket = weixin_api.create_qrcode_ticket(int(setting.id), QrcodeTicket.PERMANENT)

					try:
						ticket = qrcode_ticket.ticket
					except:
						ticket = ''
					setting.ticket = ticket
					setting.save()
			except:
				pass
		current_setting.id = setting.id
		current_setting.name = setting.name
		current_setting.re_old_member =  u'是'if setting.re_old_member else u'否'
		current_setting.cur_prize = setting.cur_prize
		current_setting.ticket = setting.ticket
		current_setting.created_at = setting.created_at.strftime('%Y-%m-%d %H:%M:%S')

		items.append(current_setting)
	return items

class GetCanUseCoupon(resource.Resource):
	app = 'new_weixin'
	resource = 'coupon_can_use'

	@login_required
	@mp_required
	def api_get(request):
		"""
		判断优惠券是否之前使用过
		"""
		coupon_id = request.GET.get('coupon_id',None)
		setting_id = request.GET.get('setting_id',None)
		if setting_id:
			setting_ids = setting_id.split(',')
			settings = ChannelQrcodeSettings.objects.filter(id__in = setting_ids)
			for s in settings:
				coupon_ids = s.coupon_ids.split(',')
				if coupon_id and (coupon_id in coupon_ids):
					response = create_response(500)
					response.errMsg = u'该优惠券已被选用过！'
					return response.get_response()

		response = create_response(200)
		return response.get_response()

def format_award_prize_info(info):
	"""
	{"id":2,"name":"_score-prize_","type":"积分"} => 2积分

	"""
	info = json.loads(info)
	if info['type'] == u'积分':
		return u"%s积分"% info['id']
	else:
		return info['type']



class ChannelDistributions(resource.Resource):
	app = 'new_weixin'
	resource = 'channel_distributions'

	@login_required
	def get(request):
		"""渠道分销"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_CHANNEL_QRCODE_SECOND_NAV,
			'third_nav_name': mall_export.ADVANCE_MANAGE_CHANNEL_DISTRIBUTIONS_NAV,
		})
		return render_to_response('weixin/channels/channel_distributions.html', c)

	def api_get(request):
		distribution_rewards_status = {
			0: u'无',
			1: u'佣金'
		}

		query_name = request.GET.get('query_name')
		sort_attr = request.GET.get('sort_attr', '-created_at')
		count_per_page = int(request.GET.get('count_per_page', 15))
		# count_per_page = 1
		cur_page = int(request.GET.get('page', '1'))
		# 取出管理员的所有二维码
		qrcodes = ChannelDistributionQrcodeSettings.objects.filter(owner=request.user)
		member_ids = []
		for qrcode in qrcodes:
			member_ids.append(qrcode.bing_member_id)

		member_dict = {}  # {id: name}
		members = Member.objects.filter(id__in=member_ids)
		for member in members:
			member_dict[member.id] = member.username_for_title

		if query_name:
			qrcodes = ChannelDistributionQrcodeSettings.objects.filter(owner=request.user, bing_member_title__icontains=query_name).order_by('-is_new', sort_attr)
		else:
			qrcodes = ChannelDistributionQrcodeSettings.objects.filter(owner=request.user).order_by('-is_new', sort_attr)




		pageinfo, qrcodes = paginator.paginate(qrcodes, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		items = []
		for qrcode in qrcodes:
			qrcode_dict = {}
			qrcode_dict['id'] = qrcode.id
			qrcode_dict['title'] = qrcode.bing_member_title  # 标题
			qrcode_dict['bing_member_name'] = member_dict[qrcode.bing_member_id]  # 关联会员: 是名字
			qrcode_dict['bing_member_count'] = qrcode.bing_member_count  # 关注数量
			qrcode_dict['total_transaction_volume'] = str(qrcode.total_transaction_volume)  # 总交易额
			qrcode_dict['total_return'] = str(qrcode.total_return)  # 总返现额
			qrcode_dict['award_prize_info'] = format_award_prize_info(qrcode.award_prize_info)  # 关注奖励
			qrcode_dict['distribution_rewards'] = str(distribution_rewards_status[qrcode.distribution_rewards])  # 分销奖励
			qrcode_dict['created_at'] = str(qrcode.created_at)  # 创建时间
			qrcode_dict['clearing'] = ''  # 会员结算 TODO 有新的提现请求显示new
			qrcode_dict['ticket'] = qrcode.ticket
			qrcode_dict['is_new'] = qrcode.is_new
			items.append(qrcode_dict)

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': sort_attr,
			'data': {}
		}
		return response.get_response()


class ChannelDistribution(resource.Resource):
	app = 'new_weixin'
	resource = 'channel_distribution'

	@login_required
	def get(request):
		"""渠道分销,新建二维码 和 编辑二维码页面"""
		setting_id = int(request.GET.get('setting_id', '-1'))
		qrcode = None
		jsons = []
		member_name = ''  # 绑定昵称

		if setting_id > 0:
			qrcode = ChannelDistributionQrcodeSettings.objects.get(id=setting_id)
			if qrcode and (qrcode.owner_id == request.user.id): # 如果有二维码,
				# 获取优惠券剩余个数
				award_prize_info = qrcode.award_prize_info
				info_dict = json.loads(award_prize_info)
				if info_dict['type'] == u'优惠券':
					coupon_rule = CouponRule.objects.get(id=info_dict['id'])
					info_dict['remained_count'] = coupon_rule.remained_count
					if coupon_rule.limit_product:
						info_dict['coupon_type'] = u'单品券'
					else:
						info_dict['coupon_type'] = u'全店通用券'
					qrcode.award_prize_info = json.dumps(info_dict)

				answer_content = {}
				if qrcode.reply_material_id > 0:
					answer_content['type'] = 'news'
					answer_content['newses'] = []
					answer_content['content'] = qrcode.reply_material_id
					newses = News.get_news_by_material_id(qrcode.reply_material_id)

					news_array = []
					for news in newses:
						news_dict = {}
						news_dict['id'] = news.id
						news_dict['title'] = news.title
						answer_content['newses'].append(news_dict)
				else:
					answer_content['type'] = 'text'
					answer_content['content'] = emotion.change_emotion_to_img(qrcode.reply_detail)
				# jsons : 扫码回复的数据
				jsons = [{
					"name": "qrcode_answer",
					"content": answer_content
				}]
				member = Member.objects.get(id=qrcode.bing_member_id)
				member_name = member.username_for_title
			else:
				return HttpResponseRedirect('/new_weixin/channel_distributions/')  # 阻止非该二维码所有者访问

		webapp_id = request.user_profile.webapp_id
		groups = MemberGrade.get_all_grades_list(webapp_id)
		member_tags = MemberTag.get_member_tags(webapp_id)
		edit_qrcode = None
		# 调整排序，将为分组放在最前面
		tags = []
		for tag in member_tags:
			if tag.name == '未分组':
				tags = [tag] + tags
			else:
				tags.append(tag)

		input_disabled = True  # 前端修改3个字段的属性为disabled
		if request.user.username == 'weizoomxiaoyuan':
			input_disabled = False
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_CHANNEL_QRCODE_SECOND_NAV,
			'third_nav_name': mall_export.ADVANCE_MANAGE_CHANNEL_DISTRIBUTIONS_NAV,
			'tags': tags,
			'webapp_id': webapp_id,
			'edit_qrcode': edit_qrcode,
			'qrcode': qrcode,
			'jsons': jsons,
			'member_name': member_name,
			'input_disabled' : input_disabled
			# 'selectedMemberIds': json.dumps(selectedMemberIds),
		})
		return render_to_response('weixin/channels/channel_distribution.html', c)

	@login_required
	def api_put(request):
		"""新建渠道分销二维码"""
		bing_member_title = request.POST["bing_member_title"]  # 会员头衔
		if  ChannelDistributionQrcodeSettings.objects.filter(bing_member_title=bing_member_title).exists():  # 检测重复
			response = create_response(500)
			response.errMsg = u"重复的会员头衔"
			return response.get_response()

		bing_member_id = request.POST["bing_member_id"]  # 关联会员
		if ChannelDistributionQrcodeSettings.objects.filter(bing_member_id=bing_member_id).exists():
			response = create_response(500)
			response.errMsg = u"一个会员只能绑定一个二维码"
			return response.get_response()

		if ChannelQrcodeSettings.objects.filter(bing_member_id=bing_member_id).exists():
			response = create_response(500)
			response.errMsg = u"一个会员只能绑定一个二维码"
			return response.get_response()

		award_prize_info = request.POST['prize_info'].strip()  # 扫描奖励
		coupon_id = ''

		info_dict = json.loads(award_prize_info)
		if info_dict['type'] == u'优惠券':
			coupon_id = str(info_dict['id'])
		if not (info_dict.has_key('id') and info_dict.has_key('name') and info_dict.has_key('type')):
			response = create_response(500)
			response.errMsg = u'不合法的award_prize_info：' + award_prize_info
			return response.get_response()


		distribution_rewards = int(request.POST["distribution_rewards"])  # 分销奖励 0:无 1:佣金
		if distribution_rewards == 0:  # 如果分销奖励是无
			commission_rate = 0
			minimun_return_rate = 0
			commission_return_standard = 0
			return_standard = 0
		elif distribution_rewards == 1:
			commission_rate = int(request.POST.get("commission_rate", 0))  # 佣金返现率
			minimun_return_rate = int(request.POST.get("minimun_return_rate", 0))  # 最低返现折扣
			commission_return_standard = float(request.POST.get("commission_return_standard", 0))  # 佣金返现标准
			return_standard = int(request.POST.get("return_standard", 0))  # 多少天返现标准

			if commission_rate > 20 or commission_rate < 0:
				response = create_response(500)
				response.errMsg = u'佣金返现率输入错误'
				return response.get_response()

			if minimun_return_rate > 100 or minimun_return_rate < 0:
				response = create_response(500)
				response.errMsg = u'最低返现折扣输入错误'
				return response.get_response()

			if commission_return_standard < 0:
				response = create_response(500)
				response.errMsg = u'佣金返现标准输入错误'
				return response.get_response()

			if 7 >= return_standard >= 0:
				pass
			else:
				response = create_response(500)
				response.errMsg = u'请输入大于等于0且小于等于7的数字'
				return response.get_response()

		group_id = request.POST["group_id"]  # 添加到分组,会员分组
		reply_type = request.POST['reply_type']  # 回复类型
		reply_material_id = request.POST['reply_material_id']  # 图文

		if reply_type == '0':
			reply_material_id = 0
			reply_detail = ''
		elif reply_type == '1':
			reply_material_id = 0
			reply_detail = request.POST['reply_detail']
		elif reply_type == '2':
			reply_detail = ''

		cur_setting = ChannelDistributionQrcodeSettings.objects.create(
			owner = request.user,
			bing_member_title = bing_member_title,
			bing_member_id = bing_member_id,
			award_prize_info = award_prize_info,
			distribution_rewards = distribution_rewards,
			commission_rate = commission_rate,
			minimun_return_rate = minimun_return_rate,
			commission_return_standard = commission_return_standard,
			return_standard = return_standard,
			group_id = group_id,
			coupon_ids = coupon_id,
			reply_type = reply_type,
			reply_detail = reply_detail,
			reply_material_id = reply_material_id,
		)

		if settings.MODE != 'develop':
			mp_user = get_binding_weixin_mpuser(request.user)
			mpuser_access_token = get_mpuser_accesstoken(mp_user)
			weixin_api = get_weixin_api(mpuser_access_token)

			try:
				qrcode_ticket = weixin_api.create_qrcode_ticket(int(cur_setting.id), QrcodeTicket.PERMANENT)
				ticket = qrcode_ticket.ticket
			except Exception, e:
				ticket = ''
		else:
			ticket = ''

		cur_setting.ticket = ticket

		create_time = request.POST.get('create_time')
		if create_time:
			cur_setting.created_at = create_time
		cur_setting.save()

		if cur_setting:
			response = create_response(200)
		else:
			response = create_response(500)

		return response.get_response()

	@login_required
	def api_post(request):
		"""更新渠道分销二维码"""

		qrcode_id = int(request.POST.get('qrcode_id'))
		group_id = request.POST['group_id']
		prize_info = request.POST['prize_info']
		reply_type = request.POST['reply_type']
		reply_detail = request.POST['reply_detail']
		reply_material_id = request.POST['reply_material_id']
		commission_rate = int(request.POST['commission_rate'])  # 佣金返现率
		minimun_return_rate = int(request.POST['minimun_return_rate'])  # 最低返现折扣
		commission_return_standard = float(request.POST['commission_return_standard'])  # 佣金返现标准


		# 如果修改者操作的二维码不是自己的 不执行任何操作
		if ChannelDistributionQrcodeSettings.objects.filter(id=qrcode_id, owner_id=request.user.id).exists():

			bing_member_title = request.POST["bing_member_title"]  # 会员头衔
			if ChannelDistributionQrcodeSettings.objects.filter(bing_member_title=bing_member_title).exclude(id=qrcode_id):  # 检测重复
				response = create_response(500)
				response.errMsg = u"重复的会员头衔"
				return response.get_response()

			if request.user.username == 'weizoomxiaoyuan':  # 一个奇怪的需求,单独给这个用户添加修改3个字段的权限.
				if commission_rate > 20 or commission_rate < 0:
					response = create_response(500)
					response.errMsg = u'佣金返现率输入错误'
					return response.get_response()

				if minimun_return_rate > 100 or minimun_return_rate < 0:
					response = create_response(500)
					response.errMsg = u'最低返现折扣输入错误'
					return response.get_response()

				if commission_return_standard < 0:
					response = create_response(500)
					response.errMsg = u'佣金返现标准输入错误'
					return response.get_response()

				ChannelDistributionQrcodeSettings.objects.filter(id=qrcode_id).update(
					bing_member_title = bing_member_title,
					group_id = group_id,
					award_prize_info = prize_info,
					reply_type = reply_type,
					reply_detail = reply_detail,
					reply_material_id = reply_material_id,
					commission_rate = commission_rate,
					minimun_return_rate = minimun_return_rate,
					commission_return_standard = commission_return_standard
				)
			else:
				ChannelDistributionQrcodeSettings.objects.filter(id=qrcode_id).update(
					bing_member_title=bing_member_title,
					group_id=group_id,
					award_prize_info=prize_info,
					reply_type=reply_type,
					reply_detail=reply_detail,
					reply_material_id=reply_material_id,
				)

			response = create_response(200)
			return response.get_response()
		else:
			response = create_response(500)
			return response.get_response()


class ChannelDistributionClearing(resource.Resource):
	app = 'new_weixin'
	resource = 'distribution_clearing'

	@login_required
	def get(request):
		"""
		分销会员结算
		"""
		qrcodes = ChannelDistributionQrcodeSettings.objects.filter(owner__id=request.user.id)
		return_money_total = 0  # 已返现总额
		not_return_money_total = 0  # 未返现总额
		current_total_return = 0# 本期返现总额
		total_transaction_volume = 0 # 总交易额
		extraction_money = 0  # 所有的extraction_money 之和

		for qrcode in qrcodes:
			total_transaction_volume += qrcode.total_transaction_volume
			return_money_total += qrcode.total_return
			# current_total_return += qrcode.will_return_reward
			extraction_money += qrcode.extraction_money
			not_return_money_total += qrcode.will_return_reward
			if qrcode.status > 0:
				current_total_return += qrcode.extraction_money

		qrcodes.update(is_new=False)
		webapp_id = request.user_profile.webapp_id

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_CHANNEL_QRCODE_SECOND_NAV,
			'third_nav_name': mall_export.ADVANCE_MANAGE_CHANNEL_DISTRIBUTIONS_NAV,
			'return_money_total': return_money_total,
			'not_return_money_total': not_return_money_total,
			'current_total_return': current_total_return,
			'total_transaction_volume': total_transaction_volume,
			'webapp_id': webapp_id,
		})


		return render_to_response('weixin/channels/channel_distribution_clearing.html', c)

	@login_required
	def api_get(request):

		sort_attr = request.GET.get('sort_attr', '-created_at')
		count_per_page = int(request.GET.get('count_per_page', 15))
		cur_page = int(request.GET.get('page', '1'))
		return_min = request.GET.get('return_min')
		return_max = request.GET.get('return_max')
		start_date = request.GET.get('start_date')
		end_date = request.GET.get('end_date')

		# 取出管理员的所有二维码
		qrcodes = ChannelDistributionQrcodeSettings.objects.filter(owner=request.user)
		member_ids = []
		for qrcode in qrcodes:
			member_ids.append(qrcode.bing_member_id)
		member_dict = {}  # {id: name}
		members = Member.objects.filter(id__in=member_ids)
		for member in members:
			member_dict[member.id] = member.username_for_title

		qrcodes = ChannelDistributionQrcodeSettings.objects.filter(owner=request.user).order_by('-status', '-commit_time')
		if return_min:
			if return_max:
				qrcodes = qrcodes.filter(extraction_money__range=(return_min, return_max))
			else:
				qrcodes =  qrcodes.filter(extraction_money__gte=return_min)
		elif return_max:
			qrcodes = qrcodes.filter(extraction_money__lte=return_max)
		if start_date and end_date:
			qrcodes = qrcodes.filter(commit_time__range=(start_date, end_date))


		pageinfo, qrcodes = paginator.paginate(qrcodes, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		items = []
		for qrcode in qrcodes:
			commit_time = qrcode.commit_time
			if str(commit_time) == '0001-01-01 00:00:00':
				commit_time = '----'
			else:
				commit_time = str(qrcode.commit_time)
			return_dict = {}

			return_dict['qrcode_id'] = qrcode.id
			return_dict['name'] = member_dict[qrcode.bing_member_id]  # 用户名
			return_dict['commit_time'] = commit_time  # 提交时间
			return_dict['current_transaction_amount'] = str(qrcode.current_transaction_amount)  # 本期交易额
			return_dict['commission_return_standard']  = str(qrcode.commission_return_standard)  # 返现标准
			return_dict['commission_rate'] = qrcode.commission_rate  # 返现率
			return_dict['will_return_reward'] = str(qrcode.will_return_reward)  # 实施奖励
			return_dict['extraction_money'] = str(qrcode.extraction_money)  # 返现金额
			return_dict['status'] = qrcode.status  # 返现状态
			items.append(return_dict)

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': sort_attr,
			'data': {}
		}
		return response.get_response()


class ChannelDistributionTransactionAmount(resource.Resource):
	app = 'new_weixin'
	resource = 'channel_distribution_transaction_amount'

	@login_required
	def api_get(request):
		"""
		查看记录的一个页面
		"""
		# log_select = int(request.POST.get('log_select', 1))  # 0 本期, 1总的
		qrcode_id = request.GET.get('qrcode_id')
		count_per_page = int(request.GET.get('count_per_page', 15))
		cur_page = int(request.GET.get('page', '1'))
		items = []
		total_money = 0

		# 得到该店铺下所有绑定会员
		channel_distribution_has_members = ChannelDistributionQrcodeHasMember.objects.filter(
			channel_qrcode_id=qrcode_id)

		member_ids = []
		for channel_distribution_has_member in channel_distribution_has_members:
			member_ids.append(channel_distribution_has_member.member_id)

		member_dict = {}  # {id: name}
		members = Member.objects.filter(id__in=member_ids)

		for member in members:
			member_dict[member.id] = member.username_for_title

		pageinfo, channel_distribution_has_members = paginator.paginate(channel_distribution_has_members, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		for channel_distribution_has_member in channel_distribution_has_members:
			dict = {}
			dict['name'] = member_dict[channel_distribution_has_member.member_id]
			dict['cost_money'] = str(channel_distribution_has_member.cost_money)  # 花费的金额
			dict['commission'] = str(channel_distribution_has_member.commission)  #　带来的佣金
			total_money += channel_distribution_has_member.cost_money
			items.append(dict)


		response = create_response(200)
		response.data = {
			'items': items,
			'total_money': str(total_money),
			'pageinfo': paginator.to_dict(pageinfo),
		}
		return response.get_response()


class ChannelDistributionRewardDetail(resource.Resource):
	"""奖励明细"""
	app = 'new_weixin'
	resource = 'channel_distribution_detail'

	@login_required
	def api_get(request):
		count_per_page = int(request.GET.get('count_per_page', 15))
		cur_page = int(request.GET.get('page', '1'))
		qrcode_id = request.GET.get('qrcode_id')
		qrocde = ChannelDistributionQrcodeSettings.objects.get(id=qrcode_id)

		details = ChannelDistributionDetail.objects.filter(channel_qrcode_id=qrcode_id, order_id=0)

		pageinfo, details = paginator.paginate(details, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		items = []
		for detail in details:
			time_cycle_start = str(detail.last_extract_time)
			if time_cycle_start == '0001-01-01 00:00:00':
				time_cycle_start = '----'
			dict = {}

			dict['time_cycle_start'] = time_cycle_start  # 上次提现时间
			dict['time_cycle_end'] = str(detail.next_extract_time)
			dict['commission_rate'] = str(qrocde.commission_rate)  # 佣金返现率
			dict['total_money'] = str(detail.transaction_volume)
			dict['commission'] = str(detail.money)

			items.append(dict)

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
		}
		return response.get_response()


class ChannelDistributionChangeStatus(resource.Resource):
	app = 'new_weixin'
	resource = 'channel_distribution_change_status'

	@login_required
	def api_post(request):
		"""
		修改返款状态
		"""
		qrcode_id = request.POST.get('qrcode_id')
		status = int(request.POST.get('status'))

		qrcode = ChannelDistributionQrcodeSettings.objects.filter(id=qrcode_id, owner=request.user)

		# if status == 2 and qrcode[0].status > status:
		if qrcode[0].status < 1:
			response = create_response(200)
			response.errMsg = u"请等待会员申请返现"
			return response.get_response()


		if status == 2:
			# 等待审核--> 正在返现中
			qrcode.update(status=status)

		if status == 3:
			# 商家已打款
			extraction_money = qrcode[0].extraction_money

			channel_distribution_detail = ChannelDistributionDetail.objects.filter(channel_qrcode_id=qrcode[0].id, order_id=0)
			if channel_distribution_detail:
				last_extract_time = channel_distribution_detail[0].next_extract_time
			else:
				last_extract_time = qrcode[0].created_at

			# 新建奖励明细列表
			ChannelDistributionDetail.objects.create(
				channel_qrcode_id = qrcode_id,
				money = extraction_money,
				transaction_volume = qrcode[0].current_transaction_amount,
				member_id = qrcode[0].bing_member_id,
				last_extract_time = last_extract_time,  # start
				next_extract_time = qrcode[0].commit_time  # end
			)
			# 修改member带来的总佣金
			# ChannelDistributionQrcodeHasMember.objects.filter(channel_qrcode_id=qrcode[0].id).update(
			# 	commission = F('commission_not_add') + F('commission'),
			# 	commission_not_add = 0
			# )
			has_members = ChannelDistributionQrcodeHasMember.objects.filter(channel_qrcode_id=qrcode[0].id)

			for has_member in has_members:
				commission_not_add = has_member.commission_not_add
				has_member.commission = has_member.commission + commission_not_add
				has_member.commission_not_add = 0
				has_member.save()

			extraction_money = qrcode[0].extraction_money
			qrcode.update(
				total_return = F('total_return') + extraction_money,
				status = 0,
				# commit_time = datetime.strptime('0001-01-01', '%Y-%m-%d'),
				will_return_reward = F('will_return_reward') - F('extraction_money'),
				extraction_money = 0,
				current_transaction_amount = 0, # 本期交易额,清零
			)

		response = create_response(200)
		response.errMsg = u'修改成功'
		return response.get_response()

