# __author__ : "冯雪静"

Feature: 订单管理
"""
	Jobs能通过管理系统获取到订单列表、订单详情(修改价格、支付订单、申请退款、财务审核、退款完成、设置订单等)

	1.修改待支付订单的价格，减少订单金额,查看详情完成支付
	2.修改待支付订单的价格，增加订单金额,查看详情完成支付
	3.使用微信支付的订单，支付后可以申请退款，财务审核，退款成功
	4.使用货到付款的订单，支付后完成订单可以申请退款，财务审核，退款成功
	5.设置未付款订单过期时间，设置时间后，创建订单，在设置的时间内没有完成支付，订单自动取消，为已取消状态
		不设置过期时间，订单状态不受影响
"""

Background:
	Given jobs登录系统
	When jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用",
			"weixin_appid": "12345",
			"weixin_partner_id": "22345",
			"weixin_partner_key": "32345",
			"weixin_sign": "42345"
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"stocks": 8
		},{
			"name": "商品2",
			"price": 50.00,
			"stocks": 8
		 }]
		"""
	And bill关注jobs的公众号
	Given jobs已有的会员
		"""
		[{
			"name": "bill",
			"integral":"150"
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 50.00,
			"count": 2,
			"coupon_id_prefix": "coupon1_id_"
		},{
			"name": "优惠券2",
			"money": 50.00,
			"count": 1,
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	Given jobs设定会员积分策略
		"""
		{
			"use_ceiling": 100,
			"use_condition": "on",
			"integral_each_yuan": 10
		}
		"""
	When bill访问jobs的webapp
	And bill领取jobs的优惠券
		"""
		[{
			"name": "优惠券1",
			"coupon_ids": ["coupon1_id_1"]
		}, {
			"name": "优惠券2",
			"coupon_ids": ["coupon2_id_1"]
		}]
		"""
	And bill购买jobs的商品
		"""
		{
			"order_id": "001",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"pay_type": "微信支付",
			"date":"2015-08-08 00:00:00"
		}
		"""
	And bill购买jobs的商品
		"""
		{
			"order_id":"002",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon1_id_1",
			"pay_type": "微信支付",
			"date":"2015-08-09 00:00:00"
		}
		"""
	And bill购买jobs的商品
		"""
		{
			"order_id":"003",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"integral": 150,
			"integral_money":15.00,
			"pay_type": "微信支付",
			"date":"2015-08-10 00:00:00"
		}
		"""
	And bill购买jobs的商品
		"""
		{
			"order_id":"004",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon2_id_1",
			"pay_type": "微信支付",
			"date":"2015-08-11 00:00:00"
		}
		"""

@mall2 @order @editMoney
Scenario: 1 修改待支付订单的价格，减少订单金额
	bill创建订单后
	1.jobs修改订单'001'的价格
	2.jobs修改价格后，bill从webapp端能获取修改后的订单价格
	3.bill能进行支付修改后的订单

	Given jobs登录系统
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 50.00,
			"save_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}, {
			"order_no": "003",
			"order_time":"2015-08-10 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 85.00,
			"save_money":15.00,
			"integral": 150,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		},{
			"order_no": "002",
			"order_time":"2015-08-09 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 50.00,
			"save_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		},{
			"order_no": "001",
			"order_time":"2015-08-08 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}]
		"""
	When jobs修改订单'001'的价格
		"""
		{
			"order_no": "001",
			"final_price": 90.00
		}
		"""
	#jobs修改完价格，后台的订单号会多一个加后缀的单号
	Then jobs能获得订单'001'
		"""
		{
			"order_no": "001-100",
			"order_time":"2015-08-08 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 90.00,
			"edit_money": 10.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When bill访问jobs的webapp
	Then bill手机端获取订单'001'
		"""
		{
			"order_no": "001",
			"order_time":"2015-08-08 00:00:00",
			"methods_of_payment":"微信支付",
			"status":"待支付",
			"final_price": 90.00,
			"edit_money": 10.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When bill使用支付方式'微信支付'进行支付
	Then bill支付订单成功
		"""
		{
			"order_no": "001",
			"order_time":"2015-08-08 00:00:00",
			"methods_of_payment":"微信支付",
			"status":"待发货",
			"final_price": 90.00,
			"edit_money": 10.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	Then jobs能获得订单'001'
		"""
		{
			"order_no": "001-100",
			"order_time":"2015-08-08 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待发货",
			"actions": ["发货", "申请退款"],
			"final_price": 90.00,
			"edit_money": 10.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""

@mall2 @order @editMoney
Scenario: 2 修改待支付订单的价格，增加订单金额
	bill创建订单后
	1.jobs修改订单'002'的价格
	2.jobs修改价格后，bill从webapp端能获取修改后的订单价格
	3.bill能进行支付修改后的订单

	Given jobs登录系统
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 50.00,
			"save_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}, {
			"order_no": "003",
			"order_time":"2015-08-10 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 85.00,
			"save_money":15.00,
			"integral": 150,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		},{
			"order_no": "002",
			"order_time":"2015-08-09 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 50.00,
			"save_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		},{
			"order_no": "001",
			"order_time":"2015-08-08 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}]
		"""
	When jobs修改订单'002'的价格
		"""
		{
			"order_no": "002",
			"final_price": 90.00
		}
		"""
	#jobs修改完价格，后台的订单号会多一个加后缀的单号
	Then jobs能获得订单'002'
		"""
		{
			"order_no": "002-400",
			"order_time":"2015-08-09 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 90.00,
			"save_money": 10.00,
			"coupon_money": 50.00,
			"edit_money": -40.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When bill访问jobs的webapp
	Then bill手机端获取订单'002'
		"""
		{
			"order_no": "002",
			"order_time":"2015-08-09 00:00:00",
			"methods_of_payment":"微信支付",
			"status":"待支付",
			"final_price": 90.00,
			"coupon_money": 50.00,
			"edit_money": -40.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When bill使用支付方式'微信支付'进行支付
	Then bill支付订单成功
		"""
		{
			"order_no": "002",
			"order_time":"2015-08-09 00:00:00",
			"methods_of_payment":"微信支付",
			"status":"待发货",
			"final_price": 90.00,
			"coupon_money": 50.00,
			"edit_money": -40.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	Then jobs能获得订单'002'
		"""
		{
			"order_no": "002-400",
			"order_time":"2015-08-09 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待发货",
			"actions": ["发货", "申请退款"],
			"final_price": 90.00,
			"save_money": 10.00,
			"coupon_money": 50.00,
			"edit_money": -40.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""

@mall2 @order @finance @returnOrder
Scenario: 3 使用微信支付的订单，支付后可以申请退款
	bill创建订单后
	1.bill使用微信支付方式支付
	2.jobs申请退款
	3.bill手机端获取订单详情
	4.bill获得会员积分

	Given jobs登录系统
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 50.00,
			"save_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}, {
			"order_no": "003",
			"order_time":"2015-08-10 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 85.00,
			"save_money":15.00,
			"integral": 150,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		},{
			"order_no": "002",
			"order_time":"2015-08-09 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 50.00,
			"save_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		},{
			"order_no": "001",
			"order_time":"2015-08-08 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}]
		"""
	When jobs'支付'订单'003'
	Then jobs能获得订单'003'
		"""
		{
			"order_no": "003",
			"order_time":"2015-08-10 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待发货",
			"actions": ["发货", "申请退款"],
			"final_price": 85.00,
			"save_money":15.00,
			"integral_money":15.00,
			"integral": 150,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When jobs'申请退款'订单'003'
	Then jobs能获得订单'003'
		"""
		{
			"order_no": "003",
			"order_time":"2015-08-10 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"退款中",
			"actions": [],
			"final_price": 85.00,
			"save_money":15.00,
			"integral_money":15.00,
			"integral": 150,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When bill访问jobs的webapp
	Then bill手机端获取订单'003'
		"""
		{
			"order_no": "003",
			"order_time":"2015-08-10 00:00:00",
			"methods_of_payment":"微信支付",
			"status":"退款中",
			"final_price": 85.00,
			"integral_money":15.00,
			"integral": 150,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	when jobs根据给定条件查询订单
		"""
		{
			"order_status":"退款中"
		}
		"""

	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "003",
			"order_time":"2015-08-10 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"退款中",
			"final_price": 85.00,
			"save_money":15.00,
			"integral": 150,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}]
		"""

	When jobs通过财务审核'退款成功'订单'003'
	Then jobs能获得订单'003'
		"""
		{
			"order_no": "003",
			"order_time":"2015-08-10 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"退款成功",
			"actions": [],
			"final_price": 85.00,
			"save_money":15.00,
			"integral_money":15.00,
			"integral": 150,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When bill访问jobs的webapp
	Then bill手机端获取订单'003'
		"""
		{
			"order_no": "003",
			"order_time":"2015-08-10 00:00:00",
			"methods_of_payment":"微信支付",
			"status":"退款成功",
			"final_price": 85.00,
			"integral_money":15.00,
			"integral": 150,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	And bill在jobs的webapp中拥有150会员积分

@mall2 @order @finance @returnOrder
Scenario: 4 使用货到付款的订单，支付后完成订单可以申请退款
	bill创建订单后
	1.bill使用货到付款方式支付
	2.jobs完成订单，申请退款
	3.bill手机端获取订单详情
	4.bill获得优惠券列表

	Given jobs登录系统
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 50.00,
			"save_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}, {
			"order_no": "003",
			"order_time":"2015-08-10 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 85.00,
			"save_money":15.00,
			"integral": 150,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		},{
			"order_no": "002",
			"order_time":"2015-08-09 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 50.00,
			"save_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		},{
			"order_no": "001",
			"order_time":"2015-08-08 00:00:00",
			"methods_of_payment":"微信支付",
			"member": "bill",
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}]
		"""
	When bill访问jobs的webapp
	When bill使用支付方式'货到付款'进行支付订单'004'
	Then bill支付订单成功
		"""
		{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"货到付款",
			"status":"待发货",
			"final_price": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	Then jobs能获得订单'004'
		"""
		{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"货到付款",
			"member": "bill",
			"status":"待发货",
			"actions": ["发货", "取消订单"],
			"final_price": 50.00,
			"save_money": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	when jobs填写发货信息
		"""
		[{
		 	"order_no": "004"
		}]
		"""
	Then jobs能获得订单'004'
		"""
		{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"货到付款",
			"member": "bill",
			"status":"已发货",
			"actions": ["标记完成", "取消订单", "修改物流"],
			"final_price": 50.00,
			"save_money": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When bill访问jobs的webapp
	Then bill手机端获取订单'004'
		"""
		{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"货到付款",
			"status":"待收货",
			"final_price": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	When jobs完成订单'004'
	Then jobs能获得订单'004'
		"""
		{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"货到付款",
			"member": "bill",
			"status":"已完成",
			"actions": ["申请退款"],
			"final_price": 50.00,
			"save_money": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When bill访问jobs的webapp
	Then bill手机端获取订单'004'
		"""
		{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"货到付款",
			"status":"已完成",
			"final_price": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	When jobs'申请退款'订单'004'
	Then jobs能获得订单'004'
		"""
		{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"货到付款",
			"member": "bill",
			"status":"退款中",
			"actions": [],
			"final_price": 50.00,
			"save_money": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When bill访问jobs的webapp
	Then bill手机端获取订单'004'
		"""
		{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"货到付款",
			"status":"退款中",
			"final_price": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
  	when jobs根据给定条件查询订单
		"""
		{
			"order_status":"退款中"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"货到付款",
			"member": "bill",
			"status":"退款中",
			"final_price": 50.00,
			"save_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}]
		"""
	When jobs通过财务审核'退款成功'订单'004'
	Then jobs能获得订单'004'
		"""
		{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"货到付款",
			"member": "bill",
			"status":"退款成功",
			"actions": [],
			"final_price": 50.00,
			"save_money": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When bill访问jobs的webapp
	Then bill手机端获取订单'004'
		"""
		{
			"order_no": "004",
			"order_time":"2015-08-11 00:00:00",
			"methods_of_payment":"货到付款",
			"status":"退款成功",
			"final_price": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_1",
			"money": 50.00,
			"status": "未使用"
		}]
		"""

@mall2 @order @setOrder
Scenario: 5 设置未付款订单过期时间
	jobs设置未付款订单过期时间后
	1.bill创建订单后，未支付订单的时间超过了过期时间
	2.订单自动变为取消状态
	3.jobs获取优惠券详情
	4.过期时间为空，为不限制

	Given jobs登录系统
	#订单过期时间是按照小时计算
	When jobs设置未付款订单过期时间24小时
	When bill访问jobs的webapp
	And bill领取jobs的优惠券
		"""
		[{
			"name": "优惠券1",
			"coupon_ids": ["coupon1_id_2"]
		}]
		"""
	And bill购买jobs的商品
		"""
		{
			"date":"1天前",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon1_id_2"
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status":"待支付",
			"final_price": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	#jobs1天后查看最新订单，状态为已取消
	Given jobs登录系统
	When jobs触发订单超时取消任务
	Then jobs可以获得最新订单详情
		"""
		{
			"status":"已取消",
			"actions": [],
			"final_price": 50.00,
			"save_money": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	And jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 50.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 50.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""
	#jobs设置订单过期时间为空
	When jobs设置未付款订单过期时间0小时
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon1_id_2"
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status":"待支付",
			"final_price": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	#jobs1天后查看最新订单，状态为待支付
	Given jobs登录系统
	Then jobs可以获得最新订单详情
		"""
		{
			"status":"待支付",
			"actions": ["修改价格", "取消订单", "支付"],
			"final_price": 50.00,
			"save_money": 50.00,
			"coupon_money": 50.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	And jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 50.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 50.00,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			}
		}
		"""

# __author__ : "王丽" 2016-02-02
@order @setOrder @XXXX
Scenario:6 支付后的订单，添加首单标记-会员订单
	#用户支付的订单，按照【付款时间】付款时间最早的标记为“首单”
	#非会员购买的订单，【买家】修改成“非会员”，关注之后显示成会员名称
	#非会员购买首单按照会员的规则处理

	#没有支付的订单
		Given jobs登录系统
		Then jobs可以看到订单列表
			"""
			[{
				"order_no": "004",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-11 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "003",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-10 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "002",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-09 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "001",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-08 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			}]
			"""

	#有多个支付的订单-手机端支付和后台支付，支付时间最早的标记为首单
		When bill访问jobs的webapp
		When bill使用支付方式'微信支付'进行支付订单'002'于2015-09-01 10:00:00

		Given jobs登录系统
		When jobs'支付'订单'003'于2015-09-02 10:00:00

		Then jobs可以看到订单列表
			"""
			[{
				"order_no": "004",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-11 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "003",
				"member": "bill",
				"status": "待发货",
				"order_time": "2015-08-10 00:00:00",
				"payment_time":"2015-09-02 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "002",
				"member": "bill",
				"status": "待发货",
				"order_time": "2015-08-09 00:00:00",
				"payment_time":"2015-09-01 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"true"
			},{
				"order_no": "001",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-08 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			}]
			"""

	#取消有首单标记的订单，首单标记仍然存在
		Given jobs登录系统
		When jobs'取消'订单'002'
		Then jobs可以看到订单列表
			"""
			[{
				"order_no": "004",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-11 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "003",
				"member": "bill",
				"status": "待发货",
				"order_time": "2015-08-10 00:00:00",
				"payment_time":"2015-09-02 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "002",
				"member": "bill",
				"status": "已取消",
				"order_time": "2015-08-09 00:00:00",
				"payment_time":"2015-09-01 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"true"
			},{
				"order_no": "001",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-08 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			}]
			"""

	#货到付款的订单
		Given tom关注jobs的公众号
		When tom访问jobs的webapp

		When tom购买jobs的商品
			"""
			{
				"order_id":"005",
				"products": [{
					"name": "商品2",
					"count": 1
				}],
				"pay_type": "货到付款",
				"date":"2015-08-12 00:00:00"
			}
			"""
		When tom购买jobs的商品
			"""
			{
				"order_id":"006",
				"products": [{
					"name": "商品2",
					"count": 1
				}],
				"pay_type": "货到付款",
				"date":"2015-08-13 00:00:00"
			}
			"""

		Given jobs登录系统
		Then jobs可以看到订单列表
			"""
			[{
				"order_no": "006",
				"member": "tom",
				"status": "待发货",
				"order_time": "2015-08-13 00:00:00",
				"payment_time":"2015-08-13 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"false"
			},{
				"order_no": "005",
				"member": "tom",
				"status": "待发货",
				"order_time": "2015-08-12 00:00:00",
				"payment_time":"2015-08-12 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"true"
			},{
				"order_no": "004",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-11 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "003",
				"member": "bill",
				"status": "待发货",
				"order_time": "2015-08-10 00:00:00",
				"payment_time":"2015-09-02 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "002",
				"member": "bill",
				"status": "已取消",
				"order_time": "2015-08-09 00:00:00",
				"payment_time":"2015-09-01 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"true"
			},{
				"order_no": "001",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-08 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			}]
			"""

		When jobs对订单进行发货
			"""
			{
				"order_no":"005",
				"logistics":"顺丰速运",
				"number":"123456789",
				"shipper":"jobs|发货一箱",
				"date":"今天"
			}
			"""
		Then jobs可以看到订单列表
			"""
			[{
				"order_no": "006",
				"member": "tom",
				"status": "待发货",
				"order_time": "2015-08-13 00:00:00",
				"payment_time":"2015-08-13 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"false"
			},{
				"order_no": "005",
				"member": "tom",
				"status": "已发货",
				"order_time": "2015-08-12 00:00:00",
				"payment_time":"2015-08-12 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"true"
			},{
				"order_no": "004",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-11 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "003",
				"member": "bill",
				"status": "待发货",
				"order_time": "2015-08-10 00:00:00",
				"payment_time":"2015-09-02 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "002",
				"member": "bill",
				"status": "已取消",
				"order_time": "2015-08-09 00:00:00",
				"payment_time":"2015-09-01 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"true"
			},{
				"order_no": "001",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-08 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			}]
			"""

		When jobs'完成'订单'005'
		Then jobs可以看到订单列表
			"""
			[{
				"order_no": "006",
				"member": "tom",
				"status": "待发货",
				"order_time": "2015-08-13 00:00:00",
				"payment_time":"2015-08-13 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"false"
			},{
				"order_no": "005",
				"member": "tom",
				"status": "已完成",
				"order_time": "2015-08-12 00:00:00",
				"payment_time":"2015-08-12 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"true"
			},{
				"order_no": "004",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-11 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "003",
				"member": "bill",
				"status": "待发货",
				"order_time": "2015-08-10 00:00:00",
				"payment_time":"2015-09-02 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "002",
				"member": "bill",
				"status": "已取消",
				"order_time": "2015-08-09 00:00:00",
				"payment_time":"2015-09-01 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"true"
			},{
				"order_no": "001",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-08 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			}]
			"""

		When jobs'申请退款'订单'005'
		Then jobs可以看到订单列表
			"""
			[{
				"order_no": "006",
				"member": "tom",
				"status": "待发货",
				"order_time": "2015-08-13 00:00:00",
				"payment_time":"2015-08-13 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"false"
			},{
				"order_no": "005",
				"member": "tom",
				"status": "退款中",
				"order_time": "2015-08-12 00:00:00",
				"payment_time":"2015-08-12 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"true"
			},{
				"order_no": "004",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-11 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "003",
				"member": "bill",
				"status": "待发货",
				"order_time": "2015-08-10 00:00:00",
				"payment_time":"2015-09-02 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "002",
				"member": "bill",
				"status": "已取消",
				"order_time": "2015-08-09 00:00:00",
				"payment_time":"2015-09-01 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"true"
			},{
				"order_no": "001",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-08 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			}]
			"""

		When jobs通过财务审核'退款成功'订单'005'
		Then jobs可以看到订单列表
			"""
			[{
				"order_no": "006",
				"member": "tom",
				"status": "待发货",
				"order_time": "2015-08-13 00:00:00",
				"payment_time":"2015-08-13 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"false"
			},{
				"order_no": "005",
				"member": "tom",
				"status": "退款成功",
				"order_time": "2015-08-12 00:00:00",
				"payment_time":"2015-08-12 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"true"
			},{
				"order_no": "004",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-11 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "003",
				"member": "bill",
				"status": "待发货",
				"order_time": "2015-08-10 00:00:00",
				"payment_time":"2015-09-02 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "002",
				"member": "bill",
				"status": "已取消",
				"order_time": "2015-08-09 00:00:00",
				"payment_time":"2015-09-01 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"true"
			},{
				"order_no": "001",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-08 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			}]
			"""

	#优惠抵扣的订单
		Given jack关注jobs的公众号
		When jack领取jobs的优惠券
			"""
			[{
				"name": "优惠券1",
				"coupon_ids": ["coupon1_id_2"]
			}]
			"""
		Given jobs已有的会员
			"""
			[{
				"name": "jack",
				"integral":"1000"
			}]
			"""

		When jack访问jobs的webapp
		And jack购买jobs的商品
			"""
			{
				"order_id":"007",
				"products": [{
					"name": "商品2",
					"count": 1
				}],
				"coupon": "coupon1_id_2",
				"pay_type": "微信支付",
				"date":"2015-08-14 00:00:00"
			}
			"""
		And jack购买jobs的商品
			"""
			{
				"order_id":"008",
				"products": [{
					"name": "商品2",
					"count": 1
				}],
				"integral": 500,
				"integral_money":50.00,
				"pay_type": "微信支付",
				"date":"2015-08-15 00:00:00"
			}
			"""

		Given jobs登录系统
		Then jobs可以看到订单列表
			"""
			[{
				"order_no": "008",
				"member": "jack",
				"status": "待发货",
				"order_time": "2015-08-15 00:00:00",
				"payment_time":"2015-08-15 00:00:00",
				"methods_of_payment": "优惠抵扣",
				"is_first_order":"false"
			},{
				"order_no": "007",
				"member": "jack",
				"status": "待发货",
				"order_time": "2015-08-14 00:00:00",
				"payment_time":"2015-08-14 00:00:00",
				"methods_of_payment": "优惠抵扣",
				"is_first_order":"true"
			},{
				"order_no": "006",
				"member": "tom",
				"status": "待发货",
				"order_time": "2015-08-13 00:00:00",
				"payment_time":"2015-08-13 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"false"
			},{
				"order_no": "005",
				"member": "tom",
				"status": "退款成功",
				"order_time": "2015-08-12 00:00:00",
				"payment_time":"2015-08-12 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"true"
			},{
				"order_no": "004",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-11 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "003",
				"member": "bill",
				"status": "待发货",
				"order_time": "2015-08-10 00:00:00",
				"payment_time":"2015-09-02 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "002",
				"member": "bill",
				"status": "已取消",
				"order_time": "2015-08-09 00:00:00",
				"payment_time":"2015-09-01 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"true"
			},{
				"order_no": "001",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-08 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			}]
			"""

		When jobs对订单进行发货
			"""
			{
				"order_no":"007",
				"logistics":"顺丰速运",
				"number":"123456789",
				"shipper":"jobs|发货一箱",
				"date":"今天"
			}
			"""
		Then jobs可以看到订单列表
			"""
			[{
				"order_no": "008",
				"member": "jack",
				"status": "待发货",
				"order_time": "2015-08-15 00:00:00",
				"payment_time":"2015-08-15 00:00:00",
				"methods_of_payment": "优惠抵扣",
				"is_first_order":"false"
			},{
				"order_no": "007",
				"member": "jack",
				"status": "已发货",
				"order_time": "2015-08-14 00:00:00",
				"payment_time":"2015-08-14 00:00:00",
				"methods_of_payment": "优惠抵扣",
				"is_first_order":"true"
			},{
				"order_no": "006",
				"member": "tom",
				"status": "待发货",
				"order_time": "2015-08-13 00:00:00",
				"payment_time":"2015-08-13 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"false"
			},{
				"order_no": "005",
				"member": "tom",
				"status": "退款成功",
				"order_time": "2015-08-12 00:00:00",
				"payment_time":"2015-08-12 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"true"
			},{
				"order_no": "004",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-11 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "003",
				"member": "bill",
				"status": "待发货",
				"order_time": "2015-08-10 00:00:00",
				"payment_time":"2015-09-02 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "002",
				"member": "bill",
				"status": "已取消",
				"order_time": "2015-08-09 00:00:00",
				"payment_time":"2015-09-01 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"true"
			},{
				"order_no": "001",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-08 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			}]
			"""

		When jobs'完成'订单'007'
		Then jobs可以看到订单列表
			"""
			[{
				"order_no": "008",
				"member": "jack",
				"status": "待发货",
				"order_time": "2015-08-15 00:00:00",
				"payment_time":"2015-08-15 00:00:00",
				"methods_of_payment": "优惠抵扣",
				"is_first_order":"false"
			},{
				"order_no": "007",
				"member": "jack",
				"status": "已完成",
				"order_time": "2015-08-14 00:00:00",
				"payment_time":"2015-08-14 00:00:00",
				"methods_of_payment": "优惠抵扣",
				"is_first_order":"true"
			},{
				"order_no": "006",
				"member": "tom",
				"status": "待发货",
				"order_time": "2015-08-13 00:00:00",
				"payment_time":"2015-08-13 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"false"
			},{
				"order_no": "005",
				"member": "tom",
				"status": "退款成功",
				"order_time": "2015-08-12 00:00:00",
				"payment_time":"2015-08-12 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"true"
			},{
				"order_no": "004",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-11 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "003",
				"member": "bill",
				"status": "待发货",
				"order_time": "2015-08-10 00:00:00",
				"payment_time":"2015-09-02 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "002",
				"member": "bill",
				"status": "已取消",
				"order_time": "2015-08-09 00:00:00",
				"payment_time":"2015-09-01 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"true"
			},{
				"order_no": "001",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-08 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			}]
			"""

		When jobs'取消'订单'007'
		Then jobs可以看到订单列表
			"""
			[{
				"order_no": "008",
				"member": "jack",
				"status": "待发货",
				"order_time": "2015-08-15 00:00:00",
				"payment_time":"2015-08-15 00:00:00",
				"methods_of_payment": "优惠抵扣",
				"is_first_order":"false"
			},{
				"order_no": "007",
				"member": "jack",
				"status": "已取消",
				"order_time": "2015-08-14 00:00:00",
				"payment_time":"2015-08-14 00:00:00",
				"methods_of_payment": "优惠抵扣",
				"is_first_order":"true"
			},{
				"order_no": "006",
				"member": "tom",
				"status": "待发货",
				"order_time": "2015-08-13 00:00:00",
				"payment_time":"2015-08-13 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"false"
			},{
				"order_no": "005",
				"member": "tom",
				"status": "退款成功",
				"order_time": "2015-08-12 00:00:00",
				"payment_time":"2015-08-12 00:00:00",
				"methods_of_payment": "货到付款",
				"is_first_order":"true"
			},{
				"order_no": "004",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-11 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "003",
				"member": "bill",
				"status": "待发货",
				"order_time": "2015-08-10 00:00:00",
				"payment_time":"2015-09-02 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			},{
				"order_no": "002",
				"member": "bill",
				"status": "已取消",
				"order_time": "2015-08-09 00:00:00",
				"payment_time":"2015-09-01 10:00:00",
				"methods_of_payment": "微信支付",
				"is_first_order":"true"
			},{
				"order_no": "001",
				"member": "bill",
				"status": "待支付",
				"order_time": "2015-08-08 00:00:00",
				"payment_time":"",
				"methods_of_payment": "微信支付",
				"is_first_order":"false"
			}]
			"""

# __author__ : "王丽" 2016-02-02
@order @setOrder
Scenario:7 支付后的订单，添加首单标记-非会员订单
	#用户支付的订单，按照【付款时间】付款时间最早的标记为“首单”
	#非会员购买的订单，【买家】修改成“非会员”，关注之后显示成会员名称
	#非会员购买首单按照会员的规则处理

	When marry访问jobs的webapp
	And marry购买jobs的商品
		"""
		{
			"order_id":"009",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon2_id_1",
			"pay_type": "支付宝",
			"date":"2015-08-12 00:00:00"
		}
		"""
	When marry使用支付方式'支付宝'进行支付订单'002'于'2015-08-12 10:00:00'
	And marry购买jobs的商品
		"""
		{
			"order_id":"010",
			"products": [{
				"name": "商品2",
				"count": 1
			}],
			"coupon": "coupon2_id_1",
			"pay_type": "货到付款",
			"date":"2015-08-13 00:00:00"
		}
		"""

	Given jobs登录系统
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "010",
			"member": "非会员",
			"status": "待发货",
			"order_time": "2015-08-13 00:00:00",
			"payment_time":"2015-08-13 00:00:00",
			"methods_of_payment": "货到付款",
			"is_first_order":"false"
		},{
			"order_no": "009",
			"member": "非会员",
			"status": "待发货",
			"order_time": "2015-08-12 00:00:00",
			"payment_time":"2015-08-12 10:00:00",
			"methods_of_payment": "支付宝",
			"is_first_order":"true"
		},{
			"order_no": "004",
			"member": "bill",
			"status": "待支付",
			"order_time": "2015-08-11 00:00:00",
			"payment_time":"",
			"methods_of_payment": "微信支付",
			"is_first_order":"false"
		},{
			"order_no": "003",
			"member": "bill",
			"status": "待支付",
			"order_time": "2015-08-10 00:00:00",
			"payment_time":"",
			"methods_of_payment": "微信支付",
			"is_first_order":"false"
		},{
			"order_no": "002",
			"member": "bill",
			"status": "待支付",
			"order_time": "2015-08-09 00:00:00",
			"payment_time":"",
			"methods_of_payment": "微信支付",
			"is_first_order":"false"
		},{
			"order_no": "001",
			"member": "bill",
			"status": "待支付",
			"order_time": "2015-08-08 00:00:00",
			"payment_time":"",
			"methods_of_payment": "微信支付",
			"is_first_order":"false"
		}]
		"""

	Given marry关注jobs的公众号
	When marry访问jobs的webapp
	Given jobs登录系统
	Then jobs可以看到订单列表
		"""
		[{
			"order_no": "010",
			"member": "marry",
			"status": "待发货",
			"order_time": "2015-08-13 00:00:00",
			"payment_time":"2015-08-13 00:00:00",
			"methods_of_payment": "货到付款",
			"is_first_order":"false"
		},{
			"order_no": "009",
			"member": "marry",
			"status": "待发货",
			"order_time": "2015-08-12 00:00:00",
			"payment_time":"2015-08-12 10:00:00",
			"methods_of_payment": "支付宝",
			"is_first_order":"true"
		},{
			"order_no": "004",
			"member": "bill",
			"status": "待支付",
			"order_time": "2015-08-11 00:00:00",
			"payment_time":"",
			"methods_of_payment": "微信支付",
			"is_first_order":"false"
		},{
			"order_no": "003",
			"member": "bill",
			"status": "待支付",
			"order_time": "2015-08-10 00:00:00",
			"payment_time":"",
			"methods_of_payment": "微信支付",
			"is_first_order":"false"
		},{
			"order_no": "002",
			"member": "bill",
			"status": "待支付",
			"order_time": "2015-08-09 00:00:00",
			"payment_time":"",
			"methods_of_payment": "微信支付",
			"is_first_order":"false"
		},{
			"order_no": "001",
			"member": "bill",
			"status": "待支付",
			"order_time": "2015-08-08 00:00:00",
			"payment_time":"",
			"methods_of_payment": "微信支付",
			"is_first_order":"false"
		}]
		"""
