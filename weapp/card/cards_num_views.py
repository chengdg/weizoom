# -*- coding: utf-8 -*-
import re
from core.jsonresponse import create_response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from card import export
from core.restful_url_route import view, api

from market_tools.tools.weizoom_card.models import *
from modules.member.models import Member
from excel_response import ExcelResponse
from mall.models import *
from cards_num_api_views import get_num_cards,get_num_details
from cards_channel_views import export_csv


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
    start_date = request.GET.get('start_date','')
    end_date = request.GET.get('end_date','')
    card = WeizoomCard.objects.get(weizoom_card_id=card_id)
    active_card_user_id = card.active_card_user_id
    IS_CARD_RULE = request.GET.get('IS_CARD_RULE','')

    # if not start_date:
    #     total_days, start_date, cur_date, end_date = dateutil.get_date_range(dateutil.get_today(), "6", 0)
    #     start_date = str(start_date) + ' 00:00:00'
    #     end_date = str(end_date) + ' 23:59:59'
    if card:
        status_str = u''
        password_is_show = False
        if card.is_expired:
            status_str = u'己过期'
            password_is_show = True
        else:
            if card.status==WEIZOOM_CARD_STATUS_UNUSED:
                status_str = u'未使用'
                if active_card_user_id == request.user.id:
                    password_is_show = True
            if card.status==WEIZOOM_CARD_STATUS_USED:
                status_str = u'使用中'
                if active_card_user_id == request.user.id:
                    password_is_show = True
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
        card_operations = WeizoomCardOperationLog.objects.filter(card_id=card.id)
        card.start_date= start_date
        card.end_date= end_date

        if IS_CARD_RULE =='TRUE':
            c = RequestContext(request, {
                'first_nav_name': export.MALL_CARD_FIRST_NAV,
                'second_navs': export.get_card_second_navs(request),
                'second_nav_name': export.MALL_CARD_MANAGER_NAV,
                'card_rule_name': card_rule_name,
                'weizoom_card_rule_id': weizoom_card_rule_id,
                'card': card,
                'card_orders': card_orders,
                'card_operations': card_operations,
                'IS_CARD_RULE': True,
                'password_is_show':password_is_show
            })
        else:
            c = RequestContext(request, {
                'first_nav_name': export.MALL_CARD_FIRST_NAV,
                'second_navs': export.get_card_second_navs(request),
                'second_nav_name': export.MALL_CARD_CENSUS_NAV,
                'third_nav_name': export.MALL_CARD_BY_CARD_NAV,
                'card': card,
                'card_orders': card_orders,
                'card_operations': card_operations,
                'IS_CARD_RULE': False
            })

    return render_to_response('card/editor/weizoom_num_card_detail.html', c)


