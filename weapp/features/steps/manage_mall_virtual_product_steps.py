# -*- coding: utf-8 -*-
import json
import time
import datetime as dt
import utils
import apps_step_utils as apps_util
import steps_db_util
import logging

from datetime import datetime, timedelta
from behave import *
from test.bdd_util import *
from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from django.contrib.auth.models import User

from account.models import UserProfile
from utils.dateutil import parse_datetime
from mall.models import *
from mall import models as mall_models
from mall import module_api
from mall.promotion import models as promotion_models
from modules.member import models as member_models
from weixin.user.models import *
from features_steps_util import *
from core import dateutil
from mall.promotion.virtual_product import *
from collections import OrderedDict

VIRTUAL_ORDER_TYPE = [mall_models.PRODUCT_VIRTUAL_TYPE, mall_models.PRODUCT_WZCARD_TYPE]
# WESHOP_DING_GROUP_ID = '105507196'  #微众商城FT团队钉钉id
# WESHOP_DING_GROUP_ID = '80035247'  #发消息测试群

@when(u'{user}新建福利卡券活动')
def step_impl(context, user):
    context.product_viturals = json.loads(context.text)

    for product_viturals in context.product_viturals:

        products = mall_models.Product.objects.get(name=product_viturals['product']['name'])
        owner = User.objects.get(username=user)
        product_id = products.id
        name = product_viturals['activity_name']
        card_start_date = product_viturals['card_start_date']
        start_time = get_date(card_start_date)
        card_end_date = product_viturals['card_end_date']
        end_time = get_date(card_end_date)

        
        if product_viturals.has_key('card_info'):
            code_file_path = _get_file_path(product_viturals['card_info']['cards'])
        else:
            code_file_path = _get_file_path(product_viturals['cards'])
        data={
            "product_id": product_id,
            "name": name,
            "start_time": start_time,
            "end_time": end_time,
            "code_file_path": code_file_path
        }
        url ="/mall2/api/virtual_product/?_method=put"
        response = context.client.post(url,data)
        errMsg = json.loads(response.content)['errMsg']
    if not errMsg:
        bdd_util.assert_api_call_success(response) 
    else:
        context.errMsg = errMsg
        virtual_product = promotion_models.VirtualProduct.objects.get(owner=owner, name=product_viturals['activity_name'], is_finished=False)
        print "============virtual_product===========",virtual_product.id
        data = {"virtual_product_id": virtual_product.id}
        url ="/mall2/api/virtual_product/?_method=delete"
        response = context.client.post(url,data)
        bdd_util.assert_api_call_success(response) 

@when(u"{user}对福利卡券活动进行'增加库存'")
def step_impl(context, user):
    product_viturals = json.loads(context.text)

    products = mall_models.Product.objects.get(name=product_viturals['product']['name'])
    owner = User.objects.get(username=user)
    product_id = products.id
    # 根据活动product_id 查询出活动 id
    virtual_product = promotion_models.VirtualProduct.objects.get(owner=owner, product_id=product_id, is_finished=False)

    card_start_date = product_viturals['card_start_date']
    start_time = get_date(card_start_date)
    card_end_date = product_viturals['card_end_date']
    end_time = get_date(card_end_date)
    code_file_path = _get_file_path(product_viturals['cards'])

    data={
            "id": virtual_product.id,
            "start_time": start_time,
            "end_time": end_time,
            "code_file_path": code_file_path
        }
    url ="/mall2/api/virtual_product/"
    response = context.client.post(url,data)
    bdd_util.assert_api_call_success(response)

