# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from core import paginator
from core.jsonresponse import JsonResponse,create_response

from market_tools.tools.weizoom_card.models import *
from core.restful_url_route import api
from mall.models import *
from django.contrib.auth.models import User
from modules.member.models import Member
from utils.string_util import byte_to_hex,hex_to_byte
from datetime import datetime
from core import dateutil


@api(app='card', resource='cards_num_census', action='get')
@login_required
def get_cards_num_census(request):
    """
    微众卡列表页面
    """
    count_per_page = int(request.GET.get('count_per_page', '1'))
    cur_page = int(request.GET.get('page', '1'))
    filter_value = request.GET.get('filter_value', None)
    query_string=request.META['QUERY_STRING']
    cards,pageinfo= get_num_cards(filter_value,cur_page,count_per_page,query_string)
    cards = sorted(cards.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])),reverse=True)
    response = create_response(200)
    response.data.items = cards
    response.data.sortAttr = request.GET.get('sort_attr', 'money')
    response.data.pageinfo = paginator.to_dict(pageinfo)
    
    return response.get_response()


@api(app='card', resource='card_num_details', action='get')
@login_required
def get_card_num_details(request):
    """
    微众卡明细页面
    """
    card_id = request.GET.get('card_id','')
    #处理过滤
    filter_value = request.GET.get('filter_value', None)
    count_per_page = int(request.GET.get('count_per_page', '1'))
    cur_page = int(request.GET.get('page', '1'))
    card_orders = get_num_details(card_id,filter_value)
    pageinfo, card_orders = paginator.paginate(card_orders, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

    cards = []
    for  card_order in card_orders:
        cur_weizoom_card = JsonResponse()
        order = Order.objects.get(order_id=card_order.order_id)
        cur_weizoom_card.created_at = card_order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        cur_weizoom_card.orderid = order.id
        cur_weizoom_card.order_id = card_order.order_id
        cur_weizoom_card.owner = User.objects.get(id=card_order.owner_id).username
        cur_weizoom_card.money = '%.2f' % card_order.money
        cur_weizoom_card.remainder = '%.2f' % card_order.remainder
        #获取order对应的会员
        webappuser2member = Member.members_from_webapp_user_ids([order.webapp_user_id])
        #获取order对应的member的显示名
        member = webappuser2member.get(order.webapp_user_id, None)
        if member:
            cur_weizoom_card.use_name = member.username_for_html
        else:
           cur_weizoom_card.use_name = u'未知'
        cards.append(cur_weizoom_card)
    response = create_response(200)
    response.data.items = cards
    response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
    response.data.pageinfo = paginator.to_dict(pageinfo)

    return response.get_response()


@api(app='card', resource='card_num_filter_params', action='get')
@login_required
def get_card_num_filter_params(request):
    # 卡类型

    cardTypes = [
        {'name': u'外部卡', 'value': WEIZOOM_CARD_EXTERNAL_USER},
        {'name': u'内部卡', 'value': WEIZOOM_CARD_INTERNAL_USER},
        {'name': u'赠品卡', 'value': WEIZOOM_CARD_GIFT_USER}
    ]
    # 状态
    cardStatus = [
        {'name': u'未激活', 'value': WEIZOOM_CARD_STATUS_INACTIVE},
        {'name': u'未使用', 'value': WEIZOOM_CARD_STATUS_UNUSED},
        {'name': u'使用中', 'value': WEIZOOM_CARD_STATUS_USED},
        {'name': u'已用完', 'value': WEIZOOM_CARD_STATUS_EMPTY},
        {'name': u'已过期', 'value': 4},
        
    ]
    response = create_response(200)
    response.data = {
        "cardTypes": cardTypes,
        "cardStatus": cardStatus
    }
    return response.get_response()


#获得按卡号统计的集合
def get_num_cards(filter_value, cur_page=None, count_per_page=None, query_string=""):
    card_relation2orders = WeizoomCardHasOrder.objects.exclude(order_id=-1)
    weizoom_cards = WeizoomCard.objects.all()
    
    #处理过滤
    filter_data_args = {}

    if filter_value:
        filter_data_dict = {}
        for filter_data_item in filter_value.split('|'):
            try:
                key, value = filter_data_item.split(":")
            except:
                key = filter_data_item[:filter_data_item.find(':')]
                value = filter_data_item[filter_data_item.find(':')+1:]

            filter_data_dict[key] = value
        if filter_data_dict.has_key('card_id'):
            # filter_data_args["weizoom_card_id__contains"] = filter_data_dict['card_id']
            weizoom_cards = weizoom_cards.filter(weizoom_card_id__contains=filter_data_dict['card_id'])

        if filter_data_dict.has_key('name'):
            rules = WeizoomCardRule.objects.filter(name__contains=filter_data_dict['name'])
            rule_ids = []
            if rules:
                for rule in rules:
                    rule_ids.append(rule.id)
                # filter_data_args["weizoom_card_rule_id__in"] = rule_ids
                weizoom_cards = weizoom_cards.filter(weizoom_card_rule_id__in=rule_ids)
            else:
                # filter_data_args["weizoom_card_rule_id"] = -1
                weizoom_cards = weizoom_cards.filter(weizoom_card_rule_id=-1)

        if filter_data_dict.has_key('status'):
            if filter_data_dict['status'] == "4":
                weizoom_cards = weizoom_cards.filter(is_expired=True)
            else:
                weizoom_cards = weizoom_cards.filter(is_expired=False, status=filter_data_dict['status'])

        if filter_data_dict.has_key('type'):
            rules = WeizoomCardRule.objects.filter(card_type=int(filter_data_dict['type']))
            if rules:
                rule_ids = []
                for rule in rules:
                    rule_ids.append(rule.id)
                # filter_data_args["weizoom_card_rule_id__in"] = rule_ids
                weizoom_cards = weizoom_cards.filter(weizoom_card_rule_id__in=rule_ids)
            else:
                # filter_data_args["weizoom_card_rule_id"] = -1
                weizoom_cards = weizoom_cards.filter(weizoom_card_rule_id=-1)

        if filter_data_dict.has_key('created_at'):
            value = filter_data_dict['created_at']
            if value.find('--') > -1:
                val1,val2 = value.split('--')
                low_date = val1 +' 00:00:00'
                high_date = val2 +' 23:59:59'
                # filter_data_args['created_at__gte'] = low_date
                # filter_data_args['created_at__lte'] = high_date
                weizoom_cards = weizoom_cards.filter(created_at__gte=low_date,created_at__lte=high_date)

        if filter_data_dict.has_key('member'):
            member_ids = []
            for member in  Member.objects.filter(username_hexstr__contains=byte_to_hex(filter_data_dict['member'])):
                member_ids.append(member.id)
            if member_ids:
                app_users = WebAppUser.objects.filter(member_id__in=member_ids)
                app_user_ids = [a.id for a in app_users]
                orders = Order.objects.filter(webapp_user_id__in=app_user_ids)
                card_ids = []
                card_relation2orders = card_relation2orders.filter(order_id__in=[o.order_id for o in orders])
                card_has_order_dict = {}
                for one_relation in card_relation2orders:
                    order_id = one_relation.order_id
                    if not card_has_order_dict.has_key(order_id):
                        card_has_order_dict[order_id] = [one_relation]
                    else:
                        card_has_order_dict[order_id].append(one_relation)
                for order in orders:
                    for card in card_has_order_dict.get(order.order_id, []):
                        if card:
                            card_ids.append(card.card_id)
                # filter_data_args["id__in"] = card_ids
                weizoom_cards = weizoom_cards.filter(id__in=card_ids)
            else:
                # filter_data_args["id"] = -1
                weizoom_cards = weizoom_cards.filter(id=-1)

        if filter_data_dict.has_key('money'):
            val1,val2 = filter_data_dict['money'].split('-')
            low_money = float(val1)
            high_money = float(val2)
            card2money={}

            card_relation2orders = card_relation2orders.filter(card_id__in=[card.id for card in weizoom_cards])
            cardid2orders = {}
            for one_order in card_relation2orders:
                card_id = one_order.card_id
                if not cardid2orders.has_key(card_id):
                    cardid2orders[card_id] = [one_order]
                else:
                    cardid2orders[card_id].append(one_order)

            for weizoom_card in weizoom_cards:
                orders = cardid2orders.get(weizoom_card.id, [])
                if orders:
                    for order in orders:
                        if not card2money.has_key(order.card_id):
                            card2money[order.card_id] = order.money
                        else:
                            card2money[weizoom_card.id] += order.money
                else:
                    card2money[weizoom_card.id] = 0
            card_ids = []
            for key,value in card2money.items():
                if value >= low_money and value <= high_money:
                    card_ids.append(key)
            # filter_data_args['id__in'] = card_ids
            weizoom_cards = weizoom_cards.filter(id__in=card_ids)
    else:
        total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), "6", 0)
        low_date = str(low_date) + ' 00:00:00'
        high_date = str(high_date) + ' 23:59:59'
        weizoom_cards = weizoom_cards.filter(created_at__gte=low_date,created_at__lte=high_date)
    #获得已经过期的微众卡id
    today = datetime.today()
    card_ids_need_expire = []
    for card in weizoom_cards:
        #记录过期并且是未使用的微众卡id
        if card.expired_time < today:
            card_ids_need_expire.append(card.id)

    if len(card_ids_need_expire) > 0:
       weizoom_cards.filter(id__in=card_ids_need_expire).update(is_expired=True)

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
    card_id2card_rule = sorted(card_id2card_rule.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])),reverse=True)
    if cur_page:
        pageinfo, card_id2card_rule = paginator.paginate(card_id2card_rule, cur_page, count_per_page, query_string)

    ids = [card[0] for card in card_id2card_rule]
    card2orders = {}
    for order in card_relation2orders.filter(card_id__in=ids).order_by('-created_at'):
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
    for card in card_id2card_rule:
        buyer_name = u''
        order_count = 0
        if card2orders.has_key(card[0]):
            webapp_user_id = member2order[card2orders[card[0]][0].order_id]
            member = all_webappuser2member[webapp_user_id]
            #获取order对应的member的显示名
            # member = webappuser2member.get(webapp_user_id, None)
            if member:
                buyer_name = member.username_for_html
            else:
                buyer_name = u'未知'
            order_count = len(card2orders[card[0]])
        card_type = u''
        if card[1]['card_type'] == WEIZOOM_CARD_EXTERNAL_USER:
            card_type = u'外部卡'
        if card[1]['card_type'] == WEIZOOM_CARD_INTERNAL_USER:
            card_type = u'内部卡'
        if card[1]['card_type'] == WEIZOOM_CARD_GIFT_USER:
            card_type = u'赠品卡'
        status_str = u''
        if card[1]['is_expired']:
            status_str = u'己过期'
        else:
            if card[1]['status']==WEIZOOM_CARD_STATUS_UNUSED:
                status_str = u'未使用'
            if card[1]['status']==WEIZOOM_CARD_STATUS_USED:
                status_str = u'使用中'
            if card[1]['status'] == WEIZOOM_CARD_STATUS_INACTIVE:
                status_str = u'未激活'
            if card[1]['status']==WEIZOOM_CARD_STATUS_EMPTY:
                status_str = u'己用完'
        cur_cards[card[0]]={
            'card_id': card[0],
            'weizoom_card_id': card[1]['weizoom_card_id'],
            'name': card[1]['name'],
            'rule_money': '%.2f' %  card[1]['rule_money'],
            'status' : status_str,
            'money': '%.2f' % card[1]['money'],
            'use_money': '%.2f' % card[1]['use_money'],
            'card_type': card_type,
            'order_count': order_count,
            'buyer_name': buyer_name
        }
    if cur_page:
        return cur_cards,pageinfo
    else:
        return cur_cards

