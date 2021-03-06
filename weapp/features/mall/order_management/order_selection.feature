# __author__ : "冯雪静"
# __editor__ : "王丽" 2016-03-08
Feature:订单筛选
"""

	Jobs能通过管理系统为管理用户订单
	1 增加“首单”和“非首单”的过滤
		全部勾选和全部不勾选都是查询的全部订单
"""

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
			"price": 9.90,
			"pay_interfaces":[{
				"type": "在线支付"
			}, {
				"type": "货到付款"
			}]
		}, {
			"name": "商品2",
			"price": 9.90,
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
			"payment_time":"2014-10-03 12:00:00",
			"methods_of_payment": "货到付款",
			"sources": "本店",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"is_first_order":"true"
		},{
			"order_no": "00004",
			"member": "bill",
			"status": "已取消",
			"order_time": "2014-10-04 12:00:00",
			"payment_time":"2014-10-04 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "本店",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"is_first_order":"true"
		},{
			"order_no": "00005",
			"member": "tom",
			"status": "已完成",
			"order_time": "2014-10-05 12:00:00",
			"payment_time":"2014-10-05 13:00:00",
			"methods_of_payment": "微信支付",
			"sources": "本店",
			"products": [{
				"name": "商品2",
				"count": 1
			}],
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"logistics": "顺丰",
			"number": "123",
			"shipper": "",
			"is_first_order":"false"
		},{
			"order_no": "00006",
			"member": "tom",
			"status": "已发货",
			"order_time": "2014-10-06 12:00:00",
			"payment_time":"2014-10-06 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "本店",
			"products": [{
				"name": "商品2",
				"count": 1
			}],
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"logistics": "顺丰",
			"number": "123",
			"shipper": "",
			"is_first_order":"false"
		},{
			"order_no": "00007",
			"member": "bill",
			"status": "待发货",
			"order_time": "2014-10-07 12:00:00",
			"payment_time":"2014-10-07 13:00:00",
			"methods_of_payment": "支付宝",
			"sources": "本店",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"is_first_order":"false"
		},{
			"order_no": "00008",
			"member": "bill",
			"status": "待支付",
			"order_time": "2014-10-08 12:00:00",
			"payment_time":"",
			"methods_of_payment": "微信支付",
			"sources": "本店",
			"products": [{
				"name": "商品2",
				"count": 1
			}],
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"is_first_order":"false"
		}]
		"""

@mall2 @order @allOrder
Scenario:1 选择订单筛选条件
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
			"sources": "本店",
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
			"sources": "本店",
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
			"sources": "本店",
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
			"sources": "本店",
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
			"sources": "本店",
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
			"sources": "本店",
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
			"sources": "本店",
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
			"sources": "本店",
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
			"order_source": "本店"
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
			"sources": "本店",
			"ship_name": "bill",
			"ship_tel": "13811223344"
		}, {
			"order_no": "00004",
			"member": "bill",
			"status": "已取消",
			"order_time": "2014-10-04 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "本店",
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
			"sources": "本店",
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
			"sources": "本店",
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
			"sources": "本店",
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
			"sources": "本店",
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
			"order_source": "本店"
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
			"sources": "本店",
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
			"sources": "本店",
			"product_name": "商品1",
			"count": 1,
			"ship_name": "bill",
			"ship_tel": "13811223344"
		}]
		"""

