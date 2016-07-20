# -*- coding: utf-8 -*-
from __future__ import absolute_import
from operator import attrgetter
import time
import urllib2

import itertools
from django.conf import settings
from django.db.models import signals

import cache
from account.models import UserProfile
from utils import cache_util
from mall.models import WeizoomMall, ProductCategory, CategoryHasProduct
from mall import module_api as mall_api
from mall import models as mall_models
from mall.promotion import models as promotion_models
from mall.promotion.models import PROMOTION_TYPE_FLASH_SALE
from django.core.exceptions import ObjectDoesNotExist
import json

from weapp.hack_django import post_update_signal, post_delete_signal

def get_product_display_price(product, webapp_owner_id, member_grade_id=None):
    """根据促销类型返回商品价格
    """
    # 微众商城代码
    # if webapp_owner_id != product.owner_id and product.weshop_sync == 2:
    #     return round(product.display_price * 1.1, 2)
    if (hasattr(product, 'promotion') and
                (product.promotion is not None) and
                product.promotion['type'] == PROMOTION_TYPE_FLASH_SALE):
        return product.promotion['detail']['promotion_price']
    else:
        return product.display_price

# zhaolei 2015-11-23 unused
# def get_webapp_products_from_db(webapp_owner_user_profile, is_access_weizoom_mall):
#
#     def inner_func():
#         webapp_id = webapp_owner_user_profile.webapp_id
#         webapp_owner_id = webapp_owner_user_profile.user_id
#
#         _, products = mall_api.get_products_in_webapp(webapp_id, is_access_weizoom_mall, webapp_owner_id, 0)
#
#         categories = mall_models.ProductCategory.objects.filter(owner_id=webapp_owner_id)
#
#         product_ids = [product.id for product in products]
#         category_has_products = mall_models.CategoryHasProduct.objects.filter(product_id__in=product_ids)
#         product2categories = dict()
#         for relation in category_has_products:
#             product2categories.setdefault(relation.product_id, set()).add(relation.category_id)
#
#         try:
#             categories = [{"id": category.id, "name": category.name} for category in categories]
#             product_dicts = []
#
#             # Fill detail
#             new_products = []
#             for product in products:
#                 new_product = get_webapp_product_detail(webapp_owner_id, product.id)
#                 new_products.append(new_product)
#
#             mall_models.Product.fill_display_price(new_products)
#
#             for product in new_products:
#                 product_dict = product.to_dict()
#                 product_dict['display_price'] = product.display_price
#                 product_dict['categories'] = product2categories.get(product.id, set())
#                 product_dict['promotion'] = product.promotion if hasattr(product, 'promotion') else None
#                 product_dicts.append(product_dict)
#             return {
#                 'value': {
#                     "products": product_dicts,
#                     "categories": categories
#                 }
#             }
#         except:
#             if settings.DEBUG:
#                 raise
#             else:
#                 return None
#     return inner_func

def get_webapp_product_ids_from_db_new(webapp_owner_user_profile, is_access_weizoom_mall,category_id):
    """
        获取商品分类下的商品id集合
    :param webapp_owner_user_profile:
    :param is_access_weizoom_mall:
    :param category_id:
    :return:
    """
    webapp_id = webapp_owner_user_profile.webapp_id
    webapp_owner_id = webapp_owner_user_profile.user_id
    products = mall_api.get_products_in_webapp(webapp_id, is_access_weizoom_mall, webapp_owner_id, category_id)
    return products

