# __author__ : "崔帅帅"
@func:weixin.message.qa.views.add_rule
Feature: Update Rule
	Jobs能通过管理系统更新Rule

Background:
	Given jobs登录系统
	And jobs已添加关键词自动回复规则
		"""
		[{
			"patterns": "keyword1",
			"answer": "answer1"
		}, {
			"patterns": "keyword2",
			"answer": "answer2"
		}, {
			"patterns": "keyword3",
			"answer": "answer3"
		}]	
		"""

@weixin.message.qa
Scenario: 更新"关键词自动回复规则"
	Jobs添加一组规则后
	1. 能更改单个规则的所有字段的属性
	2. 更改后规则列表排序不变
	3. 模拟器上输入keyword后自动回复发生变化

	When jobs更新关键词自动回复规则'keyword2'
		"""
		{
			"patterns": "keyword2*",
			"answer": "answer2*"
		}	
		"""	
	Then jobs无法获取关键词自动回复规则'keyword2'
	And jobs能获取关键词自动回复规则'keyword2*'
		"""
		{
			"type": "text",
			"patterns": "keyword2*",
			"answer": "answer2*"
		}
		"""
	And jobs能获取关键词自动回复规则列表
		"""
		[{
			"patterns": "keyword3",
			"answer": "answer3"
		}, {
			"patterns": "keyword2*",
			"answer": "answer2*"
		}, {
			"patterns": "keyword1",
			"answer": "answer1"
		}]
		"""

	#更新后影响自动回复
	When jobs在模拟器中发送消息'keyword2'
	Then jobs收到自动回复'None'
	When jobs在模拟器中发送消息'keyword2*'
	Then jobs收到自动回复'answer2*'
	When jobs在模拟器中发送消息'keyword1'
	Then jobs收到自动回复'answer1'
