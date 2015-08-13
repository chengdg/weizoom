# __author__ : "冯雪静"
Feature:商品销量
	Jobs能通过管理系统为管理商城"商品销量"


Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 10
					}
				}
			}
		}]
		"""
	And jobs已添加支付方式
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


@mall2
Scenario: 1 成功支付订单后，商品销量增加
	bill购买商品支付成功后，jobs的商品销量增加
	1.商品库存减少

	When bill访问jobs的webapp
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		'''
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When bill使用支付方式'货到付款'进行支付
	Then bill支付订单成功
		"""
		{
			"status": "待发货",
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	Then jobs能获取商品'商品1'
	"""
		{
			"name": "商品1",
			"sales": 1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		}
	"""


@mall2
Scenario: 2 订单为待支付状态时，商品销量不变
	bill成功创建订单待支付状态，jobs的商品销量不变
	1.商品库存减少

	When bill访问jobs的webapp
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		'''
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	Then jobs能获取商品'商品1'
	"""
		{
			"name": "商品1",
			"sales": 0,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		}
	"""

@mall2
Scenario: 3 成功支付订单后，取消订单，商品销量不变
	bill购买商品支付成功后，jobs取消订单，jobs的商品销量不变
	1.商品库存不变

	When bill访问jobs的webapp
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		'''
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When bill使用支付方式'货到付款'进行支付
	Then bill支付订单成功
		"""
		{
			"status": "待发货",
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	Then jobs可以获得最新订单详情
		"""
		{
			"status": "待发货",
			"final_price": 100.00,
			"actions": ["发货","取消订单"]
		}
		"""
	When jobs'取消'最新订单
		"""
		{
			"reason": "不想要了"
		}
		"""
	Then jobs可以获得最新订单详情
		"""
		{
			"status": "已取消",
			"final_price": 100.00,
			"actions": []
		}
		"""
	And jobs能获取商品'商品1'
	"""
		{
			"name": "商品1",
			"sales": 0,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 10
					}
				}
			}
		}
	"""
