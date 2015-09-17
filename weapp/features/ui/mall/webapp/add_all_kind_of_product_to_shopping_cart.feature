# __edit__ : "新新8.26"
#1.添加活动(限时抢购,买赠,积分活动,普通商品)到购物车中
#相关活动的会员价添加到购物车已在相关活动中写了


Feature: 普通商品，促销商品到购物车中
	bill能在webapp中将jobs添加的"普通商品，普通商品有规格商品,促销商品(限时抢购,积分商品,买1赠1)"放入购物车

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
			"price": 100
		}, {
			"name": "商品2",
			"price": 200
		}, {
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 300,
						"stock_type": "无限"
					},
					"S": {
						"price": 300,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品4",
			"price":400
		}, {
			"name": "商品5",
			"price": 50
		}, {
			"name": "商品6",
			"price": 100
		}]	
		"""

	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"count_per_purchase": 2,
			"promotion_price": 10
		}]

		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "商品2买二赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品2",
			"premium_products": [{
				"name": "商品4",
				"count": 1
			}],
			"count": 2,
			"is_enable_cycle_mode": true
		}]
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品6积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品6"],
			"discount": 70,
			"discount_money": 70.0,
			"is_permanant_active": false
		}
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号


Scenario:1 放入多个商品到购物车
	#商品1是限时抢购活动，商品2是买赠活动赠商品4，商品3是多规格商品没有参加任何活动,商品5是普通无规格没有参加活动,商品6是积分活动
	jobs添加商品后
	1. bill能在webapp中将jobs添加的商品放入购物车
	2. tom的购物车不受bill操作的影响

	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		},{
			"name": "商品2",
			"count": 2
		},{
			"name": "商品3",
			"model": {
				"models":{
					"M": {
						"count": 1
					}
				}
			}
		}, {
			"name": "商品3",
			"model": {
				"models":{
					"S": {
						"count": 1
					}
				}
			}
		}, {
			"name": "商品5",
			"count": 1
		}, {
			"name": "商品6",
			"count": 1
		}]
		"""
	
	Then bill能获得购物车:ui
		"""
		{
			"product_groups": [{
				"promotion": {
					"type": "flash_sale",
					"result": {
						"saved_money": 90
					}
				},
				"can_use_promotion": true,
				"products": [{
					"name": "商品1",
					"price": 10,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "premium_sale",
					"result": {
						"premium_products": [{
							"name": "商品4",
							"premium_count": 1
						}]
					}
				},
				"can_use_promotion": true,
				"products": [{
					"name": "商品2",
					"price": 200,
					"count": 2
				}]
			}, {
				"products": [{
					"name": "商品3",
					"price": 300,
					"count": 1,
					"model": "M"
				}, {
					"name": "商品3",
					"price": 300,
					"count": 1,
					"model": "S"
				}]
			}, {
				"products": [{
					"name": "商品5",
					"price": 50,
					"count": 1
				}]
			}, {
				"products": [{
					"name": "商品6",
					"price": 100,
					"count": 1
				}]
			}],
			"invalid_products": []
		}
		"""
	
	When tom访问jobs的webapp
	Then tom能获得购物车:ui
		"""
		{
			"product_groups": [],
			"invalid_products": []
		}
		"""
	
