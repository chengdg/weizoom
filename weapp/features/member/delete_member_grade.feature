# __author__ : "冯雪静"
# __edite__ : "benchi" 没有问题，添加标签
Feature: 删除会员等级
	Jobs能删除会员管理中的会员等级

Background:
	Given jobs登录系统
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"discount": "10"
		}]
		"""
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""

@mall2 @member @meberGrade
Scenario: 1 删除已存在的手动升级的会员等级
	jobs能删除已存在的会员等级

	Given jobs登录系统
	When jobs删除会员等级'银牌会员'
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"discount": "10"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""

@mall2 @member @meberGrade
Scenario: 2 删除已存在的自动升级的会员等级
	jobs能删除已存在的会员等级

	Given jobs登录系统
	When jobs开启自动升级
		"""
		{
			"upgrade": "自动升级",
			"condition": ["满足一个条件即可"]
		}
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"discount": "10"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	When jobs添加会员等级
		"""
		[{
			"name": "蓝钻会员",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 20,
			"upgrade_lower_bound": 10000,
			"discount": "6"
		}, {
			"name": "红钻会员",
			"upgrade": "自动升级",
			"pay_money": 5000.00,
			"pay_times": 50,
			"upgrade_lower_bound": 50000,
			"discount": "4"
		}]
		"""
	When jobs删除会员等级'蓝钻会员'
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"discount": "10"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}, {
			"name": "红钻会员",
			"upgrade": "自动升级",
			"pay_money": 5000.00,
			"pay_times": 50,
			"upgrade_lower_bound": 50000,
			"discount": "4"
		}]
		"""
