# __author__ : "冯雪静"
Feature: 批量发货
	jobs能为用户批量发货
	"""
	1.对多个订单同时进行发货
	2.对多个订单同时进行发货失败
	3.对修改过价格的订单进行批量发货
	"""
Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100,
			"stocks": 4
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
		},{
			"order_no":"00005",
			"member":"tom",
			"status":"待发货",
			"order_time":"2014-10-05 12:00:00",
			"methods_of_payment":"微信支付",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
		},{
			"order_no":"00004",
			"member":"bill",
			"status":"待发货",
			"order_time":"2014-10-04 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		},{
			"order_no":"00003",
			"member":"tom",
			"status":"待发货",
			"order_time":"2014-10-03 12:00:00",
			"methods_of_payment":"货到付款",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
		},{
			"order_no":"00002",
			"member":"bill",
			"status":"已取消",
			"order_time":"2014-10-02 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		},{
			"order_no":"00001",
			"member":"tom",
			"status":"待支付",
			"order_time":"2014-10-01 12:00:00",
			"methods_of_payment":"",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
		}]
		"""

@mall2 @mall.order_filter @mall.order_filter.bulk_shipments
Scenario: 1 对多个订单同时进行发货
	jobs填写多个订单号和快递信息进行发货
	1.填写信息正确,发货成功
	2.填写信息有误,发货失败

	Given jobs登录系统
	When jobs填写订单信息
		"""
		[{
			"order_no":"00003",
			"logistics":"顺丰速运",
			"number":"147258369"
		},{
			"order_no":"00004",
			"logistics":"申通快递",
			"number":"147258368"
		},{
			"order_no":"00005",
			"logistics":"圆通速递",
			"number":"147258367"
		}]
		"""
	When jobs根据给定条件查询订单
		"""
		{}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no":"00001",
			"member":"tom",
			"status":"待支付",
			"order_time":"2014-10-01 12:00:00",
			"methods_of_payment":"",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
		},{
			"order_no":"00002",
			"member":"bill",
			"status":"已取消",
			"order_time":"2014-10-02 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		},{
			"order_no":"00003",
			"member":"tom",
			"status":"已发货",
			"order_time":"2014-10-03 12:00:00",
			"methods_of_payment":"货到付款",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344",
			"logistics":"顺丰速运",
			"number":"147258369",
			"shipper":""
		},{
			"order_no":"00004",
			"member":"bill",
			"status":"已发货",
			"order_time":"2014-10-04 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"logistics":"申通快递",
			"number":"147258368",
			"shipper":""
		},{
			"order_no":"00005",
			"member":"tom",
			"status":"已发货",
			"order_time":"2014-10-05 12:00:00",
			"methods_of_payment":"微信支付",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344",
			"logistics":"圆通速递",
			"number":"147258367",
			"shipper":""
		},{
			"order_no":"00006",
			"member":"tom",
			"status":"待发货",
			"order_time":"2014-10-06 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
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
			"order_no":"00008",
			"member":"bill",
			"status":"待发货",
			"order_time":"2014-10-08 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		}]
		"""
	When jobs填写订单信息
		"""
		[{
			"order_no":"00001",
			"logistics":"顺丰速运",
			"number":"147258365"
		},{
			"order_no":"00006",
			"logistics":"申通",
			"number":"147258364"
		},{
			"order_no":"00007",
			"logistics":"圆通速递",
			"number":"147258366"
		},{
			"order_no":"00002",
			"logistics":"顺丰速运",
			"number":"147258363"
		},{
			"order_no":"00008",
			"logistics":"ems",
			"number":"147258362"
		}]
		"""
#	When jobs选择条件为
#		"""
#		{}
#		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no":"00001",
			"member":"tom",
			"status":"待支付",
			"order_time":"2014-10-01 12:00:00",
			"methods_of_payment":"",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
		},{
			"order_no":"00002",
			"member":"bill",
			"status":"已取消",
			"order_time":"2014-10-02 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		},{
			"order_no":"00003",
			"member":"tom",
			"status":"已发货",
			"order_time":"2014-10-03 12:00:00",
			"methods_of_payment":"货到付款",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344",
			"logistics":"顺丰速运",
			"number":"147258369",
			"shipper":""
		},{
			"order_no":"00004",
			"member":"bill",
			"status":"已发货",
			"order_time":"2014-10-04 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"logistics":"申通快递",
			"number":"147258368",
			"shipper":""
		},{
			"order_no":"00005",
			"member":"tom",
			"status":"已发货",
			"order_time":"2014-10-05 12:00:00",
			"methods_of_payment":"微信支付",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344",
			"logistics":"圆通速递",
			"number":"147258367",
			"shipper":""
		},{
			"order_no":"00006",
			"member":"tom",
			"status":"待发货",
			"order_time":"2014-10-06 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
		},{
			"order_no":"00007",
			"member":"bill",
			"status":"已发货",
			"order_time":"2014-10-07 12:00:00",
			"methods_of_payment":"支付宝",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"logistics":"圆通速递",
			"number":"147258366",
			"shipper":""
		},{
			"order_no":"00008",
			"member":"bill",
			"status":"待发货",
			"order_time":"2014-10-08 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		}]
		"""


@mall2 @deliver
Scenario: 2 对多个订单同时进行发货失败
	jobs填写多个订单号和快递信息进行发货
	1.填写信息有误,发货失败
	2.提示错误信息

	#1.订单状态错误2.订单号错误3.快递名称错误4.格式不正确
	Given jobs登录系统
	When jobs填写订单信息
		"""
		[{
			"order_no":"00001",
			"logistics":"顺丰速运",
			"number":"147258369"
		},{
			"order_no":"000030",
			"logistics":"顺丰速运",
			"number":"147258368"
		},{
			"order_no":"00003",
			"logistics":"顺丰",
			"number":"147258367"
		},{
			"order_no":"00004",
			"logistics":"顺丰速运",
			"number":""
		}]
		"""
	Then jobs获得批量发货提示错误信息
		| order_no | logistics |   number   | failure_reasons |
		|  00001   | 顺丰速运  | 147258369  |  订单状态错误   |
		|  000030  | 顺丰速运  | 147258368  |   订单号错误    |
		|  00003   |   顺丰    | 147258367  |  快递名称错误   |
		|  00004   | 顺丰速运  |            |   格式不正确    |

	When jobs根据给定条件查询订单
		"""
		{}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no":"00001",
			"member":"tom",
			"status":"待支付",
			"order_time":"2014-10-01 12:00:00",
			"methods_of_payment":"",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
		},{
			"order_no":"00002",
			"member":"bill",
			"status":"已取消",
			"order_time":"2014-10-02 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		},{
			"order_no":"00003",
			"member":"tom",
			"status":"待发货",
			"order_time":"2014-10-03 12:00:00",
			"methods_of_payment":"货到付款",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
		},{
			"order_no":"00004",
			"member":"bill",
			"status":"待发货",
			"order_time":"2014-10-04 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		},{
			"order_no":"00005",
			"member":"tom",
			"status":"待发货",
			"order_time":"2014-10-05 12:00:00",
			"methods_of_payment":"微信支付",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
		},{
			"order_no":"00006",
			"member":"tom",
			"status":"待发货",
			"order_time":"2014-10-06 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
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
			"order_no":"00008",
			"member":"bill",
			"status":"待发货",
			"order_time":"2014-10-08 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		}]
		"""


@deliver @ztq
Scenario: 3 对修改过价格的订单进行批量发货
	jobs对修改过价格的订单进行批量发货
	1.填写新的订单号也可以发货成功
	2.新生成的订单号错误，发货失败

	Given jobs登录系统
	And jobs已有的订单
		"""
		[{
			"order_no":"00011",
			"member":"bill",
			"status":"待支付",
			"final_price": 100.00,
			"order_time":"2014-10-08 12:00:00",
			"methods_of_payment":"",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		},{
			"order_no":"00010",
			"member":"bill",
			"status":"待支付",
			"final_price": 100.00,
			"order_time":"2014-10-08 12:00:00",
			"methods_of_payment":"",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		},{
			"order_no":"00009",
			"member":"bill",
			"status":"待支付",
			"final_price": 100.00,
			"order_time":"2014-10-07 12:00:00",
			"methods_of_payment":"",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}]
		"""
	When jobs修改订单'00011'的价格
		"""
		{
			"order_no": "00011",
			"final_price": 90.00
		}
		"""
	And jobs'支付'订单'00011'
	Then jobs能获得订单"00011"
		"""
		{
			"order_no":"00011-100",
			"member":"bill",
			"status":"待发货",
			"final_price": 90.00,
			"edit_money": 10.00,
			"order_time":"2014-10-08 12:00:00",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When jobs修改订单'00010'的价格
		"""
		{
			"order_no": "00010",
			"final_price": 119.00
		}
		"""
	And jobs'支付'订单'00010'
	Then jobs能获得订单"00010"
		"""
		{
			"order_no":"00010-190",
			"member":"bill",
			"status":"待发货",
			"final_price": 119.00,
			"edit_money": -19.00,
			"order_time":"2014-10-08 12:00:00",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When jobs修改订单'00009'的价格
		"""
		{
			"order_no": "00009",
			"final_price": 99.00
		}
		"""
	And jobs'支付'订单'00009'
	Then jobs能获得订单"00009"
		"""
		{
			"order_no":"00009-10",
			"member":"bill",
			"status":"待发货",
			"final_price": 99.00,
			"edit_money": 1.00,
			"order_time":"2014-10-07 12:00:00",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""

	#1.新订单号正确发货成功，2.新订单号错误发货失败，3.产生新的订单号后还使用老订单号发货成功
	When jobs填写订单信息
		"""
		[{
			"order_no":"00009-10",
			"logistics":"顺丰速运",
			"number":"147258369"
		},{
			"order_no":"00010-19",
			"logistics":"顺丰速运",
			"number":"147258368"
		},{
			"order_no":"00011",
			"logistics":"顺丰速运",
			"number":"147258367"
		}]
		"""
	Then jobs获得批量发货提示错误信息
		| order_no | logistics |   number   | failure_reasons |
		| 00010-19 | 顺丰速运  | 147258368  |   订单号错误    |

	When jobs根据给定条件查询订单
		"""
		{}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no":"00009-10",
			"member":"bill",
			"status":"已发货",
			"final_price": 99.00,
			"edit_money": 1.00,
			"order_time":"2014-10-07 12:00:00",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		},{
			"order_no":"00010-190",
			"member":"bill",
			"status":"待发货",
			"final_price": 119.00,
			"edit_money": -19.00,
			"order_time":"2014-10-08 12:00:00",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		},{
			"order_no":"00011-100",
			"member":"bill",
			"status":"已发货",
			"final_price": 90.00,
			"edit_money": 10.00,
			"order_time":"2014-10-08 12:00:00",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		},{
			"order_no":"00001",
			"member":"tom",
			"status":"待支付",
			"order_time":"2014-10-01 12:00:00",
			"methods_of_payment":"",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
		},{
			"order_no":"00002",
			"member":"bill",
			"status":"已取消",
			"order_time":"2014-10-02 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		},{
			"order_no":"00003",
			"member":"tom",
			"status":"待发货",
			"order_time":"2014-10-03 12:00:00",
			"methods_of_payment":"货到付款",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
		},{
			"order_no":"00004",
			"member":"bill",
			"status":"待发货",
			"order_time":"2014-10-04 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		},{
			"order_no":"00005",
			"member":"tom",
			"status":"待发货",
			"order_time":"2014-10-05 12:00:00",
			"methods_of_payment":"微信支付",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
		},{
			"order_no":"00006",
			"member":"tom",
			"status":"待发货",
			"order_time":"2014-10-06 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"tom",
			"ship_tel":"13711223344"
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
			"order_no":"00008",
			"member":"bill",
			"status":"待发货",
			"order_time":"2014-10-08 12:00:00",
			"methods_of_payment":"优惠抵扣",
			"sources":"商城",
			"ship_name":"bill",
			"ship_tel":"13811223344"
		}]
		"""




