# __author__ : "崔帅帅"
@func:weixin.message.qa.views.edit_unmatch_rule
Feature: 更新Unmatch Rule的启用策略
	Jobs能通过管理系统管理"自动回复规则"的启用策略

@weixin.message.qa
Scenario Outline: 改变"自动回复规则"的启用策略
	Jobs改变"自动回复规则"的启用策略后，自动回复结果出现相应变化
	
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
	When jobs更新自动回复规则启用策略为'<active_type>'
	And bill在微信中向jobs的公众号发送消息'unknown'
	Then bill收到自动回复'<answer>'
	
	Examples: 
		| active_type     | answer         |
		| 禁用            | None           |
		| 现在-1小时后    | unmatch answer |
		| 1小时前-现在    | None           |
		| 现在-现在       | None           |
		| 1小时前-1小时后 | unmatch answer |
		| 2小时前-1小时前 | None           |
		| 1小时后-2小时后 | None           |


@weixin.message.qa
Scenario: 改变"自动回复规则"的启用策略: 从禁用到启用
	Jobs将"自动回复规则"的启用策略从禁用改为启用后，能收到自动回复结果
	
	Given jobs登录系统
	When jobs添加自动回复规则
		"""
		{
			"active_type": "禁用",
			"answer": "unmatch answer"
		}	
		"""
	And bill在微信中向jobs的公众号发送消息'unknown'
	Then bill收到自动回复'None'
	Given jobs登录系统
	When jobs更新自动回复规则启用策略为'全天启用'
	And bill在微信中向jobs的公众号发送消息'unknown'
	Then bill收到自动回复'unmatch answer'