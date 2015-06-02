# __author__ : "崔帅帅"
@func:weixin.message.qa.views.edit_follow_rule
Feature: 删除'Unmatch Rule'
	Jobs能通过管理系统删除"自动回复规则"

@weixin.message.qa
Scenario: 删除"自动回复规则"
	Jobs更新"自动回复规则"的内容为空后，等同于删除"自动回复规则"
	
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
			"active_type": "全天启用",
			"answer": ""
		}	
		"""
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