def get_webapp_products_new(webapp_owner_user_profile,
                        is_access_weizoom_mall,
                        category_id):
    # 商城下分类对应的商品id
    categories_products_key = '{wo:%s}_{co:%s}_products' % (webapp_owner_user_profile.user_id,category_id)
    category_pros_data = cache_util.get_set_from_redis(categories_products_key)
    if len(category_pros_data)==0:
        # product.id,display_index
        productid_display_list = []
        products = get_webapp_product_ids_from_db_new(webapp_owner_user_profile, is_access_weizoom_mall,category_id)
        if products:
            for product in products:
                productid_display_list.append(product.id)
                product.promotion = None
                # 添加promation
            cache_util.add_set_to_redis(categories_products_key,*productid_display_list)
        cache_products = products
    else:
        cache_products = get_webapp_products_detail(webapp_owner_user_profile.user_id,category_pros_data)
        print('--------------3',cache_products[0].promotion)

        products = get_webapp_product_ids_from_db_new(webapp_owner_user_profile, is_access_weizoom_mall,category_id)
        if products:
            if len(cache_products) == len(products):
                pass
            else:
                productid_display_list = []
                if products:
                    for product in products:
                        productid_display_list.append(product.id)
                        product.promotion = None
                        # 添加promation
                    cache_util.delete_cache(categories_products_key)
                    cache_util.add_set_to_redis(categories_products_key,*productid_display_list)
                cache_products = products

    if category_id == 0:
        category = mall_models.ProductCategory()
        category.name = u'全部'
    else:
        categories_data = get_webapp_categories_from_cache(webapp_owner_user_profile)
        id2category_name = dict([(c["id"], c["name"]) for c in categories_data])
        if category_id in id2category_name:
            category = mall_models.ProductCategory()
            category.id = category_id
            category.name = id2category_name[category_id]
        else:
            category = mall_models.ProductCategory()
            category.is_deleted = True
            category.name = u'已删除分类'
    mall_models.Product.fill_display_price(cache_products)

    # 分组商品排序，有商品分类和无商品分类的排序规则不同
    if category_id != 0:
        products_id = map(lambda p: p.id, cache_products)
        chp_list = mall_models.CategoryHasProduct.objects.filter(
            category_id=category_id, product_id__in=products_id)
        product_id2chp = dict(map(lambda chp: (chp.product_id, chp), chp_list))
        for product in cache_products:
            product.display_index = product_id2chp[product.id].display_index
            product.join_category_time = product_id2chp[product.id].created_at
        # 1.shelve_type, 2.display_index, 3.id
        products_is_0 = filter(lambda p: p.display_index == 0,
                                             cache_products)
        products_not_0 = filter(lambda p: p.display_index != 0,
                                              cache_products)
        products_is_0 = sorted(products_is_0, key=attrgetter('join_category_time','id'), reverse=True)
        products_not_0 = sorted(products_not_0, key=attrgetter('display_index'))
        cache_products = products_not_0 + products_is_0
    else:
        products_is_0 = filter(lambda p: p.display_index == 0,
                                             cache_products)
        products_not_0 = filter(lambda p: p.display_index != 0,
                                              cache_products)
        products_is_0 = sorted(products_is_0, key=attrgetter('id'), reverse=True)
        products_not_0 = sorted(products_not_0, key=attrgetter('display_index'))
        cache_products = products_not_0 + products_is_0
    print('---------0',cache_products[0].promotion)
    return category, cache_products

def get_webapp_categories_from_cache(webapp_owner_user_profile):
    # 商城下所有的分类,存放id，name，之后更改包括商品数量等信息，主要参考ProductCategory
    categories_key = '{wo:%s}_categories' % webapp_owner_user_profile.user_id
    return cache_util.get_from_cache(categories_key,get_webapp_categories_for_cache(webapp_owner_user_profile))


# zhaolei 2014-11-9 the right code, may be used
# def get_webapp_products(webapp_owner_user_profile,
#                         is_access_weizoom_mall,
#                         category_id):
#     key = 'webapp_products_categories_{wo:%s}' % webapp_owner_user_profile.user_id
#     if key in local_cache:
#         data = local_cache[key]
#     else:
#         data = cache_util.get_from_cache(key, get_webapp_products_from_db(webapp_owner_user_profile, is_access_weizoom_mall))
#         local_cache[key] = data
#
#     if category_id == 0:
#         category = mall_models.ProductCategory()
#         category.name = u'全部'
#     else:
#         id2category = dict([(c["id"], c) for c in data['categories']])
#         if category_id in id2category:
#             category_dict = id2category[category_id]
#             category = mall_models.ProductCategory()
#             category.id = category_dict['id']
#             category.name = category_dict['name']
#         else:
#             category = mall_models.ProductCategory()
#             category.is_deleted = True
#             category.name = u'已删除分类'
#
#     products = mall_models.Product.from_list(data['products'])
#     if category_id != 0:
#         products = [product for product in products if category_id in product.categories]
#
#         # 分组商品排序
#         products_id = map(lambda p: p.id, products)
#         chp_list = mall_models.CategoryHasProduct.objects.filter(
#             category_id=category_id, product_id__in=products_id)
#         product_id2chp = dict(map(lambda chp: (chp.product_id, chp), chp_list))
#         for product in products:
#             product.display_index = product_id2chp[product.id].display_index
#             product.join_category_time = product_id2chp[product.id].created_at
#
#         # 1.shelve_type, 2.display_index, 3.id
#
#         products_is_0 = filter(lambda p: p.display_index == 0,
#                                              products)
#         products_not_0 = filter(lambda p: p.display_index != 0,
#                                               products)
#         products_is_0 = sorted(products_is_0, key=attrgetter('join_category_time'), reverse=True)
#         products_not_0 = sorted(products_not_0, key=attrgetter('display_index'))
#         # products = sorted(products, key=attrgetter('shelve_type'), reverse=False)
#         products = products_not_0 + products_is_0
#     return category, products


# zhaolei 2014-11-9 unuse
# def get_webapp_product_categories(webapp_owner_user_profile, is_access_weizoom_mall):
#     key = 'webapp_products_categories_{wo:%s}' % webapp_owner_user_profile.user_id
#     if key in local_cache:
#         data = local_cache[key]
#     else:
#         data = cache_util.get_from_cache(key, get_webapp_products_from_db(
#             webapp_owner_user_profile, is_access_weizoom_mall))
#         local_cache[key] = data
#
#     return mall_models.ProductCategory.from_list(data['categories'])


