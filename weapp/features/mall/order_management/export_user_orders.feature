# __author__ : "冯雪静"

Feature:用户订单导出功能
	jobs能导出用户的订单
	"""
	1.导出全部订单
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
	When jobs已创建微众卡
		"""
		{
			"cards": [{
				"id": "0000001",
				"password": "1234567",
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
			}
		},{
			"name": "商品2",
			"price": 100.00,
			"weight": 1
		},{
			"name": "商品3",
			"price": 100.00,
			"weight": 0
		}]
		"""
	And bill关注jobs的公众号
	And bill添加收货地址
		"""
		[{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市,北京市,海淀区",
			"ship_address": "泰兴大厦"
		}]
		"""
	Given jobs已有的会员
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


@order
Scenario: 导出全部订单
	jobs可以导出全部订单

	When 微信用户批量消费jobs的商品
		| order_no | order_source |  date | payment_time | consumer | type | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   |
		|  000001  |      0       | 3天前 |    3天前     | bill     | 购买 |   jobs      | 商品1,红色 L,1 | 支付    |   微信支付     | 10      |      100      |  0       |              |              |    110      |         |    待发货       |
		|  000002  |      0       | 3天前 |              | bill     | 购买 |   jobs      | 商品1,红色 M,1 |         |   微信支付     | 10      |      100      |  0       |              |              |    110      |         |    待支付       |
		|  000003  |      0       | 3天前 |              | bill     | 购买 |   jobs      | 商品1,红色 S,1 | 支付    |   微信支付     | 10      |      100      |  0       |              |              |    110      |jobs,取消|    已取消       |
		|  000004  |      0       | 2天前 |    2天前     | bill     | 购买 |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |         |    待发货       |
		|  000005  |      0       | 2天前 |    2天前     | bill     | 购买 |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |         |    待发货       |
		|  000006  |      0       | 2天前 |    2天前     | bill     | 购买 |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |         |    待发货       |
		|  000007  |      0       | 1天前 |    1天前     | bill     | 购买 |   jobs      | 商品3,1        | 支付    |   优惠抵扣     |  0      |      100      |  0       | coupon1_id_1 |              |     0       |         |    待发货       |
		|  000008  |      0       | 1天前 |    1天前     | bill     | 购买 |   jobs      | 商品3,1        | 支付    |   货到付款     |  0      |      100      |  100     |              |              |     50      |         |    待发货       |
		|  000009  |      0       | 1天前 |    1天前     | bill     | 购买 |   jobs      | 商品3,1        | 支付    |   优惠抵扣     |  0      |      100      |  0       |              | 0000001      |     0       |         |    待发货       |
		|  000010  |      0       | 今天  |    今天      | bill     | 购买 |   jobs      | 商品2,2        | 支付    |   货到付款     | 15      |      200      |  0       |              |              |    215      |         |    待发货       |

	Given jobs登录系统
	#备注放在发货人后面用“|”隔开
	When jobs对订单'000001'进行"发货"
		"""
		{
			"order_no":"000001",
			"logistics":"顺丰速运",
			"number":"123456789",
			"shipper":"jobs|发货一箱"
		}
		"""
	Then jobs能获得订单'000001'
		| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
		|  000001  |      0       | 3天前 |    3天前     | bill     |   jobs      | 商品1,红色 L,1 | 支付    |   微信支付     | 10      |      100      |  0       |              |              |    110      |jobs,发货|    已发货       |  jobs   | 发货一箱 |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |
	When jobs对订单'000004'进行'发货'
		"""
		{
			"order_no":"000004",
			"logistics":"顺丰速运",
			"number":"123456789",
			"shipper":"jobs"
		}
		"""
	Then jobs能获得订单'000004'
		| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
		|  000004  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,发货|    已发货       |  jobs   |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs完成订单'000004'
	Then jobs能获得订单'000004'
		| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
		|  000004  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,完成|    已完成       |  jobs   |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs对订单'000005'进行'发货'
		"""
		{
			"order_no":"000005",
			"logistics":"顺丰速运",
			"number":"123456789",
			"shipper":""
		}
		"""
	Then jobs能获得订单'000005'
		| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
		|  000005  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,发货|    已发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs完成订单'000005'
	Then jobs能获得订单'000005'
		| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
		|  000005  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,完成|    已发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs'申请退款'订单'000005'
	Then jobs能获得订单'000005'
		| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |   action    |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
		|  000005  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,申请退款|    退款中       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs对订单'000006'进行'发货'
		"""
		{
			"order_no":"000006",
			"logistics":"顺丰速运",
			"number":"123456789",
			"shipper":""
		}
		"""
	Then jobs能获得订单'000006'
		| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
		|  000006  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,发货|    已发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs完成订单'000006'
	Then jobs能获得订单'000006'
		| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |  action |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
		|  000006  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,完成|    已完成       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs'申请退款'订单'000006'
	Then jobs能获得订单'000006'
		| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |   action    |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
		|  000006  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,申请退款|    退款中       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs通过财务审核'退款成功'订单'000006'
	Then jobs能获得订单'000006'
		| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |   action    |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           | express_company_name | express_number | delivery_time |
		|  000006  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,退款成功|    退款成功     |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |

	When jobs根据给定条件查询订单
		"""
		{}
		"""
	Then jobs可以看到订单列表
		| order_no | order_source |  date | payment_time | consumer | businessman |      product   | payment | payment_method | postage | product_price | integral |    coupon    | weizoom_card | final_price |   action    |  order_status   | shipper | remark   | "ship_name |  ship_tel   |        ship_address           |
		|  000010  |      0       | 今天  |    今天      | bill     |   jobs      | 商品2,2        | 支付    |   货到付款     | 15      |      200      |  0       |              |              |    215      |             |    待发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
		|  000009  |      0       | 1天前 |    1天前     | bill     |   jobs      | 商品3,1        | 支付    |   优惠抵扣     |  0      |      100      |  0       |              | 0000001      |     0       |             |    待发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
		|  000008  |      0       | 1天前 |    1天前     | bill     |   jobs      | 商品3,1        | 支付    |   货到付款     |  0      |      100      |  100     |              |              |     50      |             |    待发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
		|  000007  |      0       | 1天前 |    1天前     | bill     |   jobs      | 商品3,1        | 支付    |   优惠抵扣     |  0      |      100      |  0       | coupon1_id_1 |              |     0       |             |    待发货       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
		|  000006  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,申请成功|    退款成功     |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
		|  000005  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,申请退款|    退款中       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
		|  000004  |      0       | 2天前 |    2天前     | bill     |   jobs      | 商品2,1        | 支付    |   支付宝       | 10      |      100      |  0       |              |              |    110      |jobs,完成    |    已完成       |  jobs   |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
		|  000003  |      0       | 3天前 |              | bill     |   jobs      | 商品1,红色 S,1 | 支付    |   微信支付     | 10      |      100      |  0       |              |              |    110      |jobs,取消    |    已取消       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
		|  000002  |      0       | 3天前 |              | bill     |   jobs      | 商品1,红色 M,1 |         |   微信支付     | 10      |      100      |  0       |              |              |    110      |             |    待支付       |         |          |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |
		|  000001  |      0       | 3天前 |    3天前     | bill     |   jobs      | 商品1,红色 L,1 | 支付    |   微信支付     | 10      |      100      |  0       |              |              |    110      |             |    已发货       |  jobs   | 发货一箱 |    bill    | 13811223344 | 北京市,北京市,海淀区,泰兴大厦 |

	When jobs'导出订单'
	Then jobs获取导出订单信息
		| order_no | order_source |  date | payment_time | consumer | product | model  | price | count | weight | payment_method | postage | payment_amount | integral_money | coupon_money |    coupon    | weizoom_card | cash |  order_status   | shipper | remark   | "ship_name |  ship_tel   | ship_province |        ship_address           | express_company_name | express_number | delivery_time |
		|  000010  |      0       | 今天  |    今天      | bill     |  商品2  |        |  100  |   2   |   2    |   货到付款     | 15      |      215       |        0       |              |              |              | 215  |    待发货       |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |                      |                |               |
		|  000009  |      0       | 1天前 |    1天前     | bill     |  商品3  |        |  100  |   1   |   0    |   优惠抵扣     |  0      |      100       |        0       |              |              |     100      |  0   |    待发货       |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |                      |                |               |
		|  000008  |      0       | 1天前 |    1天前     | bill     |  商品3  |        |  100  |   1   |   0    |   货到付款     |  0      |      50        |        50      |              |              |              |  50  |    待发货       |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |                      |                |               |
		|  000007  |      0       | 1天前 |    1天前     | bill     |  商品3  |        |  100  |   1   |   0    |   优惠抵扣     |  0      |      0         |        0       |      100     |    优惠券    |              |  0   |    待发货       |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |                      |                |               |
		|  000006  |      0       | 2天前 |    2天前     | bill     |  商品2  |        |  100  |   1   |   1    |   支付宝       | 10      |      0         |        0       |              |              |              |  0   |    退款成功     |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |
		|  000005  |      0       | 2天前 |    2天前     | bill     |  商品2  |        |  100  |   1   |   1    |   支付宝       | 10      |      0         |        0       |              |              |              |  0   |    退款中       |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |
		|  000004  |      0       | 2天前 |    2天前     | bill     |  商品2  |        |  100  |   1   |   1    |   支付宝       | 10      |      110       |        0       |              |              |              | 110  |    已完成       |  jobs   |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |
		|  000003  |      0       | 3天前 |              | bill     |  商品1  | 红色 S |  100  |   1   |   1    |   微信支付     | 10      |      0         |        0       |              |              |              |  0   |    已取消       |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |                      |                |               |
		|  000002  |      0       | 3天前 |              | bill     |  商品1  | 红色 M |  100  |   1   |   1    |   微信支付     | 10      |      0         |        0       |              |              |              |  0   |    待支付       |         |          |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |                      |                |               |
		|  000001  |      0       | 3天前 |    3天前     | bill     |  商品1  | 红色 L |  100  |   1   |   1    |   微信支付     | 10      |      110       |        0       |              |              |              | 110  |    待发货       |  jobs   | 发货一箱 |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |       顺丰速运       |   123456789    |     今天      |
