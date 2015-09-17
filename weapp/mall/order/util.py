#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, datetime

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from mall import export
from tools.regional import views as regional_util
from tools.regional.views import get_str_value_by_string_ids_new
from mall.promotion.models import CouponRule, Promotion, ProductHasPromotion, PROMOTION_TYPE_COUPON
from modules.member.models import WebAppUser
import mall.models
import mall.export
from core.jsonresponse import create_response
from core import paginator
from mall.models import *
from market_tools.tools.channel_qrcode.models import ChannelQrcodeHasMember
import mall.module_api as mall_api
from market_tools.tools.weizoom_card.models import AccountHasWeizoomCardPermissions
from core.restful_url_route import api
from watchdog.utils import watchdog_info
import re

COUNT_PER_PAGE = 20

DEFAULT_CREATE_TIME = '2000-01-01 00:00:00'

COUNT_PER_PAGE = 20
FIRST_NAV = export.ORDER_FIRST_NAV


def export_orders_json(request):
    # debug
    # pre_page = 500
    # test_index = 0
    # begin_time = time.time()
    status = {
        '0': u'待支付',
        '1': u'已取消',
        '2': u'已支付',
        '3': u'待发货',
        '4': u'已发货',
        '5': u'已完成',
        '6': u'退款中',
        '7': u'退款完成',
    }

    payment_type = {
        '-1': u'',
        '0': u'支付宝',
        '2': u'微信支付',
        '3': u'微众卡支付',
        '9': u'货到付款',
        '10': u'优惠抵扣'
    }

    source_list = {
        'mine_mall': u'本店',
        'weizoom_mall': u'商城'
    }

    orders = [
        [u'订单号', u'下单时间', u'付款时间', u'商品名称', u'规格',
         u'商品单价', u'商品数量', u'销售额', u'商品总重量（斤）', u'支付方式', u'支付金额', u'现金支付金额', u'微众卡支付金额',
         u'运费', u'积分抵扣金额', u'优惠券金额', u'优惠券名称', u'订单状态', u'购买人',
         u'收货人', u'联系电话', u'收货地址省份', u'收货地址', u'发货人', u'发货人备注', u'来源' ,u'物流公司', u'快递单号', u'发货时间',u'商家备注',u'用户备注']
    ]

    # -----------------------获取查询条件字典和时间筛选条件-----------构造oreder_list-------------开始
    webapp_id = request.user_profile.webapp_id
    order_list = Order.objects.belong_to(webapp_id).order_by('-id')
    status_type = request.GET.get('status', None)
    if status_type:
        if status_type == 'refund':
            order_list = order_list.filter(status__in=[ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED])
        elif status_type == 'audit':
            order_list = order_list.filter(status__in=[ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED])

    #####################################
    query_dict, date_interval = __get_select_params(request)
    product_name = ''
    if query_dict.get("product_name"):
        product_name = query_dict["product_name"]

    order_list = __get_orders_by_params(query_dict, date_interval, order_list)

    if product_name:
        # 订单总量
        order_count = len(order_list)
        finished_order_count = 0
        for order in order_list:
            if order.type != PRODUCT_INTEGRAL_TYPE and order.status == ORDER_STATUS_SUCCESSED:
                finished_order_count += 1
    else:
        order_count = order_list.count()
        finished_order_count = order_list.filter(status=ORDER_STATUS_SUCCESSED).count()
        order_list = list(order_list.all())
    # -----------------------获取查询条件字典和时间筛选条件--------------构造oreder_list----------结束
    # 商品总额：
    total_product_money = 0.0
    # 支付金额
    final_total_order_money = 0.0
    # 微众卡支付金额
    weizoom_card_total_order_money = 0.0
    # 积分抵扣总金额
    use_integral_money = 0.0
    # 赠品总数
    total_premium_product = 0
    # 优惠劵价值总和
    coupon_money_count = 0
    #####################################

    # print 'begin step 1 order_list - '+str(time.time() - begin_time)
    order_ids = []
    order_order_ids = []
    coupon_ids = []
    for o in order_list:
        order_ids.append(o.id)
        order_order_ids.append(o.order_id)
        if o.coupon_id:
            coupon_ids.append(o.coupon_id)
    coupon2role = {}
    role_ids = []
    from mall.promotion.models import Coupon, CouponRule

    for coupon in Coupon.objects.filter(id__in=coupon_ids):
        coupon2role[coupon.id] = coupon.coupon_rule_id
        if role_ids.count(coupon.coupon_rule_id) == 0:
            role_ids.append(coupon.coupon_rule_id)
    role_id2role = dict([(role.id, role) for role in CouponRule.objects.filter(id__in=role_ids)])

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
                if i > 0 and re.match('', mod[i:]) and model_value_ids.count(mod[i:]) == 0:
                    model_value_ids.append(mod[i:])

    # print 'begin step 3 products - '+str(time.time() - begin_time)
    id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])
    # print 'begin step 4 coupons - '+str(time.time() - begin_time)

    # print 'begin step 5 models - '+str(time.time() - begin_time)
    id2modelname = dict(
        [(str(value.id), value.name) for value in ProductModelPropertyValue.objects.filter(id__in=model_value_ids)])
    # print 'end step 6 coupons - '+str(time.time() - begin_time)

    # 获取order对应的会员
    webapp_user_ids = set([order.webapp_user_id for order in order_list])
    from modules.member.models import Member

    webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

    # print 'end step 6.7 - '+str(time.time() - begin_time)
    # 获取order对应的赠品
    order2premium_product = {}
    order2promotion = dict()
    for relation in OrderHasPromotion.objects.filter(order_id__in=order_ids, promotion_id__in=promotion_ids,
                                          promotion_type='premium_sale'):
        order2promotion[relation.order_id] = relation.promotion_result
        order2promotion[relation.order_id]['promotion_id'] = relation.promotion_id

    premium_product_ids = []
    for order_id in order2promotion:
        temp_premium_products = []
        promotion = order2promotion[order_id]
        if promotion.get('premium_products'):
            for premium_product in order2promotion[order_id]['premium_products']:
                temp_premium_products.append({
                    'id': premium_product['id'],
                    'name': premium_product['name'],
                    'count': premium_product['count'],
                    'price': premium_product['price'],
                    'purchase_price': premium_product.get('purchase_price', 0),
                })
                premium_product_ids.append(premium_product['id'])
        order2premium_product[order_id] = {}
        order2premium_product[order_id][promotion['promotion_id']] = temp_premium_products

    # 获取商品对应的重量
    product_idandmodel_value2weigth = dict([((model.product_id, model.name), model.weight) for model in
                                            ProductModel.objects.filter(product_id__in=product_ids)])
    # 赠品为单规格
    premium_product_id2weight = dict([(model.product_id, model.weight) for model in
                                      ProductModel.objects.filter(product_id__in=premium_product_ids)])
    fackorders = list(Order.objects.filter(origin_order_id__in=order_ids))

    # 获取order对应的供货商

    order2supplier2fackorders = {}
    # 取出所有的子订单

    for order in fackorders:
        origin_order_id = order.origin_order_id
        order2supplier2fackorders.setdefault(origin_order_id, {})
        order2supplier2fackorders[origin_order_id][order.supplier] = order
        # 在order_order_ids中添加子订单
        order_order_ids.append(order.order_id)
    # 获取order对应的发货时间
    order2postage_time = dict([(log.order_id, log.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8')) for log in
                        OrderOperationLog.objects.filter(order_id__in=order_order_ids, action__startswith="订单发货")])

    order2supplier = dict([(supplier.id,supplier) for supplier in Supplier.objects.filter(owner=request.manager)])
    # 判断是否有供货商，如果有则显示该字段
    has_supplier = False
    for order in order_list:
        if 0 != order.supplier:
            has_supplier = True
            break

    if has_supplier:
        orders[0].append(u'采购价')
        orders[0].append(u'采购成本')
    # print 'end step 8 order - '+str(time.time() - begin_time)
    # 获取order对应的收货地区
    temp_premium_id = None
    temp_premium_products = []
    for order in order_list:
        # 获取order对应的member的显示名
        member = webappuser2member.get(order.webapp_user_id, None)
        if member:
            order.buyer_name = handle_member_nickname(member.username_for_html)
            order.member_id = member.id
        else:
            order.buyer_name = u'未知'

        # 计算总和
        final_price = 0.0
        weizoom_card_money = 0.0
        if order.status in [2, 3, 4, 5, 6]:
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
            province = area.split(' ')[0]
            address = '%s %s' % (area, order.ship_address)
        else:
            province = u''
            address = '%s' % (order.ship_address)

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

        i = 0 # 判断是否订单第一件商品
        orderRelations = relations.get(order.id, [])
        for relation in sorted(orderRelations, key=lambda o:o.id):
            if temp_premium_id and '%s_%s' % (order.id, relation.promotion_id) != temp_premium_id:
                # 添加赠品信息
                orders.extend(temp_premium_products)
                temp_premium_products = []
                temp_premium_id = None
            product = id2product[relation.product_id]
            model_value = ''
            for mod in relation.product_model_name.split('_'):
                mod_i = mod.find(':') + 1
                if mod_i > 0:
                    model_value += '-' + id2modelname.get(mod[mod_i:], '')
                else:
                    model_value = '-'

            # 付款时间
            if order.payment_time and DEFAULT_CREATE_TIME != order.payment_time.__str__():
                payment_time = order.payment_time.strftime('%Y-%m-%d %H:%M').encode('utf8')
            else:
                payment_time = ''

            # 优惠券和金额
            coupon_name = ''
            coupon_money = ''
            if order.coupon_id:
                role_id = coupon2role.get(order.coupon_id, None)
                if role_id:
                    if role_id2role[role_id].limit_product:
                        if role_id2role[role_id].limit_product_id == relation.product_id:
                            coupon_name = role_id2role[role_id].name + "（单品券）"
                    elif i == 0:
                        coupon_name = role_id2role[role_id].name + "（通用券）"
                if not role_id or coupon_name and order.coupon_money > 0:
                    coupon_money = order.coupon_money

            fackorder_sons = order2supplier2fackorders.get(order.id, None)
            fackorder = None
            if fackorder_sons:
                fackorder = fackorder_sons.get(product.supplier, None)

            save_money = str(order.edit_money).replace('.', '').replace('-', '') if order.edit_money else False

            order_id = '%s%s'.encode('utf8') % (order.order_id if not fackorder else fackorder.order_id, '-%s' % save_money if save_money else '')
            order_status = status[str(order.status if not fackorder else fackorder.status)].encode('utf8')
            # 订单发货时间
            postage_time = order2postage_time.get(order.order_id if not fackorder else fackorder.order_id, '')
            if fackorder and 0 != fackorder.supplier:
                source = order2supplier[fackorder.supplier].name.encode("utf-8")
            elif fackorder == None and 0 != order.supplier:
                source = order2supplier[order.supplier].name.encode("utf-8")

            if i == 0:
                # 发货人处填写的备注
                temp_leader_names = (order.leader_name if not fackorder else fackorder.leader_name).split('|')
                leader_remark = ''
                j = 1
                while j < len(temp_leader_names):
                    leader_remark += temp_leader_names[j]
                    j += 1

                tmp_order = [
                    order_id,
                    order.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8'),
                    payment_time,
                    product.name.encode('utf8'),
                    model_value[1:].encode('utf8'),
                    relation.price,
                    relation.number,
                    relation.price*relation.number,
                    product_idandmodel_value2weigth[
                        (relation.product_id, relation.product_model_name)] * 2 * relation.number,
                    payment_type[str(int(order.pay_interface_type))],
                    final_price + weizoom_card_money,
                    final_price,
                    u'' if order.status == 0 else weizoom_card_money,
                    order.postage,
                    u'' if order.status == 0 else order.integral_money,
                    u'' if order.status == 1 else coupon_money,
                    u'' if order.status == 1 else coupon_name,
                    order_status,
                    order.buyer_name.encode('utf8'),
                    order.ship_name.encode('utf8'),
                    order.ship_tel.encode('utf8'),
                    province.encode('utf8'),
                    address.encode('utf8'),
                    temp_leader_names[0].encode('utf8'),
                    leader_remark.encode('utf8'),
                    source.encode('utf8'),
                    express_util.get_name_by_value(order.express_company_name if not fackorder else fackorder.express_company_name).encode('utf8'),
                    (order.express_number if not fackorder else fackorder.express_number).encode('utf8'),
                    postage_time,
                    order.remark.encode('utf8'),
                    u'' if order.customer_message == '' else order.customer_message.encode('utf-8')

                ]
                if has_supplier:
                    tmp_order.append( u'' if 0.0 == product.purchase_price else product.purchase_price)
                    tmp_order.append(u''  if 0.0 ==product.purchase_price else product.purchase_price*relation.number)
                orders.append(tmp_order)
                total_product_money += relation.price * relation.number
            else:
                tmp_order=[
                    order_id,
                    order.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8'),
                    payment_time,
                    product.name,
                    model_value[1:],
                    relation.price,
                    relation.number,
                    relation.price*relation.number,
                    product_idandmodel_value2weigth[
                        (relation.product_id, relation.product_model_name)] * 2 * relation.number,
                    payment_type[str(int(order.pay_interface_type))],
                    u'',
                    u'',
                    u'',
                    u'',
                    u'',
                    u'' if order.status == 1 else coupon_money,
                    u'' if order.status == 1 else coupon_name,
                    order_status,
                    order.buyer_name.encode('utf8'),
                    order.ship_name.encode('utf8'),
                    order.ship_tel.encode('utf8'),
                    province.encode('utf8'),
                    address.encode('utf8'),
                    temp_leader_names[0].encode('utf8'),
                    leader_remark.encode('utf8'),
                    source.encode('utf8'),
                    express_util.get_name_by_value(order.express_company_name if not fackorder else fackorder.express_company_name).encode('utf8'),
                    (order.express_number if not fackorder else fackorder.express_number).encode('utf8'),
                    postage_time,
                    u'',
                    u''

                ]
                if has_supplier:
                    tmp_order.append(u'' if 0.0 == product.purchase_price else product.purchase_price)
                    tmp_order.append(u'' if 0.0 ==product.purchase_price else product.purchase_price*relation.number)
                orders.append(tmp_order)
                total_product_money += relation.price * relation.number
            i += 1
            if order.id in order2premium_product and not temp_premium_id:
                premium_products = order2premium_product[order.id].get(relation.promotion_id, [])
                # 已取消订单不累计赠品数量
                if order_status != STATUS2TEXT[1] and order_status != STATUS2TEXT[7]:
                    total_premium_product += len(premium_products)
                for premium_product in premium_products:
                    tmp_order = [
                        order_id,
                        order.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8'),
                        payment_time,
                        u'(赠品)' + premium_product['name'],
                        u'',
                        premium_product['price'],
                        premium_product['count'],
                        0.0,
                        premium_product_id2weight[premium_product['id']] * 2 * relation.number,
                        payment_type[str(int(order.pay_interface_type))],
                        u'',
                        u'',
                        u'',
                        u'',
                        u'',
                        u'',
                        u'',
                        order_status,
                        order.buyer_name.encode('utf8'),
                        order.ship_name.encode('utf8'),
                        order.ship_tel.encode('utf8'),
                        province.encode('utf8'),
                        address.encode('utf8'),
                        temp_leader_names[0].encode('utf8'),
                        leader_remark.encode('utf8'),
                        source.encode('utf8'),
                        express_util.get_name_by_value(order.express_company_name if not fackorder else fackorder.express_company_name).encode('utf8'),
                        (order.express_number if not fackorder else fackorder.express_number).encode('utf8'),
                        postage_time,
                        u'',
                        u''
                    ]
                    if has_supplier:
                        tmp_order.append( u'' if 0.0 == premium_product['purchase_price'] else premium_product['purchase_price'])
                        tmp_order.append(u'' if 0.0 ==premium_product['purchase_price'] else premium_product['purchase_price']*premium_product['count'])
                    temp_premium_products.append(tmp_order)
                    temp_premium_id = '%s_%s' % (order.id, relation.promotion_id)
                # if test_index % pre_page == pre_page-1:
                # 	print str(test_index)+' - '+str(time.time() - test_begin_time)+'-'+str(time.time() - begin_time)
    if temp_premium_id:
        # 处理赠品信息
        orders.extend(temp_premium_products)
    orders.append([
        u'总计',
        u'订单量:' + str(order_count).encode('utf8'),
        u'已完成:' + str(finished_order_count).encode('utf8'),
        u'商品金额:' + str(total_product_money).encode('utf8'),
        u'支付总额:' + str(final_total_order_money + weizoom_card_total_order_money).encode('utf8'),
        u'现金支付金额:' + str(final_total_order_money).encode('utf8'),
        u'微众卡支付金额:' + str(weizoom_card_total_order_money).encode('utf8'),
        u'赠品总数:' + str(total_premium_product).encode('utf8'),
        u'积分抵扣总金额:' + str(use_integral_money).encode('utf8'),
        u'优惠劵价值总额:' + str(coupon_money_count).encode('utf8'),
    ])
    # print 'end - '+str(time.time() - begin_time)

    return orders


def handle_member_nickname(name):
    try:
        reobj = re.compile(r'\<span.*?\<\/span\>')
        name, number = reobj.subn('口', name)
        return u'{}'.format(name)
    except:
        return u''


def get_detail_response(request, belong='all'):
    # 没有订单号参数直接返回订单列表页
    if not request.GET.get('order_id', None):
        return HttpResponseRedirect('/mall2/order_list/')
    else:
        order = mall.models.Order.objects.get(id=request.GET['order_id'])
    # #如果定单是微众卡支付显示微众卡号
    # try:
    # 	order.used_weizoom_card_id, order.used_weizoom_card_number = order.get_used_weizoom_card_id()
    # except:
    # 	order.used_weizoom_card_id = None
    # 	order.used_weizoom_card_number = None

    if request.method == 'GET':
        order_has_products = OrderHasProduct.objects.filter(order=order)

        number = 0
        for order_has_product in order_has_products:
            number += order_has_product.number
        order.number = number

        # 处理订单关联的优惠券
        coupon = order.get_coupon()
        if coupon:
            coupon_rule = CouponRule.objects.get(id=coupon.coupon_rule_id)
            promotion = Promotion.objects.get(detail_id=coupon_rule.id, type=PROMOTION_TYPE_COUPON)
            relation = ProductHasPromotion.objects.filter(promotion_id=promotion.id)
            if len(relation) > 0:
                coupon.product_id = relation[0].product_id
        '''
        coupons = OrderHasCoupon.objects.filter(order_id=order.order_id)
        if coupons.count() > 0:
            coupon =  coupons[0]
        '''
        if order.status in [ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED]:
            order_has_delivery_times = OrderHasDeliveryTime.objects.filter(order=order, status=UNSHIPED)
            if order_has_delivery_times.count() > 0:
                tmp_time = order_has_delivery_times[0].delivery_date
                for order_has_delivery_time in order_has_delivery_times:
                    if order_has_delivery_time.delivery_date <= tmp_time:
                        tmp_time = order_has_delivery_time.delivery_date

                # 距离配送日期达到两天之内修改订单状态为代发货
                if (tmp_time - date.today()).days <= 2:
                    order.status = ORDER_STATUS_PAYED_NOT_SHIP
                    order.save()

        order.products = mall_api.get_order_products(order)

        order.area = regional_util.get_str_value_by_string_ids(order.area)
        order.belong = belong
        order.pay_interface_name = PAYTYPE2NAME.get(order.pay_interface_type, u'')
        order.total_price = mall.models.Order.get_order_has_price_number(order)
        order.save_money = float(Order.get_order_has_price_number(order)) + float(order.postage) - float(
            order.final_price) - float(order.weizoom_card_money)
        order.pay_money = order.final_price + order.weizoom_card_money

        if order.order_source:
            order.source = u'商城'
            order.come = 'weizoom_mall'
        else:
            order.source = u'本店'
            order.come = 'mine_mall'

        if belong == 'audit':
            second_nav_name = export.ORDER_AUDIT
        elif belong == 'refund':
            second_nav_name = export.ORDER_REFUND
        else:
            second_nav_name = export.ORDER_ALL
        show_first = True if OrderStatusLog.objects.filter(order_id=order.order_id,
                                                           to_status=ORDER_STATUS_PAYED_NOT_SHIP,
                                                           operator=u'客户').count() > 0 else False
        # 获取订单状态操作日志
        order_status_logs = mall_api.get_order_status_logs(order)
        log_count = len(order_status_logs)

        # 微众卡信息
        if order.weizoom_card_money:
            from market_tools.tools.weizoom_card import models as weizoom_card_model

            cardOrders = weizoom_card_model.WeizoomCardHasOrder.objects.filter(order_id=order.order_id)
            cardIds = [card.card_id for card in cardOrders]
            cards = weizoom_card_model.WeizoomCard.objects.filter(id__in=cardIds)
            order.weizoom_cards = [card.weizoom_card_id for card in cards]
        # 获得子订单
        child_orders = list(Order.objects.filter(origin_order_id=order.id).all())
        supplier_ids = []
        for child_order in child_orders:
            supplier_ids.append(child_order.supplier)

        if supplier_ids:
            # 获取<供货商，订单状态文字显示>，因为子订单的状态是跟随供货商走的 在这个场景下
            supplier2status = dict([(tmp_order.supplier, tmp_order.get_status_text()) for tmp_order in child_orders])
            order.products.sort(lambda x, y: cmp(x['supplier'], y['supplier']))
            for product in order.products:
                product['order_status'] = supplier2status.get(product['supplier'], '')

        name = request.GET.get('name',None)
        if not name:
            suppliers = list(Supplier.objects.filter(id__in=supplier_ids).order_by('-id'))
        else:
            suppliers = list(Supplier.objects.filter(id__in=supplier_ids,name__contains=name).filter(is_delete=False).order_by('-id'))

        #add by duhao 把订单操作人信息放到操作日志中，方便精选的拆单子订单能正常显示操作员信息
        order_operation_logs = mall_api.get_order_operation_logs(order.order_id)
        for log in order_operation_logs:
            log.leader_name = order.leader_name
            for child_order in child_orders:
                if child_order.order_id == log.order_id:
                    log.leader_name = child_order.leader_name

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_orders_second_navs(request),
            'second_nav_name': second_nav_name,
            'order': order,
            'child_orders': child_orders,
            'suppliers':suppliers,
            'is_order_not_payed': (order.status == ORDER_STATUS_NOT),
            'coupon': coupon,
            'order_operation_logs': order_operation_logs,
            'order_status_logs': order_status_logs,
            'log_count': log_count,
            'order_has_delivery_times': OrderHasDeliveryTime.objects.filter(order=order),
            'show_first': show_first
        })

        return render_to_response('mall/editor/order_detail.html', c)
    else:
        return HttpResponseRedirect('/mall2/order_list/')


