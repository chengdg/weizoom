# -*- coding: utf-8 -*-
from collections import OrderedDict
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
    weizoomcardpermission=WeiZoomCardPermission.objects.filter(user_id=request.user.id)
    count_per_page = int(request.GET.get('count_per_page', '1'))
    cur_page = int(request.GET.get('page', '1'))
    sort_attr = request.GET.get('sort_attr', '-use_money')
    filter_value = request.GET.get('filter_value', None)
    query_string=request.META['QUERY_STRING']
    channel,owner2channel,pageinfo = get_channel_cards(sort_attr,filter_value,cur_page,count_per_page,query_string)
    response = create_response(200)
    response.data.items = channel
    response.data.owner2channel = owner2channel
    response.data.sortAttr = request.GET.get('sort_attr', '-use_money')
    response.data.pageinfo = paginator.to_dict(pageinfo)
    response.data.can_view_statistical_details = weizoomcardpermission[0].can_view_statistical_details
    response.data.can_export_statistical_details = weizoomcardpermission[0].can_export_statistical_details    
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
    channel_orders,pageinfo,cur_event_type = get_channel_details(filter_value,owner_id,start_date,end_date,cur_page,count_per_page,query_string)
    response = create_response(200)
    response.data.items = channel_orders
    response.data.event_type = cur_event_type
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
    orders_relation2card = WeizoomCardHasOrder.objects.exclude(order_id__in=['-1','-2'])
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
                orders = Order.objects.filter(created_at__gte=start_date, created_at__lte=end_date)
                order_ids = []
                for order in orders:
                    order_ids.append(order.order_id)
                orders_relation2card = orders_relation2card.filter(order_id__in=order_ids)
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
            for order in orders_relation2card.filter(event_type="使用"):
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
            return result, [], pageinfo

    total_days, low_date, cur_date, height_date = dateutil.get_date_range(dateutil.get_today(), "6", 0)
    if not filter_value:
        start_date = str(low_date) + ' 00:00:00'
        end_date = str(height_date) + ' 23:59:59'
        orders = Order.objects.filter(created_at__gte=start_date, created_at__lte=end_date)
        order_ids = []
        for order in orders:
            order_ids.append(order.order_id)
        orders_relation2card = orders_relation2card.filter(order_id__in=order_ids)
        users = User.objects.filter(id__in=list(order.owner_id for order in orders_relation2card))

    # user2orders = {}
    user2card = {}
    users_id2username = {user.id: user.username for user in users}
    for order_relation2card in orders_relation2card:
        order = order_relation2card
        user_id = order.owner_id
        try:
            username = users_id2username[user_id]
        except:
            continue
        if not user2card.has_key(user_id):
            # user2orders[user_id] =[order_relation2card]
            if order.event_type == "使用":
                user2card[user_id]={
                    'first_name': username,
                    'card_ids': set([order.card_id]),
                    'order_ids': set([order.order_id]),
                    'use_money': order.money,
                    'refund': 0
                }
            else:
                user2card[user_id]={
                    'first_name': username,
                    'card_ids': set([order.card_id]),
                    'order_ids': set([order.order_id]),
                    'use_money': 0,
                    'refund': order.money
                }
        else:
            # user2orders[user_id].append(order_relation2card)
            if order.event_type == "使用":
                user2card_dict = user2card[user_id]
                user2card_dict['card_ids'].add(order.card_id)
                user2card_dict['order_ids'].add(order.order_id)
                user2card_dict['use_money'] += order.money
            else:
                user2card_dict = user2card[user_id]
                user2card_dict['card_ids'].add(order.card_id)
                user2card_dict['order_ids'].add(order.order_id)
                user2card_dict['refund'] += order.money
    user2card = sorted(user2card.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])),reverse=True)

    owner2channel = OrderedDict()
    # owner2channel['sort_attr'] = sort_attr
    for order in user2card:
    # for user_id,orders in user2card.items():
        user_id = order[0]
        orders = order[1]
        owner2channel[user_id] = {
            'first_name': orders['first_name'],
            'order_ids': list(orders['order_ids']),
            'card_ids': list(orders['card_ids']),
            'use_money': '%.2f' % float(orders['use_money']),
            'refund': '%.2f' % float(-orders['refund']),
            'order_count': len(orders['order_ids']),
            'use_count': len(orders['card_ids']),
            'sort_attr': sort_attr
            }
    user2card = sort_channel(sort_attr,owner2channel)




    if cur_page:
        pageinfo, user2card = paginator.paginate(user2card, cur_page, count_per_page, query_string)
    print user2card,"user2card"
    channel = OrderedDict()
    for card in user2card:
        channel_card = card[1]
        channel[card[0]] ={
            'owner_id': card[0],
            'first_name': channel_card['first_name'],
            'use_money': '%.2f' % float(channel_card['use_money']),
            'refund': '%.2f' % float(channel_card['refund']),
            'order_ids': list(channel_card['order_ids']),
            'order_count': len(channel_card['order_ids']),
            'use_count': len(channel_card['card_ids']),
            'start_date': start_date,
            'end_date': end_date
        }
    print channel,"channel"
    channel = sort_channel(sort_attr,channel)
    # if sort_attr == "-use_money":
    #     #channel按消费金额倒序
    #     channel = sorted(channel.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])),reverse=True)
    #
    # elif sort_attr == "use_money":
    #     #channel按消费金额正序
    #     channel = sorted(channel.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])))
    #
    # elif sort_attr == "-order_count":
    #     #channel按订单数倒序
    #     channel = sorted(channel.items(), lambda x, y: cmp(x[1]['order_count'], y[1]['order_count']),reverse=True)
    # elif sort_attr == "order_count":
    #     #channel按订单数正序
    #     channel = sorted(channel.items(), lambda x, y: cmp(x[1]['order_count'], y[1]['order_count']))
    #
    # elif sort_attr == "-use_count":
    #     #channel按使用人数倒序
    #     channel = sorted(channel.items(), lambda x, y: cmp(x[1]['use_count'], y[1]['use_count']),reverse=True)
    # else:
    #     #channel按使用人数正序
    #     channel = sorted(channel.items(), lambda x, y: cmp(x[1]['use_count'], y[1]['use_count']))

    if cur_page:
        return channel,owner2channel,pageinfo
    else:
        return channel


