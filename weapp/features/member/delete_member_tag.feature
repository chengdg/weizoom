# __author__ : "崔帅帅"
@func:webapp.modules.user_center.views.list_tags
Feature: 删除会员分组
	Jobs能删除会员分组

Background:
	Given jobs登录系统
	When jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2",
			"tag_id_3": "分组3"
		}	
		"""

@crm @member @member.tag @member.delete_tag
Scenario: Jobs删除已存在的会员分组
	When jobs删除会员分组'分组2'
	Then jobs能获取会员分组列表
		"""
		[{
			"name": "分组1"
		}, {
			"name": "分组3"
		}]
		"""


