# -*- coding: utf-8 -*-

"""@package mall.product_views
商品管理模块的页面的实现文件
"""

import json

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import F

import models as mall_models
from models import *
import export
from core.restful_url_route import *


COUNT_PER_PAGE = 20
FIRST_NAV = export.PRODUCT_FIRST_NAV


@view(app='mall', resource='onshelf_products', action='get')
@login_required
def get_onshelf_products(request):
    """
    在售商品列表页面
    """
    has_product = (Product.objects.filter(owner=request.manager, shelve_type=PRODUCT_SHELVE_TYPE_ON, is_deleted=False).count() > 0)
    c = RequestContext(request, {
        'first_nav_name': FIRST_NAV,
        'second_navs': export.get_second_navs(request),
        'second_nav_name': export.PRODUCT_MANAGE_ON_SHELF_PRODUCT_NAV,
        'has_product': has_product
    })

    return render_to_response('mall/editor/onshelf_products.html', c)


@view(app='mall', resource='offshelf_products', action='get')
@login_required
def get_offshelf_products(request):
    """
    代售商品列表页面
    """
    has_product = (Product.objects.filter(owner=request.manager, shelve_type=PRODUCT_SHELVE_TYPE_OFF, is_deleted=False).count() > 0)
    c = RequestContext(request, {
        'first_nav_name': FIRST_NAV,
        'second_navs': export.get_second_navs(request),
        'second_nav_name': export.PRODUCT_MANAGE_OFF_SHELF_PRODUCT_NAV,
        'has_product': has_product
    })

    return render_to_response('mall/editor/offshelf_products.html', c)


@view(app='mall', resource='recycled_products', action='get')
@login_required
def get_recycled_products(request):
    """
    回收站商品列表页面
    """
    has_product = (Product.objects.filter(owner=request.manager, shelve_type=PRODUCT_SHELVE_TYPE_RECYCLED, is_deleted=False).count() > 0)
    c = RequestContext(request, {
        'first_nav_name': FIRST_NAV,
        'second_navs': export.get_second_navs(request),
        'second_nav_name': export.PRODUCT_MANAGE_RECYCLED_PRODUCT_NAV,
        'has_product': has_product
    })

    return render_to_response('mall/editor/recycled_products.html', c)


########################################################################
# __extract_product_model: 从商品数据中抽取商品规格
########################################################################
def __extract_product_model(request):
    """
    从商品数据中抽取商品规格
    """
    is_use_custom_model = (request.POST.get('is_use_custom_model', 'false') == 'true')
    if is_use_custom_model:
        standard_model = {
            "price": 0.0,
            "weight": 0.0,
            "stock_type": PRODUCT_STOCK_TYPE_UNLIMIT,
            "stocks": -1,
            "user_code": ''
        }
    else:
        price = request.POST.get('price', '0.0').strip()
        if not price:
            price = 0.0

        weight = request.POST.get('weight', '0.0').strip()
        if not weight:
            weight = 0.0

        stock_type = request.POST.get('stock_type', PRODUCT_STOCK_TYPE_UNLIMIT)
        if not stock_type:
            stock_type = PRODUCT_STOCK_TYPE_UNLIMIT

        stocks = request.POST.get('stocks', -1)
        if stock_type == PRODUCT_STOCK_TYPE_UNLIMIT or not stocks:
            stocks = -1

        user_code = request.POST.get('user_code', '').strip()

        standard_model = {
            "price": price,
            "weight": weight,
            "stock_type": stock_type,
            "stocks": stocks,
            "user_code": user_code
        }

    if is_use_custom_model:
        custom_models = json.loads(request.POST.get('customModels', '[]'));
        for model in custom_models:
            #model name的格式为${property_id}:${property_value_id}_..., 比如2:4_1:3
            #这里需要将其转换为：
            # [{
            #     'property_id': 2,
            #     'property_value_id': 4,
            # }, {
            #     'property_id': 1,
            #     'property_value_id': 3
            # }]
            properties = []
            property_infos = model['name'].split('_')
            for property_info in property_infos:
                items = property_info.split(':')
                properties.append({
                    'property_id': items[0],
                    'property_value_id': items[1]
                })
            model['properties'] = properties
    else:
        custom_models = []

    return standard_model, custom_models


