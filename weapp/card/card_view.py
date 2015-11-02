# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User

from core.restful_url_route import *

from datetime import datetime, timedelta
from card import export
from market_tools.tools.weizoom_card.models import *
from card_api_view import _get_cardNumber_value, _get_status_value
from excel_response import ExcelResponse


@view(app='card', resource='cards', action='get')
@login_required 
def get_cards(request):
    """
    显示卡规则列表
    """
    weizoomcardpermission=WeiZoomCardPermission.objects.filter(user_id=request.user.id)
    can_create_card=weizoomcardpermission[0].can_create_card
    c = RequestContext(request, {
        'first_nav_name': export.MALL_CARD_FIRST_NAV,
        'second_navs': export.get_card_second_navs(request),
        'second_nav_name': export.MALL_CARD_MANAGER_NAV,
        'can_create_card': can_create_card,
    })

    return render_to_response('card/editor/list_weizoom_card.html', c)


@view(app='card', resource='card_create', action='get')
@login_required 
def get_card_create(request):
    """
    显示创建卡规则
    """
    c = RequestContext(request, {
        'first_nav_name': export.MALL_CARD_FIRST_NAV,
        'second_navs': export.get_card_second_navs(request),
        'second_nav_name': export.MALL_CARD_MANAGER_NAV,
    })
    return render_to_response('card/editor/edit_weizoom_card_rule.html', c)


@view(app='card', resource='card_detail', action='get')
@login_required
def get_card_detail(request):
    """
    显示某一规则下的卡列表
    """
    weizoomcardpermission=WeiZoomCardPermission.objects.filter(user_id=request.user.id)
    can_batch_active_card=weizoomcardpermission[0].can_batch_active_card
    can_batch_stop_card=weizoomcardpermission[0].can_batch_stop_card
    can_add_card=weizoomcardpermission[0].can_add_card
    can_export_batch_card=weizoomcardpermission[0].can_export_batch_card
    
    rule_id = request.GET.get('id','')
    if rule_id:
        rule = WeizoomCardRule.objects.get(id=rule_id)
        c = RequestContext(request, {
            'first_nav_name': export.MALL_CARD_FIRST_NAV,
            'second_navs': export.get_card_second_navs(request),
            'second_nav_name': export.MALL_CARD_MANAGER_NAV,
            'weizoom_card_rule': rule,
            'can_batch_active_card': can_batch_active_card,
            'can_batch_stop_card': can_batch_stop_card,
            'can_add_card': can_add_card,
            

        })
        return render_to_response('card/editor/list_weizoom_card_detail.html', c)


@view(app='card', resource='weizoom_cards', action='export')
@login_required
def export_weizoom_cards(request):
    """
    export_weizoom_cards:  导出微众卡
    """
    id = request.GET.get('card_id', 0)
    weizoom_cards = WeizoomCard.objects.filter(weizoom_card_rule_id=id)
    weizoom_card_rule = WeizoomCardRule.objects.get(id =id)
    card_name = weizoom_card_rule.name
    try:
        filter_value = request.GET.get('filter_value', '')
        card_number = _get_cardNumber_value(filter_value)

        cardStatus = _get_status_value(filter_value)

        if card_number != -1:
            card_number = str(card_number)
            weizoom_cards = weizoom_cards.filter(weizoom_card_id__contains=card_number)
        if cardStatus != -1:
            weizoom_cards = weizoom_cards.filter(status=cardStatus)
    except:
        filter_value = -1

    titles = [u'卡号', u'密码', u'状态', u'面值/余额', u'已使用金额', u'激活时间', u'有效期', u'备注']
    weizoom_cards_table = []
    weizoom_cards_table.append(titles)
    
    for  c in weizoom_cards:
        status_str = u''
        if c.status==WEIZOOM_CARD_STATUS_EMPTY:
            status_str = u'己用完'
        else:
            if c.is_expired:
                status_str = u'己过期'
            else:
                if c.status==WEIZOOM_CARD_STATUS_UNUSED:
                    status_str = u'未使用'
                if c.status==WEIZOOM_CARD_STATUS_USED:
                    status_str = u'己使用'
                if status_str == u'':
                    status_str = u'未激活'

        if c.activated_at:
            activated_at = c.activated_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            activated_at = ''

        total_money ='%.2f' % weizoom_card_rule.money
        c.used_money = '%.2f' % (float(total_money) - float(c.money))

        c.total_and_balance_money = '%s/%s' % (total_money,c.money)

        if c.remark:
            remark = c.remark
        else:
            remark = ""

        valid_time_from = datetime.strftime(weizoom_card_rule.valid_time_from, '%Y-%m-%d %H:%M')
        valid_time_to = datetime.strftime(weizoom_card_rule.valid_time_to, '%Y-%m-%d %H:%M')
        c.time = '%s/%s' % (valid_time_from,valid_time_to)
        info = [
            c.weizoom_card_id,
            c.password, 
            status_str,
            c.total_and_balance_money, 
            c.used_money, 
            activated_at, 
            c.time,
            remark
        ]
        weizoom_cards_table.append(info)
    
    return ExcelResponse(weizoom_cards_table,output_name=card_name.encode('utf8'),force_csv=False)