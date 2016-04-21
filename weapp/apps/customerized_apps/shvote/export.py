# -*- coding: utf-8 -*-
import shvotes

NAV = {
	'section': u'',
	'navs': [
		{
			'name': "shvotes",
			'title': "高级投票",
			'url': '/apps/shvote/shvotes/',
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
	pageinfo, datas = shvotes.Shvotes.get_datas(request)
	link_targets = []
	for data in datas:
		link_targets.append({
			"id": str(data.id),
			"name": data.name,
			"link": '/m/apps/shvote/m_shvote/?webapp_owner_id=%d&id=%s' % (request.manager.id, data.id),
			"isChecked": False,
			"created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S")
		})
	return pageinfo, link_targets
