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
from modules.member.models import Member, WebAppUser, MemberFollowRelation, SOURCE_SELF_SUB, SOURCE_MEMBER_QRCODE, SOURCE_BY_URL
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
from mall.templatetags.mall_filter import *
from weixin.user.module_api import get_all_active_mp_user_ids
from account.models import UserProfile

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
         u'商品单价', u'商品数量', u'销售额', u'商品总重量（斤）', u'支付方式', u'支付金额',
         u'现金支付金额', u'微众卡支付金额', u'运费', u'积分抵扣金额', u'优惠券金额',
         u'优惠券名称', u'订单状态', u'购买人', u'收货人', u'联系电话', u'收货地址省份',
         u'收货地址', u'发货人', u'发货人备注', u'来源' ,u'物流公司', u'快递单号',
         u'发货时间',u'商家备注',u'用户备注', u'买家来源', u'买家推荐人', u'是否老用户']
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
    query_dict, date_interval,date_interval_type = __get_select_params(request)
    product_name = ''
    if query_dict.get("product_name"):
        product_name = query_dict["product_name"]

    order_list = __get_orders_by_params(query_dict, date_interval, date_interval_type, order_list)

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

    if webappuser2member:
        # 构造会员与推荐人或者带参数二维码的关系
        members = webappuser2member.values()
        member_self_sub, member_qrcode_and_by_url = [], []
        follow_member_ids = []
        all_member_ids = []
        for member in members:
            if member:
                all_member_ids.append(member.id)
                if member.source == SOURCE_SELF_SUB:
                    member_self_sub.append(member)
                elif member.source in [SOURCE_MEMBER_QRCODE, SOURCE_BY_URL]:
                    member_qrcode_and_by_url.append(member)
                    follow_member_ids.append(member.id)

        follow_member2father_member = dict([(relation.follower_member_id, relation.member_id) for relation in MemberFollowRelation.objects.filter(follower_member_id__in=follow_member_ids, is_fans=True)])
        father_member_ids = follow_member2father_member.values()
        father_member_id2member = dict([(m.id, m) for m in Member.objects.filter(id__in=father_member_ids)])

        member_id2qrcode = dict([(relation.member_id, relation) for relation in ChannelQrcodeHasMember.objects.filter(member_id__in=all_member_ids)])

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
                    'id': premium_product.get('id', ""),
                    'name': premium_product.get('name', ""),
                    'count': premium_product.get('count', ""),
                    'price': premium_product.get('price', ""),
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
        if webappuser2member:
            member = webappuser2member.get(order.webapp_user_id, None)
        else:
            member = None
        if member:
            order.buyer_name = handle_member_nickname(member.username_for_html)
            order.member_id = member.id
        else:
            order.buyer_name = u'未知'

        # 根据用户来源获取用户推荐人或者带参数二维码的名称
        father_name_or_qrcode_name = ""
        member_source_name = ""
        before_scanner_qrcode_is_member = ""
        SOURCE_SELF_SUB, SOURCE_MEMBER_QRCODE, SOURCE_BY_URL
        if member:
            if member.id in member_id2qrcode.keys():
                if member_id2qrcode[member.id].created_at < order.created_at:
                    member_source_name = "带参数二维码"
                    father_name_or_qrcode_name = member_id2qrcode[member.id].channel_qrcode.name
                    if member_id2qrcode[member.id].is_new:
                        before_scanner_qrcode_is_member = "否"
                    else:
                        before_scanner_qrcode_is_member = "是"
                else:
                    if member.source == SOURCE_SELF_SUB:
                        member_source_name = "直接关注"
                    elif member.source == SOURCE_MEMBER_QRCODE:
                        member_source_name = "推广扫码"
                        try:
                            father_name_or_qrcode_name = father_member_id2member[follow_member2father_member[member.id]].username_for_html
                        except KeyError:
                            father_name_or_qrcode_name = ""
                    elif member.source == SOURCE_BY_URL:
                        member_source_name = "会员分享"
                        try:
                            father_name_or_qrcode_name = father_member_id2member[follow_member2father_member[member.id]].username_for_html
                        except KeyError:
                            father_name_or_qrcode_name = ""
            else:
                if member.source == SOURCE_SELF_SUB:
                    member_source_name = "直接关注"
                elif member.source == SOURCE_MEMBER_QRCODE:
                    member_source_name = "推广扫码"
                    try:
                        father_name_or_qrcode_name = father_member_id2member[follow_member2father_member[member.id]].username_for_html
                    except KeyError:
                        father_name_or_qrcode_name = ""
                elif member.source == SOURCE_BY_URL:
                    member_source_name = "会员分享"
                    try:
                        father_name_or_qrcode_name = father_member_id2member[follow_member2father_member[member.id]].username_for_html
                    except KeyError:
                        father_name_or_qrcode_name = ""
        #----------end---------

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
            if fackorder and 0 != fackorder.supplier and order2supplier.has_key(fackorder.supplier):
                source = order2supplier[fackorder.supplier].name.encode("utf-8")
            elif fackorder == None and 0 != order.supplier:
                if order2supplier.has_key(order.supplier):
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
                    u'' if order.customer_message == '' else order.customer_message.encode('utf-8'),
                    member_source_name,
                    father_name_or_qrcode_name,
                    before_scanner_qrcode_is_member

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
                    u'',
                    member_source_name,
                    father_name_or_qrcode_name,
                    before_scanner_qrcode_is_member

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
                        u'',
                        member_source_name,
                        father_name_or_qrcode_name,
                        before_scanner_qrcode_is_member
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


