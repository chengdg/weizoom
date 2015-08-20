# __author__ : "崔帅帅"
@func:webapp.modules.user_center.views.list_tags
Feature: 增加会员分组
	Jobs能添加会员分组

@crm @member @member.tag @member.add_tag
Scenario: 添加会员分组
	Jobs添加多组"会员分组"后，"会员分组列表"会按照添加的顺序正序排列

	Given jobs登录系统
	
	When jobs添加会员分组
		"""
		[{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2",
			"tag_id_3": "分组3"
		}]	
		"""
	When bill关注jobs的公众号
	When bill1关注jobs的公众号
	When bill2关注jobs的公众号
	When bill3关注jobs的公众号
	When bill4关注jobs的公众号
	When bill5关注jobs的公众号

	When jobs选择会员
		| name  |  grade |
		| bill  |        |
		| bill1 |        |
		| bill2 |        |
		| bill3 |        |
		| bill4 |        |
		| bill5 |        |

	When jobs批量添加分组
		"""
		[{
			"modification_method":"给选中的人添加分组",
			"grouping":"分组1"
		}]
		"""
	When jobs选择会员
		| name  |  grade |
		| bill1 | 分组1  |
		| bill3 | 分组1  |
		| bill5 | 分组1  |

	When jobs批量添加分组
		"""
		[{
			"modification_method":"给选中的人添加分组",
			"grouping":"分组3"
		}]
		"""

	Then jobs能获取会员分组列表
		"""
		[{
			"name": "分组1",
			"group_membership":6
		}, {
			"name": "分组2",
			"group_membership":0
		}, {
			"name": "分组3",
			"group_membership":3
		}]
		"""
	Given bill登录系统
	Then bill能获取会员分组列表
		"""
		[]
		"""


