Feature: 添加商品到购物车后，浏览购物车中的商品
	bill将各种商品放入购物车后，能浏览商品信息

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
			"price": 30.00,
			"model": {
				"models": {
					"standard": {
						"price": 30100.00,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		} {
			"name": "商品2",
			"price": 5
		}, {
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 7,
						"stock_type": "有限",
						"stocks": 2
					},
					"S": {
						"price": 8,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品4",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 9,
						"stock_type": "无限"
					}
				}   
			}
		}, {
			"name": "商品5",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 40.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 40.00,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}, {
			"name": "商品2限时抢购",
			"start_date": "1天后",
			"end_date": "2天后",
			"products": ["商品2"],
			"promotion_price": 2.1
		}, {
			"name": "商品3限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品3"],
			"promotion_price": 3.1,
			"limit_period": 1
		}, {
			"name": "商品4限时抢购",
			"start_date": "前天",
			"end_date": "昨天",
			"products": ["商品4"],
			"promotion_price": 4.1
		}]
		"""
	#支付方式
	Given jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
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
	Given bill关注jobs的公众号
	And tom关注jobs的公众号
	And sam关注jobs的公众号
	And jobs登录系统
	And jobs调tom等级为铜牌会员
	And jobs调sam等级为银牌会员
	Then jobs可以获得会员列表
	"""
		[{
			"name": "sam",
			"grade_name": "银牌会员"
		}, {
			"name": "tom",
			"grade_name": "铜牌会员"
		}, {
			"name": "bill",
			"grade_name": "普通会员"
		}]
	"""
	And bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill设置jobs的webapp的默认收货地址


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.flash_sale
Scenario: 从购物车购买参加限时抢购活动的商品，商品包括无规格，有规格，活动有效，活动无效
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品6",
			"count": 1
		}, {
			"name": "商品3",
			"model": {
				"models":{
					"M": {
						"count": 1
					}
				}
			}
		}, {
			"name": "商品3",
			"model": {
				"models":{
					"S": {
						"count": 2
					}
				}
			}
		}]
		"""
	When bill访问jobs的webapp:ui
	When bill从购物车发起购买操作:ui
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 25.8,
				"product_price": 25.8,
				"promotion_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 1
				}]
			}, {
				"products": [{
					"name": "商品3",
					"model": "M",
					"price": 3.1,
					"count": 1
				}]
			}, {
				"products": [{
					"name": "商品3",
					"model": "S",
					"price": 3.1,
					"count": 2
				}]
			}, {
				"products": [{
					"name": "商品6",
					"price": 5.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 25.8
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.flash_sale
Scenario: 直接购买参加限时抢购活动的商品
	
	When bill访问jobs的webapp
	When bill访问jobs的webapp:ui
	And bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品1",
				"count": 1
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 11.5,
				"product_price": 11.5,
				"promotion_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 1
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"price": 11.5
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.flash_sale
Scenario: 直接购买参加限时抢购活动的商品，但活动当前没有启动
	
	When bill访问jobs的webapp
	When bill访问jobs的webapp:ui
	And bill立即购买jobs的商品:ui
		"""
		{
			"product": {
				"name": "商品2",
				"count": 1
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 5.0,
				"product_price": 5.0,
				"promotion_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品2",
					"price": 5.0,
					"count": 1
				}]
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui


Scenario:2 购买单个限时抢购商品，限时抢购已过期（在购物车中是限时抢购商品，但，去提交订单时已经不是限时抢购商品）

	When bill访问jobs的webapp:ui
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}]
		}
		"""
	Then bill获得创建订单失败的信息:ui
		"""
		{
			"detail": [{
				"id": "商品3",
				"msg": "该活动已经过期",
				"short_msg": "已经过期"
			}]
		}
		"""

Scenario: 4 购买多个商品，带有限时抢购商品

	Given jobs登录系统:ui
	And jobs创建限时抢购活动:ui
	"""
		{
			"name": "商品4限时抢购",
			"start_date": "前天",
			"end_date": "昨天",
			"product_name": "商品4",
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}
		"""
	When bill访问jobs的webapp:ui
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}, {
				"name": "商品2",
				"count": 1
			}, {
				"name": "商品4",
				"count": 1
			}]
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 37,
				"product_price": 37,
				"promotion_money": 0.0,
				"postage": 0.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 2
				}]
			}, {
				"promotion": null,
				"product": [{
					"name": "商品2"，
					"price": 5,
					"count": 1
				}]
			}, {
				"promotion": null,
				"product": [{
					"name": "商品4",
					"price": 9,
					"count": 1
				}]
			}]
		}
		"""

Scenario: 5 购买单个限时抢购商品，超出库存限制
	第一次购买2个，成功；第二次购买2个，超出商品库存，确保缓存更新

	When bill访问jobs的webapp:ui
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 23.0
		}
		"""
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill获得创建订单失败的信息:ui
		"""
		{
			"detail": [{
				"id": "商品1",
				"msg": "有商品库存不足，请重新下单",
				"short_msg": "库存不足"
			}]
		}
		"""

