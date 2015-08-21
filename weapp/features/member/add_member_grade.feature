# __author__ : "冯雪静"
# __edit__ : "benchi" 对ui验证的修复
Feature: 增加会员等级
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
Scenario: 1 添加手动升级的会员等级
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
Scenario: 2 添加自动升级的会员等级
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
			"upgrade_lower_bound": 10000,
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"upgrade_lower_bound": 30000,
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "自动升级",
			"pay_money": 5000.00,
			"pay_times": 50,
			"upgrade_lower_bound": 50000,
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
			"upgrade_lower_bound": 10000,
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"upgrade_lower_bound": 30000,
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "自动升级",
			"pay_money": 5000.00,
			"pay_times": 50,
			"upgrade_lower_bound": 50000,
			"discount": "7"
		}]
		"""

@mall2 @member @meberGrade
Scenario: 3 添加手动和自动升级的会员等级
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
			"upgrade_lower_bound": 10000,
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"upgrade_lower_bound": 30000,
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
			"upgrade_lower_bound": 10000,
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"upgrade_lower_bound": 30000,
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""

@ui @member @meberGrade
Scenario: 4 添加自动升级的会员等级时有冲突
	jobs添加多组自动升级的会员等级时
	1. 数据有冲突，提示错误信息
	2. 等级名称为空，提示错误信息


	Given jobs登录系统
	When jobs开启自动升级
		"""
		{
			"upgrade": "自动升级",
			"condition": ["必须满足全部条件"]
		}
		"""
	#按照创建顺序，自动升级状态下的下一级必须比上一级升级条件高，折扣可以是相同或递减
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 20,
			"upgrade_lower_bound": 10000,
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 10,
			"upgrade_lower_bound": 30000,
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "自动升级",
			"pay_money": 5000.00,
			"pay_times": 50,
			"upgrade_lower_bound": 50000,
			"discount": "9"
		}]
		"""
	Then jobs获得提示错误信息'等级升级条件必须逐级递增'
	And jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"discount": "10"
		}]
		"""
	When jobs开启自动升级
		"""
		{
			"upgrade": "自动升级",
			"condition": ["必须满足全部条件"]
		}
		"""
	#验证升级条件
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 20,
			"upgrade_lower_bound": 10000,
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 10,
			"upgrade_lower_bound": 30000,
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "自动升级",
			"pay_money": 5000.00,
			"pay_times": 50,
			"upgrade_lower_bound": 50000,
			"discount": "7"
		}]
		"""
	Then jobs获得提示错误信息'等级升级条件必须逐级递增'
	And jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"discount": "10"
		}]
		"""
	#验证折扣
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 20,
			"upgrade_lower_bound": 10000,
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"upgrade_lower_bound": 30000,
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "自动升级",
			"pay_money": 5000.00,
			"pay_times": 50,
			"upgrade_lower_bound": 50000,
			"discount": "9"
		}]
		"""
	Then jobs获得提示错误信息'等级折扣必须逐级递减或相同'
	And jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"discount": "10"
		}]
		"""
	#验证空
	When jobs添加会员等级
		"""
		[{
			"name": "",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 20,
			"upgrade_lower_bound": 10000,
			"discount": "9"
		}, {
			"name": "",
			"upgrade": "自动升级",
			"pay_money": 3000.00,
			"pay_times": 30,
			"upgrade_lower_bound": 30000,
			"discount": "8"
		}, {
			"name": "",
			"upgrade": "自动升级",
			"pay_money": 5000.00,
			"pay_times": 50,
			"upgrade_lower_bound": 50000,
			"discount": "7"
		}]
		"""
	Then jobs获得提示错误信息'内容不能为空'
	And jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"discount": "10"
		}]
		"""
	#条件为空/输入错误，金额提示'请输入正确的金额'，购买次数和经验值提示'请输入正整数'
	#折扣为空/输入错误，提示'请输入1.0~10的数'
