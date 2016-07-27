# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
import operator
from datetime import datetime
from itertools import chain
from django.conf import settings
from django.db.models import F, Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from mall.promotion import models as promotion_model
from mall.signal_handler import products_not_online_handler_for_promotions
from watchdog.utils import watchdog_warning, watchdog_error
from account.models import UserProfile

from core import paginator
from core import resource
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from mall import models  # 注意不要覆盖此module
from mall import signals as mall_signals
from . import utils
from mall import export
from weixin.user.module_api import get_all_active_mp_user_ids
from apps.customerized_apps.group import models as group_models

import logging

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
        mall_type = request.user_profile.webapp_type
        shelve_type_get = request.GET.get("shelve_type", 1)
        shelve_type = int(shelve_type_get if shelve_type_get.isdigit() else 1)
        if mall_type:
            has_product = models.Product.objects.belong_to(mall_type, request.manager, shelve_type).count() > 0
        else:
            has_product = models.Product.objects.filter(
                owner=request.manager,
                shelve_type=shelve_type,
                is_deleted=False
            ).exists()
        print has_product,"<<<D<D<D<D<D<D<D<D<D<<<<<<<<<"
        c = RequestContext(
            request,
            {'first_nav_name': export.PRODUCT_FIRST_NAV,
             'second_navs': export.get_mall_product_second_navs(request),
             'has_product': has_product,
             'high_stocks': request.GET.get('high_stocks', '-1'),
             'mall_type': mall_type
             }
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
        # 商城类型
        mall_type = request.user_profile.webapp_type
        COUNT_PER_PAGE = 10
        _type = request.GET.get('type', 'onshelf')

        #处理排序
        sort_attr = request.GET.get('sort_attr', None)
        if not sort_attr:
            sort_attr = '-display_index'

        print "1>>>>>>>"*10
        #处理商品分类
        product_pool2display_index = {}
        if _type == 'offshelf':
            sort_attr = '-update_time'
            products = models.Product.objects.belong_to(mall_type, request.manager, models.PRODUCT_SHELVE_TYPE_OFF)

            if mall_type:
                product_pool = models.ProductPool.objects.filter(woid=request.manager.id, status=models.PP_STATUS_OFF)
                product_pool2display_index = dict([(pool.product_id, pool.display_index) for pool in product_pool])
            print "2222"*10,products
            # products = models.Product.objects.filter(
            #     owner=request.manager,
            #     shelve_type=models.PRODUCT_SHELVE_TYPE_OFF,
            #     is_deleted=False)
        elif _type == 'onshelf':
            products = models.Product.objects.belong_to(mall_type, request.manager, models.PRODUCT_SHELVE_TYPE_ON)
            if mall_type:
                product_pool = models.ProductPool.objects.filter(woid=request.manager.id, status=models.PP_STATUS_ON)
                product_pool2display_index = dict([(pool.product_id, pool.display_index) for pool in product_pool])
            # products = models.Product.objects.filter(
            #     owner=request.manager,
            #     shelve_type=models.PRODUCT_SHELVE_TYPE_ON,
            #     is_deleted=False)
        elif _type == 'recycled':
            products = models.Product.objects.belong_to(mall_type, request.manager, models.PRODUCT_SHELVE_TYPE_RECYCLED)
            # products = models.Product.objects.filter(
            #     owner=request.manager,
            #     shelve_type=models.PRODUCT_SHELVE_TYPE_RECYCLED,
            #     is_deleted=False)
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

        if mall_type:
            products = utils.weizoom_filter_products(request, products_not_0 + products_is_0)
            supplier_type = request.GET.get('orderSupplierType', '')
            if supplier_type == '0':
                products = filter(lambda p: p.supplier_user_id > 0, products)
            elif supplier_type == '1':
                products = filter(lambda p: p.supplier > 0, products)
        else:
            products = utils.filter_products(request, products_not_0 + products_is_0)



        #进行分页
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, products = paginator.paginate(
            products,
            cur_page,
            count_per_page,
            query_string=request.META['QUERY_STRING'])

        if mall_type:
            product_ids = [product.id for product in products]
            product_id2store_name, product_id2sync_time = utils.get_sync_product_store_name(product_ids)

            manager_product_user_id = UserProfile.objects.filter(webapp_type=2)[0].user_id
            manager_supplier_ids2name = dict([(s.id, s.name) for s in models.Supplier.objects.filter(owner_id=manager_product_user_id)])


        else:
            product_id2store_name = {}
            product_id2sync_time = {}
            manager_supplier_ids2name = {}

        # 手动添加供货商的信息
        supplier_ids2name = dict([(s.id, s.name) for s in models.Supplier.objects.filter(owner=request.manager, is_delete=False)])
        # 商品团购信息
        woid = request.webapp_owner_id
        try:
            pids = [str(product.id) for product in products]
            product2group = utils.get_product2group(pids, woid)
        except:
            error_msg = u"获取商品列表是否在团购中失败, cause:\n{}".format(unicode_full_stack())
            watchdog_error(error_msg)
            product2group={}

        #构造返回数据
        items = []
        items1 = []
        items2 = []
        for product in products:
            product_dict = product.format_to_dict()
            product_dict['is_self'] = (request.manager.id == product.owner_id)

            if manager_supplier_ids2name:
                store_name = manager_supplier_ids2name.get(product.supplier, "")
                if store_name:
                    is_sync = True
            else:
                store_name = ''

            if not store_name:
                store_name = supplier_ids2name[product.supplier] if product.supplier and supplier_ids2name.has_key(product.supplier) else product_id2store_name.get(product.id, "")
                is_sync = product_id2store_name.has_key(product.id)

            product_dict['store_name'] = store_name
            product_dict['sync_time'] = product_id2sync_time.get(product.id, product.created_at.strftime('%Y-%m-%d %H:%M'))
            product_dict['is_sync'] = is_sync

            if product.id in product_pool2display_index.keys():
                product_dict['display_index'] = product_pool2display_index[product.id]
            #增加团购属性
            if product2group.has_key(product.id):
                product_dict["is_group_buying"] = product2group[product.id]
                logging.info("product.is_group_buying:{},{}".format(product_dict["is_group_buying"],product.id))
            else:
                product_dict["is_group_buying"] = False
            #增加团购属性
            if product_dict['sync_time'] and not product_dict['purchase_price']:
                items1.append(product_dict)
            else:
                items2.append(product_dict)


            items.append(product_dict)

        # 微众系列待售排序
        if mall_type and _type == 'offshelf':
            items1 = sorted(items1, key=lambda item:item['sync_time'], reverse=True)
            items2 = sorted(items2, key=lambda item:item['sync_time'], reverse=True)
            items = items1 + items2

        data = dict()
        data['owner_id'] = request.manager.id
        data['mall_type'] = mall_type
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
        mall_type = request.user_profile.webapp_type
        ids = request.POST.getlist('ids', [])
        _ids = request.POST.getlist('ids[]', [])
        ids = ids if ids else _ids
        ids = [int(tmp_id) for tmp_id in ids] #兼容bdd
        p_id = request.POST.get('id')
        if p_id:
            ids.append(int(p_id))
        if not ids:
            return create_response(200).get_response()

        #团购
        #if mall_type == 0:
        woid = request.webapp_owner_id
        try:
            pids = [str(product_id) for product_id in ids]
            product2group = utils.get_product2group(pids, woid)
        except:
            error_msg = u"获取商品列表是否在团购中失败, cause:\n{}".format(unicode_full_stack())
            watchdog_error(error_msg)
            product2group={}
        if product2group:
            for id_tmp in ids:
                if product2group.has_key(id_tmp) and product2group[id_tmp] == True:
                    ids.remove(id_tmp)


        if ids:
            is_deleted = False
            shelve_type = request.POST['shelve_type']

            if mall_type:
                product_pool = models.ProductPool.objects.filter(woid=request.manager.id, product_id__in=ids)
                product_pool_ids = [pool.product_id for pool in product_pool]
            else:
                product_pool_ids = []

            # set_c = set(product_pool_ids) & set(ids)
            # duplicate_id = list(set_c)

            if shelve_type == 'onshelf':
                shelve_type = models.PRODUCT_SHELVE_TYPE_ON

                if mall_type:
                    product_pool = models.ProductPool.objects.filter(woid=request.manager.id, product_id__in=ids).update(status=models.PP_STATUS_ON)

            elif shelve_type == 'offshelf':
                shelve_type = models.PRODUCT_SHELVE_TYPE_OFF
                reason = utils.MALL_PRODUCT_OFF_SHELVE

                if mall_type:
                    product_pool = models.ProductPool.objects.filter(woid=request.manager.id, product_id__in=ids).update(status=models.PP_STATUS_OFF)

            elif shelve_type == 'recycled':
                shelve_type = models.PRODUCT_SHELVE_TYPE_RECYCLED
            elif shelve_type == 'delete':
                is_deleted = True
                reason = utils.MALL_PRODUCT_DELETED

            prev_shelve_type = models.Product.objects.get(
                id=ids[0]).shelve_type






            products = models.Product.objects.filter(owner=request.manager, id__in=ids)
            product_id2product = {}
            for product in products:
                product_id2product[product.id] = product



            if is_deleted:
                products.update(is_deleted=True, display_index=0)
            else:
                # 更新商品上架状态以及商品排序
                # 微众商城代码
                # if request.manager.id == products[0].owner_id:
                #     now = datetime.now()
                #     if shelve_type != models.PRODUCT_SHELVE_TYPE_ON:
                #         products.update(shelve_type=shelve_type, weshop_status=shelve_type, display_index=0, update_time=now)
                #     else:
                #         #上架
                #         products.update(shelve_type=shelve_type, display_index=0, update_time=now)
                # else:
                #     # 微众商城更新商户商品状态
                #     products.update(weshop_status=shelve_type)

                now = datetime.now()
                if shelve_type != models.PRODUCT_SHELVE_TYPE_ON:
                    products.update(shelve_type=shelve_type, display_index=0, update_time=now)
                else:
                    #上架
                    products.update(shelve_type=shelve_type, display_index=0, update_time=now)
            is_prev_shelve = prev_shelve_type == models.PRODUCT_SHELVE_TYPE_ON
            is_not_sale = shelve_type != models.PRODUCT_SHELVE_TYPE_ON

            if (is_prev_shelve and is_not_sale) or is_deleted:
                # 商品不再处于上架状态，发出product_not_offline signal
                product_ids = [int(id) for id in ids]
                mall_signals.products_not_online.send(
                    sender=models.Product,
                    product_ids=product_ids,
                    request=request
                )

            # 供货商商品下架或者删除对应删除weizoom系列上架的商品
            if not mall_type and (shelve_type == models.PRODUCT_SHELVE_TYPE_OFF or is_deleted):
                for id in ids:
                    utils.delete_weizoom_mall_sync_product(request, product_id2product[int(id)], reason)
            if mall_type and is_deleted:
                models.WeizoomHasMallProductRelation.objects.filter(weizoom_product_id__in=ids).update(is_deleted=True, delete_type=True)
                #处理商品池
                models.ProductPool.objects.filter(product_id__in=ids, woid=request.manager.id).update(status=models.PP_STATUS_ON_POOL)

        response = create_response(200)
        return response.get_response()

webapp_id = "3185"

class ProductPool(resource.Resource):
    app = 'mall2'
    resource = 'product_pool'

    @login_required
    def get(request):
        # 商城的类型
        mall_type = request.user_profile.webapp_type
        c = RequestContext(request, {
            'first_nav_name': export.PRODUCT_FIRST_NAV,
            'second_navs': export.get_mall_product_second_navs(request),
            'second_nav_name': export.PRODUCT_ADD_PRODUCT_NAV,
            'mall_type': mall_type,
        })
        return render_to_response('mall/editor/product_pool.html', c)

    @login_required
    def api_get(request):
        product_name = request.GET.get('name', '')
        supplier_name = request.GET.get('supplier', '')
        #status = request.GET.get('status', '-1')

        # 获取所有供货商的id
        #OLD CODE
        # all_user_ids = get_all_active_mp_user_ids()
        # all_mall_userprofiles = UserProfile.objects.filter(user_id__in=all_user_ids, webapp_type=0)
        # user_id2userprofile = dict([(profile.user_id, profile) for profile in all_mall_userprofiles])
        # owner_ids = user_id2userprofile.keys()
        # if not owner_ids:
        #     return create_response(200).get_response()

        manager_user_profile = UserProfile.objects.filter(webapp_type=2)[0]
        product_pool = models.ProductPool.objects.filter(woid=request.manager.id, status=models.PP_STATUS_ON_POOL)

        product_ids = [pool.product_id for pool in product_pool]
        products = models.Product.objects.filter(id__in=product_ids)


        if supplier_name:
            supplier_ids = [s.id for s in models.Supplier.objects.filter(owner_id=manager_user_profile.user_id, name__contains=supplier_name)]
            if supplier_ids:
                products = products.filter(supplier__in=supplier_ids)
            else:
                products = []
        # 筛选出所有商品
        if product_name and products:
            products = products.filter(name__contains=product_name)


        # else:
        #     all_mall_product = models.Product.objects.filter(
        #         owner__in=owner_ids,
        #         shelve_type=models.PRODUCT_SHELVE_TYPE_ON,
        #         is_deleted=False)

        # # 筛选出单规格的商品id
        # standard_model_product_ids = [model.product_id for model in models.ProductModel.objects.filter(owner_id__in=owner_ids, name='standard', is_deleted=False)]

        # # 筛选出已经同步的商品
        # mall_product_id2relation = dict([(relation.mall_product_id, relation) for relation in models.WeizoomHasMallProductRelation.objects.filter(owner=request.manager, is_deleted=False)])

        #products = all_mall_product.filter(id__in=standard_model_product_ids)
        models.Product.fill_details(manager_user_profile.user, products, {
            "with_product_model": True,
            "with_model_property_info": True,
            "with_selected_category": True,
            'with_image': False,
            'with_property': True,
            'with_sales': True
        })

        # dict_products = []
        # for product in products:
        #     product.price = product.display_price
        #     product = product.to_dict()
        #     if product['id'] in mall_product_id2relation:
        #         if mall_product_id2relation[product['id']].is_updated and not mall_product_id2relation[product['id']].is_deleted:
        #             product['status'] = 1
        #         elif not mall_product_id2relation[product['id']].is_updated and not mall_product_id2relation[product['id']].is_deleted:
        #             product['status'] = 3
        #     else:
        #         product['status'] = 2
        #     dict_products.append(product)
        # products = dict_products

        # products = sorted(products, key=lambda product:product['created_at'], reverse=True)
        # products = sorted(products, key=lambda product:product['status'])

        # if status != '-1':
        #     products = filter(lambda product:product['status'] == int(status), products)


        COUNT_PER_PAGE = 15
        #进行分页
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, products = paginator.paginate(
            products,
            cur_page,
            count_per_page,
            query_string=request.META['QUERY_STRING'])

        manager_product_user_id = 0
        if request.user_profile.webapp_type == 1:
            manager_product_user_id = UserProfile.objects.filter(webapp_type=2)[0].user_id

        supplier_ids2name = {}
        if manager_product_user_id:
            supplier_ids2name = dict([(s.id, s.name) for s in models.Supplier.objects.filter(owner_id=manager_product_user_id)])

        # 对应商品营销活动信息
        # product_ids = [product['id'] for product in products]
        # relations = models.WeizoomHasMallProductRelation.objects.filter(mall_product_id__in=product_ids, is_deleted=False)
        # mall_product_id2weizoom_product_id = dict([(r.mall_product_id, r.weizoom_product_id) for r in relations])
        # promotionrelations = promotion_model.ProductHasPromotion.objects.filter(
        #         product_id__in=mall_product_id2weizoom_product_id.values()
        #     ).exclude(promotion__type=promotion_model.PROMOTION_TYPE_COUPON)

        # product_id2relation = dict([(relation.product_id, relation)for relation in promotionrelations])

        # 对应商品团购数据
        # weizoom_product_ids = [str(id) for id in mall_product_id2weizoom_product_id.values()]
        # product2group = utils.get_product2group(weizoom_product_ids, request.webapp_owner_id)
        #构造返回数据

        items = []
        for product in products:

            # if (mall_product_id2weizoom_product_id.has_key(product['id']) and
            #     product_id2relation.has_key(mall_product_id2weizoom_product_id[product['id']]) and
            #     product_id2relation[mall_product_id2weizoom_product_id[product['id']]].promotion.status in [promotion_model.PROMOTION_STATUS_STARTED, promotion_model.PROMOTION_STATUS_NOT_START]):
            #     product_has_promotion = 1
            # else:
            #     product_has_promotion = 0

            # if mall_product_id2weizoom_product_id.has_key(product['id']) and product2group.has_key(mall_product_id2weizoom_product_id[product['id']]):
            #     product_has_group = product2group[mall_product_id2weizoom_product_id[product['id']]]
            # else:
            #     product_has_group = 0
            # product = product.to_dict()
            # print ">>>>>>>>>>>>>>price", product
            # product = product.to_dict()zai
            # product.fill_standard_model()


            items.append({
                'id': product.id,
                # 'product_has_promotion': product_has_promotion,
                # 'product_has_group': product_has_group,
                'name': product.name,
                'thumbnails_url': product.thumbnails_url,
                'user_code': product.user_code,
                #'status': product['status'],
                'store_name': supplier_ids2name.get(product.supplier, product.supplier),#user_id2userprofile[product['owner_id']].store_name,
                'stocks': product.stocks,
                'price':product.price,
                'is_use_custom_model': product.is_use_custom_model,
                'models': product.models[1:],
                'display_price_range': product.display_price_range
               # 'sync_time': mall_product_id2relation[product['id']].sync_time.strftime('%Y-%m-%d %H:%M') if mall_product_id2relation.has_key(product['id']) else ''
            })

        data = dict()
        data['owner_id'] = request.manager.id
        response = create_response(200)
        response.data = {
            'items': items,
            'pageinfo': paginator.to_dict(pageinfo),
            'data': data
        }
        return response.get_response()

    @login_required
    def api_put(request):
        """
        put 方法

        将商品池中的商品上架
        """
        product_ids = request.POST.get('product_ids', '')
        if not product_ids:
            return create_response(200).get_response()
        product_ids = json.loads(product_ids)
        products = models.Product.objects.filter(id__in=product_ids)


        models.ProductPool.objects.filter(woid=request.manager.id, product_id__in=product_ids).update(status=models.PP_STATUS_ON)
        return create_response(200).get_response()
        #for product in products:

        # products = models.Product.objects.filter(id__in=product_ids)
        # for product in products:
        #     # 商品信息
        #     new_product = models.Product.objects.create(
        #         owner = request.manager,
        #         name = product.name,
        #         physical_unit = product.physical_unit,
        #         price = product.price,
        #         introduction = product.introduction,
        #         weight = product.weight,
        #         thumbnails_url = product.thumbnails_url,
        #         pic_url = product.pic_url,
        #         detail = product.detail,
        #         remark = product.remark,
        #         shelve_type = models.PRODUCT_SHELVE_TYPE_OFF,
        #         stock_type = product.stock_type,
        #         stocks = product.stocks,
        #         is_support_make_thanks_card = product.is_support_make_thanks_card,
        #         type = product.type,
        #         promotion_title = product.promotion_title,
        #         user_code = product.user_code,
        #         bar_code = product.bar_code,
        #         supplier = product.supplier,
        #         supplier_user_id = product.owner_id
        #     )
        #     # 商品规格
        #     product_model = models.ProductModel.objects.get(product=product, is_deleted=False)
        #     models.ProductModel.objects.create(
        #         owner=request.manager,
        #         product=new_product,
        #         name='standard',
        #         is_standard=True,
        #         price=product_model.price,
        #         weight=product_model.weight,
        #         stock_type=product_model.stock_type,
        #         stocks=product_model.stocks,
        #         user_code=product_model.user_code,
        #         is_deleted=product_model.is_deleted
        #     )
        #     # 商品轮播图
        #     product_swipe_images = models.ProductSwipeImage.objects.filter(product=product)
        #     for item in product_swipe_images:
        #         models.ProductSwipeImage.objects.create(
        #             product = new_product,
        #             url = item.url,
        #             link_url = item.link_url,
        #             width = item.width,
        #             height = item.height
        #         )
        #     # 商品属性
        #     properties = models.ProductProperty.objects.filter(product=product)
        #     for property in properties:
        #         models.ProductProperty.objects.create(
        #             owner=request.manager,
        #             product=new_product,
        #             name=property.name,
        #             value=property.value
        #         )
        #     # 创建新商品和同步商品的关系
        #     models.WeizoomHasMallProductRelation.objects.create(
        #         owner = request.manager,
        #         mall_id = product.owner_id,
        #         mall_product_id = product.id,
        #         weizoom_product_id = new_product.id
        #     )

        # return create_response(200).get_response()

    @login_required
    def api_post(request):
        product_id = request.POST.get('product_id', "")
        if not product_id:
            return create_response(500).get_response()
        relation = models.WeizoomHasMallProductRelation.objects.get(
            owner=request.manager,
            mall_product_id=product_id,
            is_deleted=False)
        # 后台验证更新的商品是否参与团购
        product2group = utils.get_product2group([str(relation.weizoom_product_id)], request.webapp_owner_id)

        if product2group.has_key(relation.weizoom_product_id) and product2group[relation.weizoom_product_id]:
            return create_response(500).get_response()

        # 微众系列商品参加的促销活动
        products_not_online_handler_for_promotions([relation.weizoom_product_id], request)

        weizoom_product = models.Product.objects.get(id=relation.weizoom_product_id)
        mall_product = models.Product.objects.get(id=relation.mall_product_id)

        weizoom_product.name = mall_product.name
        weizoom_product.physical_unit = mall_product.physical_unit
        weizoom_product.price = mall_product.price
        weizoom_product.introduction = mall_product.introduction
        weizoom_product.weight = mall_product.weight
        weizoom_product.thumbnails_url = mall_product.thumbnails_url
        weizoom_product.pic_url = mall_product.pic_url
        weizoom_product.detail = mall_product.detail
        weizoom_product.remark = mall_product.remark
        weizoom_product.shelve_type = models.PRODUCT_SHELVE_TYPE_OFF
        weizoom_product.stock_type = mall_product.stock_type
        weizoom_product.stocks = mall_product.stocks
        weizoom_product.is_support_make_thanks_card = mall_product.is_support_make_thanks_card
        weizoom_product.type = mall_product.type
        weizoom_product.promotion_title = mall_product.promotion_title
        weizoom_product.user_code = mall_product.user_code
        weizoom_product.bar_code = mall_product.bar_code
        weizoom_product.supplier = mall_product.supplier
        weizoom_product.save()

        # 商品规格
        mall_product_model = models.ProductModel.objects.get(product=mall_product, is_standard=True, is_deleted=False)
        weizoom_product_model = models.ProductModel.objects.get(product=weizoom_product, is_standard=True, is_deleted=False)
        weizoom_product_model.price = mall_product_model.price
        weizoom_product_model.weight = mall_product_model.weight
        weizoom_product_model.user_code = mall_product_model.user_code
        weizoom_product_model.save()

        # 商品轮播图
        models.ProductSwipeImage.objects.filter(product=weizoom_product).delete()
        mall_product_swipe_images = models.ProductSwipeImage.objects.filter(product=mall_product)
        for item in mall_product_swipe_images:
            models.ProductSwipeImage.objects.create(
                product = weizoom_product,
                url = item.url,
                link_url = item.link_url,
                width = item.width,
                height = item.height
            )
        # 商品属性
        models.ProductProperty.objects.filter(product=weizoom_product).delete()
        properties = models.ProductProperty.objects.filter(product=mall_product)
        for property in properties:
            models.ProductProperty.objects.create(
                owner=request.manager,
                product=weizoom_product,
                name=property.name,
                value=property.value
            )
        # 创建新商品和同步商品的关系
        relation.is_updated = False
        relation.sync_time = datetime.now()
        relation.save()
        return create_response(200).get_response()


class DeletedProductList(resource.Resource):
    app = 'mall2'
    resource = 'deleted_product_list'

    @login_required
    def api_get(request):
        """
        查看失效商品
        """
        start_date = request.GET.get('startDate', "")
        end_date = request.GET.get('endDate', "")

        if start_date and end_date:
            params = dict(
                    owner=request.manager,
                    is_deleted=True,
                    delete_type=False,
                    delete_time__gte=start_date,
                    delete_time__lte=end_date
                )
        else:
            params = dict(
                    owner=request.manager,
                    is_deleted=True,
                    delete_type=False,
                )


        relations = models.WeizoomHasMallProductRelation.objects.filter(**params).order_by('-id')

        COUNT_PER_PAGE = 8
        #进行分页
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, relations = paginator.paginate(
            relations,
            cur_page,
            count_per_page,
            query_string=request.META['QUERY_STRING'])

        #构造返回数据
        items = []
        product_id2product_name = dict([(product.id, product.name) for product in models.Product.objects.filter(id__in=[relation.weizoom_product_id for relation in relations])])
        for relation in relations:
            items.append({
                'id': relation.weizoom_product_id,
                'name': product_id2product_name[relation.weizoom_product_id],
                'delete_time': relation.delete_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        response = create_response(200)
        response.data = {
            'items': items,
            'pageinfo': paginator.to_dict(pageinfo),
        }
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

        # 商城的类型
        mall_type = request.user_profile.webapp_type

        #自营平台去掉添加新商品
        if mall_type and not has_product_id and request.manager.username not in ['weshop', 'weizoomjx']:
            return HttpResponseRedirect(
            '/mall2/product_pool/')

        has_store_name = False
        store_name = ''

        pool_mall_type = False
        if has_product_id:
            try:
                if mall_type:
                    if models.ProductPool.objects.filter(woid=request.manager.id, product_id=has_product_id).count() > 0:
                        #商品池中的商品状态不在Product中，在ProductPool中
                        shelve_type = models.ProductPool.objects.filter(woid=request.manager.id, product_id=has_product_id)[0].status
                        product = models.Product.objects.get(id=has_product_id)
                        product.shelve_type = shelve_type
                        pool_mall_type = True
                    else:
                        product = models.Product.objects.get(owner=request.manager, id=has_product_id)
                else:
                    product = models.Product.objects.get(owner=request.manager, id=has_product_id)
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
            # 判断微众系列商品是不是供货商提供的
            if mall_type:
                relations = models.WeizoomHasMallProductRelation.objects.filter(weizoom_product_id=has_product_id, is_deleted=False)
                if relations.count() > 0:
                    has_store_name = True
                    store_name = UserProfile.objects.get(user_id=relations[0].mall_id).store_name
            #获取商品分类信息
            categories = product.categories

            # 限时抢购的商品不能修改起购数量
            for promotion in [relation.promotion for relation in
                              promotion_model.ProductHasPromotion.objects.filter(product_id=product.id)]:
                if promotion.type == promotion_model.PROMOTION_TYPE_FLASH_SALE and promotion.status == promotion_model.PROMOTION_STATUS_STARTED:
                    product.is_in_flash_sale = True
                    break
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
        #自营平台的供货商不可修改，所以只传它自己的supplier即可。微众商城和精选如果没有供货商就传空list
        if mall_type and has_product_id:
            supplier = [(s.id, s.name) for s in models.Supplier.objects.filter(id=product.supplier, is_delete=False)]
        else:
            supplier = [(s.id, s.name) for s in models.Supplier.objects.filter(owner=request.manager, is_delete=False)]

        is_bill = True if request.manager.username not in settings.WEIZOOM_ACCOUNTS else  False

        #增加团购判断接口
        if product:
            woid = request.webapp_owner_id
            product.is_group_buying = product_is_group(product.id, woid)


        c = RequestContext(request, {
            'first_nav_name': export.PRODUCT_FIRST_NAV,
            'second_navs': export.get_mall_product_second_navs(request),
            'second_nav_name': export.PRODUCT_ADD_PRODUCT_NAV,
            'product': product,
            'categories': categories,
            'postage': '',
            'pay_interface_config': pay_interface_config,
            'postage_config_info': postage_config_info,
            'property_templates': property_templates,
            'supplier': supplier,
            'is_bill': is_bill,
            'mall_type': mall_type,
            'has_store_name': has_store_name,
            'store_name': store_name,
            'pool_mall_type': pool_mall_type
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

        purchase_price = request.POST.get("purchase_price", '')

        if purchase_price == '':
            purchase_price = 0
        is_enable_bill = request.POST.get('is_enable_bill', False)
        if is_enable_bill in [True, '1', 'True']:
            is_enable_bill=True
        else:
            is_enable_bill=False
        #配送时间
        is_delivery = request.POST.get('is_delivery', False)
        if is_delivery in [True, '1', 'True','on']:
            is_delivery=True
        else:
            is_delivery=False

        is_bill = True if request.manager.username not in settings.WEIZOOM_ACCOUNTS else  False
        if is_bill is False:
            is_enable_bill = False
            is_delivery = False

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
            is_member_product=request.POST.get("is_member_product", False) == 'on',
            supplier=request.POST.get("supplier", 0),
            purchase_price=purchase_price,
            is_enable_bill=is_enable_bill,
            is_delivery=is_delivery
        )
        # 设置新商品显示顺序
        # product.display_index = models.Product.objects.filter(
        #     owner=request.manager
        # ).order_by('-display_index').first().display_index + 1
        # 处理商品排序
        display_index = int(request.POST.get('display_index', '0'))
        if display_index > 0:
            product.move_to_position(display_index)

        is_deleted = False
        if standard_model.get('is_deleted', None):
            is_deleted = True
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
            user_code=standard_model['user_code'],
            is_deleted=is_deleted
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
        mall_type = request.user_profile.webapp_type
        woid = request.webapp_owner_id
        product_id = request.GET.get('id')
        if mall_type:
            if models.ProductPool.objects.filter(product_id=product_id, woid=woid).count()>0:
                # 减少原category的product_count
                _update_product_category(request,product_id)
                source = int(request.GET.get('shelve_type', 0))
                if source == models.PRODUCT_SHELVE_TYPE_OFF:
                    url = '/mall2/product_list/?shelve_type=%d' % (models.PRODUCT_SHELVE_TYPE_OFF, )
                    return HttpResponseRedirect(url)
                elif source == models.PRODUCT_SHELVE_TYPE_ON:
                    url = '/mall2/product_list/?shelve_type=%d' % (models.PRODUCT_SHELVE_TYPE_ON, )
                    return HttpResponseRedirect(url)
                else:
                    url = '/mall2/product_list/?shelve_type=%d' % (models.PRODUCT_SHELVE_TYPE_RECYCLED, )
                    return HttpResponseRedirect(url)



        swipe_images = request.POST.get('swipe_images', '[]')
        if not swipe_images:
            url = '/mall2/product_list/?shelve_type=%d' % int(request.GET.get('shelve_type', 0))
            return HttpResponseRedirect(url)
        else:
            swipe_images = json.loads(swipe_images)
        thumbnails_url = swipe_images[0]["url"]

        #添加团购活动判断:非自营\团购\标准规格
        if mall_type == 0:
            is_group_buying = product_is_group(product_id, woid)
        else:
            is_group_buying = False
        has_product_model = models.ProductModel.objects.filter(
                owner_id=woid,
                product_id=product_id,
                name='standard').exists()

        # 更新对应同步的商品状态
        if not request.user_profile.webapp_type:
            from .tasks import update_sync_product_status
            products = models.Product.objects.filter(owner_id=woid, id=product_id)
            models.Product.fill_details(request.manager, products, {
                'with_product_model': True,
                'with_image': True,
                'with_property': True,
                'with_model_property_info': True,
                'with_all_category': True,
                'with_sales': True
            })
            update_sync_product_status(products[0], request, is_group_buying)

        if is_group_buying and has_product_model:
            #团购流程
            utils.handle_group_product(request, product_id, swipe_images, thumbnails_url)
        else:
            #标准流程


            # 处理商品排序
            display_index = int(request.POST.get('display_index', '0'))
            if display_index > 0:
                models.Product.objects.get(owner_id=woid, id=product_id).move_to_position(display_index)

            # 处理商品规格
            standard_model, custom_models = utils.extract_product_model(request)
            # 处理standard商品规格
            has_product_model = models.ProductModel.objects.filter(
                owner_id=woid,
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
                # 多规格的情况
                db_standard_model = models.ProductModel.objects.filter(
                    owner_id=woid,
                    product_id=product_id,
                    name='standard'
                )
                if not db_standard_model[0].is_deleted:
                    from mall.promotion import models as promotion_models
                    # 单规格改多规格商品
                    db_standard_model.update(is_deleted=True)

                    # 结束对应买赠活动 jz
                    premiumSaleIds = set(promotion_models.PremiumSaleProduct.objects.filter(
                        product_id=db_standard_model[0].product_id).values_list('premium_sale_id', flat=True))
                    if len(premiumSaleIds) > 0:
                        from webapp.handlers import event_handler_util
                        promotionIds = set(promotion_models.Promotion.objects.filter(
                            detail_id__in=premiumSaleIds, type=promotion_models.PROMOTION_TYPE_PREMIUM_SALE).values_list('id', flat=True))
                        event_data = {
                            "id": ','.join([str(id) for id in promotionIds])
                        }
                        event_handler_util.handle(event_data, 'finish_promotion')
            else:
                models.ProductModel.objects.filter(
                    owner_id=woid, product_id=product_id, name='standard'
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
            existed_model_names_not_delete = set([model.name for model in existed_models if not model.is_deleted])
            to_be_deleted_model_names = existed_model_names_not_delete - updated_model_names
            if len(to_be_deleted_model_names):
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
                    owner_id=woid, product_id=product_id)
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
                        owner_id=woid, id=property['id']
                    ).update(name=property['name'], value=property['value'])
            property_ids_to_be_delete = existed_property_ids - property_ids
            models.ProductProperty.objects.filter(
                id__in=property_ids_to_be_delete).delete()

            # 减少原category的product_count
            _update_product_category(request,product_id)

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

            min_limit = request.POST.get('min_limit', '0')
            if not min_limit.isdigit():
                min_limit = 0
            else:
                min_limit = float(min_limit)
            purchase_price = request.POST.get("purchase_price", '')
            if purchase_price == '':
                purchase_price = 0
            is_enable_bill = request.POST.get('is_enable_bill', False)
            if is_enable_bill in [True, '1', 'True']:
                is_enable_bill=True
            else:
                is_enable_bill=False

            is_delivery = request.POST.get('is_delivery', False)

            is_bill = True if request.manager.username not in settings.WEIZOOM_ACCOUNTS else  False
            if is_bill is False:
                is_enable_bill = False
                is_delivery = False

            param = {
                'name': request.POST.get('name', '').strip(),
                'promotion_title': request.POST.get('promotion_title', '').strip(),
                'user_code': request.POST.get('user_code', '').strip(),
                'bar_code': request.POST.get('bar_code', '').strip(),
                'thumbnails_url': thumbnails_url,
                'detail': request.POST.get('detail', '').strip(),
                'type': request.POST.get('type', models.PRODUCT_DEFAULT_TYPE),
                'is_use_online_pay_interface': 'is_enable_online_pay_interface' in request.POST,
                'is_use_cod_pay_interface': 'is_enable_cod_pay_interface' in request.POST,
                'postage_id': postage_id,
                'unified_postage_money': unified_postage_money,
                'postage_type': postage_type,
                'stocks': min_limit,
                'is_member_product': request.POST.get("is_member_product", False) == 'on',
                'supplier': request.POST.get("supplier", 0),
                'purchase_price': purchase_price,
                'is_enable_bill': is_enable_bill,
                'is_delivery': is_delivery,
                'buy_in_supplier': int(request.POST.get('buy_in_supplier', False))
            }
            # 微众商城代码
            # if request.POST.get('weshop_sync', None):
            #     param['weshop_sync'] = request.POST['weshop_sync'][0]
            models.Product.objects.record_cache_args(
                ids=[product_id]
            ).filter(
                owner=request.manager,
                id=product_id
            ).update(**param)

        # 更新product结束

        source = int(request.GET.get('shelve_type', 0))
        if source == models.PRODUCT_SHELVE_TYPE_OFF:
            url = '/mall2/product_list/?shelve_type=%d' % (models.PRODUCT_SHELVE_TYPE_OFF, )
            return HttpResponseRedirect(url)
        elif source == models.PRODUCT_SHELVE_TYPE_ON:
            url = '/mall2/product_list/?shelve_type=%d' % (models.PRODUCT_SHELVE_TYPE_ON, )
            return HttpResponseRedirect(url)
        else:
            url = '/mall2/product_list/?shelve_type=%d' % (models.PRODUCT_SHELVE_TYPE_RECYCLED, )
            return HttpResponseRedirect(url)

def _update_product_category(request,product_id):
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


class ProductPos(resource.Resource):
    app = 'mall2'
    resource = 'product_pos'

    @login_required
    def api_get(request):
        """
        获取商品是否存在已有的排序值
        """
        try:
            is_index_exists = False
            owner = request.manager
            pos = int(request.GET.get('pos'))
            obj_bs = models.Product.objects.filter(
                owner=owner, display_index=pos, is_deleted=False, shelve_type=models.PRODUCT_SHELVE_TYPE_ON)
            if obj_bs.exists():
                is_index_exists = True

            response = create_response(200)
            response.data = {
                'is_index_exists': is_index_exists
            }
        except:
            error_msg = u"获取商品是否存在已有的排序值失败, cause:\n{}".format(unicode_full_stack())
            print error_msg
            watchdog_warning(error_msg)
            response = create_response(500)

        return response.get_response()

    @login_required
    def api_post(request):
        """根据update_type，更新对应的商品信息.

        Args:
          update_type:
            update_pos: 更新商品位置信息
              id: product.id
              pos: product new position
        """
        try:
            id = request.POST.get('id')
            pos = int(request.POST.get('pos'))
            mall_type = request.user_profile.webapp_type

            if mall_type and models.ProductPool.objects.filter(woid=request.manager.id, product_id=id).count():
                models.ProductPool.objects.filter(woid=request.manager.id, product_id=id).update(display_index=pos)
            elif request.POST.get('update_type', '') == 'update_pos':
                product = models.Product.objects.get(id=id)
                product.move_to_position(pos)
            response = create_response(200)
            return response.get_response()
        except:
            watchdog_warning(
                u"failed to update product pos, cause:\n{}".format(unicode_full_stack())
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
            if not model_info.get('id', None):
                # 商品没有规格的情况, 避免报错
                response = create_response(400)
                response.errMsg = '商品规格错误请重新编辑商品'
                return response.get_response()
            product_model_id = model_info['id']
            stocks = model_info['stocks']
            if stock_type == models.PRODUCT_STOCK_TYPE_UNLIMIT:
                stocks = 0
            product_model = models.ProductModel.objects.filter(
                owner=request.manager,
                id=product_model_id
            )
            if len(product_model) == 1 and product_model[0].stock_type == models.PRODUCT_STOCK_TYPE_LIMIT and product_model[0].stocks < 1:
                #触发signal，清理缓存
                product_model.update(stocks=0)

            product_model.update(stock_type=stock_type, stocks=stocks)

        response = create_response(200)
        return response.get_response()


class ProductModelPrice(resource.Resource):
    app = 'mall2'
    resource = 'product_model_price'

    @login_required
    def api_post(request):
        """更新商品规格价格
        """
        model_infos = json.loads(request.POST.get('model_infos', '[]'))
        woid = request.webapp_owner_id
        for model_info in model_infos:
            if not model_info.get('id', None):
                # 商品没有规格的情况, 避免报错
                response = create_response(400)
                response.errMsg = '商品规格错误请重新编辑商品'
                return response.get_response()
            product_model_id = model_info['id']
            price = model_info['price']

            product_model = models.ProductModel.objects.filter(
                owner=request.manager,
                id=product_model_id
            )

            product_model.update(price=price)

            #更新对应同步的商品状态
            if not request.user_profile.webapp_type:
                from .tasks import update_sync_product_status
                product_id = product_model[0].product_id
                products = models.Product.objects.filter(owner_id=woid, id=product_id)
                models.Product.fill_details(request.manager, products, {
                    'with_product_model': True,
                    'with_image': True,
                    'with_property': True,
                    'with_model_property_info': True,
                    'with_all_category': True,
                    'with_sales': True
                })
                update_sync_product_status(products[0], request)
        response = create_response(200)
        return response.get_response()


class GroupProductList(resource.Resource):
    app = 'mall2'
    resource = 'group_product_list'

    @login_required
    def api_get(request):
        COUNT_PER_PAGE = 10
        product_name = request.GET.get('name', '')

        # 筛选出单规格的商品id
        standard_model_product_ids = [model.product_id for model in models.ProductModel.objects.filter(owner=request.manager, name='standard', is_deleted=False)]
        promotion_ids = [promotion.id for promotion in promotion_model.Promotion.objects.filter(owner=request.manager, status__in=[promotion_model.PROMOTION_STATUS_NOT_START, promotion_model.PROMOTION_STATUS_STARTED])]
        has_promotion_product_ids = [relation.product_id for relation in promotion_model.ProductHasPromotion.objects.filter(promotion_id__in=promotion_ids)]
        woid = request.webapp_owner_id
        pids = utils.get_pids(woid)
        if pids:
            has_promotion_product_ids.extend(pids)

        group_product_ids = [id for id in standard_model_product_ids if id not in has_promotion_product_ids]
        products = models.Product.objects.filter(
                owner=request.manager,
                id__in=group_product_ids,
                shelve_type=models.PRODUCT_SHELVE_TYPE_ON,
                is_deleted=False,
                is_member_product=False,
                stocks__lte=1,
                buy_in_supplier=False
                )
        if product_name:
            products = products.filter(name__contains=product_name)

        #进行分页
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, products = paginator.paginate(
            products,
            cur_page,
            count_per_page,
            # query_string=request.META['QUERY_STRING'],
            )
        models.Product.fill_details(request.manager, products, {
            "with_product_model": True,
            "with_model_property_info": True,
            "with_selected_category": True,
            'with_image': False,
            'with_property': True,
            'with_sales': True
        })

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
            'data': data
        }
        return response.get_response()

def product_is_group(product_id, woid):
    is_group_buying = False
    try:
        pids = []
        pids.append(str(product_id))
        product2group = utils.get_product2group(pids, woid)
        if product2group.has_key(int(product_id)):
            is_group_buying = product2group[int(product_id)]
    except:
        error_msg = u"获取商品是否在团购中失败, cause:\n{}".format(unicode_full_stack())
        watchdog_error(error_msg)
    return is_group_buying

class GroupProductListWoid(resource.Resource):
    app = 'mall2'
    resource = 'group_product_list_woid'

    def api_get(request):
        COUNT_PER_PAGE = 10
        product_name = request.GET.get('name', '')
        woid = request.GET.get('woid', '')
        if not woid:
            response = create_response(200)
            response.data = {
            'error': "less woid",
        }
            return response.get_jsonp_response(request)
        # 筛选出单规格的商品id
        standard_model_product_ids = [model.product_id for model in models.ProductModel.objects.filter(owner=woid, name='standard', is_deleted=False)]
        promotion_ids = [promotion.id for promotion in promotion_model.Promotion.objects.filter(owner=woid, status__in=[promotion_model.PROMOTION_STATUS_NOT_START, promotion_model.PROMOTION_STATUS_STARTED])]
        has_promotion_product_ids = [relation.product_id for relation in promotion_model.ProductHasPromotion.objects.filter(promotion_id__in=promotion_ids)]
        pids = utils.get_pids(woid)
        if pids:
            has_promotion_product_ids.extend(pids)

        group_product_ids = [id for id in standard_model_product_ids if id not in has_promotion_product_ids]
        products = models.Product.objects.filter(
                owner=woid,
                id__in=group_product_ids,
                shelve_type=models.PRODUCT_SHELVE_TYPE_ON,
                is_deleted=False,
                is_member_product=False,
                stocks__lte=1,
                buy_in_supplier=False
                )
        if product_name:
            products = products.filter(name__contains=product_name)

        #进行分页
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, products = paginator.paginate(
            products,
            cur_page,
            count_per_page,
            )
        models.Product.fill_details(woid, products, {
            "with_product_model": True,
            "with_model_property_info": True,
            "with_selected_category": True,
            'with_image': False,
            'with_property': True,
            'with_sales': True
        })

        #构造返回数据
        items = []
        for product in products:
            product_dict = product.format_to_dict()
            product_dict['is_self'] = (int(woid) == product.owner_id)
            items.append(product_dict)
        data = dict()
        data['owner_id'] = woid
        response = create_response(200)
        response.data = {
            'items': items,
            'pageinfo': paginator.to_dict(pageinfo),
            'data': data
        }
        return response.get_jsonp_response(request)

class CheckProductHasPromotion(resource.Resource):
    app = 'mall2'
    resource = 'check_product_has_promotion'

    @login_required
    def api_get(request):
        product_id = request.GET.get('product_id', 0)
        buy_in_supplier = request.GET.get('buy_in_supplier', 0)
        if not buy_in_supplier:
            return create_response(200).get_response()
        if product_id:
            promotion_relation = promotion_model.ProductHasPromotion.objects.filter(promotion__owner=request.manager, product_id=product_id, promotion__status__in=[promotion_model.PROMOTION_STATUS_STARTED, promotion_model.PROMOTION_STATUS_NOT_START])
            group_records = group_models.Group.objects(product_id=product_id,status__lte=1)
            forbidden_coupon_product_relation = promotion_model.ForbiddenCouponProduct.objects.filter(
                    owner=ForbiddenCouponProduct,
                    product_id=product_id,
                    status__in=[promotion_model.FORBIDDEN_STATUS_NOT_START, promotion_model.FORBIDDEN_STATUS_STARTED]
                )
            if promotion_relation.count() + group_records.count() + forbidden_coupon_product_relation.count() > 0:
                return create_response(500).get_response()
            else:
                return create_response(200).get_response()
        else:
            return create_response(500).get_response()