# __editor__ : "王丽" 2016-03-08
@mall2 @order @allOrder @eugene
Scenario:2 按照【订单类型】进行筛选
	#筛选“订单类型”内容为“全部、首单、非首单”
	#"全部":筛选出所有订单；"首单"：筛选出带有首单标记的订单；"非首单":筛选出没有首单标记的订单

	Given jobs登录系统
	#全部
	#全部勾选查询全部订单
	When jobs根据给定条件查询订单
		"""
		{
			"is_first_order": "true",
			"is_not_first_order": "true"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "00008",
			"member": "bill",
			"status": "待支付",
			"order_time": "2014-10-08 12:00:00",
			"payment_time":"",
			"methods_of_payment": "微信支付",
			"sources": "本店",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"is_first_order":"false"
		},{
			"order_no": "00007",
			"member": "bill",
			"status": "待发货",
			"order_time": "2014-10-07 12:00:00",
			"payment_time":"2014-10-07 13:00:00",
			"methods_of_payment": "支付宝",
			"sources": "本店",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"is_first_order":"false"
		},{
			"order_no": "00006",
			"member": "tom",
			"status": "已发货",
			"order_time": "2014-10-06 12:00:00",
			"payment_time":"2014-10-06 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "本店",
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"is_first_order":"false"
		},{
			"order_no": "00005",
			"member": "tom",
			"status": "已完成",
			"order_time": "2014-10-05 12:00:00",
			"payment_time":"2014-10-05 13:00:00",
			"methods_of_payment": "微信支付",
			"sources": "本店",
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"is_first_order":"false"
		},{
			"order_no": "00004",
			"member": "bill",
			"status": "已取消",
			"order_time": "2014-10-04 12:00:00",
			"payment_time":"2014-10-04 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "本店",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"is_first_order":"true"
		},{
			"order_no": "00003",
			"member": "tom",
			"status": "待发货",
			"order_time": "2014-10-03 12:00:00",
			"payment_time":"2014-10-03 12:00:00",
			"methods_of_payment": "货到付款",
			"sources": "本店",
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"is_first_order":"true"
		}]
		"""

	#全部不勾选查询全部订单
	When jobs根据给定条件查询订单
		"""
		{
			"is_first_order": "false",
			"is_not_first_order": "false"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "00008",
			"member": "bill",
			"status": "待支付",
			"order_time": "2014-10-08 12:00:00",
			"payment_time":"",
			"methods_of_payment": "微信支付",
			"sources": "本店",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"is_first_order":"false"
		},{
			"order_no": "00007",
			"member": "bill",
			"status": "待发货",
			"order_time": "2014-10-07 12:00:00",
			"payment_time":"2014-10-07 13:00:00",
			"methods_of_payment": "支付宝",
			"sources": "本店",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"is_first_order":"false"
		},{
			"order_no": "00006",
			"member": "tom",
			"status": "已发货",
			"order_time": "2014-10-06 12:00:00",
			"payment_time":"2014-10-06 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "本店",
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"is_first_order":"false"
		},{
			"order_no": "00005",
			"member": "tom",
			"status": "已完成",
			"order_time": "2014-10-05 12:00:00",
			"payment_time":"2014-10-05 13:00:00",
			"methods_of_payment": "微信支付",
			"sources": "本店",
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"is_first_order":"false"
		},{
			"order_no": "00004",
			"member": "bill",
			"status": "已取消",
			"order_time": "2014-10-04 12:00:00",
			"payment_time":"2014-10-04 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "本店",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"is_first_order":"true"
		},{
			"order_no": "00003",
			"member": "tom",
			"status": "待发货",
			"order_time": "2014-10-03 12:00:00",
			"payment_time":"2014-10-03 12:00:00",
			"methods_of_payment": "货到付款",
			"sources": "本店",
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"is_first_order":"true"
		}]
		"""

	#首单
	When jobs根据给定条件查询订单
		"""
		{
			"is_first_order": "true",
			"is_not_first_order": "false"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "00004",
			"member": "bill",
			"status": "已取消",
			"order_time": "2014-10-04 12:00:00",
			"payment_time":"2014-10-04 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "本店",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"is_first_order":"true"
		},{
			"order_no": "00003",
			"member": "tom",
			"status": "待发货",
			"order_time": "2014-10-03 12:00:00",
			"payment_time":"2014-10-03 12:00:00",
			"methods_of_payment": "货到付款",
			"sources": "本店",
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"is_first_order":"true"
		}]
		"""

	#非首单
	When jobs根据给定条件查询订单
		"""
		{
			"is_first_order": "false",
			"is_not_first_order": "true"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "00008",
			"member": "bill",
			"status": "待支付",
			"order_time": "2014-10-08 12:00:00",
			"payment_time":"",
			"methods_of_payment": "微信支付",
			"sources": "本店",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"is_first_order":"false"
		},{
			"order_no": "00007",
			"member": "bill",
			"status": "待发货",
			"order_time": "2014-10-07 12:00:00",
			"payment_time":"2014-10-07 13:00:00",
			"methods_of_payment": "支付宝",
			"sources": "本店",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"is_first_order":"false"
		},{
			"order_no": "00006",
			"member": "tom",
			"status": "已发货",
			"order_time": "2014-10-06 12:00:00",
			"payment_time":"2014-10-06 12:00:00",
			"methods_of_payment": "优惠抵扣",
			"sources": "本店",
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"is_first_order":"false"
		},{
			"order_no": "00005",
			"member": "tom",
			"status": "已完成",
			"order_time": "2014-10-05 12:00:00",
			"payment_time":"2014-10-05 13:00:00",
			"methods_of_payment": "微信支付",
			"sources": "本店",
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"is_first_order":"false"
		}]
		"""

# __editor__ : "王丽" 2016-03-08
@mall2 @order @allOrder @eugene
Scenario:3 混合条件进行筛选
	Given jobs登录系统
	When jobs根据给定条件查询订单
		"""
		{
			"order_no": "00003",
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"product_name": "商品",
			"date_interval": "2014-10-03|2014-10-04",
			"date_interval_type": "付款时间",
			"pay_type": "货到付款",
			"express_number": "",
			"order_source": "全部",
			"order_status": "待发货",
			"isUseWeizoomCard": "false",
			"is_first_order": "true",
			"is_not_first_order": "false"
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
			"sources": "本店",
			"ship_name": "tom",
			"ship_tel": "13711223344",
			"is_first_order":"true"
		}]
		"""
