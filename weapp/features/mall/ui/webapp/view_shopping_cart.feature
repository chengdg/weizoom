Feature: 添加商品到购物车后，浏览购物车中的商品
	bill将各种商品放入购物车后，能浏览商品信息

Background:
	Given jobs登录系统
	And jobs已添加商品规格
		'''
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "红色",
				"image": "/standard_static/test_resource_img/icon_color/icon_1.png"
			}, {
				"name": "黄色",
				"image": "/standard_static/test_resource_img/icon_color/icon_5.png"
			}, {
				"name": "蓝色",
				"image": "/standard_static/test_resource_img/icon_color/icon_9.png"
			}]
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}, {
				"name": "L"
			}]
		}]
		'''
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 3
		}, {
			"name": "商品2",
			"price": 5
		}, {
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"红色 S": {
						"price": 10.0,
						"stock_type": "有限",
						"stocks": 3
					},
					"黄色 M": {
						"price": 9.1,
						"stock_type": "无限"
					},
					"蓝色 M": {
						"price": 11.1,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}, {
			"name": "商品4",
			"price": 3
		}, {
			"name": "商品5",
			"price": 5
		}]	
		"""
	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}, {
			"name": "商品2限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品2"],
			"promotion_price": 2.1
		}, {
			"name": "商品3限时抢购",
			"start_date": "1天后",
			"end_date": "2天后",
			"products": ["商品3"],
			"promotion_price": 3.1
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 放入单种商品到购物车，商品参加限时抢购
	
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1"
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 1,
			"total_price": 11.5,
			"product_groups": [{
				"promotion": {
					"type": "flash_sale"
				},
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 1
				}]
			}]
		}
		"""
	When bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1",
			"count": 2
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 3,
			"total_price": 34.5,
			"product_groups": [{
				"promotion": {
					"type": "flash_sale"
				},
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 3
				}]
			}]
		}
		"""
	When tom访问jobs的webapp:ui
	Then tom能获得购物车:ui
		"""
		{
			"total_product_count": 0,
			"total_price": 0.0,
			"product_groups": []
		}
		"""	


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 放入多个商品到购物车
	jobs添加商品后
	1. bill能在webapp中将jobs添加的商品放入购物车
	2. 多次放入不同商品会增加购物车中商品的条数
	
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品4"
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 1,
			"total_price": 3.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品4",
					"price": 3,
					"count": 1
				}]
			}]
		}
		"""
	When bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品5"
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 2,
			"total_price": 8.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品4",
					"price": 3,
					"count": 1
				}]
			}, {
				"promotion": null,
				"products": [{
					"name": "商品5",
					"price": 5,
					"count": 1
				}]
			}]
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 放入同一种商品的不同规格到购物车
	jobs添加商品后
	1. 商品的不同规格会增加购物车中商品的条数
	
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品3",
			"model": "红色 S",
			"count": 1
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 1,
			"total_price": 10.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品3",
					"model": "红色 S",
					"price": 10.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品3",
			"model": "黄色 M",
			"count": 2
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 3,
			"total_price": 28.2,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品3",
					"model": "红色 S",
					"price": 10,
					"count": 1
				}]
			}, {
				"promotion": null,
				"products": [{
					"name": "商品3",
					"model": "黄色 M",
					"price": 9.1,
					"count": 2
				}]
			}]
		}
		"""