@view(app='mall', resource='product', action='create')
@login_required
def create_product(request):
    """
    创建商品

    @note 处理GET请求时，返回页面
    @note 处理post请求时，创建相应数据，成功后跳转到待售商品页面
    """
    user = request.manager
    # 获取默认运费
    postage = None#module_api.get_default_postage_by_owner_id(user.id)
    # 获取在线支付
    pay_interface_onlines = []#module_api.get_pay_interface_onlines_by_owner_id(user.id)
    # 获取货到付款
    pay_interface_cod = []#module_api.get_pay_interface_cod_by_owner_id(user.id)

    if request.POST:
        standard_model, custom_models = __extract_product_model(request)

        #创建product
        postage_type = request.POST['postage_type']
        if postage_type == POSTAGE_TYPE_UNIFIED:
            postage_id = -1
            unified_postage_money = request.POST.get('unified_postage_money', 0.0)
        else:
            postage_id = 0
            unified_postage_money = 0.0
        product = mall_models.Product.objects.create(
            owner = request.manager,
            name = request.POST.get('name', '').strip(),
            promotion_title = request.POST.get('promotion_title', '').strip(),
            user_code = request.POST.get('user_code', '').strip(),
            bar_code = request.POST.get('bar_code', '').strip(),
            thumbnails_url = request.POST.get('thumbnails_url', '').strip(),
            pic_url = request.POST.get('pic_url', '').strip(),
            detail = request.POST.get('detail', '').strip(),
            type = request.POST.get('type', PRODUCT_DEFAULT_TYPE),
            is_use_online_pay_interface = 'is_enable_online_pay_interface' in request.POST,
            is_use_cod_pay_interface = 'is_enable_cod_pay_interface' in request.POST,
            postage_type = postage_type,
            postage_id = postage_id,
            unified_postage_money = unified_postage_money,
            weshop_sync = request.POST.get('weshop_sync', 0)
        )
        first_product = Product.objects.filter(owner=request.manager).order_by('-display_index')[0]
        product.display_index = first_product.display_index+1

        #处理standard商品规格
        ProductModel.objects.create(
            owner = request.manager,
            product = product,
            name = 'standard',
            is_standard = True,
            price = standard_model['price'],
            weight = standard_model['weight'],
            stock_type = standard_model['stock_type'],
            stocks = standard_model['stocks'],
            user_code = standard_model['user_code']
        )

        #处理custom商品规格
        for custom_model in custom_models:
            product_model = ProductModel.objects.create(
                owner = request.manager,
                product = product,
                name = custom_model['name'],
                is_standard = False,
                price = custom_model['price'],
                weight = custom_model['weight'],
                stock_type = custom_model['stock_type'],
                stocks = custom_model['stocks'],
                user_code = custom_model['user_code']
            )

            for property in custom_model['properties']:
                ProductModelHasPropertyValue.objects.create(
                    model = product_model,
                    property_id = property['property_id'],
                    property_value_id = property['property_value_id']
                )

        #处理轮播图
        swipe_images = json.loads(request.POST.get('swipe_images', '[]'))
        for swipe_image in swipe_images:
            ProductSwipeImage.objects.create(
                product = product,
                url = swipe_image['url'],
                width = swipe_image['width'],
                height = swipe_image['height']
            )

        #商品后处理
        thumbnails_url = swipe_images[0]["url"]
        product.thumbnails_url = thumbnails_url
        product.save()

        #处理商品分类
        product_category_id = request.POST.get('product_category', -1)
        if product_category_id != -1:
            for category_id in product_category_id.split(','):
                if not category_id.isdigit():
                    continue
                cid = int(category_id)
                CategoryHasProduct.objects.create(category_id=cid, product_id=product.id)
                #ProductCategory.objects.filter(id=cid).update(product_count = F('product_count') + 1)

        #创建property
        properties = json.loads(request.POST.get('properties', '[]'))
        for property in properties:
            ProductProperty.objects.create(
                owner = request.manager,
                product = product,
                name = property['name'],
                value = property['value']
            )

        return HttpResponseRedirect('/mall/offshelf_products/get/')
    else:
        categories = ProductCategory.objects.filter(owner=request.manager)

        #确定支付接口配置
        pay_interface_config = {
            "online_pay_interfaces": [],
            "is_enable_cod_pay_interface": False
        }
        online_pay_interface_type_set = set(ONLINE_PAY_INTERFACE)
        pay_interfaces = list(PayInterface.objects.filter(owner=request.manager))
        for pay_interface in pay_interfaces:
            if not pay_interface.is_active:
                continue
            pay_interface.name = PAYTYPE2NAME[pay_interface.type]
            if pay_interface.type == PAY_INTERFACE_COD:
                pay_interface_config['is_enable_cod_pay_interface'] = True
            elif pay_interface.type == PAY_INTERFACE_WEIZOOM_COIN:
                pass
            else:
                pay_interface_config['online_pay_interfaces'].append(pay_interface)

        #确定运费配置
        system_postage_configs = list(PostageConfig.objects.filter(owner=request.manager, is_used=True))
        if len(system_postage_configs) > 0:
            system_postage_config = system_postage_configs[0]
        else:
            system_postage_config = None
        postage_config_info = {
            'system_postage_config': system_postage_config,
            'is_use_system_postage_config': True
        }

        #确定属性模板
        property_templates = ProductPropertyTemplate.objects.filter(owner=request.manager)

        type = request.GET.get('type', 'object')
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_second_navs(request),
            'second_nav_name': export.PRODUCT_ADD_PRODUCT_NAV,
            'categories': categories,
            'postage': postage,
            'pay_interface_config': pay_interface_config,
            'postage_config_info': postage_config_info,
            'property_templates': property_templates
        })
        if type == PRODUCT_INTEGRAL_TYPE:
            return render_to_response('mall/editor/edit_integral_product.html', c)
        else:
            return render_to_response('mall/editor/edit_product.html', c)


