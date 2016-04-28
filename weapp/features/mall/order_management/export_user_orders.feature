# __author__ : "冯雪静"
#editor:王丽 2015.10.16

Feature:用户订单导出功能-商家账号
"""
	能导出用户的订单
	1.导出全部订单
	2.导出促销订单
"""

Background:
	Given 添加tom店铺名称为'tom商家'
	Given tom登录系统
	When tom已添加支付方式
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
	When tom开通使用微众卡权限
	When tom添加支付方式
		"""
		[{
			"type": "微众卡支付",
			"description": "我的微众卡支付",
			"is_active": "启用"
		}]
		"""
	Given tom已创建微众卡
		"""
		{
			"cards": [{
				"id": "0000001",
				"password": "1",
				"status": "未激活",
				"price": 100
			},{
				"id": "0000002",
				"password": "1",
				"status": "未激活",
				"price": 50
			}]
		}
		"""
	When tom给id为'0000001'的微众卡激活
	When tom给id为'0000002'的微众卡激活
	When tom添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":10.00,
			"added_weight":1,
			"added_weight_price":5.00
		}]
		"""
	And tom选择'顺丰'运费配置
	And tom已添加商品规格
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
	And tom已添加商品
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
	And bill关注tom的公众号
	And bill设置tom的webapp的收货地址
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"area": "北京市,北京市,海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
	Given tom登录系统
	And tom已有的会员
		"""
		[{
			"name": "bill",
			"integral": 500
		}]
		"""
	When tom添加优惠券规则
		"""
		[{
			"name": "优惠券",
			"money": 100.00,
			"count": 1,
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	Given tom设定会员积分策略
		"""
		{
			"integral_each_yuan": 2,
			"use_ceiling": 50
		}
		"""

@mall2 @order
Scenario:1 导出全部订单
	tom 可以导出全部订单

	When 微信用户批量消费tom 的商品
		| order_id |   date     | payment_time | consumer |      product   | payment | pay_type  | price* | integral |    coupon          | weizoom_card | paid_amount*|  action | order_status* |
		|  000001  | 2016-04-10 |    3天前     | bill     | 商品1,红色 L,1 |   支付  |  微信支付 |  100   |  0       |                    |              |    110      |         |   待发货      |
		|  000002  |   3天前    |              | bill     | 商品1,红色 M,1 |         |           |  100   |  0       |                    |              |    110      |         |   待支付      |
		|  000003  |   3天前    |              | bill     | 商品1,红色 S,1 |         |           |  100   |  0       |                    |              |    110      |tom ,取消|   已取消      |
		|  000004  |   2天前    |    2天前     | bill     | 商品2,1        |   支付  |  支付宝   |  100   |  0       |                    |              |    110      |         |   待发货      |
		|  000005  |   2天前    |    2天前     | bill     | 商品2,1        |   支付  |  支付宝   |  100   |  0       |                    |              |    110      |         |   待发货      |
		|  000006  |   2天前    |    2天前     | bill     | 商品2,1        |   支付  |  支付宝   |  100   |  0       |                    |              |    110      |         |   待发货      |
		|  000007  |   1天前    |    1天前     | bill     | 商品3,1        |   支付  |           |  100   |  0       |优惠券,coupon1_id_1 |              |     0       |         |   待发货      |
		|  000008  |   1天前    |    1天前     | bill     | 商品3,1        |   支付  | 货到付款  |  100   |  100     |                    |              |     50      |         |   待发货      |
		|  000009  |   1天前    |    1天前     | bill     | 商品3,1        |   支付  |           |  100   |  0       |                    | 0000001,1    |     0       |         |   待发货      |
		|  000010  |   今天     |    今天      | bill     | 商品2,2        |   支付  | 货到付款  |  200   |  0       |                    |              |    215      |         |   待发货      |
	# postage 运费是根据商品配置系统计算的，不是输入参数
	# order_source 订单来源不是输入参数
	Given tom登录系统
	#备注放在发货人后面用“|”隔开
	When tom对订单进行发货
		"""
		{
			"order_no":"000001",
			"logistics":"顺丰速运",
			"number":"123456789",
			"shipper":"tom|发货一箱",
			"date":"今天"
		}
		"""
	When tom对订单进行发货
		"""
		{
			"order_no":"000004",
			"logistics":"顺丰速运",
			"number":"123456789",
			"shipper":"tom",
			"date":"今天"
		}
		"""
	When tom'完成'订单'000004'
	When tom对订单进行发货
		"""
		{
			"order_no":"000005",
			"logistics":"顺丰速运",
			"number":"123456789",
			"shipper":"",
			"date":"今天"
		}
		"""

	When tom'完成'订单'000005'
	When tom'申请退款'订单'000005'

	When tom对订单进行发货
		"""
		{
			"order_no":"000006",
			"logistics":"顺丰速运",
			"number":"123456789",
			"shipper":"",
			"date":"今天"
		}
		"""
	When tom'完成'订单'000006'
	When tom'申请退款'订单'000006'
	When tom通过财务审核'退款成功'订单'000006'

	Then tom导出订单获取订单信息
		| order_no |  order_time | pay_time | product_name |  model | product_unit_price | count | sales_money | weight | methods_of_payment | money_total | money  | money_wcard | postage | integral | coupon_money | coupon_name    |  status   | member | ship_name  |  ship_tel   | ship_province |          ship_address         | shipper | leader_remark   | sources | logistics |   number  | delivery_time | remark | customer_message | customer_source | customer_recommender | is_qr_code | is_older_mermber |
		|  000010  |    今天     |   今天   |     商品2    |        |       100.00       |   2   |   200.00    |  4.0   |        货到付款    |     210.00  | 210.00 |     0.00    |   10.00 |    0.00  |              |                |  待发货   | bill   |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |                 |   本店  |           |           |               |        |                  |     直接关注    |                      |            |                  |
		|  000009  |    1天前    |   1天前  |     商品3    |        |       100.00       |   1   |   100.00    |  0.0   |        优惠抵扣    |     100.00  |  0.00  |    100.00   |    0.00 |    0.00  |              |                |  待发货   | bill   |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |                 |   本店  |           |           |               |        |                  |     直接关注    |                      |            |                  |
		|  000008  |    1天前    |   1天前  |     商品3    |        |       100.00       |   1   |   100.00    |  0.0   |        货到付款    |     50.00   |  50.00 |     0.00    |    0.00 |    50.00 |              |                |  待发货   | bill   |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |                 |   本店  |           |           |               |        |                  |     直接关注    |                      |            |                  |
		|  000007  |    1天前    |   1天前  |     商品3    |        |       100.00       |   1   |   100.00    |  0.0   |        优惠抵扣    |     0.00    |  0.00  |     0.00    |    0.00 |    0.00  |    100.00    |优惠券（通用券）|  待发货   | bill   |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |                 |   本店  |           |           |               |        |                  |     直接关注    |                      |            |                  |
		|  000006  |    2天前    |   2天前  |     商品2    |        |       100.00       |   1   |   100.00    |  2.0   |        支付宝      |     0.00    |  0.00  |     0.00    |   10.00 |    0.00  |              |                |  退款完成 | bill   |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |                 |   本店  |  顺丰速运 | 123456789 |     今天      |        |                  |     直接关注    |                      |            |                  |
		|  000005  |    2天前    |   2天前  |     商品2    |        |       100.00       |   1   |   100.00    |  2.0   |        支付宝      |     110.00  | 110.00 |     0.00    |   10.00 |    0.00  |              |                |  退款中   | bill   |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |                 |   本店  |  顺丰速运 | 123456789 |     今天      |        |                  |     直接关注    |                      |            |                  |
		|  000004  |    2天前    |   2天前  |     商品2    |        |       100.00       |   1   |   100.00    |  2.0   |        支付宝      |     110.00  | 110.00 |     0.00    |   10.00 |    0.00  |              |                |  已完成   | bill   |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |  tom    |                 |   本店  |  顺丰速运 | 123456789 |     今天      |        |                  |     直接关注    |                      |            |                  |
		|  000003  |    3天前    |          |     商品1    | 红色-S |       100.00       |   1   |   100.00    |  2.0   |                    |     0.00    |  0.00  |     0.00    |   10.00 |    0.00  |              |                |  已取消   | bill   |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |                 |   本店  |           |           |               |        |                  |     直接关注    |                      |            |                  |
		|  000002  |    3天前    |          |     商品1    | 红色-M |       100.00       |   1   |   100.00    |  2.0   |                    |     0.00    |  0.00  |             |   10.00 |          |              |                |  待支付   | bill   |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |                 |   本店  |           |           |               |        |                  |     直接关注    |                      |            |                  |
		|  000001  | 2016-04-10  |   3天前  |     商品1    | 红色-L |       100.00       |   1   |   100.00    |  2.0   |        微信支付    |     110.00  | 110.00 |     0.00    |   10.00 |    0.00  |              |                |  已发货   | bill   |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |  tom    | 发货一箱        |   本店  |  顺丰速运 | 123456789 |     今天      |        |                  |     直接关注    |                      |            |        是        |

@mall2 @order
Scenario:2 促销订单导出
	tom可以促销导订单

	#一个订单多个商品包括：买赠的主商品和赠品和限时抢购
	Given tom登录系统
	When tom创建限时抢购活动
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
	When tom创建买赠活动
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
	When bill访问tom的webapp
	When bill购买tom的商品
		"""
		{
			"order_id": "9999999",
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
	Given tom登录系统
	Then tom导出订单获取订单信息
		| order_no |  order_time | pay_time | product_name |  model | product_unit_price | count | sales_money | weight | methods_of_payment | money_total | money | money_wcard | postage | integral | coupon_money | coupon_name |  status   | member | ship_name  |  ship_tel   | ship_province |          ship_address         | shipper | leader_remark | sources | logistics |   number  | delivery_time | remark   | customer_message | customer_source | customer_recommender | is_qr_code | is_older_mermber |
		| 9999999  |     今天    |          |    商品1     | 红色-L |        100.00      |   1   |    100.00   |  2.0   |                    |     0.0     |  0.0  |             |  20.0   |          |              |             |  待支付   |  bill  |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |               |  本店   |           |           |               |          |                  |     直接关注    |                      |            |                  |   
		| 9999999  |     今天    |          |    商品1     | 红色-M |        100.00      |   1   |    100.00   |  2.0   |                    |             |       |             |         |          |              |             |  待支付   |  bill  |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |               |  本店   |           |           |               |          |                  |     直接关注    |                      |            |                  |   
		| 9999999  |     今天    |          | (赠品)商品3  |        |        100.00      |   2   |    100.00   |  0.0   |                    |             |       |             |         |          |              |             |  待支付   |  bill  |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |               |  本店   |           |           |               |          |                  |     直接关注    |                      |            |                  |   
		| 9999999  |     今天    |          |    商品2     |        |        50.00       |   1   |    50.00    |  2.0   |                    |             |       |             |         |          |              |             |  待支付   |  bill  |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |               |  本店   |           |           |               |          |                  |     直接关注    |                      |            |                  |   

@mall2 @order
Scenario:3 导出订单信息中'总计'信息的校验
	#导出所有订单
	Given tom登录系统
	When tom添加优惠券规则
		"""
		[{
			"name": "优惠券2",
			"money": 100.00,
			"count": 10,
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	When tom创建买赠活动
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
	When 微信用户批量消费tom的商品
		| order_id | date  | payment_time | consumer |      product   | payment   | pay_type  | price*|integral |    coupon          | weizoom_card | paid_amount*|  action     | order_status* |delivery_time|
		|  000001  | 3天前 |    3天前     | bill     | 商品1,红色 L,1 |   支付    |  微信支付 | 100   |         |                    |              |    110      |             |   待发货      |             |
		|  000002  | 今天  |    今天      | bill     | 商品3,1        |   支付    |  支付宝   | 100   |         |                    |              |    100      |tom,发货     |   已发货      |   今天      |
		|  000003  | 2天前 |    2天前     | bill     | 商品2,1        |   支付    |  支付宝   | 100   |         |                    |              |    110      |tom,完成     |   已完成      | 今天        |
		|  000004  | 2天前 |    2天前     | bill     | 商品2,1        |   支付    |  支付宝   | 100   |         |优惠券2,coupon2_id_1|              |    10       |tom,完成     |   已完成      | 今天        |
		|  000005  | 1天前 |    1天前     | bill     | 商品2,2        |   支付    | 货到付款  | 200   |         |                    |              |    210      |             |   待发货      |             |
		|  000006  | 今天  |    今天      | bill     | 商品3,1        |   支付    |  微信支付 | 100   |   100   |                    |              |     50      |             |   待发货      |             |
		|  000007  | 今天  |    今天      | bill     | 商品3,1        |   支付    |  支付宝   | 100   |         |                    | 0000002,1    |     50      |tom,完成     |   已完成      | 今天        |
		|  000008  | 今天  |    今天      | bill     | 商品2,1        |   支付    |  支付宝   | 100   |         |优惠券,coupon1_id_1 |              |     10      |tom,退款     |   退款中      | 今天        |
		|  000009  | 今天  |              | bill     | 商品3,1        |           |  微信支付 | 100   |   100   |                    |              |     50      |             |   待支付      |             |
		|  000010  | 今天  |    今天      | bill     | 商品3,1        |   支付    |  微信支付 | 100   |         |                    |              |   100       |tom,完成退款 |   退款成功    | 今天        |
		|  000011  | 今天  |         	  | bill     | 商品3,1        |           |  微信支付 | 100   |         |                    |              |     50      |tom,取消     |   已取消      |             |
		|  000012  | 今天  |              | bill     | 商品3,1        |           |  微信支付 | 100   |         |优惠券2,coupon2_id_2|              |    0        |tom,取消     |   已取消      |             |
		|  000013  | 今天  |              | bill     | 商品1,红色 S,1 |           |  支付宝   | 100   |         |                    | 0000001,1    |     10      |tom,取消     |   已取消      |             |
	#导出所有订单
	Then tom导出订单获取订单统计信息
		"""
		[{
			"订单量":13,
			"已完成":3,
			"商品金额":1400.00,
			"支付总额":700.00,
			"现金支付金额":650.00,
			"微众卡支付金额":50.00,
			"赠品总数":5,
			"积分抵扣总金额":50.00,
			"优惠劵价值总额":200.00
		}]
		"""
	#查询结果中，导出订单
	When tom根据给定条件查询订单
		"""
		{
			"order_status": "已取消"
		}
		"""
	Then tom导出订单获取订单统计信息
		"""
		[{
			"订单量":3,
			"已完成":0,
			"商品金额":300.00,
			"支付总额":0.00,
			"现金支付金额":0.00,
			"微众卡支付金额":0.00,
			"赠品总数":0,
			"积分抵扣总金额":0.00,
			"优惠劵价值总额":0.00
		}]
		"""

@order
Scenario:4 同步订单导出
	#自营平台tom的信息
	Given 设置jobs为自营平台账号
	Given jobs登录系统
	And jobs已添加供货商
		"""
		[{
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
	And bill设置tom的webapp的收货地址
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"area": "北京市,北京市,海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
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
			"supplier": "丹江湖",
			"name": "商品4",
			"purchase_price": 2.00,
			"price": 100.00
		}, {
			"supplier": "丹江湖",
			"purchase_price": 4.00,
			"name": "商品5",
			"price": 100.00
		}]
		"""
	When jobs将商品池商品批量放入待售于'2016-04-02 10:30'
			"""
			[
				"商品2",
				"商品3"
			]
			"""
	When jobs更新商品'商品2'
		"""
		{
			"supplier": "tom",
			"name": "商品2",
			"purchase_price": 20.00,
			"price": 100.00,
			"status": "待售"
		}
		"""
	When jobs更新商品'商品3'
		"""
		{
			"supplier": "tom",
			"name": "商品3",
			"purchase_price": 30.00,
			"price": 100.00,
			"status": "待售"
		}
		"""
	When jobs批量上架商品
		"""
		["商品2","商品3"]
		"""

	#购买jobs商品并拆单
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_id": "0001",
			"date": "2016-02-01",
			"pay_type":"微信支付",
			"products": [{
				"name": "商品2",
				"count": 1
			}, {
				"name": "商品3",
				"count": 1
			}, {
				"name": "商品4",
				"count": 1
			}, {
				"name": "商品5",
				"count": 1
			}],
			"integral": 50,
			"integral_money": 50
		}
		"""
	When bill使用支付方式'微信支付'进行支付订单'0001'

	#自营平台jobs发货自建商家商品
	Given jobs登录系统
	When jobs对订单进行发货
		"""
		{
			"order_no":"0001-丹江湖",
			"logistics":"顺丰速运",
			"number":"123456789"
		}
		"""

	#商家账号tom发货同步的订单
	Given tom登录系统
	When tom对订单进行发货
		"""
		{
			"order_no":"0001-tom",
			"logistics":"顺丰速运",
			"number":"123456789"
		}
		"""

	#商家账号导出同步订单
	Then tom导出订单获取订单信息
		| order_no |  order_time | pay_time | product_name |  model | product_unit_price | count | sales_money | weight | methods_of_payment | money_total | money | money_wcard | postage | integral | coupon_money | coupon_name |  status   | member | ship_name  |  ship_tel   | ship_province |          ship_address         | shipper | leader_remark | sources | logistics |   number  | delivery_time | remark   | customer_message | customer_source | customer_recommender | is_qr_code | is_older_mermber |
		| 0001-tom |     今天    |   今天   |    商品2     |        |        20.00       |   1   |    20.00    |  2.0   |     微信支付       |     50.0    |  50.0 |    0.00     |  0.00   |   0.00   |     0.00     |             |  已发货   |  bill  |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |               |  商城   | 顺丰速运  | 123456789 |      今天     |          |                  |     直接关注    |                      |            |                  |   
		| 0001-tom |     今天    |   今天   |    商品3     |        |        30.00       |   1   |    30.00    |  2.0   |     微信支付       |             |       |             |         |          |              |             |  已发货   |  bill  |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |               |  商城   | 顺丰速运  | 123456789 |      今天     |          |                  |     直接关注    |                      |            |                  |   

@order
Scenario:5 团购订单导出
	Given tom登录系统
	When tom新建团购活动:weapp
		"""
		[{
			"group_name":"团购活动1",
			"start_date":"今天",
			"end_date":"2天后",
			"product_name":"商品2",
			"group_dict":{
				"0":{
					"group_type":"3",
					"group_days":"1",
					"group_price":"90.00"
					}
				},
				"ship_date":20,
				"product_counts":100,
				"material_image":"1.jpg",
				"share_description":"团购活动1分享描述"
		}]
		"""
	When tom开启团购活动'团购活动1'

	Given tom1关注tom的公众号
	And tom1关注tom的公众号

	#bill开团，团购成功
		When bill访问tom的webapp
		When bill参加tom的团购活动"团购活动1"进行开团:weapp
			"""
			{
				"group_name": "团购活动1",
				"group_leader": "bill",
				"group_dict":
					{
						"group_type":3,
						"group_days":1,
						"group_price":90.00
					},
				"products": {
					"name": "商品2"
				}
			}
			"""
		When bill提交团购订单
			"""
			{
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"distribution_time":"5天后 10:00-12:30",
				"order_id":"00101",
				"pay_type":"微信支付"
			}
			"""
		When bill使用支付方式'微信支付'进行支付

		When tom1访问tom的webapp
		When tom1参加bill的团购活动"团购活动1":weapp
			"""
			{
				"group_name": "团购活动1",
				"group_leader": "bill",
				"group_dict":
					{
						"group_type":3,
						"group_days":1,
						"group_price":90.00
					},
				"products": {
					"name": "商品2"
				}
			}
			"""
		When tom1提交团购订单
			"""
			{
				"ship_name": "tom1",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"distribution_time":"5天后 10:00-12:30",
				"order_id":"00102",
				"pay_type":"微信支付"
			}
			"""
		When tom1使用支付方式'微信支付'进行支付

		When tom2访问tom的webapp
		When tom2参加bill的团购活动"团购活动1":weapp
			"""
			{
				"group_name": "团购活动1",
				"group_leader": "bill",
				"group_dict":
					{
						"group_type":3,
						"group_days":1,
						"group_price":90.00
					},
				"products": {
					"name": "商品2"
				}
			}
			"""
		When tom2提交团购订单
			"""
			{
				"ship_name": "tom2",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"distribution_time":"5天后 10:00-12:30",
				"order_id":"00103",
				"pay_type":"微信支付"
			}
			"""
		When tom2使用支付方式'微信支付'进行支付

	#tom3开团，团购失败
		When tom3访问tom的webapp
		When tom3参加tom的团购活动"团购活动1"进行开团:weapp
			"""
			{
				"group_name": "团购活动1",
				"group_leader": "tom3",
				"group_dict":
					{
						"group_type":3,
						"group_days":1,
						"group_price":90.00
					},
				"products": {
					"name": "商品2"
				}
			}
			"""
		When tom3提交团购订单
			"""
			{
				"ship_name": "tom3",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"distribution_time":"5天后 10:00-12:30",
				"order_id":"00201",
				"pay_type":"微信支付"
			}
			"""
		When tom3使用支付方式'微信支付'进行支付

		When tom1访问tom的webapp
		When tom1参加bill的团购活动"团购活动1":weapp
			"""
			{
				"group_name": "团购活动1",
				"group_leader": "tom3",
				"group_dict":
					{
						"group_type":3,
						"group_days":1,
						"group_price":90.00
					},
				"products": {
					"name": "商品2"
				}
			}
			"""
		When tom1提交团购订单
			"""
			{
				"ship_name": "tom1",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"distribution_time":"5天后 10:00-12:30",
				"order_id":"00202",
				"pay_type":"微信支付"
			}
			"""
		Given tom登录系统
		When tom关闭团购活动'团购活动1'

	#tom导出团购订单
	Then tom导出订单获取订单信息
		| order_no |  order_time | pay_time | product_name |  model | product_unit_price | count | sales_money | weight | methods_of_payment | money_total | money | money_wcard | postage | integral | coupon_money | coupon_name |  status   | member | ship_name  |  ship_tel   | ship_province |          ship_address         | shipper | leader_remark | sources | logistics |   number  | delivery_time | remark   | customer_message | customer_source | customer_recommender | is_qr_code | is_older_mermber |
		|  00201   |     今天    |   今天   |    商品2     |        |        100.00      |   1   |    100.00   |  2.0   |     微信支付       |    90.00    | 90.00 |             |  0.00   |          |              |             |  退款中   |  tom3  |    tom3    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |               |  本店   |           |           |               |          |                  |     直接关注    |                      |            |                  |   
		|  00103   |     今天    |   今天   |    商品2     |        |        100.00      |   1   |    100.00   |  2.0   |     微信支付       |    90.00    | 90.00 |             |  0.00   |          |              |             |  待发货   |  tom2  |    tom2    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |               |  本店   |           |           |               |          |                  |     直接关注    |                      |            |                  |   
		|  00102   |     今天    |   今天   |    商品2     |        |        100.00      |   1   |    100.00   |  0.0   |     微信支付       |    90.00    | 90.00 |             |  0.00   |          |              |             |  待发货   |  tom1  |    tom1    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |               |  本店   |           |           |               |          |                  |     直接关注    |                      |            |                  |   
		|  00101   |     今天    |   今天   |    商品2     |        |        100.00      |   1   |    100.00   |  2.0   |     微信支付       |    90.00    | 90.00 |             |  0.00   |          |              |             |  待发货   |  bill  |    bill    | 13811223344 |    北京市     | 北京市,北京市,海淀区,泰兴大厦 |         |               |  本店   |           |           |               |          |                  |     直接关注    |                      |            |                  |   
