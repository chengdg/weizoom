#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy

from excel_response import ExcelResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from core import resource
from mall import export
import util
from core.jsonresponse import create_response
from core import paginator
from mall.models import *
from market_tools.tools.channel_qrcode.models import ChannelQrcodeHasMember
import mall.module_api as mall_api
from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning
from core.exceptionutil import unicode_full_stack
from modules.member.models import WebAppUser

COUNT_PER_PAGE = 20
FIRST_NAV = export.ORDER_FIRST_NAV


class OrderInfo(resource.Resource):
    """
    单个订单资源
    """
    app = 'mall2'
    resource = 'order'

    @login_required
    def get(request):
        """
        订单详情页
        """

        return util.get_detail_response(request)


    @login_required
    def api_post(request):
        """
        更新订单状态 取消订单
        """
        mall_type = request.user_profile.webapp_type
        order_id = request.POST['order_id']
        action = request.POST.get('action', None)
        order_status = request.POST.get('order_status', None)
        bill_type = int(request.POST.get('bill_type', ORDER_BILL_TYPE_NONE))
        # postage = request.POST.get('postage', None)
        ship_name = request.POST.get('ship_name', None)
        ship_tel = request.POST.get('ship_tel', None)
        ship_address = request.POST.get('ship_address', None)
        remark = request.POST.get('remark', None)
        # 待支付状态下 修改价格  最终价格
        final_price = request.POST.get('final_price', None)
        order = Order.objects.get(id=order_id)
        if action:
            # 检查order的状态是否可以跳转，如果是非法跳转则报错
            if mall_type and Order.objects.filter(origin_order_id=order.origin_order_id).count() == 1:
                order = Order.objects.get(id=order.origin_order_id)
            flag = util.check_order_status_filter(order,action,mall_type=request.user_profile.webapp_type)
            if not flag:
                response = create_response(500)
                response.data = {'msg':"非法操作，订单状态不允许进行该操作"}
                return response.get_response()
            mall_api.update_order_status(request.user, action, order, request)
        else:
            operate_log = ''
            # expired_status = order.status
            # if order_status:
            #     if order.status != int(order_status):
            #         operate_log = u' 修改状态'
            #         mall_api.record_status_log(order.order_id, order.status, order_status, request.manager.username)
            #         order.status = order_status
            #
            #         try:
            #             if expired_status < ORDER_STATUS_SUCCESSED and int(
            #                     order_status) == ORDER_STATUS_SUCCESSED and expired_status != ORDER_STATUS_CANCEL:
            #                 integral.increase_father_member_integral_by_child_member_buyed(order, order.webapp_id)
            #                 # integral.increase_for_self_buy(order.webapp_user_id, order.webapp_id, order.final_price)
            #         except:
            #             notify_message = u"订单状态为已完成时为贡献者增加积分，cause:\n{}".format(unicode_full_stack())
            #             watchdog_error(notify_message)

            # if bill_type:
            #     bill = request.POST.get('bill', '')
            #     # 允许发票信息随意修改
            #     # if order.bill_type != bill_type:
            #     operate_log = operate_log + u' 修改发票'
            #     order.bill_type = bill_type
            #     order.bill = bill

            # if postage:
            # if float(order.postage) != float(postage):
            # operate_log = operate_log + u' 修改邮费'
            # 		order.final_price = order.final_price - order.postage + float(postage) #更新最终价格
            # 		order.postage = postage

            # if ship_name:
            #     if order.ship_name != ship_name:
            #         operate_log = operate_log + u' 修改收货人'
            #         order.ship_name = ship_name
            #
            # if ship_tel:
            #     if order.ship_tel != ship_tel:
            #         operate_log = operate_log + u' 修改收货人电话号'
            #         order.ship_tel = ship_tel
            #
            # if ship_address:
            #     if order.ship_address != ship_address:
            #         operate_log = operate_log + u' 修改收货人地址'
            #         order.ship_address = ship_address

            if 'remark' in request.POST:
                remark = remark.strip()
                if order.remark != remark:
                    operate_log = operate_log + u' 修改订单备注'
                    order.remark = remark

            if final_price:
                # 只有价格不相等 以及待支付的时候 才可以进行订单价格的修改
                if float(order.final_price) != float(final_price) and order.status == ORDER_STATUS_NOT:
                    operate_log = operate_log + u' 修改订单金额'
                    order.final_price = float(final_price)
                    order.edit_money = (order.product_price + order.postage) - (
                        order.coupon_money + order.integral_money + order.weizoom_card_money + order.promotion_saved_money) - order.final_price
                    # 限时抢购
                    promotions = OrderHasPromotion.objects.filter(order_id=order.id)
                    for promotion in promotions:
                        if promotion.promotion_type == 'flash_sale':
                            order.edit_money += json.loads(promotion.promotion_result_json)['promotion_saved_money']

            if len(operate_log.strip()) > 0:
                mall_api.record_operation_log(order.order_id, request.manager.username, operate_log)

            order.save()

        response = create_response(200)
        return response.get_response()

