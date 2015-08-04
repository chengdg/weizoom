@func:
Feature: 删除盛景课程
	Jobs能通过管理系统删除"盛景课程"

Background:
	Given jobs登录系统
	And jobs已添加'盛景课程'
		"""
		[{
			"name": "课程1",
			"start_date": "2014-01-01",
			"end_date": "2014-10-10",
			"description": '11111'
		},{
			"name": "课程2",
			"start_date": "2014-01-01",
			"end_date": "2014-10-10",
			"description": '2222'
		},{
			"name": "课程3",
			"start_date": "2014-01-01",
			"end_date": "2014-10-10",
			"description": '33333'
		}]
		"""

@weapp.apps.shengjing @weapp.apps.shengjing.edit_course @ignore
Scenario: 删除"盛景课程"
	Jobs删除"盛景课程"后，获取不到删除的课程，并且更改后列表排序不变

	Given jobs登录系统
	When jobs删除盛景课程'课程1'
	Then jobs能获取盛景课程列表
		"""
		[{
			"name": "课程3"
		},{
			"name": "课程2"
		}]
		"""
	When jobs删除盛景课程'课程2'
	Then jobs能获取盛景课程列表
		"""
		[{
			"name": "课程3"
		}]
		"""
	When jobs删除盛景课程'课程3'
	Then jobs能获取盛景课程列表
		"""
		[]
		"""

