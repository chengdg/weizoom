@func:webapp.modules.mall.views.list_products
Feature: 在webapp中使用会员积分购买商品
	bill能在webapp中使用会员积分购买jobs添加的"商品"

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "商品2",
			"price": 200
		}, {
			"name": "商品3",
			"price": 50
		}, {
			"name": "商品4",
			"model": {
				"models": {
					"standard": {
						"price": 40.0,
						"stock_type": "有限",
						"stocks": 3
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
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部",
				"discount": 70,
				"discount_money": 70.0
			}]
		}, {
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "2天后",
			"product_name": "商品3",
			"is_permanant_active": true,
			"rules": [{
				"member_grade": "全部",
				"discount": 50,
				"discount_money": 25.0
			}]
		}, {
			"name": "商品5积分应用",
			"start_date": "今天",
			"end_date": "2天后",
			"product_name": "商品5",
			"is_permanant_active": true,
			"rules": [{
				"member_grade": "全部",
				"discount": 50,
				"discount_money": 20.0
			}]
		}]
		"""
	And jobs设定会员积分策略
		"""
		{
			"一元等价的积分数量": 5
		}
		"""
	When jobs添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号
	When bill访问jobs的webapp
	And bill设置jobs的webapp的默认收货地址


@ui @ui-mall @ui-member @ui-member.integral
Scenario: 使用少于商品金额的积分金额进行购买，并查看积分日志
	bill购买jobs的商品时，使用少于商品金额的积分金额进行购买
	1. 创建订单成功, 订单状态为“等待支付”
	2. bill积分减少
	3. bill能看到积分日志
	
	When bill访问jobs的webapp
	When bill获得jobs的5会员积分
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有5会员积分:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"use_integral": true
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"price_info": {
				"integral_count": 5,
				"integral_money": 1.0
			}
		}
		"""
	And bill在jobs的webapp中拥有0会员积分:ui
	And bill在jobs的webapp中的积分日志为:ui
		"""
		[{
			"integral": -5,
			"event": "使用积分"
		}, {
			"integral": 20,
			"event": "首次关注"
		}]
		"""


@ui @ui-mall @ui-member @ui-member.integral
Scenario: 使用等于商品金额的积分金额进行购买
	bill购买jobs的商品时，使用等于商品金额的积分金额进行购买
	1. 创建订单成功, 订单状态为“等待发货”
	2. bill积分减少
	
	When bill访问jobs的webapp
	When bill获得jobs的75会员积分
	Then bill在jobs的webapp中拥有75会员积分
	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}],
			"use_integral": true
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"cover": "下单成功",
			"price_info": {
				"integral_count": 75,
				"integral_money": 25
			}
		}
		"""
	And bill在jobs的webapp中拥有0会员积分:ui


@ui @ui-mall @ui-member @ui-member.integral
Scenario: 使用大于商品金额的积分金额进行购买
	bill购买jobs的商品时，使用等于商品金额的积分金额进行购买
	1. 创建订单失败
	2. bill积分不变
	3. 49.5积分会自动调整为50积分
	
	When bill访问jobs的webapp
	When bill获得jobs的500会员积分
	Then bill在jobs的webapp中拥有500会员积分
	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"use_integral": true
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"price_info": {
				"integral_count": 350,
				"integral_money": 70
			}
		}
		"""
	Then bill在jobs的webapp中拥有150会员积分:ui