@then(u'{user}获得福利卡券活动列表')
def step_impl(context, user):
    """
    "create_time":"2天前"
    说明：由于 VirtualProduct 中的 created_at 字段是实时时间字段，
    所以features中的create_time并不能与之对应，故删除features中的create_time这一属性
    """
    if hasattr(context,"search_egg"):
        context.virtual_product = context.search_egg
    else:
        url ="/mall2/api/virtual_products"
        response = context.client.get(url,data={"coupon_status": -1})
        context.virtual_product = json.loads(response.content)['data']['items']
    actual = []
    # print "================================"
    # print json.loads(response.content)['data']['items']
    # print "length:",len(json.loads(response.content)['data']['items'])
    # print "================================"
    if context.virtual_product:
        # print "context.virtual_product---->",len(context.virtual_product)
        for virtual_product in context.virtual_product:
            # print "///////////////",virtual_product
            tmp_product = {
                'id': virtual_product['id'],
                'name': virtual_product['name'],
                'product': {
                    'name': virtual_product['product']['name'],
                    'bar_code': virtual_product['product']['bar_code']
                },
                'total_stock': virtual_product['total_stock'],
                'code_stock': virtual_product['code_stock'],
                'sell_num': virtual_product['sell_num'],
                'overdue_num': virtual_product['overdue_num'],
                'expired_num': virtual_product['expired_num'],
                'created_at': virtual_product['created_at'],
                'is_finished': virtual_product['is_finished']
            }
            actual.append(tmp_product)
    expected = []
    expected_data = json.loads(context.text)
    if expected_data:
        for ex in expected_data:
            tmp_product = OrderedDict()
            if ex.has_key('activity_name'):
                tmp_product['name'] = ex['activity_name']
            if ex.has_key('total_stocks'):
                tmp_product['total_stock'] = ex['total_stocks']
            if ex.has_key('remain_stocks'):
                tmp_product['code_stock'] = ex['remain_stocks']
            if ex.has_key('sale_cards'):
                tmp_product['sell_num'] = ex['sale_cards']
            if ex.has_key('invalid_cards'):
                tmp_product['expired_num'] = ex['invalid_cards']
            if ex.has_key('expired_cards'):
                tmp_product['overdue_num'] = ex['expired_cards']
            if ex.has_key('actions'):
                tmp_product['is_finished'] = False if (len(ex['actions']) == 3) else True
            expected.append(tmp_product)

    apps_util.debug_print(expected)
    apps_util.debug_print(actual)
    bdd_util.assert_list(expected, actual)

@then(u"{user}新建福利卡券活动时能获得在售虚拟商品列表")
def step_impl(context, user):
    if hasattr(context,"query_param"):
        query_param = context.query_param
    else:
        query_param = {}
    print "===============================",query_param
    url ="/mall2/api/virtual_product"
    response = context.client.get(url, data=query_param)

    actual = []
    # print "================================"
    # print json.loads(response.content)['data']['items']
    # print "================================"
    context.virtual_product = json.loads(response.content)['data']['items']
    if context.virtual_product:
        for virtual_product in context.virtual_product:
            tmp_product = OrderedDict()
            tmp_product['bar_code'] = virtual_product['bar_code']
            tmp_product['name'] = virtual_product['name']
            tmp_product['price'] = virtual_product['price']
            tmp_product['stocks'] = virtual_product['stocks']
            tmp_product['created_at'] = get_datetime_str(virtual_product['created_at'])
            tmp_product['can_use'] = virtual_product['can_use']
            # print "============================================actual",tmp_product['bar_code']
            actual.append(tmp_product)
    expected = []
    expected_data = []
    if context.table:
        for row in context.table:
            cur_p = row.as_dict()
            expected_data.append(cur_p)
        # print ">>>>>>>>>>>>>",expected
        for expect in expected_data:
            tmp_product = OrderedDict()
            # print "---",tmp_product
            tmp_product['bar_code'] = expect['bar_code']
            tmp_product['name'] = expect['name']
            tmp_product['price'] = expect['price']
            tmp_product['stocks'] = expect['stocks']
            tmp_product['created_at'] = get_datetime_str(expect['create_time'])
            tmp_product['can_use'] = True if(expect['actions'] == '选取') else False
            # print "============================================expected",tmp_product['bar_code']
            expected.append(tmp_product)
            print "--->>>",tmp_product
    print("expected: {}".format(expected))
    print("actual_data: {}".format(actual))
    bdd_util.assert_list(expected, actual)

@then(u"{user}获得福利卡券活动'{name}'的码库详情列表")
def step_impl(context, name, user):
    _get_virtual_code_list(context, name)

