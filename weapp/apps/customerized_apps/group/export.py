# -*- coding: utf-8 -*-
import groups

NAV = {
	'section': u'',
	'navs': [
		{
			'name': "groups",
			'title': "团购",
			'url': '/apps/group/groups/',
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

	#增加查询
	query = request.GET.get('query',None)
	if query:
		request.GET = request.GET.copy()
		request.GET['group_name'] = query
	pageinfo, datas = groups.Groups.get_datas(request)
	link_targets = []
	for data in datas:
		link_targets.append({
			"id": data['id'],
			"name": data['name'],
			"link": '/m/apps/group/m_group/?webapp_owner_id=%d&id=%s' % (request.manager.id, data['id']),
			"isChecked": False,
			"created_at": data['created_at']
		})
	return pageinfo, link_targets