@ui @ui-mall @ui-member @ui-member.integral
Scenario: 使用积分购买影响商品库存
	bill购买jobs的商品时，使用积分购买
	1. 创建订单成功, 商品库存减少
	2. 创建订单失败，商品库存不变
	
	Given jobs登录系统
	Then jobs能获取商品'商品4'
		"""
		{
			"name": "商品4",
			"model": {
				"models": {
					"standard": {
						"price": 40.0,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			} 
		}
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品4积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品4",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部",
				"discount": 50,
				"discount_money": 20.0
			}]
		}]
		"""
	When bill访问jobs的webapp
	When bill获得jobs的500会员积分
	Then bill在jobs的webapp中拥有500会员积分
	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 2
			}],
			"use_integral": true
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货"
		}
		"""
	#job登录，验证库存减少
	Given jobs登录系统:ui
	Then jobs能获取商品'商品4':ui
		"""
		{
			"name": "商品4",
			"model": {
				"models": {
					"standard": {
						"price": 40.0,
						"stock_type": "有限",
						"stocks": 1
					}
				}
			} 
		}
		"""
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有300会员积分

# _author_ "师帅8.26"补充
#1.设置统一积分抵扣，积分金额小于最大折扣金额，积分为0
#2.设置统一积分抵扣，积分金额等于最大折扣金额，积分为0
#3.设置统一积分抵扣，积分金额大于最大折扣金额，积分剩余
#4.设置统一积分抵扣，购买多规格商品和单规格商品，使用积分，先计算商品总金额，在积分抵扣
#5.设置统一积分抵扣，购买限时抢购商品，不含会员价，按照限时抢购价使用积分抵扣
#6.设置统一积分抵扣，购买买赠商品，可以使用积分抵扣，不影响买赠活动
#7.设置分级积分抵扣，购买时按照会员等级使用积分抵扣，活动结束后，原价购买
#8.设置分级积分抵扣，购买多规格商品，在商品列表页显示商品原价，在详情显示最低价格积分抵扣，在订单页显示选择规格的价格相应的积分抵扣
#9.设置会员价，参加积分抵扣，商品优先参与会员价，在根据会员价进行积分抵扣
#10.设置积分抵扣活动，活动未开始，购买时不显示积分活动
#11.设置积分抵扣活动，活动已失效，购买时不显示积分活动
#12.购买多个积分商品，包含统一抵扣和分级抵扣，购买时分开计算
#13.使用积分则不能选择使用优惠券
Scenario:使用积分购买商品后，取消订单，积分返回
	bill购买jobs的商品时，使用少于商品金额的积分金额进行购买
	1. 创建订单成功, 订单状态为“等待支付”
	2. bill积分减少
	3. bill能看到积分日志
	
	When bill访问jobs的webapp
	When bill获得jobs的5会员积分
	When bill访问jobs的webapp:ui
	Then bill在jobs的webapp中拥有5会员积分:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"use_integral": true
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"price_info": {
				"integral_count": 5,
				"integral_money": 1.0
			}
		}
		"""
	And bill在jobs的webapp中拥有0会员积分:ui
	And bill在jobs的webapp中的积分日志为:ui
		"""
		[{
			"integral": -5,
			"event": "使用积分"
		}, {
			"integral": 20,
			"event": "首次关注"
		}]
		"""
	When jobs取消订单
	Then bill在jobs的webapp中拥有5会员积分
	And bill在jobs的webapp中的积分日志为
	"""
		[{
			"integral": +5,
			"event": "取消订单，返回积分"
		}, {
			"integral": -5,
			"event": "使用积分"
		}, {
			"integral": 20,
			"event": "首次关注"
		}]
	"""

Scenario:  4 购买多个积分折扣商品，总积分金额小于最大折扣金额

	When bill访问jobs的webapp
	When bill获得jobs的150会员积分
	Then bill在jobs的webapp中拥有150会员积分
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1,
				"integral": 100
			}, {
				"name": "商品3",
				"count": 1,
				"integral": 50
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 120.0,
			"product_price": 150.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money": 30.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 1
			}, {
				"name": "商品3",
				"count": 1
			}]
		}
		"""
	Then bill在jobs的webapp中拥有0会员积分

Scenario: 5 购买单个积分折扣商品，积分活动还未开始
	积分活动还未开始，按原价下单

	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品4积分应用",
			"start_date": "1天后",
			"end_date": "2天后",
			"product_name": "商品4",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部",
				"discount": 50,
				"discount_money": 20.0
			}]
		}]
		"""
	When bill访问jobs的webapp
	When bill获得jobs的150会员积分
	Then bill在jobs的webapp中拥有150会员积分

	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1,
				"integral": 0
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 40.0,
			"product_price": 40.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品4",
				"count": 1
			}]
		}
		"""
	Then bill在jobs的webapp中拥有150会员积分

Scenario: 6 购买单个积分折扣商品，积分活动已结束，积分活动不是永久有效
	积分活动还未开始，按原价下单

	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品4积分应用",
			"start_date": "昨天",
			"end_date": "今天",
			"product_name": "商品4",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部",
				"discount": 50,
				"discount_money": 20.0
			}]
		}]
		"""
	When bill访问jobs的webapp
	When bill获得jobs的150会员积分
	Then bill在jobs的webapp中拥有150会员积分
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1,
				"integral": 0
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 40.0,
			"product_price": 40.00,
			"integral_money": 0.00,
			"products": [{
				"name": "商品4"
			}]
		}
		"""
	Then bill在jobs的webapp中拥有150会员积分

Scenario: 7 购买单个积分折扣商品，超出库存限制 后台进行库存数量验证
	第一次购买1个，成功；第二次购买2个，超出商品库存，确保缓存更新

	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付"
		}
		"""
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill获得创建订单失败的信息
		"""
		{
			"detail": [{
				"id": "商品1",
				"msg": "有商品库存不足，请重新下单",
				"short_msg": "库存不足"
			}]
		}
		"""

