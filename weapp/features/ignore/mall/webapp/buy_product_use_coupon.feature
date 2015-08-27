@func:webapp.modules.mall.views.list_products
Feature: 在webapp中使用优惠券购买商品
	bill能在webapp中使用优惠券购买jobs添加的"商品"

Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 9.9
		}, {
			"name": "商品2",
			"price": 8.8
		}, {
			"name": "商品3",
			"price": 10.0
		}, {
			"name": "商品4",
			"model": {
				"models": {
					"standard": {
						"price": 11.0,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			} 
		}]	
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "1元券",
			"money": 1,
			"expire_days": 1,
			"using_limit": "无限制"
		}, {
			"name": "10元券",
			"money": 10,
			"expire_days": 1,
			"using_limit": "无限制"
		}, {
			"name": "满10元可用1元券",
			"money": 1,
			"expire_days": 2,
			"using_limit": "满10元可以使用"
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}]
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	And bill设置jobs的webapp的默认收货地址
	And tom关注jobs的公众号


@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 使用少于商品价格的优惠券金额进行购买
	bill购买jobs的商品时，能使用少于商品价格的优惠券
	1. 订单支付成功，订单状态为'等待发货'
	2. 优惠券状态变为“被bill使用”
	3. bill用户中心中“我的优惠券”发生变化
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"coupon_rule": "1元券",
			"count": 2,
			"members": ["bill"],
			"coupon_ids": ["coupon_1", "coupon_2"]
		}
		"""
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "1元券",
			"coupon_id": "coupon_2",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}, {
			"coupon_rule": "1元券",
			"coupon_id": "coupon_1",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		"""
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon_1": {
					"price": 1.0,
					"status": "还剩23小时过期"
				},
				"coupon_2": {
					"price": 1.0,
					"status": "还剩23小时过期"
				}
			},
			"used": {},
			"expired": {}
		}
		"""
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}],
			"coupon_type": "选择",
			"coupon": "coupon_1"
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"cover": "下单成功"
		}
		"""
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon_2": {
					"price": 1.0,
					"status": "还剩23小时过期"
				}
			},
			"used": {
				"coupon_1": {
					"price": 1.0,
					"status": "bill已使用"
				}
			},
			"expired": {}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "1元券",
			"coupon_id": "coupon_2",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}, {
			"coupon_rule": "1元券",
			"coupon_id": "coupon_1",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "已使用",
			"consumer": "bill",
			"target": "bill"
		}]
		"""


@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 使用多于商品价格的优惠券金额进行购买
	bill购买jobs的商品时，能使用多于商品价格的优惠券
	1. 订单状态直接变为'待发货'
	2. 优惠券状态变为“被bill使用”
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"coupon_rule": "10元券",
			"count": 2,
			"members": ["bill"],
			"coupon_ids": ["coupon_1", "coupon_2"]
		}
		"""
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "10元券",
			"coupon_id": "coupon_2",
			"money": 10.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}, {
			"coupon_rule": "10元券",
			"coupon_id": "coupon_1",
			"money": 10.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		"""
	When bill访问jobs的webapp:ui
	When bill使用'不支付'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "选择",
			"coupon": "coupon_1"
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"cover": "下单成功"
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "10元券",
			"coupon_id": "coupon_2",
			"money": 10.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "bill"
		}, {
			"coupon_rule": "10元券",
			"coupon_id": "coupon_1",
			"money": 10.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "已使用",
			"consumer": "bill",
			"target": "bill"
		}]
		"""


@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 使用等于商品价格的优惠券金额进行购买
	bill购买jobs的商品时，能使用等于商品价格的优惠券
	1. 订单状态直接变为'等待发货'
	2. 优惠券状态变为“被bill使用”
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"coupon_rule": "10元券",
			"count": 2,
			"members": ["bill"],
			"coupon_ids": ["coupon_1", "coupon_2"]
		}
		"""
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "10元券",
			"coupon_id": "coupon_2",
			"money": 10.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}, {
			"coupon_rule": "10元券",
			"coupon_id": "coupon_1",
			"money": 10.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		"""
	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}],
			"coupon_type": "选择",
			"coupon": "coupon_1"
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "10元券",
			"coupon_id": "coupon_2",
			"money": 10.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "bill"
		}, {
			"coupon_rule": "10元券",
			"coupon_id": "coupon_1",
			"money": 10.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "已使用",
			"consumer": "bill",
			"target": "bill"
		}]
		"""


@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 输入错误的优惠券码进行购买
	bill购买jobs的商品时，输入错误的优惠券码
	1. 创建订单失败
	2. 优惠券状态不变
	3. 我的优惠券不变
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"coupon_rule": "10元券",
			"count": 2,
			"members": ["bill"],
			"coupon_ids": ["coupon_11111", "coupon_22222"]
		}
		"""
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "10元券",
			"coupon_id": "coupon_22222",
			"money": 10.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}, {
			"coupon_rule": "10元券",
			"coupon_id": "coupon_11111",
			"money": 10.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		"""
	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon_3"
		}
		"""
	Then bill获得创建订单失败的信息'优惠券码格式不正确':ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon_33333"
		}
		"""
	Then bill获得创建订单失败的信息'请输入正确的优惠券号':ui
	Given jobs登录系统
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "10元券",
			"coupon_id": "coupon_22222",
			"money": 10.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}, {
			"coupon_rule": "10元券",
			"coupon_id": "coupon_11111",
			"money": 10.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		"""


