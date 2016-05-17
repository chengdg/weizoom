# -*- coding: utf-8 -*-

import json
import random
from datetime import date, datetime
import os
from weapp import settings

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack

import models as app_models
import export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api
from modules.member.models import Member
from mall import export as mall_export
from modules.member import models as member_models
from mall import models as mall_models
from mall import module_api as mall_module_api
from watchdog.utils import watchdog_error

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

class RebateOrderList(resource.Resource):
	app = 'apps/rebate'
	resource = 'rebate_order_list'

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

		return render_to_response('rebate/templates/editor/rebate_order_list.html', c)

	@staticmethod
	def get_datas(request,export_id=0):
		webapp_id = request.user_profile.webapp_id
		record_id = request.GET.get('record_id', 0)
		is_show = int(request.GET.get('is_show', 0))

		records = app_models.Rebate.objects(id=record_id)
		rebate_start_time = records[0].start_time
		rebate_end_time = records[0].end_time

		# member_id2scan_time = {}
		# if is_show:
		# 	rebate_participances = app_models.RebateParticipance.objects(belong_to=record_id)
		# 	member_id2scan_time = {p.member_id: p.created_at for p in rebate_participances}

		webapp_user_id_belong_to_member_id, id2record, member_id2records, member_id2order_ids, all_orders = export.get_target_orders(records, is_show)
		webapp_user_ids = webapp_user_id_belong_to_member_id.keys()

		params = {'webapp_user_id__in': webapp_user_ids}
		start_date = request.GET.get('start_date', '')
		end_date = request.GET.get('end_date', '')
		start_money = request.GET.get('start_money', 0)
		end_money = request.GET.get('end_money', 0)
		is_first_order = int(request.GET.get('is_first_order', 0))
		not_first_order = int(request.GET.get('not_first_order', 0))

		if is_show:
			all_orders = all_orders.filter(created_at__gte=rebate_start_time, created_at__lte=rebate_end_time)
		else:
			all_orders = all_orders.filter(created_at__lte=rebate_end_time)

		if start_date:
			params['created_at__gte'] = start_date
		if end_date:
			params['created_at__lte'] = end_date
		if start_money:
			params['final_price__gte'] = start_money
		if end_money:
			params['final_price__lte'] = end_money
		if not (is_first_order and not_first_order):
			if is_first_order:
				params['is_first_order'] = 1
			if not_first_order:
				params['is_first_order'] = 0

		orders = all_orders.filter(**params)
		#统计微众卡支付总金额和现金支付总金额(退款成功不算)
		final_price = 0
		weizoom_card_money = 0
		for order in orders.exclude(status=mall_models.ORDER_STATUS_REFUNDED):
			final_price += order.final_price
			weizoom_card_money += order.weizoom_card_money

		# 进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))

		if not export_id:
			pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page,query_string=request.META['QUERY_STRING'])

		# 获取order对应的会员
		webapp_user_ids = set([order.webapp_user_id for order in orders])
		webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

		# 获得order对应的商品数量
		order_ids = [order.id for order in orders]
		order2productcount = {}
		for relation in mall_models.OrderHasProduct.objects.filter(order_id__in=order_ids):
			order_id = relation.order_id
			if order_id in order2productcount:
				order2productcount[order_id] = order2productcount[order_id] + 1
			else:
				order2productcount[order_id] = 1

		items = []

		for order in orders:
			# 获取order对应的member的显示名
			member = webappuser2member.get(order.webapp_user_id, None)
			if member:
				# if is_show:
				# 	member_id = member.id
				# 	scan_time = member_id2scan_time.get(member_id, None)
				# 	if scan_time and scan_time > order.created_at:
				# 		continue
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
				'pay_interface_name': mall_models.PAYTYPE2NAME.get(order.pay_interface_type, u''),
				'created_at': datetime.strftime(order.created_at, '%Y-%m-%d %H:%M'),
				'payment_time': datetime.strftime(order.payment_time, '%Y-%m-%d %H:%M'),
				'product_count': order2productcount.get(order.id, 0),
				'products': mall_module_api.get_order_products(order),
				'customer_message': order.customer_message,
				'order_status': order.status,
				'express_company_name': order.express_company_name,
				'express_number': order.express_number,
				'leader_name': order.leader_name,
				'remark': order.remark,
				'postage': '%.2f' % order.postage,
				'save_money': '%.2f' % (float(mall_models.Order.get_order_has_price_number(order)) + float(order.postage) - float(order.final_price) - float(order.weizoom_card_money)),
				'weizoom_card_money': float('%.2f' % order.weizoom_card_money),
				'pay_money': '%.2f' % order.final_price,
				'is_first_order': order.is_first_order
			})
		if not export_id:
			return pageinfo, items, final_price, weizoom_card_money
		else:
			return items

	@login_required
	def api_get(request):
		"""
		响应GET api
		"""
		pageinfo, items, final_price, weizoom_card_money = RebateOrderList.get_datas(request)
		response_data = {
			'items': items,
			'final_price': '%.2f' % final_price,
			'weizoom_card_money': '%.2f' % weizoom_card_money,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': request.GET.get('sort_attr', '-created_at'),
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()

class RebateOrder_Export(resource.Resource):
	'''
	批量导出
	'''
	app = 'apps/rebate'
	resource = 'rebate_order_export'

	@login_required
	def api_get(request):
		"""
		分析导出
		"""
		export_id = request.GET.get('export_id', 0)
		download_excel_file_name = u'返利活动订单.xls'
		excel_file_name = 'rebate_order_' + datetime.now().strftime('%H_%M_%S') + '.xls'
		dir_path_suffix = '%d_%s' % (request.user.id, date.today())
		dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		export_file_path = os.path.join(dir_path, excel_file_name)
		# Excel Process Part
		try:
			import xlwt
			datas = RebateOrderList.get_datas(request, export_id)
			fields_pure = []
			export_data = []

			# from sample to get fields4excel_file
			fields_pure.append(u'订单号')
			fields_pure.append(u'下单时间')
			fields_pure.append(u'付款时间')
			fields_pure.append(u'商品名称')
			fields_pure.append(u'商品单价')
			fields_pure.append(u'商品数量')
			fields_pure.append(u'支付方式')
			fields_pure.append(u'支付金额')
			fields_pure.append(u'现金支付金额')
			fields_pure.append(u'微众卡支付金额')
			fields_pure.append(u'订单状态')
			fields_pure.append(u'购买人')
			fields_pure.append(u'是否首单')
			# fields_pure.append(u'采购价')
			# fields_pure.append(u'采购成本')

			# processing data
			num = 0
			for data in datas:
				export_record = []
				order_id = data["order_id"]
				created_at = data["created_at"]
				payment_time = data["payment_time"]
				products = data["products"]
				pay_interface_name = data["pay_interface_name"]
				pay_money = data["pay_money"]
				# final_price = data["final_price"]
				weizoom_card_money = data["weizoom_card_money"]
				status = data["status"]
				buyer_name = data["buyer_name"]
				is_first_order = u'是' if data["is_first_order"] else u'否'
				# purchase_price = data["purchase_price"] #采购价
				# purchase_cost = data["purchase_cost"] #采购成本

				export_record.append(order_id)
				export_record.append(created_at)
				export_record.append(payment_time)
				export_record.append(products)
				export_record.append(products)
				export_record.append(products)
				export_record.append(pay_interface_name)
				export_record.append(pay_money)
				export_record.append(pay_money)
				export_record.append(weizoom_card_money)
				export_record.append(status)
				export_record.append(buyer_name)
				export_record.append(is_first_order)
				# export_record.append(purchase_price)
				# export_record.append(purchase_cost)

				export_data.append(export_record)
			# workbook/sheet
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet('id%s' % export_id)
			header_style = xlwt.XFStyle()

			##write fields
			row = col = 0
			for h in fields_pure:
				ws.write(row, col, h)
				col += 1
			##write data
			if export_data:
				row = 1
				lens = len(export_data[0])
				for record in export_data:
					row_l = []
					for col in range(lens):
						record_col = record[col]
						if type(record_col) == list:
							row_l.append(len(record_col))
							for n in range(len(record_col)):
								data = record_col[n]
								try:
									ws.write(row + n, col, data['name'])
									ws.write(row + n, col + 1, data['price'])
									ws.write(row + n, col + 2, data['count'])
								except:
									# '编码问题，不予导出'
									# print record
									pass
						else:
							try:
								ws.write(row, col, record[col])
							except:
								# '编码问题，不予导出'
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
					print '/static/upload/%s/%s' % (dir_path_suffix, excel_file_name)
			else:
				ws.write(1, 0, '')
				wb.save(export_file_path)
			response = create_response(200)
			response.data = {'download_path': '/static/upload/%s/%s' % (dir_path_suffix, excel_file_name),
							 'filename': download_excel_file_name, 'code': 200}
		except Exception, e:
			error_msg = u"导出文件失败, cause:\n{}".format(unicode_full_stack())
			watchdog_error(error_msg)
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()

		return response.get_response()

def get_order_status_text(status):
	from mall.models import STATUS2TEXT
	return STATUS2TEXT[status]