Scenario: 6  购买单个限时抢购商品，未超过库存限制，但超过单次购买限制

	Given jobs登录系统:ui
	When jobs创建限时抢购活动:ui
		"""
		{
			"name": "商品4限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品4",
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}
		"""
	When bill访问jobs的webapp:ui
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 2
			}]
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 23.0
		}
		"""
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 3
			}]
		}
		"""
	Then bill获得创建订单失败的信息'限购2件':ui

Scenario: 7 在限购周期内连续购买限时抢购商品

	When bill访问jobs的webapp:ui
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品2",
				"count": 1
			}]
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 2.1
		}
		"""
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}]
		}
		"""
		Then bill获得创建订单失败的信息:ui
		"""
		{
			"detail": [{
				"id": "商品3",
				"msg": "在限购周期内不能多次购买",
				"short_msg": "限制购买"
			}]
		}
		"""

Scenario: 8 购买多规格限时抢购商品
	Given jobs登录系统:ui
	When jobs创建限时抢购活动:ui
		"""
		{
			"name": "商品5限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品5",
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}
		"""
	When bill访问jobs的webapp:ui
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品5",
				"count": 1,
				"model": "S"
			}, {
				"name": "商品5",
				"count": 1,
				"model": "M"
			}]
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 23.0
		}
		"""
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品5",
				"count": 2,
				"model": "S"
			}, {
				"name": "商品5",
				"count": 1,
				"model": "M"
			}]
		}
		"""
	Then bill获取创建订单失败的信息:ui
	"""
		[{
			"detail": [{
				"id": "商品5",
				"msg": "该订单内商品状态发生变化！",
				"short_msg": "限购2件"
			}]
		}]
	"""

Scenario: 9 购买多规格限时抢购商品同时适用于积分规则

	Given jobs登录系统:ui
	And jobs设定会员积分策略:ui
		"""
		{
			"integral_each_yuan": 2,
			"use_ceiling": 50
		}
		"""


	When jobs创建限时抢购活动:ui
		"""
		{
			"name": "商品5限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品5",
			"count_per_purchase": 2,
			"promotion_price": 10
		}
		"""
	When bill访问jobs的webapp:ui
	When bill获得jobs的50会员积分:ui
	Then bill在jobs的webapp中拥有50会员积分:ui
	When bill购买jobs的商品:ui
		"""
		{
			"integral_money":10.00,
			"integral":20.00,
			"products": [{
				"name": "商品5",
				"count": 1,
				"model": "S"
			}, {
				"name": "商品5",
				"count": 1,
				"model": "M"
			}]
		}
		"""
	Then bill获得待编辑订单:ui
	"""
		{
			"price_info": {
				"final_price": 10.0,
				"product_price": 20.00,
				"promotion_saved_money": 60.00,
				"integral_money": 10.00,
				"integral": 20.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品5",
					"price": 10,
					"count": 1,
					"model": "S"
				}, {
					"name": "商品5",
					"price": 10,
					"count": 1,
					"model": "M"
				}]
			}]
		}
		"""

	Then bill在jobs的webapp中拥有30会员积分:ui

