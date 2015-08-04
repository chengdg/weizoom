Feature: 购买参加“满减”活动的商品
	todo: 缺少已赠完的场景

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
			"model": {
				"models":{
					"standard": {
						"price": 7,
						"stock_type": "有限",
						"stocks": 4
					}
				}
			}
		}, {
			"name": "商品4",
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
			"name": "商品5",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"S": {
						"price": 10,
						"stock_type": "无限"
					}
				}
			}
		}]	
		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "商品1买一赠二",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
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
			"products": ["商品2"],
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
			"products": ["商品3"],
			"premium_products": [{
				"name": "商品4",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": false
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


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.premium_sale
Scenario: 直接购买商品，商品不满足买赠的购买基数
	
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
				"final_price": 30.0,
				"product_price": 30.0,
				"promotion_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": null,
				"subtotal": {
					"count": 1,
					"money": 30.0
				},
				"products": [{
					"name": "商品1",
					"price": 30.0,
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


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.premiun_sale
Scenario: 从购物车购买商品，商品数量大于买赠的购买基数，并满足循环买赠
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 5
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
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "premium_sale",
					"result": {
						"premium_products": [{
							"name": "商品2",
							"count": 2,
							"stock_info": ""
						}, {
							"name": "商品3",
							"count": 4,
							"stock_info": ""
						}]
					}
				},
				"subtotal": {
					"count": 11,
					"money": 150.0
				},
				"products": [{
					"name": "商品1",
					"price": 30.0,
					"count": 5
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 150.0
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.premium_sale @todo
Scenario: 直接购买商品，商品满足买赠，但赠品库存不足
	库存不足，应该弹出提示框
	
	When bill访问jobs的webapp
	When bill访问jobs的webapp:ui
	And bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品1",
				"count": 6
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 180.0,
				"product_price": 180.0,
				"promotion_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": {
					"type": "premium_sale",
					"result": {
						"premium_products": [{
							"name": "商品2",
							"count": 3,
							"stock_info": ""
						}, {
							"name": "商品3",
							"count": 6,
							"stock_info": "赠品不足"
						}]
					}
				},
				"subtotal": {
					"count": 15,
					"money": 180.0
				},
				"products": [{
					"name": "商品1",
					"price": 30.0,
					"count": 6
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 180.0
		}
		"""
