# -*- coding: utf-8 -*-
from __future__ import absolute_import
import copy
import json, time
import logging
from behave import when, then, given
from mall.models import ProductCategory, Product, ProductModel
from webapp.models import WebApp
from django.contrib.auth.models import User
from django.db.models import Q

from mall import models as mall_models  # 注意不要覆盖此module
from test import bdd_util
from features.testenv.model_factory import (
    ProductCategoryFactory, ProductFactory
)
from .steps_db_util import (
    get_custom_model_id_from_name, get_custom_model_name_from_id,
    get_product_response_from_web_page, get_custom_model_id_from_user_code
)

@when(u'{user}暂停{scend}秒')
def step_impl(context, user, scend):
    time.sleep(float(scend))


@when(u'{user}已添加商品')
def step_impl(context, user):
    step_product_add(context, user)


@given(u'{user}已添加商品')
def step_product_add(context, user):
    """
    添加一个或多个商品.

    用户user添加一个或多个商品到后台, 但添加商品前请确保用户已经登陆且设置支付方式.

    所需参数信息如下:
      [
        {
          *'name': "",           # 商品名称
          *'price': "",          # 商品价格
          *'weight': "",         # 商品重量
        },
        {...},
      ]

    """
    url = '/mall2/product/?_method=put'
    if context.table:
        context.products = context.table
    else:
        context.products = json.loads(context.text)
    for product in context.products:
        if hasattr(product, 'as_dict'):
            # Row 转换成dict
            product = product.as_dict()
        if 'stock_type' in product:
            product['stock_type'] = 1 if product['stock_type'] == '有限' else 0
        else:
            if product.get('stocks'):
                product['stock_type'] = 1
            else:
                product['stock_type'] = 0
        product['type'] = mall_models.PRODUCT_DEFAULT_TYPE
        __process_product_data(product, user=user)
        product = __supplement_product(context.webapp_owner_id, product)
        product['is_enable_bill'] = product.get('invoice', False)
        tmp_properties = []
        for property in product.get('properties', []):
            tmp_property = {}
            tmp_property['name'] = property['name']
            tmp_property['value'] = property['description']
            tmp_properties.append(tmp_property)
        product['properties'] = json.dumps(tmp_properties)
        # 转换供货商
        if 'supplier' in product:
            response = context.client.get('/mall2/api/supplier_list/',data={"name":product['supplier']})
            supplier = json.loads(response.content)['data']['items'][0]
            product['supplier'] = supplier['id']
        context.client.post(url, product)
        is_be_for_sale = product.get('status', '') == u'待售'
        is_shelve = product['shelve_type'] == mall_models.PRODUCT_SHELVE_TYPE_OFF
        if not is_be_for_sale and not is_shelve:
            latest_product = mall_models.Product.objects.all().order_by('-id')[0]
            mall_models.Product.objects.filter(
                id=latest_product.id
            ).update(shelve_type=1)
        if product.get('created_at'):
            latest_product = mall_models.Product.objects.all().order_by('-id')[0]
            mall_models.Product.objects.filter(
                id=latest_product.id
            ).update(created_at=product.get('created_at'))


@then(u"{user}能获取商品'{product_name}'")
def step_get_products(context, user, product_name):
    expected = json.loads(context.text)
    actual = __get_product_from_web_page(context, product_name)
    bdd_util.assert_dict(expected, actual)


@when(u"{user}删除商品'{product_name}'的商品规格'{model_name}")
def step_delete_product_with_custom_model(context, user, product_name, model_name):
    """删除有定制规格商品的某个规则
    """
    step_update_product(context, user, product_name)


@then(u"{user}后端获取'{product_name}'库存")
def step_get_product_stock(context, user, product_name):
    expected = json.loads(context.text)
    response = get_product_response_from_web_page(context, product_name)
    product = response.context['product']
    actual_product = dict()
    actual_product['name'] = product.name
    actual_product['stocks'] = product.stocks

    bdd_util.assert_dict(expected, actual_product)


