# -*- coding: utf-8 -*-
from datetime import datetime
from core import paginator
from mall.promotion import models as promotion_models
from mall.promotion.models import CouponRule

NAV = {
	'section': u'',
	'navs': [
		{
			'name': "red_envelopes",
			'title': "分享红包",
			'url': '/apps/red_envelope/red_envelopes/',
			'need_permissions': []
		},
	]
}


########################################################################
# get_second_navs: 获得二级导航
########################################################################
def get_second_navs(request):
	if request.user.username == 'manager':
		second_navs = [NAV]
	else:
		# webapp_module_views.get_modules_page_second_navs(request)
		second_navs = [NAV]
	
	return second_navs


def get_link_targets(request):
	# pageinfo, datas = red_envelopes.Red_envelopes.get_datas(request)
	# link_targets = []
	# for data in datas:
	# 	link_targets.append({
	# 		"id": str(data.id),
	# 		"name": data.name,
	# 		"link": '/apps/red_envelope/m_red_envelope/?webapp_owner_id=%d&id=%s' % (request.user.id, data.id),
	# 		"isChecked": False,
	# 		"created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S")
	# 	})
	# return pageinfo, link_targets
	# 增加查询
	query = request.GET.get('query', None)
	count_per_page = int(request.GET.get('count_per_page', '10'))
	cur_page = int(request.GET.get('page', '1'))
	params = {'receive_method':1,'is_delete':False}
	if query:
		params['name__contains'] = query
	objects = promotion_models.RedEnvelopeRule.objects.filter(**params).order_by('-id')
	pageinfo, rules = paginator.paginate(objects, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	link_targets = []
	for object in objects:
		id2coupon_rule = dict([(coupon_rule.id, coupon_rule) for coupon_rule in
                                   CouponRule.objects.filter(id=object.coupon_rule_id)])
		if object.limit_time:
			data = {
				"id": object.id,
                "name": object.name,
				"limit_time": object.limit_time,
                "start_time": object.start_time.strftime("%Y-%m-%d %H:%M"),
                "end_time": object.end_time.strftime("%Y-%m-%d %H:%M"),
                "coupon_rule_name": id2coupon_rule[object.coupon_rule_id].name,
                "remained_count": id2coupon_rule[object.coupon_rule_id].remained_count,
				"link": './?module=market_tool:share_red_envelope&model=share_red_envelope&action=get&order_id=2&red_envelope_rule_id=%s&webapp_owner_id=%d&project_id=0' % (object.id,request.user.id)
            }
			link_targets.append(data)
		else:
			is_timeout = False if object.end_time > datetime.now() else True
			if not is_timeout:
				data = {
					"id": object.id,
                    "name": object.name,
					"limit_time": object.limit_time,
                    "start_time": object.start_time.strftime("%Y-%m-%d %H:%M"),
                    "end_time": object.end_time.strftime("%Y-%m-%d %H:%M"),
                    "coupon_rule_name": id2coupon_rule[object.coupon_rule_id].name,
                    "remained_count": id2coupon_rule[object.coupon_rule_id].remained_count,
					"link": './?module=market_tool:share_red_envelope&model=share_red_envelope&action=get&order_id=2&red_envelope_rule_id=%s&webapp_owner_id=%d&project_id=0' % (object.id,request.user.id)
                }
				link_targets.append(data)
	return pageinfo, link_targets
