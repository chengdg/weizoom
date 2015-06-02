# __author__ : "崔帅帅"
@func:webapp.modules.user_center.views.list_grades
Feature: 更新会员等级
	Jobs能管理会员中心的会员等级列表

Background:
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

@crm @member @member.grade @member.update_grade
Scenario: Jobs更新已存在的会员等级

	When jobs更新会员等级金牌会员
		"""
		[{
			"name": "金牌牌会员",
			"upgrade": "自动升级",
			"shop_discount": "50%"
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
		},{
			"name": "金牌牌会员",
			"upgrade": "自动升级",
			"shop_discount": "50%"
		}]
		"""


