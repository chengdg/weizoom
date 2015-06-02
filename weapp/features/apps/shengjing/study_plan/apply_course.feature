@func:
Feature: 盛景课程报名
	微信用户能通过系统进行课程报名

	
Background:
	Given jobs登录系统
	And jobs已添加课程
		""" 
		[{
			"name": "课程1",
			"start_date": "2014-01-01",
			"end_date": "2014-10-10"
		}]
		"""
	And bill关注jobs的公众号
 
@shengjing.apply_course @ignore
Scenario: 会员课程报名
	Jobs添加"课程"后，会员可进行报名

	Given jobs登录系统
	When bill报名课程'课程1'
	Then bill再次进入'课程1'
		"""
			[{
				"status": "己报名"
			}]
		"""
	
	
