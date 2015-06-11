# -*- coding: utf-8 -*-

__author__ = 'jz'


from core.jsonresponse import create_response

from apps.module_api import get_app_link_url

from mall.models import *
from mall import module_api

########################################################################
# get_link_targets: 获取可链接的目标
########################################################################
def get_link_targets(request):
	response = create_response(200)

	workspace_template_info = 'workspace_id=mall&webapp_owner_id=%d' % request.workspace.owner_id
	has_data_category_filter = (request.GET.get('data_category_filter', None) != None)

	#获得category集合
	if has_data_category_filter:
		categories = []
	else:
		categories = [{'text': u'全部', 'value': get_app_link_url(request, 'weshop', 'mall', 'products', 'list', 'category_id=0')}]

	for category in ProductCategory.objects.filter(owner=request.user):
		categories.append({
			'text': category.name, 
			'value': get_app_link_url(request, 'weshop', 'mall', 'products', 'list', 'category_id=%d' % category.id),
			'meta': {
				'id': category.id,
				'name': category.name,
				'type': 'product_category'
			}
		})

	if not has_data_category_filter:
		#获得product集合
		products = []
		#获得本商户的商品
		temp_products = list(Product.objects.filter(owner=request.user, is_deleted=False, type='object'))
		if request.user.is_weizoom_mall:
			#获取微众商城中其他商户的商品
			other_mall_products,other_mall_product_ids = module_api.get_verified_weizoom_mall_partner_products_and_ids(request.user_profile.webapp_id)
			#合并商品
			temp_products.extend(other_mall_products)
		temp_products.sort(lambda x,y: cmp(y.display_index, x.display_index))

		Product.fill_display_price(temp_products)
		for product in temp_products:
			products.append({
				'text': product.name, 
				'value': get_app_link_url(request, 'weshop', 'mall', 'product', 'get', 'rid=%d' % product.id),
				'meta': {
					'pic_url': product.thumbnails_url,
					'name': product.name,
					'price': product.display_price,
					'id': product.id
				}
			})

		response.data = [
			{
				'name': u'商品分类',
				'data': categories
			}, {
				'name': u'商品',
				'data': products
			}, {
				'name': u'页面',
				'data': [{
					'text': u'活动测试页面',
					'value': u'/static/weshop.html?1='
				}]
			}
		]
	else:
		response.data = [
			{
				'name': u'商品分类',
				'data': categories
			}
		]
	return response.get_response()
