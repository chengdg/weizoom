# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
from operator import attrgetter
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from mall.promotion.utils import verification_multi_product_coupon
from .. import models as mall_models
from .. import export
from . import utils as category_ROA_utils
from core import resource, paginator
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_warning


class Categories(resource.Resource):
    """
    分组列表通用类，只返回分组本身信息
    """
    app = 'mall2'
    resource = 'categories'

    @login_required
    def api_get(request):
        filter_name = request.GET.get('filter_name', '')
        categories = mall_models.ProductCategory.objects.filter(
            owner=request.manager)
        if filter_name:
            categories = categories.filter(name__contains=filter_name)
        count_per_page = int(request.GET.get('count_per_page', 10))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, categories = paginator.paginate(
            categories, cur_page, count_per_page,
            query_string=request.META['QUERY_STRING'])

        items = []
        for category in categories:
            data = {
                'id': category.id,
                'name': category.name,
                'created_at': category.created_at.strftime("%Y-%m-%d %H:%M")
            }
            items.append(data)

        response = create_response(200)
        response.data = {
            'items': items,
            'pageinfo': paginator.to_dict(pageinfo),
            'sortAttr': '',
            'data': {}
        }
        return response.get_response()


class CategoryProducts(resource.Resource):
    app = 'mall2'
    resource = 'category_products'

    @login_required
    def api_get(request):
        category_ids = request.GET.get('category_ids', '').split(',')
        relations = mall_models.CategoryHasProduct.objects.filter(
            category_id__in=category_ids)

        product_ids = set([relation.product_id for relation in relations])

        _, error_product_ids = verification_multi_product_coupon(request.manager, product_ids)

        product_ids = list(set(product_ids) - set(error_product_ids))

        products = list(mall_models.Product.objects.filter(
            owner=request.manager, is_deleted=False, shelve_type=mall_models.PRODUCT_SHELVE_TYPE_ON,id__in=product_ids))

        mall_models.Product.fill_details(request.manager,
                                         products,
                                         {"with_product_model": True,
                                          "with_model_property_info": True,
                                          'with_sales': True})

        mall_models.Product.fill_details(request.manager,
                             products,
                                    {"with_product_model": True,
                                     "with_model_property_info": True,
                                     'with_sales': True})

        id2product = {}
        for product in products:
            data = product.format_to_dict()
            id2product[product.id] = data
        items = id2product.values()
        items.sort(lambda x, y: cmp(x['id'], y['id']))
        response = create_response(200)
        response.data = {
            'products': items
        }
        return response.get_response()