def get_detail_response(request):
    # 没有订单号参数直接返回订单列表页
    if not request.GET.get('order_id', None):
        return HttpResponseRedirect('/mall2/order_list/')
    else:
        order = mall.models.Order.objects.get(id=request.GET['order_id'])

    if request.method == 'GET':
        mall_type = request.user_profile.webapp_type
        order_has_products = OrderHasProduct.objects.filter(order=order)

        number = 0
        for order_has_product in order_has_products:
            number += order_has_product.number
        order.number = number
        order.products = mall_api.get_order_products(order)

        # 如果有单品积分抵扣，则不显示整单的积分抵扣数额
        for product in order.products:
            if 'integral_count' in product and product['integral_count'] > 0:
                order.integral = None

        # 处理订单关联的优惠券
        coupon = order.get_coupon()
        if coupon:
            coupon_rule = CouponRule.objects.get(id=coupon.coupon_rule_id)
            promotion = Promotion.objects.get(detail_id=coupon_rule.id, type=PROMOTION_TYPE_COUPON)
            relation = ProductHasPromotion.objects.filter(promotion_id=promotion.id)
            if len(relation) > 0:
                coupon.product_id = relation[0].product_id
            else:
                coupon.product_id = -1  # 通用券标志

            for product in order.products:
                if coupon.product_id == product['id']:
                    product['has_coupon'] = True
                    print(product['id'], product['has_coupon'])
                    break

        order.area = regional_util.get_str_value_by_string_ids(order.area)
        order.pay_interface_name = PAYTYPE2NAME.get(order.pay_interface_type, u'')
        order.total_price = mall.models.Order.get_order_has_price_number(order)
        order.save_money = float(Order.get_order_has_price_number(order)) + float(order.postage) - float(
            order.final_price) - float(order.weizoom_card_money)
        order.pay_money = order.final_price + order.weizoom_card_money
        order.actions = get_order_actions(order, is_detail_page=True)

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
        supplier_user_ids = []
        for child_order in child_orders:
            if child_order.supplier:
                supplier_ids.append(child_order.supplier)
            if child_order.supplier_user_id:
                supplier_user_ids.append(child_order.supplier_user_id)

        # 商城自己添加的供货商
        if supplier_ids:
            # 获取<供货商，订单状态文字显示>，因为子订单的状态是跟随供货商走的 在这个场景下
            supplier2status = dict([(tmp_order.supplier, tmp_order.get_status_text()) for tmp_order in child_orders])
            order.products.sort(lambda x, y: cmp(x['supplier'], y['supplier']))
            for product in order.products:
                product['order_status'] = supplier2status.get(product['supplier'], '')

        if supplier_user_ids:
            # 获取<供货商，订单状态文字显示>，因为子订单的状态是跟随供货商走的 在这个场景下
            supplier_user_id2status = dict([(tmp_order.supplier_user_id, tmp_order.get_status_text()) for tmp_order in child_orders])
            order.products.sort(lambda x, y: cmp(x['supplier_user_id'], y['supplier_user_id']))
            for product in order.products:
                product['order_status'] = supplier_user_id2status.get(product['supplier_user_id'], '')

        name = request.GET.get('name', None)
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
            'second_navs': export.get_mall_order_second_navs(request),
            'second_nav_name': export.ORDER_ALL,
            'mall_type': mall_type,
            'order': order,
            'child_orders': child_orders,
            'suppliers': suppliers,
            'is_order_not_payed': (order.status == ORDER_STATUS_NOT),
            'coupon': coupon,
            'order_operation_logs': order_operation_logs,
            'order_status_logs': order_status_logs,
            'log_count': log_count,
            'show_first': show_first,
            'is_sync': True if (not request.user_profile.webapp_type and order.supplier_user_id > 0) else False,
            'is_show_order_status': True if len(supplier_ids) + len(supplier_user_ids) > 1 else False
            })

        return render_to_response('mall/editor/order_detail.html', c)
    else:
        return HttpResponseRedirect('/mall2/order_list/')


