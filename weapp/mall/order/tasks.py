# -*- coding: utf-8 -*-

from core.exceptionutil import unicode_full_stack
from django.conf import settings
from django.contrib.auth.models import User
from watchdog.utils import watchdog_error
import json
from celery import task
from core import upyun_util
from datetime import datetime
from export_job.models import ExportJob
from account.models import UserProfile
import os
import re
import xlsxwriter
from mall.order.util import get_orders_by_params,handle_member_nickname

from tools.regional.views import get_str_value_by_string_ids_new
from modules.member.models import Member, WebAppUser, MemberFollowRelation, SOURCE_SELF_SUB, SOURCE_MEMBER_QRCODE, SOURCE_BY_URL
from mall.models import *
from market_tools.tools.channel_qrcode.models import ChannelQrcodeHasMember


DEFAULT_CREATE_TIME = '2000-01-01 00:00:00'



@task(bind=True, time_limit=7200, max_retries=2)
def send_order_export_job_task(self, exportjob_id, filter_data_args, type):

    export_jobs = ExportJob.objects.filter(id=exportjob_id)
    status = {
        '0': u'待支付',
        '1': u'已取消',
        '2': u'已支付',
        '3': u'待发货',
        '4': u'已发货',
        '5': u'已完成',
        '6': u'退款中',
        '7': u'退款完成',
        '8': u'退款中',
        '9': u'退款完成',
    }

    payment_type = {
        '-1': u'',
        '0': u'支付宝',
        '2': u'微信支付',
        '3': u'微众卡支付',
        '9': u'货到付款',
        '10': u'优惠抵扣',
        '11': u'翼支付'
    }

    source_list = {
        'mine_mall': u'本店',
        'weizoom_mall': u'商城'
    }

    orders = [u'订单号', u'下单时间', u'付款时间', u'商品名称', u'规格',
         u'商品单价', u'商品数量', u'销售额', u'商品总重量（斤）', u'支付方式', u'支付金额',
         u'现金支付金额', u'微众卡', u'运费', u'积分抵扣金额', u'优惠券金额',
         u'优惠券名称', u'订单状态', u'购买人', u'收货人', u'联系电话', u'收货地址省份',
         u'收货地址', u'发货人', u'发货人备注', u'来源' ,u'物流公司', u'快递单号',
         u'发货时间',u'商家备注',u'用户备注', u'买家来源', u'买家推荐人', u'扫描带参数二维码之前是否已关注', u'是否首单']

    user_id = filter_data_args["user_id"]
    status_type = filter_data_args["status_type"]
    query_dict, date_interval, date_interval_type = filter_data_args["query_dict"], filter_data_args["date_interval"], filter_data_args["date_interval_type"]
    order_status = filter_data_args["order_status"]
    manager_id = filter_data_args["manager_id"]
    user_profile = UserProfile.objects.get(user_id=user_id)
    webapp_id = user_profile.webapp_id
    mall_type = user_profile.webapp_type
    manager = User.objects.get(id=manager_id)

    supplier_users = None
    suplier_not_sub_order_ids = []


    if mall_type:
        orders[25] = u"供货商"
        orders.insert(25, u'供货商类型')

        orders[12] = u"微众卡支付金额"

    # 判断是否有供货商，如果有则显示该字段

    has_supplier = False
    if mall_type:
        has_supplier = True

    if has_supplier:
        orders.append(u'采购价')
        orders.append(u'采购成本')

    if type in [1,3]:
        filename = "order_{}.xlsx".format(exportjob_id)
        dir_path_excel = "excel"
        dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_excel)
        file_path = "{}/{}".format(dir_path,filename)
        workbook   = xlsxwriter.Workbook(file_path)
        table = workbook.add_worksheet()

        table.write_row('A1', orders)
        try:
            order_list = Order.objects.belong_to(webapp_id).order_by('-id')
            if status_type:
                if status_type == 'refund':
                    order_list = order_list.filter(status__in=[ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED])
                elif status_type == 'audit':
                    if order_status == '8':
                        order_list = order_list.filter(status__in=[ORDER_STATUS_GROUP_REFUNDING,ORDER_STATUS_GROUP_REFUNDED])
                    else:
                        order_list = order_list.filter(status__in=[ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED])

            if not mall_type:
                order_list = order_list.exclude(
                        supplier_user_id__gt=0,
                        status__in=[ORDER_STATUS_NOT, ORDER_STATUS_CANCEL, ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED]
                    )

            product_name = ''
            if query_dict.get("product_name"):
                product_name = query_dict["product_name"]

            # 处理团购筛选
            group_order_relations = OrderHasGroup.objects.filter(webapp_id=webapp_id)
            group_order_ids = [r.order_id for r in group_order_relations]
            if query_dict.get('order_type') and query_dict['order_type'] == 2 and not mall_type:
                order_list = order_list.filter(order_id__in=group_order_ids)

            order_list = get_orders_by_params(query_dict, date_interval, date_interval_type, order_list, user_profile)



            if product_name:
                    # 订单总量
                    order_count = len(order_list)
                    finished_order_count = 0
                    for order in order_list:
                        if order.type != PRODUCT_INTEGRAL_TYPE and order.status == ORDER_STATUS_SUCCESSED:
                            finished_order_count += 1
            else:
                try:
                    order_count = order_list.count()
                except:
                    order_count = len(order_list)
                try:
                    finished_order_count = order_list.filter(status=ORDER_STATUS_SUCCESSED).count()
                except:
                    finished_order_count = len(filter(__filter_order_status, order_list))
                # order_list = list(order_list.all())
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


            relations = {}
            product_ids = []
            promotion_ids = []
            model_value_ids = []

            for relation in OrderHasProduct.objects.filter(order_id__in=order_ids):

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
            order2store2fackorders = {}
            # 取出所有的子订单
            for order in fackorders:
                origin_order_id = order.origin_order_id
                order2supplier2fackorders.setdefault(origin_order_id, {})
                order2store2fackorders.setdefault(origin_order_id, {})
                if order.supplier:
                    order2supplier2fackorders[origin_order_id][order.supplier] = order
                if order.supplier_user_id:
                    order2store2fackorders[origin_order_id][order.supplier_user_id] = order
                # 在order_order_ids中添加子订单
                order_order_ids.append(order.order_id)

            # 获取order对应的发货时间
            order2postage_time = dict([(log.order_id, log.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8')) for log in
                                OrderOperationLog.objects.filter(order_id__in=order_order_ids, action__startswith="订单发货")])

            order2supplier = dict([(supplier.id, supplier) for supplier in Supplier.objects.filter(owner=manager)])
            id2store = dict([(profile.user_id, profile) for profile in UserProfile.objects.filter(webapp_type=0)])

            # print 'end step 8 order - '+str(time.time() - begin_time)
            # 获取order对应的收货地区
            temp_premium_id = None
            temp_premium_products = []

            export_jobs.update(count=order_list.count(), update_at=datetime.now())
            tmp_line = 1
            write_order_count = 0
            for order in order_list:
                # order= __filter_order(order)
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
                    if not mall_type and(order.supplier or order.supplier_user_id):
                        final_total_order_money += order.total_purchase_price
                    else:
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
                    province = u'-'
                    address = '%s' % (order.ship_address)

                if order.order_source:
                    order.come = 'weizoom_mall'
                else:
                    order.come = 'mine_mall'

                source = source_list.get(order.come, u'本店')


                i = 0 # 判断是否订单第一件商品
                orderRelations = relations.get(order.id, [])
                for relation in sorted(orderRelations, key=lambda o:o.id):
                    if temp_premium_id and '%s_%s' % (order.id, relation.promotion_id) != temp_premium_id:
                        # 添加赠品信息
                        #orders.extend(temp_premium_products)
                        for temp_premium_product in temp_premium_products:
                            tmp_line += 1

                            table.write_row("A{}".format(tmp_line), temp_premium_product)
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
                        payment_time = '-'

                    # 优惠券和金额
                    coupon_name = ''
                    coupon_money = '0'
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

                    fackorder = None
                    fackorder_sons = None
                    if relation.product.supplier:
                        fackorder_sons = order2supplier2fackorders.get(order.id, None)
                    if relation.product.supplier_user_id:
                        fackorder_sons = order2store2fackorders.get(order.id, None)

                    if fackorder_sons:
                        if product.supplier:
                            fackorder = fackorder_sons.get(product.supplier, None)
                        if product.supplier_user_id:
                            fackorder = fackorder_sons.get(product.supplier_user_id, None)

                    save_money = str(order.edit_money).replace('.', '').replace('-', '') if order.edit_money else False
                    if fackorder:
                        if not '^' in fackorder.order_id:
                            order_id = '%s%s'.encode('utf8') % (order.order_id if not fackorder else fackorder.order_id, '-%s' % save_money if save_money else '')
                        else:
                            order_id = fackorder.order_id
                    else:
                        order_id = order.order_id

                    order_status = status[str(order.status if not fackorder else fackorder.status)].encode('utf8')
                    # 订单发货时间
                    postage_time = order2postage_time.get(order.order_id if not fackorder else fackorder.order_id, '')
                    supplier_type = ""
                    if fackorder:
                        if fackorder.supplier and order2supplier.has_key(fackorder.supplier):
                            source = order2supplier[fackorder.supplier].name.encode("utf-8")
                            supplier_type = u"自建供货商"
                        if fackorder.supplier_user_id and id2store.has_key(fackorder.supplier_user_id):
                            source = id2store[fackorder.supplier_user_id].store_name.encode("utf-8")
                            supplier_type = u"同步供货商"
                    else:
                        if order.supplier and order2supplier.has_key(order.supplier):
                            source = order2supplier[order.supplier].name.encode("utf-8")
                            supplier_type = u"自建供货商"
                        if order.supplier_user_id and id2store.has_key(order.supplier_user_id):
                            source = id2store[order.supplier_user_id].store_name.encode("utf-8")
                            supplier_type = u"同步供货商"

                    if not mall_type and source != u"本店":
                        source = u"商城"


                    if not mall_type and (order.supplier_user_id > 0 or order.supplier >0):
                        coupon_name = '无'

                    if i == 0:
                        # 发货人处填写的备注
                        temp_leader_names = (order.leader_name if not fackorder else fackorder.leader_name).split('|')
                        leader_remark = ''
                        j = 1
                        while j < len(temp_leader_names):
                            leader_remark += temp_leader_names[j]
                            j += 1

                        order_express_number = (order.express_number if not fackorder else fackorder.express_number).encode('utf8')
                        express_name = express_util.get_name_by_value(order.express_company_name if not fackorder else fackorder.express_company_name).encode('utf8')

                        if '^' in order_id:
                            if mall_type:
                                try:
                                    key = order_id.split('^')[1]
                                    customer_message = json.loads(order.customer_message).get(key, {}).get('customer_message')
                                except:
                                    customer_message = ''
                            else:
                                customer_message = order.customer_message
                        else:
                            customer_message = fackorder.customer_message

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
                            order.total_purchase_price if not mall_type and(order.supplier or order.supplier_user_id) else final_price + weizoom_card_money,
                            u'0' if not mall_type and(order.supplier or order.supplier_user_id) else final_price,
                            u'0' if order.status == 0 else weizoom_card_money,
                            # order.weizoom_card_money_huihui,
                            order.postage,
                            u'0' if order.status == 0 else order.integral_money,
                            u'0' if order.status == 1 and coupon_name else coupon_money,
                            u'无' if order.status == 1 else coupon_name,
                            order_status,
                            order.buyer_name.encode('utf8') if order.buyer_name else '-',
                            order.ship_name.encode('utf8') if order.ship_name else '-',
                            order.ship_tel.encode('utf8') if order.ship_tel else '-',
                            province.encode('utf8') if province else '-',
                            address.encode('utf8') if address else '-',
                            temp_leader_names[0].encode('utf8'),
                            leader_remark.encode('utf8'),
                            source.encode('utf8'),
                            express_name if express_name else '-',
                            order_express_number if order_express_number else '-',
                            postage_time if postage_time else '-',
                            order.remark.encode('utf8') if order.remark.encode('utf8') else '-',
                            u'-' if customer_message == '' or not customer_message else order.customer_message.encode('utf-8'),
                            member_source_name if member_source_name else '-',
                            father_name_or_qrcode_name if father_name_or_qrcode_name else '-',
                            before_scanner_qrcode_is_member if before_scanner_qrcode_is_member else '-',
                            u'首单' if order.is_first_order else u'非首单'

                        ]
                        if mall_type:
                            tmp_order.insert(25, supplier_type)
                        if has_supplier:
                            tmp_order.append( u'-' if 0.0 == product.purchase_price else product.purchase_price)
                            tmp_order.append(u'-'  if 0.0 ==product.purchase_price else product.purchase_price*relation.number)
                        # orders.append(tmp_order)
                        tmp_line += 1

                        table.write_row("A{}".format(tmp_line), tmp_order)
                        total_product_money += relation.price * relation.number
                    else:
                        order_express_number = (order.express_number if not fackorder else fackorder.express_number).encode('utf8')
                        express_name = express_util.get_name_by_value(order.express_company_name if not fackorder else fackorder.express_company_name).encode('utf8')
                        if '^' in order_id:
                            if mall_type:
                                try:
                                    key = order_id.split('^')[1]
                                    customer_message = json.loads(order.customer_message).get(key, {}).get('customer_message')
                                except:
                                    customer_message = ''
                            else:
                                customer_message = order.customer_message
                        else:
                            customer_message = fackorder.customer_message
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
                            u'-',
                            u'-',
                            u'-',
                            # u'-',
                            u'-',
                            u'-',
                            u'-' if order.status == 1 and coupon_name else coupon_money,
                            u'-' if order.status == 1 or not coupon_name else coupon_name,
                            order_status,
                            order.buyer_name.encode('utf8') if order.buyer_name else '-',
                            order.ship_name.encode('utf8') if order.ship_name else '-',
                            order.ship_tel.encode('utf8') if order.ship_tel else '-',
                            province.encode('utf8') if province else '-',
                            address.encode('utf8') if address else '-',
                            temp_leader_names[0].encode('utf8'),
                            leader_remark.encode('utf8'),
                            source.encode('utf8'),
                            express_name if express_name else '-',
                            order_express_number if order_express_number else '-',
                            postage_time if postage_time else '-',
                            u'-',
                            u'-' if customer_message == '' or not customer_message else customer_message.encode('utf-8'),
                            member_source_name if member_source_name else '-',
                            father_name_or_qrcode_name if father_name_or_qrcode_name else '-',
                            before_scanner_qrcode_is_member if before_scanner_qrcode_is_member else '-',
                            u'首单' if order.is_first_order else u'非首单'

                        ]
                        if mall_type:
                            tmp_order.insert(25, supplier_type)
                        if has_supplier:
                            tmp_order.append(u'' if 0.0 == product.purchase_price else product.purchase_price)
                            tmp_order.append(u'' if 0.0 ==product.purchase_price else product.purchase_price*relation.number)
                        # orders.append(tmp_order)
                        tmp_line += 1
                        table.write_row("A{}".format(tmp_line), tmp_order)
                        total_product_money += relation.price * relation.number
                    i += 1
                    if order.id in order2premium_product and not temp_premium_id:
                        premium_products = order2premium_product[order.id].get(relation.promotion_id, [])
                        # 已取消订单不累计赠品数量
                        if order_status != STATUS2TEXT[1] and order_status != STATUS2TEXT[7]:
                            total_premium_product += len(premium_products)
                        for premium_product in premium_products:
                            order_express_number = (order.express_number if not fackorder else fackorder.express_number).encode('utf8')
                            express_name = express_util.get_name_by_value(order.express_company_name if not fackorder else fackorder.express_company_name).encode('utf8')
                            tmp_order = [
                                order_id,
                                order.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8'),
                                payment_time,
                                u'(赠品)' + premium_product['name'],
                                u'-',
                                premium_product['price'],
                                premium_product['count'],
                                0.0,
                                premium_product_id2weight[premium_product['id']] * 2 * relation.number,
                                payment_type[str(int(order.pay_interface_type))],
                                u'-',
                                u'-',
                                u'-',
                                u'-',
                                u'-',
                                u'-',
                                u'-',
                                order_status,
                                order.buyer_name.encode('utf8') if order.buyer_name else '-',
                                order.ship_name.encode('utf8') if order.ship_name else '-',
                                order.ship_tel.encode('utf8') if order.ship_tel else '-',
                                province.encode('utf8') if province else '-',
                                address.encode('utf8') if address else '-',
                                temp_leader_names[0].encode('utf8'),
                                leader_remark.encode('utf8'),
                                source.encode('utf8'),
                                express_name if express_name else '-',
                                order_express_number if order_express_number else '-',
                                postage_time if postage_time else '-',
                                u'-',
                                u'-',
                                member_source_name if member_source_name else '-',
                                father_name_or_qrcode_name if father_name_or_qrcode_name else '-',
                                before_scanner_qrcode_is_member if before_scanner_qrcode_is_member else '-',
                                '-'
                            ]
                            if mall_type:
                                tmp_order.insert(25, supplier_type)
                            if has_supplier:
                                tmp_order.append( u'-' if 0.0 == premium_product['purchase_price'] else premium_product['purchase_price'])
                                tmp_order.append(u'-' if 0.0 ==premium_product['purchase_price'] else premium_product['purchase_price']*premium_product['count'])
                            temp_premium_products.append(tmp_order)
                            temp_premium_id = '%s_%s' % (order.id, relation.promotion_id)
                        # if test_index % pre_page == pre_page-1:
                        #   print str(test_index)+' - '+str(time.time() - test_begin_time)+'-'+str(time.time() - begin_time)

                write_order_count += 1
                export_jobs.update(processed_count=write_order_count,update_at=datetime.now())
            if temp_premium_id:
                # 处理赠品信息
                #orders.extend(temp_premium_products)
                for temp_premium_product in temp_premium_products:
                    tmp_line += 1
                    table.write_row("A{}".format(tmp_line), temp_premium_product)

            totals = [
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
            ]
            tmp_line += 1
            table.write_row("A{}".format(tmp_line), totals)
            #return orders

            workbook.close()
            upyun_path = '/upload/excel/{}'.format(filename)
            yun_url = upyun_util.upload_image_to_upyun(file_path, upyun_path)
            export_jobs.update(status=1,file_path=yun_url,update_at=datetime.now())

        except:
            notify_message = "导出商品评论任务失败,response:{}".format(unicode_full_stack())
            export_jobs.update(status=2,is_download=1)
            watchdog_error(notify_message)

