#! -*- coding:UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime, timedelta
import time

from core.restful_url_route import *
from core.jsonresponse import *
from core import paginator

from market_tools.tools.weizoom_card.models import *
from card import export
from mall.models import Order
from card_datetime import *

@view(app='card', resource='overview', action='get')
@login_required
def get_overview_data(request):
    c = RequestContext(request, {
        'first_nav_name': export.MALL_CARD_FIRST_NAV,
        'second_navs': export.get_card_second_navs(request),
        'second_nav_name': export.MALL_CARD_CENSUS_NAV,
        'third_nav_name': export.MALL_CARD_TOTAL_CENSUS_NAV,

    })
    return render_to_response('card/editor/overview.html', c)


@api(app='card',resource='overview',action='get')
@login_required
def get_overview(request):

    date_str = request.GET.get('date_interval', '')

    #过滤日期
    if date_str:
        date_interval = get_datetime_from_date_interval(date_str)
    else:
        date_interval= get_previous_date_range_list('today',7)

    #rules
    weizoom_card_rules = WeizoomCardRule.objects.filter(created_at__gte=date_interval[0],created_at__lte=date_interval[1]).order_by('-created_at')
    rules=[rule for rule in weizoom_card_rules]

    #cards
    rule_ids=[r.id for r in weizoom_card_rules]
    cards=WeizoomCard.objects.filter(weizoom_card_rule_id__in=rule_ids)
    rule_id2cards={}

    for card in cards:
        cur_rule_id = card.weizoom_card_rule_id
        if cur_rule_id not in rule_id2cards:
            rule_id2cards[cur_rule_id]=[card]
        else:
            rule_id2cards[cur_rule_id].append(card)

    card_ids=[c.id for c in cards]
    order_relations=WeizoomCardHasOrder.objects.filter(card_id__in=card_ids)
    card_id2order_relations={}
    for relation in order_relations:
        if relation.card_id not in card_id2order_relations:
            card_id2order_relations[relation.card_id]=[relation]
        else:
            card_id2order_relations[relation.card_id].append(relation)

    #符合过滤条件的渠道
    user_ids=set([rule.owner_id for rule in rules])

    #用来传走的数据表
    cur_weizoom_card_rules=[] #这是overvie details表中

    #多个数据表在一个循环中，添加到不同的数据表中，减少数据库访问次数
    overinfo_list=[]
    card_order_ids = set()
    for rule in rules:
        cur_weizoom_card_rule={}

        overinfo_item={}
        total_money_num=rule.money*rule.count#总金额 num
        cur_weizoom_card_rule['id'] = rule.id#卡id
        cur_weizoom_card_rule['name'] = rule.name#卡名称
        cur_weizoom_card_rule['count_num']=rule.count#一种卡发行总张数
        cur_weizoom_card_rule['count'] = str(rule.count)#卡总张数str
        cur_weizoom_card_rule['money']=str(rule.money)#卡面值str
        cur_weizoom_card_rule['total_money']= str(total_money_num)#总金额 str
        cur_weizoom_card_rule['card_type'] = rule.card_type#卡类型
        
        overinfo_item['id']=rule.id
        overinfo_item['name']=rule.name
        overinfo_item['count']=rule.count
        overinfo_item['money']=rule.money
        overinfo_item['total_money']=total_money_num
        overinfo_item['card_type']=rule.card_type

        rule_cards = rule_id2cards[rule.id]#weizoom card数据库

        used_cards_count = 0
        active_cards_count = 0
        expired_cards_count = 0
        inactive_cards_count = 0
        for card in rule_cards:
            if card.status in [WEIZOOM_CARD_STATUS_USED, WEIZOOM_CARD_STATUS_EMPTY]:
                used_cards_count += 1
            if card.status in [WEIZOOM_CARD_STATUS_UNUSED, WEIZOOM_CARD_STATUS_USED, WEIZOOM_CARD_STATUS_EMPTY]:
                active_cards_count += 1
            if card.is_expired:
                expired_cards_count += 1
            if card.status == WEIZOOM_CARD_STATUS_INACTIVE:
                inactive_cards_count += 1

        cur_weizoom_card_rule['use_num'] = str(used_cards_count)#使用张数str
        overinfo_item['use_num']=used_cards_count
        overinfo_item['active_num']=active_cards_count
        overinfo_item['expired_num']=expired_cards_count
        overinfo_item['inactive_num']=inactive_cards_count

        balance_total_num=sum([card.money for card in rule_cards])#总余额
        cur_weizoom_card_rule['balance_total']=str(balance_total_num)#总余额str
        overinfo_item['balance_total']=balance_total_num

        consum_total_num=total_money_num-balance_total_num#总金额-总余额=消费金额
        cur_weizoom_card_rule['consum_total'] = str(consum_total_num)#消费金额str
        overinfo_item['consum_total']=consum_total_num

        #符合过滤条件的weizoom_card_orders
        order_li=set()
        cards_tmp=rule_id2cards[rule.id]
        for card in cards_tmp:
            try:
                relation_tmp=card_id2order_relations[card.id]
            except:
                relation_tmp=[]
            for relation in relation_tmp:
                order_id=str(relation.order_id)
                if order_id != '-1':
                    order_li.add(order_id)
                    card_order_ids.add(order_id)

        wcards_orders_num = len(order_li)
        cur_weizoom_card_rule['orders_num'] = str(wcards_orders_num)
        overinfo_item['orders_num'] = wcards_orders_num

        try:
            use_rate_num= float(used_cards_count)/float(rule.count)*100#使用率*100是百分数
        except ZeroDivisionError:
            use_rate_num=0
        cur_weizoom_card_rule['use_rate']= '%.1f %%'%use_rate_num #使用率str
        overinfo_item['use_rate']=use_rate_num

        cur_weizoom_card_rules.append(cur_weizoom_card_rule)#添加进入数组
        overinfo_list.append(overinfo_item)#加入列表，保存数据用来统计

    #按照消费金额排序
    cur_weizoom_card_rules=sorted(cur_weizoom_card_rules,key= lambda card:float(card['consum_total']),reverse=True)

    #overview info table 展示的统计信息
    overinfo_rules_num=0                #1卡规则数量
    overinfo_cards_total_num=0          #2发行总量：新建所有卡 总数
    overinfo_cards_total_money_num=0    #3总金额
    overinfo_cards_average_money_num=0  #4卡均面值：总金额/发行总数
    overinfo_cards_total_active_num=0   #5激活总数：所选时间段内激活总数
    overinfo_cards_total_expired_num=0  #6过期总数：
    overinfo_cards_total_inactive_num=0 #7停用总数
    overinfo_cards_total_use_num_value=0#8使用张数
    overinfo_cards_total_consum_num=0   #9总消费
    overinfo_cards_average_consum_num=0 #10卡均消费金额:总消费金额/发行总数
    overinfo_cards_total_orders_num=len(card_order_ids)   #11订单数
    for item in overinfo_list:
        overinfo_rules_num += 1
        overinfo_cards_total_num += item['count']
        overinfo_cards_total_money_num += item['total_money']
        overinfo_cards_total_active_num += item['active_num']
        overinfo_cards_total_expired_num += item['expired_num']
        overinfo_cards_total_inactive_num += item['inactive_num']
        overinfo_cards_total_use_num_value += item['use_num']
        overinfo_cards_total_consum_num += item['consum_total']

    overinfo_rules_num_str = str(overinfo_rules_num)#最新制卡str
    overinfo_cards_total = str(overinfo_cards_total_num)#发行总数
    overinfo_cards_total_money = '%.2f'%overinfo_cards_total_money_num#总金额

    #4卡均面值：总金额/发行总数
    try:
        overinfo_cards_average_money_num = float(overinfo_cards_total_money_num/overinfo_cards_total_num)
        overinfo_cards_average_money = '%.2f'%overinfo_cards_average_money_num
    except ZeroDivisionError:
        overinfo_cards_average_money_num = 0
        overinfo_cards_average_money = '0.00'

    #5激活总数：所选时间段内激活总数
    overinfo_cards_total_active = str(overinfo_cards_total_active_num)

    #6过期总数：
    overinfo_cards_total_expired = str(overinfo_cards_total_expired_num)

    #7停用总数
    overinfo_cards_total_inactive = str(overinfo_cards_total_inactive_num)

    #8使用张数
    overinfo_cards_total_use_num = str(overinfo_cards_total_use_num_value)

    #9总消费
    overinfo_cards_total_consum = '%.2f'%overinfo_cards_total_consum_num

    #10卡均消费金额:总消费金额/发行总数
    try:
        overinfo_cards_average_consum_num = float(overinfo_cards_total_consum_num)/float(overinfo_cards_total_num)
        overinfo_cards_average_consum = '%.2f'%overinfo_cards_average_consum_num
    except ZeroDivisionError:
        overinfo_cards_average_consum_num = 0
        overinfo_cards_average_consum = '0.00'

    #11订单数
    overinfo_cards_total_orders = str(overinfo_cards_total_orders_num)

    #12平均使用率:使用总张数/发行总数：这里方法是：使用率相加除以加数的个数
    try:
        overinfo_average_use_rate_num = float(overinfo_cards_total_use_num_value)/float(overinfo_cards_total_num)*100
        overinfo_average_use_rate = '%.1f'%overinfo_average_use_rate_num
    except ZeroDivisionError:
        overinfo_average_use_rate_num = 0
        overinfo_average_use_rate = '0.0'

    count_per_page = int(request.GET.get('count_per_page', '20'))
    cur_page = int(request.GET.get('page', '1'))
    pageinfo, weizoom_card_rules = paginator.paginate(cur_weizoom_card_rules, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

    overview_info_dict={
        'overinfo_new_cards':overinfo_rules_num_str,                        #1最新制卡数量：所选时间段内，最新卡 种类
        'overinfo_cards_total':overinfo_cards_total,                        #2发行总量：新建所有卡 总数
        'overinfo_cards_total_money':'￥'+overinfo_cards_total_money,       #3总金额：所选卡 面值x数量 相加 sum
        'overinfo_cards_average_money':'￥'+overinfo_cards_average_money,   #4卡均面值：总金额/发行总数
        'overinfo_cards_total_active':overinfo_cards_total_active,          #5激活总数：所选时间段内激活总数
        'overinfo_cards_total_expired':overinfo_cards_total_expired,        #6过期总数：
        'overinfo_cards_total_inactive':overinfo_cards_total_inactive,      #7停用总数
        'overinfo_cards_total_use_num':overinfo_cards_total_use_num,        #8使用张数
        'overinfo_cards_total_consum':'￥'+overinfo_cards_total_consum,     #9总消费
        'overinfo_cards_average_consum':'￥'+overinfo_cards_average_consum, #10卡均消费金额:总消费金额/发行总数
        'overinfo_cards_total_orders':overinfo_cards_total_orders,          #11订单数
        'overinfo_average_use_rate':overinfo_average_use_rate+' %',         #12平均使用率:使用总张数/发行总数：这里方法是：使用率相加除以加数的个数
    }

    #微众卡TOP10
    wcards_use_list=[{'name':card['name'],'use_num':card['use_num']} for card in overinfo_list]
    #排序
    wcards_use_list_sorted_raw=sorted(wcards_use_list,key= lambda card:float(card['use_num']),reverse=True)
    wcards_use_list_sorted=[]
    if wcards_use_list_sorted_raw:
        for item in wcards_use_list_sorted_raw:
            if not item['use_num']==float(0):
                wcards_use_list_sorted.append(item)

    if len(wcards_use_list_sorted)==0:
        for i in range(10):
            wcards_use_list_sorted.append({'name':' ','use_num':' '})
        wcards_use_top10=wcards_use_list_sorted
    elif len(wcards_use_list_sorted)>10:
        wcards_use_top10=wcards_use_list_sorted[:10]
    else:
        wcards_use_top10=wcards_use_list_sorted

    #卡消费TOP10
    wcards_consum_list=[]
    for rule in rules:
        for card in rule_id2cards[rule.id]:
            wcards_dic={}
            wcards_dic['weizoom_card_id']=card.weizoom_card_id
            wcards_dic['consum_money']=float(rule.money)-float(card.money)
            wcards_consum_list.append(wcards_dic)
    #排序
    wcards_consum_list_sorted_raw =sorted(wcards_consum_list,key= lambda card:float(card['consum_money']),reverse=True)
    wcards_consum_list_sorted=[]
    if wcards_consum_list_sorted_raw:
        for item in wcards_consum_list_sorted_raw:
            if not item['consum_money']==float(0):
                wcards_consum_list_sorted.append(item)
    if len(wcards_consum_list_sorted)==0:
        for i in range(10):
            wcards_consum_list_sorted.append({'weizoom_card_id':' ','consum_money':' '})
        wcards_consum_top10=wcards_consum_list_sorted
    elif len(wcards_consum_list_sorted)>10:
        wcards_consum_top10=wcards_consum_list_sorted[:10]
    else:
        wcards_consum_top10=wcards_consum_list_sorted

    #卡类型统计
    #ex card
    card_ex_num=count_card_type(rules,rule_id2cards,0,[1,2])
    #in card
    card_in_num=count_card_type(rules,rule_id2cards,1,[1,2])
    #gift card
    card_gift_num=count_card_type(rules,rule_id2cards,2,[1,2])

    card_type_static=[
        {'name':'外部卡','value':card_ex_num},
        {'name':'内部卡','value':card_in_num},
        {'name':'赠品卡','value':card_gift_num}
    ]

    #卡渠道统计
    #符合过滤条件的渠道card_id2order_relations

    user_dic_list =[{'name':user.username,'id':user.id} for user in User.objects.filter(id__in=user_ids)]

    cards2money={}
    for card_id in card_id2order_relations:
        for relation in card_id2order_relations[card_id]:
            if card_id not in cards2money:
                cards2money[card_id]=relation.money
            else:
                cards2money[card_id]+=relation.money

    rules2money={}
    for rule_id in rule_id2cards:
        for card in rule_id2cards[rule_id]:
            try:
                money = cards2money[card.id]
            except:
                money = 0
            if rule_id not in rules2money:
                rules2money[rule_id]=money
            else:
                rules2money[rule_id]+=money

    user2money={}
    for rule in rules:
        try:
            money = rules2money[rule.id]
        except:
            money = 0
        if rule.owner_id not in user2money:
            user2money[rule.owner_id]=money
        else:
            user2money[rule.owner_id]+=money

    user_consum=[]
    for user in user_dic_list:
        user_consum_dic={}
        user_consum_dic['name']=user['name']
        user_consum_dic['value']=float(user2money[user['id']])
        user_consum.append(user_consum_dic)

    #如果大于11个。取11个，如果小于11个如实统计
    if len(user_consum)>=11:
        user_consum=user_consum[:11]


    #准备传输的数据
    data={'overview_info_dict':overview_info_dict,#统计面板
          'wcards_use_top10':wcards_use_top10,#微众卡top10
          'wcards_consum_top10':wcards_consum_top10,#消费top10
          'card_type_static':card_type_static,#卡类型统计
          'user_consum':user_consum#渠道统计
          }

    response = create_response(200)
    response.data.items = weizoom_card_rules
    response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
    response.data.pageinfo = paginator.to_dict(pageinfo)
    response.data.data=data

    return response.get_response()

#数卡片类型
def count_card_type(rules,rule_id2cards,type,card_status_list):
    card_list=[]
    for rule in rules:
        if rule.card_type==type:
            for card in rule_id2cards[rule.id]:
                if card.status in card_status_list:
                    card_list.append(card)
    return len(card_list)
