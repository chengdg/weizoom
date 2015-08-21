# __edit__ : "新新"
@func:webapp.modules.mall.views.list_products
Feature: 在webapp中使用优惠券购买商品（使用全局优惠劵）
	bill能在webapp中使用优惠券购买jobs添加的"商品"

Background:
	Given jobs登录系统
	And jobs已添加商品规格
		"""
		[{
			"name": "尺寸",
			"type": "文字",
			"values": [{
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
			"price": 100.00,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "商品2",
			"price": 200.00
		}, {
			"name": "商品3",
			"price": 50.00
		}, {
			"name": "商品4",
			"model": {
				"models": {
					"standard": {
						"price": 40.00,
						"stock_type"1: "有限",
						"stocks": 20
					}
				}
			}
		}, {
			"name": "商品5",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 40.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 40.00,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品6",
			"price": 20.00,
			"weight": 1,
			"postage": 10.00
		}]
		"""
	#支付方式
	Given jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	Given jobs已添加了优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 1,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "优惠券2",
			"money": 100,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_"
		}, {
			"name": "优惠券3",
			"money": 1,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
		}, {
			"name": "优惠券4",
			"money": 10,
			"start_date": "前天",
			"end_date": "昨天",
			"coupon_id_prefix": "coupon4_id_"
		}, {
			"name": "优惠券5",
			"money": 10,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon5_id_"
		}]
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	And bill设置jobs的webapp的默认收货地址
	When bill领取jobs的优惠券
		"""
		[{
			"name": "优惠券1",
			"coupon_ids": ["coupon1_id_2", "coupon1_id_1"]
		}, {
			"name": "优惠券2",
			"coupon_ids": ["coupon2_id_2", "coupon2_id_1"]
		}, {
			"name": "优惠券3",
			"coupon_ids": ["coupon3_id_2", "coupon3_id_1"]
		}, {
			"name": "优惠券4",
			"coupon_ids": ["coupon4_id_2", "coupon4_id_1"]
		}, {
			"name": "优惠券5",
			"coupon_ids": ["coupon5_id_2", "coupon5_id_1"]
		}]
		"""
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom领取jobs的优惠券
		"""
		[{
			"name": "优惠券1",
			"coupon_ids": ["coupon1_id_3", "coupon1_id_4"]
		}]
		"""
	And tom设置jobs的webapp的默认收货地址

# __edit__ : "新新"
@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 1 使用少于商品价格的优惠券金额进行购买
	bill购买jobs的商品时，能使用少于商品价格的优惠券
	1. 订单支付成功，订单状态为'等待发货'
	2. 优惠券状态变为“被bill使用”
	3. bill用户中心中“我的优惠券”发生变化
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		'''
		{
			"coupon_rule": "优惠券1",
			"count": 2,
			"members": ["bill"],
			"coupon_ids": ["coupon1_id_1", "coupon1_id_2"]
		}
		'''
	Then jobs能获得优惠券列表

		'''
		[{
			"coupon_rule": "优惠券1",
			"coupon_id": "coupon1_id_2",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		},{
			"coupon_rule": "优惠券1",
			"coupon_id": "coupon1_id_1",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		'''
	#第一次使用
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon1_id_2": {
					"coupon_rule": "优惠券1",
					"money": 1.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				},{
				"coupon1_id_1": {
					"coupon_rule": "优惠券1",
					"money": 1.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				}

			},
			"used": {},
			"expired": {}
		}
		"""
	When bill使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}],
			"coupon_type": "选择",
			"coupon": "coupon1_id_1"
		}
		'''
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
				"coupon1_id_2": {
					"coupon_rule": "优惠券1",
					"money": 1.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				}
			},
			"used": {
				"coupon1_id_1": {
					"coupon_rule": "优惠券1",
					"money": 1.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				}
			},
			"expired": {}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券1",
			"coupon_id": "coupon1_id_2",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		},{
			"coupon_rule": "优惠券1",
			"coupon_id": "coupon1_id_1",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "已使用",
			"consumer": "bill",
			"target": "bill"
		}]
		'''

# __edit__ : "新新"
@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 2 使用多于商品价格的优惠券金额进行购买
	bill购买jobs的商品时，能使用多于商品价格的优惠券
	1. 订单状态直接变为'待发货'
	2. 优惠券状态变为“被bill使用”
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		'''
		{
			"coupon_rule": "优惠券2",
			"count": 2,
			"members": ["bill"],
			"coupon_ids": ["coupon2_id_1", "coupon2_id_2"]
		}
		'''
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_2",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		},{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_1",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		'''

	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon2_id_2": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				},{
				"coupon2_id_1": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				}

			},
			"used": {},
			"expired": {}
		}
		"""
	When bill使用'微信支付'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}],
			"coupon_type": "选择",
			"coupon": "coupon2_id_1"
		}
		'''
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
				"coupon2_id_2": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
			}},
			"used": {
				"coupon2_id_1": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
			}},
			"expired": {}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_2",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		},{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_1",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "已使用",
			"consumer": "bill",
			"target": "bill"
		}]
		'''
