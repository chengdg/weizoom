# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
import operator
from datetime import datetime
from itertools import chain
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from watchdog.utils import watchdog_warning

from core import paginator
from core import resource
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from mall import models  # 注意不要覆盖此module
from mall import signals as mall_signals
from . import utils
from mall import export

class ProductList(resource.Resource):
    app = 'mall2'
    resource = 'product_list'

    @login_required
    def get(request):
        """得到上架的类型商品


        Requirement:
          shelve_type(str): must be provided, the value range -> (0,1,2)
                            必须提供， 取值范围(0, 1, 2)

        Return:
          HttpResponse: the context in it include:{
            'first_nav_name',
            'second_navs',
            'second_nav_name',
            'has_product'
          }

        Raise:
          if shelve_type is not be provided the TypeError will be raise
          如果shelve_type没有被提供， 将触发TypeError异常
        """
        shelve_type = int(request.GET.get("shelve_type", 1))
        has_product = models.Product.objects.filter(
            owner=request.manager,
            shelve_type=shelve_type,
            is_deleted=False
        ).exists()
        c = RequestContext(
            request,
            {'first_nav_name': export.PRODUCT_FIRST_NAV,
             'second_navs': export.get_second_navs(request),
             'has_product': has_product}
        )
        if shelve_type == models.PRODUCT_SHELVE_TYPE_ON:
            c.update({'second_nav_name': export.PRODUCT_MANAGE_ON_SHELF_PRODUCT_NAV})
            return render_to_response('mall/editor/onshelf_products.html', c)
        elif shelve_type == models.PRODUCT_SHELVE_TYPE_OFF:
            c.update({'second_nav_name': export.PRODUCT_MANAGE_OFF_SHELF_PRODUCT_NAV})
            return render_to_response('mall/editor/offshelf_products.html', c)
        elif shelve_type == models.PRODUCT_SHELVE_TYPE_RECYCLED:
            c.update({'second_nav_name': export.PRODUCT_MANAGE_RECYCLED_PRODUCT_NAV})
            return render_to_response('mall/editor/recycled_products.html', c)
        else:
            return Http404("Poll does not exist")

    @login_required
    def api_get(request):
        """获取商品列表
        API:
            method: get
            url: mall2/product_list/

        Args:
          type: 上架类型
            取值以及说明:
              onshelf  : 上架
              offshelf : 下架
              recycled : 回收站
              delete   : 删除

        """
        COUNT_PER_PAGE = 10
        _type = request.GET.get('type', 'onshelf')

        #处理排序
        sort_attr = request.GET.get('sort_attr', None)
        if not sort_attr:
            sort_attr = '-display_index'

        #处理商品分类
        if _type == 'offshelf':
            sort_attr = '-update_time'
            products = models.Product.objects.filter(
                owner=request.manager,
                shelve_type=models.PRODUCT_SHELVE_TYPE_OFF,
                is_deleted=False)
        elif _type == 'onshelf':
            products = models.Product.objects.filter(
                owner=request.manager,
                shelve_type=models.PRODUCT_SHELVE_TYPE_ON,
                is_deleted=False)
        elif _type == 'recycled':
            products = models.Product.objects.filter(
                owner=request.manager,
                shelve_type=models.PRODUCT_SHELVE_TYPE_RECYCLED,
                is_deleted=False)
        else:
            products = models.Product.objects.filter(
                owner=request.manager,
                is_deleted=False)

        # import pdb
        # pdb.set_trace()
        #未回收的商品
        models.Product.fill_details(request.manager, products, {
            "with_product_model": True,
            "with_model_property_info": True,
            "with_selected_category": True,
            'with_image': False,
            'with_property': True,
            'with_sales': True
        })
        # pdb.set_trace()
        # products = products.order_by(sort_attr)
        if '-' in sort_attr:
            sort_attr = sort_attr.replace('-', '')
            products = sorted(products, key=operator.attrgetter('id'), reverse=True)
            products = sorted(products, key=operator.attrgetter(sort_attr), reverse=True)
            sort_attr = '-' + sort_attr
        else:
            products = sorted(products, key=operator.attrgetter('id'))
            products = sorted(products, key=operator.attrgetter(sort_attr))
        products_is_0 = filter(lambda p: p.display_index == 0, products)
        products_not_0 = filter(lambda p: p.display_index != 0, products)
        products_not_0 = sorted(products_not_0, key=operator.attrgetter('display_index'))

        products = utils.filter_products(request, products_not_0 + products_is_0)

        #进行分页
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, products = paginator.paginate(
            products,
            cur_page,
            count_per_page,
            query_string=request.META['QUERY_STRING'])

        #构造返回数据
        items = []
        for product in products:
            product_dict = product.format_to_dict()
            product_dict['is_self'] = (request.manager.id == product.owner_id)
            items.append(product_dict)

        data = dict()
        data['owner_id'] = request.manager.id
        response = create_response(200)
        response.data = {
            'items': items,
            'pageinfo': paginator.to_dict(pageinfo),
            'sortAttr': sort_attr,
            'data': data
        }
        return response.get_response()

    @login_required
    def api_post(request):
        """批量更新one or more商品的上架状态


        Args:
          id/ids/ids[]:
            id   : 更新单个商品
            ids  : 更新多个商品
            ids[]: 更新多个商品 (为向前兼容)
          shelve_type: 上架类型
            取值以及说明:
              onshelf  : 上架
              offshelf : 下架
              recycled : 回收站
              delete   : 删除



        """
        ids = request.POST.getlist('ids', [])
        _ids = request.POST.getlist('ids[]', [])
        ids = ids if ids else _ids
        p_id = request.POST.get('id')
        if p_id:
            ids.append(int(p_id))
        if not ids:
            return create_response(200).get_response()

        #
        prev_shelve_type = models.Product.objects.get(
            id=ids[0]).shelve_type
        shelve_type = request.POST['shelve_type']

        is_deleted = False
        if shelve_type == 'onshelf':
            shelve_type = models.PRODUCT_SHELVE_TYPE_ON
        elif shelve_type == 'offshelf':
            shelve_type = models.PRODUCT_SHELVE_TYPE_OFF
        elif shelve_type == 'recycled':
            shelve_type = models.PRODUCT_SHELVE_TYPE_RECYCLED
        elif shelve_type == 'delete':
            is_deleted = True

        products = models.Product.objects.filter(id__in=ids)
        if is_deleted:
            products.update(is_deleted=True)
        else:
            # 更新商品上架状态以及商品排序
            if request.manager.id == products[0].owner_id:
                now = datetime.now()
                if shelve_type != models.PRODUCT_SHELVE_TYPE_ON:
                    products.update(shelve_type=shelve_type, weshop_status=shelve_type, is_deleted=False, display_index=0, update_time=now)
                else:
                    products.update(shelve_type=shelve_type, is_deleted=False, display_index=0, update_time=now)
            else:
                # 微众商城更新商户商品状态
                products.update(weshop_status=shelve_type)

        is_prev_shelve = prev_shelve_type == models.PRODUCT_SHELVE_TYPE_ON
        is_not_sale = shelve_type != models.PRODUCT_SHELVE_TYPE_ON

        if is_prev_shelve and is_not_sale or is_deleted:
            # 商品不再处于上架状态，发出product_not_offline signal
            product_ids = [int(id) for id in ids]
            mall_signals.products_not_online.send(
                sender=models.Product,
                product_ids=product_ids,
                request=request
            )

        response = create_response(200)
        return response.get_response()