@when(u"{user}更新商品'{product_name}'")
def step_update_product(context, user, product_name):
    user_id = User.objects.get(username=user).id
    existed_product = Product.objects.get(owner_id=user_id, name=product_name)

    if hasattr(context, 'caller_step_json'):
        product = context.caller_step_json
        delattr(context, 'caller_step_json')
    else:
        product = json.loads(context.text)
    if 'name' not in product:
        product['name'] = existed_product.name

    existed_product_properties = mall_models.ProductProperty.objects.filter(product_id=existed_product.id)
    tmp_properties = []
    for index, property in enumerate(product.get('properties', [])):
        tmp_property = {}
        if existed_product_properties:
            tmp_property['id'] = existed_product_properties[index].id
        tmp_property['name'] = property['name']
        tmp_property['value'] = property['description']
        tmp_properties.append(tmp_property)
    product['properties'] = json.dumps(tmp_properties)
    product['supplier'] = existed_product.supplier
    __process_product_data(product, user=user)
    product = __supplement_product(context.webapp_owner_id, product)
    print("POST DATA: {}".format(product))

    if product['buy_in_supplier']:
        url = '/mall2/api/check_product_has_promotion/'
        data = {
            'product_id': existed_product.id,
            'buy_in_supplier': product['buy_in_supplier']
        }
        response = context.client.get(url, data)
        response_json = json.loads(response.content)
        if response_json['code'] == 500:
            context.event_hint = u"请先停止该商品参与的活动"
            return

    # url = '/mall2/product/?id=%d&source=offshelf' % existed_product.id
    url = '/mall2/product/?id=%d&?shelve_type=%d' % (
        existed_product.id, existed_product.shelve_type, )
    response = context.client.post(url, product)
    bdd_util.tc.assertEquals(302, response.status_code)
    #assert False


@then(u"{user}能获取商品列表")
def step_impl(context, user):
    actual = __get_products(context)
    expected = []
    if context.table:
        for product in context.table:
            product = product.as_dict()
            expected.append(product)
    else:
        expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@then(u"{user}能获得'{type_name}'商品列表")
def step_impl(context, user, type_name):
    actual = __get_products(context, type_name)
    context.products = actual

    if hasattr(context, 'caller_step_text'):
        expected = json.loads(context.caller_step_text)
        delattr(context, 'caller_step_text')
    else:
        if context.table:
            expected = []
            for product in context.table:
                product = product.as_dict()
                if 'barCode' in product:
                    product['bar_code'] = product['barCode']
                    del product['barCode']
                product['categories'] = product['categories'].split(',')
                # 处理空字符串分割问题
                if product['categories'][0] == '':
                    product['categories'] = []
                # 处理table中没有验证库存的行
                if 'stocks' in product and product['stocks'] == '':
                    del product['stocks']
                # 处理table中没有验证条码的行
                if 'bar_code' in product and product['bar_code'] == '':
                    del product['bar_code']
                expected.append(product)
        else:
            expected = json.loads(context.text)

    for item in actual:
        if item['is_sync']:
            item['is_sync_supplier'] = 'true'
        else:
            item['is_sync_supplier'] = 'false'
    # for i in range(len(expected)):
    #     print expected[i]['name'], "-----", actual[i]['name']
    #     print expected[i]['is_sync_supplier'], "-----", actual[i]['is_sync_supplier']

    bdd_util.assert_list(expected, actual)

