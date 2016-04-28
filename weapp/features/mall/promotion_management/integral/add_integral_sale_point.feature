# __author__ : "宋温馨"

Feature: 创建积分应用活动

Background:
	Given jobs登录系统

	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 15.00
		}, {
			"name": "商品2",
			"price": 50.00
		}] 
		"""

	#会员等级
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
		}]
		"""

@mall2 @promotion @promotionIntegral @integral @ztq
Scenario: 1 创建统一设置积分活动（填写抵扣金额，积分抵扣百分比显示小数点后两位，若是整数直接显示）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"is_permanant_active": false,
			"discount": 33.33,
			"discount_money": 5.00
			 
		}]
		"""
	Then jobs获取积分应用活动列表 
		"""
		[{
			"name":"商品1积分应用",
			"procucts":[{
				"name": "商品1",
				"price":15.00,
				"status":""
				}],
			"discount": "33.33%",
			"discount_money":5.00,
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral @ztq
Scenario: 2 创建分级设置积分应用活动（填写抵扣金额，积分抵扣百分比显示小数点后两位，若是整数直接显示）
	Given jobs登录系统
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
					"discount": 10.2,
					"discount_money": 5.10
				},{
					"member_grade": "铜牌会员",
					"discount": 20.5,
					"discount_money": 10.25
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品2积分应用",
			"procucts":[{
				"name": "商品2",
				"price":50.00,
				"status":""
				}],
			"discount": "10.2%~20.5%",
			"discount_money": "5.10~10.25",
			"status":"进行中"
		}]
		"""


