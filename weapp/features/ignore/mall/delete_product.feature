#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
Feature: 删除商品
	Jobs能通过管理系统删除商品

Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"category": "分类1"
		}, {
			"name": "商品2",
			"category": "分类1"
		}, {
			"name": "商品3",
			"category": "分类1"
		}, {
			"name": "商品4",
			"category": "分类2"
		}]	
		"""

@ui @ui-mall @ui-mall.product
Scenario: 删除商品
	Jobs添加一组商品后，能删除单个商品。
	删除后：
		1. 排序不会被破坏
		2. 并且商品所属的分类中的商品统计数会改变

	Given jobs登录系统:ui
	Then jobs能获取商品列表:ui
		"""
		[{"name":"商品4"}, {"name":"商品3"}, {"name":"商品2"}, {"name":"商品1"}]
		"""
	And jobs能获取商品分类列表:ui
		"""
		[{"name":"分类3", "product_count":0}, {"name":"分类2", "product_count":1}, {"name":"分类1", "product_count":3}]
		"""
	When jobs删除后台商品'商品3':ui
	Then jobs能获取商品列表:ui
		"""
		[{"name":"商品4"}, {"name":"商品2"}, {"name":"商品1"}]
		"""
	And jobs能获取商品分类列表:ui
		"""
		[{"name":"分类3", "product_count":0}, {"name":"分类2", "product_count":1}, {"name":"分类1", "product_count":2}]
		"""
	When jobs删除后台商品'商品2':ui
	Then jobs能获取商品列表:ui
		"""
		[{"name":"商品4"}, {"name":"商品1"}]
		"""
	And jobs能获取商品分类列表:ui
		"""
		[{"name":"分类3", "product_count":0}, {"name":"分类2", "product_count":1}, {"name":"分类1", "product_count":1}]
		"""
	When jobs删除后台商品'商品1':ui
	When jobs删除后台商品'商品4':ui
	Then jobs能获取商品列表:ui
		"""
		[]
		"""
	And jobs能获取商品分类列表:ui
		"""
		[{"name":"分类3", "product_count":0}, {"name":"分类2", "product_count":0}, {"name":"分类1", "product_count":0}]
		"""