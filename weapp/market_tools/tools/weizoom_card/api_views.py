# -*- coding: utf-8 -*-
import random


from core import paginator
from core import apiview_util
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from account.models import *
from webapp.modules.mall.models import * 
from core.jsonresponse import JsonResponse, create_response
from datetime import datetime, timedelta

from models import *

from excel_response import ExcelResponse
import module_api

########################################################################
# get_adjust_accounts: 获取核算信息
########################################################################
@login_required
def get_adjust_accounts(request):
	response = create_response(200)
	items,total_price = create_adjust_accounts_infos(request)

	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, red_envelopes = paginator.paginate(items, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])	
	
	response.data.items = red_envelopes
	response.data.total_price = '%.2f' % float(total_price)
	
	response.data.pageinfo = paginator.to_dict(pageinfo)
	response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
		
	return response.get_response()


########################################################################
# get_adjust_accounts_info: 获取核算明细
########################################################################
@login_required
def get_adjust_accounts_info(request):
	response = create_response(200)
	if request.GET.get('username', None):
		items = create_detail_adjust_accounts_infos(request)
		count_per_page = int(request.GET.get('count_per_page', 15))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, red_envelopes = paginator.paginate(items, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])	
		
		response.data.items = red_envelopes
		response.data.pageinfo = paginator.to_dict(pageinfo)
		response.data.sortAttr = request.GET.get('created_at', '-created_at')
		
	return response.get_response()


########################################################################
# export_detail_adjust_accounts:  导出核算明细列表
########################################################################
@login_required
def export_detail_adjust_accounts(request):
	items = create_detail_adjust_accounts_infos(request)
	username = request.GET.get('username', None)
	adjust_accounts_table = [[u'时间', u'卡号', u'操作', u'金额（元）']]
	total = 0.0
	for row in items:
		action = u"【{}】 {}".format(row['event_type'], ('' if row['order_id'] == '-1' else row['order_id']))
		adjust_accounts_table.append([row['created_at'], row['card_id'], action, row['money']])
		total = total + float(row['money'])
	adjust_accounts_table.append([u'合计', '%.2f' % total])
	return ExcelResponse(adjust_accounts_table,output_name=u'核算明细列表'.encode('utf8'),force_csv=False)


########################################################################
# create_detail_adjust_accounts_infos:  生成核算明细信息
########################################################################
@login_required
def create_detail_adjust_accounts_infos(request):
	username = request.GET.get('username', None)
	items = []
	user = User.objects.get(username=username)
	adjust_accounts_infos = WeizoomCardHasOrder.objects.filter(owner_id=user.id).order_by('-created_at')
	if 'start_date' in request.GET:
		try:
			start_date = datetime.strptime(request.GET.get('start_date', '2001-01-01'), '%Y-%m-%d')
			adjust_accounts_infos = adjust_accounts_infos.filter(created_at__gt=start_date).order_by('-created_at')
		except:
			pass
	if 'end_date' in request.GET:
		try:
			end_date = datetime.strptime(request.GET.get('end_date', '2100-01-01'), '%Y-%m-%d') + timedelta(days=1)
			adjust_accounts_infos = adjust_accounts_infos.filter(created_at__lt=end_date).order_by('-created_at')
		except:
			pass
	for adjust_accounts_info in adjust_accounts_infos:
		order_id = adjust_accounts_info.order_id
		# if int(adjust_accounts_info.order_id) == -1:
		# 	order_id = u'积分兑换'
		card_id = adjust_accounts_info.card.weizoom_card_id
		items.append({
			'created_at': adjust_accounts_info.created_at.strftime('%Y/%m/%d %H:%M'),
			'card_id': card_id,
			'data_card_id': adjust_accounts_info.card_id,
			'order_id': order_id,
			'money': '%.2f' % adjust_accounts_info.money,
			'event_type': adjust_accounts_info.event_type
		})
	return items


########################################################################
# export_adjust_accounts:  导出核算列表
########################################################################
@login_required
def export_adjust_accounts(request):
	items,_ = create_adjust_accounts_infos(request)
	adjust_accounts_table = [[u'商家名', u'账号',u'运营类型',u'微众卡（元）', u'积分（元）', u'总金额']]
	total = 0.0
	for row in items:
		adjust_accounts_table.append([row['display_name'], row['name'], row['account_type'], row['weizoom_card_money'],row['integral_money'], row['total_sum']])
		total = float(row['total_sum'])
	adjust_accounts_table.append([u'合计', '%.2f' % total])
	return ExcelResponse(adjust_accounts_table,output_name=u'核算列表'.encode('utf8'),force_csv=False)