Scenario: 8 不同等级的会员购买有会员价同时有积分统一设置抵扣5的商品
#会员价和积分抵扣可以同时使用，会员价后再算积分抵扣的比例
	When tom1关注jobs的公众号
	And tom2关注jobs的公众号
	And tom3关注jobs的公众号
	And tom4关注jobs的公众号
	Given jobs登录系统
	And jobs已添加商品
	"""
		[{
			"name": "商品10",
			"price": 100.00,
			"is_member_product": "on"
		},{
			"name": "商品11",
			"price": 100.00,
			"is_member_product": "on"
		}]
	"""
	When jobs创建积分应用活动
	"""
		[{
			"name": "商品11积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品11",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部",
				"discount": 50,
				"discount_money": 50.0
				}]
		}]
	"""
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"discount": "9"
		},{
			"name": "银牌会员",
			"discount": "8"
		},{
			"name": "金牌会员",
			"discount": "7"
		}]
		"""
	When jobs更新"tom2"的会员等级
	"""
	{
		"name": "tom2",
		"member_rank": "铜牌会员"
	}
	"""
	When jobs更新"tom3"的会员等级
	"""
	{
		"name": "tom4",
		"member_rank": "银牌会员"
	}
	"""
	When jobs更新"tom4"的会员等级
	"""
	{
		"name": "tom4",
		"member_rank": "金牌会员"
	}
	"""
	Then jobs可以获得会员列表
	"""
	[{
		"name": "tom4",
		"member_rank": "金牌会员"
	}, {
		"name": "tom3",
		"member_rank": "银牌会员"
	}, {
		"name": "tom2",
		"member_rank": "铜牌会员"
	}, {
		"name": "tom1",
		"member_rank": "普通会员"
	}, {
		"name": "tom",
		"member_rank": "普通会员"
	}, {
		"name": "bill",
		"member_rank": "普通会员"
	}]
	"""


#1101会员tom1购买商品11，使用积分抵扣最高：50元，订单金额：50元
	When tom1访问jobs的webapp
	When tom1获得jobs的100会员积分
	Then tom1在jobs的webapp中拥有100会员积分
	When tom1购买jobs的商品
		"""
		{
			"products": [{
				"integral_money":50.00,
				"integral":100.00,
				"name": "商品11",
				"count": 1
			}]
		}
		"""
	Then tom1成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 50.0,
			"product_price": 100.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"coupon_money":0.00,
			"integral_money":50.00,
			"integral":100.00,
			"products": [{
				"name": "商品11",
				"price": 100.0,
				"grade_discounted_money": 0.0,
				"count": 1
			}]
		}
		"""
		#	"members_money":0.00,
		#	"member_price":100.00,
	Then tom1在jobs的webapp中拥有0会员积分


