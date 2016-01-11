# -*- coding:utf-8 -*-
from django import template


register = template.Library()


@register.inclusion_tag('single_chart.html')
def single_chart(id, json_url, width, height, show_sidebar='false', show_date_range='false', show_current_day='false'):
	return {
			'id': id,
			'show_sidebar': show_sidebar == 'true',
			'show_date_range': show_date_range == 'true',
			'show_current_day': show_current_day == 'true',
			'data_url': json_url, 
			'width': width, 
			'height': height
			}

@register.inclusion_tag('single_title_chart.html')
def single_title_chart(id, title, json_url, width, height, show_date_range='false', show_sidebar='false', sidebar_url=None, show_current_day='false'):
	return {
			'id': id,
	        'title': title,
			'show_sidebar': show_sidebar == 'true',
			'show_date_range': show_date_range == 'true',
			'show_current_day': show_current_day == 'true',
			'data_url': json_url,
	        'sidebar_url': sidebar_url,
			'width': width,
			'height': height
			}
	
#@register.inclusion_tag('single_popup_chart.html')
#def single_popup_chart(id, json_url, width, height, show_sidebar='false', show_date_range='false', show_current_day='false'):
#	return {
#			'id': id,
#			'show_sidebar': show_sidebar == 'true',
#			'show_date_range': show_date_range == 'true',
#			'show_current_day': show_current_day == 'true',
#			'data_url': json_url,
#			'width': width,
#			'height': height
#			}
#
#
#@register.inclusion_tag('combined_chart.html')
#def combined_chart(category, create_date, width, height, show_sidebar='false'):
#	return {
#			'id': category,
#			'category': category,
#			'func_name': category+'_statistics',
#			'create_date': create_date,
#			'width':width,
#			'height':height,
#			'show_sidebar':show_sidebar
#			}
#
#@register.inclusion_tag('single_chart.html')
#def top_n_line_chart(id, json_url, width, height):
#	return {
#			'id': id,
#			'show_sidebar': 'false',
#			'data_url': json_url,
#			'width': width,
#			'height': height
#			}