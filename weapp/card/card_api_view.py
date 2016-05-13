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
from excel_response import ExcelResponse
#微众卡类型
from weixin.user.models import MpuserPreviewInfo, ComponentAuthedAppidInfo

WEIZOOM_CARD_EXTERNAL = 0
WEIZOOM_CARD_INTERNAL = 1
WEIZOOM_CARD_GIFT = 2

TYPE2NAME = {
	'WEIZOOM_CARD_EXTERNAL': u'外部卡',
	'WEIZOOM_CARD_INTERNAL': u'内部卡',
	'WEIZOOM_CARD_GIFT': u'赠品卡'
}
CARDTYPE2NAME = {
	WEIZOOM_CARD_EXTERNAL: u'外部卡',
	WEIZOOM_CARD_INTERNAL: u'内部卡',
	WEIZOOM_CARD_GIFT: u'赠品卡'
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
	weizoomcardpermission=WeiZoomCardPermission.objects.filter(user_id=request.user.id)
	can_export_batch_card=0
	can_delay_card=0
	if weizoomcardpermission:
		can_export_batch_card=weizoomcardpermission[0].can_export_batch_card
		can_delay_card=weizoomcardpermission[0].can_delay_card
	if card_name:
		weizoom_card_rules = weizoom_card_rules.filter(name__icontains = card_name)

	# 时间区间
	date_interval = request.GET.get('date_interval', '')
	if date_interval:
		date_interval = get_datetime_from_date_interval(date_interval)
		weizoom_card_rules = weizoom_card_rules.filter(valid_time_from__gte=date_interval[0],valid_time_to__lte=date_interval[1])


	filter_value = request.GET.get('filter_value', '')
	card_type = _get_type_value(filter_value)
	card_attr = _get_attr_value(filter_value)
	if card_type != -1:
		weizoom_card_rules = weizoom_card_rules.filter(card_type= card_type)
	if card_attr != -1:
		weizoom_card_rules = weizoom_card_rules.filter(card_attr= card_attr)

	#卡号区间查询
	card_num_min = request.GET.get('card_num_min','')
	card_num_max = request.GET.get('card_num_max','')

	if card_num_min or card_num_max:

		card_rule_ids = [int(r.id) for r in weizoom_card_rules]
		all_cards = WeizoomCard.objects.filter(weizoom_card_rule_id__in=card_rule_ids)
		rule_id2cards = {}

		for c in all_cards:
			card_rule_id = c.weizoom_card_rule_id
			if card_rule_id not in rule_id2cards:
				rule_id2cards[card_rule_id] = [c]
			else:
				rule_id2cards[card_rule_id].append(c)

		weizoom_card_id2rule_ids={}

		for rule_id in rule_id2cards:
			for card in rule_id2cards[rule_id]:
				weizoom_card_id2rule_ids[card.weizoom_card_id] = rule_id

		card_num_set = set(int(i) for i in weizoom_card_id2rule_ids.keys())

		if card_num_min and card_num_max:
			max_num = int(card_num_max)
			min_num = int(card_num_min)
			search_set = set(range(min_num,max_num+1))
		elif card_num_max:
			search_set = set([int(card_num_max)])
		elif card_num_min:
			search_set = set([int(card_num_min)])
		else:
			search_set = set([])
		result_set = search_set & card_num_set
		result_list = list(result_set)

		if len(result_list)>0:
			filter_cards_id_list=[]
			for card_num in result_list:
				filter_cards_id_list.append(u'%07d'%card_num)

			filter_rule_ids = []
			for card in filter_cards_id_list:
				r_id = weizoom_card_id2rule_ids[card]
				filter_rule_ids.append(r_id)
			filter_rule_ids = list(set(filter_rule_ids))
			weizoom_card_rules = weizoom_card_rules.filter(id__in= filter_rule_ids)
		if len(result_list)==0:
			weizoom_card_rules =[]

	pageinfo, weizoom_card_rules = paginator.paginate(weizoom_card_rules, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

	card_rule_ids = []
	user_ids = []
	for r in weizoom_card_rules:
		card_rule_ids.append(int(r.id))
		belong_to_owner_list = str(r.shop_limit_list).split(',')
		for a in belong_to_owner_list:
			if a != '-1':
				user_ids.append(a)
	user_id2store_name = {}
	user_profiles = UserProfile.objects.filter(user_id__in=user_ids)
	for user_profile in user_profiles:
		if user_profile.store_name:
			user_id2store_name[str(user_profile.user_id)] = user_profile.store_name

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
		if r_id in rule_id2cards:
			weizoom_cards = rule_id2cards[r_id]
			weizoom_card_ids = [int(weizoom_cards[0].weizoom_card_id), int(weizoom_cards[::-1][0].weizoom_card_id)]
			rule_id2card_ids[r_id] = weizoom_card_ids

	cur_weizoom_card_rules = []

	for rule in weizoom_card_rules:
		belong_to_owner_list2store_names=[]
		belong_to_owner_list = str(rule.shop_limit_list).split(',')
		for a in belong_to_owner_list:
			if a != '-1':
				belong_to_owner_list2store_name=user_id2store_name.get(a,None)
				belong_to_owner_list2store_names.append(belong_to_owner_list2store_name)
		cur_weizoom_card_rule = JsonResponse()
		cur_weizoom_card_rule.id = rule.id
		cur_weizoom_card_rule.name = rule.name
		cur_weizoom_card_rule.count = rule.count
		cur_weizoom_card_rule.remark = rule.remark
		cur_weizoom_card_rule.money = '%.2f' % rule.money
		cur_weizoom_card_rule.card_type = rule.card_type
		cur_weizoom_card_rule.is_new_member_special = rule.is_new_member_special
		cur_weizoom_card_rule.card_attr = rule.card_attr
		cur_weizoom_card_rule.belong_to_owner = belong_to_owner_list2store_names
		cur_weizoom_card_rule.valid_time_from = rule.valid_time_from.strftime('%Y-%m-%d %H:%M')
		cur_weizoom_card_rule.valid_time_to = rule.valid_time_to.strftime('%Y-%m-%d %H:%M')
		cur_weizoom_card_rule.created_at = rule.created_at.strftime('%Y-%m-%d %H:%M')
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
	response.data.can_delay_card = can_delay_card
	response.data.can_export_batch_card = can_export_batch_card
	return response.get_response()

@api(app='card', resource='managers', action='get')
@login_required 
def get_managers(request):
	count_per_page = int(request.GET.get('count_per_page', '1'))
	cur_page = int(request.GET.get('page', '1'))
	is_manage = 'manage' in request.GET
	if is_manage:
		card_managers=WeiZoomCardManager.objects.all()
	else:
		card_managers=WeiZoomCardManager.objects.exclude(user_id=request.user.id)
	pageinfo, card_managers = paginator.paginate(card_managers, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	weizoomcardpermissions=WeiZoomCardPermission.objects.all()
	card_manager2weizoomcardpermission={}
	for weizoomcardpermission in weizoomcardpermissions:
		card_manager2weizoomcardpermission[weizoomcardpermission.user_id]=weizoomcardpermission
	cur_card_managers=[]
	for card_manager in card_managers:
		cur_card_manager=JsonResponse()
		cur_card_manager.id=card_manager.id
		cur_card_manager.user_id=card_manager.user_id
		cur_card_manager.username=card_manager.username
		cur_card_manager.nickname=card_manager.nickname		
		try:
			cur_card_manager.can_create_card=card_manager2weizoomcardpermission[card_manager.user_id].can_create_card
			cur_card_manager.can_export_batch_card=card_manager2weizoomcardpermission[card_manager.user_id].can_export_batch_card
			cur_card_manager.can_add_card=card_manager2weizoomcardpermission[card_manager.user_id].can_add_card
			cur_card_manager.can_batch_stop_card=card_manager2weizoomcardpermission[card_manager.user_id].can_batch_stop_card
			cur_card_manager.can_batch_active_card=card_manager2weizoomcardpermission[card_manager.user_id].can_batch_active_card
			cur_card_manager.can_view_card_details=card_manager2weizoomcardpermission[card_manager.user_id].can_view_card_details
			cur_card_manager.can_stop_card=card_manager2weizoomcardpermission[card_manager.user_id].can_stop_card
			cur_card_manager.can_active_card=card_manager2weizoomcardpermission[card_manager.user_id].can_active_card
			cur_card_manager.can_delay_card=card_manager2weizoomcardpermission[card_manager.user_id].can_delay_card
			cur_card_manager.can_change_shop_config=card_manager2weizoomcardpermission[card_manager.user_id].can_change_shop_config
			cur_card_manager.can_view_statistical_details=card_manager2weizoomcardpermission[card_manager.user_id].can_view_statistical_details
			cur_card_manager.can_export_statistical_details=card_manager2weizoomcardpermission[card_manager.user_id].can_export_statistical_details
		except:
			pass
		cur_card_managers.append(cur_card_manager)
	response = create_response(200)
	response.data.items = cur_card_managers 
	response.data.pageinfo = paginator.to_dict(pageinfo)  
	return response.get_response()


@api(app='card', resource='weizoomcard_permission_own', action='get')
@login_required 
def get_weizoomcard_permission_own(request):
	post = request.POST
	user_id =int(post.get('user_id',''))
	weizoomcardpermission=WeiZoomCardPermission.objects.filter(user_id=user_id)
	cur_weizoomcardpermission=[]
	if weizoomcardpermission:
		cur_weizoomcardpermission=JsonResponse()
		cur_weizoomcardpermission.can_create_card=weizoomcardpermission[0].can_create_card
		cur_weizoomcardpermission.can_export_batch_card=weizoomcardpermission[0].can_export_batch_card
		cur_weizoomcardpermission.can_add_card=weizoomcardpermission[0].can_add_card
		cur_weizoomcardpermission.can_batch_stop_card=weizoomcardpermission[0].can_batch_stop_card
		cur_weizoomcardpermission.can_batch_active_card=weizoomcardpermission[0].can_batch_active_card
		cur_weizoomcardpermission.can_view_card_details=weizoomcardpermission[0].can_view_card_details
		cur_weizoomcardpermission.can_stop_card=weizoomcardpermission[0].can_stop_card
		cur_weizoomcardpermission.can_active_card=weizoomcardpermission[0].can_active_card
		cur_weizoomcardpermission.can_delay_card=weizoomcardpermission[0].can_delay_card
		cur_weizoomcardpermission.can_change_shop_config=weizoomcardpermission[0].can_change_shop_config
		cur_weizoomcardpermission.can_view_statistical_details=weizoomcardpermission[0].can_view_statistical_details
		cur_weizoomcardpermission.can_export_statistical_details=weizoomcardpermission[0].can_export_statistical_details
	response = create_response(200)
	response.data.items = cur_weizoomcardpermission 
	return response.get_response()


@api(app='card', resource='weizoomcard_permission', action='get')
@login_required 
def get_weizoomcard_permission(request):
	post = request.POST
	user_id =int(post.get('user_id',''))
	can_create_card = post.get('can_create_card','')
	if can_create_card =='false':
		can_create_card=0
	else:
		can_create_card=1
	can_export_batch_card = post.get('can_export_batch_card','')
	if can_export_batch_card =='false':
		can_export_batch_card=0
	else:
		can_export_batch_card=1
	can_add_card = post.get('can_add_card','')
	if can_add_card =='false':
		can_add_card=0
	else:
		can_add_card=1
	can_batch_stop_card = post.get('can_batch_stop_card','')
	if can_batch_stop_card =='false':
		can_batch_stop_card=0
	else:
		can_batch_stop_card=1
	can_batch_active_card = post.get('can_batch_active_card','')
	if can_batch_active_card =='false':
		can_batch_active_card=0
	else:
		can_batch_active_card=1
	can_stop_card = post.get('can_stop_card','')
	if can_stop_card =='false':
		can_stop_card=0
	else:
		can_stop_card=1
	can_active_card = post.get('can_active_card','')
	if can_active_card =='false':
		can_active_card=0
	else:
		can_active_card=1
	can_delay_card = post.get('can_delay_card','')
	if can_delay_card =='false':
		can_delay_card=0
	else:
		can_delay_card=1
	can_view_card_details = post.get('can_view_card_details','')
	if can_view_card_details =='false':
		can_view_card_details=0
	else:
		can_view_card_details=1
	can_change_shop_config = post.get('can_change_shop_config','')
	if can_change_shop_config =='false':
		can_change_shop_config=0
	else:
		can_change_shop_config=1
	can_view_statistical_details = post.get('can_view_statistical_details','')
	if can_view_statistical_details =='false':
		can_view_statistical_details=0
	else:
		can_view_statistical_details=1
	can_export_statistical_details = post.get('can_export_statistical_details','')
	if can_export_statistical_details =='false':
		can_export_statistical_details=0
	else:
		can_export_statistical_details=1
	managers = WeiZoomCardPermission.objects.all()
	manager_ids = []
	for manager in managers:
		manager_ids.append(manager.user_id)
	if user_id in manager_ids:
		weizoomcardpermission=WeiZoomCardPermission.objects.filter(user_id=user_id)
		weizoomcardpermission.update(can_create_card=can_create_card,
		can_export_batch_card=can_export_batch_card,
		can_add_card=can_add_card,
		can_batch_stop_card=can_batch_stop_card,
		can_batch_active_card=can_batch_active_card,
		can_stop_card=can_stop_card,
		can_active_card=can_active_card,
		can_delay_card=can_delay_card,
		can_view_card_details=can_view_card_details,
		can_change_shop_config=can_change_shop_config,
		can_view_statistical_details=can_view_statistical_details,
		can_export_statistical_details=can_export_statistical_details)
		response = create_response(200)
	else:
		try:
			WeiZoomCardPermission.objects.create(
				user_id=user_id,
				can_create_card=can_create_card,
				can_export_batch_card=can_export_batch_card,
				can_add_card=can_add_card,
				can_batch_stop_card=can_batch_stop_card,
				can_batch_active_card=can_batch_active_card,
				can_stop_card=can_stop_card,
				can_active_card=can_active_card,
				can_delay_card=can_delay_card,
				can_view_card_details=can_view_card_details,
				can_change_shop_config=can_change_shop_config,
				can_view_statistical_details=can_view_statistical_details,
				can_export_statistical_details=can_export_statistical_details
				)
			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'error'
	return response.get_response()

@api(app='card', resource='card_filter_params', action='get')
@login_required
def get_card_filter_params(request):
	"""
	获得卡类型的所有筛选条件
	"""
	# 类型

	card_types = [
		{'name': u'外部卡', 'value': WEIZOOM_CARD_EXTERNAL_USER},
		{'name': u'内部卡', 'value': WEIZOOM_CARD_INTERNAL_USER},
		{'name': u'赠品卡', 'value': WEIZOOM_CARD_GIFT_USER}
	]
	#卡的属性
	card_attrs = [
		{'name': u'通用卡', 'value': WEIZOOM_CARD_ORDINARY},
		{'name': u'专属卡', 'value': WEIZOOM_CARD_SPECIAL}
	]
	response = create_response(200)
	response.data = {
		'card_types': card_types,
		'card_attrs': card_attrs
	}
	return response.get_response()


@api(app='card', resource='weizoom_cards', action='get')
@login_required
def get_weizoom_cards(request):
	"""
	卡列表
	"""
	count_per_page = int(100)
	cur_page = int(request.GET.get('page', '1'))
	weizoom_card_rule_id = int(request.GET.get('weizoom_card_rule_id', '-1'))
	weizoom_cards = WeizoomCard.objects.filter(weizoom_card_rule_id=weizoom_card_rule_id)
	weizoomcardpermission=WeiZoomCardPermission.objects.filter(user_id=request.user.id)
	can_active_card=0
	can_stop_card=0
	can_view_card_details = 0
	if weizoomcardpermission:
		can_active_card=weizoomcardpermission[0].can_active_card
		can_stop_card=weizoomcardpermission[0].can_stop_card
		can_view_card_details=weizoomcardpermission[0].can_view_card_details

	#获得已经过期的微众卡id
	today = datetime.today()
	card_ids_need_expire = []
	for card in weizoom_cards:
		#记录过期并且是未使用的微众卡id
		if card.expired_time < today:
			card_ids_need_expire.append(card.id)
	if len(card_ids_need_expire) > 0:
		WeizoomCard.objects.filter(id__in=card_ids_need_expire).update(is_expired=True)
	# weizoom_cards = WeizoomCard.objects.filter(weizoom_card_rule_id=weizoom_card_rule_id)
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

	#卡号区间查询
	card_num_min = request.GET.get('card_num_min','')
	card_num_max = request.GET.get('card_num_max','')

	if card_num_min or card_num_max:
		weizoom_card_id_set = set([int(c.weizoom_card_id) for c in weizoom_cards])

		if card_num_min and card_num_max:
			min_num = int(card_num_min)
			max_num = int(card_num_max)
			search_set = set(range(min_num,max_num+1))
		elif card_num_max:
			search_set = set([int(card_num_max)])
		elif card_num_min:
			search_set = set([int(card_num_min)])
		else:
			search_set = set([])
		result_set = search_set & weizoom_card_id_set
		result_list = list(result_set)

		if len(result_list)>0:
			filter_cards_id_list=[]
			for card_num in result_list:
				filter_cards_id_list.append(u'%07d'%card_num)
			weizoom_cards = weizoom_cards.filter(weizoom_card_id__in=filter_cards_id_list)
		if len(result_list)==0:
			weizoom_cards =[]



	pageinfo, weizoom_cards = paginator.paginate(weizoom_cards, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

	weizoom_card_rule = WeizoomCardRule.objects.filter(id=weizoom_card_rule_id)
	rule_id2rule = {rule.id:rule for rule in weizoom_card_rule}
	card_recharge = WeizoomCardRecharge.objects.all()
	id2recharge_money = {}
	for card in card_recharge:
		if card.card_id not in id2recharge_money:
			id2recharge_money[card.card_id] = card.recharge_money
		else:
			id2recharge_money[card.card_id] += card.recharge_money
	cur_weizoom_cards = []
	for c in weizoom_cards:
		cur_weizoom_card = JsonResponse()
		cur_weizoom_card.id = c.id
		cur_weizoom_card.status = c.status
		cur_weizoom_card.weizoom_card_id = c.weizoom_card_id
		cur_weizoom_card.password = c.password
		cur_weizoom_card.active_card_user_id = c.active_card_user_id #激活卡用户的id
		cur_weizoom_card.user_id = request.user.id #当前用户的id
		cur_weizoom_card.money = '%.2f' % c.money # 余额

		rule_money = 0.0 if c.weizoom_card_rule_id not in rule_id2rule else rule_id2rule[c.weizoom_card_rule_id].money
		money = '%.2f' % c.money # 余额
		recharge_money = 0 if c.id not in id2recharge_money else id2recharge_money[c.id]
		total_money ='%.2f' % (float(rule_money) + recharge_money) #总额
		used_money = '%.2f' % (float(total_money) - float(money)) #已使用金额

		if c.activated_at:
			cur_weizoom_card.activated_at = c.activated_at.strftime('%Y-%m-%d %H:%M:%S')
		else:
			cur_weizoom_card.activated_at = ''
		valid_time_from = '' if c.weizoom_card_rule_id not in rule_id2rule else rule_id2rule[c.weizoom_card_rule_id].valid_time_from
		valid_time_to = '' if c.weizoom_card_rule_id not in rule_id2rule else rule_id2rule[c.weizoom_card_rule_id].valid_time_to
		cur_weizoom_card.total_money = total_money#总额
		cur_weizoom_card.used_money = used_money #已使用金额
		cur_weizoom_card.remark = c.remark
		cur_weizoom_card.activated_to = c.activated_to
		cur_weizoom_card.department = c.department
		cur_weizoom_card.valid_time_from = datetime.strftime(valid_time_from, '%Y-%m-%d %H:%M')
		cur_weizoom_card.valid_time_to = datetime.strftime(c.expired_time, '%Y-%m-%d %H:%M')
		cur_weizoom_card.is_expired = c.is_expired
		if (c.is_expired and cardStatus == -1) or not c.is_expired:
			cur_weizoom_cards.append(cur_weizoom_card)
		else:
			pageinfo.object_count -= 1

	response = create_response(200)
	response.data.items = cur_weizoom_cards
	response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
	response.data.pageinfo = paginator.to_dict(pageinfo)
	response.data.can_active_card=can_active_card
	response.data.can_stop_card=can_stop_card
	response.data.can_view_card_details = can_view_card_details
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
	card_attr = request.POST.get('card_attr','')
	cur_belong_to_owner = request.POST.get('belong_to_owner','[-1]')
	is_new_member_special = request.POST.get('is_new_member_special', 0)
	valid_restrictions = request.POST.get('full_use_value', -1)
	belong_to_owner = json.loads(cur_belong_to_owner)

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
			expired_time = valid_time_to,
			card_attr = card_attr,
			shop_limit_list = ','.join(belong_to_owner),
			is_new_member_special = is_new_member_special,
			valid_restrictions= valid_restrictions if valid_restrictions else -1
			)
		#生成微众卡
		__create_weizoom_card(rule, count, request)
		response = create_response(200)
		response.data.id = rule.id
	else:
		response = create_response(500)
		response.errMsg = u'您填写的名称已存在，请修改后再提交!'
	return response.get_response()

@api(app='card', resource='all_cards', action='post')
@login_required
def post_all_cards(request):
	count_per_page = int(15)
	cur_page = int(request.GET.get('page', '1'))
	search_query = request.GET.get('query','')
	orgin_card_list = request.GET.get('orginCardList', '')
	#获得已经过期的微众卡id
	today = datetime.today()
	WeizoomCard.objects.filter(expired_time__lte=today, is_expired=False).update(is_expired=True)

	card_status = [WEIZOOM_CARD_STATUS_UNUSED,WEIZOOM_CARD_STATUS_USED,WEIZOOM_CARD_STATUS_EMPTY]
	weizoom_cards = WeizoomCard.objects.filter(status__in=card_status,is_expired=False)
	if search_query:
		search_query_dict=json.loads(search_query)
		card_filter_id = search_query_dict['cardIds']
		if card_filter_id:
			weizoom_cards = WeizoomCard.objects.filter(weizoom_card_id__contains=card_filter_id)
	can_active_card = 0
	can_stop_card = 0
	can_view_card_details = 0

	pageinfo, weizoom_cards = paginator.paginate(weizoom_cards, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	rule_card_ids = set([weizoom_card.weizoom_card_rule_id for weizoom_card in weizoom_cards])
	w_card_ids = set([weizoom_card.id for weizoom_card in weizoom_cards])
	weizoom_card_rule = WeizoomCardRule.objects.filter(id__in=rule_card_ids)
	card_recharge = WeizoomCardRecharge.objects.filter(card_id__in=w_card_ids)
	id2recharge_money = {}
	for card in card_recharge:
		if card.card_id not in id2recharge_money:
			id2recharge_money[card.card_id] = card.recharge_money
		else:
			id2recharge_money[card.card_id] += card.recharge_money
	id2total_money = {card_rule.id:card_rule.money for card_rule in weizoom_card_rule}
	cur_weizoom_cards = []
	for c in weizoom_cards:
		cur_weizoom_card = JsonResponse()
		cur_weizoom_card.id = c.id
		cur_weizoom_card.status = c.status
		cur_weizoom_card.weizoom_card_id = c.weizoom_card_id
		cur_weizoom_card.user_id = request.user.id #当前用户的id
		cur_weizoom_card.money = '%.2f' % c.money # 余额

		if c.activated_at:
			cur_weizoom_card.activated_at = c.activated_at.strftime('%Y-%m-%d %H:%M:%S')
		else:
			cur_weizoom_card.activated_at = ''
		recharge_money = 0 if c.id not in id2recharge_money else id2recharge_money[c.id]
		cur_weizoom_card.total_money ='%.2f' % (0 if c.weizoom_card_rule_id not in id2total_money else id2total_money[c.weizoom_card_rule_id]) #总额
		cur_weizoom_card.used_money = '%.2f' % (float(cur_weizoom_card.total_money) - float(cur_weizoom_card.money) + recharge_money)#已使用金额
		cur_weizoom_card.is_expired = c.is_expired
		cur_weizoom_card.recharge_money = '%.2f' % recharge_money
		if (c.is_expired) or not c.is_expired:
			cur_weizoom_cards.append(cur_weizoom_card)
		else:
			pageinfo.object_count -= 1
	response = create_response(200)
	response.data.items = cur_weizoom_cards
	response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
	response.data.pageinfo = paginator.to_dict(pageinfo)
	response.data.can_active_card = can_active_card
	response.data.can_stop_card = can_stop_card
	response.data.can_view_card_details = can_view_card_details
	response.data.orgin_card_list = orgin_card_list
	return response.get_response()

@api(app='card', resource='card_recharge', action='save')
@login_required
def save_card_recharge(request):
	card_choose = request.GET.get('card_choose', None)  
	card_choose = json.loads(card_choose)
	create_list = []
	# add_log_fields_list = []
	for card in card_choose:
		cardId = card['cardId']
		rechargeMoney = card['rechargeMoney']
		cardNum = card['cardNum']
		weizoom_card = WeizoomCard.objects.get(id=cardId)
		remainder = float(weizoom_card.money) + float(rechargeMoney)
		weizoom_card.money = remainder
		weizoom_card.save()
		create_list.append(WeizoomCardRecharge(
			user_id = request.user.id,
			card_id = cardId,
			recharge_money = rechargeMoney,
			remainder = remainder
		))
		#记录卡充值
		# add_log_fields_list.append({
		#	 'operater': request.user,
		#	 'operater_name': request.user,
		#	 'operate_log': u'给微众卡 %s 充值 %s 元' % (cardNum,rechargeMoney)
		# })
	# moneyLog.create_money_log(add_log_fields_list)
	WeizoomCardRecharge.objects.bulk_create(create_list)
	response = create_response(200)
	return response.get_response()

@api(app='card', resource='recharge_card_list', action='get')
@login_required
def get_recharge_card_list(request):
	card_recharge_list, pageinfo = get_recharge_datas(request)
	response = create_response(200)
	response.data.items = card_recharge_list
	response.data.pageinfo = paginator.to_dict(pageinfo)
	return response.get_response()

@view(app='card', resource='recharge_card_export', action='get')
@login_required
def get_recharge_card_export(request):
	"""
	微众卡充值导出
	"""
	card_recharge_list = get_recharge_datas(request)

	members_info = [
		[u'卡号', u'余额',u'已使用金额',u'充值额度',u'卡属性',u'卡类型',u'专属商家',u'充值日期',u'备注']
	]
	for card_recharge in card_recharge_list:
		belong_to_owner = card_recharge['belong_to_owner'] if card_recharge['belong_to_owner'] else ''
		info_list = [
			card_recharge['card_number'],
			card_recharge['remainder'],
			card_recharge['used_money'],
			card_recharge['recharge_money'],
			card_recharge['card_attr'],
			card_recharge['card_type'],
			belong_to_owner,
			card_recharge['created_at'],
			card_recharge['remark']
		]
		members_info.append(info_list)
	filename = u'微众卡充值列表'#TODO 上线 加.encode('utf8')
	return ExcelResponse(members_info, output_name=filename.encode('utf8'), force_csv=False)

def get_recharge_datas(request):
	card_number = request.GET.get('card_number', None)
	card_type = request.GET.get('cardType', None)
	card_attr = request.GET.get('cardAttr', None)
	date_interval = request.GET.get('date_interval', None)
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', 1))
	is_export = request.GET.get('is_export', 0)

	cards = WeizoomCard.objects.all().order_by('-created_at')
	weizoom_card_rules = WeizoomCardRule.objects.all().order_by('-created_at')
	card_recharges = WeizoomCardRecharge.objects.all().order_by('-created_at')
	card_orders = WeizoomCardHasOrder.objects.exclude(order_id__in=['-1','-2']).order_by('-created_at')

	#查询
	if card_number:
		cards = cards.filter(weizoom_card_id__contains = card_number)
		card_id_list = [card.id for card in cards]
		card_recharges = card_recharges.filter(card_id__in = card_id_list)
	if card_type and int(card_type) != -1:
		weizoom_card_rules = weizoom_card_rules.filter(card_type = card_type)
		rule_id_list = [rule.id for rule in weizoom_card_rules]
		cards = cards.filter(weizoom_card_rule_id__in = rule_id_list)
		card_id_list = [card.id for card in cards]
		card_recharges = card_recharges.filter(card_id__in = card_id_list)
	if card_attr and int(card_attr) != -1:
		weizoom_card_rules = weizoom_card_rules.filter(card_attr = card_attr)
		rule_id_list = [rule.id for rule in weizoom_card_rules]
		cards = cards.filter(weizoom_card_rule_id__in = rule_id_list)
		card_id_list = [card.id for card in cards]
		card_recharges = card_recharges.filter(card_id__in = card_id_list)
	if date_interval:
		date_interval = get_datetime_from_date_interval(date_interval)
		# weizoom_card_rules = weizoom_card_rules.filter(valid_time_from__gte=date_interval[0],valid_time_to__lte=date_interval[1])
		# start_date = start_date.replace(' ','') + " 00:00:00"
		# end_date = end_date.replace(' ','') + " 23:59:59"
		card_recharges = card_recharges.filter(created_at__gte = date_interval[0],created_at__lte = date_interval[1])
	if not is_export:
		#分页的数据
		pageinfo, card_recharges = paginator.paginate(card_recharges, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

	user_ids = []
	for r in weizoom_card_rules:
		belong_to_owner_list = str(r.shop_limit_list).split(',')
		for a in belong_to_owner_list:
			if a != '-1':
				user_ids.append(a)

	user_id2store_name = {}
	user_profiles = UserProfile.objects.filter(user_id__in=user_ids)
	for user_profile in user_profiles:
		if user_profile.store_name:
			user_id2store_name[user_profile.user_id] =user_profile.store_name
	card_recharge_list = []
	if card_recharges:
		for recharge in card_recharges:
			card_id = recharge.card_id
			orders = card_orders.filter(card_id = card_id)
			used_money = 0
			for order in orders:
				used_money = order.money = used_money +order.money
			card_detail = cards.get(id = card_id)
			weizoom_card_rule_id = card_detail.weizoom_card_rule_id
			rule_detail = weizoom_card_rules.get(id = weizoom_card_rule_id)
			is_new_member_special = rule_detail.is_new_member_special
			belong_to_owner_list = str(rule_detail.shop_limit_list).split(',')
			belong_to_owner = [user_id2store_name.get(int(i), '') for i in belong_to_owner_list]
			recharge_money = recharge.recharge_money
			if recharge_money > 0:
				recharge_money = '+'+str('%.2f' % recharge_money)
			else:
				recharge_money = '%.2f' % recharge_money

			card_recharge_list.append({
				"recharge_money": recharge_money,
				'created_at': recharge.created_at.strftime('%Y-%m-%d %H:%M'),
				'remainder': '%.2f' % recharge.remainder,
				'card_number': card_detail.weizoom_card_id,
				'remark': card_detail.remark,
				'card_type': CARDTYPE2NAME[rule_detail.card_type],
				'card_attr': rule_detail.card_attr,
				'is_new_member_special': is_new_member_special,
				'belong_to_owner': belong_to_owner,
				'used_money': '%.2f' % used_money
			})
	if not is_export:
		return card_recharge_list,pageinfo
	else:
		return card_recharge_list

def __create_weizoom_card(rule, count, request):
	"""
	生成微众卡
	"""
	count = int(count)
	weizoom_cards = WeizoomCard.objects.filter(weizoom_card_id__startswith='0').order_by('-weizoom_card_id')
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
			password = password,
			active_card_user_id = 0
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


@api(app='card', resource='card_info', action='get')
@login_required
def get_card_info(request):
	id = request.POST['card_id']
	weizoom_card = WeizoomCard.objects.get(id=id)
	dic_card = {
		'card_remark': weizoom_card.remark,
		'activated_to': weizoom_card.activated_to,
		'department': weizoom_card.department
	}

	response = create_response(200)
	response.data.weizoom_card_info = dic_card
	return response.get_response()


@api(app='card', resource='status', action='update')
@login_required
def update_status(request):
	"""
	激活或停用微众卡
	"""
	try:
		id = request.POST.get('card_id','')
		card_remark = request.POST.get('card_remark','')
		activated_to = request.POST.get('activated_to','')
		department = request.POST.get('department','')
		operate_style = request.POST.get('operate_style','')  
		# status = int(request.POST['status'])
		event_type = WEIZOOM_CARD_LOG_TYPE_DISABLE
		weizoom_card = WeizoomCard.objects.get(id=id)
		if operate_style == 'active':
			status = 0
			weizoom_card.active_card_user_id = request.user.id
			operate_log = u'激活'
		else:
			status = 3
			operate_log = u'停用'
		if weizoom_card.status == WEIZOOM_CARD_STATUS_INACTIVE:
			weizoom_card.activated_at = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
			event_type = WEIZOOM_CARD_LOG_TYPE_ACTIVATION

		if (status==0 and weizoom_card.weizoom_card_rule.money!=weizoom_card.money):
			weizoom_card.status = WEIZOOM_CARD_STATUS_USED
		else:
			weizoom_card.status = status
		weizoom_card.target_user_id = 0
		if card_remark and activated_to and department:
			weizoom_card.remark = card_remark
			weizoom_card.activated_to = activated_to
			weizoom_card.department = department
		weizoom_card.save()
		# 创建激活日志
		module_api.create_weizoom_card_log(request.user.id, -1, event_type, id, weizoom_card.money)
		response = create_response(200)
		# 创建操作日志
		WeizoomCardOperationLog.objects.create(card_id=id,operater_id=request.user.id,operater_name=request.user,operate_log=operate_log,remark=card_remark,activated_to=activated_to,department=department)
	except:
		response = create_response(500)
	return response.get_response()


@api(app='card', resource='batch_status', action='update')
@login_required
def update_batch_status(request):
	"""
	批量激活微众卡
	"""
	card_ids = request.POST.get('card_id', '')
	card_remark = request.POST['card_remark']
	activated_to = request.POST['activated_to']
	department = request.POST['department']
	if card_ids:
		card_ids = card_ids.split(',')
		activated_at = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
		cards = WeizoomCard.objects.filter(id__in=card_ids)

		cards.update(status=0, activated_at=activated_at, remark=card_remark, activated_to=activated_to,department=department,active_card_user_id=request.user.id)
		# 创建操作日志
		operation_logs=[]
		for card_id in card_ids:
			operation_logs.append(WeizoomCardOperationLog(card_id=card_id,operater_id=request.user.id,operater_name=request.user,operate_log=u'激活',remark=card_remark,activated_to=activated_to))
		WeizoomCardOperationLog.objects.bulk_create(operation_logs)
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
	card_remark = request.POST['card_remark']
	activated_to = request.POST['activated_to']
	department = request.POST['department']
	if card_ids:
		card_ids = card_ids.split(',')
		activated_at = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
		cards = WeizoomCard.objects.filter(id__in=card_ids)
		cards.update(status=3, remark=card_remark, activated_to=activated_to,department=department)

		# 创建操作日志
		operation_logs=[]
		for card_id in card_ids:
			operation_logs.append(WeizoomCardOperationLog(card_id=card_id,operater_id=request.user.id,operater_name=request.user,operate_log=u'停用',remark=card_remark,activated_to=activated_to))
		WeizoomCardOperationLog.objects.bulk_create(operation_logs)

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


@api(app='card', resource='card_expired_time', action='append')
@login_required
def append_card_expired_time(request):
	"""
	追加卡规则时间
	"""
	rule_id = int(request.POST.get('rule_id', 0))
	card_ids = request.POST.get('card_ids', '')
	card_append_time = request.POST.get('card_append_time', '')
	rule = WeizoomCardRule.objects.get(id=rule_id)
	valid_time_from = datetime.strftime(rule.valid_time_from, '%Y-%m-%d %H:%M:%S')
	valid_time_to = datetime.strftime(rule.valid_time_to, '%Y-%m-%d %H:%M:%S')
	if valid_time_from >('%s' %card_append_time):
		response = create_response(500)
	else:
		if card_ids:
			card_ids = card_ids.split(',')
			if ('%s' %card_append_time) > valid_time_to:
				WeizoomCard.objects.filter(id__in=card_ids).update(
					is_expired=False,
					expired_time = card_append_time
				)
			else:
				WeizoomCard.objects.filter(id__in=card_ids).update(
					expired_time = card_append_time
				)
		else:
			if ('%s' %card_append_time) > valid_time_to:
				WeizoomCard.objects.filter(weizoom_card_rule_id=rule_id).update(
					is_expired=False,
					expired_time = card_append_time
				)
			else:
				WeizoomCard.objects.filter(weizoom_card_rule_id=rule_id).update(
					expired_time = card_append_time
				)
			rule.valid_time_to = card_append_time
			rule.expired_time = card_append_time
			rule.save()
		response = create_response(200)
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

def _get_attr_value(filter_value):
	if filter_value == '-1':
		return -1
	try:
		for item in filter_value.split('|'):
			if item.split(':')[0] == 'cardAttr':
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