class OrderList(resource.Resource):
    """
    订单列表资源
    """
    app = "mall2"
    resource = "order_list"

    @login_required
    def get(request):
        """
        显示订单列表

        """
        belong = request.GET.get("belong", "all")
        #处理来自“微商城-首页-待发货订单-更多”过来的查看待发货订单的请求
        #add by duhao 2015-09-17
        order_status = request.GET.get('order_status' , '-1')
        mall_type = request.user_profile.webapp_type

        if belong == 'audit':
            second_nav_name = export.ORDER_AUDIT
            has_order = util.is_has_order(request, True)
            page_type = u"财务审核"
        else:
            second_nav_name = export.ORDER_ALL
            has_order = util.is_has_order(request)
            page_type =u"所有订单"
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_mall_order_second_navs(request),
            'second_nav_name': second_nav_name,
            'has_order': has_order,
            'page_type': page_type,
            'order_status': order_status,
            'mall_type': mall_type
        })
        return render_to_response('mall/editor/orders.html', c)

    @login_required
    def api_get(request):
        """
        advanced table中订单列表
        """
        belong = request.GET.get("belong", "all")

        if belong == 'all':
            return util.get_orders_response(request)
        else:
            return util.get_orders_response(request, True)


class OrderProduct(resource.Resource):
    """
    订单中的商品列表
    """

    app = "mall2"
    resource = "order_product"

    @login_required
    def api_get(request):
        order_id = request.GET['order_id']
        order = Order.objects.get(id=order_id)
        response = create_response(200)
        response.data = {
            'products': mall_api.get_order_products(order),
            'postage': '%.2f' % order.postage,
            'final_price': '%.2f' % order.final_price,
            'ship_name': order.ship_name,
            'ship_tel': order.ship_tel,
            'ship_address': order.ship_address,
            'area_str': order.get_str_area
        }
        return response.get_response()


class OrderFilterParams(resource.Resource):
    app = "mall2"
    resource = "order_filter_params"

    @login_required
    def api_get(request):
        mall_type = request.user_profile.webapp_type
        response = create_response(200)
        # 类型

        type = [{'name': u'普通订单', 'value': PRODUCT_DEFAULT_TYPE},
                {'name': u'测试订单', 'value': PRODUCT_TEST_TYPE},
                {'name': u'积分商品', 'value': PRODUCT_INTEGRAL_TYPE}]
        # 状态
        # status = [{'name': u'待支付', 'value': ORDER_STATUS_NOT},
        # {'name': u'已取消', 'value': ORDER_STATUS_CANCEL},
        # 		{'name': u'待发货', 'value': ORDER_STATUS_PAYED_NOT_SHIP},
        # 		{'name': u'已发货', 'value': ORDER_STATUS_PAYED_SHIPED},
        # 		{'name': u'已完成', 'value': ORDER_STATUS_SUCCESSED}]
        status_type = request.GET.get('status', None)
        status = []
        status_dict = {}
        if status_type == 'audit':
            status_dict = AUDIT_STATUS2TEXT
        elif status_type == 'refund':
            status_dict = REFUND_STATUS2TEXT
        else:
            current_status_dict = copy.copy(STATUS2TEXT)
            # del current_status_dict[ORDER_STATUS_REFUNDED]
            del current_status_dict[ORDER_STATUS_GROUP_REFUNDING]
            del current_status_dict[ORDER_STATUS_GROUP_REFUNDED]
            status_dict = current_status_dict

        for key, value in status_dict.items():
            if key != ORDER_STATUS_PAYED_SUCCESSED:
                status.append({'name': value, 'value': key})

        # 来源
        # if WeizoomMallHasOtherMallProductOrder.objects.filter(
        #         webapp_id=request.manager.get_profile().webapp_id).count() > 0:

        orders = belong_to(request.manager.get_profile().webapp_id)

        if not mall_type:
            source = [{'name': u'本店', 'value': 0},
                      {'name': u'商城', 'value': 1}]
        else:
            source = []

        # 支付方式
        pay_interface_type = mall_api.get_pay_interfaces_by_user(request.manager)
        # pay_interface_type.append({'pay_name':u'优惠抵扣','data_value':PAY_INTERFACE_PREFERENCE})

        # 有该营销工具才会显示此选项
        # user_market_tool_modules = request.manager.market_tool_modules
        # if 'delivery_plan' in user_market_tool_modules:
        # 	type.append({'name': u'套餐订单', 'value': PRODUCT_DELIVERY_PLAN_TYPE})
        # if 'thanks_card' in user_market_tool_modules:
        # 	type.append({'name': u'贺卡订单', 'value': THANKS_CARD_ORDER})
        response.data = {
            'type': type,
            'mall_type': mall_type,
            'status': status,
            'pay_interface_type': pay_interface_type,
            'source': source
        }
        return response.get_response()