def is_has_order(request, is_refund=False):
    webapp_id = request.user_profile.webapp_id
    user_id = request.user_profile.user.id
    mall_type = request.user_profile.webapp_type
    # weizoom_mall_order_ids = WeizoomMallHasOtherMallProductOrder.get_order_ids_for(webapp_id)
    if is_refund:
        orders = belong_to(webapp_id)
        has_order = orders.filter(status__in=[ORDER_STATUS_REFUNDING,ORDER_STATUS_REFUNDED]).count() > 0
    else:
        has_order = (belong_to(webapp_id, user_id, mall_type).count() > 0)
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

    # 商城的类型
    mall_type = request.user_profile.webapp_type

    # 获取查询条件字典和时间筛选条件
    query_dict, date_interval, date_interval_type = __get_select_params(request)
    watchdog_message = "query_dict:" + json.dumps(query_dict) + ",date:" + str(date_interval) + ",date_type" \
                       + str(date_interval_type)
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
    items, pageinfo, order_return_count = __get_order_items(user, query_dict, sort_attr,
                                                                               date_interval_type,
                                                                               query_string,
                                                                               count_per_page, cur_page,
                                                                               date_interval=date_interval,
                                                                               is_refund=is_refund)
    # 获取该用户下的所有支付方式
    existed_pay_interfaces = mall_api.get_pay_interfaces_by_user(user)
    supplier = dict((supplier.id, supplier.name) for supplier in Supplier.objects.filter(owner=request.manager))

    #
    all_user_ids = get_all_active_mp_user_ids()
    all_mall_userprofiles = UserProfile.objects.filter(user_id__in=all_user_ids, webapp_type=0)
    supplier_users = dict([(profile.user_id, profile.store_name) for profile in all_mall_userprofiles])

    response = create_response(200)
    response.data = {
        'items': items,
        'pageinfo': paginator.to_dict(pageinfo),
        'supplier': supplier,
        'supplier_users': supplier_users,
        'sortAttr': sort_attr,
        'existed_pay_interfaces': existed_pay_interfaces,
        'order_return_count': order_return_count,
        'current_status_value': query_dict['status'] if query_dict.has_key('status') else '-1',
        'is_refund': is_refund,
        'mall_type': mall_type
    }

    if query_dict or date_interval:
        watchdog_info(watchdog_message, type="mall")

    return response.get_response()


def check_order_status_filter(order,action):
        """
            检查订单的状态是否允许跳转
        """
        flag = False
        is_refund = True if action == 'return_success' else False
        actions = get_order_actions(order, is_refund=is_refund)
        for ac in actions:
            if action == ac['action']:
                flag = True
        return flag


def get_order_status_text(status):
    return STATUS2TEXT[status]

def set_children_order_status(origin_order, status):
    Order.objects.filter(origin_order_id=origin_order.id).update(status=status)