def get_channel_details(filter_value,owner_id=None,start_date="",end_date="",cur_page=None,count_per_page=None,query_string=""):
    if not start_date and owner_id:
        total_days, start_date, cur_date, end_date = dateutil.get_date_range(dateutil.get_today(), "6", 0)
        start_date = str(start_date) + ' 00:00:00'
        end_date = str(end_date) + ' 23:59:59'
    webapp = WebApp.objects.all()
    if owner_id:
        webapp = webapp.filter(owner_id=owner_id)
    webapp_appids = []
    for w in webapp:
        webapp_appids.append(w.appid)
    orders = Order.by_webapp_id(webapp_appids).order_by('-created_at')
    if owner_id:
        orders = orders.filter(created_at__gte=start_date, created_at__lte=end_date)
    id2order_ids = {}
    for r in orders:
       id2order_ids[r.order_id] = r.id
    order_ids = id2order_ids.keys()
    card_orders = WeizoomCardHasOrder.objects.filter(order_id__in=order_ids).order_by('-created_at')

    #处理过滤
    cur_event_type = '0'
    filter_data_args = {}
    filter_card_rule_ids = []
    if filter_value:
        filter_data_dict = {}
        for filter_data_item in filter_value.split('|'):
            try:
                key, value = filter_data_item.split(":")
            except:
                key = filter_data_item[:filter_data_item.find(':')]
                value = filter_data_item[filter_data_item.find(':')+1:]

            filter_data_dict[key] = value
        created_at = filter_data_dict['created_at']
        if created_at.find('--') > -1:
            val1,val2 = created_at.split('--')
            val1 = val1 +' 00:00:00'
            val2 = val2 +' 23:59:59'
            if owner_id:
                if val1 < start_date:
                    val1 = start_date
                if val2 > end_date:
                    val2 = end_date
            orders = Order.by_webapp_id(webapp_appids).filter(created_at__gte=val1, created_at__lte=val2).order_by('-created_at')
            order_ids = []
            for r in orders:
                order_ids.append(r.order_id)
            card_orders = card_orders.filter(order_id__in=order_ids)
        for key,value in filter_data_dict.items():

            #卡号
            if key == 'card_id':
                card_ids = list(card.id for card in WeizoomCard.objects.filter(weizoom_card_id__contains=value))
                if card_ids:
                    card_orders = card_orders.filter(card_id__in=card_ids)
            #卡名称
            if key == 'name':
                rules = WeizoomCardRule.objects.filter(name__contains=value)
                if rules:
                    for rule in rules:
                        filter_card_rule_ids.append(rule.id)
                    card_ids = list(weizoom_card.id for weizoom_card in WeizoomCard.objects.filter(weizoom_card_rule_id__in=filter_card_rule_ids))
                    if not filter_data_args.has_key('card_id__in'):
                        # filter_data_args['card_id__in'] = card_ids
                        card_orders = card_orders.filter(card_id__in=card_ids)
                    else:
                        old_card_ids = filter_data_args['card_id__in']
                        new_card_ids = list(set(old_card_ids).intersection(set(card_ids)))
                        # filter_data_args['card_id__in'] = new_card_ids
                        card_orders = card_orders.filter(card_id__in=new_card_ids)
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
                    order_ids = list(order.order_id for order in orders.filter(webapp_user_id__in=member_webappuser_ids))
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
                val1,val2 = value.split('--')
                low_money = float(val1)
                high_money = float(val2)
                card2money= {}
                orderids = []
                cur_orders = WeizoomCardHasOrder.objects.filter(order_id__in=order_ids)
                if cur_orders:
                    for order in cur_orders:
                        if not card2money.has_key(order.order_id):
                            if order.event_type == "使用":
                                card2money[order.order_id] = {
                                    'use_money': order.money,
                                    'refund': 0,
                                }
                            else:
                                card2money[order.order_id] = {
                                    'refund': order.money,
                                    'use_money': 0
                                }
                        else:
                            if order.event_type == "使用":
                                card2money[order.order_id]['use_money'] += order.money
                            else:
                                card2money[order.order_id]['refund'] += order.money
                if card2money:
                    for key,value in card2money.items():
                        for k,v in value.items():
                            print v
                            if v >= low_money and v <= high_money and v != 0:
                                orderids.append(key)
                    if orderids:
                        if not filter_data_args.has_key('order_id__in'):
                            card_orders = card_orders.filter(order_id__in=orderids)
                        else:
                            old_card_ids = filter_data_args['order_id__in']
                            new_card_ids = list(set(old_card_ids).intersection(set(orderids)))
                            filter_data_args['order_id__in'] = new_card_ids
                    else:
                        filter_data_args['order_id'] = -1
            if key == 'event_type':
                cur_event_type = value
                if value == '1':
                    orders = orders.filter(status=ORDER_STATUS_CANCEL)
                    order_ids = []
                    for r in orders:
                        order_ids.append(r.order_id)
                    card_orders = card_orders.filter(order_id__in=order_ids,event_type="返还")

                if value == '0':
                    # order_ids = []
                    # for r in orders:
                    #     order_ids.append(r.order_id)
                    card_orders = card_orders.filter(order_id__in=order_ids,event_type="使用")
        card_orders = card_orders.filter(**filter_data_args).exclude(order_id=-1).order_by('-created_at')
        print filter_data_args
        print card_orders,"print card_orders"
    else:
        card_orders = card_orders.filter(event_type="使用")
    # order2card_id = OrderedDict()
    order2card_id = []
    inner_dict = OrderedDict()
    user_id2username = {u.id: u.username for u in User.objects.all()}
    for card_order in card_orders.order_by('-created_at'):
        inner_order_id = card_order.order_id
        if not inner_dict.has_key(card_order.order_id):
            if card_order.event_type == "使用":
                inner_dict[card_order.order_id] = [{
                    'order_id': card_order.order_id,
                    'id': id2order_ids[card_order.order_id],
                    'card_id': card_order.card_id,
                    'use_money': '%.2f' % card_order.money,
                    'created_at': card_order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'onwer_id': card_order.owner_id,
                    'owner_username': user_id2username[card_order.owner_id],
                    'event_type': card_order.event_type
                }]
            else:
                inner_dict[card_order.order_id] = [{
                    'order_id': card_order.order_id,
                    'id': id2order_ids[card_order.order_id],
                    'card_id': card_order.card_id,
                    'refund': '%.2f' % -card_order.money,
                    'created_at': card_order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'onwer_id': card_order.owner_id,
                    'owner_username': user_id2username[card_order.owner_id],
                    'event_type': card_order.event_type
                }]
        else:
            if card_order.event_type == "使用":
                inner_dict[card_order.order_id].append({
                    'card_id': card_order.card_id,
                    'use_money': '%.2f' % card_order.money,
                })
            else:
                inner_dict[card_order.order_id].append({
                    'card_id': card_order.card_id,
                    'refund': '%.2f' % -card_order.money,
                })
    temp_list = []
    for k, v in inner_dict.items():
       temp_list.append({k:v})
    order2card_id.append(inner_dict)

    # order2card_id = sorted(order2card_id.items(), lambda x, y: cmp(x[1][0]['created_at'], y[1][0]['created_at']),reverse=True)order2card_id = sorted(order2card_id.items(), lambda x, y: cmp(x[1][0]['created_at'], y[1][0]['created_at']),reverse=True)
    if cur_page:
        pageinfo, temp_list = paginator.paginate(temp_list, cur_page, count_per_page, query_string)
        key_list = []
        for one_dict in temp_list:
            key_list.append(one_dict.keys()[0])

        needed_keys = list(set(inner_dict.keys()) ^ (set(key_list)))
        for k in needed_keys:
            del inner_dict[k]

    order_ids = set()
    card_ids = set()
    for inner_dict in order2card_id:
        # cards = card[1]
        for order_id,v in inner_dict.items():
            for card in v:
                card_ids.add(card['card_id'])
            order_ids.add(order_id)
    order_id2webapp_user_id = {}
    webapp_user_ids = []
    for order in Order.objects.filter(order_id__in=order_ids):
        order_id2webapp_user_id[order.order_id]= order.webapp_user_id
        webapp_user_ids.append(order.webapp_user_id)

    owner_ids = [user.id for user in User.objects.filter(username__in=['weshop','wzjx001'])]
    webapp_ids = [webapp.appid for webapp in WebApp.objects.filter(owner_id__in=owner_ids)]
    ids = []
    order_id2orderid = {}
    for order in Order.by_webapp_id(webapp_ids).filter(order_id__in=order_ids):
        ids.append(order.id)
        order_id2orderid[order.id] = order.order_id
    order_order_id2Product_ids = {}
    product_ids = set()
    for p in OrderHasProduct.objects.filter(order_id__in=ids):
        if not order_order_id2Product_ids.has_key(p.product_id):
            order_order_id2Product_ids[order_id2orderid[p.order_id]] = [p.product_id]
        else:
            order_order_id2Product_ids[order_id2orderid[p.order_id]].append(p.product_id)
        product_ids.add(p.product_id)
    product_id2category_name = {}
    catetory_id2name = {c.id: c.name for c in ProductCategory.objects.all()}
    for p in CategoryHasProduct.objects.filter(product_id__in=product_ids):
        if not product_id2category_name.has_key(p.product_id):
            product_id2category_name[p.product_id] = [catetory_id2name[p.category_id]]
        else:
            product_id2category_name[p.product_id].append(catetory_id2name[p.category_id])

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
    for inner_dict in order2card_id:
        for k,orders in inner_dict.items():

            # card_orders = order[1]
            # order_id = order[0]
            order_id = k
            product_dict = orders[0]['product'] = {}
            if order_order_id2Product_ids.has_key(order_id):
                product_ids = order_order_id2Product_ids[order_id]
                for one_id in product_ids:
                    try:
                        product_dict[one_id] = ','.join(product_id2category_name[one_id])
                    except:
                        product_dict[one_id] = ''

            webapp_user_id = order_id2webapp_user_id[order_id]
            member = all_webappuser2member[webapp_user_id]
            if member:
                buyer_name = member.username_for_html
            else:
                buyer_name = u'未知'
            orders[0].update({'buyer_name': buyer_name})
            for card_order in  orders:
                card_id = card_order['card_id']
                card_order.update(weizoom_cards[card_id])
    print order2card_id
    if cur_page:
        return order2card_id,pageinfo,cur_event_type
    else:
        return order2card_id

def sort_channel(sort_attr,user2card):
    if sort_attr == "-use_money":
        #channel按消费金额倒序
        user2card = sorted(user2card.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])),reverse=True)

    elif sort_attr == "use_money":
        #channel按消费金额正序
        user2card = sorted(user2card.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])))

    elif sort_attr == "-order_count":
        #channel按订单数倒序
        user2card = sorted(user2card.items(), lambda x, y: cmp(int(x[1]['order_count']), int(y[1]['order_count'])),reverse=True)
    elif sort_attr == "order_count":
        #channel按订单数正序
        user2card = sorted(user2card.items(), lambda x, y: cmp(int(x[1]['order_count']), int(y[1]['order_count'])))

    elif sort_attr == "-use_count":
        #channel按使用人数倒序
        user2card = sorted(user2card.items(), lambda x, y: cmp(int(x[1]['use_count']), int(y[1]['use_count'])),reverse=True)
    else:
        #channel按使用人数正序
        user2card = sorted(user2card.items(), lambda x, y: cmp(int(x[1]['use_count']), int(y[1]['use_count'])))
    return  user2card