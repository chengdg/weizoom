#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import logging

from excel_response import ExcelResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from core import resource
from mall import export
import util
from tools.regional import views as regional_util
from core.jsonresponse import create_response
from core import paginator
from mall.models import *
from market_tools.tools.channel_qrcode.models import ChannelQrcodeHasMember
import mall.module_api as mall_api
from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning
from core.exceptionutil import unicode_full_stack
from modules.member.models import WebAppUser
from account.models import UserProfile
from mall.module_api import update_order_status
from weixin.user.module_api import get_mp_qrcode_img
from weixin2.models import News
from export_job.models import ExportJob

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
        webapp_id = request.user_profile.webapp_id
        order = Order.objects.get(id=order_id)
        success = util.assert_webapp_id(order, webapp_id)
        if success == False:
            response = create_response(404)
            return response.get_response()

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
        woid = request.webapp_owner_id
        export2data = {}

        if belong == 'audit':
            second_nav_name = export.ORDER_AUDIT
            has_order = util.is_has_order(request, True)
            page_type = u"财务审核"
            export_jobs = ExportJob.objects.filter(woid=woid,type=3,is_download=0).order_by("-id")
            if export_jobs:
                export2data = {
                    "woid":int(export_jobs[0].woid) ,#
                    "status":1 if export_jobs[0].status else 0,
                    "is_download":1 if export_jobs[0].is_download else 0,
                    "id":int(export_jobs[0].id),
                    # "file_path": export_jobs[0].file_path,
                    }

        else:
            second_nav_name = export.ORDER_ALL
            has_order = util.is_has_order(request)
            page_type =u"所有订单"
            export_jobs = ExportJob.objects.filter(woid=woid,type=1,is_download=0).order_by("-id")
            if export_jobs:
                export2data = {
                    "woid":int(export_jobs[0].woid) ,#
                    "status":1 if export_jobs[0].status else 0,
                    "is_download":1 if export_jobs[0].is_download else 0,
                    "id":int(export_jobs[0].id),
                    # "file_path": export_jobs[0].file_path,
                    }
        if not export2data:
            export2data = {
                "woid":0,
                "status":1,
                "is_download":1,
                "id":0,
                "file_path":0,
                }
        
        
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_mall_order_second_navs(request),
            'second_nav_name': second_nav_name,
            'has_order': has_order,
            'page_type': page_type,
            'order_status': order_status,
            'mall_type': mall_type,
            'export2data': export2data,
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
        webapp_id = request.user_profile.webapp_id
        order = Order.objects.get(id=order_id, webapp_id=webapp_id)
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
            del current_status_dict[ORDER_STATUS_REFUNDED]
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


# class OrderExport(resource.Resource):
#     app = "mall2"
#     resource = "order_export"

#     @login_required
#     def get(request):
#         orders = util.export_orders_json(request)
#         return ExcelResponse(orders, output_name=u'订单列表'.encode('utf8'), force_csv=False)


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
                refund_orders = Order.objects.filter(
                    order_id__in=order_ids,
                    status=ORDER_STATUS_GROUP_REFUNDED
                )
                refund_order_ids = [order.order_id for order in refund_orders]
                webapp_ids = [order.webapp_id for order in orders]
                webapp_id2user = dict([(profile.webapp_id, profile.user) for profile in UserProfile.objects.filter(webapp_id__in=webapp_ids)])
                refunding_order_ids = [order.order_id for order in orders]
                order_id2order = dict([(order.order_id, order) for order in orders])
                for order in orders:
                    update_order_status(webapp_id2user[order.webapp_id], 'return_success', order)
                    order.status = ORDER_STATUS_GROUP_REFUNDED
                    order.save()
                response.updated_order_ids = refunding_order_ids + refund_order_ids
                response.not_update_order_ids = [id for id in order_ids if id not in (refunding_order_ids + refund_order_ids)]
            except:
                logging.info(unicode_full_stack())
                updated_order_ids = [order.order_id for order in Order.objects.filter(
                    order_id__in=order_ids,
                    status=ORDER_STATUS_GROUP_REFUNDED
                )]
                response.updated_order_ids = updated_order_ids
                response.not_update_order_ids = [id for id in order_ids if id not in updated_order_ids]
        else:
            response.updated_order_ids = []
            response.not_update_order_ids = order_ids
        return response.get_response()

