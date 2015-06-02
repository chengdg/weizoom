# __author__ : "崔帅帅"
@func:weixin.message.qa.views.edit_follow_rule
Feature: 更新Follow Rule
	Jobs能通过管理系统管理"关注自动回复规则"

@weixin.message.qa
Scenario: 更新"关注自动回复规则"
	Jobs更新"关注自动回复规则"后
	1. jobs能获取他更新后的规则
	3. bill在微信中关注jobs的公众账号能收到更新后的回复
	
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
			"answer": "follow answer*"
		}	
		"""
	Then jobs能获取关注自动回复规则
		"""
		{
			"type": "text",
			"answer": "follow answer*"
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
	Then bill收到自动回复'follow answer*'