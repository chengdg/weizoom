# __author__ : "冯雪静"
Feature: 删除会员等级
	Jobs能删除会员管理中的会员等级

Background:
	Given jobs登录系统
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"shop_discount": "100%"
		}]
		"""
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"shop_discount": "90%"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"shop_discount": "80%"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "70%"
		}]
		"""


Scenario: 1 删除已存在的手动升级的会员等级
	jobs能删除已存在的会员等级

	Given jobs登录系统
	When jobs删除会员等级'银牌会员'
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "手动升级",
			"shop_discount": "100%"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"shop_discount": "90%"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "70%"
		}]
		"""



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
			"shop_discount": "100%"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"shop_discount": "90%"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"shop_discount": "80%"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "70%"
		}]
		"""
	When jobs添加会员等级
		"""
		[{
			"name": "蓝钻会员",
			"upgrade": "自动升级",
			"deal_price": 1000.00,
			"buy_counts": 20,
			"empirical_value": 10000,
			"shop_discount": "60%"
		}, {
			"name": "红钻会员",
			"upgrade": "自动升级",
			"deal_price": 5000.00,
			"buy_counts": 50,
			"empirical_value": 50000,
			"shop_discount": "40%"
		}]
		"""
	When jobs删除会员等级'蓝钻会员'
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"shop_discount": "100%"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"shop_discount": "90%"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"shop_discount": "80%"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "70%"
		}, {
			"name": "红钻会员",
			"upgrade": "自动升级",
			"deal_price": 5000.00,
			"buy_counts": 50,
			"empirical_value": 50000,
			"shop_discount": "40%"
		}]
		"""
