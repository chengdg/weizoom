# __edit__ : "benchi"
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
	#商品6是新加的
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
						"stock_type": "有限",
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


@mall2 @mall.webapp @mall.coupon @bc1
Scenario: 1 使用少于商品价格的优惠券金额进行购买
	bill购买jobs的商品时，能使用少于商品价格的优惠券
	1. 创建订单成功，订单状态为“等待支付”
	2. 优惠券状态变为“被bill使用”
	3. 再次使用优惠券码，购物失败
	
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		'''
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_3": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			},
			"coupon1_id_4": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			}
		}
		'''
	When bill访问jobs的webapp
	#第一次使用
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}],
			"coupon": "coupon1_id_1"
		}
		'''
	Then bill成功创建订单
		'''
		{
			"status": "待支付",
			"final_price": 199.0,
			"product_price": 200.0,
			"coupon_money": 1.0,
			"promotion_saved_money": 0.0,
			"postage": 0.00,
			"integral_money":0.00
		}
		'''
	#第二次使用
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}],
			"coupon": "coupon1_id_1"
		}
		'''
	Then bill获得创建订单失败的信息'该优惠券已使用'
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		'''
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		'''


@mall2 @mall.webapp @mall.coupon 
Scenario: 2 使用多于商品价格的优惠券金额进行购买
	bill购买jobs的商品时，能使用多于商品价格的优惠券
	1. 订单状态直接变为'等待发货'
	2. 优惠券状态变为“被bill使用”
	
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券2'的码库
		'''
		{
			"coupon2_id_1": {
				"money": 100.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 100.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		'''
	When bill访问jobs的webapp
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}],
			"coupon": "coupon2_id_1"
		}
		'''
	Then bill成功创建订单
		'''
		{
			"status": "待发货",
			"final_price": 0.0,
			"product_price": 50.0,
			"coupon_money": 50.0
		}
		'''
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券2'的码库
		'''
		{
			"coupon2_id_1": {
				"money": 100.0,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 100.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		'''


@mall2 @mall.webapp @mall.coupon 
Scenario: 3 使用等于商品价格的优惠券金额进行购买
	bill购买jobs的商品时，能使用等于商品价格的优惠券
	1. 订单状态直接变为'等待发货'
	2. 优惠券状态变为“被bill使用”
	
	When bill访问jobs的webapp
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon2_id_1"
		}
		'''
	Then bill成功创建订单
		'''
		{
			"status": "待发货",
			"final_price": 0.0,
			"product_price": 100.0,
			"coupon_money": 100.0
		}
		'''
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券2'的码库
		'''
		{
			"coupon2_id_1": {
				"money": 100.0,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 100.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		'''


@mall2 @mall.webapp @mall.coupon 
Scenario: 4 输入错误的优惠券码进行购买
	bill购买jobs的商品时，输入错误的优惠券码
	1. 创建订单失败
	2. 优惠券状态不变
	
	When bill访问jobs的webapp
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon_23"
		}
		'''
	Then bill获得创建订单失败的信息'请输入正确的优惠券号'
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		'''
		{
			"coupon1_id_1": {
				"status": "未使用"
			},
			"coupon1_id_2": {
				"status": "未使用"
			}
		}
		'''
	Then jobs能获得优惠券'优惠券2'的码库
		'''
		{
			"coupon2_id_1": {
				"status": "未使用"
			},
			"coupon2_id_2": {
				"status": "未使用"
			}
		}
		'''
	Then jobs能获得优惠券'优惠券3'的码库
		'''
		{
			"coupon3_id_1": {
				"status": "未使用"
			},
			"coupon3_id_2": {
				"status": "未使用"
			}
		}
		'''


@mall2 @mall.webapp @mall.coupon 
Scenario: 5 输入未领取的可用优惠券码进行购买，bill创建订单成功，优惠券状态变为已使用
	
	When bill访问jobs的webapp
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon3_id_4"
		}
		'''
	# Then bill获得创建订单失败的信息'请输入正确的优惠券号'

	Then bill成功创建订单
		'''
		{
			"status": "待支付",
			"final_price": 99.0,
			"product_price": 100.0,
			"coupon_money": 1.0,
			"promotion_saved_money": 0.0,
			"postage": 0.00,
			"integral_money":0.00
		}
		'''

	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		'''
		{
			"coupon1_id_1": {
				"status": "未使用"
			},
			"coupon1_id_2": {
				"status": "未使用"
			}
		}
		'''
	Then jobs能获得优惠券'优惠券2'的码库
		'''
		{
			"coupon2_id_1": {
				"status": "未使用"
			},
			"coupon2_id_2": {
				"status": "未使用"
			}
		}
		'''
	Then jobs能获得优惠券'优惠券3'的码库
		'''
		{
			"coupon3_id_1": {
				"status": "未使用"
			},
			"coupon3_id_2": {
				"status": "未使用"
			},
			"coupon3_id_4": {
				"money": 1.0,
				"status": "已使用",
				"consumer": "bill",
				"target": ""
			}
		}
		'''


@mall2 @mall.webapp @mall.coupon 
Scenario: 6 输入已过期的优惠券码进行购买
	bill购买jobs的商品时，使用已过期的优惠券进行购买
	1. 购物失败
	
	When bill访问jobs的webapp
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon4_id_1"
		}
		'''
	Then bill获得创建订单失败的信息'该优惠券已过期'
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券4'的码库
		'''
		{
			"coupon4_id_1": {
				"money": 10.0,
				"status": "已过期",
				"consumer": "",
				"target": "bill"
			},
			"coupon4_id_2": {
				"money": 10.0,
				"status": "已过期",
				"consumer": "",
				"target": "bill"
			}
		}
		'''


@mall2 @mall.webapp @mall.coupon 
Scenario: 7 输入别人的优惠券码进行购买
	bill购买jobs的商品时，能使用tom的优惠券进行购买
	1. 购物失败
	
	When bill访问jobs的webapp
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon1_id_3"
		}
		'''
	Then bill获得创建订单失败的信息'该优惠券已被他人领取不能使用'
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		'''
		{
			"coupon1_id_3": {
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			},
			"coupon1_id_4": {
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			}
		}
		'''