def is_has_order(request, is_refund=False):
    webapp_id = request.user_profile.webapp_id
    # weizoom_mall_order_ids = WeizoomMallHasOtherMallProductOrder.get_order_ids_for(webapp_id)
    if is_refund:
        orders = belong_to(webapp_id)
        has_order = orders.filter(status__in=[ORDER_STATUS_REFUNDING,ORDER_STATUS_REFUNDED]).count() > 0
    else:
        has_order = (belong_to(webapp_id).count() > 0)
    MallCounter.clear_unread_order(webapp_owner_id=request.manager.id)  # 清空未读订单数量
    return has_order


def get_orders_response(request, is_refund=False):
    """

    Args:
      sort_attr: id,
      count_per_page: 15
      cur_page: 1
    """
    is_weizoom_mall_partner = AccountHasWeizoomCardPermissions.is_can_use_weizoom_card_by_owner_id(request.manager.id)
    if request.manager.is_weizoom_mall:
        is_weizoom_mall_partner = False

    # 获取查询条件字典和时间筛选条件
    query_dict, date_interval = __get_select_params(request)
    watchdog_message = "query_dict:" + json.dumps(query_dict) + ",date:" + str(date_interval)
    # 处理排序
    sort_attr = request.GET.get('sort_attr', '-id')
    if sort_attr == 'created_at':
        sort_attr = 'id'
    if sort_attr == '-created_at':
        sort_attr = '-id'

    # 分页
    count_per_page = int(request.GET.get('count_per_page', 15))
    cur_page = int(request.GET.get('page', '1'))

    # 用户
    user = request.manager
    query_string = request.META['QUERY_STRING']
    watchdog_message += ",webapp_id:" + str(request.manager.get_profile().webapp_id)
    items, pageinfo, order_total_count, order_return_count = __get_order_items(user, query_dict, sort_attr,
                                                                               query_string,
                                                                               count_per_page, cur_page,
                                                                               date_interval=date_interval,
                                                                               is_refund=is_refund)

    # 获取该用户下的所有支付方式
    existed_pay_interfaces = mall_api.get_pay_interfaces_by_user(user)

    if is_weizoom_mall_partner or request.manager.is_weizoom_mall:
        is_show_source = True
    else:
        is_show_source = False

    response = create_response(200)
    if sort_attr == 'id':
        sort_attr = 'created_at'
    if sort_attr == '-id':
        sort_attr = '-created_at'

    supplier = dict((s.id, s.name) for s in Supplier.objects.filter(owner=request.manager))
    if len(supplier.keys()) > 0:
        is_show_source = True

    show_supplier = Supplier.objects.filter(owner=request.manager, is_delete=False).count() > 0

    response.data = {
        'items': items,
        'pageinfo': paginator.to_dict(pageinfo),
        'supplier': supplier,
        'sortAttr': sort_attr,
        'is_show_source': is_show_source,
        'existed_pay_interfaces': existed_pay_interfaces,
        'order_total_count': order_total_count,
        'order_return_count': order_return_count,
        'current_status_value': query_dict['status'] if query_dict.has_key('status') else '-1',
        'is_refund': is_refund,
        'show_supplier': show_supplier
    }

    if query_dict or date_interval:
        watchdog_info(watchdog_message, type="mall")

    return response.get_response()