def _get_virtual_code_list(context, name):
    expected = []
    expected_data = []
    if context.table:
        for row in context.table:
            cur_p = row.as_dict()
            expected_data.append(cur_p)
        for expect in expected_data:
            tmp_product = OrderedDict()
            tmp_product['code'] = expect['card_id']
            tmp_product['created_at'] = get_datetime_str(expect['create_time'])
            tmp_product['start_time'] = get_datetime_str(expect['start_date'])
            # print "****************tmp_product['start_time']",tmp_product['start_time'],tmp_product['created_at']
            tmp_product['end_time'] = get_datetime_str(expect['end_date'])
            tmp_product['status'] = expect['status']

            tmp_product['member_name'] = expect['member']
            tmp_product['get_time'] = get_datetime_str(expect['get_time']) if expect['get_time'] else ""
            tmp_product['order_id'] = expect['order_no']
            # print "===================================",tmp_product['order_id']
            expected.append(tmp_product)

        # 获取实际数据
        virtual_product = promotion_models.VirtualProduct.objects.get(name=name)
        url ="/mall2/api/virtual_product_codes"
        response = context.client.get(url,data={"virtual_product_id":virtual_product.id})
        context.virtual_product = json.loads(response.content)['data']['items']
        if context.virtual_product:
            actual = _get_actual_data(context.virtual_product)
    else:    
        if hasattr(context,"search_egg"):
            context.virtual_product = context.search_egg       
        else:
            url ="/mall2/api/virtual_product_codes"
            response = context.client.get(url)
            context.virtual_product = json.loads(response.content)['data']['items']
        actual = []
        if context.virtual_product:
            actual = _get_actual_data(context.virtual_product)

        # 期望数据
        expected_data = json.loads(context.text)
        expected = []
        if expected_data:
            # print "=========================expected=",expected_data
            for ex in expected_data:
                tmp_product = OrderedDict()
                tmp_product['code'] = ex['card_id']
                if 'member' in ex:
                    tmp_product['member_name'] = ex.get('member', '')
                if 'create_time' in ex:
                    tmp_product['created_at'] = get_datetime_str(ex['create_time']) if ex['create_time'] else ""
                if 'start_date' in ex:
                    tmp_product['start_time'] = get_datetime_str(ex['start_date']) if ex['start_date'] else ""
                if 'end_date' in ex:
                    tmp_product['end_time'] = get_datetime_str(ex['end_date']) if ex['end_date'] else ""
                if 'status' in ex:
                    tmp_product['status'] = ex['status']
                if 'get_time' in ex:
                    tmp_product['get_time'] = get_datetime_str(ex['get_time']) if ex['get_time'] else ""
                if 'order_no' in ex:
                    tmp_product['order_id'] = ex['order_no']
                expected.append(tmp_product)
    print("expected: {}".format(expected))
    print("actual_data: {}".format(actual))
    bdd_util.assert_list(expected, actual)

def _get_actual_data(context_virtual_product):
    # print "context.virtual_product---->",len(context.virtual_product)
    actual = []
    for virtual_product in context_virtual_product:
        # print "///////////////=========///////////////",virtual_product
        tmp_product = {
            'id': virtual_product['id'],
            'code': virtual_product['code'],
            'created_at': get_datetime_str(virtual_product['created_at']),
            'start_time': get_datetime_str(virtual_product['start_time']),
            'end_time': get_datetime_str(virtual_product['end_time']),
            'status': virtual_product['status'],
            'get_time': get_datetime_str(virtual_product['get_time']) if virtual_product['get_time'] else "",
            'member_id': virtual_product['member_id'],
            'member_name': virtual_product['member_name'],
            'order_id': virtual_product['order_id']
        }
        actual.append(tmp_product)
    return actual

@when(u"{user}获得福利卡券活动'{name}'的码库详情列表")
def step_impl(context, name, user):
    _get_virtual_code_list(context, name)

@when(u"{user}'结束'福利卡券活动'{name}'")
def step_impl(context, name, user):
    virtual_product = promotion_models.VirtualProduct.objects.get(name=name)
    # print "-------->>>>>>>>>",virtual_product.id
    url ="/mall2/api/virtual_product/?_method=delete"
    del_response = context.client.post(url,data={"virtual_product_id":virtual_product.id})
    bdd_util.assert_api_call_success(del_response)

