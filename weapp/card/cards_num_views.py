# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from card import export
from core.restful_url_route import view

from market_tools.tools.weizoom_card.models import *
from modules.member.models import Member
from excel_response import ExcelResponse
from mall.models import *
from cards_num_api_views import get_num_cards,get_num_details


@view(app='card', resource='cards_num_census', action='get')
@login_required
def get_cards_num_census(request):
    """
    微众卡列表页面
    """
    has_cards = (WeizoomCard.objects.filter().count() > 0)
    c = RequestContext(request, {
        'first_nav_name': export.MALL_CARD_FIRST_NAV,
        'second_navs': export.get_card_second_navs(request),
        'second_nav_name': export.MALL_CARD_CENSUS_NAV,
        'third_nav_name': export.MALL_CARD_BY_CARD_NAV,
        'has_cards': has_cards,
    })
    return render_to_response('card/editor/list_weizoom_num_card.html', c)


@view(app='card', resource='card_num_details', action='get')
@login_required
def get_card_num_details(request):
    """
    微众卡明细页面
    """
    card_id = request.GET.get('card_id','')
    card = WeizoomCard.objects.get(weizoom_card_id=card_id)
    IS_CARD_RULE = request.GET.get('IS_CARD_RULE','')

    if card:
        status_str = u''
        if card.is_expired:
            status_str = u'己过期'
        else:
            if card.status==WEIZOOM_CARD_STATUS_UNUSED:
                status_str = u'未使用'
            if card.status==WEIZOOM_CARD_STATUS_USED:
                status_str = u'使用中'
            if card.status == WEIZOOM_CARD_STATUS_INACTIVE:
                status_str = u'未激活'
            if card.status==WEIZOOM_CARD_STATUS_EMPTY:
                status_str = u'己用完'

        card.status_str = status_str
        card_rule = WeizoomCardRule.objects.get(id=card.weizoom_card_rule_id)
        card.rule_name = card_rule.name
        card.rule_money = card_rule.money
        card_rule_name = card.rule_name
        weizoom_card_rule_id = card_rule.id
        card_type = u''
        if card_rule.card_type == WEIZOOM_CARD_EXTERNAL_USER:
            card_type = u'外部卡'
        if card_rule.card_type == WEIZOOM_CARD_INTERNAL_USER:
            card_type = u'内部卡'
        if card_rule.card_type == WEIZOOM_CARD_GIFT_USER:
            card_type = u'赠品卡'
        card.type = card_type
        card_orders = WeizoomCardHasOrder.objects.filter(card_id=card.id)

        if IS_CARD_RULE =='TRUE':
            c = RequestContext(request, {
                'first_nav_name': export.MALL_CARD_FIRST_NAV,
                'second_navs': export.get_card_second_navs(request),
                'second_nav_name': export.MALL_CARD_MANAGER_NAV,
                'card_rule_name': card_rule_name,
                'weizoom_card_rule_id': weizoom_card_rule_id,
                'card': card,
                'card_orders': card_orders,
                'IS_CARD_RULE': True
            })
        else:
            c = RequestContext(request, {
                'first_nav_name': export.MALL_CARD_FIRST_NAV,
                'second_navs': export.get_card_second_navs(request),
                'second_nav_name': export.MALL_CARD_CENSUS_NAV,
                'third_nav_name': export.MALL_CARD_BY_CARD_NAV,
                'card': card,
                'card_orders': card_orders,
                'IS_CARD_RULE': False
            })

    return render_to_response('card/editor/weizoom_num_card_detail.html', c)


@view(app='card', resource='cards', action='export')
@login_required
def export_cards(request):
    filter_value = request.GET.get('filter_value', None)
    cards = get_num_cards(filter_value)
    cards = sorted(cards.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])),reverse=True)
    members_info = [
        [u'卡号', u'卡名称',u'面值',u'状态',u'余额',u'卡类型',u'消费金额',u'订单数',u'使用人']
    ]
    for ch in cards:
        weizoom_card_id = ch[1]['weizoom_card_id']
        weizoom_card_name = ch[1]['name']
        weizoom_card_rule_money = ch[1]['rule_money']
        status = ch[1]['status']
        money = ch[1]['money']
        weizoom_card_type= ch[1]['card_type']
        weizoom_card_use_money =ch[1]['use_money']
        order_count = ch[1]['order_count']
        buyer_name = ch[1]['buyer_name']
        info_list = [
            weizoom_card_id,
            weizoom_card_name,
            weizoom_card_rule_money,
            status,
            money,
            weizoom_card_type,
            weizoom_card_use_money,
            order_count,
            buyer_name
        ]
        members_info.append(info_list)
    return ExcelResponse(members_info,output_name=u'微众卡按卡号统计列表'.encode('utf8'),force_csv=False)


@view(app='card', resource='card_detail', action='export')
@login_required
def export_card_detail(request):
    card_id = request.GET.get('card_id','')
    filter_value = request.GET.get('filter_value', None)
    card_orders = get_num_details(card_id,filter_value)

    members_info = [
        [u'消费时间', u'订单号',u'渠道',u'消费金额',u'余额',u'使用人']
    ]

    for card in card_orders:
        order = Order.objects.get(order_id=card.order_id)
        created_at = card.created_at
        order_id = card.order_id
        channel = User.objects.get(id=card.owner_id).username
        money = '%.2f' % card.money
        remainder = '%.2f' % card.remainder
        #获取order对应的会员
        webappuser2member = Member.members_from_webapp_user_ids([order.webapp_user_id])
        #获取order对应的member的显示名
        member = webappuser2member.get(order.webapp_user_id, None)
        if member:
            use_name = member.username_for_html
        else:
            use_name = u'未知'
        info_list = [
                created_at,
                order_id,
                channel,
                money,
                remainder,
                use_name
            ]

        members_info.append(info_list)

    return ExcelResponse(members_info,output_name=u'微众卡按卡号统计列表'.encode('utf8'),force_csv=False)