def get_order_status_text(status):
    return STATUS2TEXT[status]


def set_children_order_status(origin_order, status):
    Order.objects.filter(origin_order_id=origin_order.id).update(status=status)


# 页脚未读订单数统计
def get_unship_order_count(request):
    from cache.webapp_owner_cache import get_unship_order_count_from_cache
    return get_unship_order_count_from_cache(request.manager.get_profile().webapp_id)


# get_orders_response调用
def __get_order_items(user, query_dict, sort_attr, query_string, count_per_page=15, cur_page=1, date_interval=None,
                      is_refund=False):
    webapp_id = user.get_profile().webapp_id
    orders = belong_to(webapp_id)

    if is_refund:
        orders = orders.filter(status__in=[ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED])

    # 统计订单总数
    count = orders.count()
    status_not_count = orders.filter(status=ORDER_STATUS_NOT).count()
    status_payed_not_ship_total = orders.filter(status=ORDER_STATUS_PAYED_NOT_SHIP).count()
    status_payed_shiped_total = orders.filter(status=ORDER_STATUS_PAYED_SHIPED).count()
    status_cancel_count = orders.filter(status=ORDER_STATUS_CANCEL).count()
    status_successed_count = orders.filter(status=ORDER_STATUS_SUCCESSED).count()

    order_total_count = {
        'total_count': count,
        'status_not_count': status_not_count,
        'status_payed_not_ship_total': status_payed_not_ship_total,
        'status_payed_shiped_total': status_payed_shiped_total,
        'status_cancel_count': status_cancel_count,
        'status_successed_count': status_successed_count
    }

    # 处理排序
    if sort_attr != 'created_at':
        orders = orders.order_by(sort_attr)

    orders = __get_orders_by_params(query_dict, date_interval, orders)

    # 返回订单的数目
    order_return_count = orders.count()
    ###################################################
    if count_per_page > 0:
        # 进行分页
        pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page, query_string=query_string)
    else:
        # 全部订单
        pageinfo = {"object_count": order_return_count}

        # 获取order对应的会员
    webapp_user_ids = set([order.webapp_user_id for order in orders])
    from modules.member.models import Member
    webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

    # 获得order对应的商品数量
    order_ids = [order.id for order in orders]

    order2productcount = {}
    for relation in OrderHasProduct.objects.filter(order_id__in=order_ids).order_by('id'):
        order_id = relation.order_id
        if order_id in order2productcount:
            order2productcount[order_id] = order2productcount[order_id] + 1
        else:
            order2productcount[order_id] = 1

    # 微众精选子订单
    order2fackorders = {}
    fackorders = Order.objects.filter(origin_order_id__in=order_ids)
    for order in fackorders:
        origin_order_id = order.origin_order_id
        # order_supplier = order.supplier
        order2fackorders.setdefault(origin_order_id, [])
        # order2fackorders[origin_order_id].setdefault(order_supplier, {})
        order2fackorders[origin_order_id].append(order)

    # 构造返回的order数据
    items = []
    for order in orders:
        # 获取order对应的member的显示名
        member = webappuser2member.get(order.webapp_user_id, None)
        if member:
            order.buyer_name = member.username_for_html
            order.member_id = member.id
        else:
            order.buyer_name = u'未知'
            order.member_id = 0

        if order.payment_time is None:
            payment_time = ''
        elif datetime.strftime(order.payment_time, '%Y-%m-%d %H:%M:%S') == DEFAULT_CREATE_TIME:
            payment_time = ''
        else:
            payment_time = datetime.strftime(order.payment_time, '%Y-%m-%d %H:%M:%S')

        if order.order_source:
            order.come = 'weizoom_mall'
        else:
            order.come = 'mine_mall'

        order.status_text = get_order_status_text(order.status)
        order.product_count = order2productcount.get(order.id, 0)
        order.payment_time = payment_time
        if order.pay_interface_type == 3:
            order.pay_interface_type_text = PAYTYPE2NAME.get(10, u'')
        else:
            order.pay_interface_type_text = PAYTYPE2NAME.get(order.pay_interface_type, u'')

        if order.come is 'weizoom_mall' and user.is_weizoom_mall is False:
            order.member_id = 0

            # 构造返回的order数据
    items = []

    for order in orders:
        products = mall_api.get_order_products(order)

        # 用于微众精选拆单
        groups = []
        if order2fackorders.get(order.id) and order.status > ORDER_STATUS_CANCEL:
            # 需要拆单
            for fackorder in sorted(order2fackorders.get(order.id),key = lambda obj:obj.supplier):
                if fackorder.status == ORDER_STATUS_NOT:
                    # 处理子订单未支付的问题
                    fackorder.status = ORDER_STATUS_PAYED_NOT_SHIP
                    fackorder.save()
                group_order = {
                    "id": fackorder.id,
                    "status": fackorder.get_status_text(),
                    "order_status": fackorder.status,
                    'express_company_name': fackorder.express_company_name,
                    'express_number': fackorder.express_number,
                    'leader_name': fackorder.leader_name,
                }
                group = {
                    "id": fackorder.supplier,
                    "fackorder": group_order,
                    "products": filter(lambda p: p['supplier'] == fackorder.supplier , products)
                }
                groups.append(group)
        else:
            group_order = {
                "id": order.id,
                "status": order.get_status_text(),
                "order_status": order.status,
                'express_company_name': order.express_company_name,
                'express_number': order.express_number,
                'leader_name': order.leader_name,
            }

            group_id = order.supplier
            group = {
                "id": group_id,
                "fackorder": group_order,
                "products": products
            }
            groups.append(group)

        items.append({
            'id': order.id,
            'order_id': order.order_id,
            'status': order.get_status_text(),
            'total_price': float(
                '%.2f' % order.final_price) if order.pay_interface_type != 9 or order.status == 5 else 0,
            'order_total_price': float('%.2f' % order.get_total_price()),
            'ship_name': order.ship_name,
            'ship_address': '%s %s' % (regional_util.get_str_value_by_string_ids(order.area), order.ship_address),
            'ship_tel': order.ship_tel,
            'bill_type': order.bill_type,
            'bill': order.bill,
            'customer_message': order.customer_message,
            'buyer_name': order.buyer_name,
            'pay_interface_name': order.pay_interface_type_text,
            'created_at': datetime.strftime(order.created_at, '%Y-%m-%d %H:%M:%S'),
            'product_count': order.product_count,
            'payment_time': order.payment_time,
            'come': order.come,
            'member_id': order.member_id,
            'type': order.type,
            'webapp_id': order.webapp_id,
            'integral': order.integral,
            'pay_interface_type': order.pay_interface_type,
            'order_status': order.status,
            'express_company_name': order.express_company_name,
            'express_number': order.express_number,
            'leader_name': order.leader_name,
            'remark': order.remark,
            'postage': '%.2f' % order.postage,
            'save_money': float(Order.get_order_has_price_number(order)) + float(order.postage) - float(
                order.final_price) - float(order.weizoom_card_money),
            'weizoom_card_money': float('%.2f' % order.weizoom_card_money),
            'pay_money': '%.2f' % (order.final_price + order.weizoom_card_money),
            'edit_money': str(order.edit_money).replace('.', '').replace('-', '') if order.edit_money else False,
            'groups': groups,
        })
    return items, pageinfo, order_total_count, order_return_count