@api(app='card', resource='cards', action='export')
@login_required
def export_cards(request):
    # filter_value = request.POST.get('filter_value', None)
    # cards = get_num_cards(filter_value)
    card_ids = request.POST.get('cards','')
    card_ids = json.loads(card_ids)
    print card_ids,"card_ids"
    weizoom_cards = WeizoomCard.objects.filter(id__in=card_ids)
    rule_ids = [card.weizoom_card_rule_id for card in weizoom_cards]
    rule_id2rule = {rule.id: rule  for rule in  WeizoomCardRule.objects.filter(id__in=rule_ids)}
    card_id2card_rule ={}
    for card in weizoom_cards:
        rule = rule_id2rule[card.weizoom_card_rule_id]
        card_id2card_rule[card.id] = {
            'weizoom_card_id': card.weizoom_card_id,
            'rule_money': rule.money,
            'status': card.status,
            'is_expired': card.is_expired,
            'money': card.money,
            'use_money': rule.money - card.money,
            'name': rule.name,
            'card_type': rule.card_type
        }
    card2orders = {}
    for order in WeizoomCardHasOrder.objects.filter(card_id__in=card_ids).exclude(order_id__in=['-1','-2']).order_by('-created_at'):
        if not card2orders.has_key(order.card_id):
            card2orders[order.card_id] = [order]
        else:
            card2orders[order.card_id].append(order)
    order_ids = set()
    for order in card2orders.values():
        order_ids.add(order[0].order_id)
    member2order = {}
    webapp_user_ids = []
    for order in Order.objects.filter(order_id__in=list(order_ids)):
        member2order[order.order_id]= order.webapp_user_id
        webapp_user_ids.append(order.webapp_user_id)
    cur_cards = {}
    all_webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)
    for k,card in card_id2card_rule.items():
        buyer_name = u''
        order_count = 0
        if card2orders.has_key(k):
            webapp_user_id = member2order[card2orders[k][0].order_id]
            member = all_webappuser2member[webapp_user_id]
            #获取order对应的member的显示名
            # member = webappuser2member.get(webapp_user_id, None)
            if member:
                buyer_name = member.username_for_html
            else:
                buyer_name = u'未知'
            order_ids = set()
            for o in card2orders[k]:
                order_ids.add(o.order_id)
            order_count = len(order_ids)
        card_type = u''
        if card['card_type'] == WEIZOOM_CARD_EXTERNAL_USER:
            card_type = u'外部卡'
        if card['card_type'] == WEIZOOM_CARD_INTERNAL_USER:
            card_type = u'内部卡'
        if card['card_type'] == WEIZOOM_CARD_GIFT_USER:
            card_type = u'赠品卡'
        status_str = u''
        if card['is_expired']:
            status_str = u'己过期'
        else:
            if card['status']==WEIZOOM_CARD_STATUS_UNUSED:
                status_str = u'未使用'
            if card['status']==WEIZOOM_CARD_STATUS_USED:
                status_str = u'使用中'
            if card['status'] == WEIZOOM_CARD_STATUS_INACTIVE:
                status_str = u'未激活'
            if card['status']==WEIZOOM_CARD_STATUS_EMPTY:
                status_str = u'己用完'
        cur_cards[k]={
            'card_id': k,
            'weizoom_card_id': card['weizoom_card_id'],
            'name': card['name'],
            'rule_money': '%.2f' %  card['rule_money'],
            'status' : status_str,
            'money': '%.2f' % card['money'],
            'use_money': '%.2f' % card['use_money'],
            'card_type': card_type,
            'order_count': order_count,
            'buyer_name': buyer_name
        }
    crad_ids = cur_cards.keys()
    cards = sorted(cur_cards.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])),reverse=True)
    members_info = [
        [u'卡号', u'面额', u'建卡日期', u'建卡人', u'到期时间', u'领用人', u'领用日期', u'激活日期', u'激活人', u'已消费金额',u'余额',u'备注']
    ]
    all_nedded_cards = WeizoomCard.objects.filter(id__in=crad_ids)
    cards_id2card = {c.id: c for c in all_nedded_cards}
    for ch in cards:
        card = cards_id2card[ch[0]]
        weizoom_card_id = ch[1]['weizoom_card_id']
        weizoom_card_name = ch[1]['name']
        weizoom_card_rule_money = ch[1]['rule_money']
        status = ch[1]['status']
        money = ch[1]['money']
        weizoom_card_type= ch[1]['card_type']
        weizoom_card_use_money =ch[1]['use_money']
        order_count = ch[1]['order_count']
        buyer_name = ch[1]['buyer_name']
        created_at = card.created_at.strftime('%Y-%m-%d %H:%M:%S')
        created_by = 'card_admin'
        expire_time = card.expired_time.strftime('%Y-%m-%d %H:%M:%S')
        activated_to = card.activated_to
        activate_time = card.activated_at.strftime('%Y-%m-%d %H:%M:%S') if card.activated_at else ''
        activated_by = 'card_admin'
        remark = card.remark

        info_list = [
            weizoom_card_id,#卡号
            weizoom_card_rule_money,#面值
            created_at,#建卡日期
            created_by,#建卡人
            expire_time,#到期时间
            activated_to,#领用人
            activate_time,#领用日期
            activate_time,#激活日期
            activated_by,#激活人
            weizoom_card_use_money,#已消费金额
            money,#余额
            remark,#注释
        ]
        members_info.append(info_list)
    # return ExcelResponse(members_info,output_name=u'微众卡按卡号统计列表'.encode('utf8'),force_csv=False)
    filename = u'微众卡按卡号统计列表.xls'#TODO 上线 加.encode('utf8')
    url = export_csv(members_info,filename,force_csv=False)
    response = create_response(200)
    response.data.url = url
    response.data.filename = filename
    return response.get_response()


@api(app='card', resource='card_detail', action='export')
@login_required
def export_card_detail(request):
    card_id = request.POST.get('card_id','')
    filter_value = request.POST.get('filter_value', None)
    start_date = request.POST.get('start_date','')
    end_date = request.POST.get('end_date','')
    card_orders = get_num_details(card_id,filter_value,start_date,end_date)

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
        re_h = re.compile('</?\w+[^>]*>')#HTML标签
        use_name =  re_h.sub('',use_name) #去掉HTML 标签
        info_list = [
                created_at,
                order_id,
                channel,
                money,
                remainder,
                use_name
            ]

        members_info.append(info_list)

    # return ExcelResponse(members_info,output_name=u'微众卡按卡号统计详细列表'.encode('utf8'),force_csv=False)
    filename = u'微众卡按卡号统计详细列表.xls'#TODO 上线 加.encode('utf8')
    url = export_csv(members_info,filename,force_csv=False)
    response = create_response(200)
    response.data.url = url
    response.data.filename = filename
    return response.get_response()