class PrintOrder(resource.Resource):
    app = 'mall2'
    resource = 'print_order'

    @login_required
    def api_get(request):
        store_name = UserProfile.objects.get(user_id=request.manager.id).store_name
        qrcode_url = get_mp_qrcode_img(request.manager.id)

        order_ids = json.loads(request.GET.get('order_ids', '[]'))
        #order_ids = request.GET.get('order_ids', '')
        orders = Order.objects.filter(id__in=[int(id) for id in order_ids])
        webapp_user_ids = set([order.webapp_user_id for order in orders])
        from modules.member.models import Member
        webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

        order_ids = [order.id for order in orders]
        # 获得order对应的商品数量
        order2productcount = {}
        for relation in OrderHasProduct.objects.filter(order_id__in=order_ids).order_by('id'):
            order_id = relation.order_id
            if order_id in order2productcount:
                order2productcount[order_id] = order2productcount[order_id] + 1
            else:
                order2productcount[order_id] = 1

        # 构造返回的order数据
        for order in orders:
            # 获取order对应的member的显示名
            member = webappuser2member.get(order.webapp_user_id, None)
            if member:
                order.buyer_name = member.username_for_print
            else:
                order.buyer_name = u'未知'
            order.product_count = order2productcount.get(order.id, 0)

        # 构造返回的order数据
        items = []
        for order in orders:
            products = mall_api.get_order_products(order)

            for product in products:
                property_values = []

                if product['promotion']:
                    if product['promotion']['type'] == "flash_sale":
                        product['name'] = u"【限时抢购】" + product['name']
                    elif product['promotion']['type'] == "premium_sale:premium_product":
                        product['name'] = u"【赠品】" + product['name']
                if product.has_key('grade_discounted_money') and product['grade_discounted_money']:
                        product['name'] = u"【会员优惠】" + product['name']


                if product.has_key('custom_model_properties') and product['custom_model_properties']:
                    for model in product['custom_model_properties']:
                        property_values.append(model['property_value'])
                product['property_values'] = '/'.join(property_values)

                if order.supplier_user_id:
                    product['price'] = product['purchase_price']
                    product['total_price'] = product['purchase_price'] * product['count']

            items.append({
                'id': order.id,
                'order_id': order.order_id,
                'supplier_user_id': order.supplier_user_id,
                'products': products,
                'total_price': order.total_purchase_price if order.supplier_user_id else Order.get_order_has_price_number(order),
                'order_total_price': float('%.2f' % order.get_total_price()),
                'ship_name': order.ship_name,
                'ship_address': '%s %s' % (regional_util.get_str_value_by_string_ids(order.area), order.ship_address),
                'ship_tel': order.ship_tel,
                'buyer_name': order.buyer_name,
                'created_at': datetime.strftime(order.created_at, '%Y-%m-%d %H:%M:%S'),
                'product_count': order.product_count,
                'postage': 0 if order.supplier_user_id else '%.2f' % order.postage,
                'save_money': 0 if order.supplier_user_id else float(Order.get_order_has_price_number(order)) + float(order.postage) - float(
                    order.final_price) - float(order.weizoom_card_money),
                'pay_money': order.total_purchase_price if order.supplier_user_id else order.final_price + order.weizoom_card_money,
            })

        response = create_response(200)
        response.data = {
            'items': items,
            'store_name': store_name,
            'qrcode_url': qrcode_url,
            'order_count': len(order_ids)
        }
        return response.get_response()