@then(u"{user}能获取商品规格详情'{product_name}'")
def get_product_model(context, user, product_name):
    product = __get_product_from_web_page(context, product_name)
    expect_dict = {}
    for row in context.table:
        # | 颜色 | 价格(元) | 库存 | 商品编码 | 尺寸
        if u'尺寸' in row.headings:

            title = row[u'颜色'] + " "+ row[u'尺寸']
        else:
            title = row[u'颜色']
        if u'库存' in row.headings and u'无限' == row['库存']:
            try:
                expect_dict[title] = {'price':int(row['价格(元)']),'stock_type':row['库存']}
            except:
                expect_dict[title] = {'price':float(row['价格(元)']),'stock_type':row['库存']}
        else:
            try:
                expect_dict[title] = {'price':int(row['价格(元)']),'stocks':int(row['库存'])}
            except:
                expect_dict[title] = {'price':float(row['价格(元)']),'stocks':int(row['库存'])}
        if row[u'商品编码'] != u'':
            expect_dict[title]['user_code'] = row[u'商品编码']

    bdd_util.assert_dict(expect_dict,product['model']['models'])

@when(u"{user}更新商品'{product_name}'的库存为")
def step_impl(context, user, product_name):
    stock_infos = json.loads(context.text)

    model_infos = []
    for stock_info in stock_infos:
      model = get_custom_model_id_from_user_code(context.webapp_owner_id, stock_info['user_code'])
      stock_info['id'] = model.id
      if stock_info['stock_type'] == u'有限':
          stock_info['stock_type'] = 'limit'
      else:
          stock_info['stock_type'] = 'unlimit'
          stock_info['stocks'] = 0
      model_infos.append(stock_info)

    data = {
      'model_infos': json.dumps(model_infos)
    }

    response = context.client.post('/mall2/api/product_model/?_method=post', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}修改商品'{product_name}'的价格为")
def step_impl(context, user, product_name):
    price_infos = json.loads(context.text)

    model_infos = []
    for price_info in price_infos:
        product = bdd_util.get_product_by(product_name)
        if price_info.get('user_code', None) is not None:
            product_model = ProductModel.objects.get(product_id=product.id, user_code=price_info['user_code'])
        else:
            product_model = ProductModel.objects.filter(Q(product_id=product.id) & ~Q(user_code=''))[0]
        price_info['id'] = product_model.id
        model_infos.append(price_info)

    data = {
      'model_infos': json.dumps(model_infos)
    }

    response = context.client.post('/mall2/api/product_model_price', data)
    bdd_util.assert_api_call_success(response)
    # bdd_util.assert_list([], [])


@when(u"{user}查看商品'{product_name}'的规格为")
def step_impl(context, user, product_name):
    target_product = None
    for product in context.products:
      if product['name'] == product_name:
          target_product = product
          break

    product = target_product
    models = []
    for model in product['models']:
      buf = []
      for property_value in model['property_values']:
          buf.append(property_value['name'])
      models.append({
          "name": u' '.join(buf),
          "price": model['price'],
          "stocks": model['stocks'],
          "user_code": model['user_code']
      })
    actual = models

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@when(u"{user}将商品'{product_name}'放入回收站")
def step_impl(context, user, product_name):
    __update_prducts_by_name(context, product_name, u'回收站', user)


@when(u"{user}将商品批量放入回收站")
def step_impl(context, user):
    update_products(context, user, u'回收站')


@when(u"{user}'{action}'商品'{product_name}'")
def update_product(context, user, action, product_name):
    __update_prducts_by_name(context, product_name, action, user)


@when(u"{user}批量{action}商品")
def update_products(context, user, action):
    __update_prducts_by_name(context, json.loads(context.text), action, user)

@when(u"{user}更新'{product_name}'商品排序{pos}")
def update_product_display_index(context, user, product_name, pos):
    data = {
        "id": ProductFactory(name=product_name).id,
        "update_type": "update_pos",
        "pos": pos
    }
    response = context.client.post('/mall2/api/product_pos/?_method=post', data)
    bdd_util.assert_api_call_success(response)