def update_webapp_product_cache(**kwargs):
    if hasattr(cache, 'request') and cache.request.user_profile:
        webapp_owner_id = cache.request.user_profile.user_id
        instance = kwargs.get('instance', None)
        before_instance = kwargs.get('before_instance', None)
        sender = kwargs.get('sender', None)
        if instance and sender==mall_models.Product:
            if isinstance(instance, mall_models.Product):
                product_id = instance.id
                shelve_type = instance.shelve_type
                is_deleted = instance.is_deleted
                # 微众商城代码
                # weshop_status = instance.weshop_status
                # weshop_sync = instance.weshop_sync
            else:
                product_id = instance[0].id
                shelve_type = instance[0].shelve_type
                is_deleted = instance[0].is_deleted
                # 微众商城代码
                # weshop_status = instance[0].weshop_status
                # weshop_sync = instance[0].weshop_sync
            if before_instance:
                # 微众商城代码
                #微众商城下架处理 duhao 20151120
                # if before_instance.weshop_status != weshop_status and mall_models.PRODUCT_SHELVE_TYPE_OFF == weshop_status:
                #     cache_util.rem_set_member_by_patten_from_redis('{wo:216}_{co:*}_products',product_id)

                if before_instance.shelve_type != shelve_type and mall_models.PRODUCT_SHELVE_TYPE_OFF == shelve_type or is_deleted == True:
                    #下架商品，清除redis中{wo:38}_{co:*}_products的数据项,批量更新
                    # 或者删除商品时
                    categories_products_key = '{wo:%s}_{co:*}_products' % (webapp_owner_id)
                    cache_util.rem_set_member_by_patten_from_redis(categories_products_key,product_id)

                    # 微众商城代码
                    # if weshop_sync > 0:
                    #     #微众商城的缓存也要一起更新 duhao 20151120
                    #     cache_util.rem_set_member_by_patten_from_redis('{wo:216}_{co:*}_products',product_id)
                elif before_instance.shelve_type != shelve_type and mall_models.PRODUCT_SHELVE_TYPE_ON == shelve_type:
                # 微众商城代码
                # elif (before_instance.shelve_type != shelve_type or webapp_owner_id == 216) and mall_models.PRODUCT_SHELVE_TYPE_ON == shelve_type:
                    #上架商品，确定该商品原来是否有category
                    category_has_products = mall_models.CategoryHasProduct.objects.filter(product_id=product_id)
                    if category_has_products:
                        for category_has_pro in category_has_products:
                            categories_products_key = '{wo:%s}_{co:%s}_products' % (webapp_owner_id,category_has_pro.category.id)
                            cache_util.add_set_to_redis(categories_products_key,category_has_pro.product_id)
                    categories_products_key = '{wo:%s}_{co:0}_products' % (webapp_owner_id)
                    cache_util.delete_cache(categories_products_key)
                    #todo zhaolei
                    # cache_util.add_set_to_redis(categories_products_key,product_id)
            update_product_cache(webapp_owner_id, product_id)

        elif instance and sender==mall_models.CategoryHasProduct:
            # 商品分组中更新商品时
            if isinstance(instance, mall_models.CategoryHasProduct):
                catory_id = instance.category_id
                product_id = instance.product_id
            else:
                catory_id = instance[0].category_id
                product_id = instance[0].product_id
            product = mall_models.Product.objects.filter(id = product_id).get()
            # 非待售添加
            if product.shelve_type != mall_models.PRODUCT_SHELVE_TYPE_OFF :
            # 微众商城代码
            # if product.shelve_type != mall_models.PRODUCT_SHELVE_TYPE_OFF and (webapp_owner_id != 216 or \
            #     (webapp_owner_id == 216 and product.weshop_status != mall_models.PRODUCT_SHELVE_TYPE_OFF)):
            #如果是微众商城过来的请求，则需要验证微众商城里的在售状态 duhao 20151120
            # if product.shelve_type != mall_models.PRODUCT_SHELVE_TYPE_OFF:
                categories_products_key = '{wo:%s}_{co:%s}_products' % (webapp_owner_id,catory_id)
                # todo zhaolei 会存在多次删除的情况
                cache_util.delete_cache(categories_products_key)
                # todo zhaolei 清除对应的varnish缓存,需要重构
                # if settings.EN_VARNISH:
                #     if not settings.DEBUG:
                #         url = 'http://%s/termite/workbench/jqm/preview/?woid=%s&module=mall&model=products&action=list&category_id=%s' % \
                #                 (settings.DOMAIN, webapp_owner_id, catory_id)
                #         request = urllib2.Request(url)
                #         request.get_method = lambda: 'PURGE'
                #         urllib2.urlopen(request)
        elif instance and sender==mall_models.ProductCategory:
            categories_key = '{wo:%s}_categories' % (webapp_owner_id)
            cache_util.delete_cache(categories_key)
        elif instance and sender == mall_models.ProductModel:
            if isinstance(instance, mall_models.ProductModel):
                #暂不处理
                pass
            else:
                for ins in instance:
                    product_id = ins.product_id
                    key = 'webapp_product_detail_{wo:%s}_{pid:%s}' % (webapp_owner_id, product_id)
                    cache_util.delete_pattern(key)

        # pattern_categories = "webapp_products_categories_{wo:%s}" % webapp_owner_id
        # cache_util.delete_pattern(pattern_categories)
        update_product_list_cache(webapp_owner_id)

        key_termite_page = 'termite_webapp_page_%s_*' % webapp_owner_id
        cache_util.delete_pattern(key_termite_page)
        try:
            from termite2.tasks import purge_webapp_page_from_varnish_cache
            purge_webapp_page_from_varnish_cache.delay(webapp_owner_id)
        except:
            pass


