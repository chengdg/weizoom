#author: 冯雪静
#editor: benchi 对ui验证的修复
#editor: 张三香 2015.10.15

Feature: 添加会员等级
	Jobs能添加会员等级

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

@mall2 @member @meberGrade
Scenario:1 添加手动升级的会员等级
	jobs添加多组手动升级的"会员等级"后，"会员等级列表"会按照添加的顺序正序排列

	Given jobs登录系统
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

@mall2 @member @meberGrade
Scenario:2 添加自动升级的会员等级
	jobs添加多组自动升级的"会员等级"后，"会员等级列表"会按照添加的顺序正序排列

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
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"discount": "10"
		},{
			"name": "铜牌会员",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 20,
			"discount": "9"
		},{
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"discount": "8"
		},{
			"name": "金牌会员",
			"upgrade": "自动升级",
			"pay_money": 5000.00,
			"pay_times": 50,
			"discount": "7"
		}]
		"""

@mall2 @member @meberGrade
Scenario:3 添加手动和自动升级的会员等级
	jobs添加多组手动升级和自动升级的"会员等级"后，"会员等级列表"会按照添加的顺序正序排列

	Given jobs登录系统
	When jobs开启自动升级
		"""
		{
			"upgrade": "自动升级",
			"condition": ["必须满足全部条件"]
		}
		"""
	When jobs添加会员等级
		"""
		[{
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
			"upgrade": "手动升级",
			"discount": "7"
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
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""

