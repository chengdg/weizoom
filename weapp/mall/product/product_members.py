# -*- coding: utf-8 -*-
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from watchdog.utils import watchdog_warning, watchdog_error


from core import resource
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from mall import models  # 注意不要覆盖此module
from mall import export
from modules.member.models import MemberGrade,MemberTag
from member.util import build_return_members_json
import logging

COUNT_PER_PAGE = 50

class ProductMember(resource.Resource):
    app = 'mall2'
    resource = 'product_members'

    @login_required
    def get(request):
        """购买该商品的会员列表


        Requirement:
          id(str): must be provided,
                            商品id必须提供， 

        Return:
          HttpResponse: the context in it include:{
            'first_nav_name',
            'second_navs',
            'second_nav_name',
            'id'
          }

        Raise:
          if id is not be provided return product_list
          如果id没有被提供， 将返回到在售商品列表
        """
        mall_type = request.user_profile.webapp_type
        webapp_id = request.user_profile.webapp_id
        if not mall_type:
            return HttpResponseRedirect('/mall2/product_list/?shelve_type=1')
        has_product_id = request.GET.get('id')
        if has_product_id:
            try:
                product = models.Product.objects.get(owner=request.manager, id=has_product_id)
            except models.Product.DoesNotExist:
                return Http404
        else:
            return Http404
        member_tags = MemberTag.get_member_tags(webapp_id)
        member_grades = MemberGrade.get_all_grades_list(webapp_id)
        #调整排序，将为分组放在最前面
        tags = []
        for tag in member_tags:
            if tag.name == '未分组':
                tags = [tag] + tags
            else:
                tags.append(tag)
        member_tags = tags
        #0:下架（待售） 1:上架（在售）
        if product.shelve_type == 0:
            second_nav_name = export.PRODUCT_MANAGE_OFF_SHELF_PRODUCT_NAV
        else:
            second_nav_name = export.PRODUCT_MANAGE_ON_SHELF_PRODUCT_NAV
        c = RequestContext(
            request,
            {'first_nav_name': export.PRODUCT_FIRST_NAV,
             'second_navs': export.get_mall_product_second_navs(request),
             'second_nav_name': second_nav_name,
             'product_name': product.name,
             'mall_type': mall_type,
             'shelve_type':product.shelve_type,
             'id':has_product_id,
             'user_tags': member_tags,
             'grades': member_grades,
             }
        )
        return render_to_response('mall/editor/product_member.html', c)


    @login_required
    def api_get(request):
        """获取商品下的会员列表
        API:
            method: get
            url: mall2/product_members/

        """

        # 商城类型
        mall_type = request.user_profile.webapp_type
        webapp_id = request.user_profile.webapp_id
        has_product_id = request.GET.get('id')
        
        sort_attr = request.GET.get('sort_attr', '-id') #之后处理
        order_has_products = models.OrderHasProduct.objects.filter(product_id=has_product_id, origin_order_id=0)
        order_ids = order_has_products.values_list('order', flat=True)
        orders = models.Order.objects.filter(webapp_id=webapp_id, id__in=order_ids,status__in=[models.ORDER_STATUS_PAYED_NOT_SHIP, 
            models.ORDER_STATUS_PAYED_SHIPED, models.ORDER_STATUS_SUCCESSED, models.ORDER_STATUS_REFUNDING, models.ORDER_STATUS_GROUP_REFUNDING])
        webapp_user_ids = orders.values_list('webapp_user_id', flat=True)

        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))

        data = build_return_members_json(webapp_user_ids,cur_page=cur_page,count_per_page=count_per_page,sort_attr=sort_attr, webapp_id=webapp_id)
        response = create_response(200)
        response.data = data
        return response.get_response()

