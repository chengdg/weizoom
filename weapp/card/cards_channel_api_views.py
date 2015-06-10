# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from core import paginator
from core.jsonresponse import JsonResponse,create_response

from market_tools.tools.weizoom_card.models import *
from core.restful_url_route import api
from mall.models import *
from django.contrib.auth.models import User
from modules.member.models import Member
from utils.string_util import byte_to_hex
from core import dateutil
import datetime


@api(app='card', resource='cards_channel_census', action='get')
@login_required
def get_cards_channel_census(request):
    """
    channel列表页面
    """
    count_per_page = int(request.GET.get('count_per_page', '1'))
    cur_page = int(request.GET.get('page', '1'))
    sort_attr = request.GET.get('sort_attr', '-use_money')
    filter_value = request.GET.get('filter_value', None)
    query_string=request.META['QUERY_STRING']
    channel,pageinfo = get_channel_cards(sort_attr,filter_value,cur_page,count_per_page,query_string)
    response = create_response(200)
    response.data.items = channel
    response.data.sortAttr = request.GET.get('sort_attr', '-use_money')
    response.data.pageinfo = paginator.to_dict(pageinfo)
    
    return response.get_response()


@api(app='card', resource='card_channel_details', action='get')
@login_required
def get_card_channel_details(request):
    """
    微众卡明细页面
    """
    owner_id = request.GET.get('owner_id',-1)
    count_per_page = int(request.GET.get('count_per_page', '1'))
    cur_page = int(request.GET.get('page', '1'))
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    filter_value = request.GET.get('filter_value', None)
    query_string=request.META['QUERY_STRING']
    channel_orders,pageinfo = get_channel_details(owner_id,start_date,end_date,filter_value,cur_page,count_per_page,query_string)



    response = create_response(200)
    response.data.items = channel_orders
    response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
    response.data.pageinfo = paginator.to_dict(pageinfo)

    return response.get_response()


@api(app='card', resource='card_channel_filter_params', action='get')
@login_required
def get_card_channel_filter_params(request):
    # 状态
    cardStatus = [
        {'name': u'未激活', 'value': WEIZOOM_CARD_STATUS_INACTIVE},
        {'name': u'使用中', 'value': WEIZOOM_CARD_STATUS_USED},
        {'name': u'已用完', 'value': WEIZOOM_CARD_STATUS_EMPTY},
        {'name': u'已过期', 'value': 4},
        
    ]
    response = create_response(200)
    response.data = {
        "cardStatus": cardStatus
    }
    return response.get_response()


