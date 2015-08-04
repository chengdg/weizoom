# __author__ : "崔帅帅"
@func:webapp.modules.user_center.views.list_grades
Feature: 删除会员等级
	Jobs能删除会员中心的会员等级

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
			"name": "金牌会员",
			"upgrade":"自动升级",
			"shop_discount": "98%"
		},{
			"name": "银牌会员",
			"upgrade": "不自动升级",
			"shop_discount": "100%"
		}]
		"""

@crm @member @member.grade @member.delete_grade
Scenario: Jobs删除已存在的会员等级

	When jobs删除会员等级银牌会员
	"""
	[]
	"""

	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "不自动升级",
			"shop_discount": "100%"
		},{
			"name": "金牌会员",
			"upgrade":"自动升级",
			"shop_discount": "98%"
		}]
		"""


