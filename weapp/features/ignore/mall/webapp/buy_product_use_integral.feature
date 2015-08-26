@func:webapp.modules.mall.views.list_products
Feature: 在webapp中使用会员积分购买商品
	bill能在webapp中使用会员积分购买jobs添加的"商品"

Background:
	Given jobs登录系统
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
	And jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 5
		}
		"""
	When jobs添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号
	When bill访问jobs的webapp
	And bill设置jobs的webapp的默认收货地址


@ui @ui-mall @ui-member @ui-member.integral
Scenario: 使用少于商品金额的积分金额进行购买，并查看积分日志
	bill购买jobs的商品时，使用少于商品金额的积分金额进行购买
	1. 创建订单成功, 订单状态为“等待支付”
	2. bill积分减少
	3. bill能看到积分日志
	
	When bill访问jobs的webapp
	When bill获得jobs的5会员积分
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有5会员积分:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"use_integral": true
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"price_info": {
				"integral_count": 5,
				"integral_money": 1.0
			}
		}
		"""
	And bill在jobs的webapp中拥有0会员积分:ui
	And bill在jobs的webapp中的积分日志为:ui
		"""
		[{
			"integral": -5,
			"event": "使用积分"
		}, {
			"integral": 20,
			"event": "首次关注"
		}]
		"""


@ui @ui-mall @ui-member @ui-member.integral
Scenario: 使用等于商品金额的积分金额进行购买
	bill购买jobs的商品时，使用等于商品金额的积分金额进行购买
	1. 创建订单成功, 订单状态为“等待发货”
	2. bill积分减少
	
	When bill访问jobs的webapp
	When bill获得jobs的50会员积分
	Then bill在jobs的webapp中拥有50会员积分
	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}],
			"use_integral": true
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"cover": "下单成功",
			"price_info": {
				"integral_count": 50,
				"integral_money": 10
			}
		}
		"""
	And bill在jobs的webapp中拥有0会员积分:ui


@ui @ui-mall @ui-member @ui-member.integral
Scenario: 使用大于商品金额的积分金额进行购买
	bill购买jobs的商品时，使用等于商品金额的积分金额进行购买
	1. 创建订单失败
	2. bill积分不变
	3. 49.5积分会自动调整为50积分
	
	When bill访问jobs的webapp
	When bill获得jobs的500会员积分
	Then bill在jobs的webapp中拥有500会员积分
	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"use_integral": true
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"price_info": {
				"integral_count": 50,
				"integral_money": 10
			}
		}
		"""
	Then bill在jobs的webapp中拥有450会员积分:ui


@ui @ui-mall @ui-member @ui-member.integral
Scenario: 使用积分购买影响商品库存
	bill购买jobs的商品时，使用积分购买
	1. 创建订单成功, 商品库存减少
	2. 创建订单失败，商品库存不变
	
	Given jobs登录系统
	Then jobs能获取商品'商品4'
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
	When bill访问jobs的webapp
	When bill获得jobs的500会员积分
	Then bill在jobs的webapp中拥有500会员积分
	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 2
			}],
			"use_integral": true
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货"
		}
		"""
	#job登录，验证库存减少
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
						"stocks": 1
					}
				}
			} 
		}
		"""
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有390会员积分