class OrderExport(resource.Resource):
    app = "mall2"
    resource = "order_export"

    @login_required
    def get(request):
        orders = util.export_orders_json(request)
        return ExcelResponse(orders, output_name=u'订单列表'.encode('utf8'), force_csv=False)


class ChannelQrcodePayedOrder(resource.Resource):
    app = "mall2"
    resource = "channel_qrcode_payed_order"

    @login_required
    def api_get(request):
        channel_qrcode_id = request.GET.get('id', None)
        relations = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=channel_qrcode_id)
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

        webapp_users = WebAppUser.objects.filter(member_id__in=member_ids)
        webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
        webapp_user_ids = set(webapp_user_id2member_id.keys())
        orders = Order.by_webapp_user_id(webapp_user_ids).filter(status=ORDER_STATUS_SUCCESSED).order_by(
            '-created_at')
        # 进行分页
        count_per_page = int(request.GET.get('count_per_page', 15))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page,
                                              query_string=request.META['QUERY_STRING'])

        # 获取order对应的会员
        webapp_user_ids = set([order.webapp_user_id for order in orders])
        from modules.member.models import Member

        webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

        # 获得order对应的商品数量
        order_ids = [order.id for order in orders]
        order2productcount = {}
        for relation in OrderHasProduct.objects.filter(order_id__in=order_ids):
            order_id = relation.order_id
            if order_id in order2productcount:
                order2productcount[order_id] = order2productcount[order_id] + 1
            else:
                order2productcount[order_id] = 1
        # 构造返回的order数据
        items = []
        today = datetime.today()
        for order in orders:
            # 获取order对应的member的显示名
            member = webappuser2member.get(order.webapp_user_id, None)
            if member:
                order.buyer_name = member.username_for_html
            else:
                order.buyer_name = u'未知'

            items.append({
                'id': order.id,
                'order_id': order.order_id,
                'status': util.get_order_status_text(order.status),
                'total_price': order.final_price,
                'ship_name': order.ship_name,
                'buyer_name': order.buyer_name,
                'pay_interface_name': PAYTYPE2NAME.get(order.pay_interface_type, u''),
                'created_at': datetime.strftime(order.created_at, '%m-%d %H:%M'),
                'product_count': order2productcount.get(order.id, 0),  # 'products': product_items,
                'customer_message': order.customer_message
            })

        response = create_response(200)
        response.data = {
            'items': items,
            'sortAttr': request.GET.get('sort_attr', '-created_at'),
            'pageinfo': paginator.to_dict(pageinfo),
        }
        return response.get_response()

class GroupOrderRefunded(resource.Resource):
    app = "mall2"
    resource = "group_order_refunded"

    def post(request):
        KEY = "MjExOWYwMzM5M2E4NmYwNWU4ZjI5OTI1YWFmM2RiMTg="
        order_ids = request.POST.getlist('order_ids', [])
        key = request.POST.get('authkey', '')
        response = create_response(200)
        if key == KEY:
            if not order_ids:
                response.updated_order_ids = []
                response.not_update_orders_ids = []
                return response.get_response()
            try:
                orders = Order.objects.filter(
                    order_id__in=order_ids,
                    status=ORDER_STATUS_GROUP_REFUNDING
                )
                refunding_order_ids = [order.order_id for order in orders]
                order_id2order = dict([(order.order_id, order) for order in orders])
                orders.update(status=ORDER_STATUS_GROUP_REFUNDED)
                response.updated_order_ids = refunding_order_ids
                response.not_update_order_ids = [id for id in order_ids if id not in refunding_order_ids]

                for order_id in refunding_order_ids:
                    order = order_id2order[order_id]
                    record_status_log(order_id, u'系统', order.status, ORDER_STATUS_GROUP_REFUNDED)
                    record_operation_log(order_id, u'系统', "退款完成", order)

            except:
                updated_order_ids = [order.order_id for order in Order.objects.filtr(
                    order_id__in=order_ids,
                    status=ORDER_STATUS_GROUP_REFUNDED
                )]
                response.updated_order_ids = updated_order_ids
                response.not_update_order_ids = [id for id in order_ids if id not in updated_order_ids]
        else:
            response.updated_order_ids = []
            response.not_update_order_ids = order_ids
        return response.get_response()