#获取按卡号明细列表
def get_num_details(card_id,filter_value):
    card = WeizoomCard.objects.get(weizoom_card_id=card_id)
    card_relation2orders = WeizoomCardHasOrder.objects.filter(card_id=card.id).exclude(order_id=-1).order_by('-created_at')
    #处理过滤
    filter_data_args = {}

    if filter_value:
        filter_data_dict = {}
        for filter_data_item in filter_value.split('|'):
            try:
                key, value = filter_data_item.split(":")
            except:
                key = filter_data_item[:filter_data_item.find(':')]
                value = filter_data_item[filter_data_item.find(':')+1:]
            filter_data_dict[key] = value
            if key == 'order_id':
                filter_data_args["order_id__contains"] = value

            if key == 'name':
                users = User.objects.filter(username__contains=value)
                user_ids = []
                if users:
                    for user in users:
                        user_ids.append(user.id)
                    filter_data_args["owner_id__in"] = user_ids
                else:
                    filter_data_args["owner_id"] = -1

            if key == 'member':
                member_ids = []
                for member in  Member.objects.filter(username_hexstr__contains=byte_to_hex(value)):
                    member_ids.append(member.id)
                member_webappuser_ids = [member.id for member in WebAppUser.objects.filter(member_id__in=member_ids)]
                if member_ids:
                    order_ids = list(order.order_id for order in Order.objects.filter(webapp_user_id__in=member_webappuser_ids))
                    filter_data_args["order_id__in"] = order_ids
                else:
                    filter_data_args["order_id"] = -1

            if key == 'money':
                val1,val2 = value.split('-')
                filter_data_args['money__gte'] = float(val1)
                filter_data_args['money__lte'] = float(val2)

            if key == 'created_at':
                if value.find('--') > -1:
                    val1,val2 = value.split('--')
                    filter_data_args['created_at__gte'] = val1 +' 00:00:00'
                    filter_data_args['created_at__lte'] = val2 +' 23:59:59'

        card_relation2orders = card_relation2orders.filter(**filter_data_args)
    else:
        total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), "6", 0)
        low_date = str(low_date) + ' 00:00:00'
        high_date = str(high_date) + ' 23:59:59'
        card_relation2orders = card_relation2orders.filter(created_at__gte=low_date, created_at__lte=high_date)
    card_rule = WeizoomCardRule.objects.get(id=card.weizoom_card_rule_id)
    money = card_rule.money #面值
    for order in reversed(card_relation2orders):
        money = order.remainder = money - order.money
    return card_relation2orders