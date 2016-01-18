# -*- coding: utf-8 -*-

import json
from core import dateutil
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from stats import export
from core import resource
from core import paginator
from core.jsonresponse import create_response
from mall.models import *
from excel_response import ExcelResponse
from tools.regional.views import get_str_value_by_string_ids, get_str_value_by_string_ids_new
from market_tools.tools.channel_qrcode.models import ChannelQrcodeHasMember
from modules.member.models import Member, WebAppUser, MemberFollowRelation, SOURCE_SELF_SUB, SOURCE_MEMBER_QRCODE, SOURCE_BY_URL
from mall import module_api as mall_api
import re

COUNT_PER_PAGE = 15
FIRST_NAV = export.STATS_HOME_FIRST_NAV

########################################################################
# export_orders:  导出订单列表
########################################################################


class OrderExport(resource.Resource):
	"""
	导出订单
	"""
	app = 'stats'
	resource = 'order_export'

	@login_required
	def get(request):
		"""
		导出订单列表
		"""
		params = _extract_params(request)
		orders = _get_stats_data(request.manager, params, True)
		data = _export_orders_json(request, orders, params)
		return ExcelResponse(data,output_name=u'订单列表'.encode('utf8'),force_csv=False)

def _export_orders_json(request, order_list, params):
	# debug
	# pre_page = 500
	# test_index = 0
	# begin_time = time.time()
	status = {
		'0':u'待支付',
		'1':u'已取消',
		'2':u'已支付',
		'3':u'待发货',
		'4':u'已发货',
		'5':u'已完成',
		'6':u'退款中',
		'7':u'退款完成',
	}

	payment_type = {
		'-1': u'',
		'0': u'支付宝',
		'2': u'微信支付',
		'3': u'微众卡支付',
		'9': u'货到付款',
		'10': u'优惠抵扣'
	}

	member_source = {
		'0': u'直接关注',
		'1': u'推广扫码',
		'2': u'会员分享'
	}

	# type = ORDER_TYPE2TEXT

	source_list = {
		'mine_mall': u'本店',
		'weizoom_mall': u'商户'
	}

	orders = [
		[u'订单号', u'下单时间',u'付款时间', u'商品名称', u'规格',
		u'商品单价', u'商品数量', u'支付方式', u'支付金额',u'现金支付金额',u'微众卡支付金额',
		u'运费', u'积分抵扣金额', u'优惠券金额',u'优惠券名称', u'订单状态', u'购买人',
		u'收货人', u'联系电话', u'收货地址省份', u'收货地址', u'发货人', u'备注', u'来源', u'物流公司', u'快递单号', u'发货时间',
		u'买家来源', u'买家推荐人']
	]

	webapp_id = request.user_profile.webapp_id

	# 订单总量
	order_count = len(order_list)
	finished_order_count = 0
	for order in order_list:
		if order.type != PRODUCT_INTEGRAL_TYPE and order.status == ORDER_STATUS_SUCCESSED:
			finished_order_count += 1

	#商品总额：
	total_product_money = 0.0
	# 订单金额
	# total_order_money = 0.0
	# 支付金额
	final_total_order_money = 0.0
	# 微众卡支付金额
	weizoom_card_total_order_money = 0.0
	# 积分总和
	# use_integral_count = 0
	# 积分抵扣总金额
	use_integral_money = 0.0
	#赠品总数
	total_premium_product = 0
	# 优惠劵价值总和
	coupon_money_count = 0
	# 直降总金额
	# save_money_count = 0
	#
	#####################################

	# print 'begin step 1 order_list - '+str(time.time() - begin_time)
	# order_list = list(order_list.all())
	order_ids = []
	order_order_ids = []
	coupon_ids = []
	for o in order_list:
		order_ids.append(o.id)
		order_order_ids.append(o.order_id)
		if o.coupon_id:
			coupon_ids.append(o.coupon_id)

	# print 'begin step 2 relations - '+str(time.time() - begin_time)
	relations = {}
	product_ids = []
	promotion_ids = []
	model_value_ids = []
	# print 'begin step 2.5 order_list - '+str(time.time() - begin_time)
	# product_ids =
	for relation in OrderHasProduct.objects.filter(order__id__in=order_ids):
		# if test_index % pre_page == pre_page - 1:
		# 	print str(test_index) + 's-' +str(time.time() - begin_time)
		# 	print relation.order_id
		# test_index+=1
		key = relation.order_id
		promotion_ids.append(relation.promotion_id)
		if relations.get(key):
			relations[key].append(relation)
		else:
			relations[key] = [relation]
		if product_ids.count(relation.product_id) == 0:
			product_ids.append(relation.product_id)
		if relation.product_model_name != 'standard':
			for mod in relation.product_model_name.split('_'):
				i = mod.find(':') + 1
				if i > 0 and re.match('',mod[i:]) and model_value_ids.count(mod[i:]) == 0:
					model_value_ids.append(mod[i:])



	# print 'begin step 3 products - '+str(time.time() - begin_time)
	id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])

	# print 'begin step 4 coupons - '+str(time.time() - begin_time)
	coupon2role = {}
	role_ids = []
	from mall.promotion.models import Coupon,CouponRule
	for coupon in Coupon.objects.filter(id__in=coupon_ids):
		coupon2role[coupon.id] = coupon.coupon_rule_id
		if role_ids.count(coupon.coupon_rule_id) == 0:
			role_ids.append(coupon.coupon_rule_id)
	role_id2role = dict([(role.id, role) for role in CouponRule.objects.filter(id__in=role_ids)])

	# print 'begin step 5 models - '+str(time.time() - begin_time)
	id2modelname = dict([(str(value.id), value.name) for value in ProductModelPropertyValue.objects.filter(id__in = model_value_ids)])
	# print 'end step 6 coupons - '+str(time.time() - begin_time)

	#获取order对应的会员
	webapp_user_ids = set([order.webapp_user_id for order in order_list])
	# from modules.member.models import Member
	webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

	#++++++++++++++++++++++++++++++members++++++++++++++++++++++++++++++
	members = webappuser2member.values()
	member_self_sub, member_qrcode_and_by_url = [], []
	follow_member_ids = []
	for member in members:
		if member.source == SOURCE_SELF_SUB:
			member_self_sub.append(member)
		elif member.source in [SOURCE_MEMBER_QRCODE, SOURCE_BY_URL]:
			member_qrcode_and_by_url.append(member)
			follow_member_ids.append(member.id)

	follow_member2father_member = dict([(relation.follower_member_id, relation.member_id) for relation in MemberFollowRelation.objects.filter(follower_member_id__in=follow_member_ids, is_fans=True)])
	father_member_ids = follow_member2father_member.values()
	father_member_id2member = dict([(m.id, m) for m in Member.objects.filter(id__in=father_member_ids)])

	member_id2qrcode = dict([(relation.member_id, relation) for relation in ChannelQrcodeHasMember.objects.filter(member_id__in=member_self_sub)])


	# print 'end step 6.7 - '+str(time.time() - begin_time)
	#获取order对应的赠品
	order2premium_product = {}
	order2promotion = dict([(order_promotion_relation.order_id, order_promotion_relation.promotion_result)for order_promotion_relation in OrderHasPromotion.objects.filter(order_id__in=order_ids, promotion_id__in=promotion_ids, promotion_type='premium_sale')])
	for order_id in order2promotion:
		temp_premium_products = []
		if order2promotion[order_id].has_key('premium_products'):
			for premium_product in order2promotion[order_id]['premium_products']:
				temp_premium_products.append({
					'name' : premium_product['name'],
					'count' : premium_product['count'],
					'price' : premium_product['price']
				})
		order2premium_product[order_id] = temp_premium_products


	#获取order对应的发货时间
	order2postage_time = dict([(log.order_id, log.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8')) for log in OrderOperationLog.objects.filter(order_id__in=order_order_ids, action="订单发货")])

	# print 'end step 8 order - '+str(time.time() - begin_time)
	#获取order对应的收货地区
	#area = get_str_value_by_string_ids(order.area)
	for order in order_list:
		# if test_index % pre_page == 0:
		# 	test_begin_time = time.time()
		# test_index+=1

		#获取order对应的member的显示名
		member = webappuser2member.get(order.webapp_user_id, None)
		if member:
			try:
				order.buyer_name = member.username_for_html
			except:
				# 回避名字解析异常
				order.buyer_name = u'未能解析的名字'
			order.member_id = member.id
		else:
			order.buyer_name = u'未知'

		#获取推荐人的姓名或者带参数二维码的名称
		father_name_or_qrcode_name = ""
		member_source_name = ""
		before_scanner_qrcode_is_member = "是"
		SOURCE_SELF_SUB, SOURCE_MEMBER_QRCODE, SOURCE_BY_URL
		if member.source == SOURCE_SELF_SUB:
			if member.id in member_id2qrcode.keys() and member_id2qrcode[member.id].created_at > order.created_at:
				member_source_name = "带参数二维码"
				father_name_or_qrcode_name = member_id2qrcode[member.id].channel_qrcode.name
				if member_id2qrcode[member.id].is_new:
					before_scanner_qrcode_is_member = "否"
			else:
				member_source_name = "直接关注"
		elif member.source == SOURCE_MEMBER_QRCODE:
			member_source_name = "推广扫码"
			father_name_or_qrcode_name = father_member_id2member[follow_member2father_member[member.id]].username_for_html
		elif member.source == SOURCE_BY_URL:
			member_source_name = "会员分享"
			father_name_or_qrcode_name = father_member_id2member[follow_member2father_member[member.id]].username_for_html
		else:
			pass

		# 计算总和
		final_price = 0.0
		weizoom_card_money = 0.0
		# total_price = order.get_total_price()
		# use_integral = order.get_use_integral(webapp_id)
		if order.type == PAY_INTERFACE_COD:
			if order.status == ORDER_STATUS_SUCCESSED:
				final_price = order.final_price
				weizoom_card_money = order.weizoom_card_money
				final_total_order_money += order.final_price
				try:
					coupon_money_count += order.coupon_money
					weizoom_card_total_order_money += order.weizoom_card_money
					use_integral_money += order.integral_money
				except:
					pass
		else:
			if order.status in [2,3,4,5]:
				final_price = order.final_price
				weizoom_card_money = order.weizoom_card_money
				final_total_order_money += order.final_price
				try:
					coupon_money_count += order.coupon_money
					weizoom_card_total_order_money += order.weizoom_card_money
					use_integral_money += order.integral_money
				except:
					pass

		area = get_str_value_by_string_ids_new(order.area)
		if area:
			addr = '%s %s' % (area, order.ship_address)
		else:
			addr = '%s' % (order.ship_address)
		# pay_type = PAYTYPE2NAME.get(order.pay_interface_type, '')

		if order.order_source:
			order.come = 'weizoom_mall'
		else:
			order.come = 'mine_mall'

		source = source_list.get(order.come, u'本店')
		if webapp_id != order.webapp_id:
			if request.manager.is_weizoom_mall:
				source = request.manager.username
			else:
				source = u'微众商城'

		orderRelations = relations.get(order.id,[])
		product_ids = [r.product_id for r in orderRelations]

		i = 0
		for relation in orderRelations:
			product = id2product[relation.product_id]
			model_value = ''
			for mod in relation.product_model_name.split('_'):
				mod_i = mod.find(':') + 1
				if mod_i > 0:
					model_value += '-' + id2modelname.get(mod[mod_i:], '')
				else:
					model_value = '-'
			# models_name = ''
			coupon_name = ''
			coupon_money = ''
			# promotion_name = ''
			promotion_type = ''
			#订单发货时间
			postage_time = order2postage_time.get(order.order_id, '')
			#付款时间
			if order.status > ORDER_STATUS_CANCEL and order.payment_time:
				payment_time = order.payment_time.strftime('%Y-%m-%d %H:%M').encode('utf8')
			else:
				payment_time = ''
			total_product_money += relation.price * relation.number
			#save_money_count += relation.total_price - relation.price * relation.number

			# if relation.promotion_id:
			# 	promotion_name = Promotion.objects.get(id=relation.promotion_id).name
			# 	promotion_type = Promotion.objects.get(id=relation.promotion_id).type
			if order.coupon_id:
				role_id = coupon2role.get(order.coupon_id,None)
				if role_id:
					if role_id2role[role_id].limit_product:
						if role_id2role[role_id].limit_product_id == relation.product_id:
							coupon_name = role_id2role[role_id].name+"（单品券）"
					elif i == 0:
						coupon_name = role_id2role[role_id].name+"（通用券）"


			if i == 0:
				if promotion_type == 1 and "(限时抢购)" not in product.name:
					product.name = u"(限时抢购)" + product.name

				if coupon_name:
					coupon_money = order.coupon_money

				# type_name = type.get(order.type,'')

				if area:
					province = area.split(' ')[0]
				else:
					province = u''

				temp_leader_names = order.leader_name.split('|')
				remark = ''
				j = 1
				while j < len(temp_leader_names):
					remark += temp_leader_names[j]
					j += 1
				order.leader_name = temp_leader_names[0]
				save_money = str(order.edit_money).replace('.','').replace('-','') if order.edit_money else False
				orders.append([
					'%s%s'.encode('utf8') % (order.order_id, '-%s' % save_money if save_money else ''),
					order.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8'),
					payment_time,
					product.name.encode('utf8'),
					model_value[1:].encode('utf8'),
					relation.price,
					relation.number,
					payment_type[str(int(order.pay_interface_type))],
					final_price + weizoom_card_money,
					final_price,
					weizoom_card_money,
					order.postage,
					order.integral_money,
					coupon_money,
					coupon_name,
					status[str(order.status)].encode('utf8'),
					order.buyer_name.encode('utf8'),
					order.ship_name.encode('utf8'),
					order.ship_tel.encode('utf8'),
					province.encode('utf8'),
					addr.encode('utf8'),
					order.leader_name.encode('utf8'),
					remark.encode('utf8'),
					source.encode('utf8'),
					express_util.get_name_by_value(order.express_company_name).encode('utf8'),
					order.express_number.encode('utf8'),
					postage_time,
					member_source_name,
					father_name_or_qrcode_name,
					before_scanner_qrcode_is_member
				])
			else:
				if coupon_name:
					coupon_money = order.coupon_money
				orders.append([
				'%s%s'.encode('utf8') % (order.order_id, '-%s' % save_money if save_money else ''),
				order.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8'),
				payment_time,
				product.name,
				model_value[1:],
				relation.price,
				relation.number,
				payment_type[str(int(order.pay_interface_type))],
					u'',
					u'',
					u'',
					u'',
					u'',
				coupon_money,
				coupon_name,
				status[str(order.status)].encode('utf8'),
				order.buyer_name.encode('utf8'),
				order.ship_name.encode('utf8'),
				order.ship_tel.encode('utf8'),
				province.encode('utf8'),
				addr.encode('utf8'),
				order.leader_name.encode('utf8'),
				remark.encode('utf8'),
				source.encode('utf8'),
				express_util.get_name_by_value(order.express_company_name).encode('utf8'),
				order.express_number.encode('utf8'),
				postage_time,
				member_source_name,
				father_name_or_qrcode_name,
				before_scanner_qrcode_is_member
				])
			i = i +  1
			if order.id in order2premium_product:
				total_premium_product += len(order2premium_product[order.id])
				for premium_product in order2premium_product[order.id]:
					orders.append([
					'%s%s'.encode('utf8') % (order.order_id, '-%s' % save_money if save_money else ''),
					order.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8'),
					payment_time,
					u'(赠品)'+premium_product['name'],
						u'',
					premium_product['price'],
					premium_product['count'],
					payment_type[str(int(order.pay_interface_type))],
						u'',
						u'',
						u'',
						u'',
						u'',
						u'',
						u'',
					status[str(order.status)].encode('utf8'),
					order.buyer_name.encode('utf8'),
					order.ship_name.encode('utf8'),
					order.ship_tel.encode('utf8'),
					province.encode('utf8'),
					addr.encode('utf8'),
					order.leader_name.encode('utf8'),
					remark.encode('utf8'),
					source.encode('utf8'),
					express_util.get_name_by_value(order.express_company_name).encode('utf8'),
					order.express_number.encode('utf8'),
					postage_time,
					member_source_name,
					father_name_or_qrcode_name,
					before_scanner_qrcode_is_member
					])
				temp_premium_products = []
		# if test_index % pre_page == pre_page-1:
		# 	print str(test_index)+' - '+str(time.time() - test_begin_time)+'-'+str(time.time() - begin_time)
	orders.append([
		u'总计',
		u'订单量:'+str(order_count).encode('utf8'),
		u'已完成:'+str(finished_order_count).encode('utf8'),
		u'商品金额:' + str(total_product_money).encode('utf8'),
		u'支付总额:'+str(final_total_order_money + weizoom_card_total_order_money).encode('utf8'),
		u'现金支付金额:'+str(final_total_order_money).encode('utf8'),
		u'微众卡支付金额:'+str(weizoom_card_total_order_money).encode('utf8'),
		u'赠品总数:'+str(total_premium_product).encode('utf8'),
		u'积分抵扣总金额:'+str(use_integral_money).encode('utf8'),
		u'优惠劵价值总额:'+str(coupon_money_count).encode('utf8'),
		#u'直降金额总额:'+str(save_money_count).encode('utf8'),
	])
	# print 'end - '+str(time.time() - begin_time)

	return orders

class OrderList(resource.Resource):
	"""
	订单明细
	"""
	app = 'stats'
	resource = 'order_list'

	#@mp_required
	@login_required
	def get(request):
		"""
		显示订单明细
		"""
		params = _extract_url_params(request)

		jsons = [{
			"name": "params",
			"content": params
		}]

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'app_name': 'stats',
			'second_navs': export.get_stats_second_navs(request),
			'second_nav_name': export.STATS_SALES_SECOND_NAV,
			'third_nav_name': export.SALES_ORDER_LIST_NAV,
			'jsons': jsons
		})

		return render_to_response('sales/order_list.html', c)

	@login_required
	def api_get(request):
		"""
		显示订单明细列表
		"""
		params = _extract_params(request)
		# print params

		if params:
			response = create_response(200)
			response.data = _get_stats_data(request.manager, params, False)
			# print response.data
			return response.get_response()
		else:
			response = create_response(500)
			response.errMsg = u'未指定查询时间段'
			return response.get_response()

def _extract_url_params(request):
	params = dict()

	start_time = request.GET.get('start_time', '')
	end_time = request.GET.get('end_time', '')
	if start_time and end_time:
		params['start_time'] = start_time
		params['end_time'] = end_time
	else:
		#默认显示最近7天的日期
		end_date = dateutil.get_today()
		start_date = dateutil.get_previous_date(end_date, 6) #获取7天前日期
		params['start_time'] = start_date + ' 00:00:00'
		params['end_time'] = end_date + ' 23:59:59'

	status_str = request.GET.get('order_status', '')
	if status_str:
		params['order_status'] = status_str

	params['repeat_buy'] = int(request.GET.get('repeat_buy', '-1'))
	params['buyer_source'] = int(request.GET.get('buyer_source', '-1'))

	discount_type = request.GET.get('discount_type', '')
	if discount_type:
		params['discount_type'] = discount_type

	return params

def _get_stats_data(user, params, is_export):
	webapp_id = user.get_profile().webapp_id
	total_orders =  belong_to(webapp_id)
	# time_qualified_orders = total_orders.filter(created_at__gte=params['start_time'], created_at__lt=params['end_time'])
	status_qualified_orders = total_orders.filter(status__in=[ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED])
	pre_status_qualified_orders = status_qualified_orders.filter(created_at__lt=params['start_time'])
	past_status_qualified_orders = status_qualified_orders.filter(created_at__lt=params['end_time'])
	webapp_user_ids = set([order.webapp_user_id for order in past_status_qualified_orders])
	webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

	# 生成查询对象
	# print params
	q_obj = _create_q(params)
	# print q_obj

	# 提前获取所需内容
	if params['repeat_buy'] == -1 or params['sort_attr'] == 'id':
		qualified_orders = total_orders.prefetch_related('orderhasproduct_set__product').filter(q_obj).order_by(params['sort_attr'])
	else:
		qualified_orders = total_orders.prefetch_related('orderhasproduct_set__product').filter(q_obj)

	wuid_dict = { 'pos': 0 }
	items = []
	# print 'qualified order num=', qualified_orders.count()
	for order in qualified_orders:
		tmp_member = webappuser2member.get(order.webapp_user_id, None)
		if not _check_buyer_source(params['buyer_source'], tmp_member):
			continue

		checked = __check_repeat_buy(params['repeat_buy'], order.webapp_user_id, wuid_dict, tmp_member, webappuser2member, pre_status_qualified_orders)
		if not checked:
			continue

		# clock_t_3 = time.clock()
		# wall_t_3  = time.time()
		save_money = float(_get_total_price(order)) + float(order.postage) - float(order.final_price) - float(order.weizoom_card_money)
		# __report_performance(clock_t_3, wall_t_3, '*****doubt***** part')
		# clock_t_3 = time.clock()
		# wall_t_3  = time.time()
		if is_export:
			items.append(order)
		else:
			member_id = -1
			buyer_name = u'未知'
			if tmp_member:
				member_id = tmp_member.id
				try:
					buyer_name = tmp_member.username_for_html
				except:
					buyer_name = u'未能解析的名字'
			items.append({
				'id': order.id,
				'products': _get_products(order),
				'order_id': order.order_id,
				'save_money': '%.2f' % save_money,
				'postage': '%.2f' % order.postage,
				'pay_money': '%.2f' % (order.final_price + order.weizoom_card_money),
				'pay_interface_type':order.get_pay_interface_name,
				'buyer_name': buyer_name,
				'member_id': member_id,
				'created_at': datetime.strftime(order.created_at, '%Y/%m/%d %H:%M:%S'),
				'order_status': order.get_status_text()
			})
		# __report_performance(clock_t_3, wall_t_3, 'doubt part')

	if params['repeat_buy'] != -1 and params['sort_attr'] == '-id':
		items.reverse()

	if is_export:
		return items

	return_count = len(items)
	if params['count_per_page'] > 0:
		#进行分页
		pageinfo, items = paginator.paginate(items, params['cur_page'], params['count_per_page'], params['query_string'])
	else:
		#全部订单
		pageinfo = {"object_count": return_count}

	if params.get('sort_attr') == 'id':
		params['sort_attr'] = 'created_at'
	if params.get('sort_attr') == '-id':
		params['sort_attr'] = '-created_at'

	total_count = status_qualified_orders.count()
	if total_count > 0:
		percent = "%.2f%%" % float(float(return_count) / float(total_count) * 100)
	else:
		percent = '0.00%'

	data = {
		'items': items,
		'pageinfo': paginator.to_dict(pageinfo),
		'sortAttr': params['sort_attr'],
		'total_count': total_count,
		'return_count': return_count,
		'percent': percent
	}

	return data

def _get_total_price(order):
	result = 0.0
	for r in order.orderhasproduct_set.all():
		result += r.total_price

	return result

def _get_products(order):
	result = []

	for r in order.orderhasproduct_set.all():
		tmp = {}
		tmp['name'] = r.product.name
		tmp['thumbnails_url'] = r.product.thumbnails_url
		result.append(tmp)

	return result

def __report_performance(clock_t, wall_t, title):
	clock_x = time.clock() - clock_t
	wall_x = time.time() - wall_t
	clock_msg = "seconds process time for " + title
	wall_msg = "seconds wall time for " + title
	print clock_x, clock_msg
	print wall_x, wall_msg
	print "=========================================="


def __check_repeat_buy(repeat_buy, wuid, wuid_dict, member, webappuser2member, pre_status_qualified_orders):
	if repeat_buy == -1:
		return True

	want_repeat = (repeat_buy == 2)

	if wuid_dict.has_key(wuid):
		return want_repeat

	wuid_dict[wuid] = ""

	if pre_status_qualified_orders:
		for index in range(wuid_dict['pos'], len(pre_status_qualified_orders)):
			tmp_wuid = pre_status_qualified_orders[index].webapp_user_id
			if wuid == tmp_wuid:
				wuid_dict['pos'] = index + 1
				return want_repeat

			wuid_dict[tmp_wuid] = ""
			tmp_member = webappuser2member.get(tmp_wuid, None)
			if member and tmp_member:
				if tmp_member.id == member.id:
					wuid_dict['pos'] = index + 1
					return want_repeat

	return not want_repeat

def _check_buyer_source(buyer_source, member):
	if buyer_source == -1:
		return True

	if member:
		if member.source in [SOURCE_SELF_SUB, SOURCE_MEMBER_QRCODE, SOURCE_BY_URL]:
			return buyer_source == member.source
		else:
			return buyer_source == 3
	else:
		return buyer_source == 3

def _create_q(params):
	q_obj = Q(created_at__gte=params['start_time']) & Q(created_at__lt=params['end_time'])
	q_obj = q_obj & Q(status__in=params['status'])
	if params.get('product_name'):
		q_obj = q_obj & Q(orderhasproduct__product__name__icontains=params['product_name'])
	if params.get('order_id'):
		q_obj = q_obj & Q(order_id=params['order_id'])
	if params.get('pay_interface_type') != None:
		q_obj = q_obj & Q(pay_interface_type=params['pay_interface_type'])

	q_list = []
	if params.get('iswzcard_pay') == 1:
		tmp = Q(weizoom_card_money__gt=0.0) & Q(coupon_money=0.0) & Q(integral_money=0.0)
		q_list.append(tmp)
	if params.get('isfavorable_coupon') == 1:
		tmp = Q(weizoom_card_money=0.0) & Q(coupon_money__gt=0.0) & Q(integral_money=0.0)
		q_list.append(tmp)
	if params.get('isintegral_deduction') == 1:
		tmp = Q(weizoom_card_money=0.0) & Q(coupon_money=0.0) & Q(integral_money__gt=0.0)
		q_list.append(tmp)
	if params.get('iswzcard_integral') == 1:
		tmp = Q(weizoom_card_money__gt=0.0) & Q(coupon_money=0.0) & Q(integral_money__gt=0.0)
		q_list.append(tmp)
	if params.get('iswzcard_discountcoupon') == 1:
		tmp = Q(weizoom_card_money__gt=0.0) & Q(coupon_money__gt=0.0) & Q(integral_money=0.0)
		q_list.append(tmp)

	list_len = len(q_list)
	if list_len > 0:
		tmp = q_list[0]
		for index in range(1, list_len):
			tmp = tmp | q_list[index]
		q_obj = q_obj & tmp

	return q_obj

def _formalize_date_str(is_start, date_str):
	num = date_str.count(":")

	if num == 2:
		return date_str

	if num == 0:
		if is_start:
			date_str += ' 00:00:00'
		else:
			date_str += ' 23:59:59'
	elif num == 1:
		date_str += ":00"

	return date_str

def _extract_params(request):
	params = dict()

	# 处理起止时间参数
	date_interval = request.GET.get('date_interval', '')
	if date_interval:
		date_interval = date_interval.split('|')
		params['start_time'] = _formalize_date_str(True, date_interval[0])
		params['end_time'] = _formalize_date_str(False, date_interval[1])
	else:
		date_now = datetime.strftime(datetime.now(), '%Y-%m-%d')
		params['start_time'] = date_now + ' 00:00:00'
		params['end_time'] = date_now + ' 23:59:59'

	params['cur_page'] = int(request.GET.get('page', '1'))
	params['count_per_page'] = int(request.GET.get('count_per_page', 20))
	params['query_string'] = request.META['QUERY_STRING']

	tmp = request.GET.get('sort_attr', '-id')
	if tmp == 'created_at':
		tmp = 'id'
	if tmp == '-created_at':
		tmp = '-id'
	params['sort_attr'] = tmp

	query = request.GET.get('query', '').strip()
	if len(query):
		params['order_id'] = query.strip().split('-')[0]

	params['product_name'] = request.GET.get('product_name', '').strip()
	pay_type = int(request.GET.get('pay_type', '-1').strip())
	if pay_type == 1:
		params['pay_interface_type'] = PAY_INTERFACE_ALIPAY
	elif pay_type == 2:
		params['pay_interface_type'] = PAY_INTERFACE_WEIXIN_PAY
	elif pay_type == 3:
		params['pay_interface_type'] = PAY_INTERFACE_COD

	params['buyer_source'] = int(request.GET.get('buyer_source', '-1').strip())
	params['repeat_buy'] = int(request.GET.get('repeat_buy', '-1').strip())

	status_list = []
	iswait_send = int(request.GET.get('iswait_send', '0').strip())
	isalready_send = int(request.GET.get('isalready_send', '0').strip())
	isalready_complete = int(request.GET.get('isalready_complete', '0').strip())
	if iswait_send == 1:
		status_list.append(ORDER_STATUS_PAYED_NOT_SHIP)
	if isalready_send == 1:
		status_list.append(ORDER_STATUS_PAYED_SHIPED)
	if isalready_complete == 1:
		status_list.append(ORDER_STATUS_SUCCESSED)

	params['status'] = status_list

	params['iswzcard_pay'] = int(request.GET.get('iswzcard_pay', '0').strip())
	params['isintegral_deduction'] = int(request.GET.get('isintegral_deduction', '0').strip())
	params['isfavorable_coupon'] = int(request.GET.get('isfavorable_coupon', '0').strip())
	params['iswzcard_integral'] = int(request.GET.get('iswzcard_integral', '0').strip())
	params['iswzcard_discountcoupon'] = int(request.GET.get('iswzcard_discountcoupon', '0').strip())

	return params