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


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.price_cut
Scenario: 直接购买参加满减活动的商品，金额大于满减价格阈值，循环满减没启用
	
	When bill访问jobs的webapp
	When bill访问jobs的webapp:ui
	And bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品1",
				"count": 5
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 239.5,
				"product_price": 250.0,
				"promotion_money": 10.5,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "price_cut",
					"result": {
						"price": 100.0,
						"cut_money": 10.5
					}
				},
				"subtotal": {
					"count": 5,
					"money": 239.5
				},
				"products": [{
					"name": "商品1",
					"price": 50.0,
					"count": 5
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 239.5
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.price_cut
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
	When bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 151.0,
				"product_price": 171.0,
				"promotion_money": 20.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "price_cut",
					"result": {
						"price": 140,
						"cut_money": 20.0
					}
				},
				"subtotal": {
					"count": 18,
					"money": 150.0
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
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 151.0
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.price_cut
Scenario: 直接购买参加满减活动的商品，金额等于满减价格阈值
	
	When bill访问jobs的webapp
	When bill访问jobs的webapp:ui
	And bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品1",
				"count": 2
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 89.5,
				"product_price": 100.0,
				"promotion_money": 10.5,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "price_cut",
					"result": {
						"price": 100,
						"cut_money": 10.5
					}
				},
				"subtotal": {
					"count": 2,
					"money": 89.5
				},
				"products": [{
					"name": "商品1",
					"price": 50.0,
					"count": 2
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 89.5
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.price_cut
Scenario: 直接购买参加满减活动的商品，金额小于满减价格阈值
	
	When bill访问jobs的webapp
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
				"final_price": 50.0,
				"product_price": 50.0,
				"promotion_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "price_cut",
					"result": {
						"price": 100.0,
						"cut_money": 10.5
					}
				},
				"subtotal": {
					"count": 1,
					"money": 50.0
				},
				"products": [{
					"name": "商品1",
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
			"price": 50.0
		}
		"""
