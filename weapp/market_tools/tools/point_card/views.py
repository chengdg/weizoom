# -*- coding: utf-8 -*-

from django.template import Context, RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from core import paginator
from models import *
from market_tools import export
from excel_response import ExcelResponse

MARKET_TOOLS_NAV = 'market_tools'
SECOND_NAV_NAME = 'point_card'


########################################################################
# list_point_card: 获取充值卡列表
########################################################################
@login_required
def list_point_card(request):
    point_card_rules = PointCardRule.get_all_point_card_rules_list(request.user)
    records = PointCard.objects.filter(owner=request.user).order_by('-id')
    c = RequestContext(request, {
        'first_nav_name': MARKET_TOOLS_NAV,
        'second_navs': export.get_second_navs(request),
        'second_nav_name': SECOND_NAV_NAME,
        'point_card_rules': point_card_rules,
        'records': records
    })
    return render_to_response('point_card/editor/list_point_card.html', c)


########################################################################
# create_point_card_rule: 创建充值卡
########################################################################
@login_required
def create_point_card_rule(request):
    if request.POST:
        name = request.POST['name']
        prefix = request.POST['prefix']
        point = request.POST['point']
        is_add = PointCardRule.objects.filter(owner=request.user, prefix=prefix)
        if is_add:
            c = RequestContext(request, {
                'first_nav_name': MARKET_TOOLS_NAV,
                'second_navs': export.get_second_navs(request),
                'second_nav_name': SECOND_NAV_NAME,
                'is_add': True
            })
            return render_to_response('point_card/editor/edit_point_card.html', c)
        PointCardRule.objects.create(owner=request.user, name=name, prefix=prefix, point=point)
        return HttpResponseRedirect(('/market_tools/point_card/'))
    else:
        c = RequestContext(request, {
            'first_nav_name': MARKET_TOOLS_NAV,
            'second_navs': export.get_second_navs(request),
            'second_nav_name': SECOND_NAV_NAME
        })
        return render_to_response('point_card/editor/edit_point_card.html', c)
    
########################################################################
# edit_point_card_rule: 编辑充值卡
########################################################################
@login_required
def edit_point_card_rule(request, id):
    point_card_rule = PointCardRule.objects.get(id=id)
    if request.POST:
        name = request.POST['name']
#        prefix = request.POST['prefix']
#        point = request.POST['point']
        point_card_rule.name = name
#        point_card_rule.prefix = prefix
#        point_card_rule.point = point
        point_card_rule.save()
        return HttpResponseRedirect(('/market_tools/point_card/'))
    else:
         c = RequestContext(request, {
             'first_nav_name': MARKET_TOOLS_NAV,
             'second_navs': export.get_second_navs(request),
             'second_nav_name': SECOND_NAV_NAME, 
             'point_card_rule': point_card_rule
         })
         return render_to_response('point_card/editor/edit_point_card.html', c)
     
     
########################################################################
# export_point_card_rule: 导出积分充值卡
########################################################################
@login_required
def export_point_card_rule(request):
    rule_id = request.GET['rule_id']
    card_list  = [
        [u'积分充值卡', u'卡号', u'密码', u'包含积分', u'使用状态', u'生成日期']
    ]
    point_cards = PointCard.objects.filter(point_card_rule_id = rule_id)
    for point_card in point_cards:
        card_list.append([
            point_card.point_card_rule.name,
            point_card.point_card_id,
            point_card.password,
            point_card.point,
            POINT_CARD_STATUS2POINT_CARD_STATUS_STR[point_card.status],
            point_card.created_at.strftime('%Y-%m-%d')
        ])

    return ExcelResponse(card_list, output_name=u'积分卡'.encode('utf8'), force_csv=False)
