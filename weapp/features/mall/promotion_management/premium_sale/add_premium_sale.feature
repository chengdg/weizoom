#_author_:张三香

Feature:创建买赠活动

Background:
	Given jobs登录系统
	And jobs已添加商品规格
		"""
		[{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name":"商品1",
			"price":100.00
		},{
			"name":"赠品1",
			"price":100.00
		},{
			"name": "商品2",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 100.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 200.00,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name":"商品3",
			"price":100.00,
			"is_member_product": "on"
		},{
			"name":"商品4",
			"price":100.00,
			"is_member_product": "on"
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
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"discount": "10.0"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9.0"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8.0"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7.0"
		}]
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品4积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品4",
			"is_permanant_active": false,
			"rules": 
			[{
				"member_grade": "普通会员",
				"discount": 100,
				"discount_money": 100.0
			},{
				"member_grade": "铜牌会员",
				"discount": 90,
				"discount_money": 90.0
			},{
				"member_grade": "银牌会员",
				"discount": 80,
				"discount_money": 80.0
			},{
				"member_grade": "金牌会员",
				"discount": 70,
				"discount_money": 70.0
			}]
		}]
		"""

@mall2 @promotion @promotionPremium
Scenario: 1 主商品和赠品均为无规格商品，创建买赠活动
	Given jobs登录系统
	When jobs创建买赠活动
		"""
		[{
			"name": "商品1买二赠一",
			"promotion_title":"",
			"start_date": "今天",
			"end_date": "1天后",
			"member_grade": "普通会员",
			"product_name": "商品1",
			"premium_products": 
			[{
				"name": "赠品1",
				"count": 1
			}],
			"count": 2,
			"is_enable_cycle_mode": true
		}]
		"""
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "商品1买二赠一",
			"product_name": "商品1",
			"product_price":100.00,
			"status":"进行中",
			"start_date": "今天",
			"end_date": "1天后",
			"actions": ["详情","结束"]
		}]
		"""

@mall2 @promotion @promotionPremium
Scenario: 2 主商品为多规格，赠品为无规格商品，创建买赠活动
	Given jobs登录系统
	When jobs创建买赠活动
		"""
		[{
			"name": "商品2买一赠一",
			"promotion_title":"买一赠一啦",
			"start_date": "明天",
			"end_date": "3天后",
			"member_grade": "全部会员",
			"product_name": "商品2",
			"premium_products": 
			[{
				"name": "赠品1",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": true
		}]
		"""
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "商品2买一赠一",
			"promotion_title": "买一赠一啦",
			"product_name": "商品2",
			"product_price":"100.0 ~ 200.0",
			"status":"未开始",
			"start_date": "明天",
			"end_date": "3天后",
			"actions": ["详情","结束"]
		}]
		"""

@mall2 @promotion @promotionPremium
Scenario: 3 主商品为会员价商品，赠品为无规格，创建买赠活动
	Given jobs登录系统
	When jobs创建买赠活动
		"""
		[{
			"name": "商品3买一赠一",
			"promotion_title":"会员价商品买赠",
			"start_date": "明天",
			"end_date": "3天后",
			"member_grade": "铜牌会员",
			"product_name": "商品3",
			"premium_products": 
			[{
				"name": "赠品1",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": true
		}]
		"""
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "商品3买一赠一",
			"promotion_title": "会员价商品买赠",
			"product_name": "商品3",
			"product_price":100.00,
			"status":"未开始",
			"start_date": "明天",
			"end_date": "3天后",
			"actions": ["详情","结束"]
		}]
		"""

@mall2 @promotion @promotionPremium
Scenario: 4 主商品为会员价和积分应用商品，赠品为无规格，创建买赠活动
	Given jobs登录系统
	When jobs创建买赠活动
		"""
		[{
			"name": "商品4买一赠一",
			"promotion_title":"会员价商品买赠",
			"start_date": "今天",
			"end_date": "1天后",
			"member_grade": "金牌会员",
			"product_name": "商品4",
			"premium_products": 
			[{
				"name": "赠品1",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": true
		}]
		"""
	Then jobs获取买赠活动列表
		"""
		[{
			"name": "商品4买一赠一",
			"promotion_title": "会员价商品买赠",
			"product_name": "商品4",
			"product_price":100.00,
			"status":"进行中",
			"start_date": "今天",
			"end_date": "1天后",
			"actions": ["详情","结束"]
		}]
		"""

@mall2 @promotion @promotionPremium
Scenario: 5 主商品和赠品为同一个商品，创建买赠活动
	Given jobs登录系统
	When jobs创建买赠活动
		"""
			[{
				"name": "商品1买一赠一",
				"promotion_title":"",
				"start_date": "今天",
				"end_date": "1天后",
				"member_grade": "全部会员",
				"product_name": "商品1",
				"premium_products": 
				[{
					"name": "商品1",
					"count": 1
				}],
				"count": 1,
				"is_enable_cycle_mode": false
			}]
		"""
	Then jobs获取买赠活动列表
		"""
			[{
				"name": "商品1买一赠一",
				"product_name": "商品1",
				"product_price":100.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			}]
		"""

@mall2 @promotion @promotionPremium
Scenario: 6 选取多个赠品，创建买赠活动
	Given jobs登录系统
	When jobs创建买赠活动
		"""
			[{
				"name": "多个赠品买赠",
				"promotion_title":"",
				"start_date": "今天",
				"end_date": "1天后",
				"member_grade": "全部会员",
				"product_name": "商品1",
				"premium_products": 
				[{
					"name": "商品1",
					"count": 1
				},{
					"name": "赠品1",
					"count": 2
				},{
					"name": "商品3",
					"count": 1
				}],
				"count": 1,
				"is_enable_cycle_mode": false
			}]
		"""
	Then jobs获取买赠活动列表
		"""
			[{
				"name": "多个赠品买赠",
				"product_name": "商品1",
				"product_price":100.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			}]
		"""

