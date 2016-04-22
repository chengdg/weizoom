# __author__ : "张三香"
#editor:雪静 2015.10.15
Feature: 创建积分应用活动
		Jobs能通过管理系统在商城中添加'积分应用'活动

"""
	1、积分应用活动设置规则
		1）【活动名称】：必填字段，1-20个字内
		2）【广告语】：在商品名称后红字显示
		3）【比例设置】：设置商品的积分抵扣上限，积分抵扣金额：【抵扣金额】=【商品数量】*【商品单价】*【抵扣上限】
			（1）统一设置：
				为全部等级的会员设置统一的积分抵扣上限
			（2）分级设置：
				为系统中所有等级的会员分别设置积分抵扣上限
		4）【活动时间】：开始结束时间只能选择今天及其之后的时间，结束时间必须在开始时间之后
			勾选"永久"，清空活动时间，此活动永久有效，除非手动结束活动

	2、结束积分应用活动
		‘进行中’和‘未开始’的积分应用活动，可以手动进行'结束'操作
		‘永久’和‘非永久’的积分应用活动，一旦结束在购买时就不能使用了
	3、删除积分应用活动
		‘已结束’的积分应用活动才可以删除
	4、积分使用规则
		1）积分和优惠券不能在同一个订单中同时使用，即使两个活动针对的是不同的商品
		2）一个订单包含多个具有积分活动的商品，每个商品分别使用自己的积分活动
		3）会员既具有会员等级价又具有会员积分活动权限的，会员看到的商品显示会员价，购买时会员价下单，并在会员价的基础上使用积分抵扣，
			积分抵扣的上限，按照会员价计算
	5、设置了“限时抢购”的商品，不能再设置“买赠”“优惠券活动”，三个活动是互斥的，只要设置了其中的一个活动，就不能再设置其他两个活动
"""
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
			"name": "商品1",
			"price": 100.00
		}, {
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
		}, {
			"name": "商品3",
			"is_member_product": "on",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 100.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 100.00,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name": "商品4",
			"price": 100.00
		},{
			"name": "商品5",
			"is_member_product": "on",
			"price": 100.00
		},{
			"name": "商品6",
			"price": 100.00
		},{
			"name": "赠品6",
			"price": 10.00
		},{
			"name": "商品7",
			"is_member_product": "on",
			"price": 100.00
		},{
			"name": "赠品7",
			"price": 10.00
		},{
			"name": "商品8",
			"price": 100.00
		},{
			"name": "商品9",
			"is_member_product": "on",
			"price": 100.00
		}]
		"""

	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品4限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品4",
			"member_grade": "全部",
			"count_per_purchase": 2,
			"promotion_price": 90.00
		},{
			"name": "商品5限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品5",
			"member_grade": "全部",
			"promotion_price": 90.00,
			"limit_period": 1
			}]
		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "商品6买二赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品6",
			"premium_products": 
			[{
				"name": "赠品6",
				"count": 1
			}],
			"count": 2,
			"is_enable_cycle_mode": true
		},{
			"name": "商品7买一赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品7",
			"premium_products":
			[{
				"name": "赠品7",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": true
		}]
		"""
	When jobs添加优惠券规则
		"""
		[{
			"name": "单品券商品8",
			"money": 1.00,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "商品8"
		},{
			"name": "单品券商品9",
			"money": 10.00,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品9"
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
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2,
			"use_ceiling": -1
		}
		"""



@mall2 @promotion @promotionIntegral @integral
Scenario: 1 选取普通商品，创建统一设置积分应用活动
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"is_permanant_active": false,
			"discount": 50,
			"discount_money": 50.00
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品1积分应用",
			"product_name": "商品1",
			"product_price":100.00,
			"discount": "50.0%",
			"discount_money": 50.00,
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 2 选取多规格商品，创建分级设置积分应用活动
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
					"discount": 100,
					"discount_money": 100.00
				},{
					"member_grade": "铜牌会员",
					"discount": 90,
					"discount_money": 90.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品2积分应用",
			"product_name": "商品2",
			"product_price": "100.00 ~ 200.00",
			"discount": "90.0%~100.0%",
			"discount_money": "90.00~100.00",
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 3 选取有会员价的商品，创建分级设置积分应用活动（后台抵扣金额按照商品原价进行计算显示，手机端购买时按照会员价进行计算）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品3",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "普通会员",
					"discount": 100,
					"discount_money": 100.00
				},{
					"member_grade": "铜牌会员",
					"discount": 90,
					"discount_money": 90.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品3积分应用",
			"product_name": "商品3",
			"product_price":100.00,
			"discount": "90.0%~100.0%",
			"discount_money": "90.00~100.00",
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 4 选取无会员价且已参与'限时抢购'活动的商品，创建积分应用活动（后台抵扣金额按照商品原价进行计算显示，手机端购买时显示限购价格，）
	Given jobs登录系统
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
					"discount_money": 100.00
				},{
					"member_grade": "铜牌会员",
					"discount": 90,
					"discount_money": 90.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品4积分应用",
			"product_name": "商品4",
			"product_price":100.00,
			"discount": "90.0%~100.0%",
			"discount_money": "90.00~100.00",
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 5 选取有会员价且已参与'限时抢购'活动的商品，创建积分应用活动
	#（后台抵扣金额按照商品原价进行计算显示，限时抢购优先，手机端抵扣金额按照当前页面显示的商品价格进行计算）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品5积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品5",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 50,
					"discount_money": 50.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品5积分应用",
			"product_name": "商品5",
			"product_price":100.00,
			"discount": "50.0%",
			"discount_money": 50.00,
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 6 选取无会员价且已参与'买赠'活动的商品，创建积分应用活动（后台抵扣金额按照商品原价进行计算显示）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品6积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品6",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 50,
					"discount_money": 50.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品6积分应用",
			"product_name": "商品6",
			"product_price":100.00,
			"discount": "50.0%",
			"discount_money": 50.00,
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 7 选取有会员价且已参与'买赠'活动的商品，创建积分应用活动 （后台抵扣金额按照商品原价进行计算显示，买赠优先，手机端抵扣金额按照当前页面显示的商品价格进行计算）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品7积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品7",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 50,
					"discount_money": 50.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品7积分应用",
			"product_name": "商品7",
			"product_price":100.00,
			"discount": "50.0%",
			"discount_money": 50.00,
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 8 选取无会员价且已设置单品券的商品，创建积分应用活动（后台抵扣金额按照商品原价进行计算显示，手机端购买时积分和优惠券不能同时使用）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品8积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品8",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 50,
					"discount_money": 50.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品8积分应用",
			"product_name": "商品8",
			"product_price":100.00,
			"discount": "50.0%",
			"discount_money": 50.00,
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 9 选取有会员价且已设置单品券的商品，创建积分应用活动（后台抵扣金额按照商品原价进行计算显示，手机端购买时积分抵扣按照会员价计算，但积分和优惠券不能同时使用）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品9积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品9",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 50,
					"discount_money": 50.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品9积分应用",
			"product_name": "商品9",
			"product_price":100.00,
			"discount": "50.0%",
			"discount_money": 50.00,
			"status":"进行中"
		}]
		"""






