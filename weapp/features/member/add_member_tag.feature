#author: 崔帅帅
#author: 王丽
#editor: 张三香 2015.10.15
@func:webapp.modules.user_center.views.list_tags

Feature: 增加会员分组
	Jobs能添加会员分组
	"""
		# __author__ : "王丽"
		2015-9新增需求
		1、会员分组默认有个分组："未分组"，不能修改（没有修改框）、不能删除（没有删除按钮）
		2、新增会员和调整没有分组的会员，默认进入"未分组"
	"""

@mall2 @member @meberGroup   @member.tag @member.add_tag
Scenario:1 添加会员分组
	Jobs添加多组"会员分组"后，"会员分组列表"会按照添加的顺序正序排列

	Given jobs登录系统
	When jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2",
			"tag_id_3": "分组3"
			}
		"""
	Then jobs能获取会员分组列表
		"""
		[{
			"name": "未分组",
			"group_membership":0
		},{
			"name": "分组1",
			"group_membership":0
		},{
			"name": "分组2",
			"group_membership":0
		},{
			"name": "分组3",
			"group_membership":0
		}]
		"""
	Given bill登录系统
	Then bill能获取会员分组列表
		"""
		[{
			"name": "未分组",
			"group_membership":0
		}]
		"""


