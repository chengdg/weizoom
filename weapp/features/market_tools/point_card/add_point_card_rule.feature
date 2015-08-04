# __author__ : "崔帅帅"
Feature: 添加积分卡规则
	Jobs能通过管理系统添加"积分卡规则"


@weapp.market_tools.point_card
Scenario: 添加积分卡规则
	jobs添加多个"积分卡规则"后
	1. jobs能获得添加的积分卡规则
	2. 积分卡规则列表按添加的顺序倒序排列
	3. bill不能获得jobs添加的积分卡规则

	Given jobs登录系统
	When jobs添加积分卡规则
		"""
		[{
			"name": "积分卡规则1",
			"prefix": "0123456",
			"point": "100"
		}, {
			"name": "积分卡规则2",
			"prefix": "6543210",
			"point": "200"
		}]
		"""
	Then jobs能获得积分卡规则'积分卡规则1'
		'''
		{
			"name": "积分卡规则1",
			"prefix": "0123456",
			"point": "100"
		}
		'''
	Then jobs能获得积分卡规则'积分卡规则2'
		'''
		{
			"name": "积分卡规则2",
			"prefix": "6543210",
			"point": "200"
		}
		'''
	Then jobs能获得积分卡规则列表
		'''
		[{
			"name": "积分卡规则2"
		}, {
			"name": "积分卡规则1"
		}]
		'''
	Given bill登录系统
	Then bill能获得积分卡规则列表
		'''
		[]
		'''
		'''