def get_channel_cards(sort_attr,filter_value,cur_page=None,count_per_page=None,query_string=""):
    orders_relation2card = WeizoomCardHasOrder.objects.exclude(order_id=-1)
    #处理过滤
    filter_data_args = {}
    filter_data_dict = {}
    start_date = end_date = ''
    if filter_value:
        for filter_data_item in filter_value.split('|'):
            try:
                key, value = filter_data_item.split(":")
            except:
                key = filter_data_item[:filter_data_item.find(':')]
                value = filter_data_item[filter_data_item.find(':')+1:]
            filter_data_dict[key] = value

        if filter_data_dict.has_key('created_at'):
            value = filter_data_dict['created_at']
            if value.find('--') > -1:
                val1,val2 = value.split('--')
                start_date = val1 +' 00:00:00'
                end_date = val2 +' 23:59:59'
                orders_relation2card = orders_relation2card.filter(created_at__gte=start_date,created_at__lte=end_date)
                owner_ids =list(order.owner_id for order in orders_relation2card)
                if not filter_data_args.has_key('id__in'):
                    filter_data_args['id__in'] = owner_ids
                else:
                    old_owner_ids = filter_data_args['id__in']
                    new_owner_ids = list(set(old_owner_ids).intersection(set(owner_ids)))
                    filter_data_args['id__in'] = new_owner_ids
        if filter_data_dict.has_key('money'):
            value = filter_data_dict['money']
            val1,val2 = value.split('-')
            low_money = float(val1)
            high_money = float(val2)
            owner_ids = []
            user2orders = {}
            user2money= {}
            for order in orders_relation2card:
                user_id = order.owner_id
                if not user2orders.has_key(user_id):
                    user2orders[user_id] =[order]
                    user2money[user_id]= order.money
                else:
                    user2orders[user_id].append(order)
                    user2money[user_id] += order.money
            for k,v in user2money.items():
                if v >= low_money and v <= high_money:
                    owner_ids.append(k)
            filter_data_args['id__in'] = owner_ids
            orders_relation2card = orders_relation2card.filter(owner_id__in=owner_ids)
        if filter_data_dict.has_key('channel'):

            filter_data_args['username__contains'] = filter_data_dict['channel']

        users = User.objects.filter(**filter_data_args)
        if not users.exists():
            pageinfo, result = paginator.paginate([], cur_page, count_per_page, query_string)
            return result,pageinfo

    total_days, low_date, cur_date, height_date = dateutil.get_date_range(dateutil.get_today(), "6", 0)
    if not filter_value:
        start_date = str(low_date) + ' 00:00:00'
        end_date = str(height_date) + ' 23:59:59'
        orders_relation2card = orders_relation2card.filter(created_at__gte=start_date, created_at__lte=end_date)
        users = User.objects.filter(id__in=list(order.owner_id for order in orders_relation2card))

    user2orders = {}
    user2card = {}
    users_id2username = {user.id: user.username for user in users}
    for order_relation2card in orders_relation2card:
        order = order_relation2card
        user_id = order.owner_id
        try:
            username = users_id2username[user_id]
        except:
            continue
        if not user2orders.has_key(user_id):
            user2orders[user_id] =[order_relation2card]
            user2card[user_id]={
                'first_name': username,
                'card_ids': set([order.card_id]),
                'order_ids': set([order.order_id]),
                'use_money': order.money
            }
        else:
            user2orders[user_id].append(order_relation2card)
            user2card_dict = user2card[user_id]
            user2card_dict['card_ids'].add(order.card_id)
            user2card_dict['order_ids'].add(order.order_id)
            user2card_dict['use_money'] += order.money
    user2card = sorted(user2card.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])),reverse=True)
    if cur_page:
        pageinfo, user2card = paginator.paginate(user2card, cur_page, count_per_page, query_string)
    channel = {}
    for card in user2card:
        channel_card = card[1]
        channel[card[0]] ={
            'owner_id': card[0],
            'first_name': channel_card['first_name'],
            'use_money': '%.2f' % channel_card['use_money'],
            'order_count': len(channel_card['order_ids']),
            'use_count': len(channel_card['card_ids']),
            'start_date': start_date,
            'end_date': end_date
        }
    if sort_attr == "-use_money":
        #channel按消费金额倒序
        channel = sorted(channel.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])),reverse=True)
    elif sort_attr == "use_money":
        #channel按消费金额正序
        channel = sorted(channel.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])))

    elif sort_attr == "-order_count":
        #channel按订单数倒序
        channel = sorted(channel.items(), lambda x, y: cmp(x[1]['order_count'], y[1]['order_count']),reverse=True)
    elif sort_attr == "order_count":
        #channel按订单数正序
        channel = sorted(channel.items(), lambda x, y: cmp(x[1]['order_count'], y[1]['order_count']))

    elif sort_attr == "-use_count":
        #channel按使用人数倒序
        channel = sorted(channel.items(), lambda x, y: cmp(x[1]['use_count'], y[1]['use_count']),reverse=True)
    else:
        #channel按使用人数正序
        channel = sorted(channel.items(), lambda x, y: cmp(x[1]['use_count'], y[1]['use_count']))
    if cur_page:
        return channel,pageinfo
    else:
        return channel


