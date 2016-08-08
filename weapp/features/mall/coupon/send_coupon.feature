#author: 冯雪静
#editor: 张三香 2015.10.13

Feature: 发放优惠券
	Jobs能通过管理系统将生成的"优惠券"发放给会员

Background:
	Given 重置'apiserver'的bdd环境
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "单品券2",
			"money": 10.00,
			"limit_counts": "不限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品1"
		}, {
			"name": "全体券3",
			"money": 100.00,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
		}]
		"""
	Given bill关注jobs的公众号
	Given tom关注jobs的公众号

@mall2 @promotion @promotionSendCoupon   @send_coupon @eugene
Scenario: 1 发送优惠券给一个会员
	jobs添加"优惠券规则"后，将优惠券"单品券2"发放给一个会员(bill)
	1.bill访问jobs的webapp时能看到获得的优惠券
	2.tom访问jobs的webapp不能看到bill获得的优惠券
	3.jobs能获得包含发放的优惠券的的优惠券码库

	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	When jobs创建优惠券发放规则发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 2,
			"members": ["bill"]
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_1",
				"money": 10.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_2",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

@mall2 @promotion @promotionSendCoupon   @send_coupon @eugene
Scenario: 2 发送优惠券给多个会员
	jobs添加"优惠券规则"后，将优惠券"单品券2"发放给多个会员(bill，tom)
	1.bill访问jobs的webapp时能看到获得的优惠券
	2.tom访问jobs的webapp时能看到获得的优惠券
	3.jobs能获得包含发放的优惠券的优惠券码库

	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	When jobs创建优惠券发放规则发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 1,
			"members": ["bill", "tom"],
			"coupon_ids": ["coupon2_id_2", "coupon2_id_1"]
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_1",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_2",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

@mall2 @promotion @promotionSendCoupon   @send_coupon @eugene
Scenario: 3 多次发送有领取限制的优惠券给一个会员
	jobs添加"优惠券规则"后，将优惠券"全体券3"发放给1个会员(bill)
	1. bill访问jobs的webapp时只能看到一张优惠券
	2. jobs能获得包含发放的优惠券的优惠券码库

	Given jobs登录系统
	Then jobs能获得优惠券'全体券3'的码库
		"""
		{
			"coupon3_id_1": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_2": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	When jobs创建优惠券发放规则发放优惠券
		"""
		{
			"name": "全体券3",
			"count": 1,
			"members": ["bill"]
		}
		"""
	When jobs创建优惠券发放规则发放优惠券
		"""
		{
			"name": "全体券3",
			"count": 1,
			"members": ["bill"]
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon3_id_1",
				"money": 100.00,
				"status": "未使用"
			}
		]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'全体券3'的码库
		"""
		{
			"coupon3_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon3_id_2": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

@mall2 @promotion @promotionSendCoupon   @send_coupon @eugene
Scenario: 4 发送优惠券总数超出优惠券库存
	jobs添加"优惠券规则"后，将优惠券发放给1个会员或多个会员
	1. jobs发放优惠券总数超出库存，jobs能够看到提示信息
	2. bill访问jobs的webapp时不能看到优惠券
	3. jobs能获得发放的优惠券的优惠券码库

	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	When jobs创建优惠券发放规则发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 5,
			"members": ["bill"]
		}
		"""
	Then jobs能获得发放优惠券失败的信息
		"""
		{
			"error_message": "发放数量大于优惠券库存,请先增加库存"
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	When jobs创建优惠券发放规则发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 3,
			"members": ["bill", "tom"],
			"coupon_ids": []
		}
		"""
	Then jobs能获得发放优惠券失败的信息
		"""
		{
			"error_message": "发放数量大于优惠券库存,请先增加库存"
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[]
		"""
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

@mall2 @promotion @promotionSendCoupon
Scenario: 5 给用户发放'仅未下单用户可领取'的优惠券
	Given jobs登录系统
	And jobs已添加支付方式
		"""
		[{
			"type": "微众卡支付"
		}, {
			"type": "货到付款"
		}, {
			"type": "微信支付"
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "未下单用户单品券",
			"money": 10.00,
			"limit_counts": "不限",
			"count": 5,
			"is_no_order_user":"true",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon5_id_",
			"coupon_product": "商品1"
		},{
			"name": "未下单用户全体券",
			"money": 100.00,
			"limit_counts": "1",
			"count": 6,
			"is_no_order_user":"true",
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon4_id_"
		}]
		"""
	#给存在不同订单状态的用户发放优惠券
		#未支付订单用户，可以领取优惠券
			When bill访问jobs的webapp::apiserver
			When bill购买jobs的商品::apiserver
				"""
				{
					"order_id":"001",
					"pay_type": "微信支付",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then bill成功创建订单::apiserver
				"""
				{
					"order_no":"001",
					"status": "待支付",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			Given jobs登录系统
			When jobs创建优惠券发放规则发放优惠券
				"""
				{
					"name": "未下单用户单品券",
					"count": 1,
					"members": ["bill"],
					"coupon_ids": ["coupon5_id_1"]
				}
				"""
			When bill访问jobs的webapp
			Then bill能获得webapp优惠券列表
				"""
				[{
					"coupon_id": "coupon5_id_1",
					"money": 10.00,
					"status": "未使用"
				}]
				"""

		#待发货订单用户，不可以领取优惠券
			When tom访问jobs的webapp::apiserver
			When tom购买jobs的商品::apiserver
				"""
				{
					"order_id":"002",
					"pay_type": "货到付款",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then tom成功创建订单::apiserver
				"""
				{
					"order_no":"002",
					"status": "待发货",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			Given jobs登录系统
			When jobs创建优惠券发放规则发放优惠券
				"""
				{
					"name": "未下单用户单品券",
					"count": 1,
					"members": ["tom"],
					"coupon_ids": ["coupon5_id_2"]
				}
				"""
			When tom访问jobs的webapp
			Then tom能获得webapp优惠券列表
				"""
				[]
				"""

		#已发货订单用户，不可以领取优惠券
			Given tom1关注jobs的公众号
			When tom1访问jobs的webapp::apiserver
			When tom1购买jobs的商品::apiserver
				"""
				{
					"order_id":"003",
					"pay_type": "货到付款",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then tom1成功创建订单::apiserver
				"""
				{
					"order_no":"003",
					"status": "待发货",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

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
			When jobs创建优惠券发放规则发放优惠券
				"""
				{
					"name": "未下单用户单品券",
					"count": 1,
					"members": ["tom1"],
					"coupon_ids": ["coupon5_id_2"]
				}
				"""
			When tom1访问jobs的webapp
			Then tom1能获得webapp优惠券列表
				"""
				[]
				"""

		#已完成订单用户，不可以领取优惠券
			Given tom2关注jobs的公众号
			When tom2访问jobs的webapp::apiserver
			When tom2购买jobs的商品::apiserver
				"""
				{
					"order_id":"004",
					"pay_type": "货到付款",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then tom2成功创建订单::apiserver
				"""
				{
					"order_no":"004",
					"status": "待发货",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			Given jobs登录系统
			When jobs对订单进行发货
				"""
				{
					"order_no": "004",
					"logistics": "申通快递",
					"number": "229388967650",
					"shipper": "jobs"
				}
				"""
			When jobs完成订单'004'

			When jobs创建优惠券发放规则发放优惠券
				"""
				{
					"name": "未下单用户单品券",
					"count": 1,
					"members": ["tom2"],
					"coupon_ids": ["coupon5_id_2"]
				}
				"""
			When tom2访问jobs的webapp
			Then tom2能获得webapp优惠券列表
				"""
				[]
				"""
		
		#退款中和退款完成订单用户，可以领取优惠券
			Given tom3关注jobs的公众号
			When tom3访问jobs的webapp::apiserver
			When tom3购买jobs的商品::apiserver
				"""
				{
					"order_id":"005",
					"pay_type": "微信支付",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			When tom3使用支付方式'微信支付'进行支付
			Then tom3成功创建订单::apiserver
				"""
				{
					"order_no":"005",
					"status": "待发货",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			Given jobs登录系统
			When jobs对订单进行发货
				"""
				{
					"order_no": "004",
					"logistics": "申通快递",
					"number": "229388967650",
					"shipper": "jobs"
				}
				"""
			
			When jobs'申请退款'订单'005'

			When jobs创建优惠券发放规则发放优惠券
				"""
				{
					"name": "未下单用户单品券",
					"count": 1,
					"members": ["tom3"],
					"coupon_ids": ["coupon5_id_2"]
				}
				"""
			When tom3访问jobs的webapp
			Then tom3能获得webapp优惠券列表
				"""
				[{
					"coupon_id": "coupon5_id_2",
					"money": 10.00,
					"status": "未使用"
				}]
				"""

			Given jobs登录系统
			When jobs通过财务审核'退款成功'订单'005'

			When jobs创建优惠券发放规则发放优惠券
				"""
				{
					"name": "未下单用户单品券",
					"count": 1,
					"members": ["tom3"],
					"coupon_ids": ["coupon5_id_3"]
				}
				"""
			When tom3访问jobs的webapp
			Then tom3能获得webapp优惠券列表
				"""
				[{
					"coupon_id": "coupon5_id_2",
					"money": 10.00,
					"status": "未使用"
				},{
					"coupon_id": "coupon5_id_3",
					"money": 10.00,
					"status": "未使用"
				}]
				"""

		#已取消订单用户，可以领取优惠券
			Given tom4关注jobs的公众号
			When tom4访问jobs的webapp::apiserver
			When tom4购买jobs的商品::apiserver
				"""
				{
					"order_id":"006",
					"pay_type": "微信支付",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then tom4成功创建订单::apiserver
				"""
				{
					"order_no":"006",
					"status": "待支付",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			Given jobs登录系统
			When jobs取消订单'006'
			When jobs创建优惠券发放规则发放优惠券
				"""
				{
					"name": "未下单用户单品券",
					"count": 1,
					"members": ["tom4"],
					"coupon_ids": ["coupon5_id_4"]
				}
				"""
			When tom4访问jobs的webapp
			Then tom4能获得webapp优惠券列表
				"""
				[{
					"coupon_id": "coupon5_id_4",
					"money": 10.00,
					"status": "未使用"
				}]
				"""

	#给多人群发优惠券，只有符合条件的用户可以领取到优惠券
		Given jobs登录系统
		When jobs创建优惠券发放规则发放优惠券
			"""
			{
				"name": "未下单用户全体券",
				"count": 1,
				"members": ["bill","tom","tom1","tom2","tom3","tom4"],
				"coupon_ids": ["coupon4_id_1","coupon4_id_2","coupon4_id_3","coupon4_id_4","coupon4_id_5","coupon4_id_6"]
			}
			"""
		When bill访问jobs的webapp
		Then bill能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon4_id_1",
				"money": 100.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon5_id_1",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom访问jobs的webapp
		Then tom能获得webapp优惠券列表
			"""
			[]
			"""

		When tom1访问jobs的webapp
		Then tom1能获得webapp优惠券列表
			"""
			[]
			"""

		When tom2访问jobs的webapp
		Then tom2能获得webapp优惠券列表
			"""
			[]
			"""

		When tom3访问jobs的webapp
		Then tom3能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon4_id_2",
				"money": 100.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon5_id_3",
				"money": 10.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon5_id_2",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom4访问jobs的webapp
		Then tom4能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon4_id_3",
				"money": 100.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon5_id_4",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

	#限制另一张的优惠券，没人只能领一张
		Given jobs登录系统
		When jobs创建优惠券发放规则发放优惠券
			"""
			{
				"name": "未下单用户单品券",
				"count": 1,
				"members": ["bill"],
				"coupon_ids": ["coupon4_id_4"]
			}
			"""
		When bill访问jobs的webapp
		Then bill能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon4_id_1",
				"money": 100.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon5_id_1",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