########################################################################
# create_adjust_accounts_infos:  生成核算信息
########################################################################
@login_required
def create_adjust_accounts_infos(request):
	
	start_date, end_date = None, None
	if 'start_date' in request.GET:
		start_date = datetime.strptime(request.GET.get('start_date', '2001-01-01'), '%Y-%m-%d')
	if 'end_date' in request.GET:
		end_date = datetime.strptime(request.GET.get('end_date', '2001-01-01'), '%Y-%m-%d') + timedelta(days=1)

	filter_attr = request.GET.get('filter_attr', None)
	if filter_attr == 'account_type':
		account_type = int(request.GET.get('filter_value', '-1'))
	else:
		account_type = None
	items = []
	account_has_weizoom_cards = AccountHasWeizoomCardPermissions.objects.all()
	owner_ids = [account_has_weizoom_card.owner_id for account_has_weizoom_card in account_has_weizoom_cards]
	id2username = {u.id: u.username for u in User.objects.filter(id__in=owner_ids)}
	if account_type != None and int(account_type) >= 0:
		id2webapp_ids = {profile.user_id: profile.webapp_id for profile in UserProfile.objects.filter(user_id__in=owner_ids, account_type=account_type)}
	else:
		id2webapp_ids = {profile.user_id: profile.webapp_id for profile in UserProfile.objects.filter(user_id__in=owner_ids)}

	id2type = {profile.user_id: profile.account_type for profile in UserProfile.objects.filter(user_id__in=owner_ids)}
	total_price = 0
	for id in id2webapp_ids.keys():
		webapp_id = id2webapp_ids[id]
		if start_date and end_date:
			adjust_accounts_money = WeizoomCardHasOrder.objects.filter(created_at__gt=start_date, created_at__lt=end_date, owner_id=id).exclude(order_id='-1').aggregate(Sum("money"))
			integral_money = Order.objects.filter(status__gte=2, integral_money__gt=0, webapp_id=webapp_id, payment_time__gt=start_date, payment_time__lt=end_date).aggregate(Sum("integral_money"))
		elif start_date:
			adjust_accounts_money = WeizoomCardHasOrder.objects.filter(created_at__gt=start_date, owner_id=id).exclude(order_id='-1').aggregate(Sum("money"))
			integral_money = Order.objects.filter(status__gte=2, integral_money__gt=0 ,webapp_id=webapp_id,  payment_time__gt=start_date).aggregate(Sum("integral_money"))
		elif end_date:
			adjust_accounts_money = WeizoomCardHasOrder.objects.filter(created_at__lt=end_date, owner_id=id).exclude(order_id='-1').aggregate(Sum("money"))
			integral_money = Order.objects.filter(status__gte=2, integral_money__gt=0 ,webapp_id=webapp_id, payment_time__lt=end_date).aggregate(Sum("integral_money"))
		else:
			adjust_accounts_money = WeizoomCardHasOrder.objects.filter(owner_id=id).exclude(order_id='-1').aggregate(Sum("money"))
			integral_money = Order.objects.filter(status__gte=2, integral_money__gt=0 ,webapp_id=webapp_id).aggregate(Sum("integral_money"))

		integral_money_sum = 0.00
		if integral_money["integral_money__sum"] is not None:
			integral_money_sum = integral_money["integral_money__sum"]

		adjust_accounts_money_sum = 0.00
		if adjust_accounts_money["money__sum"] is not None:
			adjust_accounts_money_sum = adjust_accounts_money["money__sum"]

		total_sum = integral_money_sum + float(adjust_accounts_money_sum)
		total_price = total_sum + total_price

		account_name = WeizoomCardHasAccount.get_weizoom_card_account_name_by_user(request, id)
		if account_name is None:
			account_name = id2username[id]

		items.append({
			'id': id,
			'name': id2username[id],
			'display_name': account_name,
			'integral_money': '%.2f' % integral_money_sum,
			'weizoom_card_money': '%.2f' % adjust_accounts_money_sum,
			'total_sum': '%.2f' % total_sum,
			'account_type': OPERATION_TYPE[id2type[id]]
		})
	return items, '%.2f' % total_price


