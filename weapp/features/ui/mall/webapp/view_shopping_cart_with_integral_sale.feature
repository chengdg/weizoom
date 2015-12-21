# __edit__ : "新新8.26"
# 该feature与普通商品在购物车中的形式没有差别
# 无论是统一抵扣还是单独设置积分商品,加入购物中后都是一样的状态

Feature: 添加积分应用活动商品到购物车后，浏览购物车中的商品
"""
	1.bill将积分应用活动商品放入购物车后，能浏览商品信息
	2.积分活动商品为会员价添加到购物车

"""

Background:
	Given jobs登录系统
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
	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2,
			"use_ceiling": -1
		}
		"""
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
			"price": 100
		}, {
			"name": "商品2",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 100,
						"stock_type": "有限",
						"stocks": 2
					},
					"S": {
						"price": 200,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品3",
			"is_member_product": "on",
			"price": 300,
		}]	
		"""
	#创建无规格活动,统一设置
	
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"is_permanant_active": false,
			"discount": 50,
			"discount_money": 50.0
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品1积分应用",
			"product_name": "商品1",
			"product_price":100.00,
			"discount": "50%",
			"discount_money": 50.0,
			"status":"进行中"
		}]
		"""

	#创建有规格并且分级设置
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
				},{
					"member_grade": "铜牌会员",
					"discount": 90,
					"discount_money": 90.0
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品2积分应用",
			"product_name": "商品2",
			"product_price": "100.0 ~ 200.0",
			"discount": "90%~100%",
			"discount_money": "90.0~100.0",
			"status":"进行中"
		}]
		"""
	#创建有会员价商品积分抵扣活动,全部抵扣
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品3",
			"is_permanant_active": false,
			"discount": 50,
			"discount_money": 150.0
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品3积分应用",
			"product_name": "商品3",
			"product_price":300.00,
			"discount": "50%",
			"discount_money": 150.0,
			"status":"进行中"
		}]
		"""
	When bill关注jobs的公众号
	And tom关注jobs的公众号


Scenario: 放入参加积分活动的商品到购物车，商品不显示促销信息

	#bill为铜牌会员时,把商品3放到购物车时,显示商品3九折显示价格
	When jobs更新'bill'的会员等级
		"""
		{
			"name": "bill",
			"member_rank": "铜牌会员"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "普通会员"
		},{
			"name": "bill",
			"member_rank": "铜牌会员"
		}]
		"""
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品2",
			"model": {
				"models":{
					"M": {
						"count": 1
					}
				}
			}
		}, {
			"name": "商品2",
			"model": {
				"models":{
					"S": {
						"count": 1
					}
				}
			}
		},{
			"name": "商品3",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	#按加入购物车的倒序显示
	Then bill能获得购物车:ui
	#商品3在购物车中显示会员价
		"""
		{
			"total_product_count": 4,
			"total_price": 670.0,
			"product_groups": [{
				"promotion": {
					"type": "积分抵扣",
					"result": {
						"name": "商品3",
						"count": 1,
						"saved_money": 270
					}
				},
				"promotion": {
					"type": "积分抵扣",
					"result": {
						"name": "商品2",
						"model": "S",
						"count": 1,
						"saved_money": 200
					}
				},
				"promotion": {
					"type": "积分抵扣",
					"result": {
						"name": "商品2",
						"model": "M",
						"count": 1,
						"saved_money": 100
					}
				},
				"promotion": {
					"type": "积分抵扣",
					"result": {
						"name": "商品1",
						"count": 1,
						"saved_money": 100
					}
				}
			}],
			"invalid_products": []
		}
		"""

	When tom访问jobs的webapp:ui
	Then tom能获得购物车:ui
		"""
		{
			"product_groups": [],
			"invalid_products": []
		}
		"""

