# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from weixin.mp_decorators import mp_required
from django.shortcuts import render_to_response

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
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings,ChannelQrcodeHasMember
from modules.member import models as member_model
from mall import models as mall_model
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from mall.models import *
from mall import module_api as mall_api
from weixin2.message.util import get_member_groups
from modules.member.models import MemberGrade
from core.wxapi.api_create_qrcode_ticket import QrcodeTicket
import json
from mall.promotion.models import CouponRule

#COUNT_PER_PAGE = 2
COUNT_PER_PAGE = 50
FIRST_NAV = export.ADVANCE_MANAGE_FIRST_NAV

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
			'second_navs': export.get_advance_manage_second_navs(request),
			'second_nav_name': export.ADVANCE_MANAGE_QRCODE_NAV,
		})
		return render_to_response('weixin/advance_manage/qrcodes.html', c)

	@login_required
	@mp_required
	def api_get(request):
		#处理搜索
		query = request.GET.get('query', '').strip()
		sort_attr = request.GET.get('sort_attr', '-created_at')
		created_at = '-created_at'
		if 'created_at' in  sort_attr:
			created_at = sort_attr

		if query:
			settings = ChannelQrcodeSettings.objects.filter(owner=request.user, name__contains=query).order_by(created_at)
		else:
			settings = ChannelQrcodeSettings.objects.filter(owner=request.user).order_by(created_at)
		
		setting_ids = [s.id for s in settings]
		relations = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id__in=setting_ids)
		setting_id2count = {}
		member_id2setting_id = {} 
		member_ids = []
		for r in relations:
			member_ids.append(r.member_id)
			member_id2setting_id[r.member_id] = r.channel_qrcode_id
			if r.channel_qrcode_id in setting_id2count:
				setting_id2count[r.channel_qrcode_id] += 1
			else:
				setting_id2count[r.channel_qrcode_id] = 1
		
		webapp_users = member_model.WebAppUser.objects.filter(member_id__in=member_ids)
		webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
		webapp_user_ids = set(webapp_user_id2member_id.keys())
		orders = mall_model.Order.objects.filter(webapp_user_id__in=webapp_user_ids, status=mall_model.ORDER_STATUS_SUCCESSED)
		member_id2total_final_price = {}
		for order in orders:
			member_id = webapp_user_id2member_id[order.webapp_user_id]
			if member_id in member_id2total_final_price:
				member_id2total_final_price[member_id] += order.final_price
			else:
				member_id2total_final_price[member_id] = order.final_price
		
		setting_id2total_final_price = {}
		for member_id in member_id2total_final_price.keys():
			final_price = member_id2total_final_price[member_id]
			setting_id = member_id2setting_id[member_id]
			if setting_id in setting_id2total_final_price:
				setting_id2total_final_price[setting_id] += final_price
			else:
				setting_id2total_final_price[setting_id] = final_price
		
		
		response = create_response(200)
		#response.data.items = []
		items = []

		mp_user = get_binding_weixin_mpuser(request.user)
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
			
			if setting.id in setting_id2count:
				setting.count = setting_id2count[setting.id]
			else:
				setting.count = 0
			if setting.id in setting_id2total_final_price:
				setting.total_final_price = setting_id2total_final_price[setting.id]
			else:
				setting.total_final_price = 0
			
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
			current_setting.cur_prize = setting.cur_prize
			current_setting.ticket = setting.ticket
			current_setting.remark = setting.remark
			current_setting.created_at = setting.created_at.strftime('%Y-%m-%d %H:%M:%S')

			items.append(current_setting)

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
		answer_content = {}
		webapp_id = request.user_profile.webapp_id
		groups = MemberGrade.get_all_grades_list(webapp_id)
		qrcode = None

		if setting_id > 0:
			try:
				qrcode = ChannelQrcodeSettings.objects.get(id=setting_id, owner=request.user)
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

		jsons = [{
			"name": "qrcode_answer", "content": answer_content
		}]
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_advance_manage_second_navs(request),
			'second_nav_name': export.ADVANCE_MANAGE_QRCODE_NAV,
			'qrcode': qrcode,
			'groups': groups,
			'jsons': jsons
		})
		return render_to_response('weixin/advance_manage/edit_qrcode.html', c)

	@login_required
	@mp_required
	def api_put(request):
		cur_setting = None
		name = request.POST["name"]
		award_prize_info = request.POST['prize_info'].strip()
		try:
			info_dict = json.loads(award_prize_info)
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
		re_old_member = int(request.POST.get("re_old_member", 0))
		
		if reply_type == 0:
			reply_material_id = 0
			reply_detail = ''
		elif reply_type == 1:
			reply_material_id = 0
		elif reply_type == 2:
			reply_detail = ''
		
		cur_setting = ChannelQrcodeSettings.objects.create(
			owner=request.user, 
			name=name, 
			award_prize_info=award_prize_info,
			reply_type=reply_type,
			reply_detail=reply_detail,
			reply_material_id=reply_material_id,
			remark=remark,
			grade_id=grade_id,
			re_old_member=re_old_member
		)
		
		mp_user = get_binding_weixin_mpuser(request.user)
		mpuser_access_token = get_mpuser_accesstoken(mp_user)
		weixin_api = get_weixin_api(mpuser_access_token)
		
		try:
			qrcode_ticket = weixin_api.create_qrcode_ticket(int(cur_setting.id), QrcodeTicket.PERMANENT)
			ticket = qrcode_ticket.ticket
		except Exception, e:
			print 'get qrcode_ticket fail:', e
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
		setting_id = int(request.POST.get('setting_id', '-1'))
		if not setting_id > 0:
			return create_response(400).get_response()

		name = request.POST["name"]
		award_prize_info = request.POST['prize_info'].strip()
		try:
			info_dict = json.loads(award_prize_info)
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
		re_old_member = int(request.POST.get("re_old_member", 0))
		
		if reply_type == 0:
			reply_material_id = 0
			reply_detail = ''
		elif reply_type == 1:
			reply_material_id = 0
		elif reply_type == 2:
			reply_detail = ''
		
		ChannelQrcodeSettings.objects.filter(owner=request.user, id=setting_id).update(
			name=name, 
			award_prize_info=award_prize_info,
			reply_type=reply_type,
			reply_detail=reply_detail,
			reply_material_id=reply_material_id,
			remark=remark,
			grade_id=grade_id,
			re_old_member=re_old_member
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
			'second_navs': export.get_advance_manage_second_navs(request),
			'second_nav_name': export.ADVANCE_MANAGE_QRCODE_NAV,
			'setting_id': setting_id
		})

		return render_to_response('weixin/advance_manage/qrcode_member.html', c)

	@login_required
	@mp_required
	def api_get(request):
		setting_id = int(request.GET['setting_id'])
		start_date = request.GET.get('start_date', '')
		end_date = request.GET.get('end_date', '')
		is_show = request.GET.get('is_show', '0')

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


		channel_members = Member.objects.filter(**filter_data_args).order_by('-created_at')
		count_per_page = int(request.GET.get('count_per_page', 15))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, channel_members = paginator.paginate(channel_members, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		
		return_channel_members_json_array = []
		
		for channel_member in channel_members:
			member_info = MemberInfo.get_member_info(channel_member.id)
			if member_info:
				channel_member.name = member_info.name
			else:
				channel_member.name = ''

			return_channel_members_json_array.append(build_member_basic_json(channel_member))

		response = create_response(200)
		response.data = {
			'items': return_channel_members_json_array,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
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
		'grade_name': member.grade.name,
		"follow_time": member.created_at.strftime('%Y-%m-%d %H:%M:%S'),
		"is_subscribed": member.is_subscribed
	}

def get_order_status_text(status):
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
			'second_navs': export.get_advance_manage_second_navs(request),
			'second_nav_name': export.ADVANCE_MANAGE_QRCODE_NAV,
			'setting_id': setting_id
		})

		return render_to_response('weixin/advance_manage/qrcode_order.html', c)

	@login_required
	@mp_required
	def api_get(request):
		channel_qrcode_id = request.GET.get('setting_id', None)
		start_date = request.GET.get('start_date', '')
		end_date = request.GET.get('end_date', '')
		is_show = request.GET.get('is_show', '0')

		filter_data_args = {}

		if start_date:
			filter_data_args['created_at__gte'] = start_date

		if end_date:
			filter_data_args['created_at__lte'] = end_date

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
				for order in Order.objects.filter(webapp_user_id=webapp_user.id, created_at__gte=created_at):
					old_member_order_ids.append(order.id)
			if new_webapp_user_ids:
				filter_data_args['webapp_user_id__in'] = new_webapp_user_ids
			if old_member_order_ids:
				filter_data_args['id__in'] = old_member_order_ids
			filter_data_args['status'] = ORDER_STATUS_SUCCESSED
			#orders = Order.objects.filter(webapp_user_id__in=new_webapp_user_ids, status=ORDER_STATUS_SUCCESSED, id__in=old_member_order_ids).order_by('-created_at')
		else:
			webapp_users = WebAppUser.objects.filter(member_id__in=member_ids)
			webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
			webapp_user_ids = set(webapp_user_id2member_id.keys())
			if webapp_user_ids:
				filter_data_args['webapp_user_id__in'] = webapp_user_ids
			filter_data_args['status'] = ORDER_STATUS_SUCCESSED
			#orders = Order.objects.filter(webapp_user_id__in=webapp_user_ids, status=ORDER_STATUS_SUCCESSED).order_by('-created_at')
		orders = Order.objects.filter(**filter_data_args).order_by('-created_at')
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
				'payment_time':datetime.strftime(order.created_at,'%Y-%m-%d %H:%M'),
				'product_count': order2productcount.get(order.id, 0),
				'products': mall_api.get_order_products(order),
				'customer_message': order.customer_message,
				'order_status':order.status,
				'express_company_name': order.express_company_name,
				'express_number': order.express_number,
				'leader_name': order.leader_name,
				'remark': order.remark,
				'postage': '%.2f' % order.postage,
				'save_money': float(Order.get_order_has_price_number(order)) + float(order.postage) - float(order.final_price) - float(order.weizoom_card_money),
				'weizoom_card_money': float('%.2f' % order.weizoom_card_money),
				'pay_money': '%.2f' % (order.final_price + order.weizoom_card_money)
			 })

		# for order in orders:
		# 	items.append({
		# 		'id': order.id,
		# 		'order_id': order.order_id,
		# 		'status': order.get_status_text(),
		# 		'total_price': float('%.2f' % order.final_price) if order.pay_interface_type != 9 or order.status == 5 else 0,
		# 		'order_total_price': float('%.2f' % order.get_total_price()),
		# 		'ship_name': order.ship_name,
		# 		'buyer_name': order.buyer_name,
		# 		'pay_interface_name': order.pay_interface_type_text,
		# 		'created_at': datetime.strftime(order.created_at, '%Y-%m-%d %H:%M:%S'),
		# 		'product_count': order.product_count,
		# 		'customer_message': order.customer_message,
		# 		'payment_time': order.payment_time,
		# 		'come': order.come,
		# 		'member_id': order.member_id,
		# 		'type': order.type,
		# 		'webapp_id': order.webapp_id,
		# 		'integral': order.integral,
		# 		'products': mall_api.get_order_products(order),
		# 		'pay_interface_type':order.pay_interface_type,
		# 		'order_status':order.status,
		# 		'express_company_name': order.express_company_name,
		# 		'express_number': order.express_number,
		# 		'leader_name': order.leader_name,
		# 		'remark': order.remark,
		# 		'postage': '%.2f' % order.postage,
		# 		'save_money': float(Order.get_order_has_price_number(order)) + float(order.postage) - float(order.final_price) - float(order.weizoom_card_money),
		# 		'weizoom_card_money': float('%.2f' % order.weizoom_card_money),
		# 		'pay_money': '%.2f' % (order.final_price + order.weizoom_card_money)
		# 	})

		response = create_response(200)
		response.data = {
			'items': items,
			'sortAttr': request.GET.get('sort_attr', '-created_at'),
			'pageinfo': paginator.to_dict(pageinfo),
			'data': {}
		}
		return response.get_response()