# 页脚未读订单数统计
def get_unship_order_count(request):
    from cache.webapp_owner_cache import get_unship_order_count_from_cache
    return get_unship_order_count_from_cache(request.manager.get_profile().webapp_id)


# get_orders_response调用
def __get_order_items(user, query_dict, sort_attr, date_interval_type,query_string,  count_per_page=15, cur_page=1, date_interval=None,
                      is_refund=False):
    webapp_id = user.get_profile().webapp_id
    mall_type = user.get_profile().webapp_type
    orders = belong_to(webapp_id, user.id, mall_type)

    if is_refund:
        orders = orders.filter(status__in=[ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED])

    # 处理排序
    if sort_attr != 'created_at':
        orders = orders.order_by(sort_attr)

    # 除掉同步过来的订单中未支付的
    if not mall_type:
        orders = orders.exclude(supplier_user_id__gt=0, status=ORDER_STATUS_NOT)

    orders = __get_orders_by_params(query_dict, date_interval, date_interval_type, orders)

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

    # 微众系列子订单
    order2fackorders = {}
    fackorders = Order.objects.filter(origin_order_id__in=order_ids)
    for order in fackorders:
        origin_order_id = order.origin_order_id
        # order_supplier = order.supplier
        order2fackorders.setdefault(origin_order_id, [])
        # order2fackorders[origin_order_id].setdefault(order_supplier, {})
        order2fackorders[origin_order_id].append(order)

    # 供货商同步的订单
    sync_orders = Order.objects.filter(supplier_user_id=user.id)
    sync_order_ids = [order.id for order in sync_orders]
    sync_order_id2sync_product_id = dict([(relation.order_id, relation.product_id)for relation in OrderHasProduct.objects.filter(order_id__in=sync_order_ids)])
    sync_product_ids = sync_order_id2sync_product_id.values()
    weizoom_product_id2mall_product_id = dict([(relation.weizoom_product_id, relation.mall_product_id) for relation in WeizoomHasMallProductRelation.objects.filter(weizoom_product_id__in=sync_product_ids)])
    id2mall_product = dict([(product.id, product)for product in Product.objects.filter(id__in=weizoom_product_id2mall_product_id.values())])

    # 构造返回的order数据
    for order in orders:
        # 获取order对应的member的显示名
        member = webappuser2member.get(order.webapp_user_id, None)
        if member:
            order.buyer_name = member.username_for_html
            order.member_id = member.id
            order.member_is_subscribed = member.is_subscribed
        else:
            order.buyer_name = u'未知'
            order.member_id = 0
            order.member_is_subscribed = 0

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
        order.is_refund = is_refund
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
                    'actions': get_order_actions(fackorder, is_refund=is_refund)
                }
                if fackorder.supplier or (not fackorder.supplier and not fackorder.supplier_user_id):
                    group = {
                        "id": fackorder.supplier,
                        "fackorder": group_order,
                        "products": filter(lambda p: p['supplier'] == fackorder.supplier , products)
                    }
                if fackorder.supplier_user_id:
                    group = {
                        "supplier_user_id": fackorder.supplier_user_id,
                        "fackorder": group_order,
                        "products": filter(lambda p: p['supplier_user_id'] == fackorder.supplier_user_id , products)
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
                'actions': get_order_actions(order, is_refund=is_refund)
            }

            if order.supplier_user_id > 0:
                group_id = order.supplier_user_id
                pay_money = 0
                for product in products:
                    try:
                        product['name'] = id2mall_product[weizoom_product_id2mall_product_id[product['id']]].name
                    except:
                        pass
                    pay_money += float(product['total_price'])
                group = {
                    "supplier_user_id": group_id,
                    "fackorder": group_order,
                    "products": products
                }
            else:
                group_id = order.supplier
                group = {
                    "id": group_id,
                    "fackorder": group_order,
                    "products": products
                }
            groups.append(group)
        if len(groups) > 1:
            parent_action = get_order_actions(order, is_refund=is_refund,is_list_parent=True)
        else:
            parent_action = None
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
            'member_is_subscribed': order.member_is_subscribed,
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
            'delivery_time': order.delivery_time,
            'save_money': float(Order.get_order_has_price_number(order)) + float(order.postage) - float(
                order.final_price) - float(order.weizoom_card_money),
            'weizoom_card_money': float('%.2f' % order.weizoom_card_money),
            'pay_money': pay_money if order.supplier_user_id > 0 else '%.2f' % (order.final_price + order.weizoom_card_money),
            'edit_money': str(order.edit_money).replace('.', '').replace('-', '') if order.edit_money else False,
            'groups': groups,
            'parent_action': parent_action,
            'is_first_order': order.is_first_order,
            'supplier_user_id': order.supplier_user_id
        })

    return items, pageinfo, order_return_count


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
    date_interval_type = request.GET.get('date_interval_type', '')
    is_first_order = request.GET.get('order_type', '').strip()

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
    if len(is_first_order) and is_first_order != '-1':
        query_dict['is_first_order'] = int(is_first_order)

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

    return query_dict, date_interval, date_interval_type

