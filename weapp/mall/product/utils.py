# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json, copy
from datetime import datetime
from operator import attrgetter

from django.db.models import Q

from mall import models
from account.models import UserProfile
from mall.promotion import models as promotion_model
from core import search_util


def process_custom_model(custom_model_str):
    """处理custommodels字符串

    Args:
        customModels(str): a str like 2:4_1:3

    Return:
        list: the list like [{
                                'property_id': 2,
                                'property_value_id': 4
                            },{
                                'property_id': 1,
                                'property_value_id': 4
                            }]
    """
    properties = []
    property_infos = custom_model_str.split('_')
    for property_info in property_infos:
        items = property_info.split(':')
        properties.append({
            'property_id': int(items[0]),
            'property_value_id': int(items[1])
        })
    return properties


def extract_product_model(request):
    is_use_custom_models = request.POST.get("is_use_custom_model", '') == u'true'

    use_custom_models = json.loads(request.POST.get('customModels', '[]'))
    if use_custom_models and is_use_custom_models:
        standard_model = {
            "price": 0.0,
            "weight": 0.0,
            "stock_type": models.PRODUCT_STOCK_TYPE_LIMIT,
            "stocks": 0,
            "user_code": '',
            "is_deleted": True
        }
        custom_models = use_custom_models
        for model in custom_models:
            model['properties'] = process_custom_model(model['name'])

    else:
        price = request.POST.get('price', '0.0').strip()
        weight = request.POST.get('weight', '0.0').strip()
        stock_type = int(request.POST.get(
            'stock_type',
            models.PRODUCT_STOCK_TYPE_UNLIMIT)
        )
        stocks = request.POST.get('stocks')
        if stocks and int(stocks) == -1:
            stocks = 0
        stocks = int(stocks) if stocks else 0
        user_code = request.POST.get('user_code', '').strip()
        standard_model = {
            "price": price,
            "weight": weight,
            "stock_type": stock_type,
            "stocks": stocks,
            "user_code": user_code,
        }
        custom_models = []
    return (standard_model, custom_models)

PRODUCT_FILTERS = {
    'product': [{
        'comparator': lambda product, filter_value: filter_value in product.name,
        'query_string_field': 'name'
    }, {
        'comparator': lambda product, filter_value: product.sales >= int(filter_value),
        'query_string_field': 'lowSales'
    }, {
        'comparator': lambda product, filter_value: product.sales <= int(filter_value),
        'query_string_field': 'highSales'
    }, {
        'comparator': lambda product, filter_value: (int(filter_value) == -1) or (int(filter_value) in [category['id'] for category in product.categories if category['is_selected']]),
        'query_string_field': 'category'
    }, {
        'comparator': lambda product, filter_value: filter_value == product.bar_code,
        'query_string_field': 'barCode'
    }, {
        'comparator': lambda product, filter_value: product.created_at >= datetime.strptime(filter_value, '%Y-%m-%d %H:%M'),
        'query_string_field': 'startDate'
    }, {
        'comparator': lambda product, filter_value: product.created_at <= datetime.strptime(filter_value, '%Y-%m-%d %H:%M'),
        'query_string_field': 'endDate'
    }],
    'models': [{
        'comparator': lambda model, filter_value: model['price'] >= float(filter_value),
        'query_string_field': 'lowPrice'
    }, {
        'comparator': lambda model, filter_value: model['price'] <= float(filter_value),
        'query_string_field': 'highPrice'
    }, {
        'comparator': lambda model, filter_value: model['stock_type'] == models.PRODUCT_STOCK_TYPE_UNLIMIT or model['stocks'] >= int(filter_value),
        'query_string_field': 'lowStocks'
    }, {
        'comparator': lambda model, filter_value: model['stock_type'] != models.PRODUCT_STOCK_TYPE_UNLIMIT and 0 <= model['stocks'] <= int(filter_value) or int(filter_value) < 0,
        'query_string_field': 'highStocks'
    }]
}


def filter_products(request, products):
    has_filter = search_util.init_filters(request, PRODUCT_FILTERS)
    if not has_filter:
        return products

    filtered_products = []
    products = search_util.filter_objects(products, PRODUCT_FILTERS['product'])
    if not products:
        return filtered_products

    for product in products:
        models = copy.copy(product.models)
        if None in models:
            models.remove(None)
        models = search_util.filter_objects(models, PRODUCT_FILTERS['models'])
        if models:
            filtered_products.append(product)
    return filtered_products


