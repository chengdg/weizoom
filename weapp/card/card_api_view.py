# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from core.restful_url_route import *
from core import paginator
from core.jsonresponse import JsonResponse, create_response

from market_tools.tools.weizoom_card.models import *
import module_api
from datetime import datetime, timedelta
from card_datetime import *
import random

#微众卡类型
WEIZOOM_CARD_EXTERNAL = 0
WEIZOOM_CARD_INTERNAL = 1
WEIZOOM_CARD_GIFT = 2

TYPE2NAME = {
    'WEIZOOM_CARD_EXTERNAL': u'外部卡',
    'WEIZOOM_CARD_INTERNAL': u'内部卡',
    'WEIZOOM_CARD_GIFT': u'赠品卡'
}


@api(app='card', resource='cards', action='get')
@login_required 
def get_cards(request):
    """
    卡规则列表 
    """
    count_per_page = int(request.GET.get('count_per_page', '1'))
    cur_page = int(request.GET.get('page', '1'))
    card_name = request.GET.get('cardName', '').strip()
    weizoom_card_rule_id = int(request.GET.get('weizoom_card_rule_id', '-1'))
    weizoom_card_rules = WeizoomCardRule.objects.all().order_by('-created_at')
    if card_name:
        weizoom_card_rules = weizoom_card_rules.filter(name__icontains = card_name)

    # 时间区间
    date_interval = request.GET.get('date_interval', '')
    if date_interval:
        date_interval = get_datetime_from_date_interval(date_interval)
        weizoom_card_rules = weizoom_card_rules.filter(valid_time_from__gte=date_interval[0],valid_time_to__lte=date_interval[1])
        
    filter_value = request.GET.get('filter_value', '')
    card_type = _get_type_value(filter_value)
    if card_type != -1:
        weizoom_card_rules = weizoom_card_rules.filter(card_type= card_type)
    
    pageinfo, weizoom_card_rules = paginator.paginate(weizoom_card_rules, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])  

    card_rule_ids = [int(r.id) for r in weizoom_card_rules]
    all_cards = WeizoomCard.objects.filter(weizoom_card_rule_id__in=card_rule_ids)
    
    rule_id2card_ids={}
    rule_id2cards = {}

    for c in all_cards:
        card_rule_id = c.weizoom_card_rule_id
        if card_rule_id not in rule_id2cards:
            rule_id2cards[card_rule_id] = [c]
        else:
            rule_id2cards[card_rule_id].append(c)

    for r_id in card_rule_ids:
        weizoom_cards = rule_id2cards[r_id]
        weizoom_card_ids = [int(weizoom_cards[0].weizoom_card_id), int(weizoom_cards[::-1][0].weizoom_card_id)]
        rule_id2card_ids[r_id] = weizoom_card_ids

    cur_weizoom_card_rules = []
    for rule in weizoom_card_rules:
        cur_weizoom_card_rule = JsonResponse()
        cur_weizoom_card_rule.id = rule.id
        cur_weizoom_card_rule.name = rule.name
        cur_weizoom_card_rule.count = rule.count
        cur_weizoom_card_rule.remark = rule.remark
        cur_weizoom_card_rule.money = '%.2f' % rule.money
        cur_weizoom_card_rule.card_type = rule.card_type
        cur_weizoom_card_rule.valid_time_from = datetime.strftime(rule.valid_time_from, '%Y-%m-%d %H:%M')
        cur_weizoom_card_rule.valid_time_to = datetime.strftime(rule.valid_time_to, '%Y-%m-%d %H:%M')
        cur_weizoom_card_rule.created_at = datetime.strftime(rule.created_at, '%Y-%m-%d %H:%M')

        #卡号区间
        try:
            weizoom_card_ids = rule_id2card_ids[cur_weizoom_card_rule.id]
            weizoom_card_id_start = weizoom_card_ids[0]
            weizoom_card_id_end = weizoom_card_ids[1]
            card_num_range = '%07d-%07d'%(weizoom_card_id_start,weizoom_card_id_end)
            cur_weizoom_card_rule.card_range = card_num_range
        except:
            pass

        # 卡类型
        if cur_weizoom_card_rule.card_type == WEIZOOM_CARD_EXTERNAL:
            cur_weizoom_card_rule.card_type = TYPE2NAME['WEIZOOM_CARD_EXTERNAL']
        elif cur_weizoom_card_rule.card_type == WEIZOOM_CARD_INTERNAL:
            cur_weizoom_card_rule.card_type = TYPE2NAME['WEIZOOM_CARD_INTERNAL']
        else:
            cur_weizoom_card_rule.card_type = TYPE2NAME['WEIZOOM_CARD_GIFT']
        cur_weizoom_card_rules.append(cur_weizoom_card_rule)
        
    response = create_response(200)
    response.data.items = cur_weizoom_card_rules
    response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
    response.data.pageinfo = paginator.to_dict(pageinfo)
   
    return response.get_response()