#1102会员tom2购买商品11，使用积分抵扣最高：45元，订单金额：45元
	When tom2访问jobs的webapp
	When tom2获得jobs的200会员积分
	Then tom2在jobs的webapp中拥有200会员积分
	When tom2购买jobs的商品
		"""
		{
			"products": [{
				"integral_money":45.00,
				"integral":90.00,
				"name": "商品11",
				"count": 1
			}]
		}
		"""
	Then tom2成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 45.0,
			"product_price": 90.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":45.00,
			"integral":90.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品11",
				"price": 90.0,
				"grade_discounted_money": 10.0,
				"count": 1
			}]
		}
		"""
			#"member_price":90.00,
			#"members_money":10.00,
	Then tom2在jobs的webapp中拥有110会员积分

#1103会员tom4购买商品10+商品11，使用积分抵扣最高：35元，订单金额：105元
	When tom4访问jobs的webapp
	When tom4获得jobs的400会员积分
	Then tom4在jobs的webapp中拥有400会员积分
	When tom4购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品10",
				"count": 1
			},{
			    "name": "商品11",
				"count": 1,
				"integral_money":35.00,
				"integral":70.00
			}]
		}
		"""
	Then tom4成功创建订单
	"""
		{
			"status": "待支付",
			"final_price": 105.0,
			"product_price": 140.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":35.00,
			"integral":70.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品10",
				"price": 70.0,
				"grade_discounted_money": 30.0,
				"count": 1
			},{
				"name": "商品11",
				"price": 70.0,
				"grade_discounted_money": 30.0,
				"count": 1
			}]
		}
	"""
	#		"member_price":140.00,
	#		"members_money":60.00,
	Then bill在jobs的webapp中拥有330会员积分


Scenario: 9 不同等级的会员购买有会员价同时有根据等级设置积分抵扣的商品
 #会员价和积分抵扣可以同时使用，会员价后再算积分抵扣的比例

	Given bill1关注jobs的公众号
	And bill2关注jobs的公众号
	And bill3关注jobs的公众号
	And bill4关注jobs的公众号
	And jobs登录系统
	And jobs已添加商品
	"""
		[{
			"name": "商品12",
			"price": 100.00,
			"is_member_product": "on"
		}]
	"""

	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"discount": "7"
		}]
		"""
	When jobs更新"bill2"的会员等级
	"""
	{
		"name": "bill2",
		"member_rank": "铜牌会员"
	}
	"""
	When jobs更新"bill3"的会员等级
	"""
	{
		"name": "bill3",
		"member_rank": "银牌会员"
	}
	"""
	When jobs更新"bill4"的会员等级
	"""
	{
		"name": "bill4",
		"member_rank": "金牌会员"
	}
	"""
	Then jobs可以获得会员列表
	"""
	[{
		"name": "bill4",
		"member_rank": "金牌会员"
	}, {
		"name": "bill3",
		"member_rank": "银牌会员"
	}, {
		"name": "bill2",
		"member_rank": "铜牌会员"
	}, {
		"name": "bill1",
		"member_rank": "普通会员"
	}, {
		"name": "tom",
		"member_rank": "普通会员"
	}, {
		"name": "bill",
		"member_rank": "普通会员"
	}]
	"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品12积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品12",
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


#1201会员bill1购买商品12，使用积分抵扣最高：100元，订单金额：0元
	When bill1访问jobs的webapp
	When bill1获得jobs的200会员积分
	Then bill1在jobs的webapp中拥有200会员积分
	When bill1购买jobs的商品
		"""
		{
			"products": [{
				"integral_money":100.00,
				"integral":200.00,
				"name": "商品12",
				"count": 1
			}]
		}
		"""
	Then bill1成功创建订单
		"""
		{
			"status": "待发货",
			"final_price": 0.00,
			"product_price": 100.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"coupon_money":0.00,
			"integral_money":100.00,
			"integral":200.00,
			"products": [{
				"price": 100.0,
				"grade_discounted_money": 0.0,
				"name": "商品12",
				"count": 1
			}]
		}
		"""
		#	"member_price":100.00,
		#	"members_money":0.00,
	Then bill1在jobs的webapp中拥有0会员积分


