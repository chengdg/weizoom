# __author__ : "冯雪静"

Feature:Manage the test order
	Jobs能通过管理系统为管理会员的测试订单
Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price":"100"
		}]	
		"""
	And jobs已添加了支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}]
		"""
	And tom关注jobs的公众号
	And bill关注jobs的公众号
	
@mall @mall.webapp.test.buy @pyliu
Scenario: 有测试权限的会员购买商品
	tom购买'商品1'后
	1. tom点击'测试购买'时,生成的订单价格为0.01
	2. jobs后台生成测试订单
	3. tom点击'购买'时,商品的价格变保持不变
	4. jobs后台生成普通订单

	When jobs给会员tom"分配"测试权限	
	Then tom获取测试权限
		"""
		{
			"test_whether_permission": "是"
		}
		"""
	When tom访问jobs的webapp
	When tom'测试购买'jobs的'商品1'
	Then jobs生成测试订单
		"""
		{
			"name": "商品1",
			"price": "0.01",
			"order_type":"测试订单",
			"order_status":"待支付"
		}
		"""	
	When tom'购买'jobs的'商品1'
	Then jobs生成普通订单
		"""
		{
			"name": "商品1",
			"price":"100.0",
			"order_type":"普通订单",
			"order_status":"待支付"
		}
		"""	

@mall @mall.webapp.test.buy @mall.webapp.test.not_test_buy @pyliu
Scenario: 没有测试权限的会员购买商品
	bill购买'商品1'后
	1. 购买商品时看不到'测试购买'，商品价格不变
	2. jobs后台生成普通订单

	When jobs给会员bill"不分配"测试权限	
	Then bill获取测试权限
		"""
		{
			"test_whether_permission": "否"
		}
		"""
	When bill访问jobs的webapp
	When bill'测试购买'jobs的'商品1'
	Then jobs生成普通订单
		"""
		{
			"name": "商品1",
			"price":"100.0",
			"order_type":"普通订单",
			"order_status":"待支付"
		}
		"""	
	When bill'购买'jobs的'商品1'
	Then jobs生成普通订单
		"""
		{
			"name": "商品1",
			"price":"100.0",
			"order_type":"普通订单",
			"order_status":"待支付"
		}
		"""	

@mall @mall.webapp.test.buy @mall.webapp.test.not_member_test_buy @pyliu
Scenario: 非会员购买商品
	非会员nokia购买'商品1'后
	1. nokia购买商品时看不到'测试购买'，商品价格不变
	2. job后台生成普通订单

	When nokia'测试购买'jobs的'商品1'
	Then jobs生成普通订单
		"""
		{
			"name": "商品1",
			"price":"100.0",
			"order_type":"普通订单",
			"order_status":"待支付"
		}
		"""	
	When nokia'购买'jobs的'商品1'
	Then jobs生成普通订单
		"""
		{
			"name": "商品1",
			"price":"100.0",
			"order_type":"普通订单",
			"order_status":"待支付"
		}
		"""	

