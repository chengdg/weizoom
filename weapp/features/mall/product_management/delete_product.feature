@func:webapp.modules.mall.views.update_product
Feature: Delete Product
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
			"categories": "分类1,分类2"
		}, {
			"name": "商品2",
			"categories": "分类1,分类2"
		}, {
			"name": "商品3",
			"categories": "分类1"
		}, {
			"name": "商品4",
			"categories": "分类2"
		}]
		"""

@mall2 @mall.product
Scenario: 删除商品
	Jobs添加一组商品后，能删除单个商品。
	删除后：
		1. 排序不会被破坏
		2. 并且商品所属的分类中的商品统计数会改变

	Then jobs能获取商品列表
		"""
		[{"name":"商品4"}, {"name":"商品3"}, {"name":"商品2"}, {"name":"商品1"}]
		"""
	And jobs能获取商品分类列表
		"""
		[
		{
			"name":"分类1",
			"products":
			[
				{"name": "商品3"},
				{"name": "商品2"},
				{"name": "商品1"}
			]
		}, {
			"name":"分类2",
			"products": [
				{"name": "商品4"},
				{"name": "商品2"},
				{"name": "商品1"}
			]
		}, {
			"name":"分类3",
			"products":[]
		}]
		"""
	When jobs-永久删除商品'商品3'
	Then jobs能获取商品列表
		"""
		[{"name":"商品4"}, {"name":"商品2"}, {"name":"商品1"}]
		"""
	And jobs能获取商品分类列表
		"""
		[
			{
				"name":"分类1",
				"products":[
					{"name": "商品2"},
					{"name": "商品1"}
				]
			},
			{
				"name":"分类2",
				"products": [
					{"name": "商品4"},
					{"name": "商品2"},
					{"name": "商品1"}
				]
			},
			{
				"name":"分类3",
				"products": []
			}
		]
		"""
	When jobs-永久删除商品'商品2'
	Then jobs能获取商品列表
		"""
		[{"name":"商品4"}, {"name":"商品1"}]
		"""
	And jobs能获取商品分类列表
		"""
		[
		{
			"name":"分类1",
			"products":[
					{"name": "商品1"}
				]
		},
		{
			"name":"分类2",
			"products": [
					{"name": "商品4"},
					{"name": "商品1"}
				]
		},
		{
			"name":"分类3",
			"products": []
		}]
		"""
	When jobs-永久删除商品'商品1'
	When jobs-永久删除商品'商品4'
	Then jobs能获取商品列表
		"""
		[]
		"""
	And jobs能获取商品分类列表
		"""
		[{
			"name":"分类1",
			"products": []
		},
		{
			"name":"分类2",
			"products": []
		},
		{
			"name":"分类3",
			"products": []
		}]
		"""