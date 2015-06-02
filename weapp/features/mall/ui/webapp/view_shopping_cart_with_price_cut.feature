Feature: 添加参加满减活动的商品到购物车后，浏览购物车中的商品

Background:
	Given jobs登录系统
	And jobs已添加商品规格
		"""
		[{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 50
		}, {
			"name": "商品2",
			"price": 5
		}, {
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 20,
						"stock_type": "有限",
						"stocks": 2
					},
					"S": {
						"price": 30,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品4",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 9,
						"stock_type": "无限"
					}
				}   
			}
		}, {
			"name": "商品5",
			"price": 1
		}]	
		"""
	When jobs创建满减活动
		"""
		[{
			"name": "商品1满减",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"price_threshold": 100.0,
			"cut_money": 10.5
		}, {
			"name": "商品3满减",
			"start_date": "今天",
			"end_date": "2天后",
			"products": ["商品3", "商品2"],
			"price_threshold": 70.0,
			"cut_money": 10.0,
			"is_enable_cycle_mode": true
		}]
		"""
	And bill关注jobs的公众号


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 购买单个满减商品，不满足价格阈值
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 1,
			"total_price": 50.0,
			"product_groups": [{
				"promotion": {
					"type": "price_cut",
					"result": {
						"price": 100.0,
						"cut_money": 10.5
					}
				},
				"products": [{
					"name": "商品1",
					"price": 50.0,
					"count": 1
				}]
			}]
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 购买满减活动中的全部商品，金额大于满足价格阈值，并满足循环满减条件
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品2",
			"count": 14
		}, {
			"name": "商品3",
			"model": {
				"models":{
					"M": {
						"count": 2
					}
				}
			}
		}, {
			"name": "商品3",
			"model": {
				"models":{
					"S": {
						"count": 2
					}
				}
			}
		}, {
			"name": "商品5",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 19,
			"total_price": 151.0,
			"product_groups": [{
				"promotion": {
					"type": "price_cut",
					"result": {
						"price": 140,
						"cut_money": 20,
						"subtotal": 150.0
					}
				},
				"products": [{
					"name": "商品2",
					"price": 5.0,
					"count": 14
				}, {
					"name": "商品3",
					"model": "M",
					"price": 20.0,
					"count": 2
				}, {
					"name": "商品3",
					"model": "S",
					"price": 30.0,
					"count": 2
				}]
			}, {
				"promotion": null,
				"products": [{
					"name": "商品5",
					"price": 1.0,
					"count": 1
				}]
			}]
		}
		"""