# -*- coding: utf-8 -*-

from django.template import Context, RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from webapp.modules.mall import signals as mall_signals

from core import paginator
from models import *
from market_tools import export

MARKET_TOOLS_NAV = 'market_tools'
SECOND_NAV_NAME = 'delivery_plan'


########################################################################
# list_delivery_plan: 获取套餐列表
########################################################################
@login_required
def list_delivery_plan(request):
    delivery_plans = DeliveryPlan.objects.filter(owner=request.user, is_deleted=False)
    c = RequestContext(request, {
        'first_nav_name': MARKET_TOOLS_NAV,
        'second_navs': export.get_second_navs(request),
        'second_nav_name': SECOND_NAV_NAME,
        'delivery_plans': delivery_plans,
    })
    return render_to_response('delivery_plan/editor/list_delivery_plan.html', c)


########################################################################
# create_deliver_plan: 生成新套餐
########################################################################
@login_required
def create_deliver_plan(request):
    if request.POST:
        name = request.POST['name']
        frequency = request.POST['frequency']
        type = request.POST['type']
        times = request.POST['times']
        price = request.POST['price']
        original_price = request.POST['original_price']
        product_id = request.POST.get('product_id', 3)
        delivery_plan = DeliveryPlan.objects.create(owner=request.user, name=name, original_product_id=product_id, frequency=frequency, times=times, type=type, product_id=product_id, price=price, original_price=original_price)
        
        mall_signals.create_delivery_product.send(sender=DeliveryPlan, delivery_plan=delivery_plan)
        
        return HttpResponseRedirect(('/market_tools/delivery_plan/'))
    else:
        c = RequestContext(request, {
            'first_nav_name': MARKET_TOOLS_NAV,
            'second_navs': export.get_second_navs(request),
            'second_nav_name': SECOND_NAV_NAME
        })
        return render_to_response('delivery_plan/editor/edit_deliver_plan.html', c)
    
########################################################################
# edit_delivery_plan: 编辑套餐
########################################################################
@login_required
def edit_delivery_plan(request, id):
    delivery_plan = DeliveryPlan.objects.get(id=id)
    if request.POST:
        name = request.POST['name']
        frequency = request.POST['frequency']
        type = request.POST['type']
        times = request.POST['times']
        price = request.POST['price']
        product_id = request.POST.get('product_id', 5)
        delivery_plan.name = name
        delivery_plan.frequency = frequency
        delivery_plan.times = times
        delivery_plan.type = type
        delivery_plan.price = price
        delivery_plan.product_id = product_id
        delivery_plan.save()
        
        return HttpResponseRedirect(('/market_tools/delivery_plan/'))
    else:
         c = RequestContext(request, {
             'first_nav_name': MARKET_TOOLS_NAV,
             'second_navs': export.get_second_navs(request),
             'second_nav_name': SECOND_NAV_NAME, 
             'delivery_plan': delivery_plan
         })
         return render_to_response('delivery_plan/editor/edit_deliver_plan.html', c)
     
########################################################################
# delete_delivery_plan: 删除套餐
########################################################################
@login_required
def delete_delivery_plan(request, id):
    DeliveryPlan.objects.filter(id=id).update(is_deleted=True)
    return HttpResponseRedirect(('/market_tools/delivery_plan/'))
