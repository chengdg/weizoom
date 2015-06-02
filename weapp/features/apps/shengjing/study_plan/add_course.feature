@func:
Feature: 添加盛景课程
	Jobs能通过管理系统添加"课程"

@weapp.apps.shengjing @weapp.apps.shengjing.add_course @ignore
Scenario: 添加盛景课程
	Jobs添加"添加盛景课程"后，能获取他添加的课程，"盛景课程"列表会按照排列的顺序的排列

	Given jobs登录系统
	When jobs添加盛景课程
		""" 
		[{
			"course_id_name": "1_盛景课程",
			"coure_date": "2014-06-16~2014-07-08",
			"detail": "<p>343434<br/></p>"
		}]
		"""
	Then jobs能获取盛景课程列表
		"""
		[{
			"name": "盛景课程"
		}]
		"""
	And bill能获取能获取盛景课程列表
		"""
		[]
		"""
		
		
