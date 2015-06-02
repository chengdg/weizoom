# __author__ : "崔帅帅"
Feature: 添加优惠券规则
	Jobs能通过管理系统添加"优惠券规则"


@market_tool.coupon @market_tool
Scenario: 添加优惠券规则
	jobs添加多个"优惠券规则"后
	1. jobs能获得添加的优惠券规则
	2. 优惠券规则列表按添加的顺序倒序排列
	3. bill不能获得jobs添加的优惠券规则

	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 1,
			"expire_days": 1,
			"using_limit": "无限制"
		}, {
			"name": "优惠券2",
			"money": 2,
			"expire_days": 2,
			"using_limit": "满10元可以使用"
		}]
		"""
	Then jobs能获得优惠券规则'优惠券1'
		'''
		{
			"name": "优惠券1",
			"money": 1,
			"expire_days": 1,
			"using_limit": "无限制"
		}
		'''
	Then jobs能获得优惠券规则'优惠券2'
		'''
		{
			"name": "优惠券2",
			"money": 2,
			"expire_days": 2,
			"using_limit": "满10元可以使用"
		}
		'''
	Then jobs能获得优惠券规则列表
		'''
		[{
			"name": "优惠券2",
			"money": 2,
			"expire_days": 2,
			"using_limit": "满10元可以使用"
		}, {
			"name": "优惠券1",
			"money": 1,
			"expire_days": 1,
			"using_limit": "无限制"
		}]
		'''
	Given bill登录系统
	Then bill能获得优惠券规则列表
		'''
		[]
		'''