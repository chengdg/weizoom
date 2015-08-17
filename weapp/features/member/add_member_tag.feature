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
			"name": "分组1"
		}, {
			"name": "分组2"
		}, {
			"name": "分组3"
		}]	
		"""
	Then jobs能获取会员分组列表
		"""
		[{
			"name": "分组1"
		}, {
			"name": "分组2"
		}, {
			"name": "分组3"
		}]
		"""
	Given bill登录系统
	Then bill能获取会员分组列表
		"""
		[]
		"""