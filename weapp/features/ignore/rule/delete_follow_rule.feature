# __author__ : "崔帅帅"
@func:weixin.message.qa.views.edit_follow_rule
Feature: 删除'Follow Rule'
	Jobs能通过管理系统删除"关注自动回复规则"

@weixin.message.qa
Scenario: 删除"关注自动回复规则"
	Jobs更新"关注自动回复规则"的内容为空后，等同于删除"关注自动回复规则"
	
	Given jobs登录系统
	When jobs添加关注自动回复规则
		"""
		{
			"answer": "follow answer"
		}	
		"""
	And bill关注jobs的公众号
	Then bill收到自动回复'follow answer'
	Given jobs登录系统
	When jobs更新关注自动回复规则为
		"""
		{
			"answer": ""
		}	
		"""
	Then jobs能获取关注自动回复规则
		"""
		{
			"type": "text",
			"answer": ""
		}
		"""
	And bill能获取关注自动回复规则
		"""
		{
			"type": "text",
			"answer": ""
		}
		"""
	When bill关注jobs的公众号
	Then bill收到自动回复'None'