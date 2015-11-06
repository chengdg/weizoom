# -*- coding: utf-8 -*-
from __future__ import absolute_import
from operator import attrgetter
import time
import urllib2
from django.conf import settings
from django.db.models import signals

import cache
from account.models import UserProfile
from utils import cache_util
from mall.models import WeizoomMall
from mall import module_api as mall_api
from mall import models as mall_models
from mall.promotion import models as promotion_models
from mall.promotion.models import PROMOTION_TYPE_FLASH_SALE
from django.core.exceptions import ObjectDoesNotExist
import json

from weapp.hack_django import post_update_signal, post_delete_signal

local_cache = {}


def get_product_display_price(product, webapp_owner_id, member_grade_id=None):
    """根据促销类型返回商品价格
    """
    if webapp_owner_id != product.owner_id and product.weshop_sync == 2:
        return round(product.display_price * 1.1, 2)
    elif (hasattr(product, 'promotion') and
                (product.promotion is not None) and
                product.promotion['type'] == PROMOTION_TYPE_FLASH_SALE):
        return product.promotion['detail']['promotion_price']
    else:
        return product.display_price


def get_webapp_products_from_db(webapp_owner_user_profile, is_access_weizoom_mall):

    def inner_func():
        webapp_id = webapp_owner_user_profile.webapp_id
        webapp_owner_id = webapp_owner_user_profile.user_id

        _, products = mall_api.get_products_in_webapp(webapp_id, is_access_weizoom_mall, webapp_owner_id, 0)

        categories = mall_models.ProductCategory.objects.filter(owner_id=webapp_owner_id)

        product_ids = [product.id for product in products]
        category_has_products = mall_models.CategoryHasProduct.objects.filter(product_id__in=product_ids)
        product2categories = dict()
        for relation in category_has_products:
            product2categories.setdefault(relation.product_id, set()).add(relation.category_id)

        try:
            categories = [{"id": category.id, "name": category.name} for category in categories]
            product_dicts = []

            # Fill detail
            new_products = []
            for product in products:
                new_product = get_webapp_product_detail(webapp_owner_id, product.id)
                new_products.append(new_product)

            mall_models.Product.fill_display_price(new_products)

            for product in new_products:
                product_dict = product.to_dict()
                product_dict['display_price'] = product.display_price
                product_dict['categories'] = product2categories.get(product.id, set())
                product_dict['promotion'] = product.promotion if hasattr(product, 'promotion') else None
                product_dicts.append(product_dict)
            return {
                'value': {
                    "products": product_dicts,
                    "categories": categories
                }
            }
        except:
            if settings.DEBUG:
                raise
            else:
                return None
    return inner_func

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
    _, products = mall_api.get_products_in_webapp(webapp_id, is_access_weizoom_mall, webapp_owner_id, category_id)
    return products

def get_webapp_categories(webapp_owner_user_profile):
    """
        获取webapp的所有商品分类
    :param webapp_owner_user_profile:
    :return:
    """
    webapp_id = webapp_owner_user_profile.webapp_id
    webapp_owner_id = webapp_owner_user_profile.user_id
    categories = mall_models.ProductCategory.objects.filter(owner_id=webapp_owner_id)
    categories = [{"id": category.id, "name": category.name} for category in categories]
    return categories

def get_webapp_products_new(webapp_owner_user_profile,
                        is_access_weizoom_mall,
                        category_id):
    # 商城下分类对应的商品id
    categories_products_key = '{wo:%s}_{co:%s}_products' % (webapp_owner_user_profile.user_id,category_id)
    # 商城下所有的分类,存放id，name，之后更改包括商品数量等信息，主要参考ProductCategory
    categories_key = '{wo:%s}_categories' % webapp_owner_user_profile.user_id

    category_pros_data = cache_util.get_zrange_from_redis(categories_products_key,desc=True)
    #倒叙获取，可以直接取消get_webapp_product_ids_from_db_new中的id 逆序排序，两者的效率待分析  TODO zhaolei
    if len(category_pros_data)==0:
        # product.id,display_index
        productid_display_list = []
        products = get_webapp_product_ids_from_db_new(webapp_owner_user_profile, is_access_weizoom_mall,category_id)
        if products:
            for product in products:
                productid_display_list.append(product.id)
                productid_display_list.append(product.display_index)
                product.promotion = None
                # 添加promation
            cache_util.add_zdata_to_redis(categories_products_key,*productid_display_list)
        cache_products = products
    else:
        cache_products = get_webapp_products_detail(webapp_owner_user_profile.user_id,category_pros_data)

    if categories_key in local_cache:
        categories_data = local_cache[categories_key]
    else:
        categories_data = get_webapp_categories(webapp_owner_user_profile)
        local_cache[categories_key] = categories_data
        cache_util.set_cache(categories_key,json.dumps(categories_data)) # todo 需要优化为回调函数的形式

    if category_id == 0:
        category = mall_models.ProductCategory()
        category.name = u'全部'
    else:
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

    # 分组商品排序,暂未搞清楚哪个地方在使用  todo  zhaolei
    if category_id!=0:
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
        products_is_0 = sorted(products_is_0, key=attrgetter('join_category_time'), reverse=True)
        products_not_0 = sorted(products_not_0, key=attrgetter('display_index'))
        cache_products = products_not_0 + products_is_0
        # 分类中的排序规则是不唯一的，这个地方的score要注意
    return category, cache_products

