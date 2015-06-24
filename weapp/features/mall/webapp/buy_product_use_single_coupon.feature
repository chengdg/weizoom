# __edit__ : "benchi"
@func:webapp.modules.mall.views.list_products
Feature: 在webapp中使用优惠券购买商品（使用单品劵购买）
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
		[ {
			"name": "商品1",
			"price": 200.00
		},{
			"name": "商品2",
			"price": 200.00
		},{
			"name": "商品3",
			"price": 20.00
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
	#优惠券6是新加的
	Given jobs已添加了优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 1,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "商品1"
		}, {
			"name": "优惠券2",
			"money": 10,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品3"
		}, {
			"name": "优惠券5",
			"money": 10,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon5_id_",
			"coupon_product": "商品5"
		}, {
			"name": "优惠券6",
			"money": 100,
			"start_date": "今天",
			"end_date": "2天后",
			"coupon_id_prefix": "coupon6_id_",
			"coupon_product": "商品6"
		}]
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill领取jobs的优惠券
		"""
		[{
			"name": "优惠券1",
			"coupon_ids": ["coupon1_id_2", "coupon1_id_1"]
		},{
			"name": "优惠券2",
			"coupon_ids": ["coupon2_id_2", "coupon2_id_1"]
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
		}, {
			"name": "优惠券6",
			"coupon_ids": ["coupon6_id_2", "coupon6_id_1"]
		}]
		"""


@mall2 @mall.webapp @mall.coupon 
Scenario: 1 使用单品优惠劵进行购买，该单品券适用于商品1，如果商品2使用，则，购买失败
	
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
			}
		}
		'''
	When bill访问jobs的webapp
	#第一次使用 购买商品1，成功
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品1",
				"count": 1
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
	#第二次使用 购买商品2 购买失败
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品2",
				"count": 1
			}],
			"coupon": "coupon1_id_2"
		}
		'''
	Then bill获得创建订单失败的信息'该优惠券不能购买订单中的商品'
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
Scenario: 2 使用单品优惠劵进行购买，该单品券适用于商品3并且商品3满50元才可以使用，而不是订单满50可用
		1 买3件商品3，共60元，满足条件，可用单品劵；
		2 买1件商品3，买一件商品2，订单满50，但单品不满50，不可以使用该单品卷
	
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券2'的码库
		'''
		{
			"coupon2_id_1": {
				"money": 10.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 10.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		'''
	When bill访问jobs的webapp
	#第一次使用 购买3个商品3，满足使用条件，成功
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品3",
				"count": 3
			}],
			"coupon": "coupon2_id_1"
		}
		'''
	Then bill成功创建订单
		'''
		{
			"status": "待支付",
			"final_price": 50.0,
			"product_price": 60.0,
			"coupon_money": 10.0,
			"promotion_saved_money": 0.0,
			"postage": 0.00,
			"integral_money":0.00
		}
		'''
	#第二次使用 购买商品3+商品2 订单购买失败
	When bill购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品3",
				"count": 1
			},{
				"name": "商品2",
				"count": 1
			}],
			"coupon": "coupon2_id_2"
		}
		'''
	Then bill获得创建订单失败的信息'该优惠券指定商品金额不满足使用条件'
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券2'的码库
		'''
		{
			"coupon2_id_1": {
				"money": 10.0,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 10.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		'''
@mall2 @mall.webapp @mall.coupon  
Scenario: 3 购买多规格商品，买1个商品的两个规格，总价格满足优惠劵使用条件
	
	
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
Scenario: 4 使用多于商品价格的单品券进行购买，该单品券只适用于商品6
	且不抵扣其他商品金额和运费金额

	Given jobs登录系统
	Then jobs能获得优惠券'优惠券6'的码库
		'''
		{
			"coupon6_id_1": {
				"money": 100.0,
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			},
			"coupon6_id_2": {
				"money": 100.0,
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			}
		}
		'''
	When tom访问jobs的webapp
	When tom购买jobs的商品
		'''
		{
			"products": [{
				"name": "商品3",
				"count": 1
			},{
				"name": "商品6",
				"count": 1
			}],
			"coupon": "coupon6_id_1"
		}
		'''
	Then tom成功创建订单
		'''
		{
			"status": "待支付",
			"final_price": 30.0,
			"product_price": 40.0,
			"postage": 10.00,
			"coupon_money": 20.0
		}
		'''
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券6'的码库
		'''
		{
			"coupon6_id_1": {
				"status": "已使用",
				"consumer": "tom",
				"target": "tom"
			}
		}
		'''