Scenario: 10 购买单个限时抢购商品，购买时活动进行中，提交订单时，该活动被商家手工结束

	Given jobs登录系统:ui
	When jobs创建限时抢购活动:ui
		"""
		{
			"name": "商品4限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品4",
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}
		"""
	And jobs'结束'促销活动'商品4限时抢购':ui

	When bill访问jobs的webapp:ui
	And bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1,
				"promotion": {
					"name": "商品4限时抢购"
				}
			}]
		}
		"""

	Then bill获得创建订单失败的信息:ui
		"""
		{
			"detail": [{
				"id": "商品4",
				"msg": "该活动已经过期",
				"short_msg": "已经过期"
			}]
		}
		"""

Scenario: 11 购买单个限时抢购商品，未支付然后取消订单，还可以再次下单
	有限购周期和限购数量设置

	Given jobs登录系统:ui
	When jobs创建限时抢购活动:ui
		"""
		{
			"name": "商品4限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品4",
			"count_per_purchase": 2,
			"promotion_price": 11.5,
			"limit_period": 1
		}
		"""
	When bill访问jobs的webapp:ui
	And bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1,
				"promotion": {
					"name": "商品4限时抢购"
				}
			}]
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 11.5
		}
		"""
	Given jobs登录系统:ui
	Then jobs可以获得最新订单详情:ui
		"""
		{
			"status": "待支付",
			"final_price": 11.5,
			"actions": ["取消订单", "支付","修改价格"]
		}
		"""
	When jobs"取消"最新订单:ui
		"""
		 {
		 	"reason": "不想要了"
		 }
		"""
	Then jobs可以获得最新订单详情:ui
		"""
		{
			"status": "已取消",
			"final_price": 11.5,
			"actions": []
		}
		"""
	When bill访问jobs的webapp:ui
	And bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 2,
				"promotion": {
					"name": "商品4限时抢购"
				}
			}]
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 23.00
		}
		"""
	Given jobs登录系统:ui
	Then jobs可以获得最新订单详情:ui
		"""
		{
			"status": "待支付",
			"final_price": 23.00,
			"actions": ["取消订单", "支付","修改价格"]
		}
		"""

Scenario:12 不同等级的会员购买有会员价同时有限时抢购的商品（限时抢购优先于会员价）
	When jobs更新商品'商品1':ui
	"""
	{
		"is_member_product": "on",
		"model": {
			"models": {
				"standard": {
					"stock_type": "有限",
					"stocks": 30,
					"price": 100
				}
			}
		}
	}
	"""
	#When jobs创建限时抢购活动
	#"""
	#	[{
	#		"name": "商品1限时抢购",
	#		"start_date": "今天",
	#		"end_date": "1天后",
	#		"product_name": "商品1",
	#		"member_grade": "全部",
	#		"promotion_price": 11.5
	#	}]
	#"""
	When bill访问jobs的webapp:ui
	And bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill获得待编辑订单:ui
	"""
		{
			"price_info": {
				"final_price": 23.0,
				"product_price": 23.00,
				"promotion_saved_money": 177.00,
				"integral_money": 10.00,
				"integral": 20.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 2,
					"promotion": {
						"promotioned_product_price": 11.5,
						"type": "flash_sale"
					}
				}]
			}]
		}
		"""

	When tom访问jobs的webapp:ui
	And tom购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then tom获得待编辑订单:ui
	"""
		{
			"price_info": {
				"final_price": 23.0,
				"product_price": 23.00,
				"promotion_saved_money": 177.00,
				"integral_money": 10.00,
				"integral": 20.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 11.5,
					"count": 2,
					"promotion": {
						"promotioned_product_price": 11.5,
						"type": "flash_sale"
					}
				}]
			}]
		}
		"""

Scenario: 13 不同等级的会员购买有会员价同时有会员等级限时抢购的商品（限时抢购优先于会员价）
	When jobs更新商品'商品1':ui
	"""
	{
		"is_member_product": "on",
		"model": {
			"models": {
				"standard": {
					"stock_type": "有限",
					"stocks": 30,
					"price": 100
				}
			}
		}
	}
	"""
	And jobs'结束'促销活动'商品1限时抢购':ui
	And jobs创建限时抢购活动:ui
	"""
		[{
			"name": "商品1限时抢购-50",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"member_grade": "银牌会员",
			"promotion_price": 50.0
		}]
	"""
	When bill访问jobs的webapp:ui
	And bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill获得待编辑订单:ui
	"""
		{
			"price_info": {
				"final_price": 200.0,
				"product_price": 200.0,
				"promotion_saved_money": 0.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 100,
					"count": 2
				}]
			}]
		}
		"""

	When tom访问jobs的webapp:ui
	And tom购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then tom获得待编辑订单:ui
	"""
		{
			"price_info": {
				"final_price": 180.0,
				"product_price": 180.0,
				"promotion_saved_money": 20.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 90,
					"count": 2
				}]
			}]
		}
		"""

	When sam访问jobs的webapp:ui
	And sam购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then sam获得待编辑订单:ui
	"""
		{
			"price_info": {
				"final_price": 100.0,
				"product_price": 100.0,
				"promotion_saved_money": 100.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 50,
					"count": 2,
					"promotion": {
					"promotioned_product_price": 50.0,
					"promotion_saved_money": 100.0,
					"type": "flash_sale"
				}
				}]
			}]
		}
		"""


