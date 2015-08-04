Feature:jobs管理系统里待支付的订单，用户可以在手机端直接取消

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100,
			"stocks": 4
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
	And jobs添加优惠券
		"""
		[{
			"coupon_code": "12345678",
			"coupon_price": 100
		},{
			"coupon_code": "23456789",
			"coupon_price": 50
		}]
		"""
	And jobs已有的订单
		"""
		[{
			"order_no": "001",
			"member": "bill",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"status": "待支付"
		},{
			"order_no":"002",
			"member": "bill",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_code": "12345678",
			"status": "待支付"
		},{
			"order_no":"003",
			"member": "bill",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"integral": 100,
			"status": "待支付"

		},{
			"order_no":"004",
			"member": "bill",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon_code": "23456789",
			"integral": 50,
			"status": "待支付"
		}]
		"""

@mall2 @mall.order_cancel_status @mall.order_cancel_status.member
Scenario:bill取消订单
	bill取消订单'001'
	1. bill手机端订单状态改变为'已取消'
	2. jobs后端订单状态改变为'已取消'
	3. '商品1'库存改为为:1

	When bill访问jobs的webapp
	When bill取消订单'001'
	Then bill手机端获取订单'001'状态
		"""
		{
			"order_no": "001",
			"status": "已取消"
		}
		"""
	Then jobs后端订单状态改变为
		"""
		{
			"order_no": "001",
			"status": "已取消"
		}
		"""
	Then job后端获取"商品1"库存
		"""
		{
			"name": "商品1",
			"stocks": 5
		}
		"""

@mall2 @mall.order_cancel_status @mall.order_cancel_status.coupon_member @pyliu
Scenario:bill取消使用了优惠券的订单
	bill取消订单'002'
	1. bill手机端订单状态改变为'已取消'
	2. jobs后端订单状态改变为'已取消'
	3. '商品1'库存改为为:2
	4. 优惠券'12345678'状态改变为'未使用'

	When bill访问jobs的webapp
	When bill取消订单'002'
	Then bill手机端获取订单'002'状态
		"""
		{
			"order_no": "002",
			"status": "已取消"
		}
		"""
	Then jobs后端订单状态改变为
		"""
		{
			"order_no": "002",
			"status": "已取消"
		}
		"""
	Then job后端获取"商品1"库存
		"""
		{
			"name": "商品1",
			"stocks": 5
		}
		"""
	Then jobs获取优惠券'12345678'状态
		"""
		{
			"coupon_code": "12345678",
			"coupon_status": "未使用"
		}
		"""

@mall2 @mall.order_cancel_status @mall.order_cancel_status.integral_member @pyliu02
Scenario:bill取消使用了积分的订单
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
	Then jobs后端订单状态改变为
		"""
		{
			"order_no": "003",
			"status": "已取消"
		}
		"""
	Then job后端获取"商品1"库存
		"""
		{
			"name": "商品1",
			"stocks": 5
		}
		"""
	Then bill获取积分数值
		"""
		{
			"integral":"100"
		}
		"""

@mall2 @mall.order_cancel_status @mall.order_cancel_status.integral_and_coupon_member @pyliu
Scenario:bill取消使用积分和优惠券的订单
	bill取消订单'004'
	1. bill手机端订单状态改变为'已取消'
	2. jobs后端订单状态改变为'已取消'
	3. '商品1'库存改为为:2
	4. 积分数值改变为：'100'
	5. 优惠券'2345678'状态改变为'未使用'

	When bill访问jobs的webapp
	When bill取消订单'004'
	Then bill手机端获取订单'004'状态
		"""
		{
			"order_no": "004",
			"status": "已取消"
		}
		"""
	Then jobs后端订单状态改变为
		"""
		{
			"order_no": "004",
			"status": "已取消"
		}
		"""
	Then job后端获取"商品1"库存
		"""
		{
			"name": "商品1",
			"stocks": 5
		}
		"""
	Then bill获取积分数值
		"""
		{
			"integral": "50"
		}
		"""
	Then jobs获取优惠券'23456789'状态
		"""
		{
			"coupon_code": "23456789",
			"coupon_status": "未使用"
		}
		"""
