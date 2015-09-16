# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import re
from card import export
from core.restful_url_route import view
from core.restful_url_route import api

from market_tools.tools.weizoom_card.models import *
from modules.member.models import Member
from excel_response import ExcelResponse
from mall.models import *
from core import dateutil
from cards_channel_api_views import get_channel_cards
from cards_channel_api_views import get_channel_details
from termite.core.jsonresponse import create_response


@view(app='card', resource='cards_channel_census', action='get')
@login_required
def get_chan_channel_census(request):
    """
    微众卡列表页面
    """
    total_days, start_date, cur_date, end_date = dateutil.get_date_range(dateutil.get_today(), "6", 0)
    start_date = str(start_date)
    end_date = str(end_date)
    has_cards = (WeizoomCard.objects.filter().count() > 0)
    c = RequestContext(request, {
        'first_nav_name': export.MALL_CARD_FIRST_NAV,
        'second_navs': export.get_card_second_navs(request),
        'second_nav_name': export.MALL_CARD_CENSUS_NAV,
        'third_nav_name': export.MALL_CARD_BY_CHANNEL_NAV,
        'has_cards': has_cards,
        'start_date': start_date,
        'end_date': end_date

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
    webapp = WebApp.objects.get(owner_id=owner_id)
    orders = Order.by_webapp_id(webapp.appid).filter(created_at__gte=start_date, created_at__lte=end_date).order_by('-created_at')
    id2order_ids = {}
    for r in orders:
       id2order_ids[r.order_id] = r.id
    order_ids = id2order_ids.keys()
    card_orders = WeizoomCardHasOrder.objects.filter(order_id__in=order_ids).order_by('-created_at')
    # orders = WeizoomCardHasOrder.objects.filter(owner_id=owner_id,created_at__gte=start_date,created_at__lte=end_date).exclude(order_id=-1)
    use_money = 0
    refund = 0
    card_ids = set()
    order_ids = set()
    for order in card_orders:
        if order.event_type == "使用":
            use_money += order.money
        else:
            refund += order.money
        card_ids.add(order.card_id)
        order_ids.add(order.order_id)
    channel.use_money = '%.2f' % use_money
    channel.refund = '%.2f' % -refund
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


@api(app='card', resource='channel', action='export')
@login_required
def export_channel(request):
    channels = request.POST.get('channels','')
    print channels
    channels = json.loads(channels)
    sort_attr = channels.values()[0]['sort_attr']
    if sort_attr == "-use_money":
        #channel按消费金额倒序
        channels = sorted(channels.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])),reverse=True)

    elif sort_attr == "use_money":
        #channel按消费金额正序
        channels = sorted(channels.items(), lambda x, y: cmp(float(x[1]['use_money']), float(y[1]['use_money'])))

    elif sort_attr == "-order_count":
        #channel按订单数倒序
        channels = sorted(channels.items(), lambda x, y: cmp(int(x[1]['order_count']), int(y[1]['order_count'])),reverse=True)
    elif sort_attr == "order_count":
        #channel按订单数正序
        channels = sorted(channels.items(), lambda x, y: cmp(int(x[1]['order_count']), int(y[1]['order_count'])))

    elif channels == "-use_count":
        #channel按使用人数倒序
        channels = sorted(channels.items(), lambda x, y: cmp(int(x[1]['use_count']), int(y[1]['use_count'])),reverse=True)
    else:
        #channel按使用人数正序
        channels = sorted(channels.items(), lambda x, y: cmp(int(x[1]['use_count']), int(y[1]['use_count'])))

    order_ids = set()
    for orderids in channels:
        for order_id in orderids[1]['order_ids']:
            order_ids.add(order_id)

    order_id2cards = {}
    user_id2username = {u.id: u.username for u in User.objects.all()}
    for order in WeizoomCardHasOrder.objects.filter(order_id__in=list(order_ids)).order_by('-created_at'):
        if not order_id2cards.has_key(order.order_id):
            order_id2cards[order.order_id] = [{
                'order_id': order.order_id,
                'card_id': order.card_id,
                'money': order.money,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'onwer_id': order.owner_id,
                'owner_username': user_id2username[order.owner_id],
                'event_type': order.event_type
            }]
        else:
            order_id2cards[order.order_id].append({
                'order_id': order.order_id,
                'card_id': order.card_id,
                'money': order.money,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'onwer_id': order.owner_id,
                'owner_username': user_id2username[order.owner_id],
                'event_type': order.event_type
            })
    order2cards = {}

    for k,cards in  order_id2cards.items():
        card_money = {}
        for card in cards:
            if not card_money.has_key(card['card_id']):
                if card['event_type'] == '使用':
                    card_money[card['card_id']] = {
                        'card_id':card['card_id'],
                        'order_id' :card['order_id'],
                        'use_money': card['money'],
                        'refund': 0,
                        'created_at': card['created_at'],
                        'owner_username': card['owner_username']
                    }
                else:
                    card_money[card['card_id']] = {
                        'card_id':card['card_id'],
                        'order_id' :card['order_id'],
                        'use_money': 0,
                        'refund': card['money'],
                        'created_at': card['created_at'],
                        'owner_username': card['owner_username']
                    }
            else:
                if card['event_type'] == '使用':
                    card_money[card['card_id']]['use_money'] +=card['money']
                else:
                    card_money[card['card_id']]['refund'] +=card['money']
        order2cards[k] = card_money.values()


    card_ids = set()
    for k,inner_list in order_id2cards.items():
        for order in inner_list:
            card_ids.add(order['card_id'])
    weizoom_cards = {}
    for card in WeizoomCard.objects.filter(id__in=list(card_ids)):
        weizoom_cards[card.id] = {
            'weizoom_card_id': card.weizoom_card_id
        }
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
    channel2orders = OrderedDict()
    for orderids in channels:
        for order_id in orderids[1]['order_ids']:
            if not channel2orders.has_key(orderids[0]):
                channel2orders[orderids[0]] = [order2cards[order_id]]
            else:
                channel2orders[orderids[0]].append(order2cards[order_id])

    members_info = [
        [u'渠道帐号','订单号','消费卡号',u'消费金额',u'退款金额',u'消费日期',u'商品分组']
    ]

    for k,channel2order in channel2orders.items():
        for orders in channel2order:
            for order in orders:
                card_id = order['card_id']
                order.update(weizoom_cards[card_id])
                product_dict = order['product'] = {}
                if order_order_id2Product_ids.has_key(order['order_id']):
                    product_ids = order_order_id2Product_ids[order['order_id']]
                    for one_id in product_ids:
                        try:
                            product_dict[one_id] = ','.join(product_id2category_name[one_id])
                        except:
                            product_dict[one_id] = ''
                info_list=[
                    order['owner_username'],
                    order['order_id'],
                    order['weizoom_card_id'],
                    '%.2f' % order['use_money'],
                    '%.2f' % -order['refund'],
                    order['created_at'],
                    order['product'].values()
                ]
                members_info.append(info_list)
    filename = u'微众卡按渠道统计列表.xls'
    url = export_csv(members_info,filename,force_csv=False)
    response = create_response(200)
    response.data.url = url
    response.data.filename = filename
    return response.get_response()


