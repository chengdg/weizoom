# -*- coding: utf-8 -*-
from __future__ import absolute_import
from datetime import datetime
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


from .. import models as mall_models
from .. import export
from core import resource, paginator
from core.jsonresponse import create_response


class CategoryList(resource.Resource):
    app = 'mall2'
    resource = 'category_list'

    @login_required
    def get(request):
        """商品分类列表页面
        """
        #获取category集合
        product_categories = mall_models.ProductCategory.objects.filter(
            owner=request.manager)

        #获取与category关联的product集合
        category_ids = (category.id for category in product_categories)
        relations = mall_models.CategoryHasProduct.objects.filter(
                        category_id__in=category_ids)
        category2products = {}
        relation2time = {}
        product_ids = set()
        for relation in relations:
            category2products.setdefault(relation.category_id, [])
            category2products[relation.category_id].append(relation.product_id)
            key = '%s_%s' % (relation.category_id, relation.product_id)
            relation2time[key] = relation.created_at
            product_ids.add(relation.product_id)

        products = [product for product in mall_models.Product.objects.filter(
            owner=request.manager,
            id__in=product_ids) if not product.is_deleted]
        mall_models.Product.fill_display_price(products)
        mall_models.Product.fill_sales_detail(request.manager.id, products, [product.id for product in products])
        id2product = dict([(product.id, product) for product in products])

        empty_list = []
        today = datetime.today()
        for category in product_categories:
            category.products = []
            for product_id in category2products.get(category.id, empty_list):
                if product_id not in id2product:
                    continue
                product = id2product[product_id]
                relation = '%s_%s' % (category.id, product_id)
                product.join_category_time = relation2time.get(relation, today)
                category.products.append(id2product[product_id])
            category.products.sort(lambda x,y: cmp(y.id, x.id))

        c = RequestContext(
                request,
                {
                    'first_nav_name': export.PRODUCT_FIRST_NAV,
                    'second_navs': export.get_second_navs(request),
                    'second_nav_name': export.PRODUCT_MANAGE_CATEGORY_NAV,
                    'product_categories': product_categories,
                }
        )
        return render_to_response('mall/editor/product_categories.html', c)

    @login_required
    def api_get(request):
        """获得商品分类的可选商品列表

        API:
          method: get
          args: id

        可选商品指的是还不属于当前分类的商品.
          可选商品集合 ＝ manager的所有商品集合 － 已经在分类中的商品集合

        """
        COUNT_PER_PAGE = 20
        category_id = int(request.GET.get('id'))
        name_query = request.GET.get('name')

        #获取商品集合
        products = [product for product in mall_models.Product.objects.filter(
            owner=request.manager) if not product.is_deleted]
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

        products.sort(lambda x,y: cmp(x.id, y.id))

        #进行分页
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, products = paginator.paginate(
            products,
            cur_page,
            count_per_page,
            query_string=request.META['QUERY_STRING'])

        mall_models.Product.fill_display_price(products)
        mall_models.Product.fill_details(
            request.manager,
            products,
            {
                'with_sales': True
            }
        )
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
        result_products.sort(lambda x,y: cmp(y['id'], x['id']))

        response = create_response(200)
        response.data = {
            'items': result_products,
            'pageinfo': paginator.to_dict(pageinfo),
            'sortAttr': '',
            'data': {}
        }
        return response.get_response()

    @login_required
    def put(request):
        """创建商品分类
        """


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

        mall_models.ProductCategory.objects.filter(id=category_id).update(
            name=request.POST.get('name', '').strip(),
            product_count=len(product_ids)
        )

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