@when(u"{user}设置商品查询条件")
def step_impl(context,user):
    query_param = json.loads(context.text)
    webapp_id = bdd_util.get_webapp_id_for(user)
    owner = WebApp.objects.get(appid=webapp_id)
    category_name = query_param.get('category', None)
    if category_name:
        if category_name == u'全部' or category_name == u'全部分类':
            query_param['category'] = -1
        else:
            query_param['category'] = ProductCategory.objects.get(name=query_param['category']).id

    supplier_type = query_param.get('supplier_type', None)
    if supplier_type:
        if supplier_type == u'全部':
            query_param['orderSupplierType'] = '-1'
        elif supplier_type == u'同步供货商':
            query_param['orderSupplierType'] = '0'
        elif supplier_type == u'自建供货商':
            query_param['orderSupplierType'] = '1'
        del query_param['supplier_type']
    context.query_param = query_param


@then(u"{user}获得提示信息{product_info}")
def step_impl(context, product_info, user):
    product_name = context.product_name
    expected__is_group_buying = True
    actual_is_group_buying = False
    if product_info == u"\'该商品正在进行团购活动\'":
        products = context.products
        for product in products:
            if product["name"] == product_name:
                actual_is_group_buying = product["is_group_buying"]
    delattr(context, "product_name")
    context.tc.assertEquals(actual_is_group_buying, expected__is_group_buying)

def __update_prducts_by_name(context, product_name, action, user):
    ACTION2TYPE = {
        u'上架': 'onshelf',
        u'下架': 'offshelf',
        u'回收站': 'recycled',
        u'永久删除': 'delete',
        u'删除': 'delete',
        u'彻底删除': 'delete',
    }
    action = ACTION2TYPE[action]
    if action == 'offshelf':
        time.sleep(1) #处理下架时睡眠一秒，避免测试结果不准
    data = {
        'shelve_type': action
    }

    user_id = User.objects.get(username=user).id
    if isinstance(product_name, list):
        data['ids'] = []
        for product_name in product_name:
            product_id = mall_models.Product.objects.get(owner_id=user_id, name=product_name).id
            data['ids'].append(product_id)
    else:
        data['ids'] = mall_models.Product.objects.get(owner_id=user_id, name=product_name).id
        context.product_name = product_name

    response = context.client.post('/mall2/api/product_list/?_method=post', data)
    bdd_util.assert_api_call_success(response)


def __get_products(context, type_name=u'在售'):
    NAME2TYPE = {
      u'待售': 'offshelf',
      u'在售': 'onshelf',
      u'回收站': 'recycled'
    }
    type = NAME2TYPE[type_name]
    url = '/mall2/api/product_list/?version=1&type=%s' % type
    if hasattr(context, 'query_param'):
        for key in context.query_param.keys():
            url += '&%s=%s' % (key, context.query_param[key])
    response = context.client.get(url)

    data = json.loads(response.content)['data']
    context.pageinfo = data['pageinfo']
    mall_type = data['data']['mall_type']

    for product in data["items"]:
        actions = []
        product['is_member_product'] = 'on' if product.get('is_member_product', False) else 'off'
        #价格
        product['price'] = product['display_price']
        if 'display_price_range' in product:
            product['price'] = product['display_price_range']
        #分类
        categories = []
        for category in product['categories']:
            if category['is_selected']:
                categories.append(category['name'])
        product['categories'] = categories
        #是否启用定制规格
        product['is_enable_model'] = u'启用规格' if product['is_use_custom_model'] else u'不启用规格'
        #处理规格
        if product['is_use_custom_model']:
            models = {}
            for model in product['models']:
                buf = []
                for property_value in model['property_values']:
                    buf.append(property_value['name'])
                model_name = " ".join(buf)
                models[model_name] = {
                    "price": model['price'],
                    "user_code": model['user_code'],
                    "stock_type": u'无限' if model['stock_type'] == 0 else u'有限',
                    "stocks": model['stocks']
                }
            product['model'] = {
                "models": models
            }
        else:
            standard_model = product['standard_model']
            standard_model['stock_type'] = u'无限' if standard_model['stock_type'] == 0 else u'有限'
            product['model'] = {
                'models': {
                    'standard': product['standard_model']
                }
            }
            product['stock_type'] = standard_model['stock_type']

        if product['is_self']:
            actions.append(u'修改')

        if type_name == u"在售":
            actions.append(u'下架')
        elif type_name == u"待售":
            actions.append(u'上架')
        actions.append(u'彻底删除')
        product['actions'] = actions
        product['supplier'] = product['store_name']

    return data["items"]


