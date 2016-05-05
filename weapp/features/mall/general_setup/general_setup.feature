# watcher: fengxuejing@weizoom.com, benchi@weizoom.com
# __author__ : "冯雪静"

Feature: 修改通用设置
	"""
	jobs通过管理系统在商城修改通用设置
		1.商品销量
		2.商品排序
		3.商品搜索框
		4.购物车
	"""

@mall2 @eugene @mall_config
Scenario:1 修改通用设置
	jobs修改"通用设置"
	1.商品销量
	2.商品排序
	3.商品搜索框
	4.购物车


	Given jobs登录系统
	When jobs'修改'通用设置
		"""
		{
			"product_sales": "开启",
			"product_sort": "开启",
			"product_search": "开启",
			"shopping_cart": "开启"
		}
		"""
	Then jobs获得通用设置
		"""
		{
			"product_sales": "开启",
			"product_sort": "开启",
			"product_search": "开启",
			"shopping_cart": "开启"
		}
		"""
	When jobs'修改'通用设置
		"""
		{
			"product_sales": "关闭",
			"product_sort": "关闭",
			"product_search": "关闭",
			"shopping_cart": "关闭"
		}
		"""
	Then jobs获得通用设置
		"""
		{
			"product_sales": "关闭",
			"product_sort": "关闭",
			"product_search": "关闭",
			"shopping_cart": "关闭"
		}
		"""
	When jobs'修改'通用设置
		"""
		{
			"product_sales": "开启",
			"product_sort": "开启",
			"product_search": "关闭",
			"shopping_cart": "关闭"
		}
		"""
	Then jobs获得通用设置
		"""
		{
			"product_sales": "开启",
			"product_sort": "开启",
			"product_search": "关闭",
			"shopping_cart": "关闭"
		}
		"""