# __edit__ : "新新"
@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 3 使用等于商品价格的优惠券金额进行购买
	bill购买jobs的商品时，能使用等于商品价格的优惠券
	1. 订单状态直接变为'等待发货'
	2. 优惠券状态变为“被bill使用”
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		'''
		{
			"coupon_rule": "优惠券2",
			"count": 2,
			"members": ["bill"],
			"coupon_ids": ["coupon2_id_1", "coupon2_id_2"]
		}
		'''
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_2",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		},{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_1",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		'''
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon2_id_2": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				},{
				"coupon2_id_1": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				}

			},
			"used": {},
			"expired": {}
		}
		"""
	When bill使用'微信支付'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "选择",
			"coupon": "coupon2_id_1"
		}
		'''
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
				"coupon2_id_2": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
			}},
			"used": {
				"coupon2_id_1": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
			}},
			"expired": {}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_2",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		},{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_1",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "已使用",
			"consumer": "bill",
			"target": "bill"
		}]
		'''

# __edit__ : "新新"
@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 4 输入错误的优惠券码进行购买
	bill购买jobs的商品时，输入错误的优惠券码
	1. 创建订单失败
	2. 优惠券状态不变
	
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		'''
		{
			"coupon_rule": "优惠券2",
			"count": 2,
			"members": ["bill"],
			"coupon_ids": ["coupon2_id_1", "coupon2_id_2"]
		}
		'''
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_2",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		},{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_1",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		'''
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon2_id_2": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				},{
				"coupon2_id_1": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				}

			},
			"used": {},
			"expired": {}
		}
		"""
	When bill使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon2_id_3"
		}
		'''
	Then bill获得创建订单失败的信息'优惠券码格式不正确':ui
	When bill使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon2_id_33333333"
		}
		'''
	Then bill获得创建订单失败的信息'请输入正确的优惠券号':ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon2_id_2": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				},{
				"coupon2_id_1": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				}

			},
			"used": {},
			"expired": {}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_2",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		},{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_1",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		'''
# __edit__ : "新新"
Scenario: 5 输入未领取的可用优惠券码进行购买，bill创建订单成功，优惠券状态变为已使用
	Given jobs登录系统
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券1",
			"coupon_id": "coupon1_id_1",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": ""
		}]
		'''
	When bill访问jobs的webapp:ui
	
	When bill使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon1_id_1"
		}
		'''
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"cover": "下单成功"
		}
		"""
	
	Given jobs登录系统
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券1",
			"coupon_id": "coupon1_id_1",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "已使用",
			"consumer": "bill",
			"target": ""
		}]
		'''
# __edit__ : "新新"
@ui @ui-mall @ui-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 6 输入已过期的优惠券码进行购买
	bill购买jobs的商品时，使用已过期的优惠券进行购买
	1. 购物失败
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		'''
		{
			"coupon_rule": "优惠券4",
			"count": 1,
			"members": ["bill"],
			"coupon_ids": ["coupon4_id_1"]
		}
		'''
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券4",
			"coupon_id": "coupon4_id_1",
			"money": 10.0,
			"status": "已过期",
			"consumer": "",
			"target": "bill"
		}]
		'''
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {},
			"used": {},
			"expired": {
				"coupon4_id_1": {
					"price": 10.0,
					"status": "已过期"
				}
			}
		}
		"""
	When bill使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "选择",
			"coupon": "coupon4_id_1"
		}
		'''
	Then bill获得创建订单失败的信息'该优惠券已过期':ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {},
			"used": {},
			"expired": {
				"coupon4_id_1": {
					"price": 10.0,
					"status": "已过期"
				}
			}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券4",
			"coupon_id": "coupon4_id_1",
			"money": 10.0,
			"create_date": "前天",
			"expire_date": "昨天",
			"status": "已过期",
			"consumer": "",
			"target": "bill"
		}]
		'''
# __edit__ : "新新"
Scenario: 7 输入别人的优惠券码进行购买
	bill购买jobs的商品时，能使用jobs发放给tom的优惠券进行购买
	1. 购物失败
	
	Given jobs登录系统
	When jobs为会员发放优惠券
		'''
		{
			"coupon_rule": "优惠券1",
			"count": 1,
			"members": ["tom"],
			"coupon_ids": ["coupon1_id_1"]
		}
		'''
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券1",
			"coupon_id": "coupon1_id_1",
			"money": 1.00,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "tom"
		}]
		'''
	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_type": "输入",
			"coupon": "coupon1_id_1"
		}
		'''
	Then bill获得创建订单失败的信息'该优惠券已被他人领取不能使用':ui
	Given jobs登录系统
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券1",
			"coupon_id": "coupon1_id_1",
			"money": 1.00,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "tom"
		}]
		'''
# __edit__ : "新新"
@ui @ui-mall @ui111-mall.webapp @ui-market_tool.coupon @ui-market_tool
Scenario: 8 使用满金额条件的优惠券,购买小于金额条件的商品
	bill购买jobs的商品时，能使用满金额小于优惠券使用金额
	1. 购物失败
	Given jobs登录系统
	When jobs为会员发放优惠券
		'''
		{
			"coupon_rule": "优惠券3",
			"count": 1,
			"members": ["bill"],
			"coupon_ids": ["coupon3_id_1"]
		}
		'''
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券3",
			"coupon_id": "coupon3_id_1",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "2天后",
			"using_limit": "满50元可以使用",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		'''

	#购买不满足金额限制的商品，失败
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon3_id_1": {
					"coupon_rule": "优惠券3",
					"money": 1.00,
					"create_date": "今天",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满50元可以使用",
				},
			"used": {},
			"expired": {}
		}
		"""
	When bill使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品4",
				"count": 1
			}],
			"coupon_type": "选择",
			"coupon": "coupon3_id_1"
		}
		'''
	Then bill获得创建订单失败的信息'该优惠券不满足使用金额限制':ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon3_id_1": {
					"coupon_rule": "优惠券3",
					"money": 1.00,
					"create_date": "今天",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满50元可以使用",
				},
			"used": {},
			"expired": {}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券3",
			"coupon_id": "coupon3_id_1",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "2天后",
			"using_limit": "满50元可以使用",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		'''
