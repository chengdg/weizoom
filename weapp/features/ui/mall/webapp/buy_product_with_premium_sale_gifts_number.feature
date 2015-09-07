 # __edit__ : "王丽"

 Feature: 购买买赠活动的商品，手机端订单可以看到买赠商品的数量
"""
	购买买赠活动的商品，在手机端的"待付款"、"待发货"、"待收货"、"待评价"中的订单，订单详情可以展示赠品的数量
"""

Background:
	Given jobs登录系统

@promotion @promotionPremium @order @allOrder
Scenario:1 购买买赠活动的商品，在手机端的"待付款"、"待发货"、"待收货"、"待评价"中的订单，订单详情可以展示赠品的数量

	Given jobs登录系统
	And marry1关注jobs的公众账号

	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品赠品",
			"is_member_product": "on",
			"model": {
				"models": {
					"standard": {
						"price": 10.00,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		},{
			"name": "商品6",
			"is_member_product": "on",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		}]
		"""
	When jobs更新"marry1"的会员等级
		"""
		{
			"name":"marry2",
			"member_rank":"铜牌会员"
		}
		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "商品6买一赠二",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品6"],
			"premium_products": [{
				"name": "商品赠品",
				"count": 2
			}],
			"count": 1,
			"member_grade":"金牌会员",
			"is_enable_cycle_mode": true
		}]
		"""

	#创建"待付款"订单
		When marry1访问jobs的webapp
		And marry1加入jobs的商品到购物车
			"""
			[{
				"name": "商品6",
				"count": 1
			}]
			"""
		When marry1访问jobs的webapp:ui
		When marry1从购物车发起购买操作:ui
		Then marry1获得待编辑订单:ui
			"""
			{
				"price_info": {
					"final_price": 100.0,
					"product_price": 100.0,
					"promotion_money": 0.0,
					"postage": 0.00
				},
				"product_groups": [{
					"promotion": {
						"type": "premium_sale",
						"result": {
							"premium_products": [{
								"name": "商品赠品",
								"count": 2,
								"stock_info": ""
							}]
						}
					},
					"subtotal": {
						"count": 3,
						"money": 100.0
					},
					"products": [{
						"name": "商品6",
						"price": 100.0,
						"count": 1
					}]
				}]
			}
			"""
		When marry1使用'微信支付'提交订单未支付:ui

	#创建"待发货"订单
		When marry1访问jobs的webapp
		And marry1加入jobs的商品到购物车
			"""
			[{
				"name": "商品6",
				"count": 1
			}]
			"""
		When marry1访问jobs的webapp:ui
		When marry1从购物车发起购买操作:ui
		Then marry1获得待编辑订单:ui
			"""
			{
				"price_info": {
					"final_price": 100.0,
					"product_price": 100.0,
					"promotion_money": 0.0,
					"postage": 0.00
				},
				"product_groups": [{
					"promotion": {
						"type": "premium_sale",
						"result": {
							"premium_products": [{
								"name": "商品赠品",
								"count": 2,
								"stock_info": ""
							}]
						}
					},
					"subtotal": {
						"count": 3,
						"money": 100.0
					},
					"products": [{
						"name": "商品6",
						"price": 100.0,
						"count": 1
					}]
				}]
			}
			"""
		When marry1使用'货到付款'购买订单中的商品:ui

	#创建"待收货"订单
		When marry1访问jobs的webapp
		And marry1加入jobs的商品到购物车
			"""
			[{
				"name": "商品6",
				"count": 2
			}]
			"""
		When marry1访问jobs的webapp:ui
		When marry1从购物车发起购买操作:ui
		Then marry1获得待编辑订单:ui
			"""
			{
				"price_info": {
					"final_price": 100.0,
					"product_price": 100.0,
					"promotion_money": 0.0,
					"postage": 0.00
				},
				"product_groups": [{
					"promotion": {
						"type": "premium_sale",
						"result": {
							"premium_products": [{
								"name": "商品赠品",
								"count": 4,
								"stock_info": ""
							}]
						}
					},
					"subtotal": {
						"count": 6,
						"money": 200.0
					},
					"products": [{
						"name": "商品6",
						"price": 100.0,
						"count": 2
					}]
				}]
			}
			"""
		When marry1使用'货到付款'购买订单中的商品:ui

		When jobs登录系统
		When jobs订单发货
			"""
			[{
				"product_groups": [{
					"promotion": {
						"type": "premium_sale",
						"result": {
							"premium_products": [{
								"name": "商品赠品",
								"count": 4,
								"stock_info": ""
							}]
						}
					},
					"products": [{
						"name": "商品6",
						"price": 100.0,
						"count": 2
					}]
				}],
				"deliver_goods":"是"
			}]
			"""

	#创建"待评价"订单
		When marry1访问jobs的webapp
		And marry1加入jobs的商品到购物车
			"""
			[{
				"name": "商品6",
				"count": 3
			}]
			"""
		When marry1访问jobs的webapp:ui
		When marry1从购物车发起购买操作:ui
		Then marry1获得待编辑订单:ui
			"""
			{
				"price_info": {
					"final_price": 100.0,
					"product_price": 100.0,
					"promotion_money": 0.0,
					"postage": 0.00
				},
				"product_groups": [{
					"promotion": {
						"type": "premium_sale",
						"result": {
							"premium_products": [{
								"name": "商品赠品",
								"count": 6,
								"stock_info": ""
							}]
						}
					},
					"subtotal": {
						"count": 9,
						"money": 300.0
					},
					"products": [{
						"name": "商品6",
						"price": 100.0,
						"count": 3
					}]
				}]
			}
			"""
		When marry1使用'货到付款'购买订单中的商品:ui

		When jobs登录系统
		When jobs订单发货
			"""
			[{
				"product_groups": [{
					"promotion": {
						"type": "premium_sale",
						"result": {
							"premium_products": [{
								"name": "商品赠品",
								"count": 6,
								"stock_info": ""
							}]
						}
					},
					"products": [{
						"name": "商品6",
						"price": 100.0,
						"count": 3
					}]
				}],
				"deliver_goods":"是"
			}]
			"""
		When jobs订单完成
			"""
			[{
				"product_groups": [{
					"promotion": {
						"type": "premium_sale",
						"result": {
							"premium_products": [{
								"name": "商品赠品",
								"count": 6,
								"stock_info": ""
							}]
						}
					},
					"products": [{
						"name": "商品6",
						"price": 100.0,
						"count": 3
					}]
				}],
				"order_complete":"是"
			}]
			"""

	#校验赠品数量

		#查看"待付款"订单详情
			Then marry1查看待付款订单详情
				"""
				[{
					"premium_products": [{
						"name": "商品赠品",
						"count": 2
						}],
					"products": [{
							"name": "商品6",
							"price": 100.0,
							"count": 1
						}],
					"final_price":100.0
				}]
				"""

		#查看"待发货"订单详情
			Then marry1查看"待发货"订单详情
				"""
				[{
					"premium_products": [{
						"name": "商品赠品",
						"count": 2
						}],
					"products": [{
							"name": "商品6",
							"price": 100.0,
							"count": 1
						}],
					"final_price":100.0
				}]
				"""

		#查看"待收货"订单详情
			Then marry1查看"待收货"订单详情
				"""
				[{
					"premium_products": [{
						"name": "商品赠品",
						"count": 4
						}],
					"products": [{
							"name": "商品6",
							"price": 100.0,
							"count": 2
						}],
					"final_price":200.0
				}]
				"""

		#查看"待评价"订单详情
			Then marry1查看"待收货"订单详情
				"""
				[{
					"premium_products": [{
						"name": "商品赠品",
						"count": 6
						}],
					"products": [{
							"name": "商品6",
							"price": 100.0,
							"count": 3
						}],
					"final_price":300.0
				}]
				"""