@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 输入手工发放的优惠券码进行购买
	bill购买jobs的商品时，能使用没有领取但是是手工发放的优惠券进行购买
	1. 购买后优惠券状态变为“被bill使用”
	2. 再次使用已被使用的优惠券会导致购物失败
	3. bill的“我的优惠券”不出现使用的优惠券
	
	Given jobs登录系统
	When jobs手工为优惠券规则生成优惠券
		"""
		{
			"coupon_rule": "1元券",
			"count": 2,
			"coupon_ids": ["coupon_11111", "coupon_22222"]
		}
		"""
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "1元券",
			"coupon_id": "coupon_22222",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "手工"
		}, {
			"coupon_rule": "1元券",
			"coupon_id": "coupon_11111",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "手工"
		}]
		"""
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {},
			"used": {},
			"expired": {}
		}
		"""
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon_11111"
		}
		"""
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon_11111"
		}
		"""
	Then bill获得创建订单失败的信息'该优惠券已使用':ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {},
			"used": {},
			"expired": {}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "1元券",
			"coupon_id": "coupon_22222",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "手工"
		}, {
			"coupon_rule": "1元券",
			"coupon_id": "coupon_11111",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "已使用",
			"consumer": "bill",
			"target": "手工"
		}]
		"""


@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 输入别人的优惠券码进行购买
	bill购买jobs的商品时，能使用jobs发放给tom的优惠券进行购买
	1. 购买后优惠券状态变为“被bill使用”
	2. bill再次使用已被使用的优惠券会导致购物失败
	3. tom使用被bill使用后的优惠券导致购物失败
	4. tom的“我的优惠券”受影响
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"coupon_rule": "1元券",
			"count": 2,
			"members": ["tom"],
			"coupon_ids": ["coupon_11111", "coupon_22222"]
		}
		"""
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "1元券",
			"coupon_id": "coupon_22222",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "tom"
		}, {
			"coupon_rule": "1元券",
			"coupon_id": "coupon_11111",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"consumer": "",
			"target": "tom"
		}]
		"""
	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon_11111"
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货"
		}
		"""	
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon_11111"
		}
		"""
	Then bill获得创建订单失败的信息'该优惠券已使用':ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {},
			"used": {},
			"expired": {}
		}
		"""
	When tom访问jobs的webapp:ui
	When tom使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon_11111"
		}
		"""
	Then tom获得创建订单失败的信息'该优惠券已使用':ui
	Then tom在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon_22222": {
					"price": 1.0,
					"status": "还剩23小时过期"
				}
			},
			"used": {
				"coupon_11111": {
					"price": 1.0,
					"status": "bill已使用"
				}
			},
			"expired": {}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "1元券",
			"coupon_id": "coupon_22222",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "tom"
		}, {
			"coupon_rule": "1元券",
			"coupon_id": "coupon_11111",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "已使用",
			"consumer": "bill",
			"target": "tom"
		}]
		"""


