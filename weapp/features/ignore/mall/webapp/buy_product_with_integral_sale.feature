Feature: 购买参加“满减”活动的商品


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
			"price": 100.00,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "商品2",
			"price": 200.00
		}, {
			"name": "商品3",
			"price": 50.00
		}, {
			"name": "商品4",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"M": {
						"price": 100.00
					},
					"S": {
						"price": 25.0
					}
				}
			}
		}]
		"""
	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2
		}
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"discount": 70,
			"discount_money": 70.0,
			"is_permanant_active": false
		}, {
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "2天后",
			"products": ["商品3"],
			"discount": 50,
			"discount_money": 25.0,
			"is_permanant_active": true
		}, {
			"name": "商品4积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品4"],
			"discount": 70,
			"discount_money": 70.0,
			"is_permanant_active": false
		}]
		"""
	#支付方式
	Given jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	And bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.promotion @ui-mall.webapp.integral_sale
Scenario: 购买单个积分折扣商品，积分金额小于最大折扣金额
	
	When bill访问jobs的webapp
	When bill获得jobs的50会员积分
	When bill访问jobs的webapp:ui
	And bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品1",
				"count": 1
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 100.0,
				"product_price": 100.0,
				"promotion_money": 0.0,
				"integral_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "integral_sale",
					"result": {
						"total_integral": 50,
						"usable_integral": 50,
						"money": 25.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 100.0
				},
				"products": [{
					"name": "商品1",
					"price": 100.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill对商品'商品1'使用积分:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 75.0,
				"product_price": 100.0,
				"promotion_money": 0.0,
				"integral_money": 25.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "integral_sale",
					"result": {
						"used_integral": 50,
						"money": 25.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 75.0
				},
				"products": [{
					"name": "商品1",
					"price": 100.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill对商品'商品1'取消使用积分:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 100.0,
				"product_price": 100.0,
				"promotion_money": 0.0,
				"integral_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "integral_sale",
					"result": {
						"total_integral": 50,
						"usable_integral": 50,
						"money": 25.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 100.0
				},
				"products": [{
					"name": "商品1",
					"price": 100.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 100.0
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.promotion @ui-mall.webapp.integral_sale
Scenario: 购买单个积分折扣商品，积分金额等于最大折扣金额
	
	When bill访问jobs的webapp
	When bill获得jobs的150会员积分
	When bill访问jobs的webapp:ui
	And bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品1",
				"count": 1
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 100.0,
				"product_price": 100.0,
				"promotion_money": 0.0,
				"integral_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "integral_sale",
					"result": {
						"total_integral": 150,
						"usable_integral": 140,
						"money": 70.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 100.0
				},
				"products": [{
					"name": "商品1",
					"price": 100.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill对商品'商品1'使用积分:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 30.0,
				"product_price": 100.0,
				"promotion_money": 0.0,
				"integral_money": 70.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "integral_sale",
					"result": {
						"used_integral": 140,
						"money": 70.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 30.0
				},
				"products": [{
					"name": "商品1",
					"price": 100.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 30.0
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.promotion @ui-mall.webapp.integral_sale
Scenario: 购买多个积分折扣商品，顺序：先对商品3使用积分，再对商品1使用积分
	
	When bill访问jobs的webapp
	When bill获得jobs的100会员积分
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品3",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	When bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 150.0,
				"product_price": 150.0,
				"promotion_money": 0.0,
				"integral_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "integral_sale",
					"result": {
						"total_integral": 100,
						"usable_integral": 100,
						"money": 50.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 100.0
				},
				"products": [{
					"name": "商品1",
					"price": 100.0,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "integral_sale",
					"result": {
						"total_integral": 100,
						"usable_integral": 50,
						"money": 25.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 50.0
				},
				"products": [{
					"name": "商品3",
					"price": 50.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill对商品'商品3'使用积分:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 125.0,
				"product_price": 150.0,
				"promotion_money": 0.0,
				"integral_money": 25.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "integral_sale",
					"result": {
						"total_integral": 50,
						"usable_integral": 50,
						"money": 25.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 100.0
				},
				"products": [{
					"name": "商品1",
					"price": 100.0,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "integral_sale",
					"result": {
						"used_integral": 50,
						"money": 25.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 25.0
				},
				"products": [{
					"name": "商品3",
					"price": 50.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill对商品'商品1'使用积分:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 100.0,
				"product_price": 150.0,
				"promotion_money": 0.0,
				"integral_money": 50.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "integral_sale",
					"result": {
						"used_integral": 50,
						"money": 25.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 75.0
				},
				"products": [{
					"name": "商品1",
					"price": 100.0,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "integral_sale",
					"result": {
						"used_integral": 50,
						"money": 25.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 25.0
				},
				"products": [{
					"name": "商品3",
					"price": 50.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 100.0
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.promotion @ui-mall.webapp.integral_sale
Scenario: 购买多规格的积分折扣商品
	
	When bill访问jobs的webapp
	When bill获得jobs的150会员积分
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品4",
			"model": {
				"models":{
					"M": {
						"count": 1
					}
				}
			}
		}, {
			"name": "商品4",
			"model": {
				"models":{
					"S": {
						"count": 2
					}
				}
			}
		}]
		"""
	When bill访问jobs的webapp:ui
	When bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 150.0,
				"product_price": 150.0,
				"promotion_money": 0.0,
				"integral_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "integral_sale",
					"result": {
						"total_integral": 150,
						"usable_integral": 140,
						"money": 70.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 100.0
				},
				"products": [{
					"name": "商品4",
					"model": "M",
					"price": 100.0,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "integral_sale",
					"result": {
						"total_integral": 150,
						"usable_integral": 70,
						"money": 35.0
					}
				},
				"subtotal": {
					"count": 2,
					"money": 50.0
				},
				"products": [{
					"name": "商品4",
					"price": 25.0,
					"count": 2
				}]
			}]
		}
		"""
	When bill对规格为'M'的商品'商品4'使用积分:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 80.0,
				"product_price": 150.0,
				"promotion_money": 0.0,
				"integral_money": 70.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "integral_sale",
					"result": {
						"used_integral": 140,
						"money": 70.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 30.0
				},
				"products": [{
					"name": "商品4",
					"model": "M",
					"price": 100.0,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "integral_sale",
					"result": {
						"total_integral": 10,
						"usable_integral": 10,
						"money": 5.0
					}
				},
				"subtotal": {
					"count": 2,
					"money": 50.0
				},
				"products": [{
					"name": "商品4",
					"price": 25.0,
					"count": 2
				}]
			}]
		}
		"""
	When bill对规格为'S'的商品'商品4'使用积分:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 75.0,
				"product_price": 150.0,
				"promotion_money": 0.0,
				"integral_money": 75.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "integral_sale",
					"result": {
						"used_integral": 140,
						"money": 70.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 30.0
				},
				"products": [{
					"name": "商品4",
					"model": "M",
					"price": 100.0,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "integral_sale",
					"result": {
						"used_integral": 10,
						"money": 5.0
					}
				},
				"subtotal": {
					"count": 2,
					"money": 45.0
				},
				"products": [{
					"name": "商品4",
					"price": 25.0,
					"count": 2
				}]
			}]
		}
		"""
	When bill对规格为'M'的商品'商品4'取消使用积分:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 145.0,
				"product_price": 150.0,
				"promotion_money": 0.0,
				"integral_money": 5.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "integral_sale",
					"result": {
						"total_integral": 140,
						"usable_integral": 140,
						"money": 70.0
					}
				},
				"subtotal": {
					"count": 1,
					"money": 100.0
				},
				"products": [{
					"name": "商品4",
					"model": "M",
					"price": 100.0,
					"count": 1
				}]
			}, {
				"promotion": {
					"type": "integral_sale",
					"result": {
						"used_integral": 10,
						"money": 5.0
					}
				},
				"subtotal": {
					"count": 2,
					"money": 45.0
				},
				"products": [{
					"name": "商品4",
					"price": 25.0,
					"count": 2
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 145.0
		}
		"""