#1202会员bill2购买商品12，使用积分抵扣最高：81元，订单金额：9元
	When bill2访问jobs的webapp
	When bill2获得jobs的300会员积分
	Then bill2在jobs的webapp中拥有300会员积分
	When bill2购买jobs的商品
		"""
		{
			"products": [{
				"integral_money":81.00,
				"integral":162.00,
				"name": "商品12",
				"count": 1
			}]
		}
		"""
	Then bill2成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 9.00,
			"product_price": 90.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"coupon_money":0.00,
			"integral_money":81.00,
			"integral":162.00,
			"products": [{
				"price": 90.0,
				"grade_discounted_money": 10.0,
				"name": "商品12",
				"count": 1
			}]
		}
		"""
	Then bill2在jobs的webapp中拥有138会员积分


#1203会员bill3购买商品12，使用积分抵扣最高：64元，订单金额：16元
	When bill3访问jobs的webapp
	When bill3获得jobs的400会员积分
	Then bill3在jobs的webapp中拥有400会员积分
	When bill3购买jobs的商品
		"""
		{
			"products": [{
				"integral_money":64.00,
				"integral":128.00,
				"name": "商品12",
				"count": 1
			}]
		}
		"""
	Then bill3成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 16.00,
			"product_price": 80.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"coupon_money":0.00,
			"integral_money":64.00,
			"integral":128.00,
			"products": [{
				"price": 80.0,
				"grade_discounted_money": 20.0,
				"name": "商品12",
				"count": 1
			}]
		}
		"""
		#	"member_price":80.00,
		#	"members_money":20.00,
	Then bill3在jobs的webapp中拥有272会员积分


 #1204会员bill4购买商品12，使用积分抵扣最高：49元，订单金额：21元
		When bill4访问jobs的webapp
		When bill4获得jobs的500会员积分
		Then bill4在jobs的webapp中拥有500会员积分
		When bill4购买jobs的商品
		"""
		{
			"products": [{
				"integral_money":49.00,
				"integral":98.00,
				"name": "商品12",
				"count": 1
			}]
		}
		"""
		Then bill4成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 21.00,
			"product_price": 70.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"coupon_money":0.00,
			"integral_money":49.00,
			"integral":98.00,
			"products": [{
				"price": 70.0,
				"grade_discounted_money": 30.0,
				"name": "商品12",
				"count": 1
			}]
		}
		"""
		#	"member_price":70.00,
		#	"members_money":30.00,
		Then bill4在jobs的webapp中拥有402会员积分


Scenario: 10 不同等级的会员购买原价同时有根据等级设置积分抵扣的商品

	Given bill1关注jobs的公众号
	And bill2关注jobs的公众号
	And bill3关注jobs的公众号
	And bill4关注jobs的公众号
	And jobs登录系统
	And jobs已添加商品
	"""
		[{
			"name": "商品13",
			"price": 100.00,
			"is_member_product": "no"
		}]
	"""

	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"discount": "9.8"
		}, {
			"name": "银牌会员",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"discount": "7"
		}]
		"""
	When jobs更新"bill2"的会员等级
	"""
	{
		"name": "bill2",
		"member_rank": "铜牌会员"
	}
	"""
	When jobs更新"bill3"的会员等级
	"""
	{
		"name": "bill3",
		"member_rank": "银牌会员"
	}
	"""
	When jobs更新"bill4"的会员等级
	"""
	{
		"name": "bill4",
		"member_rank": "金牌会员"
	}
	"""
	Then jobs可以获得会员列表
	"""
	[{
		"name": "bill4",
		"member_rank": "金牌会员"
	}, {
		"name": "bill3",
		"member_rank": "银牌会员"
	}, {
		"name": "bill2",
		"member_rank": "铜牌会员"
	}, {
		"name": "bill1",
		"member_rank": "普通会员"
	}, {
		"name": "tom",
		"member_rank": "普通会员"
	}, {
		"name": "bill",
		"member_rank": "普通会员"
	}]
	"""

	When jobs创建积分应用活动
		"""
		[{
			"name": "商品13积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品13",
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


#1301会员bill1购买商品13，使用积分抵扣最高：100元，订单金额：0元
	When bill1访问jobs的webapp
	When bill1获得jobs的200会员积分
	Then bill1在jobs的webapp中拥有200会员积分
	When bill1购买jobs的商品
		"""
		{
			"products": [{
				"integral_money":100.00,
				"integral":200.00,
				"name": "商品13",
				"count": 1
			}]
		}
		"""
	Then bill1成功创建订单
		"""
		{
			"status": "待发货",
			"final_price": 0.00,
			"product_price": 100.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":100.00,
			"integral":200.00,
			"coupon_money":0.00,
			"products": [{
				"price": 100.0,
				"grade_discounted_money": 0.0,
				"name": "商品13",
				"count": 1
			}]
		}
		"""
		#	"member_price":100.00,
		#	"members_money":0.00,
	Then bill1在jobs的webapp中拥有0会员积分

#1302会员bill2购买商品13，使用积分抵扣最高：90元，订单金额：10元
	When bill2访问jobs的webapp
	When bill2获得jobs的300会员积分
	Then bill2在jobs的webapp中拥有300会员积分
	When bill2购买jobs的商品
		"""
		{
			"products": [{
				"integral_money":90.00,
				"integral":180.00,
				"name": "商品13",
				"count": 1
			}]
		}
		"""
	Then bill2成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 10.00,
			"product_price": 100.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":90.00,
			"integral":180.00,
			"coupon_money":0.00,
			"products": [{
				"price": 100.0,
				"grade_discounted_money": 0.0,
				"name": "商品13",
				"count": 1
			}]
		}
		"""
		#	"member_price":100.00,
		#	"members_money":0.00,
	Then bill2在jobs的webapp中拥有120会员积分

