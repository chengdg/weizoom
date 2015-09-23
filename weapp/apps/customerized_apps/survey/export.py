# -*- coding: utf-8 -*-
from apps.customerized_apps.survey import surveies

NAV = {
	'section': u'',
	'navs': [
		{
			'name': "surveies",
			'title': "用户调研",
			'url': '/apps/survey/surveies/',
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
	selected_id = request.selected_id
	
	# 增加查询
	query = request.GET.get('query', None)
	if query:		
		request.GET = request.GET.copy()
		request.GET['name'] = query
		
	pageinfo, datas = surveies.surveies.get_datas(request)
	link_targets = []
	for data in datas:
		link_targets.append({
			"id": str(data.id),
			"name": data.name,
			"link": './m/apps/survey/m_survey/?webapp_owner_id=%d&id=%s' % (request.user.id, data.id),
			"isChecked": True if str(data.id) == selected_id else False,
			"created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S")
		})
	return pageinfo, link_targets
