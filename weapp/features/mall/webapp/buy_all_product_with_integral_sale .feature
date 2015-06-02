#  "benchi"
Feature: 在webapp中购买参与积分应用活动的商品
	jobs 设置 订单积分抵扣上限 后 用户能在webapp中能够对所有商品使用积分购买
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
			"一元等价的积分数量": 2,
			"订单积分抵扣上限": 50
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


	Given bill关注jobs的公众号
	And tom关注jobs的公众号


@mall2 @mall.promotion @mall.webapp.promotion  
Scenario: 1 购买单种一个商品，积分金额小于最大折扣金额

	When bill访问jobs的webapp
	When bill获得jobs的50会员积分
	Then bill在jobs的webapp中拥有50会员积分
	When bill购买jobs的商品
		"""
		{	"integral_money":25.00,
			"integral":50.00,
			"products": [{
				"name": "商品1",
				"count": 1
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
			"integral":50.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	Then bill在jobs的webapp中拥有0会员积分

@mall2 @mall.promotion @mall.webapp.promotion 
Scenario: 2 购买单种多个商品，积分金额等于最大折扣金额

	When bill访问jobs的webapp
	When bill获得jobs的400会员积分
	Then bill在jobs的webapp中拥有400会员积分
	When bill购买jobs的商品
		"""
		{
			"integral_money":200.00,
			"integral":400,
			"products": [{
				"name": "商品2",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 200.0,
			"product_price": 400.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":200.00,
			"integral":400,
			"coupon_money":0.00,
			"products": [{
				"name": "商品2",
				"count": 2
			}]
		}
		"""
	Then bill在jobs的webapp中拥有0会员积分

@mall2 @mall.promotion @mall.webapp.promotion 
Scenario:  3 购买多个商品，已有总积分金额大于最大折扣金额

	When bill访问jobs的webapp
	When bill获得jobs的160会员积分
	Then bill在jobs的webapp中拥有160会员积分
	When bill购买jobs的商品
		"""
		{
			"integral_money":75.00,
			"integral":150.00,
			"products": [{
				"name": "商品1",
				"count": 1
			}, {
				"name": "商品3",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 75.0,
			"product_price": 150.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":75.00,
			"integral":150.00,
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
	Then bill在jobs的webapp中拥有10会员积分

@mall2 @mall.promotion @mall.webapp.promotion 
Scenario: 4 购买单个多规格商品+一个普通商品


	When bill访问jobs的webapp
	When bill获得jobs的150会员积分
	Then bill在jobs的webapp中拥有150会员积分
	When bill购买jobs的商品
		"""
		{
			"integral_money": 65.00,
			"integral": 130.00,
			"products": [{
				"name": "商品5",
				"count": 1,
				"model": "S"
			}, {
				"name": "商品5",
				"count": 1,
				"model": "M"
			}, {
				"name": "商品3",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 65.0,
			"product_price": 130.00,
			"integral_money": 65.00,
			"integral": 130.00,
			"products": [{
				"name": "商品5",
				"count": 1,
				"model": "S"
			}, {
				"name": "商品5",
				"count": 1,
				"model": "M"
			}, {
				"name": "商品3",
				"count": 1
			}]
		}
		"""
	Then bill在jobs的webapp中拥有20会员积分

@mall2 @mall.promotion @mall.webapp.promotion 
Scenario: 5 购买单个限时抢购商品，同时使用积分购买
	
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
		{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"promotion_price": 10
		}
		"""
	When bill访问jobs的webapp
	When bill获得jobs的50会员积分
	Then bill在jobs的webapp中拥有50会员积分
	When bill购买jobs的商品
		"""
		{
			"integral_money":5.00,
			"integral":10.00,
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 5.0,
			"product_price": 10.00,
			"promotion_saved_money":90.00,
			"postage": 0.00,
			"integral_money":5.00,
			"integral":10.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 1,
				"total_price": 100.00
			}]
		}
		"""
	Then bill在jobs的webapp中拥有40会员积分

@mall2 @mall.promotion @mall.webapp.promotion 
Scenario: 6 购买单个限时抢购商品， 买赠商品，同时使用积分购买
	
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
		{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"promotion_price": 10
		}
		"""

	When jobs创建买赠活动
		"""
		{
			"name": "商品2买一赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品2"],
			"premium_products": [{
				"name": "商品4",
				"count": 5
			}],
			"count": 1,
			"is_enable_cycle_mode": true
		}
		"""
	When bill访问jobs的webapp
	When bill获得jobs的500会员积分
	Then bill在jobs的webapp中拥有500会员积分
	When bill购买jobs的商品
		"""
		{
			"integral_money":205.00,
			"integral":410.00,
			"products": [{
				"name": "商品1",
				"count": 1
			},{
				"name": "商品2",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 205.0,
			"product_price": 410.00,
			"promotion_saved_money":90.00,
			"postage": 0.00,
			"integral_money":205.00,
			"integral":410.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 1,
				"price": 10.00,
				"total_price": 100.00
			},{
				"name": "商品2",
				"count": 2
			},{
				"name": "商品4",
				"count": 10,
				"price": 0,
				"promotion": {
					"type": "premium_sale:premium_product"
				}
			}]
		}
		"""
	Then bill在jobs的webapp中拥有90会员积分