# __edit__ : "新新"
Scenario: 9 使用满金额条件的优惠券，购买等于金额条件的商品
	bill购买jobs的商品时，商品金额等于优惠券使用金额
	1. 购物成功
	#购买商品价格等于金额限制的商品，成功
	Given jobs登录系统
	When jobs为会员发放优惠券
		'''
		{
			"coupon_rule": "优惠券3",
			"count": 1,
			"members": ["bill"],
			"coupon_ids": ["coupon3_id_1"]
		}
		'''
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券3",
			"coupon_id": "coupon3_id_1",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "2天后",
			"using_limit": "满50元可以使用",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		'''
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon3_id_1": {
					"coupon_rule": "优惠券3",
					"money": 1.00,
					"create_date": "今天",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满50元可以使用",
				},
			"used": {},
			"expired": {}
		}
		"""
	When bill使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}],
			"coupon_type": "选择",
			"coupon": "coupon3_id_1"
		}
		'''

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
			"unused": {},
			"used": {
				"coupon3_id_1": {
					"coupon_rule": "优惠券3",
					"money": 1.00,
					"create_date": "今天",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满50元可以使用"
				}},
			"expired": {}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券3",
			"coupon_id": "coupon3_id_1",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "2天后",
			"using_limit": "满50元可以使用",
			"status": "已使用",
			"consumer": "bill",
			"target": "bill"
		}]
		'''
# __edit__ : "新新"
Scenario: 10 使用满金额条件的优惠券，购买大于金额条件的商品
	bill购买jobs的商品时，商品金额大于优惠券使用金额
	#购买商品价格大于金额限制的商品，成功
	Given jobs登录系统
	When jobs为会员发放优惠券
		'''
		{
			"coupon_rule": "优惠券3",
			"count": 1,
			"members": ["bill"],
			"coupon_ids": ["coupon3_id_1"]
		}
		'''
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券3",
			"coupon_id": "coupon3_id_1",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "2天后",
			"using_limit": "满50元可以使用",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		'''
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon3_id_1": {
					"coupon_rule": "优惠券3",
					"money": 1.00,
					"create_date": "今天",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满50元可以使用"
				}},
			"used": {},
			"expired": {}
		}
		"""
	When bill使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品4",
				"count": 2
			}],
			"coupon_type": "选择",
			"coupon": "coupon3_id_1"
		}
		'''
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
			"unused": {},
			"used": {
				"coupon3_id_1": {
					"coupon_rule": "优惠券3",
					"money": 1.00,
					"create_date": "今天",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满50元可以使用"
				}},
			"expired": {}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券3",
			"coupon_id": "coupon3_id_1",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "2天后",
			"using_limit": "满50元可以使用",
			"status": "已使用",
			"consumer": "bill",
			"target": "bill"
		}]
		'''
# __edit__ : "新新"


Scenario: 11 购买多规格商品，买1个商品的两个规格，总价格满足优惠劵使用条件

	Given jobs登录系统
	When jobs为会员发放优惠券
		'''
		{
			"coupon_rule": "优惠券5",
			"count": 1,
			"members": ["bill"],
			"coupon_ids": ["coupon5_id_1"]
		}
		'''
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "满50元可以使用",
			"coupon_id": "coupon5_id_1",
			"money": 10.0,
			"create_date": "今天",
			"expire_date": "2天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		'''
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon5_id_1": {
					"coupon_rule": "优惠券5",
					"money": 10.00,
					"create_date": "今天",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满50元可以使用"
				}},
			"used": {},
			"expired": {}
		}
		"""
	When bill使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品5",
				"count": 1,
				"model": "M"
			},{
				"name": "商品5",
				"count": 1,
				"model": "S"
			}],
			"coupon_type": "选择",
			"coupon": "coupon5_id_1"
		}
		'''
	
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
			"unused": {},
			"used": {
				"coupon5_id_1": {
					"coupon_rule": "优惠券5",
					"money": 10.00,
					"create_date": "今天",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满50元可以使用"
				}},
			"expired": {}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "满50元可以使用",
			"coupon_id": "coupon5_id_1",
			"money": 1.0,
			"create_date": "今天",
			"expire_date": "2天后",
			"status": "已使用",
			"consumer": "bill",
			"target": "bill"
		}]
		'''
