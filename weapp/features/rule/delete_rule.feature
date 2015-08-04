# __author__ : "崔帅帅"
@func:weixin.message.qa.views.list_rules
Feature: Delete Rule
	Jobs能通过管理系统删除Rule

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
Scenario: 删除"关键词自动回复规则"
	Jobs添加一组规则后
	1. 能删除单个规则
	2. 更改后规则列表排序不变
	3. 模拟器上输入keyword后自动回复发生变化

	When jobs在模拟器中发送消息'keyword2'
	Then jobs收到自动回复'answer2'
	When jobs删除关键词自动回复规则'keyword2'
	Then jobs能获取关键词自动回复规则列表
		"""
		[{
			"patterns": "keyword3",
			"answer": "answer3"
		}, {
			"patterns": "keyword1",
			"answer": "answer1"
		}]
		"""
	#更新后影响自动回复
	When jobs在模拟器中发送消息'keyword2'
	Then jobs收到自动回复'None'
	When jobs在模拟器中发送消息'keyword3'
	Then jobs收到自动回复'answer3'
	When jobs在模拟器中发送消息'keyword1'
	Then jobs收到自动回复'answer1'
