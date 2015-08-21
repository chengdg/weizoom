# __author__ : "崔帅帅"
@func:webapp.modules.user_center.views.list_grades
Feature: 增加会员等级
	Jobs能添加会员等级

@crm @member @member.grade @member.add_grade
Scenario: 添加会员等级
	Jobs添加多组"会员等级"后，"会员等级列表"会按照添加的顺序正序排列

	Given jobs登录系统
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "不自动升级",
			"shop_discount": "100%"
		}]
		"""

	When jobs添加会员等级
		"""
		[{
			"name": "银牌会员",
			"upgrade": "不自动升级",
			"shop_discount": "100%"
		},
		{
			"name": "金牌会员",
			"upgrade":"自动升级",
			"shop_discount": "98%"
		}]
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "不自动升级",
			"shop_discount": "100%"
		},{
			"name": "银牌会员",
			"upgrade": "不自动升级",
			"shop_discount": "100%"
		},
		{
			"name": "金牌会员",
			"upgrade": "自动升级",
			"shop_discount": "98%"
		}]
		"""