def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)


########################################################################
# get_weizoom_cards: 微众卡列表 
########################################################################
@login_required
def get_weizoom_cards(request):
	count_per_page = int(request.GET.get('count_per_page', '1'))
	cur_page = int(request.GET.get('page', '1'))
	weizoom_card_rule_id = int(request.GET.get('weizoom_card_rule_id', '-1'))
	query = request.GET.get('query', None)
	weizoom_cards = WeizoomCard.objects.filter(owner=request.user, weizoom_card_rule_id=weizoom_card_rule_id)
	#获得已经过期的微众卡id
	today = datetime.today()
	card_ids_need_expire = []
	for card in weizoom_cards:
		#记录过期并且是未使用的微众卡id
		if card.expired_time < today:
			card_ids_need_expire.append(card.id)
	
	if len(card_ids_need_expire) > 0:
		WeizoomCard.objects.filter(id__in=card_ids_need_expire).update(is_expired=True)
	
	#处理过滤
	filter_attr = request.GET.get('filter_attr', None)
	filter_value = int(request.GET.get('filter_value', -1))
	if filter_attr and (filter_value != -1):
		params = {filter_attr: filter_value}
		weizoom_cards = weizoom_cards.filter(**params)
		
	if query:
		weizoom_cards = weizoom_cards.filter(weizoom_card_id=query)
	
	pageinfo, weizoom_cards = paginator.paginate(weizoom_cards, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])	
	target_user_ids = []
	for weizoom_card in weizoom_cards:
		target_user_ids.append(weizoom_card.target_user_id)
	card_has_accounts = WeizoomCardHasAccount.objects.filter(owner=request.user, account__in=target_user_ids)
	user2name = {}
	for card_has_account in card_has_accounts:
		user2name[card_has_account.account_id] = card_has_account.account_name
	
	cur_weizoom_cards = []
	for c in weizoom_cards:
		cur_weizoom_card = JsonResponse()
		cur_weizoom_card.id = c.id
		cur_weizoom_card.status = c.status
		cur_weizoom_card.weizoom_card_id = c.weizoom_card_id
		cur_weizoom_card.password = c.password
		cur_weizoom_card.money = '%.2f' % c.money
		if c.activated_at:
			cur_weizoom_card.activated_at = c.activated_at.strftime('%Y-%m-%d %H:%M:%S')
		else:
			cur_weizoom_card.activated_at = ''
		cur_weizoom_card.target_name = user2name.get(c.target_user_id, u'')
		cur_weizoom_card.is_expired = c.is_expired
		cur_weizoom_cards.append(cur_weizoom_card)
		
	response = create_response(200)
	response.data.items = cur_weizoom_cards
	response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
	response.data.pageinfo = paginator.to_dict(pageinfo)
	
	return response.get_response()


########################################################################
# get_weizoom_card_rules: 微众卡列表 
########################################################################
@login_required
def get_weizoom_card_rules(request):
	count_per_page = int(request.GET.get('count_per_page', '1'))
	cur_page = int(request.GET.get('page', '1'))
	weizoom_card_rule_id = int(request.GET.get('weizoom_card_rule_id', '-1'))
	
	weizoom_card_rules = WeizoomCardRule.objects.filter(owner=request.user).order_by('-created_at')
	pageinfo, weizoom_card_rules = paginator.paginate(weizoom_card_rules, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])	
	
	cur_weizoom_card_rules = []
	for c in weizoom_card_rules:
		cur_weizoom_card_rule = JsonResponse()
		cur_weizoom_card_rule.id = c.id
		cur_weizoom_card_rule.name = c.name
		cur_weizoom_card_rule.count = c.count
		cur_weizoom_card_rule.remark = c.remark
		cur_weizoom_card_rule.money = '%.2f' % c.money
		cur_weizoom_card_rule.expired_time = datetime.strftime(c.expired_time, '%Y-%m-%d %H:%M')
		cur_weizoom_card_rule.created_at = datetime.strftime(c.created_at, '%Y-%m-%d %H:%M')
		cur_weizoom_card_rules.append(cur_weizoom_card_rule)
		
	response = create_response(200)
	response.data.items = cur_weizoom_card_rules
	response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
	response.data.pageinfo = paginator.to_dict(pageinfo)
	
	return response.get_response()


