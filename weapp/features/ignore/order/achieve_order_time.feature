# __author__ : "冯雪静"

Feature: 记录完成订单的时间
	"""
	实现不了step，手工测试
	1.后台完成订单记录时间-完成-商户名称
	2.手机端确认收货后完成订单记录时间-完成-客户
	3.签收快件后完成订单记录时间-完成-系统
	"""

Background:
	Given jobs登录系统
	And jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00
		}]
		"""
	And bill关注jobs的公众号


@order
Scenario: 1 后台完成订单记录时间
	bill购买jobs的商品后，jobs对订单发货，完成

	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_id": "001",
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	When bill使用支付方式'货到付款'进行支付
	Given jobs登录系统
	When jobs对订单进行发货
		"""
		{
			"order_no": "001",
			"logistics": "申通快递",
			"number": "229388967650",
			"shipper": "jobs"
		}
		"""
	When jobs完成订单'001'
	Then jobs能获得订单'001'
		"""
		{
			"order_no": "001",
			"member": "bill",
			"status": "已完成",
			"created_at": 2015-11-23 12:00:00",
			"actions": ["申请退款"],
			"shipper": "jobs",
			"methods_of_payment":"货到付款"
		}
		"""

@order
Scenario: 2 手机端确认收货后完成订单记录时间
	bill购买jobs的商品后，jobs对订单发货，bill手机端确认收货


	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_id": "002",
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	When bill使用支付方式'货到付款'进行支付
	Given jobs登录系统
	When jobs对订单进行发货
		"""
		{
			"order_no": "002",
			"logistics": "off",
			"shipper": ""
		}
		"""
	When bill访问jobs的webapp
	When bill对订单"001"确认收货
	Given jobs登录系统
	Then jobs能获得订单"002"
		"""
		{
			"order_no": "002",
			"member": "bill",
			"status": "已完成",
			"created_at": 2015-11-23 12:00:00",
			"actions": ["申请退款"],
			"shipper": "",
			"methods_of_payment":"货到付款"
		}
		"""

@order
Scenario: 3 签收快件后完成订单记录时间
	bill购买jobs的商品后，jobs对订单发货，快件被签收

	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_id": "003",
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	When bill使用支付方式'货到付款'进行支付
	Given jobs登录系统
	When jobs对订单进行发货
		"""
		{
			"order_no": "003",
			"logistics": "申通快递",
			"number": "229388967650",
			"shipper": "jobs"
		}
		"""
	When 快递100发送物流单号"229388967650"完成的信息
	Then jobs能获得订单"003"
		"""
		{
			"order_no": "003",
			"member": "bill",
			"status": "已完成",
			"created_at": 2015-11-23 12:00:00",
			"actions": ["申请退款"],
			"shipper": "jobs",
			"methods_of_payment":"货到付款"
		}
		"""
