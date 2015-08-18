@func:webapp.modules.mall.views.list_products
Feature: 在webapp中购买商品
	bill能在webapp中购买jobs添加的"商品"

Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 9.9
		}, {
			"name": "商品2",
			"price": 8.8
		}]	
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"description": "我的支付宝",
			"is_active": "启用"
		}]
		"""

@ui @ui-mall @ui-mall.webapp
Scenario: 购买单个商品
	jobs添加商品后
	1. bill能在webapp中购买jobs添加的商品
	1. bill的订单中的信息正确
	
	When bill访问jobs的webapp:ui
	And bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1",
				"price": 9.9,
				"count": 2
			}]
		}
		"""


@ui @ui-mall @ui-mall.webapp
Scenario: 购买商品时，使用订单备注
	bill在购买jobs添加的商品时
	1. 添加了"订单备注"，则jobs能在管理系统中看到该"订单备注"
	2. 不添加'订单备注', 则jobs能在管理系统中看到"订单备注"为空字符串
	
	When bill访问jobs的webapp:ui
	And bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}],
			"customer_message": "bill的订单备注"
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"customer_message": "bill的订单备注"
		}
		"""
	Given jobs登录系统:ui
	Then jobs能获取最新的订单:ui
		"""
		{
			"customer_message": "bill的订单备注"
		}
		"""

	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品2",
				"count": 1
			}]
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"customer_message": ""
		}
		"""
	Given jobs登录系统:ui
	Then jobs能获取最新的订单:ui
		"""
		{
			"customer_message": ""
		}
		"""