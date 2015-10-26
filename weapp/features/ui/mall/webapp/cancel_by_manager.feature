# __author__ : "新新9.23"

Feature: 取消订单,可获取订单状态
"""
	1.后台取消订单后,手机端订单状态为'已取消'
	2.手机端取消订单后,手机端订单状态为'已取消'

"""
Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"model": {
				"models": {
					"standard": {
						"price": 9.9,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}

		}]
		"""
	And bill关注jobs的公众号


Scenario:1 后台取消订单后,手机端订单状态为'已取消'
	jobs取消订单,bill可以获取订单状态为'已取消'


	Given jobs登录系统

	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1",
				"count": 2
			}],
			"customer_message": "bill的订单备注1"
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"final_price": 19.8,
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Given jobs登录系统
	Then jobs可以获得最新订单详情
		"""
		{
			"order_type": "普通订单",
			"status": "待支付",
			"actions": ["取消订单", "支付"],
			"total_price": 19.8,
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"customer_message": "bill的订单备注1",
			"products": [{
				"name": "商品1",
				"count": 2,
				"total_price": 19.80
			}]
		}
		"""
	When jobs'取消'最新订单
	
	Then jobs可以获得最新订单详情
		"""
		{
			"order_type": "普通订单",
			"status": "已取消",
			"actions": []
		}
		"""
	When bill访问jobs的webapp
	Then bill成功创建订单
		"""
		{
			"status": "已取消",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"final_price": 19.8,
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
Scenario:2 手机端取消订单后,手机端订单状态为'已取消'
		bill取消订单,jobs可以获取订单状态为'已取消'

	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1",
				"count": 2
			}],
			"customer_message": "bill的订单备注1"
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"final_price": 19.8,
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	
	When bill'取消'最新订单
	Then bill成功创建订单
		"""
		{
			"status": "已取消",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"final_price": 19.8,
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	When jobs登录系统
	Then jobs可以获得最新订单详情
		"""
		{
			"order_type": "普通订单",
			"status": "已取消",
			"actions": []
		}
		"""