Feature: 在webapp中购买参与积分应用活动的商品
	用户能在webapp中购买"参与积分应用活动的商品"

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
		}]
		"""
	Given jobs设定会员积分策略
		"""
		{
			"一元等价的积分数量": 2
		}
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
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"discount": 70,
			"discount_money": 70.0,
			"is_permanant_active": false
		}, {
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "2天后",
			"products": ["商品3"],
			"discount": 50,
			"discount_money": 25.0,
			"is_permanant_active": true
		}, {
			"name": "商品5积分应用",
			"start_date": "今天",
			"end_date": "2天后",
			"products": ["商品5"],
			"discount": 50,
			"discount_money": 25.0,
			"is_permanant_active": true
		}]
		"""
	Given bill关注jobs的公众号
	And tom关注jobs的公众号


@mall2 @mall.promotion @mall.webapp.promotion 
Scenario: 购买单个积分折扣商品，积分金额小于最大折扣金额
	
	When bill访问jobs的webapp
	When bill获得jobs的50会员积分
	Then bill在jobs的webapp中拥有50会员积分
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1,
				"integral": 50
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 75.0,
			"product_price": 100.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":25.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	Then bill在jobs的webapp中拥有0会员积分


@mall2 @mall.promotion @mall.webapp.promotion
Scenario: 购买单个积分折扣商品，积分金额等于最大折扣金额
	
	When bill访问jobs的webapp
	When bill获得jobs的150会员积分
	Then bill在jobs的webapp中拥有150会员积分
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1,
				"integral": 140
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 30.0,
			"product_price": 100.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":70.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	Then bill在jobs的webapp中拥有10会员积分


@mall2 @mall.promotion @mall.webapp.promotion
Scenario: 购买单个积分折扣商品，积分金额大于最大折扣金额
	
	When bill访问jobs的webapp
	When bill获得jobs的150会员积分
	Then bill在jobs的webapp中拥有150会员积分
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1,
				"integral": 150
			}]
		}
		"""
	Then bill获得创建订单失败的信息'使用积分不能大于促销限额'
	Then bill在jobs的webapp中拥有150会员积分


@mall2 @mall.promotion @mall.webapp.promotion
Scenario: 购买多个积分折扣商品，总积分金额小于最大折扣金额
	
	When bill访问jobs的webapp
	When bill获得jobs的150会员积分
	Then bill在jobs的webapp中拥有150会员积分
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1,
				"integral": 50
			}, {
				"name": "商品3",
				"count": 1,
				"integral": 50
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 100.0,
			"product_price": 150.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":50.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 1
			}, {
				"name": "商品3",
				"count": 1
			}]
		}
		"""
	Then bill在jobs的webapp中拥有50会员积分


@mall2 @mall.promotion @mall.webapp.promotion
Scenario: 购买单个积分折扣商品，积分活动还未开始
	积分活动还未开始，按原价下单
	
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品4积分应用",
			"start_date": "1天后",
			"end_date": "2天后",
			"products": ["商品4"],
			"discount": 50,
			"discount_money": 20.0,
			"is_permanant_active": false
		}]
		"""
	When bill访问jobs的webapp
	When bill获得jobs的150会员积分
	Then bill在jobs的webapp中拥有150会员积分
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1,
				"integral": 40
			}]
		}
		"""
	Then bill获得创建订单失败的信息
		"""
		{
			"detail": [{
				"id": "商品4",
				"msg": "积分折扣已经过期",
				"short_msg": "已经过期"
			}]
		}
		"""
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1,
				"integral": 0
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 40.0,
			"product_price": 40.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品4",
				"count": 1
			}]
		}
		"""
	Then bill在jobs的webapp中拥有150会员积分


@mall2 @mall.promotion @mall.webapp.promotion
Scenario: 购买单个积分折扣商品，积分活动已结束，积分活动不是永久有效
	积分活动还未开始，按原价下单
	
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品4积分应用",
			"start_date": "昨天",
			"end_date": "今天",
			"products": ["商品4"],
			"discount": 50,
			"discount_money": 20.0,
			"is_permanant_active": false
		}]
		"""
	When bill访问jobs的webapp
	When bill获得jobs的150会员积分
	Then bill在jobs的webapp中拥有150会员积分
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1,
				"integral": 40
			}]
		}
		"""
	Then bill获得创建订单失败的信息
		"""
		{
			"detail": [{
				"id": "商品4",
				"msg": "积分折扣已经过期",
				"short_msg": "已经过期"
			}]
		}
		"""
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1,
				"integral": 0
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 40.0,
			"product_price": 40.00,
			"integral_money": 0.00,
			"products": [{
				"name": "商品4"
			}]
		}
		"""
	Then bill在jobs的webapp中拥有150会员积分


@mall2 @mall.promotion @mall.webapp.promotion
Scenario: 购买单个积分折扣商品，积分活动已结束，但积分活动设置为永久有效
	积分活动永久有效，按积分折扣后的价格下单
	
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品4积分应用",
			"start_date": "昨天",
			"end_date": "今天",
			"products": ["商品4"],
			"discount": 50,
			"discount_money": 20.0,
			"is_permanant_active": true
		}]
		"""
	When bill访问jobs的webapp
	When bill获得jobs的150会员积分
	Then bill在jobs的webapp中拥有150会员积分
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1,
				"integral": 40
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 20.0,
			"product_price": 40.00,
			"integral_money": 20.00,
			"products": [{
				"name": "商品4"
			}]
		}
		"""
	Then bill在jobs的webapp中拥有110会员积分


@mall2 @mall.promotion @mall.webapp.promotion
Scenario: 购买单个积分折扣商品，超出库存限制
	第一次购买1个，成功；第二次购买2个，超出商品库存，确保缓存更新
	
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付"
		}
		"""
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill获得创建订单失败的信息
		"""
		{
			"detail": [{
				"id": "商品1",
				"msg": "有商品库存不足，请重新下单",
				"short_msg": "库存不足"
			}]
		}
		"""

@mall2 @mall.promotion @mall.webapp.promotion @uncheck1
Scenario: 购买单个,多规格积分折扣商品，积分活动已结束，但积分活动设置为永久有效
	积分活动永久有效，按积分折扣后的价格下单
	
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品5积分应用",
			"start_date": "昨天",
			"end_date": "今天",
			"products": ["商品5"],
			"discount": 50,
			"discount_money": 20.0,
			"is_permanant_active": true
		}]
		"""
	When bill访问jobs的webapp
	When bill获得jobs的150会员积分
	Then bill在jobs的webapp中拥有150会员积分
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品5",
				"count": 1,
				"integral": 40,
				"model": "S"
			}, {
				"name": "商品5",
				"count": 1,
				"integral": 40,
				"model": "M"
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 40.0,
			"product_price": 80.00,
			"integral_money": 40.00,
			"products": [{
				"name": "商品5",
				"count": 1,
				"model": "S"
			}, {
				"name": "商品5",
				"count": 1,
				"model": "M"
			}]
		}
		"""
	Then bill在jobs的webapp中拥有70会员积分