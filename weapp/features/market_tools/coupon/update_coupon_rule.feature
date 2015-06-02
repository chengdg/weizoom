# __author__ : "崔帅帅"
Feature: 更新优惠券规则
	Jobs能通过管理系统更新"优惠券规则"


@market_tool.coupon @market_tool
Scenario: 更新优惠券规则
	jobs添加"优惠券规则"后
	1. jobs能更改优惠券的规则名

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
	When jobs更新优惠券规则'优惠券1'为
		'''
		{
			"name": "优惠券1*"
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
			"name": "优惠券1*",
			"money": 1,
			"expire_days": 1,
			"using_limit": "无限制"
		}]
		'''