# __edit__ : "新新"
Scenario: 12 使用多于商品价格的优惠券进行购买，且不能抵扣运费
	bill购买jobs的商品时，优惠券金额大于商品金额时
	1.只抵扣商品金额，不能抵扣运费

	Given jobs登录系统
	When jobs为会员发放优惠券
		'''
		{
			"coupon_rule": "优惠券2",
			"count": 2,
			"members": ["bill"],
			"coupon_ids": ["coupon2_id_1", "coupon2_id_2"]
		}
		'''
	Then jobs能获得优惠券列表

		'''
		[{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_2",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		},{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_1",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		}]
		'''
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon2_id_2": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				},{
				"coupon2_id_1": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
				}

			},
			"used": {},
			"expired": {}
		}
		"""
	When bill使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品6",
				"count": 1
			}],
			"coupon_type": "选择",
			"coupon": "coupon2_id_1"
		}
		'''
	
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
				"coupon2_id_2": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
			}},
			"used": {
				"coupon2_id_1": {
					"coupon_rule": "优惠券2",
					"money": 100.00,
					"create_date": "今天",
					"expire_date": "1天后",
					"scope":"全店通用券",
					"condition":"不限制"
			}},
			"expired": {}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表

		'''
		[{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_2",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		},{
			"coupon_rule": "优惠券2",
			"coupon_id": "coupon2_id_1",
			"money": 100.0,
			"create_date": "今天",
			"expire_date": "1天后",
			"status": "已使用",
			"consumer": "bill",
			"target": "bill"
		}]
		'''
# __edit__ : "新新" 

Scenario:13 不同等级的会员购买有会员价同时使用全体券的商品

#（全体券和会员价可以同时使用，但是满多少钱可以使用计算的是会员价）

Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品9",
			"price": 100.00,
			"is_member_product": "on",
			"weight": 1,
			"postage": "系统"
		},{
			"name": "商品10",
			"price": 100.00,
			"is_member_product": "on",
			"weight": 1,
			"postage": "系统"
		}]
		"""
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"discount": "10"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	When nokia关注jobs的公众号
	Given jobs登录系统
	When jobs更新"nokia"的会员等级
		"""
		{
			"name": "nokia",
			"member_rank": "金牌会员"
		}
		"""
	When jobs更新"bill"的会员等级
		"""
		{
			"name": "bill",
			"member_rank": "铜牌会员"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "nokia",
			"member_rank": "金牌会员"
		}, {
			"name": "tom",
			"member_rank": "普通会员"
		}, {
			"name": "bill",
			"member_rank": "铜牌会员"
		}]
		"""
	Given jobs已添加了优惠券规则
		"""
		[{
			"name": "全体券1",
			"money": 20,
			"limit_counts": 3,
			"start_date": "2天前",
			"end_date": "2天后",
			"using_limit": "满100元可以使用",
			"coupon_id_prefix": "coupon9_id_"
		}]
		"""
	Given jobs登录系统
	When jobs为会员发放优惠券
		'''
		{
			"coupon_rule": "全体券1",
			"count": 3,
			"members": ["tom","bill","nokia"],
			"coupon_ids": ["coupon9_id_"]
		}
		'''
	Then jobs能获得优惠券列表

		'''
		[{
			"coupon_rule": "全体券1",
			"coupon_id": "coupon9_id_3",
			"money": 100.0,
			"create_date": "2天前",
			"expire_date": "2天后",
			"status": "未使用",
			"consumer": "",
			"target": "nokia"
		},{
			"coupon_rule": "全体券1",
			"coupon_id": "coupon9_id_2",
			"money": 100.0,
			"create_date": "2天前",
			"expire_date": "2天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		},{
			"coupon_rule": "全体券1",
			"coupon_id": "coupon9_id_1",
			"money": 100.0,
			"create_date": "2天前",
			"expire_date": "2天后",
			"status": "未使用",
			"consumer": "",
			"target": "tom"
		}]
		'''