@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 使用优惠券购买影响库存
	bill使用优惠券购买jobs的商品时
	1. 购买成功，商品库存减少
	2. 购买失败，商品库存不变
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"coupon_rule": "1元券",
			"count": 2,
			"members": ["bill"],
			"coupon_ids": ["coupon_11111", "coupon_22222"]
		}
		"""
	Given jobs登录系统:ui
	Then jobs能获取商品'商品4':ui
		"""
		{
			"name": "商品4",
			"model": {
				"models": {
					"standard": {
						"price": 11.0,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			} 
		}
		"""
	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon_11111"
		}
		"""
	Given jobs登录系统:ui
	Then jobs能获取商品'商品4':ui
		"""
		{
			"name": "商品4",
			"model": {
				"models": {
					"standard": {
						"price": 11.0,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			} 
		}
		"""
	When bill访问jobs的webapp:ui
	And bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon_33333"
		}
		"""
	Then bill获得创建订单失败的信息'请输入正确的优惠券号':ui
	Given jobs登录系统:ui
	Then jobs能获取商品'商品4':ui
		"""
		{
			"name": "商品4",
			"model": {
				"models": {
					"standard": {
						"price": 11.0,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			} 
		}
		"""


@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 使用满金额条件的优惠券
	bill购买jobs的商品时，能使用满金额条件的优惠券
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"coupon_rule": "满10元可用1元券",
			"count": 2,
			"members": ["bill"],
			"coupon_ids": ["coupon_11111", "coupon_22222"]
		}
		"""
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "满10元可用1元券",
			"coupon_id": "coupon_22222",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "后天",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}, {
			"coupon_rule": "满10元可用1元券",
			"coupon_id": "coupon_11111",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "后天",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		"""

	#购买不满足金额限制的商品，失败
	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon_11111"
		}
		"""
	Then bill获得创建订单失败的信息'该优惠券不满足使用金额限制':ui

	#购买商品价格等于金额限制的商品，成功
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon_11111"
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货"
		}
		"""

	#购买商品价格大于金额限制的商品，成功
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon_22222"
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货"
		}
		"""	
	Given jobs登录系统
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "满10元可用1元券",
			"coupon_id": "coupon_22222",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "后天",
			"status": "已使用",
			"consumer": "bill",
			"target": "bill"
		}, {
			"coupon_rule": "满10元可用1元券",
			"coupon_id": "coupon_11111",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "后天",
			"status": "已使用",
			"consumer": "bill",
			"target": "bill"
		}]
		"""


@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 使用过期的优惠券
	bill购买jobs的商品时，能使用过期优惠券
	1. 购物失败
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"coupon_rule": "1元券",
			"count": 2,
			"expire_date": "昨天",
			"members": ["bill"],
			"coupon_ids": ["coupon_11111", "coupon_22222"]
		}
		"""
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "1元券",
			"coupon_id": "coupon_22222",
			"money": 1.0,
			"status": "已过期",
			"consumer": "",
			"target": "bill"
		}, {
			"coupon_rule": "1元券",
			"coupon_id": "coupon_11111",
			"money": 1.0,
			"status": "已过期",
			"consumer": "",
			"target": "bill"
		}]
		"""
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {},
			"used": {},
			"expired": {
				"coupon_11111": {
					"price": 1.0,
					"status": "已过期"
				}, 
				"coupon_22222": {
					"price": 1.0,
					"status": "已过期"
				}
			}
		}
		"""
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon_11111"
		}
		"""
	Then bill获得创建订单失败的信息'该优惠券已使用':ui