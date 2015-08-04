# -*- coding: utf-8 -*-

__author__ = 'jiangzhe'

from django import template

from weshop import settings

register = template.Library()

@register.filter
def weshop_price(original_price, request=None):
	#add by bert in 2.2 
	return original_price
	# try:
	# 	original_price = float(original_price)
	# except:
	# 	pass

	# if request and (not hasattr(request, 'not_weshop_product') or not request.not_weshop_product):
	# 	return '%.0f' % original_price
	# if isinstance(original_price, float):
	# 	return '%.0f' % (float(original_price) * settings.WEIZOOM_PRICE)
	# elif original_price.find('-') >= 0:
	# 	original_price = original_price.split('-')
	# 	if len(original_price) == 2 and original_price[0].replace('.','').isdigit() \
	# 		and original_price[1].replace('.','').isdigit():
	# 		return '%.0f-%.0f' % (float(original_price[0]) * settings.WEIZOOM_PRICE, \
	# 			float(original_price[1]) * settings.WEIZOOM_PRICE)
	# return u'暂无报价'


@register.filter
def settings_price(str):
	return settings.WEIZOOM_PRICE