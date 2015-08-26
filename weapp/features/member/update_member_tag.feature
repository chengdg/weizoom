# __author__ : "崔帅帅"
@func:webapp.modules.user_center.views.list_tags
Feature: 更新会员分组
	Jobs能更新会员分组

Background:
	Given jobs登录系统
	When jobs添加会员分组
		"""
		[{
			"name": "分组1"
		}, {
			"name": "分组2"
		}, {
			"name": "分组3"
		}]	
		"""

@crm @member @member.tag @member.update_tag
Scenario: Jobs更新已存在的会员分组
	When jobs更新会员分组'分组1'
		"""
		{
			"name": "分组1*"
		}	
		"""
	Then jobs能获取会员分组列表
		"""
		[{
			"name": "分组1*"
		},{
			"name": "分组2"
		},{
			"name": "分组3"
		}]
		"""