@when(u"{user}设置福利卡券活动列表查询条件")
def step_impl(context, user):

    expect = json.loads(context.text)
    # print "=================",expect['product_name']
    # print "-------------------expect",expect
    search_dic = {"coupon_status": -1}
    if 'create_start_time' in expect:
        expect['start_time'] = get_datetime_str(expect['create_start_time']) if expect['create_start_time'] else ""
        search_dic['start_time'] = expect['start_time']
    if 'create_end_time' in expect:
        expect['end_time'] = get_datetime_str(expect['create_end_time']) if expect['create_start_time'] else ""
        search_dic['end_time'] = expect['end_time']
    search_dic['product_name'] = expect['product_name']
    search_dic['barCode'] = expect['product_bar_code']

    print "=========**********========="
    print search_dic
    print "=========**********========="

    search_url = "/mall2/api/virtual_products"

    search_response = context.client.get(search_url,data=search_dic)

    egg_array = json.loads(search_response.content)['data']['items']
    # print "+++++++++++++++++++++++++++>>>>>>>>>>>",egg_array
    context.search_egg = egg_array
    bdd_util.assert_api_call_success(search_response)

@when(u"{user}访问福利卡券活动'{name}'的卡券详情")
def step_impl(context, name, user):
    context.virtual_name = {'virtual_name':name}

@when(u"{user}设置码库详情列表查询条件")
def step_impl(context, user):
    if hasattr(context,"virtual_name"):
        virtual_name = context.virtual_name['virtual_name']
    else:
        virtual_name = {}
    virtual_product = promotion_models.VirtualProduct.objects.get(name=virtual_name)
    virtual_product_id = virtual_product.id
    print "virtual_product_id",virtual_product_id
    expect = json.loads(context.text)
    # print "=================",expect['product_name']
    # print "============expect==========",expect
    search_dic = {'virtual_product_id':virtual_product_id}
    search_dic['code'] = expect['card_id']
    search_dic['member_name'] = expect['member']

    expect['get_time_start'] = get_datetime_str(expect['get_start_time']) if expect['get_start_time'] else ""
    search_dic['get_time_start'] = expect['get_time_start']
    expect['get_time_end'] = get_datetime_str(expect['get_end_time']) if expect['get_end_time'] else ""
    search_dic['get_time_end'] = expect['get_time_end']

    search_dic['order_id'] = expect['order_no']
    search_dic['status'] = steps_db_util.code_status_to_num(expect['status']) if expect['status'] else -1

    expect['valid_time_start'] = get_datetime_str(expect['card_start_date']) if expect['card_start_date'] else ""
    search_dic['valid_time_start'] = expect['valid_time_start']
    expect['valid_time_end'] = get_datetime_str(expect['card_end_date']) if expect['card_end_date'] else ""
    search_dic['valid_time_end'] = expect['valid_time_end']

    print "=========**********========="
    print search_dic
    print "=========**********========="

    search_url = "/mall2/api/virtual_product_codes"
    search_response = context.client.get(search_url,data=search_dic)
    egg_array = json.loads(search_response.content)['data']['items']
    # print "+++++++++++++++++++++++++++>>>>>>>>>>>",egg_array
    context.search_egg = egg_array

@then(u"{user}导出福利卡券活动'{name}'的码库详情")
def step_impl(context, name, user):
    virtual_product = promotion_models.VirtualProduct.objects.get(name=name)  
    
    from cStringIO import StringIO
    import csv

    url ="/mall2/virtual_product_codes_export/"
    response = context.client.get(url, data={"virtual_product_id":virtual_product.id})
    reader = csv.reader(StringIO(response.content.replace('\0', '')))
    # 去掉表头信息
    csv_items = [row for row in reader]
    context.last_csv_order_info = reader
    all_info = context.last_csv_order_info
    #expect_info = json.loads(context.text)
    actual = dict([(info.split(':')[0].encode('utf-8'),info.split(':')[1]) for info in all_info[1:]])
    print "=========",actual
    actual_encode = {}
    for x,y in actual.items():
        x = x.encode('utf-8')
        actual_encode[unicode(x)] = y

    bdd_util.assert_list(expect_info,[actual_encode])

