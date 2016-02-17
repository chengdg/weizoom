#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
Feature: 在webapp中购买参与满减活动的商品
	用户能在webapp中购买"参与满减活动的商品"

Background:
	Given jobs登录系统
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
	When jobs创建满减活动
		"""
		[{
			"name": "商品1满减",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"price_threshold": 100.0,
			"cut_money": 10.5
		}, {
			"name": "商品3满减",
			"start_date": "今天",
			"end_date": "2天后",
			"products": ["商品3"],
			"price_threshold": 70.0,
			"cut_money": 10.0,
			"is_enable_cycle_mode": true
		}]
		"""
	Given bill关注jobs的公众号
	And tom关注jobs的公众号


@mall.promotion @mall.webapp.promotion
Scenario: 购买单个满减商品，满足价格阈值
	
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
			"status": "待支付",
			"final_price": 89.5,
			"product_price": 100.00,
			"promotion_saved_money": 10.5,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 1,
				"promotion": {
					"type": "price_cut"
				}
			}]
		}
		"""


@mall.promotion @mall.webapp.promotion
Scenario: 购买单个满减商品，超出价格阈值，但不是循环满减
	
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 189.5,
			"product_price": 200.00,
			"promotion_saved_money": 10.5,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 2,
				"promotion": {
					"type": "price_cut"
				}
			}]
		}
		"""

@mall.promotion @mall.webapp.promotion
Scenario: 购买单个满减商品，超出价格阈值，同时也是循环满减
	
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品3",
				"count": 3
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 130.0,
			"product_price": 150.00,
			"promotion_saved_money": 20.0,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品3",
				"count": 3,
				"promotion": {
					"type": "price_cut"
				}
			}]
		}
		"""


@mall.promotion @mall.webapp.promotion
Scenario: 购买多个满减商品
	
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}, {
				"name": "商品3",
				"count": 3
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 319.5,
			"product_price": 350.00,
			"promotion_saved_money": 30.5,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 2
			}, {
				"name": "商品3",
				"count": 3
			}]
		}
		"""


@mall.promotion @mall.webapp.promotion
Scenario: 购买单个满减商品，超出库存限制
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