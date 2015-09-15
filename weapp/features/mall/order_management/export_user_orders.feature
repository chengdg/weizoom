# __author__ : "冯雪静"

Feature:用户订单导出功能
	jobs能导出用户的订单
	"""
	1.导出全部订单
	2.导出促销订单
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
		}, {
			"type": "支付宝",
			"description": "我的支付宝",
			"is_active": "启用",
			"partner": "11",
			"key": "21",
			"ali_public_key": "31",
			"private_key": "41",
			"seller_email": "a@a.com"
		}]
		"""
	When jobs开通使用微众卡权限
	When jobs添加支付方式
		"""
		[{
			"type": "微众卡支付",
			"description": "我的微众卡支付",
			"is_active": "启用"
		}]
		"""
	Given jobs已创建微众卡
		"""
		{
			"cards": [{
				"id": "0000001",
				"password": "1",
				"status": "未激活",
				"price": 100
			}]
		}
		"""
	When jobs给id为'0000001'的微众卡激活
	When jobs添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":10.00,
			"added_weight":1,
			"added_weight_price":5.00
		}]
		"""
	And jobs选择'顺丰'运费配置
	And jobs已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "红色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}]
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "L"
			}, {
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"红色 L": {
						"price": 100.00,
						"weight": 1
					},
					"红色 M": {
						"price": 100.00,
						"weight": 1
					},
					"红色 S": {
						"price": 100.00,
						"weight": 1
					}
				}
			},
			"unified_postage_money": 10
		},{
			"name": "商品2",
			"price": 100.00,
			"weight": 1,
			"unified_postage_money": 10
		},{
			"name": "商品3",
			"price": 100.00,
			"weight": 0
		}]
		"""
	And bill关注jobs的公众号
	And bill设置jobs的webapp的收货地址
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"area": "北京市,北京市,海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
	Given jobs登录系统
	And jobs已有的会员
		"""
		[{
			"name": "bill",
			"integral": 500
		}]
		"""
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券",
			"money": 100.00,
			"count": 1,
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2,
			"use_ceiling": 50
		}
		"""


@mall2 @order
Scenario: 导出全部订单
	jobs可以导出全部订单

	When 微信用户批量消费jobs的商品
		| order_id | date | payment_time | consumer | type | businessman |      product   | payment | pay_type | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   |
		|  000001  | 3天前 |    3天前     | bill     | 购买 |   jobs      | 商品1,红色 L,1  |   支付    |  微信支付 |      100      |  0       |              |              |    110      |         |    待发货       |
		|  000002  | 3天前 |              | bill     | 购买 |   jobs      | 商品1,红色 M,1 |           |  微信支付 |      100      |  0       |              |              |    110      |         |    待支付       |
		|  000003  | 3天前 |              | bill     | 购买 |   jobs      | 商品1,红色 S,1 |           |  微信支付 |      100      |  0       |              |              |    110      |jobs,取消|    已取消       |
		|  000004  | 2天前 |    2天前     | bill     | 购买 |   jobs      | 商品2,1        |   支付     |  支付宝  |      100      |  0       |              |              |    110      |         |    待发货       |
		|  000005  | 2天前 |    2天前     | bill     | 购买 |   jobs      | 商品2,1        |   支付     |  支付宝  |      100      |  0       |              |              |    110      |         |    待发货       |
		|  000006  | 2天前 |    2天前     | bill     | 购买 |   jobs      | 商品2,1        |   支付     |  支付宝  |      100      |  0       |              |              |    110      |         |    待发货       |
		|  000007  | 1天前 |    1天前     | bill     | 购买 |   jobs      | 商品3,1        |   支付     |         |      100      |  0       | coupon1_id_1 |              |     0       |         |    待发货       |
		|  000008  | 1天前 |    1天前     | bill     | 购买 |   jobs      | 商品3,1        |   支付     | 货到付款 |      100      |  100     |              |              |     50      |         |    待发货       |
		|  000009  | 1天前 |    1天前     | bill     | 购买 |   jobs      | 商品3,1        |   支付     |         |      100      |  0       |              | 0000001,1    |     0       |         |    待发货       |
		|  000010  | 今天  |    今天      | bill     | 购买 |   jobs      | 商品2,2        |   支付     | 货到付款 |      200      |  0       |              |              |    215      |         |    待发货       |
	# postage 运费是根据商品配置系统计算的，不是输入参数
	# order_source 订单来源不是输入参数
	Given jobs登录系统
	#备注放在发货人后面用“|”隔开
	When jobs对订单进行发货
		"""
		{
			"order_no":"000001",
			"logistics":"顺丰速运",
			"number":"123456789",
			"shipper":"jobs|发货一箱",
			"date":"今天"
		}
		"""
	#Then jobs能获得订单"000001"
	#	| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
	#	|  000001  |      0       | 3天前 |    3天前     | bill     |   jobs      | 商品1,红色 L,1 | 支付    |   微信支付     | 10      |      100      |  0       |              |              |    110      |jobs,发货|    已发货       |  jobs   | 发货一箱 |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |
	When jobs对订单进行发货
		"""
		{
			"order_no":"000004",
			"logistics":"顺丰速运",
			"number":"123456789",
			"shipper":"jobs",
			"date":"今天"
		}
		"""
	#Then jobs能获得订单'000004'
	#	| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
	#	|  000004  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,发货|    已发货       |  jobs   |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs'完成'订单'000004'
	#Then jobs能获得订单'000004'
	#	| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
	#	|  000004  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,完成|    已完成       |  jobs   |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs对订单进行发货
		"""
		{
			"order_no":"000005",
			"logistics":"顺丰速运",
			"number":"123456789",
			"shipper":"",
			"date":"今天"
		}
		"""
	#Then jobs能获得订单'000005'
	#	| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
	#	|  000005  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,发货|    已发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs'完成'订单'000005'
	#Then jobs能获得订单'000005'
	#	| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
	#	|  000005  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,完成|    已发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs'申请退款'订单'000005'
	#Then jobs能获得订单'000005'
	#	| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |   action    |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
	#	|  000005  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,申请退款|    退款中       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs对订单进行发货
		"""
		{
			"order_no":"000006",
			"logistics":"顺丰速运",
			"number":"123456789",
			"shipper":"",
			"date":"今天"
		}
		"""
	#Then jobs能获得订单'000006'
	#	| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
	#	|  000006  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,发货|    已发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs'完成'订单'000006'
	#Then jobs能获得订单'000006'
	#	| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
	#	|  000006  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,完成|    已完成       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs'申请退款'订单'000006'
	#Then jobs能获得订单'000006'
	#	| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |   action    |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
	#	|  000006  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,申请退款|    退款中       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs通过财务审核'退款成功'订单'000006'
	#Then jobs能获得订单'000006'
	#	| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |   action    |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
	#	|  000006  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,退款成功|    退款成功     |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	#When jobs根据给定条件查询订单
	#	"""
	#	{}
	#	"""
	#Then jobs可以看到订单列表
	#	| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |   action    |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           |
	#	|  000010  |      0       | 今天  |    今天      | bill     |   jobs      | 商品2,2        | 支付    |   货到付款     | 15      |      200      |  0       |              |              |    215      |             |    待发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
	#	|  000009  |      0       | 1天前 |    1天前     | bill     |   jobs      | 商品3,1        | 支付    |   优惠抵扣     |  0      |      100      |  0       |              | 0000001      |     0       |             |    待发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
	#	|  000008  |      0       | 1天前 |    1天前     | bill     |   jobs      | 商品3,1        | 支付    |   货到付款     |  0      |      100      |  100     |              |              |     50      |             |    待发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
	#	|  000007  |      0       | 1天前 |    1天前     | bill     |   jobs      | 商品3,1        | 支付    |   优惠抵扣     |  0      |      100      |  0       | coupon1_id_1 |              |     0       |             |    待发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
	#	|  000006  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,申请成功|    退款成功     |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
	#	|  000005  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,申请退款|    退款中       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
	#	|  000004  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,完成    |    已完成       |  jobs   |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
	#	|  000003  |      0       | 3天前 |              | bill     |   jobs      | 商品1,红色 S,1 | 支付    |   微信支付     | 10      |      100      |  0       |              |              |    110      |jobs,取消    |    已取消       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
	#	|  000002  |      0       | 3天前 |              | bill     |   jobs      | 商品1,红色 M,1 |         |   微信支付     | 10      |      100      |  0       |              |              |    110      |             |    待支付       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
	#	|  000001  |      0       | 3天前 |    3天前     | bill     |   jobs      | 商品1,红色 L,1 | 支付    |   微信支付     | 10      |      100      |  0       |              |              |    110      |             |    已发货       |  jobs   | 发货一箱 |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |

	# When jobs'导出订单'
	Then jobs导出订单获取订单信息
		| order_no | sources |  order_time | pay_time | member | product_name |  model | product_unit_price | count | weight | methods_of_payment | postage | money_total | integral | coupon_money | coupon_name | money_wcard | money |  status   | shipper | remark   | ship_name  |  ship_tel   | ship_province |      ship_address       | logistics |   number  | delivery_time |
		|  000010  |   本店   |    今天     |   今天    | bill   |     商品2     |        |       100.0        |   2   |  4.0   |        货到付款     |   10.0  |     210.0   |    0.0   |              |             |    0.0      | 210.0 |  待发货    |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |           |           |               |
		|  000009  |   本店   |    1天前    |   1天前   | bill   |     商品3     |        |       100.0        |   1   |  0.0   |        优惠抵扣     |    0.0  |     100.0   |    0.0   |              |             |   100.0     |  0.0  |  待发货    |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |           |           |               |
		|  000008  |   本店   |    1天前    |   1天前   | bill   |     商品3     |        |       100.0        |   1   |  0.0   |        货到付款     |    0.0  |     50.0    |    50.0  |              |             |      0.0    |  50.0 |  待发货    |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |           |           |               |
		|  000007  |   本店   |    1天前    |   1天前   | bill   |     商品3     |        |       100.0        |   1   |  0.0   |        优惠抵扣     |    0.0  |     0.0     |    0.0   |    100.0     |优惠券（通用券）|      0.0    |  0.0  |  待发货    |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |           |           |               |
		|  000006  |   本店   |    2天前    |   2天前   | bill   |     商品2     |        |       100.0        |   1   |  2.0   |        支付宝       |   10.0  |     0.0     |    0.0   |              |             |      0.0    |  0.0  |  退款完成  |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |  顺丰速运  | 123456789 |     今天      |
		|  000005  |   本店   |    2天前    |   2天前   | bill   |     商品2     |        |       100.0        |   1   |  2.0   |        支付宝       |   10.0  |     0.0     |    0.0   |              |             |      0.0    |  0.0  |  退款中    |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |  顺丰速运  | 123456789 |     今天      |
		|  000004  |   本店   |    2天前    |   2天前   | bill   |     商品2     |        |       100.0        |   1   |  2.0   |        支付宝       |   10.0  |     110.0   |    0.0   |              |             |    0.0      | 110.0 |  已完成    |  jobs   |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |  顺丰速运  | 123456789 |     今天      |
		|  000003  |   本店   |    3天前    |          | bill   |     商品1     |  红色-S |       100.0        |   1   |  2.0   |        微信支付     |   10.0  |     0.0     |    0.0   |              |             |      0.0    |  0.0  |  已取消    |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |           |           |               |
		|  000002  |   本店   |    3天前    |          | bill   |     商品1     |  红色-M |       100.0        |   1   |  2.0   |        微信支付     |   10.0  |     0.0     |    0.0   |              |             |      0.0    |  0.0  |  待支付    |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |           |           |               |
		|  000001  |   本店   |    3天前    |   3天前   | bill   |     商品1     |  红色-L |       100.0        |   1   |  2.0   |        微信支付     |   10.0  |     110.0   |    0.0   |              |             |    0.0      | 110.0 |  已发货    |  jobs   | 发货一箱  |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |  顺丰速运  | 123456789 |     今天      |



