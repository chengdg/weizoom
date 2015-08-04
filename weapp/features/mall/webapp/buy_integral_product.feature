# __author__ : "冯雪静"

Feature: 在webapp中购买积分商品
	bill能在webapp中购买jobs添加的"积分商品"

Background:
	Given jobs登录系统
	And jobs已添加积分商品
		"""
		[{
			"name": "商品1",
			"integral": 100
		}, {
			"name": "商品2",
			"integral": 200
		}]	
		"""
	And jobs已添加运费配置
		"""
		[{
			"name" : "顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00,
			"special_area": [{
				"to_the":"北京市",
				"first_weight_price":20.00,
				"added_weight_price":10.00
			},{
				"to_the":"西藏自治区,内蒙古自治区",
				"first_weight_price":30.00,
				"added_weight_price":20.00
			}]
		}]
		"""
	And bill关注jobs的公众号

@mall @mall.webapp @mall.webapp.integral_buy
Scenario:用户积分大于商品积分时进行购买
	bill用积分购买jobs的积分商品时,bill的积分大于商品的积分
	1. 自动扣除相对应的商品积分
	2. 创建订单成功,订单状态为“等待发货”
	3. bill积分减少
	
	When bill访问jobs的webapp
	When bill获得jobs的500会员积分
	Then bill在jobs的webapp中拥有500会员积分
	When bill购买jobs的商品
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{	
			"type": "积分商品",
			"status": "待发货",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"final_integral": 200,
			"products": [{
				"name": "商品1",
				"integral": 100,
				"count": 2
			}]
		}
		"""
	And bill在jobs的webapp中拥有300会员积分


@mall @mall.webapp @mall.webapp.integral_buy
Scenario:用户积分等于商品积分时进行购买
	bill用积分购买jobs的积分商品时,bill的积分等于商品的积分
	1. 自动扣除相对应的商品积分
	2. 创建订单成功,订单状态为“等待发货”
	3. bill积分减少
	
	When bill访问jobs的webapp
	When bill获得jobs的200会员积分
	Then bill在jobs的webapp中拥有200会员积分
	When bill购买jobs的商品
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品2",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{	
			"type": "积分商品",
			"status": "待发货",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"final_integral": 200,
			"products": [{
				"name": "商品2",
				"integral": 200,
				"count": 1
			}]
		}
		"""
	And bill在jobs的webapp中拥有0会员积分

@mall @mall.webapp @mall.webapp.integral_buy
Scenario:用户积分小于商品积分时进行购买
	bill在购买jobs添加的商品时,bill的积分小于商品的积分
	1. 创建订单失败
	2. bill积分不变
	
	When bill访问jobs的webapp
	When bill获得jobs的100会员积分
	Then bill在jobs的webapp中拥有100会员积分
	When bill购买jobs的商品
		"""
		{	
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品2",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{}
		"""
	And bill在jobs的webapp中拥有100会员积分

@ignore
Scenario:非会员时进行购买
	nokia在购买jobs添加的商品时,nokia是非会员
	1. 购买按钮置灰状态
	2. 创建订单失败
	
	When bill访问jobs的webapp
	When bill把jobs商品列表的链接分享给nokia
	Then nokia通过bill分享的链接访问jobs的商品
	When nokia购买jobs的商品
		"""
		{	
			"ship_name": "nokia",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品2",
				"count": 1
			}]
		}
		"""
	Then bill查看订单
		"""
		{}
		"""
	