#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
# __author__ : "冯雪静"

Feature: 不需要物流的订单
"""

	jobs通过管理系统能为用户发货不需要物流
"""

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100,
			"stocks": 8
		 }]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号
	And jobs已有的订单
		"""
		[{
			"order_no":"00008",
			"member":"bill",
			"status":"待发货",
			"order_time":"2014-10-08 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		},{
			"order_no":"00007",
			"member":"bill",
			"status":"待发货",
			"order_time":"2014-10-07 12:00:00",
			"methods_of_payment":"支付宝",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		},{
			"order_no":"00006",
			"member":"tom",
			"status":"待发货",
			"order_time":"2014-10-06 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
		}]
		"""

@mall2 @order @logistics
Scenario: 1 对待发货订单进行发货不需要物流
	jobs对不需要物流的订单进行发货
	1.不填写发货人
	2.填写发货人
	3.对已发货订单标记完成

	Given jobs登录系统
	When jobs对订单进行发货
		"""
		{
			"order_no": "00008",
			"logistics": "off",
			"shipper": ""
		}
		"""
	Then jobs能获得订单'00008'
		"""
		{
			"order_no":"00008",
			"member":"bill",
			"status":"已发货",
			"actions": ["标记完成", "取消订单"],
			"shipper": "",
			"order_time":"2014-10-08 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		}
		"""
	When jobs对订单进行发货
		"""
		{
			"order_no": "00007",
			"logistics": "off",
			"shipper": "jobs"
		}
		"""
	Then jobs能获得订单'00007'
		"""
		{
			"order_no":"00007",
			"member":"bill",
			"status":"已发货",
			"actions": ["标记完成", "申请退款"],
			"shipper": "jobs",
			"order_time":"2014-10-07 12:00:00",
			"methods_of_payment":"支付宝",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		}
		"""
	When jobs完成订单'00008'
	Then jobs能获得订单'00008'
		"""
		{
			"order_no":"00008",
			"member":"bill",
			"status":"已完成",
			"actions": ["取消订单"],
			"shipper": "",
			"order_time":"2014-10-08 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		}
		"""
	When jobs完成订单'00007'
	Then jobs能获得订单'00007'
		"""
		{
			"order_no":"00007",
			"member":"bill",
			"status":"已完成",
			"actions": ["申请退款"],
			"shipper": "jobs",
			"order_time":"2014-10-07 12:00:00",
			"methods_of_payment":"支付宝",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		}
		"""

