@func:
Feature: 编辑盛景课程
	Jobs能通过管理系统更新"盛景课程"

Background:
	Given jobs登录系统
	And jobs已添加'盛景课程'
		"""
		[{
			"name": "课程1",
			"start_date": "2014-01-01",
			"end_date": "2014-10-10",
			"description": '11111'
		}]
		"""

@weapp.apps.shengjing @weapp.apps.shengjing.edit_course @ignore
Scenario: 更新"盛景课程"
	Jobs更新"盛景课程"后，能获取更新的课程，并且更改后列表排序不变

	Given jobs登录系统
	When jobs更新盛景课程'课程1'
		"""
		{
			"name": "课程1",
			"start_date": "2014-01-01",
			"end_date": "2014-10-10",
			"description": "22222"
		}
		"""
	
	Then jobs能获取盛景课程'课程1'
		"""
		{
			"name": "课程1",
			"start_date": "2014-01-01",
			"end_date": "2014-10-10",
			"description": "22222"
		}
		"""
	And jobs能获取盛景课程列表
		"""
		[{
			"name": "课程1"
		}]
		"""
	And bill能获取盛景列表
		"""
		[]
		"""