def update_webapp_category_cache(**kwargs):
    if hasattr(cache, 'request') and cache.request.user_profile:
        webapp_owner_id = cache.request.user_profile.user_id
        instance = kwargs.get('instance', None)
        sender = kwargs.get('sender', None)
        category_id = 0
        if instance and sender==mall_models.ProductCategory:
            # 删除商品分类
            if isinstance(instance, mall_models.ProductCategory):
                id = instance.id
            else:
                id = instance[0].id
            category_id = id
            categories_products_key = '{wo:%s}_{co:%s}_products' % (webapp_owner_id,id)
            cache_util.delete_redis_key(categories_products_key)
            categories_key = '{wo:%s}_categories' % (webapp_owner_id)
            cache_util.delete_cache(categories_key)
        elif instance and sender==mall_models.CategoryHasProduct:
            # 删除商品分类中的商品
            if isinstance(instance, mall_models.CategoryHasProduct):
                catory_id = instance.category_id
                product_id = instance.product_id
            else:
                product_id = instance[0].product_id
                catory_id = instance[0].category_id
            category_id = catory_id
            categories_products_key = '{wo:%s}_{co:%s}_products' % (webapp_owner_id,catory_id)
            cache_util.rem_set_member_from_redis(categories_products_key,product_id)
        # todo zhaolei 清除对应的varnish缓存,需要重构
        # if settings.EN_VARNISH:
        #     if not settings.DEBUG:
        #         url = 'http://%s/termite/workbench/jqm/preview/?woid=%s&module=mall&model=products&action=list&category_id=%s' % \
        #                 (settings.DOMAIN, webapp_owner_id, category_id)
        #         request = urllib2.Request(url)
        #         request.get_method = lambda: 'PURGE'
        #         urllib2.urlopen(request)

        # pattern_categories = "webapp_products_categories_{wo:%s}" % webapp_owner_id
        # cache_util.delete_pattern(pattern_categories)
        update_product_list_cache(webapp_owner_id)

post_update_signal.connect(
    update_webapp_product_cache, sender=mall_models.Product, dispatch_uid="product.update")
signals.post_save.connect(
    update_webapp_product_cache, sender=mall_models.Product, dispatch_uid="product.save")

signals.post_save.connect(update_webapp_product_cache,
                          sender=mall_models.ProductCategory, dispatch_uid="product_category.save")
post_update_signal.connect(
    update_webapp_product_cache, sender=mall_models.ProductCategory, dispatch_uid="product_category.update")
signals.post_save.connect(update_webapp_product_cache,
                          sender=mall_models.CategoryHasProduct, dispatch_uid="category_has_product.save")
post_delete_signal.connect(
    update_webapp_category_cache, sender=mall_models.ProductCategory, dispatch_uid="mall_product_category.delete")
post_delete_signal.connect(
    update_webapp_category_cache, sender=mall_models.CategoryHasProduct, dispatch_uid="mall_category_has_product.delete")
signals.post_save.connect(update_webapp_product_cache, sender=promotion_models.Promotion,
                          dispatch_uid="update_webapp_product_cache_by_promotion.save")
post_update_signal.connect(update_webapp_product_cache, sender=promotion_models.Promotion,
                           dispatch_uid="update_webapp_product_cache_by_promotion.update")
post_update_signal.connect(update_webapp_product_cache, sender=mall_models.ProductModel,
                           dispatch_uid="update_webapp_product_cache_by_product_model.update")


def get_webapp_products_detail(webapp_owner_id, product_ids, member_grade_id=None):
    """
    功能同get_webapp_product_detail

    批量获取商品详情的缓存
    """
    key_infos = []
    for pid in product_ids:
        key_infos.append({
            'key': 'webapp_product_detail_{wo:%s}_{pid:%s}' % (webapp_owner_id, pid),
            'on_miss': mall_api.get_product_detail_for_cache(webapp_owner_id, pid)
        })
    data = cache_util.get_many_from_cache(key_infos)
    products = []

    for key in data:
        product = mall_models.Product.from_dict(data[key])

        if hasattr(product, 'integral_sale') and product.integral_sale \
                and product.integral_sale['detail'].get('rules', None):
            for i in product.integral_sale['detail']['rules']:
                if i['member_grade_id'] == member_grade_id:
                    product.integral_sale['detail'][
                        'discount'] = str(i['discount']) + "%"
                    break
        if 'promotion' in data[key]:
            promotion_data = data[key]['promotion']
            if promotion_data and len(promotion_data) > 0:
                product.promotion_model = promotion_models.Promotion.from_dict(
                    promotion_data)
            else:
                product.promotion_model = dict()
        else:
            product.promotion_model = dict()
        if 'integral_sale' in data[key]:
            integral_sale_data = data[key]['integral_sale']
            if integral_sale_data and len(integral_sale_data) > 0:
                product.integral_sale_model = promotion_models.Promotion.from_dict(
                    integral_sale_data)
            else:
                product.integral_sale_model = None
        else:
            product.integral_sale_model = None
        products.append(product)
    mall_models.Product.fill_display_price(products)
    return products