def __get_orders_by_params(query_dict, date_interval, date_interval_type, orders):
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

    if query_dict.get("isUseWeizoomCard"):
        query_dict.pop("isUseWeizoomCard")
        orders = orders.exclude(weizoom_card_money=0)
    if len(query_dict):
        orders = orders.filter(**query_dict)

    # 处理 时间区间筛选
    if date_interval:
        start_time = date_interval[0]
        end_time = date_interval[1]
        # 1 下单时间，2 付款时间， 3 发货时间
        if '1' == date_interval_type:
            orders = orders.filter(created_at__gte=start_time, created_at__lt=end_time)
        elif '2' == date_interval_type:
            orders = orders.filter(payment_time__gte=start_time, payment_time__lt=end_time)
        elif '3' == date_interval_type:
            order_ids_in_delivery_intervale = [operationlog.order_id for operationlog in list(OrderOperationLog.objects.filter(created_at__gte=start_time,created_at__lt=end_time,action__startswith="订单发货"))]
            order_ids_in_delivery_intervale = [de.split("^")[0] for de in order_ids_in_delivery_intervale]
            orders = orders.filter(order_id__in=order_ids_in_delivery_intervale)
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


ORDER_PAY_ACTION = {
    'name': u'支付',
    'action': 'pay',
    'class_name': 'xa-pay',
    'button_class': 'btn-success'
}
ORDER_SHIP_ACTION = {
    'name': u'发货',
    'action': 'ship',
    'class_name': 'xa-order-delivery',
    'button_class': 'btn-danger'
}
ORDER_FINISH_ACTION = {
    'name': u'标记完成',
    'action': 'finish',
    'class_name': 'xa-finish',
    'button_class': 'btn-success'
}
ORDER_CANCEL_ACTION = {
    'name': u'取消订单',
    'action': 'cancel',
    'class_name': 'xa-cancelOrder',
    'button_class': 'btn-danger'
}
ORDER_REFUNDIND_ACTION = {
    'name': u'申请退款',
    'action': 'return_pay',
    'class_name': 'xa-refund',
    'button_class': 'btn-danger'
}
ORDER_UPDATE_PRICE_ACTION = {
    'name': u'修改价格',
    'action': 'update_price',
    'class_name': 'xa-update-price',
    'button_class': 'btn-danger'
}
ORDER_UPDATE_EXPREDSS_ACTION = {
    'name': u'修改物流',
    'action': 'update_express',
    'class_name': 'xa-order-delivery',
    'button_class': 'btn-danger'
}
ORDER_REFUND_SUCCESS_ACTION = {
    'name': u'退款成功',
    'action': 'return_success',
    'class_name': 'xa-refundSuccess',
    'button_class': 'btn-danger'
}





