# -*- coding: utf-8 -*-
"""
商品分类相关
"""

from core import api_resource
from wapi.decorators import param_required

#from mall import models as mall_models
#from product_category import ProductCategory
from dummy_utils import DummyUserProfile
from cache import webapp_cache
from wapi import wapi_utils

class ProductsCategories(api_resource.ApiResource):
	"""
	获取商品分类列表

	举例：`http://dev.weapp.com/wapi/mall/products_categories/?webapp_id=3211&uid=33&is_access_weizoom_mall=false`
	"""
	app = 'mall'
	resource = 'products_categories'

	@param_required(['oid', 'wid'])
	def get(args):
		"""
		获取指定webapp_id的全部商品的分类列表

		返回结果举例：
		```
			data: [{
				id: 7,
				name: "分类1"
			}, {
				id: 8,
				name: "分类2"
			}, {
				id: 9,
				name: "分类3"
			}],		
		```

		@see 参考request_util.py中的
		```
			# get_webapp_product_categories() 调用 get_webapp_products_from_db()
			product_categories = webapp_cache.get_webapp_product_categories(request.user_profile, request.is_access_weizoom_mall)
		```
		"""
		owner_id = args['oid']
		webapp_id = args['wid']
		#webapp_id = wapi_utils.get_webapp_id_via_oid(owner_id)
		is_access_weizoom_mall = args.get('is_access_weizoom_mall', False)

		# 伪造一个UserProfile，便于传递参数
		user_profile = DummyUserProfile(webapp_id, owner_id)

		#product = mall_models.Product.objects.get(id=args['id'])

		# 通过缓存获取数据
		#product_categories = webapp_cache.get_webapp_product_categories(user_profile, is_access_weizoom_mall)
		func = webapp_cache.get_webapp_products_from_db(user_profile, is_access_weizoom_mall)
		data = func()
		return data['value']['categories']