def get_channel_details(owner_id,start_date,end_date,filter_value,cur_page=None,count_per_page=None,query_string=""):
    if not start_date:
        total_days, start_date, cur_date, end_date = dateutil.get_date_range(dateutil.get_today(), "6", 0)
        start_date = str(start_date) + ' 00:00:00'
        end_date = str(end_date) + ' 23:59:59'
    orders = WeizoomCardHasOrder.objects.filter(owner_id=owner_id,created_at__gte=start_date,created_at__lte=end_date).exclude(order_id=-1).order_by('-created_at')

    #处理过滤
    filter_data_args = {}
    filter_card_rule_ids = []
    if filter_value:
        filter_data_dict = {}
        filter_data_args['created_at__gte'] = start_date
        filter_data_args['created_at__lte'] = end_date
        for filter_data_item in filter_value.split('|'):
            try:
                key, value = filter_data_item.split(":")
            except:
                key = filter_data_item[:filter_data_item.find(':')]
                value = filter_data_item[filter_data_item.find(':')+1:]

            filter_data_dict[key] = value
        created_at = filter_data_dict['created_at']
        start_date_f = ""
        end_date_f = ""
        if created_at.find('--') > -1:
            v1,v2 = created_at.split('--')
            start_date_f = v1 +' 00:00:00'
            end_date_f = v2 +' 23:59:59'
        orders = WeizoomCardHasOrder.objects.filter(owner_id=owner_id,created_at__gte=start_date_f,created_at__lte=end_date_f).exclude(order_id=-1)
        for key,value in filter_data_dict.items():

            #卡号
            if key == 'card_id':
                filter_weizoom_card_id = value
                card_ids = list(card.id for card in WeizoomCard.objects.filter(weizoom_card_id__contains=value))
                if card_ids:
                    filter_data_args["card_id__in"] = card_ids
                else:
                    filter_data_args["card_id__in"] = -1
            #卡名称
            if key == 'name':
                rules = WeizoomCardRule.objects.filter(name__contains=value)
                rule_ids = []
                if rules:
                    for rule in rules:
                        filter_card_rule_ids.append(rule.id)
                    card_ids = list(weizoom_card.id for weizoom_card in WeizoomCard.objects.filter(weizoom_card_rule_id__in=filter_card_rule_ids))
                    if not filter_data_args.has_key('card_id__in'):
                        filter_data_args['card_id__in'] = card_ids
                    else:
                        old_card_ids = filter_data_args['card_id__in']
                        new_card_ids = list(set(old_card_ids).intersection(set(card_ids)))
                        filter_data_args['card_id__in'] = new_card_ids
                else:
                    filter_data_args["card_id__in"] = -1
            #订单号
            if key == 'order_id':
                filter_data_args["order_id__contains"] = value

            if key == 'member':
                member_ids = []
                for member in  Member.objects.filter(username_hexstr__contains=byte_to_hex(value)):
                    member_ids.append(member.id)
                member_webappuser_ids = [member.id for member in WebAppUser.objects.filter(member_id__in=member_ids)]
                if member_ids:
                    order_ids = list(order.order_id for order in Order.objects.filter(webapp_user_id__in=member_webappuser_ids,created_at__gte=start_date,created_at__lte=end_date))
                    filter_data_args["order_id__in"] = order_ids
                else:
                    filter_data_args["order_id"] = -1

            if key == 'status':
                if value == "4":
                    card_ids = list(card.id for card in WeizoomCard.objects.filter(is_expired=True))
                    filter_data_args['card_id__in'] = card_ids
                else:
                    card_ids = list(card.id for card in WeizoomCard.objects.filter(status=value,is_expired=False))
                    filter_data_args['card_id__in'] = card_ids
                if not filter_data_args.has_key('card_id__in'):
                    filter_data_args['card_id__in'] = card_ids
                else:
                    old_card_ids = filter_data_args['card_id__in']
                    new_card_ids = list(set(old_card_ids).intersection(set(card_ids)))
                    filter_data_args['card_id__in'] = new_card_ids

            if key == 'money':
                val1,val2 = value.split('-')
                low_money = float(val1)
                high_money = float(val2)
                card2money= {}
                orderids = []
                if orders:
                    for order in orders:
                        if not card2money.has_key(order.order_id):
                            card2money[order.order_id] = order.money
                        else:
                            card2money[order.order_id] += order.money
                if card2money:
                    for key,value in card2money.items():
                        if value >= low_money and value <= high_money:
                            orderids.append(key)
                    if orderids:
                        if not filter_data_args.has_key('order_id__in'):
                            filter_data_args['order_id__in'] = orderids
                        else:
                            old_card_ids = filter_data_args['order_id__in']
                            new_card_ids = list(set(old_card_ids).intersection(set(orderids)))
                            filter_data_args['order_id__in'] = new_card_ids
                    else:
                        filter_data_args['order_id'] = -1

            if key == 'created_at':
                if value.find('--') > -1:
                    val1,val2 = value.split('--')
                    val1 = val1 +' 00:00:00'
                    val2 = val2 +' 23:59:59'
                    if val1 < start_date:
                        val1 = start_date
                    if val2 > end_date:
                        val2 = end_date
                    filter_data_args['created_at__gte'] = val1
                    filter_data_args['created_at__lte'] = val2
        orders = WeizoomCardHasOrder.objects.filter(**filter_data_args).filter(owner_id=owner_id).exclude(order_id=-1).order_by('-created_at')
    order2card_id = {}
    order_ids = [r.order_id for r in orders]
    real_orders = Order.objects.filter(order_id__in=order_ids)
    order_id2order = dict([(o.order_id, o) for o in real_orders])
    for order in orders:
        real_order = order_id2order[order.order_id]
        if not order2card_id.has_key(order.order_id):
            order2card_id[order.order_id] = [{
                'order_id': order.order_id,
                'id': real_order.id,
                'card_id': order.card_id,
                'use_money': '%.2f' % order.money,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'onwer_id': order.owner_id
            }]
        else:
            order2card_id[order.order_id].append({
                'card_id': order.card_id,
                'use_money': '%.2f' % order.money,
            })
    order2card_id = sorted(order2card_id.items(), lambda x, y: cmp(x[1][0]['created_at'], y[1][0]['created_at']),reverse=True)
    if cur_page:
        pageinfo, order2card_id = paginator.paginate(order2card_id, cur_page, count_per_page, query_string)


    order_ids = []
    card_ids = set()
    for card in order2card_id:
        cards = card[1]
        for c in cards:
            card_ids.add(c['card_id'])
        order_ids.append(card[0])
    order_id2webapp_user_id = {}
    webapp_user_ids = []
    for order in Order.objects.filter(order_id__in=order_ids):
        order_id2webapp_user_id[order.order_id]= order.webapp_user_id
        webapp_user_ids.append(order.webapp_user_id)
        # order2card_id[order.order_id].

    weizoom_cards = {}
    for card in WeizoomCard.objects.filter(id__in=list(card_ids)):
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
        weizoom_cards[card.id] = {
            'weizoom_card_id': card.weizoom_card_id,
            'weizoom_card_rule_id': card.weizoom_card_rule_id,
            'status': status_str,
        }
    rule_ids = list(set(card['weizoom_card_rule_id'] for card in weizoom_cards.values()))

    rules = {}
    for rule in WeizoomCardRule.objects.filter(id__in=rule_ids):
        rules[rule.id] = {
            'rule_name': rule.name,
            'rule_money': '%.2f' % rule.money
        }
    for card_id in weizoom_cards.keys():
        for rule_id  in rules.keys():
            if weizoom_cards[card_id]['weizoom_card_rule_id'] == rule_id:
                weizoom_cards[card_id].update(rules[rule_id])
    all_webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)
    for order in order2card_id:
        card_orders = order[1]
        buyer_name = u''
        webapp_user_id = order_id2webapp_user_id[order[0]]
        member = all_webappuser2member[webapp_user_id]
        if member:
            buyer_name = member.username_for_html
        else:
            buyer_name = u'未知'
        card_orders[0].update({'buyer_name': buyer_name})
        for card_order in  card_orders:
            card_id = card_order['card_id']
            card_order.update(weizoom_cards[card_id])
    if cur_page:
        return order2card_id,pageinfo
    else:
        return order2card_id