def __get_select_params(request):
    """
    构造查询条件
    """
    query = request.GET.get('query', '').strip()
    ship_name = request.GET.get('ship_name', '').strip()
    ship_tel = request.GET.get('ship_tel', '').strip()
    product_name = request.GET.get('product_name', '').strip()
    pay_type = request.GET.get('pay_type', '').strip()
    express_number = request.GET.get('express_number', '').strip()
    order_source = request.GET.get('order_source', '').strip()
    order_status = request.GET.get('order_status', '').strip()
    isUseWeizoomCard = int(request.GET.get('isUseWeizoomCard', '0').strip())

    # 填充query
    query_dict = dict()
    if len(query):
        query_dict['order_id'] = query.strip().split('-')[0]
    if len(ship_name):
        query_dict['ship_name'] = ship_name
    if len(ship_tel):
        query_dict['ship_tel'] = ship_tel
    if len(express_number):
        query_dict['express_number'] = express_number
    if len(product_name):
        query_dict['product_name'] = product_name
    if len(pay_type):
        query_dict['pay_interface_type'] = int(pay_type)
    if len(order_source):
        query_dict['order_source'] = int(order_source)
    if len(order_status) and order_status != '-1':
        query_dict['status'] = int(order_status)
    if isUseWeizoomCard:
        query_dict['isUseWeizoomCard'] = isUseWeizoomCard


    # 时间区间
    try:
        date_interval = request.GET.get('date_interval', '')
        if date_interval:
            date_interval = date_interval.split('|')
            if " " in date_interval[0]:
                date_interval[0] = date_interval[0] + ':00'
            else:
                date_interval[0] = date_interval[0] + ' 00:00:00'

            if " " in date_interval[1]:
                date_interval[1] = date_interval[1] + ':59'
            else:
                date_interval[1] = date_interval[1] + ' 23:59:59'
        else:
            date_interval = None
    except:
        date_interval = None

    return query_dict, date_interval