#1303会员bill3购买商品13，使用积分抵扣最高：80元，订单金额：20元
	When bill3访问jobs的webapp
	When bill3获得jobs的400会员积分
	Then bill3在jobs的webapp中拥有400会员积分
	When bill3购买jobs的商品
		"""
		{
			"products": [{
				"integral_money":80.00,
				"integral":160.00,
				"name": "商品13",
				"count": 1
			}]
		}
		"""
	Then bill3成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 20.00,
			"product_price": 100.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":80.00,
			"integral":160.00,
			"coupon_money":0.00,
			"products": [{
				"price": 100.0,
				"grade_discounted_money": 0.0,
				"name": "商品13",
				"count": 1
			}]
		}
		"""
		#	"member_price":100.00,
		#	"members_money":0.00,
	Then bill3在jobs的webapp中拥有240会员积分

#1304会员bill4购买商品13，使用积分抵扣最高：70元，订单金额：30元
	When bill4访问jobs的webapp
	When bill4获得jobs的500会员积分
	Then bill4在jobs的webapp中拥有500会员积分
	When bill4购买jobs的商品
		"""
		{
			"products": [{
				"integral_money":70.00,
				"integral":140.00,
				"name": "商品13",
				"count": 1
			}]
		}
		"""
	Then bill4成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 30.00,
			"product_price": 100.00,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":70.00,
			"integral":140.00,
			"coupon_money":0.00,
			"products": [{
				"price": 100.0,
				"grade_discounted_money": 0.0,
				"name": "商品13",
				"count": 1
			}]
		}
		"""
		#	"member_price":100.00,
		#	"members_money":0.00,
	Then bill4在jobs的webapp中拥有360会员积分

Scenario: 11使用积分后不能使用优惠券
	bill购买jobs的商品时，使用积分时，优惠券状态变为不可用状态
	使用优惠券时，积分状态变为不可用状态
	When jobs已添加了优惠券规则
	"""
		[{
			"name": "优惠券1",
			"money": 1,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
	"""
	When bill领取jobs的优惠券
	"""
		[{
			"name": "优惠券1",
			"coupon_ids": ["coupon1_id_2", "coupon1_id_1"]
		}]
	"""
	When bill访问jobs的webapp
	When bill获得jobs的75会员积分
	Then bill在jobs的webapp中拥有75会员积分
	When bill访问jobs的webapp:ui
	When bill使用'积分'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}],
			"use_integral": true
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"cover": "下单成功",
			"price_info": {
				"integral_count": 75,
				"integral_money": 25
			}
		}
		"""
	And bill优惠券状态变为"不可选"
	And bill在jobs的webapp中拥有0会员积分:ui
	When bill使用'优惠券'购买jobs的商品
	"""
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}],
			"use_integral": false,
			"coupon_type": "选择",
			"coupon": "coupon1_id_1"
		}
	"""
	Then bill获得支付结果
	"""
		{
			"status": "待发货",
			"cover": "下单成功",
		}
	"""
	And bill积分状态变为"不可选"
	And bill在jobs的webapp众拥有0会员积分

