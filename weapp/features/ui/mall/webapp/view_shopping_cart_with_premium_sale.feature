# __edit__ : "新新8.26"

Feature:  参加买赠活动的商品到购物车后，浏览购物车中的商品
"""

该feature中需要修改和补充,涉及到场景如下
#赠品只允许为无规格商品
#赠品不足时,不在购物车验证,在订单页提示库存不足
1.无规格买赠添加到购物车中,浏览购物车中的商品
2.有规格买赠添加到购物车中,浏览购物车中的商品
#不同规格同个商品分别添加到购物车,会根据购买基数显示赠品
3.购物车数量小于购买基数,不显示赠品
#购物数量等于大于购买基数时,显示赠品
4.循环买赠,购物车数量小于购买基数,不显示赠品
#循环买赠,购物车数量增加减少时,根据购买基数显示赠品
6.购物车数量大于库存,提示库存不足,不显示赠品
#操作到购物车数量小于库存时,需点击选中该商品,才会出现赠品
7.赠品与主商品是同一商品,购物车数量大于该商品库存,提示库存不足,不显示赠品
8.买赠活动会员价添加到购物车

"""

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
			"price": 30
		}, {
			"name": "商品2",
			"price": 5
		}, {
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 7,
						"stock_type": "有限",
						"stocks": 2
					},
					"S": {
						"price": 8,
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
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 7,
						"stock_type": "有限",
						"stocks": 2
					},
					"S": {
						"price": 8,
						"stock_type": "无限"
					}
				}
			}
		}]	
		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "商品1买二赠三",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"premium_products": [{
				"name": "商品2",
				"count": 1
			}, {
				"name": "商品3",
				"count": 2
			}],
			"count": 2,
			"is_enable_cycle_mode": true
		}, {
			"name": "商品2买一赠一",
			"start_date": "今天",
			"end_date": "2天后",
			"product_name": "商品2",
			"premium_products": [{
				"name": "商品4",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": false
		}, {
			"name": "商品3买一赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品3",
			"premium_products": [{
				"name": "商品4",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": false
		}, {
			"name": "商品5买一赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品5",
			"premium_products": [{
				"name": "商品4",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": true
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号



Scenario: 1 放入1个商品到购物车，商品不满足买赠的购买基数
	bill将商品放入到购物车后
	1. bill能看到购物车中商品的详情
	
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1",
			"count": 1
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"product_groups": [{
				"promotion": null,
				"can_use_promotion": false,
				"products": [{
					"name": "商品1",
					"price": 30.0,
					"count": 1
				}]
			}],
			"invalid_products": []
		}
		"""



Scenario: 2 放入1个商品到购物车，商品数量等于买赠的购买基数
	bill将商品放入到购物车后
	1. bill能看到购物车中商品的详情
	
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1",
			"count": 2
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"product_groups": [{
				"promotion": {
					"type": "premium_sale",
					"result": {
						"premium_products": [{
							"name": "商品2",
							"premium_count": 1
						}, {
							"name": "商品3",
							"premium_count": 2
						}]
					}
				},
				"can_use_promotion": true,
				"products": [{
					"name": "商品1",
					"price": 30.0,
					"count": 2
				}]
			}],
			"invalid_products": []
		}
		"""



Scenario: 3 放入多个商品到购物车，商品数量大于买赠的购买基数，并满足循环买赠
	bill将商品放入到购物车后
	1. bill能看到购物车中商品的详情
	
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1",
			"count": 5
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"product_groups": [{
				"promotion": {
					"type": "premium_sale",
					"result": {
						"premium_products": [{
							"name": "商品2",
							"premium_count": 2
						}, {
							"name": "商品3",
							"premium_count": 4
						}]
					}
				},
				"can_use_promotion": true,
				"products": [{
					"name": "商品1",
					"price": 30.0,
					"count": 5
				}]
			}],
			"invalid_products": []
		}
		"""



Scenario: 4 放入多个商品到购物车，商品数量大于买赠的购买基数，但循环买赠没启用
	bill将商品放入到购物车后
	1. bill能看到购物车中商品的详情
	
	
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品2",
			"count": 3
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"product_groups": [{
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
					"price": 5.0,
					"count": 3
				}]
			}],
			"invalid_products": []
		}
		"""



Scenario: 5放入多规格商品到购物车
	
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品5",
			"model": {
				"models":{
					"M": {
						"count": 1
					}
				}
			}
		}, {
			"name": "商品5",
			"model": {
				"models":{
					"S": {
						"count": 2
					}
				}
			}
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"product_groups": [{
				"promotion": {
					"type": "premium_sale",
					"result": {
						"premium_products": [{
							"name": "商品4",
							"premium_count": 3
						}]
					}
				},
				"can_use_promotion": true,
				"products": [{
					"name": "商品5",
					"model": "M",
					"price": 7.0,
					"count": 1
				}, {
					"name": "商品5",
					"model": "S",
					"price": 8.0,
					"count": 2
				}]
			}],
			"invalid_products": []
		}
		"""


Scenario: 6新建买赠活动，买一赠一，买商品6赠 商品6，循环买赠
	
	Given jobs登录系统
	And jobs已添加商品
	"""
		[{
			"name": "商品6",
			"price": 100.00
		}]
	"""
	When jobs创建买赠活动
	"""
		[{
			"name": "商品6买1赠1",
			"start_date": "1天前",
			"end_date": "3天后",
			"product_name": "商品6",
			"premium_products": [{
				"name": "商品6",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": true
		}]
	"""
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品6",
			"count": 3
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"product_groups": [{
				"promotion": {
					"type": "premium_sale",
					"result": {
						"premium_products": [{
							"name": "商品6",
							"premium_count": 3
						}]
					}
				},
				"can_use_promotion": true,
				"products": [{
					"name": "商品6",
					"price": 100.0,
					"count": 3
				}]
			}],
			"invalid_products": []
		}
		"""
Scenario: 7买赠活动会员价添加到购物车
	
	Given jobs登录系统
	And jobs已添加商品
	"""
		[{
			"name": "商品7",
			"is_member_product": "on",
			"price": 100.00
		}]
	"""
	When jobs创建买赠活动
	"""
		[{
			"name": "商品7买1赠1",
			"start_date": "1天前",
			"end_date": "3天后",
			"product_name": "商品7",
			"premium_products": [{
				"name": "商品7",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": true
		}]
	"""
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品7",
			"count": 1
		}]
		"""
	Then bill能获得购物车:ui
		"""
		{
			"product_groups": [{
				"promotion": {
					"type": "premium_sale",
					"result": {
						"premium_products": [{
							"name": "商品7",
							"premium_count": 1
						}]
					}
				},
				"can_use_promotion": true,
				"products": [{
					"name": "商品7",
					"price": 100.0,
					"count": 1
				}]
			}],
			"invalid_products": []
		}
		"""