def __get_orders_by_params(query_dict, date_interval, orders):
    """
    按照查询条件筛选符合条件的订单
    """
    # 商品名称
    if query_dict.get("product_name"):
        product_name = query_dict["product_name"]
        query_dict.pop("product_name")

        product_list = Product.objects.filter(name__contains=product_name)
        product_ids = [product.id for product in product_list]

        orderHasProduct_list = OrderHasProduct.objects.filter(product_id__in=product_ids)

        order_ids = [orderHasProduct.order_id for orderHasProduct in orderHasProduct_list]

        orderHasPromotions = OrderHasPromotion.objects.filter(promotion_type="premium_sale")

        for orderHasPromotion in orderHasPromotions:
            for premium_product in orderHasPromotion.promotion_result.get('premium_products', []):
                if premium_product['id'] in product_ids and orderHasPromotion.order_id not in order_ids:
                    order_ids.append(orderHasPromotion.order_id)

        orders = orders.filter(id__in=order_ids)

        # 处理搜索
    print '----------------query_dict:',query_dict
    if len(query_dict):
        if query_dict.get("isUseWeizoomCard"):
            query_dict.pop("isUseWeizoomCard")
            orders = orders.exclude(weizoom_card_money=0)
        orders = orders.filter(**query_dict)

        # 处理 时间区间筛选
    if date_interval:
        start_time = date_interval[0]
        end_time = date_interval[1]
        orders = orders.filter(created_at__gte=start_time, created_at__lt=end_time)

    return orders