########################################################################
# export_weizoom_cards:  导出微众卡
########################################################################
@login_required
def export_weizoom_cards(request):
	id = request.GET.get('id', 0)
	titles = [u'卡号', u'密码', u'使用状态', u'剩余金额', u'激活时间', u'发放目标']
	weizoom_cards_table = []
	weizoom_cards_table.append(titles)
	weizoom_cards = WeizoomCard.objects.filter(owner=request.user, weizoom_card_rule_id=id)
	target_user_ids = []
	for weizoom_card in weizoom_cards:
		target_user_ids.append(weizoom_card.target_user_id)
	card_has_accounts = WeizoomCardHasAccount.objects.filter(owner=request.user, account__in=target_user_ids)
	user2name = {}
	for card_has_account in card_has_accounts:
		user2name[card_has_account.account_id] = card_has_account.account_name
	
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
		target_user_name = user2name.get(c.target_user_id, '')
		if c.activated_at:
			activated_at = c.activated_at.strftime('%Y-%m-%d %H:%M:%S')
		else:
			activated_at = ''
		info = [c.weizoom_card_id, c.password, status_str, c.money, activated_at, target_user_name]
		weizoom_cards_table.append(info)
	
	return ExcelResponse(weizoom_cards_table,output_name=u'微众卡表'.encode('utf8'),force_csv=False)


########################################################################
# __create_weizoom_card_password: 生成微众卡密码
########################################################################
def __create_weizoom_card_password(passwords):
	random_args_value = ['1','2','3','4','5','6','7','8','9','0']
	is_true = True
	while is_true:
		password = '%s' % ''.join(random.sample(random_args_value, 7))
		if password not in passwords:
			is_true = False
			
	return password
							

########################################################################
# __create_weizoom_card: 生成微众卡
########################################################################
def __create_weizoom_card(rule, count, request):
	count = int(count)
	weizoom_cards = WeizoomCard.objects.all().order_by('-weizoom_card_id')
	if weizoom_cards:
		weizoom_card_id = int(weizoom_cards[0].weizoom_card_id)
	else:
		weizoom_card_id = int(u'0000000')
	
	passwords = [w.password for w in WeizoomCard.objects.filter(owner=request.user)]
	for i in range(count):
		weizoom_card_id = int(weizoom_card_id) + 1
		weizoom_card_id = '%07d' % weizoom_card_id
		password = __create_weizoom_card_password(passwords)
		WeizoomCard.objects.create(
			owner = request.user,
			weizoom_card_rule = rule,
			weizoom_card_id = weizoom_card_id,
			money = rule.money,
			expired_time = rule.expired_time,
			password = password
			)
		passwords.append(password)


########################################################################
# create_weizoom_cards:  制作微众卡
########################################################################
@login_required
def create_weizoom_cards(request):
	name = request.POST.get('name', '')
	money = request.POST.get('money', '')
	remark = request.POST.get('remark', '')
	count = request.POST.get('number', '')
	expired_time = request.POST.get('expired_time', '')
	expired_hour = request.POST.get('expired_hour', '')
	expired_minute = request.POST.get('expired_minute', '')
	rule = WeizoomCardRule.objects.create(
		owner = request.user,
		name = name,
		money = money,
		remark = remark,
		count = count,
		expired_time = '%s %s:%s' % (expired_time, expired_hour, expired_minute)
		)
	#生成微众卡
	__create_weizoom_card(rule, count, request)
	
	response = create_response(200)
	response.data.id = rule.id
	return response.get_response()


########################################################################
# append_weizoom_cards:  追加微众卡
########################################################################
@login_required
def append_weizoom_cards(request):
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


########################################################################
# update_status:  激活微众卡
########################################################################
@login_required
def update_status(request):
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


########################################################################
# get_accounts: 获取微众卡对应账号信息
########################################################################
@login_required
def get_accounts(request):
	response = create_response(200)
	card_has_accounts = WeizoomCardHasAccount.get_all_weizoom_card_accounts(request.user)

	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, card_has_accounts = paginator.paginate(card_has_accounts, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])	
	
	account_ids = [c.account_id for c in card_has_accounts]
	users = User.objects.filter(id__in=account_ids)
	id2users = {}
	for user in users:
		id2users[user.id] = user
	
	items = []
	for card_has_account in card_has_accounts:
		account_id = card_has_account.account_id 
		items.append({
			'id': card_has_account.id,
			'account_id': account_id,
			'username': id2users.get(account_id, '').username,
			'nickname': card_has_account.account_name
		})
	
	response.data.items = items
	response.data.pageinfo = paginator.to_dict(pageinfo)
	response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
		
	return response.get_response()


