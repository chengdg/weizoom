Feature: 添加商品分类
	Jobs能通过管理系统为管理商城添加的"商品分类"

@ui-mall.product_category @ui-mall @ui
Scenario: 添加商品分类
	Jobs添加一组"商品分类"后，"商品分类列表"会按照添加的顺序倒序排列

	Given jobs登录系统:ui
	When jobs添加商品分类:ui
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	Then jobs能获取商品分类列表:ui
		"""
		[{
			"name": "分类3"
		}, {
			"name": "分类2"
		}, {
			"name": "分类1"
		}]
		"""
	Given bill登录系统:ui
	Then bill能获取商品分类列表:ui
		"""
		[]
		"""

Scenario: 添加商品时选择分类，能在分类中看到该商品
	Jobs添加一组"商品分类"后，"商品分类列表"会按照添加的顺序倒序排列

	Given jobs登录系统:ui
	When jobs已添加商品分类:ui
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	Given jobs已添加商品:ui
		#东坡肘子(有分类，上架，无限库存，多轮播图), 叫花鸡(无分类，下架，有限库存，单轮播图)
		"""
		[{
			"name": "东坡肘子",
			"status": "待售",
			"categories": "分类1,分类2",
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
			"categories": "分类1",
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
			"categories": "",
			"model": {
				"models": {
					"standard": {
						"price": 3.0
					}
				}
			}
		}]
		"""
	Then jobs能获取商品分类列表:ui
		"""
		[{
			"name": "分类1",
			"products": [{
				"name": "叫花鸡",
				"display_price": 12.0,
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"display_price": 11.12,
				"status": "待售"
			}]
		}, {
			"name": "分类2",
			"products": [{
				"name": "东坡肘子",
				"display_price": 11.12,
				"status": "待售"
			}]
		}, {
			"name": "分类3",
			"products": []
		}]
		"""
