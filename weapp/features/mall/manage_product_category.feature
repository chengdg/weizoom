@func:webapp.modules.mall.views.update_productcategory
Feature: Manage Product Category
	Jobs能通过管理系统管理商城中的"商品分类列表"

Background:
	Given jobs登录系统
	When jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	When jobs已添加商品
		#东坡肘子(有分类，上架，无限库存，多轮播图), 叫花鸡(无分类，下架，有限库存，单轮播图)
		"""
		[{
			"name": "东坡肘子",
			"status": "待售",
			"category": "分类1,分类2",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"status": "待售",
			"category": "分类1",
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}, {
			"name": "水晶虾仁",
			"status": "待售",
			"category": "",
			"model": {
				"models": {
					"standard": {
						"price": 3.0
					}
				}
			}
		}]	
		"""

@mall @mall.product_category @mall2
Scenario: Jobs更新已存在的商品分类
	When jobs更新商品分类'分类1'为
		"""
		{
			"name": "分类1*"
		}	
		"""
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1*"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""

@mall @mall.product_category @mall2
Scenario: Jobs删除已存在的商品分类
	When jobs删除商品分类'分类2'
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类3"
		}]
		"""

@mall.product_category @mall @mall2
Scenario: 从分类中删除商品
	
	Given jobs登录系统
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1",
			"products": [{
				"name": "叫花鸡"
			}, {
				"name": "东坡肘子"
			}]
		}, {
			"name": "分类2",
			"products": [{
				"name": "东坡肘子"
			}]
		}, {
			"name": "分类3",
			"products": []
		}]
		"""
	When jobs从商品分类'分类1'中删除商品'东坡肘子'
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1",
			"products": [{
				"name": "叫花鸡"
			}]
		}, {
			"name": "分类2",
			"products": [{
				"name": "东坡肘子"
			}]
		}, {
			"name": "分类3",
			"products": []
		}]
		"""


@mall.product_category @mall @mall2
Scenario: 向分类中添加商品
	
	Given jobs登录系统
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1",
			"products": [{
				"name": "叫花鸡"
			}, {
				"name": "东坡肘子"
			}]
		}, {
			"name": "分类2",
			"products": [{
				"name": "东坡肘子"
			}]
		}, {
			"name": "分类3",
			"products": []
		}]
		"""
	Then jobs能获得商品分类'分类3'的可选商品集合为
		"""
		[{
			"name": "水晶虾仁",
			"display_price": 3.0,
			"status": "待售"
		}, {
			"name": "叫花鸡",
			"display_price": 12.0,
			"status": "待售"
		}, {
			"name": "东坡肘子",
			"display_price": 11.12,
			"status": "待售"
		}]
		"""
	And jobs能获得商品分类'分类2'的可选商品集合为
		"""
		[{
			"name": "水晶虾仁",
			"display_price": 3.0,
			"status": "待售"
		}, {
			"name": "叫花鸡",
			"display_price": 12.0,
			"status": "待售"
		}]
		"""
	And jobs能获得商品分类'分类1'的可选商品集合为
		"""
		[{
			"name": "水晶虾仁",
			"display_price": 3.0,
			"status": "待售"
		}]
		"""
	When jobs向商品分类'分类3'中添加商品
		"""
		["东坡肘子", "叫花鸡", "水晶虾仁"]
		"""
	When jobs向商品分类'分类2'中添加商品
		"""
		["水晶虾仁"]
		"""
	Then jobs能获得商品分类'分类3'的可选商品集合为
		"""
		[]
		"""
	And jobs能获得商品分类'分类2'的可选商品集合为
		"""
		[{
			"name": "叫花鸡",
			"display_price": 12.0,
			"status": "待售"
		}]
		"""
	And jobs能获得商品分类'分类1'的可选商品集合为
		"""
		[{
			"name": "水晶虾仁",
			"display_price": 3.0,
			"status": "待售"
		}]
		"""