@mall2 @mall.webapp @mall.coupon 
Scenario: 8 使用满金额条件的优惠券，购买小于金额条件的商品
	bill购买jobs的商品时，商品金额小于优惠券使用金额
	1. 购物失败
	
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券3'的码库
		'''
		{
			"coupon3_id_1": {
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		'''
	When bill访问jobs的webapp
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品4",
				"count": 1
			}],
			"coupon": "coupon3_id_1"
		}
		'''
	Then bill获得创建订单失败的信息'该优惠券不满足使用金额限制'
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券3'的码库
		'''
		{
			"coupon3_id_1": {
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		'''


@mall2 @mall.webapp @mall.coupon
Scenario: 9 使用满金额条件的优惠券，购买等于金额条件的商品
	bill购买jobs的商品时，商品金额等于优惠券使用金额
	1. 购物成功
	
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券3'的码库
		'''
		{
			"coupon3_id_1": {
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		'''
	When bill访问jobs的webapp
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}],
			"coupon": "coupon3_id_1"
		}
		'''
	Then bill成功创建订单
		'''
		{
			"status": "待支付",
			"final_price": 49.0,
			"product_price": 50.0,
			"coupon_money": 1.0
		}
		'''
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券3'的码库
		'''
		{
			"coupon3_id_1": {
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			}
		}
		'''

@mall2 @mall.webapp @mall.coupon  
Scenario: 10 使用满金额条件的优惠券，购买大于金额条件的商品
	bill购买jobs的商品时，商品金额大于优惠券使用金额
	
	
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券3'的码库
		'''
		{
			"coupon3_id_1": {
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		'''
	When bill访问jobs的webapp
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品4",
				"count": 2
			}],
			"coupon": "coupon3_id_1"
		}
		'''
	Then bill成功创建订单
		'''
		{
			"status": "待支付",
			"final_price": 79.0,
			"product_price": 80.0,
			"coupon_money": 1.0
		}
		'''
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券3'的码库
		'''
		{
			"coupon3_id_1": {
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			}
		}
		'''

@mall2 @mall.webapp @mall.coupon  
Scenario: 11 购买多规格商品，买1个商品的两个规格，总价格满足优惠劵使用条件
	
	
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券5'的码库
		'''
		{
			"coupon5_id_1": {
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		'''
	When bill访问jobs的webapp
	When bill购买jobs的商品
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
			"coupon": "coupon5_id_1"
		}
		'''
	Then bill成功创建订单
		'''
		{
			"status": "待支付",
			"final_price": 70.0,
			"product_price": 80.0,
			"coupon_money": 10.0
		}
		'''
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券5'的码库
		'''
		{
			"coupon5_id_1": {
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			}
		}
		'''

@mall2 @mall.webapp @mall.coupon
Scenario: 12 使用多于商品价格的优惠券进行购买，且不能抵扣运费
	bill购买jobs的商品时，优惠券金额大于商品金额时
	1.只抵扣商品金额，不能抵扣运费


	Given jobs登录系统
	Then jobs能获得优惠券'优惠券2'的码库
		'''
		{
			"coupon2_id_1": {
				"money": 100.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 100.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		'''
	When bill访问jobs的webapp
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品6",
				"count": 1
			}],
			"coupon": "coupon2_id_1"
		}
		'''
	Then bill成功创建订单
		'''
		{
			"status": "待支付",
			"final_price": 10.00,
			"product_price": 20.00,
			"postage": 10.00,
			"coupon_money": 20.00
		}
		'''
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券2'的码库
		'''
		{
			"coupon2_id_1": {
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			}
		}
		'''