# todo 需要优化
def _get_products_from_redis(category_pros_data):
    """
        封装商品列表，将products_ids构造为对上层透明
    :param category_pros_data:
    :return:
    """

    for productid in category_pros_data:
        pass
    return None

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
                display_index = instance.display_index
            else:
                product_id = instance[0].id
                shelve_type = instance[0].shelve_type
                is_deleted = instance[0].is_deleted
                display_index = instance[0].display_index
            if before_instance:
                # print "zl----------------------",before_instance.shelve_type,shelve_type,before_instance.is_deleted,is_deleted,before_instance.name,product_id
                if before_instance.shelve_type != shelve_type and mall_models.PRODUCT_SHELVE_TYPE_OFF == shelve_type or is_deleted == True:
                    #下架商品，清除redis中{wo:38}_{co:*}_products的数据项,批量更新
                    # 或者删除商品时
                    categories_products_key = '{wo:%s}_{co:*}_products' % (webapp_owner_id)
                    cache_util.rem_zset_member_by_patten_from_redis(categories_products_key,product_id)
                elif before_instance.shelve_type != shelve_type and mall_models.PRODUCT_SHELVE_TYPE_ON == shelve_type:
                    #上架商品，确定该商品原来是否有category
                    category_has_products = mall_models.CategoryHasProduct.objects.filter(product=instance)
                    if category_has_products:
                        for category_has_pro in category_has_products:
                            categories_products_key = '{wo:%s}_{co:%s}_products' % (webapp_owner_id,category_has_pro.category.id)
                            cache_util.add_zdata_to_redis(categories_products_key,category_has_pro.product_id,category_has_pro.product.display_index)
                    categories_products_key = '{wo:%s}_{co:0}_products' % (webapp_owner_id)
                    cache_util.add_zdata_to_redis(categories_products_key,product_id,display_index)
            update_product_cache(webapp_owner_id, product_id)

# todo 该处触发的product较多，需要优化
def update_webapp_product_pos_cache(**kwargs):
    if hasattr(cache, 'request') and cache.request.user_profile:
        webapp_owner_id = cache.request.user_profile.user_id
        instance = kwargs.get('instance', None)
        sender = kwargs.get('sender', None)
        # instance.id 避免创建操作进入
        if instance and sender==mall_models.Product and instance.id!=None:
            if instance and sender==mall_models.Product :
                display_index = instance.display_index
                product_id = instance.id
            else:
                product_id = instance[0].id
                display_index = instance[0].display_index
            product = mall_models.Product.objects.filter(id=product_id).get()
            #更新商品排序,只更新在售和待售列表中的商品排序
            if display_index != product.display_index:
                categories_products_key = '{wo:%s}_{co:0}_products' % (webapp_owner_id)
                cache_util.add_zdata_to_redis(categories_products_key,product_id,display_index)
        elif instance and sender==mall_models.CategoryHasProduct and instance.id!=None:
            if instance and sender==mall_models.CategoryHasProduct:
                display_index = instance.display_index
                product_id = instance.product_id
                chp_id = instance.id
            else:
                product_id = instance[0]['product'][0].id
                display_index = instance[0].display_index
                chp_id = instance[0].id
            chp = mall_models.CategoryHasProduct.objects.filter(id=chp_id).get()
            #更新商品排序，只更新分组管理中的商品排序
            categories_products_key = '{wo:%s}_{co:%s}_products' % (webapp_owner_id,chp.category_id)
            cache_util.add_zdata_to_redis(categories_products_key,product_id,display_index)

post_update_signal.connect(
    update_webapp_product_cache, sender=mall_models.Product, dispatch_uid="product.update")
