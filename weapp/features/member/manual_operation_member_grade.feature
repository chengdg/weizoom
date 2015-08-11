# __author__ : "冯雪静"
Feature: 手动调整会员等级
	Jobs能管理会员管理中的会员等级


Background:
	Given jobs登录系统
	When jobs开启自动升级
		"""
		{
			"upgrade": "自动升级",
			"condition": ["满足一个条件即可"]
		}
		"""
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 20,
			"upgrade_lower_bound": 10000,
			"shop_discount": "90%"
		}, {
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"upgrade_lower_bound": 30000,
			"shop_discount": "80%"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "70%"
		}]
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"shop_discount": "100%"
		}, {
			"name": "铜牌会员",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 20,
			"upgrade_lower_bound": 10000,
			"shop_discount": "90%"
		}, {
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"upgrade_lower_bound": 30000,
			"shop_discount": "80%"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "70%"
		}]
		"""
	When bill关注jobs的公众号
	When tom关注jobs的公众号
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "铜牌会员",
			"pay_money": 0.00,
			"pay_times": 0,
			"upgrade_lower_bound": 10000
		}, {
			"name": "bill",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"pay_times": 0,
			"upgrade_lower_bound": 1000
		}]
		"""


Scenario: 1 手动把会员调到自动升级的会员等级里面
	jobs手动调整已有会员的会员等级
	1. jobs能获取会员列表
	2. jobs删除会员等级后，里面的会员，回到相应的等级里面


	Given jobs登录系统
	When jobs更新"bill"的会员等级
		"""
		{
			"name": "bill",
			"member_rank": "银牌会员"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "铜牌会员",
			"pay_money": 0.00,
			"pay_times": 0,
			"upgrade_lower_bound": 10000
		}, {
			"name": "bill",
			"member_rank": "银牌会员",
			"pay_money": 0.00,
			"pay_times": 0,
			"upgrade_lower_bound": 1000
		}]
		"""
	When jobs删除会员等级'银牌会员'
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"shop_discount": "100%"
		}, {
			"name": "铜牌会员",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 20,
			"upgrade_lower_bound": 10000,
			"shop_discount": "90%"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "70%"
		}]
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "铜牌会员",
			"pay_money": 0.00,
			"pay_times": 0,
			"upgrade_lower_bound": 10000
		}, {
			"name": "bill",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"pay_times": 0,
			"upgrade_lower_bound": 1000
		}]
		"""
	When jobs更新"tom"的会员等级
		"""
		{
			"name": "tom",
			"member_rank": "金牌会员"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "金牌会员",
			"pay_money": 0.00,
			"pay_times": 0,
			"upgrade_lower_bound": 10000
		}, {
			"name": "bill",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"pay_times": 0,
			"upgrade_lower_bound": 1000
		}]
		"""
	When jobs删除会员等级'金牌会员'
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"shop_discount": "100%"
		}, {
			"name": "铜牌会员",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 20,
			"upgrade_lower_bound": 10000,
			"shop_discount": "90%"
		}]
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "铜牌会员",
			"pay_money": 0.00,
			"pay_times": 0,
			"upgrade_lower_bound": 10000
		}, {
			"name": "bill",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"pay_times": 0,
			"upgrade_lower_bound": 1000
		}]
		"""