class CategoryList(resource.Resource):
    app = 'mall2'
    resource = 'category_list'

    @login_required
    def get(request):
        """
        商品分类列表页面
        """
        #获取category集合
        product_categories = mall_models.ProductCategory.objects.filter(
            owner=request.manager)

        category_ROA_utils.sorted_products(request.manager.id, product_categories, True)

        c = RequestContext(request, {
                    'first_nav_name': export.PRODUCT_FIRST_NAV,
                    'second_navs': export.get_mall_product_second_navs(request),
                    'second_nav_name': export.PRODUCT_MANAGE_CATEGORY_NAV,
                    'product_categories': product_categories}
        )
        return render_to_response('mall/editor/product_categories.html', c)

    @login_required
    def api_get(request):
        """
        功能1: 获得商品分类的可选商品列表

        Args:
          id:
          action:

        可选商品指的是还不属于当前分类的商品.
          可选商品集合 ＝ manager的所有商品集合 － 已经在分类中的商品集合

        功能2: 获取指定排序的分类

        Args:
          action: 'sorted'
          category_id:
          reverse: 'true' or 'false'

        """
        action = request.GET.get('action')
        category_id = int(request.GET.get('id'))
        if not action:
            COUNT_PER_PAGE = 20
            name_query = request.GET.get('name')

            #获取商品集合
            products = list(mall_models.Product.objects.filter(
                owner=request.manager, is_deleted=False).exclude(
                shelve_type=mall_models.PRODUCT_SHELVE_TYPE_RECYCLED))
            # 微众商城代码
            #duhao 20151120
            #当在 商品-分组管理 页面管理分组时，弹出的商品列表应该只包含商城自己商品列表里的在售商品
            # if request.manager.id == 216:
            #     _products = []
            #     for product in products:
            #         if product.owner_id == 216 or (product.weshop_sync > 0 and product.shelve_type == mall_models.PRODUCT_SHELVE_TYPE_ON and \
            #             product.weshop_status in (mall_models.PRODUCT_SHELVE_TYPE_ON, mall_models.PRODUCT_SHELVE_TYPE_OFF)):
            #             product.shelve_type = product.weshop_status
            #             _products.append(product)
            #     products = _products
                    
            if name_query:
                products = [
                    product for product in products if name_query in product.name
                ]

            if category_id != -1:
                #获取已在分类中的商品
                relations = mall_models.CategoryHasProduct.objects.filter(
                    category_id=category_id)
                existed_product_ids = set(
                    [relation.product_id for relation in relations]
                )

                #获取没在分类中的商品集合(分类的可选商品集合)
                products = filter(
                    lambda product: (product.id not in existed_product_ids),
                    products
                )
            products.sort(lambda x,y: cmp(y.id, x.id))
            products.sort(lambda x,y: cmp(y.update_time, x.update_time))

            #进行分页
            count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
            cur_page = int(request.GET.get('page', '1'))
            pageinfo, products = paginator.paginate(
                products,
                cur_page,
                count_per_page,
                query_string=request.META['QUERY_STRING'])

            mall_models.Product.fill_display_price(products)
            mall_models.Product.fill_details(request.manager,
                                             products,
                                             {'with_sales': True})
            result_products = []
            for product in products:
                relation = '%s_%s' % (category_id, product.id)
                result_products.append({
                    "id": product.id,
                    "name": product.name,
                    "display_price": product.display_price,
                    "status": product.status,
                    "sales": product.sales if product.sales else -1,
                    "update_time": product.update_time.strftime("%Y-%m-%d")
                })
            # result_products.sort(lambda x,y: cmp(y['update_time'], x['update_time']))

            response = create_response(200)
            response.data = {
                'items': result_products,
                'pageinfo': paginator.to_dict(pageinfo),
                'sortAttr': '',
                'data': {}
            }
            return response.get_response()
        elif action == 'sorted':
            reverse = json.loads(request.GET.get('reverse', 'true'))
            #获取category集合
            product_categories = mall_models.ProductCategory.objects.filter(
                id=category_id)

            category_ROA_utils.sorted_products(request.manager.id, product_categories, reverse)

            response = create_response(200)
            response.data = {
                'product_categories': product_categories
            }
            return response.get_response()


    @login_required
    def put(request):
        """创建商品分类
        """

    @login_required
    def api_post(request):
        """更新商品排序

        Args:
          category_id:
          product_id:
          position:
        """
        try:
            category_id = request.POST.get('category_id')
            product_id = request.POST.get('product_id')
            position = request.POST.get('position')
            category_has_product = mall_models.CategoryHasProduct.objects.get(
                category_id=category_id,
                product_id=product_id
            )
            category_has_product.move_to_position(position)
            response = create_response(200)
            return response.get_response()
        except:
            watchdog_warning(
                u"更新商品分组商品排序失败, cause:\n{}".format(unicode_full_stack())
            )
            response = create_response(500)
            return response.get_response()


class Category(resource.Resource):
    app = 'mall2'
    resource = 'category'

    @login_required
    def api_put(request):
        """创建商品分类

        method: put
        args: {'name': 'str',
               'product_ids': ''}

        """
        # pdb.set_trace()
        if request.POST:
            product_category = mall_models.ProductCategory.objects.create(
                owner=request.manager,
                name=request.POST.get('name', '').strip()
            )
            product_ids = request.POST.getlist('product_ids[]')
            product_category.product_count = len(product_ids)
            product_category.save()

            for product_id in product_ids:
                mall_models.CategoryHasProduct.objects.create(
                    product_id=product_id,
                    category=product_category
                )
            return create_response(200).get_response()

    @login_required
    def api_post(request):
        """更新商品分类

        Args:
          id: 分类id
          name: 新的分类名
          product_ids: 新的属于该分类的商品id集合

        """
        category_id = request.POST['id']
        product_ids = request.POST.getlist('product_ids[]')
        product_categorys = mall_models.ProductCategory.objects.filter(id=category_id)
        if 0 != product_categorys.count():
            product_categorys.update(
            name=request.POST.get('name', '').strip(),
            product_count=len(product_ids)
            )
        else:
            response = create_response(500)
            response.data = {'msg':"该商品分类已不存在"}
            return response.get_response()
        #重建<category, product>关系
        for product_id in product_ids:
            mall_models.CategoryHasProduct.objects.create(
                product_id=product_id,
                category_id=category_id)

        return create_response(200).get_response()

    @login_required
    def api_delete(request):
        """删除商品分类or商品分类删除一个商品

        Args:
          category_id: 分类id
          product_id: 商品id  # 对删除商品分类可选
        """

        product_id = request.POST.get('product_id')
        category_id = request.POST.get('category_id')
        # import pdb
        # pdb.set_trace()
        if product_id:
            mall_models.CategoryHasProduct.objects.filter(
                product_id=product_id,
                category_id=category_id
            ).delete()
        elif category_id:
            mall_models.ProductCategory.objects.filter(
                owner=request.manager,
                id=category_id
            ).delete()

        return create_response(200).get_response()