signals.post_save.connect(
    update_webapp_product_cache, sender=mall_models.Product, dispatch_uid="product.save")

signals.pre_save.connect(
    update_webapp_product_pos_cache, sender=mall_models.Product, dispatch_uid="product.pre_save")
signals.pre_save.connect(
    update_webapp_product_pos_cache, sender=mall_models.CategoryHasProduct, dispatch_uid="mall_category_has_product.pre_save")

signals.post_save.connect(update_webapp_product_cache,
                          sender=mall_models.ProductCategory, dispatch_uid="product_category.save")
signals.post_save.connect(update_webapp_product_cache,
                          sender=mall_models.CategoryHasProduct, dispatch_uid="category_has_product.save")
post_delete_signal.connect(
    update_webapp_product_cache, sender=mall_models.ProductCategory, dispatch_uid="mall_product_category.delete")
post_delete_signal.connect(
    update_webapp_product_cache, sender=mall_models.CategoryHasProduct, dispatch_uid="mall_category_has_product.delete")
signals.post_save.connect(update_webapp_product_cache, sender=promotion_models.Promotion,
                          dispatch_uid="update_webapp_product_cache_by_promotion.save")
post_update_signal.connect(update_webapp_product_cache, sender=promotion_models.Promotion,
                           dispatch_uid="update_webapp_product_cache_by_promotion.update")


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

        promotion_data = data[key]['promotion']
        if promotion_data and len(promotion_data) > 0:
            product.promotion_model = promotion_models.Promotion.from_dict(
                promotion_data)
        else:
            product.promotion_model = dict()

        integral_sale_data = data[key]['integral_sale']
        if integral_sale_data and len(integral_sale_data) > 0:
            product.integral_sale_model = promotion_models.Promotion.from_dict(
                integral_sale_data)
        else:
            product.integral_sale_model = None
        # product['promotion'] = product.promotion if hasattr(product, 'promotion') else None
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
                # 更新微众商城缓存
                # TODO 更好的设计微众商城
                if webapp_owner_id != 216:
                    key = 'webapp_product_detail_{wo:216}_{pid:%s}' % (product_id)
                    cache_util.delete_cache(key)
            if webapp_owner_id != 216:
                cache_util.delete_cache('webapp_products_categories_{wo:216}')
        else:
            pattern = 'webapp_product_detail_{wo:%s}_*' % webapp_owner_id
            cache_util.delete_pattern(pattern)
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
        # update_product_cache(model.owner_id, model.product_id, deleteVarnish=False)

        if model.owner_id != 216:
            key = 'webapp_product_detail_{wo:216}_{pid:%s}' % (
                model.product_id)
            cache_util.delete_cache(key)

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
        forbidden_coupon_products = promotion_models.ForbiddenCouponProduct.objects.filter(
            owner_id=webapp_owner_id, 
            status__in=(promotion_models.FORBIDDEN_STATUS_NOT_START, promotion_models.FORBIDDEN_STATUS_STARTED)
        )

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

    forbidden_coupon_products = cache_util.get_from_cache(key, get_forbidden_coupon_product_ids_for_cache(webapp_owner_id))
    product_ids = []
    for product in forbidden_coupon_products:
        if product.is_active:
            product_ids.append(product.product_id)
    return product_ids

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
    if not settings.IS_UNDER_BDD and deleteVarnish:
        url = 'http://%s/termite/workbench/jqm/preview/?woid=%s&module=mall&model=product&rid=%s' % \
            (settings.DOMAIN, webapp_owner_id, product_id)
        request = urllib2.Request(url)
        request.get_method = lambda: 'PURGE'
        urllib2.urlopen(request)

    if not settings.IS_UNDER_BDD and deleteVarnishList:
        url = 'http://%s/termite/workbench/jqm/preview/?woid=%s&module=mall&model=products&action=list' % \
            (settings.DOMAIN, webapp_owner_id)
        request = urllib2.Request(url)
        request.get_method = lambda: 'PURGE'
        urllib2.urlopen(request)
        # for catHasProduct in mall_models.CategoryHasProduct.objects.filter(product_id=product_id):
        #     url = 'http://%s/termite/workbench/jqm/preview/?woid=%s&module=mall&model=products&action=list&category_id=%s' % \
        #         (settings.DOMAIN, webapp_owner_id, catHasProduct.category_id)
        #     request = urllib2.Request(url)
        #     request.get_method = lambda: 'PURGE'
        #     urllib2.urlopen(request)