@mall2 @order
Scenario: 2 促销订单导出
	jobs可以促销导订单

	#一个订单多个商品包括：买赠的主商品和赠品和限时抢购
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
		{
			"name": "商品2限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品2",
			"member_grade": "全部",
			"count_per_purchase": 2,
			"promotion_price": 50.00
		}
		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "商品1买一赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"premium_products": [{
				"name": "商品3",
				"count": 1
			}],
			"count": 1,
			"member_grade":"全部",
			"is_enable_cycle_mode": true
		}]
		"""
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_no": "9999999",
			"date": "今天",
			"ship_area": "北京市,北京市,海淀区",
			"ship_name": "bill",
			"ship_address": "泰兴大厦",
			"ship_tel": "13811223344",
			"products": [{
				"name": "商品1",
				"model": "红色 L",
				"count": 1
			}, {
				"name": "商品1",
				"model": "红色 M",
				"count": 1
			}, {
				"name": "商品2",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"order_no": "9999999",
			"status": "待支付",
			"final_price": 270.00,
			"product_price": 250.00,
			"promotion_saved_money": 50.00,
			"postage": 20.00,
			"products": [{
				"name": "商品1",
				"count": 1,
				"model": "红色 L",
				"promotion": {
					"type": "premium_sale"
				}
			}, {
				"name": "商品1",
				"count": 1,
				"model": "红色 M",
				"promotion": {
					"type": "premium_sale"
				}
			}, {
				"name": "商品3",
				"count": 2,
				"promotion": {
					"type": "premium_sale:premium_product"
				}
			}, {
				"name": "商品2",
				"count": 1,
				"promotion": {
					"promotioned_product_price": 50.00,
					"type": "flash_sale"
				}
			}]
		}
		"""
	Given jobs登录系统
	Then jobs导出订单获取订单信息
		| order_no | sources |  order_time | pay_time | member | product_name |  model | product_unit_price | count | weight | methods_of_payment | postage | money_total | integral | coupon_money | coupon_name | money_wcard | money |  status   | shipper | remark   | ship_name  |  ship_tel   | ship_province |          ship_address         | logistics |   number  | delivery_time |
		| 9999999  |  本店   |     今天    |          |  bill  |    商品1     | 红色-L |        100.0       |   1   |  2.0   |                    |  20.0   |     0.0     |     0.0  |              |             |     0.0     |  0.0  |  待支付   |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |           |           |               |
		| 9999999  |  本店   |     今天    |          |  bill  |    商品1     | 红色-M |        100.0       |   1   |  2.0   |                    |         |             |          |              |             |             |       |  待支付   |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |           |           |               |
		| 9999999  |  本店   |     今天    |          |  bill  | (赠品)商品3  |        |        100.0       |   2   |  0.0   |                    |         |             |          |              |             |             |       |  待支付   |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |           |           |               |
		| 9999999  |  本店   |     今天    |          |  bill  |    商品2     |        |        50.0        |   1   |  2.0   |                    |         |             |          |              |             |             |       |  待支付   |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |           |           |               |

