# __author__ : "崔帅帅"
@func:weixin.message.qa.views.edit_follow_rule
Feature: 添加'Follow Rule'
	Jobs能通过管理系统添加"关注自动回复规则"


@weixin.message.qa
Scenario: 获得初始的"关注自动回复规则"
	Jobs登陆后
	1. 能获得空的关注自动回复规则
	3. bill在微信中关注jobs的公众账号后，无回复
	
	Given jobs登录系统
	Then jobs能获取关注自动回复规则
		"""
		{
			"type": "text",
			"answer": ""
		}
		"""
	When bill关注jobs的公众号
	Then bill收到自动回复'None'


@weixin.message.qa
Scenario: 添加"关注自动回复规则"
	Jobs添加"关注自动回复规则"后
	1. jobs能获取他添加的规则
	3. bill在微信中关注jobs的公众账号能收到回复
	
	Given jobs登录系统
	When jobs添加关注自动回复规则
		"""
		{
			"answer": "follow answer"
		}	
		"""
	And bill关注jobs的公众号
	Then bill收到自动回复'follow answer'
	And jobs能获取关注自动回复规则
		"""
		{
			"type": "text",
			"answer": "follow answer"
		}
		"""
	And bill能获取关注自动回复规则
		"""
		{
			"type": "text",
			"answer": ""
		}
		"""