@func:webapp.modules.mall.views.list_products
Feature: 在webapp中支付订单
	bill能在webapp中支付订单

Background:
	Given jobs登录系统
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
	And jobs已添加了支付方式
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
	And bill关注jobs的公众号


@ui @ui-mall @ui-mall.webapp
Scenario: 使用货到付款支付
	bill在下单购买jobs的商品后，能使用货到付款进行支付，支付后
	1. bill的订单中变为已支付
	2. jobs在后台看到订单变为已支付
	
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 9.9,
			"products": [{
				"name": "商品1",
				"price": 9.9,
				"count": 1
			}]
		}
		"""
	When bill使用支付方式'货到付款'进行支付
	Then bill支付订单成功
		"""
		{
			"status": "待发货",
			"final_price": 9.9,
			"products": [{
				"name": "商品1",
				"price": 9.9,
				"count": 1
			}]
		}
		"""
	