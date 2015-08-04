# __author__ : "冯雪静"
Feature: 更新会员等级
	Jobs能管理会员管理中的会员等级列表

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


Scenario: 1 更新已存在的会员等级
	jobs添加会员等级后，可以更新等级

	Given jobs登录系统
	When jobs更新会员等级'金牌会员'
		"""
		{
			"name": "钻石会员",
			"upgrade": "手动升级",
			"shop_discount": "70%"
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
			"name": "钻石会员",
			"upgrade": "手动升级",
			"shop_discount": "70%"
		}]
		"""


Scenario: 2 更新手动升级会员等级为自动升级会员等级
	jobs添加手动升级的会员等级后，可以更新为自动升级的会员等级

	Given jobs登录系统
	When jobs开启自动升级
		"""
		{
			"upgrade": "自动升级",
			"condition": ["满足一个条件即可"]
		}
		"""
	When jobs更新会员等级'铜牌会员'
		"""
		{
			"name": "铜牌会员",
			"upgrade": "自动升级",
			"deal_price": 1000.00,
			"buy_counts": 20,
			"empirical_value": 10000,
			"shop_discount": "90%"
		}
		"""
	And jobs更新会员等级'银牌会员'
		"""
		{
			"name": "银牌会员",
			"upgrade": "自动升级",
			"deal_price": 3000.00,
			"buy_counts": 30,
			"empirical_value": 30000,
			"shop_discount": "80%"
		}
		"""
	And jobs更新会员等级'金牌会员'
		"""
		{
			"name": "金牌会员",
			"upgrade": "自动升级",
			"deal_price": 5000.00,
			"buy_counts": 50,
			"empirical_value": 50000,
			"shop_discount": "70%"
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
			"upgrade": "自动升级",
			"deal_price": 1000.00,
			"buy_counts": 20,
			"empirical_value": 10000,
			"shop_discount": "90%"
		}, {
			"name": "银牌会员",
			"upgrade": "自动升级",
			"deal_price": 3000.00,
			"buy_counts": 30,
			"empirical_value": 30000,
			"shop_discount": "80%"
		}, {
			"name": "金牌会员",
			"upgrade": "自动升级",
			"deal_price": 5000.00,
			"buy_counts": 50,
			"empirical_value": 50000,
			"shop_discount": "70%"
		}]
		"""


Scenario: 3 更新自动升级会员等级为手动升级会员等级
	jobs添加自动升级的会员等级后，可以更新为自动升级的会员等级

	Given jobs登录系统
	When jobs开启自动升级
		"""
		{
			"upgrade": "自动升级",
			"condition": ["满足所有条件"]
		}
		"""
	When jobs添加会员等级
		"""
		[{
			"name": "蓝钻会员",
			"upgrade": "自动升级",
			"deal_price": 1000.00,
			"buy_counts": 20,
			"empirical_value": 10000,
			"shop_discount": "90%"
		}, {
			"name": "黄钻会员",
			"upgrade": "自动升级",
			"deal_price": 3000.00,
			"buy_counts": 30,
			"empirical_value": 30000,
			"shop_discount": "80%"
		}, {
			"name": "红钻会员",
			"upgrade": "自动升级",
			"deal_price": 5000.00,
			"buy_counts": 50,
			"empirical_value": 50000,
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
			"name": "蓝钻会员",
			"upgrade": "自动升级",
			"deal_price": 1000.00,
			"buy_counts": 20,
			"empirical_value": 10000,
			"shop_discount": "90%"
		}, {
			"name": "黄钻会员",
			"upgrade": "自动升级",
			"deal_price": 3000.00,
			"buy_counts": 30,
			"empirical_value": 30000,
			"shop_discount": "80%"
		}, {
			"name": "红钻会员",
			"upgrade": "自动升级",
			"deal_price": 5000.00,
			"buy_counts": 50,
			"empirical_value": 50000,
			"shop_discount": "70%"
		}]
		"""
	When jobs更新会员等级'红钻会员'
		"""
		{
			"name": "红钻会员",
			"upgrade": "手动升级",
			"shop_discount": "70%"
		}
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"shop_discount": "100%"
		}, {
			"name": "蓝钻会员",
			"upgrade": "自动升级",
			"deal_price": 1000.00,
			"buy_counts": 20,
			"empirical_value": 10000,
			"shop_discount": "90%"
		}, {
			"name": "黄钻会员",
			"upgrade": "自动升级",
			"deal_price": 3000.00,
			"buy_counts": 30,
			"empirical_value": 30000,
			"shop_discount": "80%"
		}, {
			"name": "红钻会员",
			"upgrade": "手动升级",
			"shop_discount": "70%"
		}]
		"""