class Product(resource.Resource):
    app = 'mall2'
    resource = 'product'

    @login_required
    def get(request):
        """
        商品创建页&&商品更新页
        """
        # 如果有product说明更新， 否则说明创建
        has_product_id = request.GET.get('id')
        has_product_id = int(has_product_id) if has_product_id else 0

        if has_product_id:
            try:
                product = models.Product.objects.get(id=has_product_id)
            except models.Product.DoesNotExist:
                return Http404
            products = [product]
            models.Product.fill_details(request.manager, products, {
                'with_product_model': True,
                'with_image': True,
                'with_property': True,
                'with_model_property_info': True,
                'with_all_category': True,
                'with_sales': True
            })

            #获取商品分类信息
            categories = product.categories
        else:
            product = {}
            categories = models.ProductCategory.objects.filter(
                owner=request.manager)

        # 确定支付接口配置
        pay_interface_config = {
            "online_pay_interfaces": [],
            "is_enable_cod_pay_interface": False
        }
        pay_interfaces = chain(
            models.PayInterface.objects.filter(owner=request.manager))
        for pay_interface in pay_interfaces:
            if not pay_interface.is_active:
                continue
            pay_interface.name = models.PAYTYPE2NAME[pay_interface.type]
            if pay_interface.type == models.PAY_INTERFACE_COD:
                pay_interface_config['is_enable_cod_pay_interface'] = True
            elif pay_interface.type == models.PAY_INTERFACE_WEIZOOM_COIN:
                pass
            else:
                pay_interface_config['online_pay_interfaces'].append(
                    pay_interface)

        # 确定运费配置(对应表: mall_postage_config)
        system_postage_configs = models.PostageConfig.objects.filter(
            owner=request.manager, is_used=True)
        if system_postage_configs.exists():
            system_postage_config = system_postage_configs[0]
        else:
            system_postage_config = None
        postage_config_info = {
            'system_postage_config': system_postage_config,
            'is_use_system_postage_config': False
        }

        if (hasattr(product, 'postage_type') and
                product.postage_type == models.POSTAGE_TYPE_CUSTOM):
            postage_config_info['is_use_system_postage_config'] = True

        # 确定属性模板
        property_templates = models.ProductPropertyTemplate.objects.filter(
            owner=request.manager)

        _type = request.GET.get('type', 'object')
        c = RequestContext(request, {
            'first_nav_name': export.PRODUCT_FIRST_NAV,
            'second_navs': export.get_second_navs(request),
            'second_nav_name': export.PRODUCT_ADD_PRODUCT_NAV,
            'product': product,
            'categories': categories,
            'postage': '',
            'pay_interface_config': pay_interface_config,
            'postage_config_info': postage_config_info,
            'property_templates': property_templates
        })
        if _type == models.PRODUCT_INTEGRAL_TYPE:
            return render_to_response('mall/editor/edit_integral_product.html', c)
        else:
            return render_to_response('mall/editor/edit_product.html', c)

    @login_required
    def put(request):
        """创建商品or update product
        """

        standard_model, custom_models = utils.extract_product_model(request)
        postage_type = request.POST['postage_type']
        if postage_type == models.POSTAGE_TYPE_UNIFIED:
            postage_id = -1
            unified_postage_money = request.POST.get(
                'unified_postage_money', '')
            if unified_postage_money == '':
                unified_postage_money = 0.0
        else:
            postage_id = 0
            unified_postage_money = 0.0

        min_limit = request.POST.get('min_limit', '0')
        if not min_limit.isdigit():
            min_limit = 0
        else:
            min_limit = float(min_limit)

        product = models.Product.objects.create(
            owner=request.manager,
            name=request.POST.get('name', '').strip(),
            promotion_title=request.POST.get('promotion_title', '').strip(),
            user_code=request.POST.get('user_code', '').strip(),
            bar_code=request.POST.get('bar_code', '').strip(),
            thumbnails_url=request.POST.get('thumbnails_url', '').strip(),
            pic_url=request.POST.get('pic_url', '').strip(),
            detail=request.POST.get('detail', '').strip(),
            type=request.POST.get('type', models.PRODUCT_DEFAULT_TYPE),
            is_use_online_pay_interface='is_enable_online_pay_interface' in request.POST,
            is_use_cod_pay_interface='is_enable_cod_pay_interface' in request.POST,
            postage_type=postage_type,
            postage_id=postage_id,
            unified_postage_money=unified_postage_money,
            weshop_sync=request.POST.get('weshop_sync', 0),
            stocks=min_limit,
            is_member_product=request.POST.get("is_member_product", False) == 'on'
        )
        # 设置新商品显示顺序
        # product.display_index = models.Product.objects.filter(
        #     owner=request.manager
        # ).order_by('-display_index').first().display_index + 1
        # 处理商品排序
        display_index = int(request.POST.get('display_index', '0'))
        if display_index > 0:
            product.move_to_position(display_index)

        # 处理standard商品规格
        models.ProductModel.objects.create(
            owner=request.manager,
            product=product,
            name='standard',
            is_standard=True,
            price=standard_model['price'],
            weight=standard_model['weight'],
            stock_type=standard_model['stock_type'],
            stocks=standard_model['stocks'],
            user_code=standard_model['user_code']
        )

        # 处理custom商品规格
        for custom_model in custom_models:
            product_model = models.ProductModel.objects.create(
                owner=request.manager,
                product=product,
                name=custom_model['name'],
                is_standard=False,
                price=custom_model['price'],
                weight=custom_model['weight'],
                stock_type=custom_model['stock_type'],
                stocks=custom_model['stocks'],
                user_code=custom_model['user_code']
            )

            for property in custom_model['properties']:
                models.ProductModelHasPropertyValue.objects.create(
                    model=product_model,
                    property_id=property['property_id'],
                    property_value_id=property['property_value_id']
                )

        # 处理轮播图
        swipe_images = request.POST.get('swipe_images', '')
        if len(swipe_images) == 0:
            swipe_images = []
        else:
            swipe_images = json.loads(swipe_images)
        if len(swipe_images) == 0:
            thumbnails_url = ''
        else:
            thumbnails_url = swipe_images[0]["url"]

        for swipe_image in swipe_images:
            if swipe_image['width'] and swipe_image['height']:
                models.ProductSwipeImage.objects.create(
                    product=product,
                    url=swipe_image['url'],
                    width=swipe_image['width'],
                    height=swipe_image['height']
                )

        # 商品后处理
        if swipe_images:
            thumbnails_url = swipe_images[0]["url"]
        else:
            thumbnails_url = ''
        product.thumbnails_url = thumbnails_url
        product.save()

        # 处理商品分类
        product_category_id = request.POST.get('product_category', -1)
        if product_category_id != -1:
            for category_id in product_category_id.split(','):
                if not category_id.isdigit():
                    continue
                cid = int(category_id)
                models.CategoryHasProduct.objects.create(
                    category_id=cid,
                    product_id=product.id)
        # 创建property
        properties = json.loads(request.POST.get('properties', '[]'))
        for property in properties:
            models.ProductProperty.objects.create(
                owner=request.manager,
                product=product,
                name=property['name'],
                value=property['value']
            )

        return HttpResponseRedirect(
            '/mall2/product_list/?shelve_type=%d' % (
                models.PRODUCT_SHELVE_TYPE_OFF,)
        )

    @login_required
    def post(request):
        """更新商品


        API:
          method: post
          url: /mall2/product/?id=%d&?shelve_type=%d

        Note:
          对于商品信息，直接更新数据库中字段.
          对于商品规格，创建不存在的规格，更新已存在的规格，删除POST中不再有而db中还有的规
            格.
          对于轮播图，先删除db中与porduct关联的所有图片，然后根据POST中提交的图片完全重新
            创建.
          对于商品属性，创建不存在的属性，更新已存在的属性，删除POST中不再有而db中还有的
            属性。需要创建的属性在POST数据中id为－1，而需要更新的属性在POST数据中id为属性
            在db中的id.
          对于分类信息，创建新的<product, category>关系，从db中删除POST中不存在的
            <product, category>关系，并更新category中的product计数.
        """

        # 获取默认运费
        source = int(request.GET.get('shelve_type', 0))
        swipe_images = request.POST.get('swipe_images', '[]')
        if not swipe_images:
            url = '/mall2/product_list/?shelve_type=%d' % int(request.GET.get('shelve_type', 0))
            return HttpResponseRedirect(url)
        else:
            swipe_images = json.loads(swipe_images)
        thumbnails_url = swipe_images[0]["url"]

        # 更新product
        postage_type = request.POST['postage_type']
        if postage_type == models.POSTAGE_TYPE_UNIFIED:
            postage_id = -1
            unified_postage_money = request.POST.get(
                'unified_postage_money', '')
            if unified_postage_money == '':
                unified_postage_money = 0.0
        else:
            postage_id = 999  # request.POST['postage_config_id']
            unified_postage_money = 0.0
        product_id = request.GET.get('id')

        min_limit = request.POST.get('min_limit', '0')
        if not min_limit.isdigit():
            min_limit = 0
        else:
            min_limit = float(min_limit)
        if request.POST.get('weshop_sync', None):
            models.Product.objects.record_cache_args(
                ids=[product_id]
            ).filter(
                owner=request.manager,
                id=product_id
            ).update(
                name=request.POST.get('name', '').strip(),
                promotion_title=request.POST.get(
                    'promotion_title', '').strip(),
                user_code=request.POST.get('user_code', '').strip(),
                bar_code=request.POST.get('bar_code', '').strip(),
                thumbnails_url=thumbnails_url,
                detail=request.POST.get('detail', '').strip(),
                is_use_online_pay_interface='is_enable_online_pay_interface' in request.POST,
                is_use_cod_pay_interface='is_enable_cod_pay_interface' in request.POST,
                postage_id=postage_id,
                unified_postage_money=unified_postage_money,
                postage_type=postage_type,
                weshop_sync=request.POST.get('weshop_sync', None),
                stocks=min_limit,
                is_member_product=request.POST.get("is_member_product", False) == 'on'

            )
        else:
            models.Product.objects.record_cache_args(
                ids=[product_id]
            ).filter(
                owner=request.manager,
                id=product_id
            ).update(
                name=request.POST.get('name', '').strip(),
                promotion_title=request.POST.get(
                    'promotion_title', '').strip(),
                user_code=request.POST.get('user_code', '').strip(),
                bar_code=request.POST.get('bar_code', '').strip(),
                thumbnails_url=thumbnails_url,
                detail=request.POST.get('detail', '').strip(),
                is_use_online_pay_interface='is_enable_online_pay_interface' in request.POST,
                is_use_cod_pay_interface='is_enable_cod_pay_interface' in request.POST,
                postage_id=postage_id,
                unified_postage_money=unified_postage_money,
                postage_type=postage_type,
                stocks=min_limit,
                is_member_product=request.POST.get("is_member_product", False) == 'on'
            )

        # 处理商品排序
        display_index = int(request.POST.get('display_index', '0'))
        if display_index > 0:
            models.Product.objects.get(id=product_id).move_to_position(display_index)

        # 处理商品规格
        standard_model, custom_models = utils.extract_product_model(request)

        # 处理standard商品规格
        has_product_model = models.ProductModel.objects.filter(
            product_id=product_id,
            name='standard').exists()
        if not has_product_model:
            models.ProductModel.objects.create(
                owner=request.manager,
                product_id=product_id,
                name='standard',
                is_standard=True,
                price=standard_model['price'],
                weight=standard_model['weight'],
                stock_type=standard_model['stock_type'],
                stocks=standard_model['stocks'],
                user_code=standard_model['user_code']
            )
        elif standard_model.get('is_deleted', None):
            models.ProductModel.objects.filter(
                product_id=product_id,
                name='standard'
            ).update(is_deleted=True)
        else:
            models.ProductModel.objects.filter(
                product_id=product_id, name='standard'
            ).update(
                price=standard_model['price'],
                weight=standard_model['weight'],
                stock_type=standard_model['stock_type'],
                stocks=standard_model['stocks'],
                user_code=standard_model['user_code'],
                is_deleted=False
            )

        # 清除旧的custom product model
        existed_models = [product_model for product_model in models.ProductModel.objects.filter(
                owner=request.manager,
                product_id=product_id
        ) if product_model.name != 'standard']
        existed_model_names = set([model.name for model in existed_models])

        # 处理custom商品规格
        updated_model_names = set()
        for custom_model in custom_models:
            custom_model_name = custom_model['name']
            if custom_model_name in existed_model_names:
                # model已经存在，更新之
                # # 记录被更新的model name
                updated_model_names.add(custom_model_name)
                models.ProductModel.objects.filter(
                    product_id=product_id, name=custom_model_name
                ).update(
                    price=custom_model['price'],
                    weight=custom_model['weight'],
                    stock_type=custom_model['stock_type'],
                    stocks=custom_model['stocks'],
                    user_code=custom_model['user_code'],
                    is_deleted=False
                )

                product_model = models.ProductModel.objects.get(
                    product_id=product_id, name=custom_model_name)
                models.ProductModelHasPropertyValue.objects.filter(
                    model=product_model).delete()
            else:
                # model不存在，创建之
                product_model = models.ProductModel.objects.create(
                    owner=request.manager,
                    product_id=product_id,
                    name=custom_model['name'],
                    is_standard=False,
                    price=custom_model['price'],
                    weight=custom_model['weight'],
                    stock_type=custom_model['stock_type'],
                    stocks=custom_model['stocks'],
                    user_code=custom_model['user_code']
                )

            for property in custom_model['properties']:
                models.ProductModelHasPropertyValue.objects.create(
                    model=product_model,
                    property_id=property['property_id'],
                    property_value_id=property['property_value_id']
                )

        # 删除不用的models
        to_be_deleted_model_names = existed_model_names - updated_model_names
        models.ProductModel.objects.filter(
            product_id=product_id, name__in=to_be_deleted_model_names
        ).update(is_deleted=True)

        # 处理轮播图
        models.ProductSwipeImage.objects.filter(
            product_id=product_id
        ).delete()
        for swipe_image in swipe_images:
            models.ProductSwipeImage.objects.create(
                product_id=product_id,
                url=swipe_image['url'],
                width=swipe_image['width'],
                height=swipe_image['height']
            )

        # 处理property
        properties = request.POST.get('properties')
        properties = json.loads(properties) if properties else []
        property_ids = set([property['id'] for property in properties])
        existed_property_ids = set([
            property.id for property in models.ProductProperty.objects.filter(
                product_id=product_id)
            ])
        for property in properties:
            if property['id'] < 0:
                models.ProductProperty.objects.create(
                    owner=request.manager,
                    product_id=product_id,
                    name=property['name'],
                    value=property['value']
                )
            else:
                models.ProductProperty.objects.filter(
                    id=property['id']
                ).update(name=property['name'], value=property['value'])
        property_ids_to_be_delete = existed_property_ids - property_ids
        models.ProductProperty.objects.filter(
            id__in=property_ids_to_be_delete).delete()

        # 减少原category的product_count
        user_category_ids = [
            category.id for category in models.ProductCategory.objects.filter(
                owner=request.manager)]
        old_category_ids = set([relation.category_id for relation in models.CategoryHasProduct.objects.filter(
            category_id__in=user_category_ids, product_id=product_id)])
        catetories_ids = request.POST.get('product_category', -1).split(',')

        for category_id in catetories_ids:
            if not category_id.isdigit():
                continue
            category_id = int(category_id)
            if category_id in old_category_ids:
                old_category_ids.remove(category_id)
            else:
                models.CategoryHasProduct.objects.create(
                    category_id=category_id, product_id=product_id)
                models.ProductCategory.objects.filter(
                    id=category_id
                ).update(product_count=F('product_count') + 1)
        if len(old_category_ids) > 0:
            # 存在被删除的ctegory关系，删除该关系
            models.CategoryHasProduct.objects.filter(
                category_id__in=old_category_ids, product_id=product_id
            ).delete()
            models.ProductCategory.objects.filter(
                id__in=old_category_ids
            ).update(product_count=F('product_count') - 1)

        if source == models.PRODUCT_SHELVE_TYPE_OFF:
            url = '/mall2/product_list/?shelve_type=%d' % (models.PRODUCT_SHELVE_TYPE_OFF, )
            return HttpResponseRedirect(url)
        elif source == models.PRODUCT_SHELVE_TYPE_ON:
            url = '/mall2/product_list/?shelve_type=%d' % (models.PRODUCT_SHELVE_TYPE_ON, )
            return HttpResponseRedirect(url)
        else:
            url = '/mall2/product_list/?shelve_type=%d' % (models.PRODUCT_SHELVE_TYPE_RECYCLED, )
            return HttpResponseRedirect(url)

    def api_post(request):
        """根据update_type，更新对应的商品信息.

        Args:
          update_type:
            update_pos: 更新商品位置信息
              id: product.id
              pos: product new position
        """
        try:
            if request.POST.get('update_type', '') == 'update_pos':
                id = request.POST.get('id')
                pos = int(request.POST.get('pos'))
                product = models.Product.objects.get(id=id)
                product.move_to_position(pos)
                response = create_response(200)
                return response.get_response()
        except:
            watchdog_warning(
                u"failed to update, cause:\n{}".format(unicode_full_stack())
            )
            response = create_response(500)
            return response.get_response()