def get_webapp_product_detail(webapp_owner_id, product_id, member_grade_id=None):
    """
    管理product detail缓存

    获取商品详情的缓存
    """
    key = 'webapp_product_detail_{wo:%s}_{pid:%s}' % (
        webapp_owner_id, product_id)
    data = cache_util.get_from_cache(
        key, mall_api.get_product_detail_for_cache(webapp_owner_id, product_id))
    product = mall_models.Product.from_dict(data)
    # 解决商品不存在以及商品在店铺间的串号问题
    # 微众商城代码
    if product.is_deleted or product.owner_id != webapp_owner_id:
        product.is_deleted = True
        return product
    # Set member's discount of the product
    if hasattr(product, 'integral_sale') and product.integral_sale \
        and product.integral_sale['detail'].get('rules', None):
        for i in product.integral_sale['detail']['rules']:
            if i['member_grade_id'] == member_grade_id:
                product.integral_sale['detail']['discount'] = str(i['discount'])+"%"
                break

    promotion_data = data['promotion']
    if promotion_data and len(promotion_data) > 0:
        product.promotion_model = promotion_models.Promotion.from_dict(
            promotion_data)
    else:
        product.promotion_model = dict()

    integral_sale_data = data['integral_sale']
    if integral_sale_data and len(integral_sale_data) > 0:
        product.integral_sale_model = promotion_models.Promotion.from_dict(
            integral_sale_data)
    else:
        product.integral_sale_model = None
    product.master_promotion_title = data.get('master_promotion_title', None)
    product.integral_sale_promotion_title = data.get('integral_sale_promotion_title', None)
    mall_models.Product.fill_display_price([product])## 填充价格
    return product


def update_webapp_product_detail_cache(**kwargs):
    """
    更新商品详情缓存
    """
    if hasattr(cache, 'request') and cache.request.user_profile:
        webapp_owner_id = cache.request.user_profile.user_id
        product_ids = None
        cache_args = kwargs.get('cache_args', None)
        if cache_args:
            product_ids = cache_args.get('ids', [])

        if product_ids and len(product_ids) > 0:
            for product_id in product_ids:
                update_product_cache(webapp_owner_id, product_id)
                # 微众商城代码
                # 更新微众商城缓存
                # TODO 更好的设计微众商城
                # if webapp_owner_id != 216:
                #     key = 'webapp_product_detail_{wo:216}_{pid:%s}' % (product_id)
                #     cache_util.delete_cache(key)
            # 微众商城代码
            # if webapp_owner_id != 216:
            #     cache_util.delete_cache('webapp_products_categories_{wo:216}')
        else:
            pattern = 'webapp_product_detail_{wo:%s}_*' % webapp_owner_id
            cache_util.delete_pattern(pattern)

            # pattern_categories = "webapp_products_categories_{wo:%s}" % webapp_owner_id
            # cache_util.delete_pattern(pattern_categories)
            update_product_list_cache(webapp_owner_id)

            instance = kwargs.get('instance', None)
            if instance:
                if isinstance(instance, mall_models.Product):
                    product_id = instance.id
                else:
                    product_id = instance[0].id
                # 会有一次多余删除 todo
                update_product_cache(webapp_owner_id, product_id,deleteRedis=False)
                # 如果没有配置varnish，则会访问报错，不用理会



post_update_signal.connect(update_webapp_product_detail_cache,
                           sender=mall_models.Product, dispatch_uid="product_detail.update")
signals.post_save.connect(update_webapp_product_detail_cache,
                          sender=mall_models.Product, dispatch_uid="product_detail.save")


#这部分代码已经转移到webapp_cache.util中  duhao 2015-08-13
def update_webapp_product_model_cache(**kwargs):
    model = kwargs.get('instance', None)
    if model and model[0].stocks < 1 and model[0].stock_type == mall_models.PRODUCT_STOCK_TYPE_LIMIT:
        # 库存发生变化
        model = model[0]
        update_product_cache(model.owner_id, model.product_id, deleteVarnish=False)
        # 微众商城代码
        # if model.owner_id != 216:
        #     key = 'webapp_product_detail_{wo:216}_{pid:%s}' % (
        #         model.product_id)
        #     cache_util.delete_cache(key)

post_update_signal.connect(update_webapp_product_model_cache,
                           sender=mall_models.ProductModel, dispatch_uid="product_model.update")