def get_order_actions(order, is_refund=False, is_detail_page=False,is_list_parent=False):

    """
    :param order:
    :param is_refund:
    :param is_detail_page:
    :return:
    所有action:
    ORDER_PAY_ACTION
    ORDER_SHIP_ACTION
    ORDER_FINISH_ACTION
    ORDER_CANCEL_ACTION
    ORDER_REFUNDIND_ACTION
    ORDER_UPDATE_PRICE_ACTION
    ORDER_UPDATE_EXPREDSS_ACTION
    ORDER_REFUND_SUCCESS_ACTION
    """

    result = []
    if not is_refund:
        if order.status == ORDER_STATUS_NOT:
            result = [ORDER_PAY_ACTION, ORDER_UPDATE_PRICE_ACTION, ORDER_CANCEL_ACTION]
        elif order.status == ORDER_STATUS_PAYED_NOT_SHIP:
            if order.pay_interface_type in [PAY_INTERFACE_ALIPAY, PAY_INTERFACE_TENPAY, PAY_INTERFACE_WEIXIN_PAY]:
                    result = [ORDER_SHIP_ACTION, ORDER_REFUNDIND_ACTION]
            else:
                    result = [ORDER_SHIP_ACTION, ORDER_CANCEL_ACTION]
        elif order.status == ORDER_STATUS_PAYED_SHIPED:
            actions = []
            if order.pay_interface_type in [PAY_INTERFACE_ALIPAY, PAY_INTERFACE_TENPAY, PAY_INTERFACE_WEIXIN_PAY]:
                if order.express_company_name:
                    actions = [ORDER_FINISH_ACTION, ORDER_UPDATE_EXPREDSS_ACTION, ORDER_REFUNDIND_ACTION]
                else:
                    actions = [ORDER_FINISH_ACTION, ORDER_REFUNDIND_ACTION]
            else:
                if order.express_company_name:
                    actions = [ORDER_FINISH_ACTION, ORDER_UPDATE_EXPREDSS_ACTION, ORDER_CANCEL_ACTION]
                else:
                    actions = [ORDER_FINISH_ACTION, ORDER_CANCEL_ACTION]
            result = actions
        elif order.status == ORDER_STATUS_PAYED_NOT_SHIP:
            if order.pay_interface_type in [PAY_INTERFACE_ALIPAY, PAY_INTERFACE_TENPAY, PAY_INTERFACE_WEIXIN_PAY]:
                if order.express_company_name:
                    result = [ORDER_REFUNDIND_ACTION, ORDER_UPDATE_EXPREDSS_ACTION]
                else:
                    result = [ORDER_REFUNDIND_ACTION]
            else:
                result = [ORDER_SHIP_ACTION, ORDER_CANCEL_ACTION]
        elif order.status == ORDER_STATUS_SUCCESSED:
            if order.pay_interface_type in [PAY_INTERFACE_ALIPAY, PAY_INTERFACE_TENPAY, PAY_INTERFACE_WEIXIN_PAY,
                                            PAY_INTERFACE_COD]:
                result = [ORDER_REFUNDIND_ACTION]
            else:
                result = [ORDER_CANCEL_ACTION]
    elif is_refund:
        if order.status == ORDER_STATUS_REFUNDING:
            result = [ORDER_REFUND_SUCCESS_ACTION]

    # 订单列表页子订单
    able_actions_for_sub_order = [ORDER_SHIP_ACTION, ORDER_UPDATE_EXPREDSS_ACTION, ORDER_FINISH_ACTION]

    # 订单详情页有子订单
    able_actions_for_detail_order_has_sub = [ORDER_PAY_ACTION, ORDER_CANCEL_ACTION, ORDER_REFUNDIND_ACTION,
                                             ORDER_UPDATE_PRICE_ACTION]

    # 订单列表页有子订单的父母订单
    able_actions_for_list_parent = [ORDER_CANCEL_ACTION, ORDER_REFUNDIND_ACTION, ORDER_REFUND_SUCCESS_ACTION]

    # 同步订单操作
    sync_order_actions = [ORDER_PAY_ACTION, ORDER_UPDATE_PRICE_ACTION, ORDER_SHIP_ACTION, ORDER_UPDATE_EXPREDSS_ACTION, ORDER_FINISH_ACTION]

    # print(order.order_id, order.is_sub_order, order.origin_order_id)
    # print(result)
    if order.supplier_user_id > 0:
        result = filter(lambda x: x in sync_order_actions, result)
    else:
        if order.is_sub_order:
            result = filter(lambda x: x in able_actions_for_sub_order, result)

    if order.has_sub_order and is_detail_page:
        result = filter(lambda x: x in able_actions_for_detail_order_has_sub, result)

    if is_list_parent:
        result = filter(lambda x: x in able_actions_for_list_parent, result)
    return result