@then(u"{user}获得上传文件提示信息'{upload_info}'")
def step_impl(context, upload_info, user):
    if hasattr(context,"errMsg"):
        errMsg = context.errMsg
        print "===========errMsg",errMsg
        print "===========upload_info",upload_info
    else:
        errMsg = {}
        print "上传文件成功！"
    context.tc.assertEquals(upload_info, errMsg)
    
@when(u"{user}自动发放卡券给订单'{order_id}'")
def step_impl(context, order_id, user):
    #auto_grant_virtual_product(order_id)
    """
    获取所有虚拟订单(非虚拟子订单)
    """
    order2products = mall_models.OrderHasProduct.objects.filter(
            order__status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP,
            order__type__in=VIRTUAL_ORDER_TYPE,
            order__origin_order_id__lt=0
        )

    oid2order = {}
    oid2product_id2count = {}
    order_ids = []
    for o2p in order2products:
        order = o2p.order
        order_ids.append(order.order_id)
        product = o2p.product
        oid = order.id
        buy_count = o2p.number

        oid2order[oid] = o2p.order
        if not oid2product_id2count.has_key(oid):
            oid2product_id2count[oid] = {}
        
        if oid2product_id2count[oid].has_key(product.id):
            oid2product_id2count[oid][product.id] += buy_count
        else:
            oid2product_id2count[oid][product.id] = buy_count

        #判断是否有促销活动
        if o2p.promotion_id:
            promotion = None
            try:
                promotion = promotion_models.Promotion.objects.get(id=o2p.promotion_id)
            except Exception, e:
                message = u'获取促销失败\norder id:%s\nproduct id:%d\n商品名称:%s' % (order.order_id, product.id, product.name)
                logging.info(message)
                # ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)

            #判断是否是买赠
            if promotion.type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
                premiums = promotion_models.PremiumSaleProduct.objects.filter(premium_sale__id=promotion.detail_id)
                for premium in premiums:
                    _product = premium.product
                    #判断赠品是否是虚拟类型
                    if _product.type in [mall_models.PRODUCT_VIRTUAL_TYPE, mall_models.PRODUCT_WZCARD_TYPE]:
                        premium_sale = premium.premium_sale
                        if premium.premium_sale.is_enable_cycle_mode:
                            premium_product_count = (buy_count / premium_sale.count) * premium.count
                        else:
                            premium_product_count = premium.count

                        logging.info(u'赠品id:%d,名称:%s,个数:%d' % (_product.id, _product.name, premium_product_count))
                        if oid2product_id2count[oid].has_key(_product.id):
                            oid2product_id2count[oid][_product.id] += premium_product_count
                        else:
                            oid2product_id2count[oid][_product.id] = premium_product_count

    order2groups = mall_models.OrderHasGroup.objects.filter(order_id__in=order_ids)
    order_id2group_status = {}
    for o2g in order2groups:
        order_id2group_status[o2g.order_id] = o2g.group_status

    logging.info('virtual order count:%d' % len(oid2order))
    for oid in oid2product_id2count:
        can_update_order_status = True  #是否可以更改订单的发货状态
        print 'process order id:', oid
        order = oid2order[oid]

        #判断团购状态
        if order_id2group_status.has_key(order.order_id):
            if order_id2group_status[order.order_id] == 1:
                logging.info(u'团购订单%s可以发货' % order.order_id)
            else:
                can_update_order_status = False
                logging.info(u'团购订单%s团购未成功，跳过发货，团购状态%d' % (order.order_id, order_id2group_status[order.order_id]))
                continue

        #获取会员信息
        member = member_models.WebAppUser.get_member_by_webapp_user_id(order.webapp_user_id)
        if not member:
            message = u'获取member信息失败\n订单id:%s' % order.order_id
            logging.info(message)
            # ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)
            continue
        product_id2count = oid2product_id2count[oid]
        for product_id in product_id2count:
            count = product_id2count[product_id]
            print '  process product id:%d, buy count:%d' % (product_id, count)
            virtual_products = promotion_models.VirtualProduct.objects.filter(product_id=product_id, is_finished=False)
            if virtual_products.count() > 0:
                virtual_product = virtual_products[0]

                #判断该订单里的这个商品是否已经被发过货了，如果发过则不重复发放，且can_update_order_status不变为False
                oids = [order.id]
                if order.origin_order_id > 0:
                    oids.append(order.origin_order_id)
                existed_records = promotion_models.VirtualProductHasCode.objects.filter(virtual_product=virtual_product, oid__in=oids)

                if existed_records.count() > 0:
                    message = u'该商品已经发过货，无需重复发货\n订单id:%s\n商品id:%d\n福利卡券活动id:%d\n商品名称:%s' % (order.order_id, product_id, virtual_product.id, virtual_product.product.name)
                    logging.info(message)
                    # ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)
                    continue

                #按id顺序发放
                codes = promotion_models.VirtualProductHasCode.objects.filter(virtual_product=virtual_product, status=promotion_models.CODE_STATUS_NOT_GET).order_by('id')

                _c = []
                for code in codes:
                    if (not code.can_not_use) and len(_c) < count:
                        _c.append(code)

                if len(_c) < count:
                    can_update_order_status = False
                    message = u'发放虚拟商品时库存不足\n订单id:%s\n商品id:%d\n待发放:%d\n库存:%d\n商品名称:%s\n福利卡券活动id:%d' % (order.order_id, product_id, count, len(_c), virtual_product.product.name, virtual_product.id)
                    logging.info(message)
                    # ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)
                    continue
                
                for code in _c:
                    print '    deliver code:', code.code
                    code.member_id = member.id
                    code.get_time = get_datetime_str('今天')
                    code.oid = order.origin_order_id
                    code.order_id = order.order_id
                    code.status = promotion_models.CODE_STATUS_GET
                    code.save()

                    if virtual_product.product.type == mall_models.PRODUCT_WZCARD_TYPE:
                        #如果商品是微众卡的话，需要往MemberHasWeizoomCard表里写入一份信息，方便手机卡包里的微众卡能正常显示
                        try:
                            member_has_wzcard = promotion_models.MemberHasWeizoomCard.objects.create(
                                member_id=member.id,
                                # member_name=member.username,
                                member_name='',
                                card_number=code.code,
                                card_password=code.password,
                                relation_id=code.virtual_product.id,
                                source=promotion_models.WEIZOOM_CARD_SOURCE_VIRTUAL
                            )

                            logging.info(u'订单%s发放微众卡到member_has_wzcard：%d' % (order.order_id, member_has_wzcard.id))
                        except Exception, e:
                            message = u'微众卡已经发放成功，但写入MemberHasWeizoomCard信息失败\n订单id:%s\n商品id:%d\n商品名称:%s' % (order.order_id, product_id, virtual_product.product.name)
                            logging.info(message)
                            logging.info(e)
                            # ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)
            else:
                can_update_order_status = False
                message = u'虚拟商品发货失败，商品没有关联福利卡券活动\n订单id:%s\n商品id:%d' % (order.order_id, product_id)
                logging.info(message)
                # ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)

        if can_update_order_status:
            #更改订单状态，发货
            logging.info(u'订单发货：%s'% order.order_id)
            module_api.ship_order(order.id, '', '', u'系统', '', False, False)

def _get_file_path(cards):
    """
    将卡号密码存为xls文件，返回文件路径+文件名
    @param cards： list类型的卡号密码
    @return 保存文件路径+文件名
    """
    file_name = xlwt.Workbook()
    sheet = file_name.add_sheet("my_sheet")
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(curr_dir, '../../../', 'upload/features/steps')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_old_path = os.path.join(dir_path)

    xls_old_file_name = time.strftime("_%Y_%m_%d_%H_%M_%S", time.localtime())
    for row in range(0,len(cards)):
        sheet.write(row,0,cards[row]["id"])
        sheet.write(row,1,cards[row]["password"])
    len_file_name = len(__file__.split('\\'))-1
    xls_file_name = __file__.split('\\')[len_file_name].split('.')[0]
    file_path = file_old_path+"/"+xls_file_name+xls_old_file_name+".xls"
    file_name.save(file_path)
    print "success"
    return file_path