#更新商品规格时，情况该账号的所有商品详情缓存 duhao 2015-08-21
#TODO:这个方案比较暴力，当修改商品规格时会把该账号下所有商品详情的缓存都清理掉
def update_webapp_product_detail_cache_when_update_model_property_value(**kwargs):
    if hasattr(cache, 'request'):
        if hasattr(cache.request, 'user'):
            owner_id = cache.request.user.id

            key = 'webapp_product_detail_{wo:%s}_{pid:*}' % (owner_id)
            cache_util.delete_pattern(key)

            # key = 'webapp_products_categories_{wo:%s' % (owner_id)
            # cache_util.delete_pattern(key)
            update_product_list_cache(owner_id)

post_update_signal.connect(update_webapp_product_detail_cache_when_update_model_property_value,
                           sender=mall_models.ProductModelPropertyValue, dispatch_uid="mall_product_model_property_value.update")


def update_webapp_product_detail_by_review_cache(**kwargs):
    if hasattr(cache, 'request'):
        webapp_owner_id = cache.request.user_profile.user_id
        instance = kwargs.get('instance', None)
        if instance:
            if isinstance(instance, mall_models.ProductReview):
                product_id = instance.product_id
            else:
                product_id = instance[0].product_id
            key = 'p_r_{id:%s}' % product_id
            cache_util.delete_pattern(key)
            
            update_product_cache(webapp_owner_id, product_id)


post_update_signal.connect(update_webapp_product_detail_by_review_cache,
                           sender=mall_models.ProductReview, dispatch_uid="product_review.update")


def update_webapp_product_detail_cache_by_promotion(instance, **kwargs):
    """
    根据促销信息，更新商品详情
    """
    if not hasattr(cache, 'request'):
        # 不是后台web系统的update，直接返回
        return

    webapp_owner_id = cache.request.user_profile.user_id
    if isinstance(instance, promotion_models.Promotion):
        promotion_ids = [instance.id]
    else:
        promotion_ids = [promotion.id for promotion in instance]
    for p in promotion_models.ProductHasPromotion.objects.filter(promotion_id__in=promotion_ids):
        update_product_cache(webapp_owner_id, p.product_id)


post_update_signal.connect(update_webapp_product_detail_cache_by_promotion,
                           sender=promotion_models.Promotion, dispatch_uid="product_detail_by_promotion.update")
signals.post_save.connect(update_webapp_product_detail_cache_by_promotion,
                          sender=promotion_models.Promotion, dispatch_uid="product_detail_by_promotion.save")


def get_webapp_product_model_properties(webapp_owner_id):
    """
    管理product model缓存
    """
    key = 'webapp_product_model_properties_{wo:%s}' % webapp_owner_id
    data = cache_util.get_from_cache(
        key, mall_api.get_product_model_properties_for_cache(webapp_owner_id))

    id2property = data['id2property']
    id2value = data['id2value']
    return id2property, id2value


def update_webapp_product_model_properties_cache(**kwargs):
    """
    更新product model缓存
    """
    if hasattr(cache, 'request') and cache.request.user_profile:
        if cache.request.user_profile:
            webapp_owner_id = cache.request.user_profile.user_id
            key = 'webapp_product_model_properties_{wo:%s}' % webapp_owner_id
            cache_util.delete_cache(key)

            for weizoom_mall in WeizoomMall.objects.filter(is_active=True):
                user_profile = UserProfile.objects.filter(
                    webapp_id=weizoom_mall.webapp_id)
                if user_profile.count() == 1:
                    key = 'webapp_product_model_properties_{wo:%s}' % user_profile[
                        0].user_id
                    cache_util.delete_cache(key)


post_update_signal.connect(update_webapp_product_model_properties_cache,
                           sender=mall_models.ProductModelProperty, dispatch_uid="product_model_property.update")
signals.post_save.connect(update_webapp_product_model_properties_cache,
                          sender=mall_models.ProductModelProperty, dispatch_uid="product_model_property.save")
post_update_signal.connect(update_webapp_product_model_properties_cache,
                           sender=mall_models.ProductModelPropertyValue, dispatch_uid="product_model_property_value.update")
signals.post_save.connect(update_webapp_product_model_properties_cache,
                          sender=mall_models.ProductModelPropertyValue, dispatch_uid="product_model_property_value.save")


def get_webapp_postage_configs(webapp_owner_id):
    """
    管理postage config缓存

    获取运费配置的缓存
    """
    key = 'webapp_postage_configs_{wo:%s}' % webapp_owner_id
    data = cache_util.get_from_cache(
        key, mall_api.get_postage_configs_for_cache(webapp_owner_id))

    postage_configs = mall_models.PostageConfig.from_list(data)
    return postage_configs


###############################################################################
# update_webapp_postage_configs_cache: 更新postage config缓存
###############################################################################
def update_webapp_postage_configs_cache(**kwargs):
    if hasattr(cache, 'request') and cache.request.user_profile:
        webapp_owner_id = cache.request.user_profile.user_id
        key = 'webapp_postage_configs_{wo:%s}' % webapp_owner_id
        cache_util.delete_cache(key)


post_update_signal.connect(update_webapp_postage_configs_cache,
                           sender=mall_models.PostageConfig, dispatch_uid="postage_config.update")
