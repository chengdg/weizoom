Feature:jobs管理系统里待支付的订单，用户可以在手机端直接取消

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100,
			"stocks": 8
		 }]
		"""
	And bill关注jobs的公众号
	And jobs已有的会员
		"""
		[{
			"name": "bill",
			"integral":"150"
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 1,
			"coupon_id_prefix": "coupon1_id_"
		},{
			"name": "优惠券2",
			"money": 50.00,
			"count": 1,
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	And jobs设定会员积分策略
		"""
		{
			"use_ceiling": 100,
			"use_condition": "on",
			"integral_each_yuan": 1
		}
		"""
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"order_id": "001",
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	And bill购买jobs的商品
		"""
		{
			"order_id":"002",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon1_id_1"
		}
		"""
	And bill购买jobs的商品
		"""
		{
			"order_id":"003",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"integral": 100
		}
		"""
	And bill购买jobs的商品
		"""
		{
			"order_id":"004",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon2_id_1",
			"integral": 50
		}
		"""

@mall2 @order @allOrder   @mall.order_cancel_status @mall.order_cancel_status.member
Scenario:1 bill取消订单
	bill取消订单'001'
	1. bill手机端订单状态改变为'已取消'
	2. jobs后端订单状态改变为'已取消'
	3. '商品1'库存改为为:1

	When bill取消订单'001'
	Then bill手机端获取订单'001'状态
		"""
		{
			"order_no": "001",
			"status": "已取消"
		}
		"""
	Given jobs登录系统
	Then jobs后端订单状态改变为
		"""
		{
			"order_no": "001",
			"status": "已取消"
		}
		"""
	Then jobs后端获取"商品1"库存
		"""
		{
			"name": "商品1",
			"stocks": 5
		}
		"""

@mall2 @order @allOrder   @mall.order_cancel_status @mall.order_cancel_status.coupon_member @pyliu
Scenario:2 bill取消使用了优惠券的订单
	bill取消订单'002'
	1. bill手机端订单状态改变为'已取消'
	2. jobs后端订单状态改变为'已取消'
	3. '商品1'库存改为为:2
	4. 优惠券'coupon1_id_1'状态改变为'未使用'

	When bill取消订单'002'
	Then bill手机端获取订单'002'状态
		"""
		{
			"order_no": "002",
			"status": "已取消"
		}
		"""
	Given jobs登录系统
	Then jobs后端订单状态改变为
		"""
		{
			"order_no": "002",
			"status": "已取消"
		}
		"""
	Then jobs后端获取"商品1"库存
		"""
		{
			"name": "商品1",
			"stocks": 5
		}
		"""
	Then jobs获取优惠券'coupon1_id_1'状态
		"""
		{
			"coupon_code": "coupon1_id_1",
			"coupon_status": "未使用"
		}
		"""

@mall2 @order @allOrder   @mall.order_cancel_status @mall.order_cancel_status.integral_member @pyliu02
Scenario:3 bill取消使用了积分的订单
	bill取消订单'003'
	1. bill手机端订单状态改变为'已取消'
	2. jobs后端订单状态改变为'已取消'
	3. '商品1'库存改为为:2
	4. 积分数值改变为：'100'

	When bill取消订单'003'
	Then bill手机端获取订单'003'状态
		"""
		{
			"order_no": "003",
			"status": "已取消"
		}
		"""
	Then bill获取积分数值
		"""
		{
			"integral":"100"
		}
		"""
	Given jobs登录系统
	Then jobs后端订单状态改变为
		"""
		{
			"order_no": "003",
			"status": "已取消"
		}
		"""
	Then jobs后端获取"商品1"库存
		"""
		{
			"name": "商品1",
			"stocks": 5
		}
		"""

@mall2 @order @allOrder   @mall.order_cancel_status @mall.order_cancel_status.integral_and_coupon_member @pyliu
Scenario:4 bill取消使用积分和优惠券的订单
	bill取消订单'004'
	1. bill手机端订单状态改变为'已取消'
	2. jobs后端订单状态改变为'已取消'
	3. '商品1'库存改为为:2
	4. 积分数值改变为：'100'
	5. 优惠券'2345678'状态改变为'未使用'

	When bill取消订单'004'
	Then bill手机端获取订单'004'状态
		"""
		{
			"order_no": "004",
			"status": "已取消"
		}
		"""
	Then bill获取积分数值
		"""
		{
			"integral": "50"
		}
		"""
	Given jobs登录系统
	Then jobs后端订单状态改变为
		"""
		{
			"order_no": "004",
			"status": "已取消"
		}
		"""
	Then jobs后端获取"商品1"库存
		"""
		{
			"name": "商品1",
			"stocks": 5
		}
		"""
	Then jobs获取优惠券'coupon2_id_1'状态
		"""
		{
			"coupon_code": "coupon2_id_1",
			"coupon_status": "未使用"
		}
		"""