@order
Scenario: 3 导出订单信息中'总计'信息的校验
	#导出所有订单
	Given jobs登录系统
	Given jobs已创建微众卡
		"""
		{
			"cards": [{
				"id": "0000002",
				"password": "1",
				"status": "未激活",
				"price": 50
			}]
		}
		"""
	When jobs给id为'0000002'的微众卡激活
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券2",
			"money": 100.00,
			"count": 10,
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "商品3买一赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品3",
			"premium_products": [{
				"name": "商品2",
				"count": 1
			}],
			"count": 1,
			"member_grade":"全部",
			"is_enable_cycle_mode": true
		}]
		"""
	When 微信用户批量消费jobs的商品
		| order_id | date  | payment_time | consumer | type | businessman |      product   | payment   | pay_type  | product_price | integral |    coupon    | weizoom_card | final_price |  action      |  order_status     |
		|  000001  | 3天前 |              | bill     | 购买 |   jobs      | 商品1,红色 M,1 |           |  微信支付 |      100      |  0       |              |              |    110      |              |    待支付         |
		|  000002  | 3天前 |    3天前     | bill     | 购买 |   jobs      | 商品1,红色 L,1 |   支付    |  微信支付 |      100      |  0       |              |              |    110      |              |    待发货         |
		|  000003  | 2天前 |    2天前     | bill     | 购买 |   jobs      | 商品3,1        |   支付    |  支付宝   |      100      |  0       |              |              |    100      |jobs,发货     |    已发货         |
		|  000004  | 2天前 |    2天前     | bill     | 购买 |   jobs      | 商品2,1        |   支付    |  支付宝   |      100      |  0       |              |              |    110      |jobs,完成     |    已完成         |
		|  000005  | 2天前 |    2天前     | bill     | 购买 |   jobs      | 商品2,1        |   支付    |  支付宝   |      100      |  0       | coupon2_id_1 |              |    10       |jobs,完成     |    已完成         |
		|  000006  | 1天前 |    1天前     | bill     | 购买 |   jobs      | 商品2,2        |   支付    | 货到付款  |      200      |  0       |              |              |    215      |              |    待发货         |
		|  000007  | 1天前 |    1天前     | bill     | 购买 |   jobs      | 商品3,1        |   支付    |  微信支付 |      100      |  80      |              |              |     60      |              |    待发货         |
		|  000008  | 1天前 |    1天前     | bill     | 购买 |   jobs      | 商品3,1        |   支付    |  支付宝   |     100       |  0       |              | 0000002,1    |     50      |jobs,完成     |    已完成         |
		|  000009  | 1天前 |    1天前     | bill     | 购买 |   jobs      | 商品2,1        |   支付    |  支付宝   |      100      |  0       | coupon1_id_1 |              |     10      |jobs,退款     |    退款中         |
		|  000010  | 今天  |    今天      | bill     | 购买 |   jobs      | 商品3,1        |   支付    |  微信支付 |      100      |  0       |              |              |   100       |jobs,完成退款 |    退款成功       |
		|  000011  | 今天  |    今天      | bill     | 购买 |   jobs      | 商品3,1        |   支付    |  微信支付 |      100      |  100     |              |              |     50      |jobs,取消     |    已取消         |
		|  000012  | 今天  |    今天      | bill     | 购买 |   jobs      | 商品3,1        |           |  微信支付 |      100      |  0       | coupon2_id_2 |              |    0        |jobs,取消     |    已取消         |
		|  000013  | 今天  |    今天      | bill     | 购买 |   jobs      | 商品1,红色 S,1 |   支付    |  支付宝   |      100      |  0       |              | 0000001,1    |     10      |jobs,取消     |    已取消         |
	#导出所有订单
	Then jobs导出订单获取订单统计信息
		"""
			[{
				"订单量":13,
				"已完成":3,
				"商品金额":1400.00,
				"支付总额":655.00,
				"现金支付金额":655.00,
				"微众卡支付金额":50.00,
				"赠品数量":3,
				"积分抵扣总金额":40.00,
				"优惠券价值总额":100.00
			}]
		"""
	#查询结果中，导出订单
	When jobs根据给定条件查询订单
		"""
		{
			"order_status": "已取消"
		}
		"""
	Then jobs导出订单获取订单统计信息
		"""
			[{
				"订单量":3,
				"已完成":0,
				"商品金额":1400.00,
				"支付金额":0.00,
				"现金支付金额":0.00,
				"微众卡支付金额":0.00,
				"赠品数量":2,
				"积分抵扣总金额":0.00,
				"优惠券价值总额":0.00
			}]
		"""
