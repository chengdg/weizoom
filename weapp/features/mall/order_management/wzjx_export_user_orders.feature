# __author__ : "冯雪静"
#微众精选：导出订单
Feature:用户订单导出功能
	jobs能导出用户的订单
	"""
	1.微众精选：导出订单：不同状态，不同供货商
	"""

Background:
	Given jobs登录系统
	And jobs已添加供货商
		"""
		[{
			"name": "土小宝",
			"responsible_person": "宝宝",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}, {
			"name": "丹江湖",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}]
		"""
	And jobs设定会员积分策略
		"""
		{
			"use_ceiling": 50,
			"use_condition": "on",
			"integral_each_yuan": 1
		}
		"""
	When bill关注jobs的公众号
	Given jobs登录系统
	Given jobs已有的会员
		"""
		[{
			"name": "bill",
			"integral":"50"
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
	And jobs已添加商品
		"""
		[{
			"supplier": "土小宝",
			"name": "商品1",
			"purchase_price": 9.00,
			"price": 100.00
		}, {
			"supplier": "丹江湖",
			"name": "商品2",
			"purchase_price": 9.00,
			"price": 100.00
		}, {
			"supplier": "土小宝",
			"name": "商品3",
			"price": 100.00
		}, {
			"supplier": "丹江湖",
			"name": "商品4",
			"price": 100.00
		}, {
			"supplier": "土小宝",
			"name": "商品5",
			"price": 100.00
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 50.00,
			"count": 2,
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When bill访问jobs的webapp
	When bill领取jobs的优惠券
		"""
		[{
			"name": "优惠券1",
			"coupon_ids": ["coupon1_id_1"]
		}]
		"""
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
		{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"member_grade": "全部",
			"count_per_purchase": 2,
			"promotion_price": 50.00
		}
		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "商品2买一赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品2",
			"premium_products": [{
				"name": "商品3",
				"count": 1
			}],
			"count": 1,
			"member_grade":"全部",
			"is_enable_cycle_mode": true
		}]
		"""


@supplier @order @mall2 @order_export
Scenario: 1 不同供货商订单导出
	jobs可以导出订单

	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_no": "0000001",
			"date": "今天",
			"products": [{
				"name": "商品1",
				"count": 1
			}, {
				"name": "商品2",
				"count": 1
			}, {
				"name": "商品3",
				"count": 1
			}],
			"coupon": "coupon1_id_1"
		}
		"""
	When bill使用支付方式'货到付款'进行支付订单'0000001'
	Given jobs登录系统
	When jobs对订单进行发货
		"""
		{
			"order_no":"0000001-丹江湖",
			"logistics":"顺丰速运",
			"number":"123456789"
		}
		"""
	When jobs'取消'订单'0000001'
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_no": "0000002",
			"date": "今天",
			"ship_tel": "13811223344",
			"products": [{
				"name": "商品1",
				"count": 1
			}, {
				"name": "商品2",
				"count": 1
			}, {
				"name": "商品3",
				"count": 1
			}],
			"integral": 50
		}
		"""
	When bill使用支付方式'微信支付'进行支付订单'0000002'
	Given jobs登录系统
	When jobs对订单进行发货
		"""
		{
			"order_no":"0000002-丹江湖",
			"logistics":"顺丰速运",
			"number":"123456789"
		}
		"""
	When jobs对订单进行发货
		"""
		{
			"order_no": "0000002-土小宝",
			"logistics": "off",
			"shipper": ""
		}
		"""
	When jobs'申请退款'订单'0000002'
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_no": "0000003",
			"date": "今天",
			"products": [{
				"name": "商品3",
				"count": 1
			}, {
				"name": "商品5",
				"count": 1
			}]
		}
		"""
	When bill使用支付方式'货到付款'进行支付订单'0000003'
	Given jobs登录系统
	When jobs对订单进行发货
		"""
		{
			"order_no":"0000003",
			"logistics":"顺丰速运",
			"number":"123456789"
		}
		"""
	When jobs'完成'订单'0000003'
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_no": "0000004",
			"date": "今天",
			"products": [{
				"name": "商品4",
				"count": 1
			}, {
				"name": "商品5",
				"count": 1
			}]
		}
		"""
	When bill使用支付方式'货到付款'进行支付订单'0000004'
	Given jobs登录系统
	When jobs对订单进行发货
		"""
		{
			"order_no":"0000004-丹江湖",
			"logistics":"顺丰速运",
			"number":"123456789"
		}
		"""
	When jobs对订单进行发货
		"""
		{
			"order_no":"0000004-土小宝",
			"logistics":"顺丰速运",
			"number":"123456789"
		}
		"""
	When jobs'完成'订单'0000004'
		"""
		{
			"order_no":"0000004",
			"supplier":"土小宝"
		}
		"""
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_no": "0000005",
			"date": "今天",
			"products": [{
				"name": "商品3",
				"count": 1
			}, {
				"name": "商品5",
				"count": 1
			}]
		}
		"""
	When bill使用支付方式'货到付款'进行支付订单'0000005'
	Given jobs登录系统
	When jobs对订单进行发货
		"""
		{
			"order_no": "0000005",
			"logistics": "off",
			"shipper": ""
		}
		"""
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_no": "0000006",
			"date": "今天",
			"products": [{
				"name": "商品3",
				"count": 1
			}, {
				"name": "商品5",
				"count": 1
			}]
		}
		"""
	When bill使用支付方式'货到付款'进行支付订单'0000006'
	When bill购买jobs的商品
		"""
		{
			"order_no": "0000007",
			"date": "今天",
			"products": [{
				"name": "商品4",
				"count": 1
			}, {
				"name": "商品5",
				"count": 1
			}]
		}
		"""
	When bill使用支付方式'货到付款'进行支付订单'0000007'
	Given jobs登录系统
	When jobs对订单进行发货
		"""
		{
			"order_no":"0000007-丹江湖",
			"logistics":"顺丰速运",
			"number":"123456789"
		}
		"""
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_no": "0000008",
			"date": "今天",
			"products": [{
				"name": "商品4",
				"count": 1
			}, {
				"name": "商品5",
				"count": 1
			}]
		}
		"""
	When bill购买jobs的商品
		"""
		{
			"order_no": "0000009",
			"date": "今天",
			"products": [{
				"name": "商品3",
				"count": 1
			}, {
				"name": "商品5",
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	Then jobs导出订单获取订单信息
	| order_no       | sources |  order_time | pay_time | member | product_name | purchase_price | product_unit_price | count | purchase_costs | sales_money | money_total | integral | coupon_money | coupon_name | money_wcard | money |  status   | logistics |   number  | delivery_time |
	| 0000009        | 土小宝  |     今天    |          |  bill  |    商品3     |                |        100.0       |   1   |                |    100.0    |     0.0     |          |              |             |             |  0.0  |  待支付   |           |           |               |
	| 0000009        | 土小宝  |     今天    |          |  bill  |    商品5     |                |        100.0       |   1   |                |    100.0    |             |          |              |             |             |       |  待支付   |           |           |               |
	| 0000008-丹江湖 | 丹江湖  |     今天    |          |  bill  |    商品4     |                |        100.0       |   1   |                |    100.0    |     0.0     |          |              |             |             |  0.0  |  待支付   |           |           |               |
	| 0000008-土小宝 | 土小宝  |     今天    |          |  bill  |    商品5     |                |        100.0       |   1   |                |    100.0    |             |          |              |             |             |       |  待支付   |           |           |               |
	| 0000007-丹江湖 | 丹江湖  |     今天    |   今天   |  bill  |    商品4     |                |        100.0       |   1   |                |    100.0    |    200.0    |     0.0  |              |             |     0.0     | 200.0 |  已发货   | 顺丰速运  | 123456789 |      今天     |
	| 0000007-土小宝 | 土小宝  |     今天    |   今天   |  bill  |    商品5     |                |        100.0       |   1   |                |    100.0    |             |          |              |             |             |       |  待发货   |           |           |               |
	| 0000006        | 土小宝  |     今天    |   今天   |  bill  |    商品3     |                |        100.0       |   1   |                |    100.0    |    200.0    |     0.0  |              |             |     0.0     | 200.0 |  待发货   |           |           |               |
	| 0000006        | 土小宝  |     今天    |   今天   |  bill  |    商品5     |                |        100.0       |   1   |                |    100.0    |             |          |              |             |             |       |  待发货   |           |           |               |
	| 0000005        | 土小宝  |     今天    |   今天   |  bill  |    商品3     |                |        100.0       |   1   |                |    100.0    |    200.0    |     0.0  |              |             |     0.0     | 200.0 |  已发货   |           |           |      今天     |
	| 0000005        | 土小宝  |     今天    |   今天   |  bill  |    商品5     |                |        100.0       |   1   |                |    100.0    |             |          |              |             |             |       |  已发货   |           |           |      今天     |
	| 0000004-丹江湖 | 丹江湖  |     今天    |   今天   |  bill  |    商品4     |                |        100.0       |   1   |                |    100.0    |    200.0    |     0.0  |              |             |     0.0     | 200.0 |  已完成   | 顺丰速运  | 123456789 |      今天     |
	| 0000004-土小宝 | 土小宝  |     今天    |   今天   |  bill  |    商品5     |                |        100.0       |   1   |                |    100.0    |             |          |              |             |             |       |  已完成   | 顺丰速运  | 123456789 |      今天     |
	| 0000003        | 土小宝  |     今天    |   今天   |  bill  |    商品3     |                |        100.0       |   1   |                |    100.0    |    200.0    |     0.0  |              |             |     0.0     | 200.0 |  已完成   | 顺丰速运  | 123456789 |      今天     |
	| 0000003        | 土小宝  |     今天    |   今天   |  bill  |    商品5     |                |        100.0       |   1   |                |    100.0    |             |          |              |             |             |       |  已完成   | 顺丰速运  | 123456789 |      今天     |
	| 0000002-土小宝 | 土小宝  |     今天    |   今天   |  bill  |    商品1     |      9.0       |        50.0        |   1   |      9.0       |    50.0     |    200.0    |    50.0  |              |             |     0.0     | 200.0 |  退款中   |          |           |      今天     |
	| 0000002-丹江湖 | 丹江湖  |     今天    |   今天   |  bill  |    商品2     |      9.0       |        100.0       |   1   |      9.0       |    100.0    |             |          |              |             |             |       |  退款中   | 顺丰速运  | 123456789 |      今天     |
	| 0000002-丹江湖 | 丹江湖  |     今天    |   今天   |  bill  | (赠品)商品3  |                |        100.0       |   1   |                |    0.0      |             |          |              |             |             |       |  退款中   | 顺丰速运  | 123456789 |      今天     |
	| 0000002-土小宝 | 土小宝  |     今天    |   今天   |  bill  |    商品3     |                |        100.0       |   1   |                |    100.0    |             |          |              |             |             |       |  退款中   |           |           |      今天     |
	| 0000001-土小宝 | 土小宝  |     今天    |   今天   |  bill  |    商品1     |      9.0       |        50.0        |   1   |      9.0       |    50.0     |      0.0    |     0.0  |              |             |     0.0     |   0.0 |  已取消   |           |           |               |
	| 0000001-丹江湖 | 丹江湖  |     今天    |   今天   |  bill  |    商品2     |      9.0       |        100.0       |   1   |      9.0       |    100.0    |             |          |              |             |             |       |  已取消   | 顺丰速运  | 123456789 |      今天     |
	| 0000001-丹江湖 | 丹江湖  |     今天    |   今天   |  bill  | (赠品)商品3  |                |        100.0       |   1   |                |    0.0      |             |          |              |             |             |       |  已取消   | 顺丰速运  | 123456789 |      今天     |
	| 0000001-土小宝 | 土小宝  |     今天    |   今天   |  bill  |    商品3     |                |        100.0       |   1   |                |    100.0    |             |          |              |             |             |       |  已取消   |           |           |               |

	Then jobs导出订单获取订单统计信息
		"""
		[{
			"订单量":9,
			"已完成":2,
			"商品金额":1900.00,
			"支付总额":1200.00,
			"现金支付金额":1200.00,
			"微众卡支付金额":0.00,
			"赠品总数":1,
			"积分抵扣总金额":50.00,
			"优惠劵价值总额":0.00
		}]
		"""