def __get_product_from_web_page(context, product_name):
    """
    访问 GET `/mall2/product/` 获取response

    """
    response = get_product_response_from_web_page(context, product_name)
    product = response.context['product']
    supplier = None
    if 'supplier' in response.context:
        supplier = response.context['supplier']
    has_store_name = response.context['has_store_name']
    if has_store_name:
        supplier = response.context['store_name']
    else:
        supplier = 0 if not supplier else dict(supplier).get(product.supplier)
    #处理category
    categories = response.context['categories']
    category_name = ''
    for category in categories:
        if category.get('is_selected'):
            category_name += ',' + category['name']
    if len(category_name) > 0:
        category_name = category_name[1:]

    tmp_properties = product.properties
    properties = []
    for property in tmp_properties:
        properties.append({
                'name': property['name'],
                'description': property['value']
            })

    actual = {
        "sales": product.sales,
        "name": product.name,
        "categories": category_name,
        "physical_unit": product.physical_unit,
        "thumbnails_url": product.thumbnails_url,
        "pic_url": product.pic_url,
        "introduction": product.introduction,
        "detail": product.detail,
        "remark": product.remark,
        "stock_type": u'无限' if product.stock_type == mall_models.PRODUCT_STOCK_TYPE_UNLIMIT else u'有限',
        "shelve_type": u'上架' if product.shelve_type == mall_models.PRODUCT_SHELVE_TYPE_ON else u'下架',
        'stocks': product.stocks,
        'category': category_name,
        'swipe_images': product.swipe_images,
        'is_use_custom_model': u'是' if product.is_use_custom_model else u'否',
        'is_enable_model': u'启用规格' if product.is_use_custom_model else u'不启用规格',
        'model': {},
        'bar_code': product.bar_code,
        'min_limit': product.min_limit,
        'postage': u'免运费',
        'pay_interfaces': [],
        "is_member_product": 'on' if product.is_member_product else 'off',
        "supplier": supplier,
        "purchase_price": product.purchase_price if product.purchase_price else "",
        "promotion_title": product.promotion_title,
        "invoice": product.is_enable_bill,
        "distribution_time": 'on' if product.is_delivery else 'off',
        "properties": properties
    }

    #填充运费
    print("product.postage_id={}".format(product.postage_id))
    if product.postage_id == 999 or product.postage_id <= 0:
        # TODO: 999表示什么？ 表示使用系统运费
        postage_config_info = response.context['postage_config_info']
        if postage_config_info['is_use_system_postage_config']:
            actual['postage'] = postage_config_info['system_postage_config'].name
        else:
            # TODO: 如何处理? 显示商品统一运费金额
            actual['postage'] = product.unified_postage_money
        #postage_config_info.system_postage_config.name
    elif product.postage_id>0:
        print("product.postage_id={}".format(product.postage_id))
        actual['postage'] = mall_models.PostageConfig.objects.get(
            id=product.postage_id).name


    # 填充支付方式
    if product.is_use_online_pay_interface:
        actual['pay_interfaces'].append({'type': u"在线支付"})
    if product.is_use_cod_pay_interface:
        actual['pay_interfaces'].append({'type': u"货到付款"})

    # 填充是否添加配送时间
    # actual['is_delivery'] = product.get("is_delivery",False)

    #填充model信息
    if product.is_use_custom_model:
        product_models = product.models
        models = {}
        for product_model in product_models:
            if not product_model or product_model['name'] == 'standard':
                continue
            else:
                display_name = get_custom_model_name_from_id(
                    context.webapp_owner_id,
                    product_model['name'])
                models[display_name] = {
                    "price": product_model['price'],
                    "weight": product_model['weight'],
                    "market_price": "" if product_model['market_price'] == 0 else product_model['market_price'],
                    "stock_type": u'无限' if product_model['stock_type'] == mall_models.PRODUCT_STOCK_TYPE_UNLIMIT else u'有限',
                    "stocks": product_model['stocks'],
                    "user_code": product_model['user_code']

                }
                # 积分商品
                if product.type == mall_models.PRODUCT_INTEGRAL_TYPE:
                    models[display_name]["integral"] = product_model['price']

        actual['model']['models'] = models
    else:
        product_models = product.models
        models = {}
        for product_model in product_models:
            if product_model['name'] == 'standard':
                models['standard'] = {
                    "price": product_model['price'],
                    "weight": product_model['weight'],
                    "market_price": "" if product_model['market_price'] == 0 else product_model['market_price'],
                    "stock_type": u'无限' if product_model['stock_type'] == mall_models.PRODUCT_STOCK_TYPE_UNLIMIT else u'有限',
                    "stocks": product_model['stocks'],
                    "bar_code": product_model['user_code']
                }
                # 积分商品
                if product.type == mall_models.PRODUCT_INTEGRAL_TYPE:
                    models['standard']["integral"] = product_model['price']

        actual['model']['models'] = models
        actual['price'] = models['standard']['price']
        actual['weight'] = models['standard']['weight']

    return actual