########################################################################
# create_user: 添加微众卡用户
########################################################################
@login_required
def create_user(request):
	username = request.POST.get('username', '')
	nickname = request.POST.get('nickname', '')
	response = create_response(200)
	user = None
	try:
		user = User.objects.get(username=username)
	except:
		response.code = 201
		pass
	if user:
		card_has_account = WeizoomCardHasAccount.objects.create(
			owner = request.user,
			account = user,
			account_name = nickname
			)
		response.data.id = card_has_account.id
	
	return response.get_response()


#===============================================================================
# filter_user_all: 检索账号信息
#===============================================================================
def filter_user_all(request):
	username = request.GET.get('username', '')
	users = User.objects.filter(username__contains=username).exclude(username__in=['admin'])
	
	items = []
	for user in users:
		items.append({
			'id': user.id,
			'name': user.username
		})
	
	response = create_response(200)
	response.data = {
		'items': items,
	}
	return response.get_response()


#===============================================================================
# filter_user_target: 检索微众卡目标账号信息
#===============================================================================
def filter_user_target(request):
	username = request.GET.get('username', '')
	card_has_accounts = WeizoomCardHasAccount.objects.filter(owner=request.user, account_name__contains=username)
	
	items = []
	for card_has_account in card_has_accounts:
		account_id = card_has_account.account_id 
		items.append({
			'id': card_has_account.id,
			'account_id': account_id,
			'nickname': card_has_account.account_name
		})
	response = create_response(200)
	response.data = {
		'items': items,
	}
	return response.get_response()


#===============================================================================
# update_batch_status: 批量激活微众卡
#===============================================================================
def update_batch_status(request):
	card_ids = request.POST.get('card_ids', '')
	target_id = request.POST.get('target_id', '')
	
	activated_at = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
	WeizoomCard.objects.filter(id__in=card_ids.split(',')).update(status=0, target_user_id=target_id, activated_at=activated_at)

	# 创建激活日志
	for card in WeizoomCard.objects.filter(id__in=card_ids.split(',')):
		module_api.create_weizoom_card_log(
			request.user.id, 
			-1, 
			WEIZOOM_CARD_LOG_TYPE_ACTIVATION, 
			card.id, 
			card.money)
	
	response = create_response(200)
	return response.get_response()


@login_required
def get_integral_adjust_accounts(request):
	count_per_page = int(request.GET.get('count_per_page', '1'))
	cur_page = int(request.GET.get('page', '1'))
	items = []
	user_profile = UserProfile.objects.get(user_id=request.GET.get('user_id'))
	group_datas = Order.objects.filter(status__gte=2, webapp_id=user_profile.webapp_id).values('integral_each_yuan').annotate(count=Count('integral_each_yuan'))
	webapp_id = user_profile.webapp_id
	for group_data in group_datas:
		integral_each_yuan = group_data['integral_each_yuan']
		if integral_each_yuan and int(integral_each_yuan) != -1:
			integral_count = Order.objects.filter(status__gte=2, webapp_id=webapp_id, integral_each_yuan=integral_each_yuan).aggregate(Sum('integral'))
			integral_sum = 0
			if integral_count["integral__sum"] is not None:
				integral_sum = integral_count["integral__sum"]

			integral_money_sums = Order.objects.filter(status__gte=2, webapp_id=webapp_id, integral_each_yuan=integral_each_yuan).aggregate(Sum('integral_money'))
			integral_money_sum = 0.00
			if integral_money_sums["integral_money__sum"] is not None:
				integral_money_sum = integral_money_sums["integral_money__sum"]

			items.append({
				'integral_each_yuan': integral_each_yuan,
				'integral': integral_sum,
				'integral_money_sum': '%.2f' %  integral_money_sum
			})

	pageinfo, items = paginator.paginate(items, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])	

	response = create_response(200)
	response.data.pageinfo = paginator.to_dict(pageinfo)
	response.data.items = items
	return response.get_response()