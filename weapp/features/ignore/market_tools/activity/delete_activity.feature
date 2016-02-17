#watcher:fengxuejing@weizoom.com,benchi@weizoom.com

@func:market_tools.tools.activity.views.list_activities
Feature: Delete Activity
	Jobs能通过管理系统删除"活动报名"
	
Background:
	Given jobs登录系统
	And jobs已添加'活动报名'
		"""
		[{
			"name": "活动1"
		}, {
			"name": "活动2"
		}, {
			"name": "活动3"
		}]
		"""

@weapp.market_tools.activity
Scenario: 删除活动报名
	Jobs删除"活动报名"后，能获取他参加的活动，"活动报名"列表会按照添加的倒序排列

	Given jobs登录系统
	Then jobs能获取活动列表
		"""
		[{
			"name": "活动3"
		}, {
			"name": "活动2"
		}, {
			"name": "活动1"
		}]
		"""
	When jobs删除活动报名'活动1'
	Then jobs能获取活动列表
		"""
		[{
			"name": "活动3"
		}, {
			"name": "活动2"
		}]
		"""
	When jobs删除活动报名'活动2'
	Then jobs能获取活动列表
		"""
		[{
			"name": "活动3"
		}]
		"""
	When jobs删除活动报名'活动3'
	Then jobs能获取活动列表
		"""
		[]
		"""
		
		
