# __author__ : "崔帅帅"
Feature: 自动生成积分卡
	Jobs能通过管理系统为一个"积分卡规则"手工生成"积分卡"

Background:
	Given jobs登录系统
	And jobs添加积分卡规则
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

@weapp.market_tools.point_card
Scenario: 生成多个积分卡

	When jobs手工为积分卡规则生成积分卡
		"""
		{
			"point_card_rule": "积分卡规则1",
			"count": 2,
			"point_card_ids": ["01234560001", "01234560002"]
		}
		"""
	Then jobs能获得积分卡列表
		"""
		[{
			"point_card_rule_name": "积分卡规则1",
			"point": "100",
			"status": "未使用"
		}, {
			"point_card_rule_name": "积分卡规则1",
			"point": "100",
			"status": "未使用"
		}]
		"""