class ProductFilterParams(resource.Resource):
    app = 'mall2'
    resource = 'product_filter_param'

    @login_required
    def api_get(request):
        """获取商品过滤参数

        Return:
          json:

          example:
            {
                categories: [{
                    id: 1,
                    name: "分类1"
                }, {
                    "id: 2,
                    name: "分类2"
                }, {
                    ......
                }]
            }
        """
        categories = []
        user_product_categorys = models.ProductCategory.objects.filter(
            owner=request.manager
        )
        for category in user_product_categorys:
            categories.append({
                "id": category.id,
                "name": category.name
            })

        response = create_response(200)
        response.data = {
            'categories': categories
        }
        return response.get_response()


class ProductModel(resource.Resource):
    app = 'mall2'
    resource = 'product_model'

    @login_required
    def api_post(request):
        """更新商品规格库存

        Args:
          model_infos: 商品规格信息

          example:
            [{
                id: 1,
                stock_type: "limit", //库存类型
                stocks: 3 //库存数量
            }, {
                id: 2,
                stock_type: "unlimit",
                stocks: 0
            }, {
                ......
            }]
        """
        model_infos = json.loads(request.POST.get('model_infos', '[]'))
        for model_info in model_infos:
            stock_type = models.PRODUCT_STOCK_TYPE_UNLIMIT
            if model_info['stock_type'] == 'limit':
                stock_type = models.PRODUCT_STOCK_TYPE_LIMIT

            product_model_id = model_info['id']
            stocks = model_info['stocks']
            if stock_type == models.PRODUCT_STOCK_TYPE_UNLIMIT:
                stocks = 0
            models.ProductModel.objects.filter(
                id=product_model_id
            ).update(stock_type=stock_type, stocks=stocks)

        response = create_response(200)
        return response.get_response()
