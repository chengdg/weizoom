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
from core import dateutil
from cards_channel_api_views import get_channel_cards
from cards_channel_api_views import get_channel_details


@view(app='card', resource='cards_channel_census', action='get')
@login_required
def get_chan_channel_census(request):
    """
    微众卡列表页面
    """
    has_cards = (WeizoomCard.objects.filter().count() > 0)
    c = RequestContext(request, {
        'first_nav_name': export.MALL_CARD_FIRST_NAV,
        'second_navs': export.get_card_second_navs(request),
        'second_nav_name': export.MALL_CARD_CENSUS_NAV,
        'third_nav_name': export.MALL_CARD_BY_CHANNEL_NAV,
        'has_cards': has_cards,
    })
    return render_to_response('card/editor/list_weizoom_channel_card.html', c)


@view(app='card', resource='card_channel_details', action='get')
@login_required
def get_card_channel_details(request):
    """
    微众卡明细页面
    """
    owner_id = request.GET.get('owner_id','')
    start_date = request.GET.get('start_date','')
    end_date = request.GET.get('end_date','')
    channel = User.objects.get(id=owner_id)
    if not start_date:
        total_days, start_date, cur_date, end_date = dateutil.get_date_range(dateutil.get_today(), "6", 0)
        start_date = str(start_date) + ' 00:00:00'
        end_date = str(end_date) + ' 23:59:59'
    orders = WeizoomCardHasOrder.objects.filter(owner_id=owner_id,created_at__gte=start_date,created_at__lte=end_date).exclude(order_id=-1)
    use_money = 0
    card_ids = set()
    order_ids = set()
    for order in orders:
        use_money += order.money
        card_ids.add(order.card_id)
        order_ids.add(order.order_id)
    channel.use_money = '%.2f' % use_money
    channel.order_count = len(order_ids)
    channel.use_count = len(card_ids)
    channel.start_date= start_date
    channel.end_date= end_date

    c = RequestContext(request, {
        'first_nav_name': export.MALL_CARD_FIRST_NAV,
        'second_navs': export.get_card_second_navs(request),
        'second_nav_name': export.MALL_CARD_CENSUS_NAV,
        'third_nav_name': export.MALL_CARD_BY_CHANNEL_NAV,
        'channel': channel,
        'has_order': orders.count()>0,
        'owner_id': owner_id
    })
    return render_to_response('card/editor/weizoom_channel_card_detail.html', c)


@view(app='card', resource='channel', action='export')
@login_required
def export_channel(request):
    #处理排序
    sort_attr = request.GET.get('sort_attr', '-use_money')
    #处理过滤
    filter_value = request.GET.get('filter_value', None)

    channel = get_channel_cards(sort_attr,filter_value)

    members_info = [
        [u'渠道名称',u'消费金额',u'订单数',u'使用张数']
    ]
    for ch in channel:
        channel_card = ch[1]
        channel_name = channel_card['first_name']
        use_money = channel_card['use_money']
        order_count = channel_card['order_count']
        use_count = channel_card['use_count']
        info_list = [
            channel_name,
            use_money,
            order_count,
            use_count
        ]
        members_info.append(info_list)

    return ExcelResponse(members_info,output_name=u'微众卡按渠道统计列表'.encode('utf8'),force_csv=False)


@view(app='card', resource='channel_detail', action='export')
@login_required
def export_channel_detail(request):
    owner_id = request.GET.get('owner_id',-1)
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    filter_value = request.GET.get('filter_value', None)
    channel_orders = get_channel_details(owner_id,start_date,end_date,filter_value)
    members_info = [
        [u'消费时间', u'订单号',u'卡名称',u'卡号',u'状态',u'面值',u'消费金额',u'使用人']
    ]
    for order in channel_orders:
        created_at = order[1][0]['created_at']
        order_id = order[1][0]['order_id']
        use_name = order[1][0]['buyer_name']
        i=0
        for o in order[1]:
            if i <1:
                info_list=[
                    created_at,
                    order_id,
                    o['rule_name'],
                    o['weizoom_card_id'],
                    o['status'],
                    o['rule_money'],
                    o['use_money'],
                    use_name
                ]
            else:
                info_list=[
                    "",
                    "",
                    o['rule_name'],
                    o['card_id'],
                    o['status'],
                    o['rule_money'],
                    o['use_money'],
                    ""
                ]
            i += 1

            members_info.append(info_list)

    return ExcelResponse(members_info,output_name=u'微众卡按渠道统计消费列表'.encode('utf8'),force_csv=False)