class orderConfig(resource.Resource):
    """
    订单配置
    """
    app = "mall2"
    resource = "order_config"

    @login_required
    def get(request):
        if MallConfig.objects.filter(owner=request.manager).count() == 0:
            MallConfig.objects.create(owner=request.user, order_expired_day=24)

        mall_config = MallConfig.objects.filter(owner=request.manager)[0]
        share_page_config = MallShareOrderPageConfig.objects.filter(owner=request.manager)
        if share_page_config.count() == 0:
            share_page_config = MallShareOrderPageConfig.objects.create(owner=request.user, is_share_page=False)
        else:
            share_page_config = share_page_config[0]

        if share_page_config.material_id:
            news = News.objects.get(material_id=share_page_config.material_id)
        else:
            news = None

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_mall_order_second_navs(request),
            'second_nav_name': export.ORDER_EXPIRED_TIME,
            'mall_config': mall_config,
            'share_page_config': share_page_config,
            'news': news
        })
        return render_to_response('mall/editor/edit_expired_time.html', c)

    @login_required
    def post(request):
        if not request.POST.get('order_expired_day', 24):
            order_expired_day = 0
        else:
            order_expired_day = int(request.POST.get('order_expired_day', 24))
        if MallConfig.objects.filter(owner=request.manager).count() > 0:
            MallConfig.objects.filter(owner=request.manager).update(order_expired_day=order_expired_day)
        else:
            MallConfig.objects.create(owner=request.user, order_expired_day=24)

        logging.info(u"user_id:%s, expired_time:%d" % (request.manager.id, order_expired_day))

        is_share_page = request.POST.get('isShowPage', False)
        share_background_image = request.POST.get('backgroundImage', '')
        material_id = request.POST.get('materialId', '')
        share_image = request.POST.get('shareImage', '')
        share_describe = request.POST.get('shareInfo', '')

        share_page_config = MallShareOrderPageConfig.objects.filter(owner=request.manager)
        if is_share_page:
            if share_page_config.count() > 0:
                share_page_config.update(
                    is_share_page=is_share_page,
                    background_image=share_background_image,
                    material_id=material_id,
                    share_image=share_image,
                    share_describe=share_describe
                )
                share_page_config = share_page_config[0]
            else:
                share_page_config = MallShareOrderPageConfig.objects.create(
                    owner=request.user,
                    is_share_page=is_share_page,
                    background_image=share_background_image,
                    share_image=share_image,
                    share_describe=share_describe,
                    material_id=material_id
                )
        else:
            if share_page_config.count() > 0:
                share_page_config.update(is_share_page=is_share_page)
                share_page_config = share_page_config[0]
            else:
                share_page_config = MallShareOrderPageConfig.objects.create(owner=request.user, is_share_page=False)

        if share_page_config.material_id:
            news = News.objects.get(material_id=share_page_config.material_id)
            share_page_config.news_id = news.id
            share_page_config.save()
        else:
            news = None

        mall_config = MallConfig.objects.filter(owner=request.manager)[0]
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_mall_order_second_navs(request),
            'second_nav_name': export.ORDER_EXPIRED_TIME,
            'mall_config': mall_config,
            'share_page_config': share_page_config,
            'news': news
        })
        return render_to_response('mall/editor/edit_expired_time.html', c)

class OrderGetFile(resource.Resource):
    """
    所有订单/财务审核中的订单导出
    获取参数，构建成文件，上传到u盘运
    """
    app = "mall2"
    resource ="export_order_param"
    
    @login_required
    def api_get(request):
        woid = request.webapp_owner_id
        type = int(request.GET.get('type', 0))

        now = datetime.now()
        #判断用户是否存在导出数据任务
        if type in [1,3] :
            
            param = util.get_param_from(request)
           
        exportjob = ExportJob.objects.create(
                                    woid = woid,
                                    type = type,
                                    status = 0,
                                    param = param,
                                    created_at = now,
                                    processed_count =0,
                                    count =0,
                                    )
        from mall.order.tasks import send_order_export_job_task
        send_order_export_job_task.delay(exportjob.id, param, type)

        response = create_response(200)
        response.data = {
            'ok':'ok',
            "exportjob_id":exportjob.id,
        }
        return response.get_response()