signals.post_save.connect(update_webapp_postage_configs_cache,
                          sender=mall_models.PostageConfig, dispatch_uid="postage_config.save")
# post_update_signal.connect(update_webapp_postage_configs_cache, sender=mall_models.SpecialPostageConfig, dispatch_uid = "special_postage_config.update")
# signals.post_save.connect(update_webapp_postage_configs_cache, sender=mall_models.SpecialPostageConfig, dispatch_uid = "special_postage_config.save")
post_update_signal.connect(update_webapp_postage_configs_cache,
                           sender=mall_models.FreePostageConfig, dispatch_uid="free_postage_config.update")
signals.post_save.connect(update_webapp_postage_configs_cache,
                          sender=mall_models.FreePostageConfig, dispatch_uid="free_postage_config.save")


'''
管理mall config缓存
'''
###############################################################################
# get_webapp_mall_config: 获取mall config的缓存
###############################################################################


def get_webapp_mall_config(webapp_owner_id):
    key = 'webapp_mall_config_{wo:%s}' % webapp_owner_id
    data = cache_util.get_from_cache(
        key, mall_api.get_mall_config_for_cache(webapp_owner_id))

    return mall_models.MallConfig.from_dict(data)


###############################################################################
# update_webapp_product_model_properties_cache: 更新product model缓存
###############################################################################
def update_webapp_mall_config_cache(**kwargs):
    if hasattr(cache, 'request') and cache.request.user_profile:
        webapp_owner_id = cache.request.user_profile.user_id
        key = 'webapp_mall_config_{wo:%s}' % webapp_owner_id
        cache_util.delete_cache(key)


post_update_signal.connect(update_webapp_mall_config_cache,
                           sender=mall_models.MallConfig, dispatch_uid="mall_config.update")
signals.post_save.connect(update_webapp_mall_config_cache,
                          sender=mall_models.MallConfig, dispatch_uid="mall_config.save")


###############################################################################
# get_webapp_mall_data: 获取商品规格的缓存
###############################################################################
def get_webapp_mall_data(webapp_owner_id):
    '''
    方便外部使用缓存的接口
    '''
    mall_config_key = 'webapp_mall_config_{wo:%s}' % webapp_owner_id
    postage_configs_key = 'webapp_postage_configs_{wo:%s}' % webapp_owner_id
    product_model_properties_key = 'webapp_product_model_properties_{wo:%s}' % webapp_owner_id
    key_infos = [{
        'key': mall_config_key,
        'on_miss': mall_api.get_mall_config_for_cache(webapp_owner_id)
    }, {
        'key': postage_configs_key,
        'on_miss': mall_api.get_postage_configs_for_cache(webapp_owner_id)
    }, {
        'key': product_model_properties_key,
        'on_miss': mall_api.get_product_model_properties_for_cache(webapp_owner_id)
    }]
    data = cache_util.get_many_from_cache(key_infos)

    result = {
        'postage_configs': mall_models.PostageConfig.from_list(data[postage_configs_key]),
        'product_model_properties': data[product_model_properties_key],
        'mall_config': mall_models.MallConfig.from_dict(data[mall_config_key])
    }

    return result

def get_forbidden_coupon_product_ids_for_cache(webapp_owner_id):
    def inner_func():
        forbidden_coupon_products = []
        for forbidden_coupon_product in promotion_models.ForbiddenCouponProduct.objects.filter(
            owner_id=webapp_owner_id,
            status__in=(promotion_models.FORBIDDEN_STATUS_NOT_START, promotion_models.FORBIDDEN_STATUS_STARTED)
        ):
            forbidden_coupon_products.append(forbidden_coupon_product.to_cache_dict())

        return {
                'keys': [
                    'forbidden_coupon_products_%s' % (webapp_owner_id)
                ],
                'value': forbidden_coupon_products
            }
    return inner_func

def get_forbidden_coupon_product_ids(webapp_owner_id):
    """
    获取商家的禁用全场优惠券的商品id列表 duhao
    """
    key = 'forbidden_coupon_products_%s' % (webapp_owner_id)

    dict_forbidden_coupon_products = cache_util.get_from_cache(key, get_forbidden_coupon_product_ids_for_cache(webapp_owner_id))
    forbidden_coupon_products = []
    for dict_forbidden_coupon_product in dict_forbidden_coupon_products:
        forbidden_coupon_products.append(promotion_models.ForbiddenCouponProduct.from_dict(dict_forbidden_coupon_product))

    product_ids = []
    for product in forbidden_coupon_products:
        if product.is_active:
            product_ids.append(product.product_id)
    return product_ids

def get_webapp_categories_for_cache(webapp_owner_user_profile):
    def inner_func():
        webapp_owner_id = webapp_owner_user_profile.user_id
        categories = mall_models.ProductCategory.objects.filter(owner_id=webapp_owner_id)
        categories = [{"id": category.id, "name": category.name} for category in categories]
        return {
            'keys': [
                '{wo:%s}_categories' % webapp_owner_id
            ],
            'value': categories
        }
    return inner_func