# 渠道扫描相关
@api(app='mall', resource='channel_qrcode_payed_orders', action='get')
def get_channel_qrcode_payed_orders(request):
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
    pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

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
            'status': get_order_status_text(order.status),
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

    # #===============================================================================
    # # get_thanks_card_orders : 获得感恩贺卡类型的订单列表
    # #===============================================================================
    # def get_thanks_card_orders(request):
    # 	webapp_id = request.manager.get_profile().webapp_id
    #
    # 	orders = None
    # 	secret = request.GET.get('secret')
    # 	if secret:
    # 		filter_ids = []
    # 		thanks_card_orders = ThanksCardOrder.objects.filter(thanks_secret=secret)
    # 		for thanks_card_order in thanks_card_orders:
    # 			filter_ids.append(thanks_card_order.order_id)
    # 		orders = Order.objects.filter(webapp_id=webapp_id, type=THANKS_CARD_ORDER, id__in=filter_ids)
    # 	else:
    # 		orders = Order.objects.filter(webapp_id=webapp_id, type=THANKS_CARD_ORDER)
    #
    # 	#处理搜索
    # 	query = request.GET.get('query', None)
    # 	if query:
    # 		orders = orders.filter(order_id=query)
    # 	#处理过滤
    # 	filter_attr = request.GET.get('filter_attr', None)
    # 	filter_value = int(request.GET.get('filter_value', -1))
    # 	if filter_attr and (filter_value != -1):
    # 		params = {filter_attr: filter_value}
    # 		orders = orders.filter(**params)
    # 	#处理排序
    # 	sort_attr = request.GET.get('sort_attr', 'created_at');
    # 	if sort_attr != 'created_at':
    # 		orders = orders.order_by(sort_attr)
    #
    # 	#进行分页
    # 	count_per_page = int(request.GET.get('count_per_page', 15))
    # 	cur_page = int(request.GET.get('page', '1'))
    # 	pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
    #
    # 	#构造返回的order数据
    # 	items = []
    # 	today = datetime.today()
    # 	for order in  orders:
    # 		payment_time = None
    # 		if order.payment_time is None:
    # 			payment_time = ''
    # 		elif datetime.strftime(order.payment_time, '%Y-%m-%d %H:%M:%S') == DEFAULT_CREATE_TIME:
    # 			payment_time = ''
    # 		else:
    # 			payment_time = datetime.strftime(order.payment_time, '%m-%d %H:%M')
    #
    # 		#感恩贺卡信息
    # 		thanks_secret_count = 0 	#感恩密码数量
    # 		card_count = 0 	#贺卡生成个数
    # 		listen_count = 0 	#贺卡收听次数
    # 		thanks_card_orders = ThanksCardOrder.objects.filter(order_id=order.id)
    # 		for thanks_card_order in thanks_card_orders:
    # 			if thanks_card_order.thanks_secret is not '':
    # 				thanks_secret_count += 1
    # 			card_count += thanks_card_order.card_count
    # 			listen_count += thanks_card_order.listen_count
    #
    # 		items.append({
    # 			'id': order.id,
    # 			'order_id': order.order_id,
    # 			'status': get_order_status_text(order.status),
    # 			'payment_time': payment_time,
    # 			'thanks_secret_count': thanks_secret_count,
    # 			'card_count': card_count,
    # 			'listen_count': listen_count
    # 		})
    #
    # 	response = create_response(200)
    # 	response.data = {
    # 		'items': items,
    # 		'pageinfo': paginator.to_dict(pageinfo),
    # 		'sortAttr': sort_attr
    # 	}
    # 	return response.get_response()
    # #######################
    #
    # ########################################################################
    # # # _get_order_products: 获得订单中的商品列表
    # # # 疑似废弃
    # # ########################################################################
    # # def _get_order_products(order_id):
    # # 	relations = list(OrderHasProduct.objects.filter(order_id=order_id))
    # # 	product_ids = [r.product_id for r in relations]
    # # 	id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])
    # #
    # # 	products = []
    # # 	for relation in OrderHasProduct.objects.filter(order_id=order_id):
    # # 		product = copy.copy(id2product[relation.product_id])
    # # 		product.fill_specific_model(relation.product_model_name)
    # # 		products.append({
    # # 			'name': product.name,
    # # 			'thumbnails_url': product.thumbnails_url,
    # # 			'count': relation.number,
    # # 			'total_price': '%.2f' % relation.total_price,
    # # 			'custom_model_properties': product.custom_model_properties
    # # 		})
    # #
    # # 	return products
    # #
    # # # 疑似废弃
    # # def _get_status_value(filter_value):
    # # 	if filter_value == '-1':
    # # 		return -1
    # # 	try:
    # # 		for item in filter_value.split('|'):
    # # 			if item.split(':')[0] == 'status':
    # # 				return int(item.split(':')[1])
    # # 		return -1
    # # 	except:
    # # 		return -1
    #
    #
    # # ########################################################################
    # # # add_express_info: 增加物流信息
    # # # 疑似废弃
    # # ########################################################################
    # # @login_required
    # # def add_express_info(request):
    # # 	order_id = request.GET['order_id']
    # # 	express_company_name = request.GET['express_company_name']
    # # 	express_number = request.GET['express_number']
    # # 	leader_name = request.GET['leader_name']
    # # 	is_update_express = request.GET['is_update_express']
    # # 	is_update_express = True if is_update_express == 'true' else False
    # # 	mall_api.ship_order(order_id, express_company_name, express_number, request.manager.username, leader_name=leader_name, is_update_express=is_update_express)
    # #
    # # 	return HttpResponseRedirect('/mall/editor/order/get/?order_id=%s' %order_id)
