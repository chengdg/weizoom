# -*- coding: utf-8 -*-
from apps.customerized_apps.event import events

NAV = {
	'section': u'',
	'navs': [
		{
			'name': "events",
			'title': "活动报名",
			'url': '/apps/event/events/',
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
		
	pageinfo, datas = events.events.get_datas(request)
	link_targets = []
	for data in datas:
		link_targets.append({
			"id": str(data.id),
			"name": data.name,
			"link": '/m/apps/event/m_event/?webapp_owner_id=%d&id=%s' % (request.user.id, data.id),
			"isChecked": True if str(data.id) == selected_id else False,
			"created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S")
		})
	return pageinfo, link_targets