def update_forbidden_coupon_product_ids(instance, **kwargs):
    if hasattr(cache, 'request') and cache.request.user_profile and not kwargs.get('created', False):
        webapp_owner_id = cache.request.user_profile.user_id
        key = 'forbidden_coupon_products_%s' % webapp_owner_id
        cache_util.delete_cache(key)

        if isinstance(instance, promotion_models.ForbiddenCouponProduct):
            product_id = instance.product_id
        else:
            product_id = instance[0].product_id

        update_product_cache(webapp_owner_id, product_id, False, deleteVarnishList=False)

post_update_signal.connect(update_forbidden_coupon_product_ids, sender=promotion_models.ForbiddenCouponProduct, dispatch_uid = "mall_forbidden_coupon_product.update")
signals.post_save.connect(update_forbidden_coupon_product_ids, sender=promotion_models.ForbiddenCouponProduct, dispatch_uid = "mall_forbidden_coupon_product.save")

def update_product_cache(webapp_owner_id, product_id, deleteRedis=True, deleteVarnish=True, deleteVarnishList=True):
    if deleteRedis:
        key = 'webapp_product_detail_{wo:%s}_{pid:%s}' % (webapp_owner_id, product_id)
        cache_util.delete_cache(key)

        # key = 'webapp_products_categories_{wo:%s}' % webapp_owner_id
        # cache_util.delete_cache(key)
        update_product_list_cache(webapp_owner_id)

    # if settings.EN_VARNISH:
    #     if not settings.IS_UNDER_BDD and deleteVarnish:
    #         url = 'http://%s/termite/workbench/jqm/preview/?woid=%s&module=mall&model=product&rid=%s' % \
    #             (settings.DOMAIN, webapp_owner_id, product_id)
    #         request = urllib2.Request(url)
    #         request.get_method = lambda: 'PURGE'
    #         urllib2.urlopen(request)

    #     if not settings.IS_UNDER_BDD and deleteVarnishList:
    #         url = 'http://%s/termite/workbench/jqm/preview/?woid=%s&module=mall&model=products&action=list' % \
    #             (settings.DOMAIN, webapp_owner_id)
    #         request = urllib2.Request(url)
    #         request.get_method = lambda: 'PURGE'
    #         urllib2.urlopen(request)
            # todo 清除商品分类列表
            # for catHasProduct in mall_models.CategoryHasProduct.objects.filter(product_id=product_id):
            #     url = 'http://%s/termite/workbench/jqm/preview/?woid=%s&module=mall&model=products&action=list&category_id=%s' % \
            #         (settings.DOMAIN, webapp_owner_id, catHasProduct.category_id)
            #     request = urllib2.Request(url)
            #     request.get_method = lambda: 'PURGE'
            #     urllib2.urlopen(request)


def update_product_list(webapp_owner_id):
    pass
    # if settings.EN_VARNISH:
    #     url = 'http://%s/termite/workbench/jqm/preview/?woid=%s&module=mall&model=products&action=list' % \
    #             (settings.DOMAIN, webapp_owner_id)
    #     request = urllib2.Request(url)
    #     request.get_method = lambda: 'PURGE'
    #     urllib2.urlopen(request)


def update_product_list_cache(webapp_owner_id):

    webapp_owner_id = webapp_owner_id
    key = 'webapp_products_categories_{wo:%s}' % webapp_owner_id

    product_models = __get_product_models_for_list(webapp_owner_id)

    categories = ProductCategory.objects.filter(owner_id=webapp_owner_id)

    product_ids = [product_model.id for product_model in product_models]
    category_has_products = CategoryHasProduct.objects.filter(product__in=product_ids)
    product2categories = dict()
    for relation in category_has_products:
        product2categories.setdefault(relation.product_id, set()).add(relation.category_id)

    categories = [{"id": category.id, "name": category.name} for category in categories]

    from django.contrib.auth.models import User
    webapp_owner = User.objects.get(id=webapp_owner_id)
    mall_models.Product.fill_details(webapp_owner=webapp_owner, products=product_models, options={
            "with_price": True,
            "flash_sale": True,
            "with_selected_category": True
        })

    product_datas = []

    for product in product_models:
        product_datas.append({
            "id": product.id,
            "name": product.name,
            "is_member_product": product.is_member_product,
            "display_price": product.display_price,
            "promotion_js": json.dumps(product.promotion),
            "thumbnails_url": product.thumbnails_url
        })

    for product_data in product_datas:
        product_data['categories'] = list(product2categories.get(product_data['id'], []))

    data = {
        "products": product_datas,
        "categories": categories
    }
    cache_util.set_cache(key, data)


def __get_product_models_for_list(webapp_owner_id):
    products = mall_models.Product.objects.filter(
        owner=webapp_owner_id,
        shelve_type=mall_models.PRODUCT_SHELVE_TYPE_ON,
        is_deleted=False).order_by('display_index', '-id')

    products_0 = products.filter(display_index=0)
    products_not_0 = products.exclude(display_index=0)
    products = list(itertools.chain(products_not_0, products_0))
    return products