class SenderInfo(resource.Resource):
    app = 'mall2'
    resource = 'sender_info'

    @login_required
    def get(request):
        """
        发件人信息创建页&&发件人信息更新页
        """
        # 如果有product说明更新， 否则说明创建
        sender_info_id = request.GET.get('id')
        sender_info_id = int(sender_info_id) if sender_info_id else 0
        webapp_id = request.user_profile.webapp_id

        if sender_info_id:
            try:
                sender_info = SenderInfo.objects.get(webapp_id=webapp_id, id=sender_info_id)
            except SenderInfo.DoesNotExist:
                raise Http404
           

        else:
            sender_info = {}

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_mall_order_second_navs(request),
            'second_nav_name': export.ORDER_SENDER_INFO,
            'sender_info': sender_info,
        })


        return render_to_response('mall/editor/sender_info.html', c)

    @login_required
    def put(request):
        """创建发件人信息
        """

        webapp_id = request.user_profile.webapp_id


        sender_info = SenderInfo.objects.create(
            webapp_id=webapp_id,
            sender_name=request.POST.get('sender_name', '').strip(),
            area=request.POST.get('area', '').strip(),
            sender_address=request.POST.get('sender_address', '').strip(),
            sender_tel=request.POST.get('tel', '').strip(),
            code=request.POST.get('code', '').strip(),
            company_name=request.POST.get('company_name', '').strip(),
            remarks=request.POST.get('remarks', '').strip(),
        )

        SenderInfo.objects.filter(~Q(id=sender_info.id),webapp_id=webapp_id).update(is_selected=False)
        # component_authed_appids = ComponentAuthedAppid.objects.filter(~Q(user_id=user_id), authorizer_appid=authorizer_appid)
        return HttpResponseRedirect('/mall2/sender_info_list/')

    @login_required
    def post(request):
        """更新发件人信息
        API:
          method: post
          url: /mall2/sender_info/?id=%d
        """

        # 获取默认运费
        sender_info_id = request.GET.get('id')
        sender_info_id = int(sender_info_id) if sender_info_id else 0
        webapp_id = request.user_profile.webapp_id
        is_selected = True if (request.GET.get('is_selected','') in ('true', 'yes', 'True', 'Yes', True, '1')) else False
        

        if sender_info_id:
            SenderInfo.objects.filter(webapp_id=webapp_id,id=sender_info_id).update(
                sender_name=request.POST.get('sender_name', '').strip(),
                area=request.POST.get('area', '').strip(),
                sender_address=request.POST.get('sender_address', '').strip(),
                sender_tel=request.POST.get('tel', '').strip(),
                code=request.POST.get('code', '').strip(),
                company_name=request.POST.get('company_name', '').strip(),
                remarks=request.POST.get('remarks', '').strip(),
                is_selected=is_selected
            )
        if is_selected:
            SenderInfo.objects.filter(~Q(id=sender_info_id),webapp_id=webapp_id).update(is_selected=False)
        return HttpResponseRedirect(
            '/mall2/sender_info_list/')

    @login_required
    def api_delete(request):
        """
        删除发货人
        """

        sender_info_id = request.GET.get('id')
        sender_info_id = int(sender_info_id) if sender_info_id else 0
        webapp_id = request.user_profile.webapp_id
        if sender_info_id:
            SenderInfo.objects.filter(webapp_id=webapp_id,id=sender_info_id).update(is_deleted=True)
        return HttpResponseRedirect(
            '/mall2/sender_info_list/')



class SenderInfoList(resource.Resource):
    app = 'mall2'
    resource = 'sender_info_list'

    @login_required
    def get(request):
        """
        发件人信息创建页&&发件人信息更新页
        """
        # 如果有product说明更新， 否则说明创建

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_mall_order_second_navs(request),
            'second_nav_name': export.ORDER_SENDER_INFO,

        })


        return render_to_response('mall/editor/sender_info_list.html', c)

    @login_required
    def api_get(request):

        webapp_id = request.user_profile.webapp_id
        sender_infos = SenderInfo.objects.filter(webapp_id=webapp_id,is_deleted=False).order_by("-id")
        count_per_page = int(request.GET.get('count_per_page', 100))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, sender_infos = paginator.paginate(
            sender_infos,
            cur_page,
            count_per_page,
            query_string=request.META['QUERY_STRING'])

        items = []
        for sender_info in sender_infos :
            items.append(sender_info.to_dict())
        response = create_response(200)
        response.data = {
            'items': items,
            'pageinfo': paginator.to_dict(pageinfo),
        }
        return response.get_response()
