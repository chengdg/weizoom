# watcher: fengxuejing@weizoom.com, benchi@weizoom.com
# __author__ : "冯雪静"

Feature: 设置搜索商品功能
	"""
	jobs通过管理系统在商城中添加“搜索商品”功能
	"""

Background:
	Given jobs登录系统
	And bill关注jobs的公众号


Scenario:1 设置商品搜索框
	jobs开启“商品搜索框”
	jobs关闭“商品搜索框”

	Given jobs登录系统
	When jobs'开启'商品搜索框
	Then jobs获得商品搜索框
		"""
		{
			"status": "开启"
		}
		"""
	When bill访问jobs的webapp
	Then bill获得webapp商品搜索框
		"""
		{
			"status": "开启"
		}
		"""
	Given jobs登录系统
	When jobs'关闭'商品搜索框
	Then jobs获得商品搜索框
		"""
		{
			"status": "关闭"
		}
		"""
	When bill访问jobs的webapp
	Then bill获得webapp商品搜索框
		"""
		{
			"status": "关闭"
		}
		"""




