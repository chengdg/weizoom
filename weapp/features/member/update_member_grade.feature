#author: 冯雪静
#editor: benchi 加标签
#editor: 张三香 2015.10.15

Feature: 更新会员等级
	Jobs能管理会员管理中的会员等级列表

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
Scenario:1 更新已存在的会员等级
	jobs添加会员等级后，可以更新等级

	Given jobs登录系统
	When jobs更新会员等级'金牌会员'
		"""
		{
			"name": "钻石会员",
			"upgrade": "手动升级",
			"discount": "7"
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
			"name": "钻石会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""

@mall2 @member @meberGrade
Scenario:2 更新手动升级会员等级为自动升级会员等级
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
			"pay_money": 1000.00,
			"pay_times": 20,
			"discount": "9"
		}
		"""
	And jobs更新会员等级'银牌会员'
		"""
		{
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"discount": "8"
		}
		"""
	And jobs更新会员等级'金牌会员'
		"""
		{
			"name": "金牌会员",
			"upgrade": "自动升级",
			"pay_money": 5000.00,
			"pay_times": 50,
			"discount": "7"
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
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 20,
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "自动升级",
			"pay_money": 5000.00,
			"pay_times": 50,
			"discount": "7"
		}]
		"""

@mall2 @member @meberGrade
Scenario:3 更新自动升级会员等级为手动升级会员等级
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
			"pay_money": 1000.00,
			"pay_times": 20,
			"discount": "6"
		}, {
			"name": "黄钻会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"discount": "5"
		}, {
			"name": "红钻会员",
			"upgrade": "自动升级",
			"pay_money": 5000.00,
			"pay_times": 50,
			"discount": "4"
		}]
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
		}, {
			"name": "蓝钻会员",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 20,
			"discount": "6"
		}, {
			"name": "黄钻会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"discount": "5"
		}, {
			"name": "红钻会员",
			"upgrade": "自动升级",
			"pay_money": 5000.00,
			"pay_times": 50,
			"discount": "4"
		}]
		"""
	When jobs更新会员等级'红钻会员'
		"""
		{
			"name": "红钻会员",
			"upgrade": "手动升级",
			"discount": "4"
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
		}, {
			"name": "蓝钻会员",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 20,
			"discount": "6"
		}, {
			"name": "黄钻会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"discount": "5"
		}, {
			"name": "红钻会员",
			"upgrade": "手动升级",
			"discount": "4"
		}]
		"""