# __author__ : "崔帅帅"
@func:weixin.message.qa.views.edit_unmatch_rule
Feature: 添加'Unmatch Rule'
	Jobs能通过管理系统添加"自动回复规则"


@weixin.message.qa
Scenario: 获得初始的"自动回复规则"
	Jobs登陆后
	1. 能获得空的自动回复规则
	3. bill在微信中关注jobs的公众账号后，无回复
	
	Given jobs登录系统
	Then jobs能获取自动回复规则
		"""
		{
			"type": "text",
			"active_type": "全天启用",
			"answer": ""
		}
		"""
	When bill在微信中向jobs的公众号发送消息'unknown'
	Then bill收到自动回复'None'


@weixin.message.qa
Scenario: 添加"自动回复规则"
	Jobs添加"自动回复规则"后
	1. jobs能获取他添加的规则
	3. bill在微信中发送'unknown'后能收到回复
	
	Given jobs登录系统
	When jobs添加自动回复规则
		"""
		{
			"active_type": "全天启用",
			"answer": "unmatch answer"
		}	
		"""
	Then jobs能获取自动回复规则
		"""
		{
			"type": "text",
			"active_type": "全天启用",
			"answer": "unmatch answer"
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
	Then bill收到自动回复'unmatch answer'