########################################################################
# update_product: 更新商品
########################################################################
@view(app='mall', resource='product', action='update')
@login_required
def update_product(request):
    """
    更新商品

    @note 对于商品信息，直接更新数据库中字段
    @note 对于商品规格，创建不存在的规格，更新已存在的规格，删除POST中不再有而db中还有的规格
    @note 对于轮播图，先删除db中与porduct关联的所有图片，然后根据POST中提交的图片完全重新创建
    @note 对于商品属性，创建不存在的属性，更新已存在的属性，删除POST中不再有而db中还有的属性。需要创建的属性在POST数据中id为－1，而需要更新的
    属性在POST数据中id为属性在db中的id。
    @note 对于分类信息，创建新的<product, category>关系，从db中删除POST中不存在的<product, category>关系，并更新category中的product计数
    """
    user = request.manager
    # 获取默认运费
    postage = None#module_api.get_default_postage_by_owner_id(user.id)
    # 获取在线支付
    pay_interface_onlines = []#module_api.get_pay_interface_onlines_by_owner_id(user.id)
    # 获取货到付款
    pay_interface_cod = []#module_api.get_pay_interface_cod_by_owner_id(user.id)

    #is_weizoom_mall_partner = AccountHasWeizoomCardPermissions.is_can_use_weizoom_card_by_owner_id(request.manager.id)
    if request.manager.is_weizoom_mall:
        is_weizoom_mall_partner = False
    if request.POST:
        #
        #获取轮播图集合
        #
        swipe_images = json.loads(request.POST.get('swipe_images', '[]'))
        thumbnails_url = swipe_images[0]["url"]

        #
        #更新product
        #
        postage_type = request.POST['postage_type']
        if postage_type == POSTAGE_TYPE_UNIFIED:
            postage_id = -1
            unified_postage_money = request.POST.get('unified_postage_money', 0.0)
        else:
            postage_id = 999#request.POST['postage_config_id']
            unified_postage_money = 0.0
        product_id = request.GET['id']

        if request.POST.get('weshop_sync', None):
            Product.objects.record_cache_args(ids=[product_id]).filter(owner=request.manager, id=product_id).update(
                name = request.POST.get('name', '').strip(),
                promotion_title = request.POST.get('promotion_title', '').strip(),
                user_code = request.POST.get('user_code', '').strip(),
                bar_code = request.POST.get('bar_code', '').strip(),
                thumbnails_url = thumbnails_url,
                detail = request.POST.get('detail', '').strip(),
                is_use_online_pay_interface = 'is_enable_online_pay_interface' in request.POST,
                is_use_cod_pay_interface = 'is_enable_cod_pay_interface' in request.POST,
                postage_id = postage_id,
                unified_postage_money = unified_postage_money,
                postage_type = postage_type,
                weshop_sync = request.POST.get('weshop_sync', None)
            )
        else:
            Product.objects.record_cache_args(ids=[product_id]).filter(owner=request.manager, id=product_id).update(
                name = request.POST.get('name', '').strip(),
                promotion_title = request.POST.get('promotion_title', '').strip(),
                user_code = request.POST.get('user_code', '').strip(),
                bar_code = request.POST.get('bar_code', '').strip(),
                thumbnails_url = thumbnails_url,
                detail = request.POST.get('detail', '').strip(),
                is_use_online_pay_interface = 'is_enable_online_pay_interface' in request.POST,
                is_use_cod_pay_interface = 'is_enable_cod_pay_interface' in request.POST,
                postage_id = postage_id,
                unified_postage_money = unified_postage_money,
                postage_type = postage_type)

        #
        #处理商品规格
        #
        standard_model, custom_models = __extract_product_model(request)
        #清除旧的custom product model
        existed_models = [product_model for product_model in ProductModel.objects.filter(owner=request.manager, product_id=product_id) if product_model.name != 'standard']
        existed_model_names = set([model.name for model in existed_models])

        #处理standard商品规格
        if ProductModel.objects.filter(product_id=product_id, name='standard').count() == 0:
            ProductModel.objects.create(
                owner = request.manager,
                product_id = product_id,
                name = 'standard',
                is_standard = True,
                price = standard_model['price'],
                weight = standard_model['weight'],
                stock_type = standard_model['stock_type'],
                stocks = standard_model['stocks'],
                user_code = standard_model['user_code']
            )
        else:
            ProductModel.objects.filter(product_id=product_id, name='standard').update(
                price = standard_model['price'],
                weight = standard_model['weight'],
                stock_type = standard_model['stock_type'],
                stocks = standard_model['stocks'],
                user_code = standard_model['user_code']
            )

        #处理custom商品规格
        updated_model_names = set()
        for custom_model in custom_models:
            custom_model_name = custom_model['name']
            if custom_model_name in existed_model_names:
                #model已经存在，更新之
                updated_model_names.add(custom_model_name) #记录被更新的model name
                ProductModel.objects.filter(product_id=product_id, name=custom_model_name).update(
                    price = custom_model['price'],
                    weight = custom_model['weight'],
                    stock_type = custom_model['stock_type'],
                    stocks = custom_model['stocks'],
                    user_code = custom_model['user_code'],
                    is_deleted = False
                )

                product_model = ProductModel.objects.get(product_id=product_id, name=custom_model_name)
                ProductModelHasPropertyValue.objects.filter(model=product_model).delete()
            else:
                #model不存在，创建之
                product_model = ProductModel.objects.create(
                    owner = request.manager,
                    product_id = product_id,
                    name = custom_model['name'],
                    is_standard = False,
                    price = custom_model['price'],
                    weight = custom_model['weight'],
                    stock_type = custom_model['stock_type'],
                    stocks = custom_model['stocks'],
                    user_code = custom_model['user_code']
                )

            for property in custom_model['properties']:
                ProductModelHasPropertyValue.objects.create(
                    model = product_model,
                    property_id = property['property_id'],
                    property_value_id = property['property_value_id']
                )

        #删除不用的models
        to_be_deleted_model_names = existed_model_names - updated_model_names
        ProductModel.objects.filter(product_id=product_id, name__in=to_be_deleted_model_names).update(is_deleted=True)

        #
        #处理轮播图
        #
        ProductSwipeImage.objects.filter(product_id=product_id).delete()
        for swipe_image in swipe_images:
            ProductSwipeImage.objects.create(
                product_id = product_id,
                url = swipe_image['url'],
                width = swipe_image['width'],
                height = swipe_image['height']
            )

        #
        # 处理property
        #
        properties = json.loads(request.POST.get('properties', '[]'))
        property_ids = set([property['id'] for property in properties])
        existed_property_ids = set([property.id for property in ProductProperty.objects.filter(product_id=product_id)])
        for property in properties:
            if property['id'] < 0:
                ProductProperty.objects.create(
                    owner = request.manager,
                    product_id = product_id,
                    name = property['name'],
                    value = property['value']
                )
            else:
                ProductProperty.objects.filter(id=property['id']).update(
                    name = property['name'],
                    value = property['value']
                )
        property_ids_to_be_delete = existed_property_ids - property_ids
        ProductProperty.objects.filter(id__in=property_ids_to_be_delete).delete()

        #
        #减少原category的product_count
        #
        user_category_ids = [category.id for category in ProductCategory.objects.filter(owner=request.manager)]
        old_category_ids = set([relation.category_id for relation in CategoryHasProduct.objects.filter(category_id__in=user_category_ids, product_id=product_id)])
        product_category_ids = request.POST.get('product_category', -1).split(',')

        for category_id in product_category_ids:
            if not category_id.isdigit():
                continue
            category_id = int(category_id)
            if category_id in old_category_ids:
                old_category_ids.remove(category_id)
            else:
                CategoryHasProduct.objects.create(category_id=category_id, product_id=product_id)
                ProductCategory.objects.filter(id=category_id).update(product_count = F('product_count') + 1)
        if len(old_category_ids) > 0:
            #存在被删除的ctegory关系，删除该关系
            CategoryHasProduct.objects.filter(category_id__in=old_category_ids, product_id=product_id).delete()
            ProductCategory.objects.filter(id__in=old_category_ids).update(product_count = F('product_count') - 1)

        source = request.GET.get('source','')
        if source == 'offshelf':
            return HttpResponseRedirect('/mall/offshelf_products/get/')
        elif source == 'onshelf':
            return HttpResponseRedirect('/mall/onshelf_products/get/')
        else:
            return HttpResponseRedirect('/mall/recycled_products/get/')
    else:
        #获取商品信息
        product_id = request.GET['id']
        product = Product.objects.get(id=product_id)
        Product.fill_details(request.manager, [product], {
            'with_product_model': True,
            'with_image': True,
            'with_property': True,
            'with_model_property_info': True,
            'with_all_category': True
        })

        #获取商品分类信息
        categories = product.categories

        #确定支付方式配置
        pay_interface_config = {
            "online_pay_interfaces": [],
            "is_enable_cod_pay_interface": False
        }
        online_pay_interface_type_set = set(ONLINE_PAY_INTERFACE)
        pay_interfaces = list(PayInterface.objects.filter(owner=request.manager))
        for pay_interface in pay_interfaces:
            if not pay_interface.is_active:
                continue
            pay_interface.name = PAYTYPE2NAME[pay_interface.type]
            if pay_interface.type == PAY_INTERFACE_COD:
                pay_interface_config['is_enable_cod_pay_interface'] = True
            else:
                pay_interface_config['online_pay_interfaces'].append(pay_interface)

        #确定运费配置
        system_postage_configs = list(PostageConfig.objects.filter(owner=request.manager, is_used=True))
        if len(system_postage_configs) > 0:
            system_postage_config = system_postage_configs[0]
        else:
            system_postage_config = None
        postage_config_info = {
            'system_postage_config': system_postage_config,
            'is_use_system_postage_config': False
        }

        if product.postage_type == POSTAGE_TYPE_CUSTOM:
            postage_config_info['is_use_system_postage_config'] = True
        '''
        if product.postage_id != -1:
            postage_config_info['is_use_system_postage_config'] = True
        '''

        #确定属性模板
        property_templates = ProductPropertyTemplate.objects.filter(owner=request.manager)

        product_type = request.GET.get('type', 'object')
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_second_navs(request),
            'second_nav_name': export.PRODUCT_ADD_PRODUCT_NAV,
            'product': product,
            'categories': categories,
            'pay_interface_config': pay_interface_config,
            'postage_config_info': postage_config_info,
            'property_templates': property_templates
        })
        if product_type == PRODUCT_INTEGRAL_TYPE:
            return render_to_response('mall/editor/edit_integral_product.html', c)
        else:
            return render_to_response('mall/editor/edit_product.html', c)
