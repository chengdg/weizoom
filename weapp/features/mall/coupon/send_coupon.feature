# __author__ : "崔帅帅"
Feature: 发放优惠券
	Jobs能通过管理系统将生成的"优惠券"发放给会员

Background:
	Given jobs登录系统
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "优惠券规则1",
			"money": 1,
			"expire_days": 1,
			"using_limit": "无限制"
		}, {
			"name": "优惠券规则2",
			"money": 2,
			"expire_days": 2,
			"using_limit": "满10元可以使用"
		}]
		"""
	Given nokia登录系统
	And nokia已添加了优惠券规则
		"""
		[{
			"name": "优惠券规则1",
			"money": 1,
			"expire_days": 1,
			"using_limit": "无限制"
		}, {
			"name": "优惠券规则2",
			"money": 2,
			"expire_days": 2,
			"using_limit": "满10元可以使用"
		}]
		"""
	Given bill关注jobs的公众号
	And bill关注nokia的公众号
	And tom关注jobs的公众号
	And tom关注nokia的公众号


@market_tool.coupon @market_tool 
Scenario: 发送优惠券给一个会员
	jobs添加"优惠券规则"后，将优惠券发放给一个会员(bill)
	1. bill访问jobs的webapp时能看到获得的优惠券
	2. bill访问nokia的webapp时不能看到获得的优惠券
	3. tom访问jobs的webapp不能看到bill获得的优惠券
	3. jobs能获得包含发放的的优惠券的优惠券列表
	4. nokia的优惠券列表不受影响

	Given jobs登录系统
	When jobs为会员发放优惠券
		'''
		{
			"coupon_rule": "优惠券规则1",
			"count": 2,
			"members": ["bill"],
			"coupon_ids": ["coupon_1", "coupon_2"]
		}
		'''
	Then jobs能获得优惠券列表
		'''
		[{
			"coupon_rule": "优惠券规则1",
			"money": 1.00,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "bill"
		}, {
			"coupon_rule": "优惠券规则1",
			"money": 1.00,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "bill"
		}]
		'''
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		'''
		[{
			"coupon_id": "coupon_1",
			"money": 1.00,
			"status": "未使用"
		}, {
			"coupon_id": "coupon_2",
			"money": 1.00,
			"status": "未使用"
		}]
		'''
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		'''
		[]
		'''
	Given nokia登录系统
	Then nokia能获得优惠券列表
		'''
		[]
		'''
	When bill访问nokia的webapp
	Then bill能获得webapp优惠券列表
		'''
		[]
		'''