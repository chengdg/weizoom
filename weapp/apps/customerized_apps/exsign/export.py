# -*- coding: utf-8 -*-
import datetime
import json
import models as app_models

NAV = {
	'section': u'',
	'navs': [
		{
			'name': "exsign",
			'title': "专项签到",
			'url': '/apps/exsign/exsign/',
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

	return fields

def get_exsign_webapp_link(request):
	exsign = app_models.exSign.objects.count()
	if exsign > 0:
		return '/m/apps/exsign/m_exsign/?webapp_owner_id=%d' % request.manager.id
	return None
