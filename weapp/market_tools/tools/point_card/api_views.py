# -*- coding: utf-8 -*-

from core import apiview_util
from core.jsonresponse import JsonResponse, create_response
from core import paginator
from models import *

from django.contrib.auth.decorators import login_required

from modules.member.module_api import get_member_by_id_list


########################################################################
# get_records: 获取充值卡列表
########################################################################
@login_required
def get_records(request):
	sort_attr = request.GET.get('sort_attr', '-created_at')
	point_cards = PointCard.objects.filter(owner=request.user).order_by(sort_attr)
	point_card_rule_id2point_card_rule = dict([(rule.id, rule) for rule in PointCardRule.get_all_point_card_rules_list(request.user)])
	
	roles = []
	for id in point_card_rule_id2point_card_rule:
		cur_point_card = JsonResponse()
		cur_point_card.name = point_card_rule_id2point_card_rule[id].name
		cur_point_card.id = point_card_rule_id2point_card_rule[id].id
		roles.append(cur_point_card)
	
	member_ids = [c.member_id for c in point_cards]
	members = get_member_by_id_list(member_ids)
	member_id2member = dict([(m.id, m) for m in members])
	
	has_active_point_card = False
	
	#处理过滤
	filter_attr = request.GET.get('filter_attr', None)
	filter_value = int(request.GET.get('filter_value', -1))
	if filter_attr and (filter_value != -1):
		params = {filter_attr: filter_value}
		point_cards = point_cards.filter(**params)
	
	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, point_cards = paginator.paginate(point_cards, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	
	items = []
	for point_card in point_cards:
		cur_point_card = JsonResponse()
		cur_point_card.id = point_card.id
		cur_point_card.point_card_rule_name = point_card_rule_id2point_card_rule[point_card.point_card_rule_id].name
		if point_card.status == POINT_CARD_STATUS_UNUSED:
			has_active_point_card = True
		cur_member = JsonResponse()
		member_id = int(point_card.member_id)
		if member_id in member_id2member:
			member = member_id2member[member_id]
			cur_member.username_for_html = member.username_for_html
		else:
			member = ''
			cur_member.username_for_html = ''
		cur_point_card.member = cur_member
		cur_point_card.status = point_card.status
		cur_point_card.point_card_id = point_card.point_card_id
		cur_point_card.created_at = point_card.created_at.strftime("%Y-%m-%d")
		cur_point_card.password = point_card.password
		cur_point_card.point = int(point_card.point)
		items.append(cur_point_card)
	
	response = create_response(200)    
	data = JsonResponse()
	data.items = items
	data.has_active_point_card = has_active_point_card
	data.sortAttr = request.GET.get('sort_attr', '-created_at')
	response.data = data
	response.data.pageinfo = paginator.to_dict(pageinfo)
	response.data.roles = roles
	return response.get_response()


########################################################################
# create_point_card: 创建充值卡
########################################################################
@login_required
def create_point_card(request):
	type = int(request.POST.get('type', 1))
	if type==1:
		point_cards = _create_point_cards(request, False)
	else:
		point_card_id = request.POST.get('point_card_id').strip()
		point_card_rule_id = request.POST['rule_id']
		password = request.POST['password'].strip()
		point_card_rule = PointCardRule.objects.get(id=point_card_rule_id)
		point_cards = []
		if len(PointCard.objects.filter(point_card_id=point_card_id))>0:
			response = create_response(500)
			response.errMsg = u'该卡号己存在'
			return response.get_response()
		new_point_card = PointCard.objects.create(
			owner = request.user,
			point_card_id = point_card_id,
			point = point_card_rule.point,
			point_card_rule = point_card_rule,
			password = password,
			is_manual_generated = True
		)
		point_cards.append(new_point_card)
	items = []
	for point_card in point_cards:
		items.append({
			'point_card_id': point_card.point_card_id,
			'point': point_card.point,
			'created_at': point_card.created_at.strftime("%Y-%m-%d")
		})

	response = create_response(200)
	response.data = {
		'items': items
	}
	return response.get_response()


########################################################################
# _create_point_cards: 创建充值卡
########################################################################
def _create_point_cards(request, is_manual_generated=False):
	owner = request.user
	count = int(request.POST.get('count', 0))
	point_card_rule_id = request.POST['rule_id']
	point_card_rule = PointCardRule.objects.get(id=point_card_rule_id)

	#创建充值卡
	point_cards = []
	i = 1
	if count > 0:
		while True:
			point_card_id = _create_random_point_card_id(point_card_rule.prefix)
			try:
				new_point_card = PointCard.objects.create(
					owner = owner,
					point_card_id = point_card_id,
					password = _create_random_point_card_password(),
					point = point_card_rule.point,
					point_card_rule = point_card_rule,
					is_manual_generated = is_manual_generated
				)
				point_cards.append(new_point_card)
				if i >= count :
					break
				i += 1
			except:
				continue
	return point_cards


########################################################################
# _create_random_point_card_id: 创建充值卡
########################################################################
def _create_random_point_card_id(point_card_rule_prefix):
	random_args_value = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	while True:
		id = '%07s%s' % (point_card_rule_prefix, ''.join(random.sample(random_args_value, 4)))
		if len(PointCard.objects.filter(point_card_id=id))==0:
			return id
		

########################################################################
# _create_random_point_card_password: 创建充值卡密码
########################################################################
def _create_random_point_card_password():
	random_args_value = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	ids = set()

	password = '%s' % (''.join(random.sample(random_args_value, 4)))
	return password

########################################################################
# discard_point_cards: 作废充值卡
########################################################################
@login_required
def discard_point_cards(request):
	ids = request.POST['point_card_ids'].split(',')
	PointCard.objects.filter(id__in=ids).update(status=2)
	response = create_response(200)
	return response.get_response()


########################################################################
# deleted_disabled_point_cards: 删除作废充值卡
########################################################################
@login_required
def deleted_disabled_point_cards(request):
	PointCard.objects.filter(owner=request.user, status=2).delete()
	response = create_response(200)
	return response.get_response()


def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)