# -*- coding: utf-8 -*-
{% for resource in resources %}
{% if resource.need_export %}
import {{resource.lower_name}}
{% endif %}
{% endfor %}

__STRIPPER_TAG__
NAV = {
	'section': u'',
	'navs': [
		{% for resource in resources %}
		{% if resource.need_export %}
		{
			'name': "{{resource.lower_name}}",
			'title': "{{resource.lower_name}}",
			'url': '/apps/{{app_name}}/{{resource.lower_name}}/',
			'need_permissions': []
		},
		{% endif %}
		{% endfor %}
	]
}


__STRIPPER_TAG__
__STRIPPER_TAG__
########################################################################
# get_second_navs: 获得二级导航
########################################################################
def get_second_navs(request):
	if request.user.username == 'manager':
		second_navs = [NAV]
	else:
		# webapp_module_views.get_modules_page_second_navs(request)
		second_navs = [NAV]
	__STRIPPER_TAG__
	return second_navs


__STRIPPER_TAG__
__STRIPPER_TAG__
def get_link_targets(request):
	{% for resource in resources %}
	{% if resource.need_export %}
	pageinfo, datas = {{resource.lower_name}}.{{resource.class_name}}.get_datas(request)
	link_targets = []
	for data in datas:
		link_targets.append({
			"id": str(data.id),
			"name": data.name,
			"link": '/apps/weixin_prize/m_{{resource.item_lower_name}}/?webapp_owner_id=%d&id=%s' % (request.user.id, data.id),
			"isChecked": False,
			"created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S")
		})
	{% endif %}
	{% endfor %}

	return pageinfo, link_targets