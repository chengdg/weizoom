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
    resource = 'product_members'

    @login_required
    def get(request):
        """购买该商品的会员列表


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
        has_product = models.Product.objects.filter(
            owner=request.manager,
            shelve_type=shelve_type,
            is_deleted=False
        ).exists()
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

        #处理商品分类
        if _type == 'offshelf':