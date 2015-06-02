# __author__ : "崔帅帅"
Feature: 删除优惠券规则
	Jobs能通过管理系统删除"优惠券规则"

Background:
	Given jobs登录系统
	And jobs已添加了优惠券规则
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
	Given bill登录系统
	And bill已添加了优惠券规则
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


@market_tool.coupon @market_tool
Scenario: 无优惠券时，可以删除优惠券规则
	jobs添加"优惠券规则"后
	1. 如果没有优惠券与之关联，则jobs能删除该优惠券
	2. jobs的删除操作不影响其他用户的优惠券规则


	Given jobs登录系统
	Then jobs能获得优惠券规则'优惠券1'
		'''
		{
			"name": "优惠券1"
		}
		'''
	When jobs删除优惠券规则'优惠券1'
	Then jobs能获得优惠券规则列表
		'''
		[{
			"name": "优惠券2",
			"money": 2,
			"expire_days": 2,
			"using_limit": "满10元可以使用"
		}]
		'''
	Given bill登录系统
	Then bill能获得优惠券规则列表
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


@market_tool.coupon @market_tool
Scenario: 已有优惠券时，不可删除优惠券规则
	jobs添加"优惠券规则"后
	1. 如果有优惠券与之关联，则jobs不能删除该优惠券
	2. jobs的删除操作不影响其他用户的优惠券规则


	Given jobs登录系统
	When jobs手工为优惠券规则生成优惠券
		'''
		{
			"coupon_rule": "优惠券1",
			"count": 2
		}
		'''
	Then jobs能获得优惠券规则'优惠券1'
		'''
		{
			"name": "优惠券1"
		}
		'''
