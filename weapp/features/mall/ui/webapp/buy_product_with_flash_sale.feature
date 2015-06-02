Feature: 添加商品到购物车后，浏览购物车中的商品
	bill将各种商品放入购物车后，能浏览商品信息

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
					"S": {
						"price": 10,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品6",
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
			"start_date": "1天后",
			"end_date": "2天后",
			"products": ["商品2"],
			"promotion_price": 2.1
		}, {
			"name": "商品3限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品3"],
			"promotion_price": 3.1
		}, {
			"name": "商品4限时抢购",
			"start_date": "前天",
			"end_date": "昨天",
			"products": ["商品4"],
			"promotion_price": 4.1
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


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.flash_sale
Scenario: 从购物车购买参加限时抢购活动的商品，商品包括无规格，有规格，活动有效，活动无效
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品6",
			"count": 1
		}, {
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
				"final_price": 25.8,
				"product_price": 25.8,
				"promotion_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 1
				}]
			}, {
				"products": [{
					"name": "商品3",
					"model": "M",
					"price": 3.1,
					"count": 1
				}]
			}, {
				"products": [{
					"name": "商品3",
					"model": "S",
					"price": 3.1,
					"count": 2
				}]
			}, {
				"products": [{
					"name": "商品6",
					"price": 5.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 25.8
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.flash_sale
Scenario: 直接购买参加限时抢购活动的商品
	
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
				"final_price": 11.5,
				"product_price": 11.5,
				"promotion_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 1
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 11.5
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.flash_sale
Scenario: 直接购买参加限时抢购活动的商品，但活动当前没有启动
	
	When bill访问jobs的webapp
	When bill访问jobs的webapp:ui
	And bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品2",
				"count": 1
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 5.0,
				"product_price": 5.0,
				"promotion_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品2",
					"price": 5.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