@api(app='card', resource='card_filter_params', action='get')
@login_required
def get_card_filter_params(request):
    """
    获得卡类型的所有筛选条件
    """
    response = create_response(200)
    # 类型

    card_type = [
        {'name': u'外部卡', 'value': WEIZOOM_CARD_EXTERNAL_USER},
        {'name': u'内部卡', 'value': WEIZOOM_CARD_INTERNAL_USER},
        {'name': u'赠品卡', 'value': WEIZOOM_CARD_GIFT_USER}
    ]

    response.data = {
        'card_type': card_type,
    }
    return response.get_response()


@api(app='card', resource='weizoom_cards', action='get')
@login_required
def get_weizoom_cards(request):
    """
    卡列表
    """
    count_per_page = int(request.GET.get('count_per_page', '1'))
    cur_page = int(request.GET.get('page', '1'))
    weizoom_card_rule_id = int(request.GET.get('weizoom_card_rule_id', '-1'))
    weizoom_cards = WeizoomCard.objects.filter(weizoom_card_rule_id=weizoom_card_rule_id)
    #获得已经过期的微众卡id
    today = datetime.today()
    card_ids_need_expire = []
    for card in weizoom_cards:
        #记录过期并且是未使用的微众卡id
        if card.expired_time < today:
            card_ids_need_expire.append(card.id)
    
    if len(card_ids_need_expire) > 0:
        WeizoomCard.objects.filter(id__in=card_ids_need_expire).update(is_expired=True)

    filter_value = request.GET.get('filter_value', '')
    card_number = _get_cardNumber_value(filter_value)
    cardStatus = _get_status_value(filter_value)
    try:
        if card_number != -1:
            weizoom_cards = weizoom_cards.filter(weizoom_card_id__contains=str(card_number))
        if cardStatus != -1:
            weizoom_cards = weizoom_cards.filter(status=cardStatus)
    except:
        pass

    pageinfo, weizoom_cards = paginator.paginate(weizoom_cards, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])    

    weizoom_card_rule = WeizoomCardRule.objects.get(id=weizoom_card_rule_id)
    cur_weizoom_cards = []
    for c in weizoom_cards:
        cur_weizoom_card = JsonResponse()
        cur_weizoom_card.id = c.id
        cur_weizoom_card.status = c.status
        cur_weizoom_card.weizoom_card_id = c.weizoom_card_id
        cur_weizoom_card.password = c.password
        cur_weizoom_card.money = '%.2f' % c.money # 余额

        if c.activated_at:
            cur_weizoom_card.activated_at = c.activated_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            cur_weizoom_card.activated_at = ''

        cur_weizoom_card.total_money ='%.2f' % weizoom_card_rule.money #总额
        cur_weizoom_card.used_money = '%.2f' % (float(cur_weizoom_card.total_money) - float(cur_weizoom_card.money)) #已使用金额
        cur_weizoom_card.remark = weizoom_card_rule.remark
        cur_weizoom_card.valid_time_from = datetime.strftime(weizoom_card_rule.valid_time_from, '%Y-%m-%d %H:%M')
        cur_weizoom_card.valid_time_to = datetime.strftime(weizoom_card_rule.valid_time_to, '%Y-%m-%d %H:%M')
        cur_weizoom_card.is_expired = c.is_expired
        if (c.is_expired and cardStatus == -1) or not c.is_expired:
            cur_weizoom_cards.append(cur_weizoom_card)
        else:
            pageinfo.object_count -= 1
        
    response = create_response(200)
    response.data.items = cur_weizoom_cards
    response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
    response.data.pageinfo = paginator.to_dict(pageinfo)

    return response.get_response()


@api(app='card', resource='weizoom_cards', action='create')
@login_required
def create_weizoom_cards(request):
    """
    创建卡规则
    """
    name = request.POST.get('name', '')
    money = request.POST.get('money', '')
    remark = request.POST.get('remark', '')
    count = request.POST.get('number', '')
    card_type = request.POST.get('card_type', '')
    valid_time_from = request.POST.get('valid_time_from', '')
    valid_time_to = request.POST.get('valid_time_to', '')

    if name not in [card_rule.name for card_rule in WeizoomCardRule.objects.all()]:
        rule = WeizoomCardRule.objects.create(
            owner = request.user,
            name = name,
            money = money,
            remark = remark,
            count = count,
            card_type = card_type,
            valid_time_to = valid_time_to,
            valid_time_from = valid_time_from,
            )
        #生成微众卡
        __create_weizoom_card(rule, count, request)
        response = create_response(200)
        response.data.id = rule.id
    else:
        response = create_response(500)
        response.errMsg = u'您填写的名称已存在，请修改后再提交!'
    return response.get_response()


