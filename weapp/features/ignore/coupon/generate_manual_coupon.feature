# __author__ : "崔帅帅"
Feature: 手工生成优惠券
	Jobs能通过管理系统为一个"优惠券规则"手工生成"优惠券"

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
	Given bill登录系统
	And bill已添加了优惠券规则
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


@market_tool.coupon @market_tool
Scenario: 生成多次优惠券
	jobs添加"优惠券规则"后，可以为该规则手工生成优惠券，生成后
	1. jobs能获得生成的优惠券
	2. jobs能多次生成优惠券
	3. jobs能为不同的优惠券规则生成优惠券

	Given jobs登录系统
	When jobs手工为优惠券规则生成优惠券
		"""
		{
			"coupon_rule": "优惠券规则1",
			"count": 2,
			"coupon_ids": ["coupon_1", "coupon_2"]
		}
		"""
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "优惠券规则1",
			"coupon_id": "coupon_2",
			"money": 1.00,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "手工"
		}, {
			"coupon_rule": "优惠券规则1",
			"coupon_id": "coupon_1",
			"money": 1.00,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "手工"
		}]
		"""
	When jobs手工为优惠券规则生成优惠券
		"""
		{
			"coupon_rule": "优惠券规则1",
			"count": 1,
			"coupon_ids": ["coupon_3"]
		}
		"""
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "优惠券规则1",
			"coupon_id": "coupon_3",
			"money": 1.00,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "手工"
		}, {
			"coupon_rule": "优惠券规则1",
			"coupon_id": "coupon_2",
			"money": 1.00,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "手工"
		}, {
			"coupon_rule": "优惠券规则1",
			"coupon_id": "coupon_1",
			"money": 1.00,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "手工"
		}]
		"""
	When jobs手工为优惠券规则生成优惠券
		"""
		{
			"coupon_rule": "优惠券规则2",
			"count": 1,
			"coupon_ids": ["coupon_4"]
		}
		"""
	Then jobs能获得优惠券列表
		"""
		[{
			"coupon_rule": "优惠券规则2",
			"coupon_id": "coupon_4",
			"money": 2.00,
			"create_date": "今天",
			"expire_date": "后天",
			"status": "未使用",
			"target": "手工"
		}, {
			"coupon_rule": "优惠券规则1",
			"coupon_id": "coupon_3",
			"money": 1.00,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "手工"
		}, {
			"coupon_rule": "优惠券规则1",
			"coupon_id": "coupon_2",
			"money": 1.00,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "手工"
		}, {
			"coupon_rule": "优惠券规则1",
			"coupon_id": "coupon_1",
			"money": 1.00,
			"create_date": "今天",
			"expire_date": "明天",
			"status": "未使用",
			"target": "手工"
		}]
		"""
	Given bill登录系统
	Then bill能获得优惠券列表
		"""
		[]
		"""