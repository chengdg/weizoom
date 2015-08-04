# -*- coding: utf-8 -*-

NAV = {
	'section': u'微站',
	'navs': [
		{% for nav in navs %}
		{
			'name': '{{ nav.value }}',
			'title': u'{{ nav.displayName }}',
			'url': '{{ nav.target }}',
		},
		{% endfor %}
	]
}