def sorted_products(manager_id, product_categories, reverse):
    """根据display_index对在售商品进行排序

    Args:
      products(list): 根据CategoryHasProduct，添加过display的product列表
    """
    #获取与category关联的product集合
    category_ids = (category.id for category in product_categories)
    relations = models.CategoryHasProduct.objects.filter(
        category_id__in=category_ids).select_related('product')
    categoryId2relations = dict()
    for relation in relations:
        categoryId2relations.setdefault(relation.category_id, []).append(relation)
    productIds = set([x.product_id for x in relations])
    products = models.Product.objects.filter(id__in=productIds, is_deleted=False).exclude(
        shelve_type=models.PRODUCT_SHELVE_TYPE_RECYCLED)
    # 微众商城代码
    #duhao 20151120
    #微众商城的商品-分组管理 页面  商品的状态应该是商品在微众商城里的状态，而不是在商户里的状态
    # if manager_id == 216:
    #     _products = []
    #     for product in products:
    #         if product.owner_id == 216 or (product.weshop_sync > 0 and product.shelve_type == models.PRODUCT_SHELVE_TYPE_ON):
    #             if product.owner_id != 216:
    #                 product.shelve_type = product.weshop_status
    #             _products.append(product)
    #     products = _products

    models.Product.fill_display_price(products)
    models.Product.fill_sales_detail(manager_id, products, productIds)
    id2product = dict([(product.id, product) for product in products])

    for c in product_categories:
        products = []
        for i in categoryId2relations.get(c.id, []):
            if id2product.has_key(i.product_id):
                product = copy.copy(id2product[i.product_id])
                product.display_index = i.display_index
                product.join_category_time = i.created_at
                products.append(product)

        products_is_0 = filter(lambda p: p.display_index == 0 or p.shelve_type != models.PRODUCT_SHELVE_TYPE_ON, products)
        products_not_0 = filter(lambda p: p.display_index != 0, products)
        products_is_0 = sorted(products_is_0, key=attrgetter('shelve_type', 'join_category_time', 'id'), reverse=True)
        products_not_0 = sorted(products_not_0, key=attrgetter('display_index'))
        products = products_not_0 + products_is_0

        # products = sorted(products, key=attrgetter('join_category_time', 'id'), reverse=True)
        # products = sorted(products, key=attrgetter('shelve_type', 'display_index'))
        # products = sorted(products, key=attrgetter('shelve_type'), reverse=reverse)


        c.products = products
    return product_categories

def delete_weizoom_mall_sync_product(request, mall_product_id):
    try:
        relations = models.WeizoomHasMallProductRelation.objects.filter(Q(mall_product_id=mall_product_id)|Q(weizoom_product_id=mall_product_id))
        from mall.promotion.utils import stop_promotion
        promotion_relations = promotion_model.ProductHasPromotion.objects.filter(product_id__in=[relation.weizoom_product_id for relation in relations])
        promotions = stop_promotion(request, [relation.promotion for relation in promotion_relations])
        models.Product.objects.filter(id__in=[relation.weizoom_product_id for relation in relations]).update(is_deleted=True)
        relations.update(is_deleted=True)
    #TODO:钉订提示
    except:
       pass

def update_weizoom_mall_sync_product_status(mall_product_id):
    try:
        models.WeizoomHasMallProductRelation.objects.filter(mall_product_id=mall_product_id, is_deleted=False).update(is_updated=True)
    except:
        pass

def get_sync_product_store_name(product_ids):
    # try:
    relations = models.WeizoomHasMallProductRelation.objects.filter(weizoom_product_id__in=product_ids, is_deleted=False)
    product_id2mall_id = {}
    product_id2sync_time = {}
    for relation in relations:
        product_id2mall_id[relation.weizoom_product_id] = relation.mall_id
        product_id2sync_time[relation.weizoom_product_id] = relation.sync_time.strftime('%Y-%m-%d %H:%M')
    mall_ids = product_id2mall_id.values()
    mall_id2store_name = dict([(profile.user_id, profile.store_name) for profile in UserProfile.objects.filter(user_id__in=mall_ids)])
    product_id2store_name = {}
    for product_id in product_id2mall_id.keys():
        product_id2store_name[product_id] = mall_id2store_name[product_id2mall_id[product_id]]
    return product_id2store_name, product_id2sync_time
    # except:
    #     pass
    #     return {}, {}
# TODO: update models ref
#
# def update_one_product(request):
#     try:
#         name = request.POST.get('name')
#         product = models.Product.objects.get(name=name)
#     except models.Product.DoesNotExist:
#         print("Product with id does not exist")


# def validate_product_necessary_arguments(request):
#     """验证商品必要的参数是否已提供

#     Return:

#     """
#     try:
#         # 商品名称验证
#         name_pattern = r'\A\w{1,20}\Z'  # 1 到 20 个字符
#         name = request.POST['name']
#         result = re.match(name_pattern, name, re.UNICODE)
#         name = True if result else False

#         # 商品图片验证
#         swipe_images = json.loads(request.POST['swipe_images'])
#         swipe_images = True if swipe_images else False

#         # 无规格商品必要参数验证
#         if not request.POST.get('is_use_custom_model'):
#             price = request.POST['price']
#             weight = request.POST['weight']
#         # 有规格商品必要参数验证
#         else:
#             is_custom_model_validation = True
#             custom_model = json.loads(request.POST['customModels'])
#             for i in customModels:
#                 price = i['price']
#                 weight = i['weight']
#     except KeyError:
#         return False