def __create_weizoom_card(rule, count, request):
    """
    生成微众卡
    """
    count = int(count)
    weizoom_cards = WeizoomCard.objects.all().order_by('-weizoom_card_id')
    if weizoom_cards:
        weizoom_card_id = int(weizoom_cards[0].weizoom_card_id)
    else:
        weizoom_card_id = int(u'0000000')
    
    passwords = set([w.password for w in WeizoomCard.objects.filter(owner=request.user)])

    create_list = []
    for i in range(count):
        weizoom_card_id = int(weizoom_card_id) + 1
        weizoom_card_id = '%07d' % weizoom_card_id
        password = __create_weizoom_card_password(passwords)
        create_list.append(WeizoomCard(
            owner = request.user,
            weizoom_card_rule = rule,
            weizoom_card_id = weizoom_card_id,
            money = rule.money,
            expired_time = rule.valid_time_to,
            password = password
        ))
        passwords.add(password)
    WeizoomCard.objects.bulk_create(create_list)


def __create_weizoom_card_password(passwords):
    """
    生成微众卡密码
    """
    random_args_value = ['1','2','3','4','5','6','7','8','9','0']
    while True:
        password = '%s' % ''.join(random.sample(random_args_value, 7))
        if password not in passwords:
            break
            
    return password


@api(app='card', resource='status', action='update')
@login_required
def update_status(request):
    """
    激活或停用微众卡
    """
    id = request.POST['card_id']
    status = int(request.POST['status'])
    event_type = WEIZOOM_CARD_LOG_TYPE_DISABLE
    weizoom_card = WeizoomCard.objects.get(id=id)
    if weizoom_card.status == WEIZOOM_CARD_STATUS_INACTIVE:
        weizoom_card.activated_at = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        event_type = WEIZOOM_CARD_LOG_TYPE_ACTIVATION

    if (status==0 and weizoom_card.weizoom_card_rule.money!=weizoom_card.money):
        weizoom_card.status = WEIZOOM_CARD_STATUS_USED
    else:
        weizoom_card.status = status=status
    weizoom_card.target_user_id = 0
    weizoom_card.save()

    # 创建激活日志
    module_api.create_weizoom_card_log(request.user.id, -1, event_type, id, weizoom_card.money)
    response = create_response(200)
    return response.get_response()


@api(app='card', resource='batch_status', action='update')
@login_required
def update_batch_status(request):
    """
    批量激活微众卡
    """
    card_ids = request.POST.get('card_id', '')
    if card_ids:
        card_ids = card_ids.split(',')
        activated_at = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        cards = WeizoomCard.objects.filter(id__in=card_ids)
        cards.update(status=0, activated_at=activated_at)

        # 创建激活日志
        for card in cards:
            module_api.create_weizoom_card_log(
                request.user.id, 
                -1, 
                WEIZOOM_CARD_LOG_TYPE_ACTIVATION, 
                card.id, 
                card.money)
        
        response = create_response(200)
    else:
        response = create_response(500)
        response.errMsg = u'没有需要激活的卡'
    return response.get_response()


@api(app='card', resource='onbatch_status', action='update')
@login_required
def update_onbatch_status(request):
    """
    批量停用微众卡
    """
    card_ids = request.POST.get('card_id', '')
    if card_ids:
        card_ids = card_ids.split(',')
        activated_at = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        cards = WeizoomCard.objects.filter(id__in=card_ids)
        cards.update(status=3, activated_at=activated_at)

        # 创建激活日志
        for card in cards:
            module_api.create_weizoom_card_log(
                request.user.id, 
                -1, 
                WEIZOOM_CARD_LOG_TYPE_DISABLE, 
                card.id, 
                card.money)
        
        response = create_response(200)
    else:
        response = create_response(500)
        response.errMsg = u'没有需要激活的卡'
    return response.get_response()


@api(app='card', resource='weizoom_cards', action='append')
@login_required
def append_weizoom_cards(request):
    """
    追加微众卡
    """
    rule_id = request.POST.get('rule_id', '')
    card_num = request.POST.get('card_num', '')
    rule = WeizoomCardRule.objects.get(id=rule_id)
    rule.count = rule.count + int(card_num)
    rule.save()
    #生成微众卡
    __create_weizoom_card(rule, card_num, request)
    
    response = create_response(200)
    response.data.id = rule.id
    response.data.count = rule.count
    return response.get_response()


def _get_status_value(filter_value):
    if filter_value == '-1':
        return -1
    try:
        for item in filter_value.split('|'):
            if item.split(':')[0] == 'cardStatus':
                return int(item.split(':')[1])
        return -1
    except:
        return -1

def _get_type_value(filter_value):
    if filter_value == '-1':
        return -1
    try:
        for item in filter_value.split('|'):
            if item.split(':')[0] == 'cardType':
                return int(item.split(':')[1])
        return -1
    except:
        return -1

def _get_cardNumber_value(filter_value):
    if filter_value == '-1':
        return -1
    try:
        for item in filter_value.split('|'):
            if item.split(':')[0] == 'card_number':
                return str(item.split(':')[1])
        return -1
    except:
        return -1