def __process_stock_type(model):
    #处理库存类型
    if ('stock_type' in model) and (model['stock_type'] == u'有限'):
        model['stock_type'] = mall_models.PRODUCT_STOCK_TYPE_LIMIT
    else:
        model['stock_type'] = mall_models.PRODUCT_STOCK_TYPE_UNLIMIT
        model['stocks'] = 0


def __pay_interface(pay_interfaces):
    if pay_interfaces is None:
        return True, True

    for pay_interface in pay_interfaces:
        if pay_interface['type'] == u"货到付款":
            return True, True

    return True, False


def __supplement_product(webapp_owner_id, product):
    product_prototype = {
        "name": "product",
        "physical_unit": u"包",
        "price": "11.0",
        "market_price": "11.0",
        "weight": "0",
        "bar_code": "12321" ,
        "thumbnails_url": "/standard_static/test_resource_img/hangzhou1.jpg",
        "pic_url": "/standard_static/test_resource_img/hangzhou1.jpg",
        "introduction": u"product的简介",
        "detail": u"product的详情",
        "remark": u"product的备注",
        "shelve_type": mall_models.PRODUCT_SHELVE_TYPE_ON,
        "stock_type": mall_models.PRODUCT_STOCK_TYPE_UNLIMIT,
        "swipe_images": json.dumps([{
            "url": "/standard_static/test_resource_img/hangzhou1.jpg",
            "width": 100,
            "height": 100
        }]),
        "postage": -1,
        "postage_deploy": -1,
        "pay_interface_online": True,
        "pay_interface_cod": True,
        "is_enable_cod_pay_interface": True,
        "is_enable_online_pay_interface": True,
        "is_delivery": False,
        "buy_in_supplier": 0
    }
    # 支付方式
    pay_interface_online, pay_interface_cod = __pay_interface(
            product.get('pay_interfaces', None)
    )
    product_prototype['pay_interface_online'] = pay_interface_online
    if pay_interface_cod is False:
        product_prototype.pop('pay_interface_cod')
        product_prototype.pop('is_enable_cod_pay_interface')
    if pay_interface_online is False:
        product_prototype.pop('pay_interface_online')
        product_prototype.pop('is_enable_online_pay_interface')
    # 配送时间
    if product.has_key('distribution_time'):
        product_prototype["is_delivery"] = product['distribution_time']
    # 运费
    postage = product.get('postage', None)
    if postage:
        try:
            postage_money = float(postage)
            product_prototype['postage_type'] = 'unified_postage_type'
            product_prototype['unified_postage_money'] = postage_money
        except:
            product_prototype['postage_type'] = 'custom_postage_type'
            product_prototype['unified_postage_money'] = 0.0
    else:
        product_prototype['postage_type'] = 'unified_postage_type'
        product_prototype['unified_postage_money'] = 0.0

    product_type = product.get('type', mall_models.PRODUCT_DEFAULT_TYPE)
    is_integral_type = product_type == mall_models.PRODUCT_INTEGRAL_TYPE

    # 积分商品
    if is_integral_type:
        product['price'] = product.get('integral', 0)

    # 下单位置
    if product.get('buy_position', "") == u'供货商':
        product['buy_in_supplier'] = 1

    #商品图
    pic_url = product.get('pic_url', None)
    if pic_url:
        product_prototype['pic_url'] = pic_url

    product_prototype.update(product)

    # print(product_prototype)

    #设置启用规格
    if product.get('is_enable_model', None) == u'启用规格':
        product_prototype['is_use_custom_model'] = 'true'

    if 'model' in product:
        if 'standard' in product['model']['models']:
            standard_model = product['model']['models']['standard']
            __process_stock_type(standard_model)

            # 积分商品
            if is_integral_type:
                standard_model['price'] = standard_model.get('integral', 0)

            product_prototype.update({
                "price": standard_model.get('price', 11.0),
                "user_code": standard_model.get('user_code', 1),
                "market_price": standard_model.get('market_price', 11.0),
                "weight": standard_model.get('weight', 0.0),
                "stock_type": standard_model.get('stock_type', mall_models.PRODUCT_STOCK_TYPE_UNLIMIT),
                "stocks": standard_model.get('stocks', 0)

            })
        else:
            #对每一个model，构造诸如customModel^2:4_3:7^price的key
            custom_models = []
            product_models_items = product['model']['models'].items()
            for custom_model_name, custom_model in product_models_items:
                __process_stock_type(custom_model)
                if 'price' not in custom_model:
                    custom_model['price'] = '1.0'
                if 'market_price' not in custom_model:
                    custom_model['market_price'] = '1.0'
                if 'weight' not in custom_model:
                    custom_model['weight'] = '0.0'
                if 'market_price' not in custom_model:
                    custom_model['market_price'] = '1.0'
                if 'user_code' not in custom_model:
                    custom_model['user_code'] = '1'

                # 积分商品
                if is_integral_type:
                    custom_model['price'] = custom_model.get('integral', 0)

                custom_model_id = get_custom_model_id_from_name(
                    webapp_owner_id,
                    custom_model_name)
                custom_model['name'] = custom_model_id
                custom_models.append(custom_model)
            product_prototype['customModels'] = json.dumps(custom_models)
    else:
        # 没有规格
        if int(product.get('stocks', '0')) > 0:
            product_prototype['stock_type'] = mall_models.PRODUCT_STOCK_TYPE_LIMIT
            product_prototype['stocks'] = product.get('stocks', '0')
    product_prototype['market_price'] = product_prototype['market_price']
    return product_prototype


def __process_product_data(product, user=None):
    """
    """
    # 商品上架状态
    if user:
        user_id = User.objects.get(username=user).id
    if product.get('shelve_type', '') == u'下架':
        product['shelve_type'] = mall_models.PRODUCT_SHELVE_TYPE_OFF
    else:
        product['shelve_type'] = mall_models.PRODUCT_SHELVE_TYPE_ON

    # 商品分类
    product['product_category'] = -1
    if product.get('categories', ''):
        product_category = ''
        for category_name in product['categories'].split(','):
            if user:
                category = mall_models.ProductCategory.objects.get(name=category_name, owner_id=user_id)
            else:
                category = ProductCategoryFactory(name=category_name)
            product_category += "%s," % str(category.id)
        product['product_category'] = product_category
        del product['categories']

    # 轮播图
    if product.get('swipe_images'):
        for swipe_image in product['swipe_images']:
            swipe_image['width'] = 100
            swipe_image['height'] = 100
        product['swipe_images'] = json.dumps(product['swipe_images'])
