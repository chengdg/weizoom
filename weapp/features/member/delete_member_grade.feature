# __author__ : "冯雪静"
# __edite__ : "benchi" 没有问题，添加标签
Feature: 删除会员等级
	Jobs能删除会员管理中的会员等级
	"""
	1.删除已存在的手动升级的会员等级
	2.删除已存在的自动升级的会员等级
	3.创建促销活动时，设置单个会员等级，删除等级后，没有此等级，促销活动自动结束，详情没有此等级
	"""

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


@mall2 @member @meberGrade @promotionFlash @promotionIntegral @promotionPremium
Scenario: 3 创建促销活动时，设置单个会员等级，删除等级后，没有此等级
	1.jobs创建完促销活动，然后删除等级
	2.促销活动自动结束，详情没有此等级

	Given jobs登录系统
	And jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 10
		}
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00
		}, {
			"name": "商品2",
			"price": 100.00
		}, {
			"name": "商品3",
			"price": 100.00
		}]
		"""
	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品1限时抢购",
			"promotion_title": "",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name":"商品1",
			"member_grade": "银牌会员",
			"count_per_purchase": 2,
			"promotion_price": 80.00,
			"limit_period": 1
		}]
		"""
	Then jobs获取限时抢购活动列表
		"""
		[{
			"name": "商品1限时抢购",
			"product_name": "商品1",
			"product_price": 100.00,
			"promotion_price": 80.00,
			"status": "进行中",
			"start_date": "今天",
			"end_date": "1天后"
		}]
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品2积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品2",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "普通会员",
					"discount": 100,
					"discount_money": 100.0
				}, {
					"member_grade": "铜牌会员",
					"discount": 90,
					"discount_money": 90.0
				}, {
					"member_grade": "银牌会员",
					"discount": 80,
					"discount_money": 80.0
				}, {
					"member_grade": "金牌会员",
					"discount": 70,
					"discount_money": 70.0
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品2积分应用",
			"product_name": "商品2",
			"product_price":100.00,
			"discount": "70%~100%",
			"discount_money": "70.0~100.0",
			"status":"进行中"
		}]
		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "商品3买二赠一",
			"promotion_title":"",
			"start_date": "今天",
			"end_date": "1天后",
			"member_grade": "银牌会员",
			"product_name": "商品3",
			"premium_products": 
				[{
				"name": "商品2",
				"count": 1
			}],
			"count": 2,
			"is_enable_cycle_mode": true
		}]
		"""
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "商品3买二赠一",
			"product_name": "商品3",
			"product_price":100.00,
			"status":"进行中",
			"start_date": "今天",
			"end_date": "1天后"
		}]
		"""
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
	And jobs获取限时抢购活动列表
		"""
		[{
			"name": "商品1限时抢购",
			"product_name": "商品1",
			"product_price": 100.00,
			"promotion_price": 80.00,
			"status": "已结束",
			"member_grade": "普通会员",
			"start_date": "今天",
			"end_date": "1天后"
		}]
		"""
	And jobs获取积分应用活动列表
		"""
		[{
			"name":"商品2积分应用",
			"product_name": "商品2",
			"product_price":100.00,
			"discount": "70%~100%",
			"discount_money": "70.0~100.0",
			"status":"进行中",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "普通会员",
					"discount": 100
				}, {
					"member_grade": "铜牌会员",
					"discount": 90
				}, {
					"member_grade": "金牌会员",
					"discount": 70
				}]
		}]
		"""
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "商品3买二赠一",
			"product_name": "商品3",
			"product_price":100.00,
			"status":"已结束",
			"member_grade": "普通会员",
			"start_date": "今天",
			"end_date": "1天后"
		}]
		"""