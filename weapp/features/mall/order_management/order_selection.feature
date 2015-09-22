# __author__ : "冯雪静"
Feature:订单筛选
	Jobs能通过管理系统为管理用户订单

Background:
	Given jobs登录系统
	And bill关注jobs的公众号
	And tom关注jobs的公众号
	Given jobs登录系统
	And jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 9.9,
			"pay_interfaces":[{
				"type": "在线支付"
			}, {
				"type": "货到付款"
			}]
		}, {
			"name": "商品2",
			"price": 9.9,
			"pay_interfaces":[{
				"type": "在线支付"
			}]
		}]
		"""
	And jobs已有的订单
		"""
		[{
			"order_no": "00003",
			"member": "tom",
			"status": "待发货",
			"order_time": "2014-10-03 12:00:00",
			"methods_of_payment": "货到付款",
			"sources": "商城",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"ship_name": "tom",
			"ship_tel": "13711223344"
		},{
			"order_no": "00004",
			"member": "bill",
			"status": "已取消",
			"order_time": "2014-10-04 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "商城",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"ship_name": "bill",
			"ship_tel": "13811223344"
		},{
			"order_no": "00005",
			"member": "tom",
			"status": "已完成",
			"order_time": "2014-10-05 12:00:00",
			"methods_of_payment": "微信支付",
			"sources": "商城",
			"products": [{
				"name": "商品2",
				"count": 1
			}],
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"logistics": "顺丰",
			"number": "123",
			"shipper": ""
		},{
			"order_no": "00006",
			"member": "tom",
			"status": "已发货",
			"order_time": "2014-10-06 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "商城",
			"products": [{
				"name": "商品2",
				"count": 1
			}],
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"logistics": "顺丰",
			"number": "123",
			"shipper": ""
		},{
			"order_no": "00007",
			"member": "bill",
			"status": "待发货",
			"order_time": "2014-10-07 12:00:00",
			"methods_of_payment": "支付宝",
			"sources": "商城",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"ship_name": "bill",
			"ship_tel": "13811223344"
		},{
			"order_no": "00008",
			"member": "bill",
			"status": "待支付",
			"order_time": "2014-10-08 12:00:00",
			"methods_of_payment": "微信支付",
			"sources": "商城",
			"products": [{
				"name": "商品2",
				"count": 1
			}],
			"ship_name": "bill",
			"ship_tel": "13811223344"
		}]
		"""

@mall2 @order @allOrder
Scenario: 选择订单筛选条件
	jobs选择订单筛选条件后
	1. jobs选择一个条件时,可以看到订单列表
	2. jobs选择多个条件时,可以看到订单列表
	3. jobs填写详细信息时,可以看到订单列表
	4. jobs选择固定标签时,可以看到订单列表

	Given jobs登录系统
	When jobs根据给定条件查询订单
		"""
		{
			"order_no": "00008"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "00008",
			"member": "bill",
			"status": "待支付",
			"order_time": "2014-10-08 12:00:00",
			"methods_of_payment": "微信支付",
			"sources": "商城",
			"ship_name": "bill",
			"ship_tel": "13811223344"
		}]
		"""
	Then jobs导出订单获取订单信息
		"""
		[{
			"order_no": "00008",
			"member": "bill",
			"status": "待支付",
			"order_time": "2014-10-08 12:00",
			"methods_of_payment": "微信支付",
			"sources": "商城",
			"product_name": "商品2",
			"count": 1,
			"ship_name": "bill",
			"ship_tel": "13811223344"
		}]
		"""

		#	"products": [{
		#		"name": "商品2",
		#		"count": 1
		#	}],

	When jobs根据给定条件查询订单
		"""
		{
			"express_number": "123"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "00006",
			"member": "tom",
			"status": "已发货",
			"order_time": "2014-10-06 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "商城",
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"logistics": "顺丰",
			"number": "123",
			"shipper": ""
		}, {
			"order_no": "00005",
			"member": "tom",
			"status": "已完成",
			"order_time": "2014-10-05 12:00:00",
			"methods_of_payment": "微信支付",
			"sources": "商城",
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"logistics": "顺丰",
			"number": "123",
			"shipper": ""
		}]
		"""
	Then jobs导出订单获取订单信息
		"""
		[{
			"order_no": "00006",
			"member": "tom",
			"status": "已发货",
			"order_time": "2014-10-06 12:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "商城",
			"product_name": "商品2",
			"count": 1,
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"logistics": "顺丰",
			"number": "123",
			"shipper": ""
		}, {
			"order_no": "00005",
			"member": "tom",
			"status": "已完成",
			"order_time": "2014-10-05 12:00",
			"methods_of_payment": "微信支付",
			"sources": "商城",
			"product_name": "商品2",
			"count": 1,
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"logistics": "顺丰",
			"number": "123",
			"shipper": ""
		}]
		"""

	When jobs根据给定条件查询订单
		"""
		{
			"order_status": "待发货",
			"pay_type": "支付宝"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "00007",
			"member": "bill",
			"status": "待发货",
			"order_time": "2014-10-07 12:00:00",
			"methods_of_payment": "支付宝",
			"sources": "商城",
			"ship_name": "bill",
			"ship_tel": "13811223344"
		}]
		"""
	Then jobs导出订单获取订单信息
		"""
		[{
			"order_no": "00007",
			"member": "bill",
			"status": "待发货",
			"order_time": "2014-10-07 12:00",
			"methods_of_payment": "支付宝",
			"sources": "商城",
			"product_name": "商品1",
			"count": 1,
			"ship_name": "bill",
			"ship_tel": "13811223344"
		}]
		"""

	When jobs根据给定条件查询订单
		"""
		{
			"product_name": "商品1",
			"ship_name": "bill",
			"order_source": "商城"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "00007",
			"member": "bill",
			"status": "待发货",
			"order_time": "2014-10-07 12:00:00",
			"methods_of_payment": "支付宝",
			"sources": "商城",
			"ship_name": "bill",
			"ship_tel": "13811223344"
		}, {
			"order_no": "00004",
			"member": "bill",
			"status": "已取消",
			"order_time": "2014-10-04 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "商城",
			"ship_name": "bill",
			"ship_tel": "13811223344"
		}]
		"""
	 Then jobs导出订单获取订单信息
		"""
		[{
			"order_no": "00007",
			"member": "bill",
			"status": "待发货",
			"order_time": "2014-10-07 12:00",
			"methods_of_payment": "支付宝",
			"sources": "商城",
			"product_name": "商品1",
			"count": 1,
			"ship_name": "bill",
			"ship_tel": "13811223344"
		}, {
			"order_no": "00004",
			"member": "bill",
			"status": "已取消",
			"order_time": "2014-10-04 12:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "商城",
			"product_name": "商品1",
			"count": 1,
			"ship_name": "bill",
			"ship_tel": "13811223344"
		}]
		"""

	When jobs根据给定条件查询订单
		"""
		{
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"product_name": "商品1"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "00003",
			"member": "tom",
			"status": "待发货",
			"order_time": "2014-10-03 12:00:00",
			"methods_of_payment": "货到付款",
			"sources": "商城",
			"ship_name": "tom",
			"ship_tel": "13711223344"
		}]
		"""
	Then jobs导出订单获取订单信息
		"""
		[{
			"order_no": "00003",
			"member": "tom",
			"status": "待发货",
			"order_time": "2014-10-03 12:00",
			"methods_of_payment": "货到付款",
			"sources": "商城",
			"product_name": "商品1",
			"count": 1,
			"ship_name": "tom",
			"ship_tel": "13711223344"
		}]
		"""

	When jobs根据给定条件查询订单
		"""
		{
			"order_status": "已发货",
			"express_number": "321",
			"order_source": "商城"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[]
		"""

	When jobs根据给定条件查询订单
		"""
		{
			"date_interval": "2014-10-07|2014-10-08",
			"date_interval_type": 1,
			"ship_name": "tom",
			"ship_tel": "13711223344"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[]
		"""

	When jobs根据给定条件查询订单
		"""
		{
			"order_status": "已取消"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "00004",
			"member": "bill",
			"status": "已取消",
			"order_time": "2014-10-04 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "商城",
			"ship_name": "bill",
			"ship_tel": "13811223344"
		}]
		"""
	Then jobs导出订单获取订单信息
		"""
		[{
			"order_no": "00004",
			"member": "bill",
			"status": "已取消",
			"order_time": "2014-10-04 12:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "商城",
			"product_name": "商品1",
			"count": 1,
			"ship_name": "bill",
			"ship_tel": "13811223344"
		}]
		"""