@api(app='card', resource='channel_detail', action='export')
@login_required
def export_channel_detail(request):
    owner_id = request.POST.get('owner_id',-1)
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    filter_value = request.POST.get('filter_value', None)
    channel_orders = get_channel_details(filter_value,owner_id,start_date,end_date)
    name = u'消费金额'
    for orders in channel_orders:
        for k,order in orders.items():
            evnet_type = order[0]['event_type']
            if evnet_type == "返还":
                name = u'退款金额'
    members_info = [
        [u'消费时间', u'订单号',u'卡名称',u'卡号',u'状态',u'面值',name,u'使用人',u'商品分组']
    ]
    for orders in channel_orders:
        for k,order in orders.items():
            created_at = order[0]['created_at']
            order_id = order[0]['order_id']
            buyer_name = order[0]['buyer_name']
            re_h = re.compile('</?\w+[^>]*>')#HTML标签
            buyer_name =  re_h.sub('',buyer_name) #去掉HTML 标签
            product = '\n'.join(order[0]['product'].values())
            evnet_type = order[0]['event_type']
            name = 'use_money'
            if evnet_type == "返还":
               name = 'refund'
            i=0
            for o in order:
                if i <1:
                    info_list=[
                        created_at,
                        order_id,
                        o['rule_name'],
                        o['weizoom_card_id'],
                        o['status'],
                        o['rule_money'],
                        o[name],
                        buyer_name,
                        product
                    ]
                else:
                    info_list=[
                        "",
                        "",
                        o['rule_name'],
                        o['weizoom_card_id'],
                        o['status'],
                        o['rule_money'],
                        o[name],
                        "",
                        ""
                    ]
                i += 1

                members_info.append(info_list)

    filename = u'微众卡按渠道统计消费列表.xls'#TODO 上线 加.encode('utf8')
    url = export_csv(members_info,filename,force_csv=False)
    response = create_response(200)
    response.data.url = url
    response.data.filename = filename
    return response.get_response()


def export_csv(data,output_name,force_csv,encoding='utf8'):
    output_name = output_name.encode('utf-8')
    import datetime,xlwt,re
    book = xlwt.Workbook(encoding=encoding)
    sheet = book.add_sheet('Sheet 1')
    styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
              'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
              'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
              'number': xlwt.easyxf(num_format_str='0.00'),
              'default': xlwt.Style.default_style}
    regex_str = '^[-+]?[0-9]*\.[0-9]+$'
    for rowx, row in enumerate(data):
        for colx, value in enumerate(row):
            if isinstance(value, datetime.datetime):
                cell_style = styles['datetime']
            elif isinstance(value, datetime.date):
                cell_style = styles['date']
            elif isinstance(value, datetime.time):
                cell_style = styles['time']
            elif isinstance(value,str) and re.match(regex_str,value):
                value = float(value)
                cell_style = styles['number']
            else:
                cell_style = styles['default']
            sheet.write(rowx, colx, value, style=cell_style)
    excel_file_path = os.path.join(settings.UPLOAD_DIR,output_name)
    book.save(excel_file_path)
    return '/static/upload/%s' % output_name
