# -*- coding: utf-8 -*-
import test1s

NAV = {
	'section': u'',
	'navs': [
		{
			'name': "test1s",
			'title': "test1s",
			'url': '/apps/test1/test1s/',
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
	pageinfo, datas = test1s.test1s.get_datas(request)
	link_targets = []
	for data in datas:
		link_targets.append({
			"id": str(data.id),
			"name": data.name,
			"link": '/apps/weixin_prize/m_test1/?webapp_owner_id=%d&id=%s' % (request.user.id, data.id),
			"isChecked": False,
			"created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S")
		})
	return pageinfo, link_targets
