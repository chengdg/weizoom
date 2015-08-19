# __author__ : "崔帅帅"
@func:weixin.message.qa.views.edit_unmatch_rule
Feature: 更新Unmatch Rule
	Jobs能通过管理系统管理"自动回复规则"

@weixin.message.qa
Scenario: 更新"自动回复规则"
	Jobs更新"自动回复规则"后
	1. jobs能获取他更新后的规则
	3. bill在微信中能收到更新后的回复
	
	Given jobs登录系统
	When jobs添加自动回复规则
		"""
		{
			"active_type": "全天启用",
			"answer": "unmatch answer"
		}	
		"""
	And bill在微信中向jobs的公众号发送消息'unknown'
	Then bill收到自动回复'unmatch answer'
	Given jobs登录系统
	When jobs更新自动回复规则为
		"""
		{
			"active_type": "定时启用",
			"start_hour": 0,
			"end_hour": 24,
			"answer": "unmatch answer*"
		}	
		"""
	Then jobs能获取自动回复规则
		"""
		{
			"active_type": "定时启用",
			"start_hour": 0,
			"end_hour": 24,
			"answer": "unmatch answer*"
		}
		"""
	And bill能获取自动回复规则
		"""
		{
			"type": "text",
			"active_type": "全天启用",
			"answer": ""
		}
		"""
	When bill在微信中向jobs的公众号发送消息'unknown'
	Then bill收到自动回复'unmatch answer*'