Scenario: 14 不同等级的会员购买原价有会员等级限时抢购的商品
	When jobs更新商品'商品1':ui
	"""
	{
		"is_member_product": "off",
		"model": {
			"models": {
				"standard": {
					"price": 100.00,
					"stock_type": "有限",
					"stocks": 30
				}
			}
		}
	}
	"""
	And jobs'结束'促销活动'商品1限时抢购':ui
	And jobs创建限时抢购活动:ui
	"""
		[{
			"name": "商品1限时抢购-50",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"member_grade": "银牌会员",
			"promotion_price": 50.0
		}]
	"""
	When bill访问jobs的webapp:ui
	And bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill获得待编辑订单:ui
	"""
		{
			"price_info": {
				"final_price": 200.0,
				"product_price": 200.0,
				"promotion_saved_money": 0.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 50,
					"count": 2
				}]
			}]
		}
		"""

	When tom访问jobs的webapp:ui
	And tom购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then tom获得待编辑订单:ui
		"""
		{
			"price_info": {
				"final_price": 200.0,
				"product_price": 200.0,
				"promotion_saved_money": 0.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 50,
					"count": 2
				}]
			}]
		}
		"""
	When sam访问jobs的webapp:ui
	And sam购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then sam获得待编辑订单:ui
	"""
		{
			"price_info": {
				"final_price": 100.0,
				"product_price": 100.0,
				"promotion_saved_money": 100.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 50,
					"count": 2,
					"promotion": {
					"promotioned_product_price": 50.0,
					"promotion_saved_money": 100.0,
					"type": "flash_sale"
				}
				}]
			}]
		}
		"""


Scenario: 15 购买多规格限时抢购商品同时适用于积分规则和会员等级

	Given jobs登录系统:ui
	And jobs设定会员积分策略:ui
	"""
	{
		"integral_each_yuan": 2,
		"use_ceiling": 50
	}
	"""
	When jobs更新商品'商品5':ui
	"""
	{
		"is_member_product": "on",
		"is_enable_model": "启用规格",
		"model": {
			"models":{
				"M": {
					"price": 40.00,
					"stock_type": "无限"
				},
				"S": {
					"price": 40.00,
					"stock_type": "无限"
				}
			}
		}
	}
	"""
	When jobs创建限时抢购活动:ui
	"""
	{
		"name": "商品5限时抢购",
		"start_date": "今天",
		"end_date": "1天后",
		"product_name": "商品5",
		"member_grade": "银牌会员",
		"promotion_price": 10
	}
	"""
	When bill访问jobs的webapp:ui
	When bill获得jobs的100会员积分:ui
	Then bill在jobs的webapp中拥有100会员积分:ui
	When tom获得jobs的100会员积分:ui
	Then tom在jobs的webapp中拥有100会员积分:ui
	When sam获得jobs的100会员积分:ui
	Then sam在jobs的webapp中拥有100会员积分:ui
	When bill访问jobs的webapp:ui
	And bill购买jobs的商品:ui
	"""
	{
		"integral_money":40.00,
		"integral":80.00,
		"products": [{
			"name": "商品5",
			"count": 1,
			"model": "S"
		}, {
			"name": "商品5",
			"count": 1,
			"model": "M"
		}]
	}
	"""
	Then bill获得待编辑订单:ui
	"""
		{
			"price_info": {
				"final_price": 40.0,
				"product_price": 80.0,
				"promotion_saved_money": 0.00,
				"integral": 80.00,
				"integral_money": 40.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品5",
					"model": "S"
					"count": 1
				}, {
					"name": "商品5",
					"model": "M",
					"count": 1
				}]
			}]
		}
		"""

	Then bill在jobs的webapp中拥有20会员积分:ui
	When tom访问jobs的webapp:ui
	And tom购买jobs的商品:ui
	"""
	{
		"integral_money":36.00,
		"integral":72.00,
		"products": [{
			"name": "商品5",
			"count": 1,
			"model": "S"
		}, {
			"name": "商品5",
			"count": 1,
			"model": "M"
		}]
	}
	"""
	Then tom获得待编辑订单:ui
	"""
		{
			"price_info": {
				"final_price": 36.0,
				"product_price": 72.0,
				"promotion_saved_money": 0.00,
				"integral": 72.00,
				"integral_money": 36.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品5",
					"model": "S"
					"count": 1
				}, {
					"name": "商品5",
					"model": "M",
					"count": 1
				}]
			}]
		}
		"""

	Then tom在jobs的webapp中拥有28会员积分:ui
	When sam访问jobs的webapp:ui
	And sam购买jobs的商品:ui
	"""
	{
		"integral_money":10.00,
		"integral":20.00,
		"products": [{
			"name": "商品5",
			"count": 1,
			"model": "S"
		}, {
			"name": "商品5",
			"count": 1,
			"model": "M"
		}]
	}
	"""
	Then sam获得待编辑订单:ui
	"""
		{
			"price_info": {
				"final_price": 10.0,
				"product_price": 20.0,
				"promotion_saved_money": 0.00,
				"integral": 20.00,
				"integral_money": 10.00
			},
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品5",
					"model": "S"
					"count": 1
				}, {
					"name": "商品5",
					"model": "M",
					"count": 1
				}]
			}]
		}
		"""

	Then sam在jobs的webapp中拥有80会员积分:ui

