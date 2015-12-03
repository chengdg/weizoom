# -*- coding: utf-8 -*-
import datetime
import json
import signs
import models as app_models

NAV = {
	'section': u'',
	'navs': [
		{
			'name': "sign",
			'title': "签到",
			'url': '/apps/sign/sign/',
			'need_permissions': []
		},
	]
}


########################################################################
# get_second_navs: 获得二级导航
########################################################################
def get_second_navs(request):
	if request.manager.username == 'manager':
		second_navs = [NAV]
	else:
		# webapp_module_views.get_modules_page_second_navs(request)
		second_navs = [NAV]
	
	return second_navs


def get_link_targets(request):
	pageinfo, datas = signs.Signs.get_datas(request)
	link_targets = []
	for data in datas:
		link_targets.append({
			"id": str(data.id),
			"name": data.name,
			"link": '/m/apps/sign/m_sign/?webapp_owner_id=%d&id=%s' % (request.manager.id, data.id),
			"isChecked": False,
			"created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S")
		})
	return pageinfo, link_targets

def get_sing_fields_to_save(request):
	fields = request.POST.dict()
	fields['created_at'] = datetime.datetime.today()
	fields['owner_id'] = request.manager.id

	webapp_user = getattr(request, 'webapp_user', None)
	if webapp_user:
		fields['webapp_user_id'] = request.webapp_user.id

	member = getattr(request, 'member', None)
	if member:
		fields['member_id'] = request.member.id

	if 'prize_settings' in request.POST:
		fields['prize_settings'] = json.loads(fields['prize_settings'])

	if 'share' in request.POST:
		fields['share'] = json.loads(fields['share'])

	if 'reply' in request.POST:
		fields['reply'] = json.loads(fields['reply'])

	return fields

def get_sign_webapp_link(request):
	sign = app_models.Sign.objects.count()
	if sign > 0:
		return '/m/apps/sign/m_sign/?webapp_owner_id=%d' % request.manager.id
	return None