#tom
	When tom访问jobs的webapp:ui
	Then tom在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon9_id_1": {
					"coupon_rule": "全体券1",
					"money": 100.00,
					"create_date": "2天前",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满100元可以使用"
				},
			"used": {},
			"expired": {}
		}
		"""
	When tom使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品9",
				"count": 1
			}],
			"coupon_type": "选择",
			"coupon": "coupon9_id_1"
		}
		'''
	
	Then tom获得支付结果:ui
		"""
		{
			"status": "待发货",
			"cover": "下单成功"
		}
		"""
	Then tom在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {},
			"used": {
				"coupon9_id_1": {
					"coupon_rule": "全体券1",
					"money": 100.00,
					"create_date": "2天前",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满100元可以使用"
				}},
			"expired": {}
		}
		"""
#bill
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon9_id_2": {
					"coupon_rule": "全体券1",
					"money": 100.00,
					"create_date": "2天前",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满100元可以使用"
				}},
			"used": {},
			"expired": {}
		}
		"""
	When bill使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品9",
				"count": 1
			}],
			"coupon_type": "选择",
			"coupon": "coupon9_id_2"
		}
		'''
	Then bill获得错误提示'该优惠券不满足使用金额限制':ui
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
				"coupon9_id_2": {
					"coupon_rule": "全体券1",
					"money": 100.00,
					"create_date": "2天前",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满100元可以使用"
				}},
			"used": {},
			"expired": {}
		}
		"""
#nokia
	When nokia访问jobs的webapp:ui
	Then nokia在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {
				"coupon9_id_3": {
					"coupon_rule": "全体券1",
					"money": 100.00,
					"create_date": "2天前",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满100元可以使用"
				}},
			"used": {},
			"expired": {}
		}
		"""
	When nokia使用'货到付款'购买jobs的商品:ui
		'''
		{
			"products": [{
				"name": "商品9",
				"count": 1
			}, {
			"name": "商品10",
			"count": 1
		}],
			"coupon_type": "选择",
			"coupon": "coupon9_id_3"
		}
		'''
	
	Then nokia获得支付结果:ui
		"""
		{
			"status": "待发货",
			"cover": "下单成功"
		}
		"""
	Then nokia在jobs的webapp中拥有优惠券:ui
		"""
		{
			"unused": {},
			"used": {
				"coupon9_id_3": {
					"coupon_rule": "全体券1",
					"money": 100.00,
					"create_date": "2天前",
					"expire_date": "2天后",
					"scope":"全店通用券",
					"using_limit": "满100元可以使用"
				}},
			"expired": {}
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "全体券1",
			"coupon_id": "coupon9_id_3",
			"money": 20.0,
			"create_date": "2天前",
			"expire_date": "2天后",
			"status": "已使用",
			"consumer": "nokia",
			"target": "nokia"
		},{
			"coupon_rule": "全体券1",
			"coupon_id": "coupon9_id_2",
			"money": 20.0,
			"create_date": "2天前",
			"expire_date": "2天后",
			"status": "未使用",
			"consumer": "",
			"target": "bill"
		},{
			"coupon_rule": "全体券1",
			"coupon_id": "coupon9_id_1",
			"money": 20.0,
			"create_date": "2天前",
			"expire_date": "2天后",
			"status": "已使用",
			"consumer": "tom",
			"target": "tom"
		}]
		'''