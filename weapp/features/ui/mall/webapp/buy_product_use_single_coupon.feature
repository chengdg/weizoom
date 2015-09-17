# __editor__ : "新新8.27"

Feature: 在webapp中使用优惠券购买商品(单品券)
"""
	bill能在webapp中使用优惠券购买jobs添加的"商品"
	该feature中需要修改和补充,涉及到场景如下
	#领取的优惠券在使用期限内按照优惠券的规则，满足规则可以使用，直接抵扣现金，不能抵扣运费
	#后台发放后,全体优惠券显示使用期限,使用范围为全店通用券,使用条件,金额,优惠券名称
	#后台发放后,单品优惠券显示使用期限,使用范围为单品券,使用条件,金额,优惠券名称
	1.购买商品时,有可用优惠券时,在订单页显示优惠券"*张可用";
	2.购买商品时,无可用优惠券时,在订单页显示优惠券"无可用";
	3.购买商品时,选择使用优惠券后,显示"已抵用*元"
	#点击取消使用后,更新优惠券"*张可用"或者"无可用"
	4.购买商品时,使用积分抵扣时,不显示优惠券项
	#与积分抵扣互斥,切换使用优惠券
	5.使用单品优惠劵进行购买(选择优惠券)，该单品券适用于商品1，如果商品2使用(用优惠券码)，不显示该优惠券,提示
	6.使用单品优惠劵进行购买，该单品券适用于商品3并且商品3满50元才可以使用，而不是订单满50可用
	#购买商品时,使用全店优惠券,满足使用条件与使用期限,即可使用并且显示该优惠券可用列表中,否则显示不可用列表中
	#该商品金额小于该优惠券时,使用优惠券后,抵扣金额为"-该商品金额"
	#购买商品时,不可使用已过期优惠券并且显示在不可用列表中
	7.购买多规格商品，买1个商品的两个规格，总价格满足优惠劵使用条件
	8.使用多于商品价格的单品券进行购买，该单品券只适用于商品6
	9.不同等级的会员购买有会员价同时有单品券的商品
	#选择单品券，商品价格变回原价，取消使用单品券，价格变回会员价，和有会员价的商品同时购买，不影响其他会员价的商品
	10.选择优惠券购买,订单经过处理处于"已取消"状态后，订单中的优惠券回复到"未使用"状态,并在未使用列表中
	11.使用优惠券码购买,订单经过处理处于"退款完成"状态后，订单中的优惠券回复到"未使用"状态,并在未使用列表中
	#优惠码使用规则在相关feature中已写
	#优惠券活动在设置的活动期间内手动结束活动之后，已经领用的优惠券仍然可以使用(优惠券码可以使用),未领用的优惠券不能再领用，优惠码不能再使用
	#输入错误的优惠码，提示"请输入正确的优惠码"	
	#输入已失效的优惠码，提示"该优惠券已失效"
	
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
	#商品6是新加的
	And jobs已添加商品
		"""
		[ {
			"name": "商品1",
			"price": 200.00
		},{
			"name": "商品2",
			"price": 200.00
		},{
			"name": "商品3",
			"price": 20.00
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
		}, {
			"name": "商品6",
			"price": 20.00,
			"weight": 1,
			"postage": 10.00
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
	#优惠券6是新加的
	Given jobs已添加了优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 1,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "商品1"
		}, {
			"name": "优惠券2",
			"money": 10,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品3"
		}, {
			"name": "优惠券5",
			"money": 10,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon5_id_",
			"coupon_product": "商品5"
		}, {
			"name": "优惠券6",
			"money": 100,
			"start_date": "今天",
			"end_date": "2天后",
			"coupon_id_prefix": "coupon6_id_",
			"coupon_product": "商品6"
		}]
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill领取jobs的优惠券
		"""
		[{
			"name": "优惠券1",
			"coupon_ids": ["coupon1_id_2", "coupon1_id_1"]
		},{
			"name": "优惠券2",
			"coupon_ids": ["coupon2_id_2", "coupon2_id_1"]
		}, {
			"name": "优惠券5",
			"coupon_ids": ["coupon5_id_2", "coupon5_id_1"]
		}]
		"""
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom领取jobs的优惠券
		"""
		[{
			"name": "优惠券1",
			"coupon_ids": ["coupon1_id_4", "coupon1_id_3"]
		}, {
			"name": "优惠券6",
			"coupon_ids": ["coupon6_id_2", "coupon6_id_1"]
		}]
		"""
	And jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2
		}
		"""

Scenario: 1 购买商品时,有可用优惠券时,在订单页显示优惠券"*张可用"
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""
	When bill访问jobs的webapp
	#第一次使用 购买商品1，成功
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	Then bill提示"优惠券2张可用":ui


Scenario: 2 购买商品时,无可用优惠券时,在订单页显示优惠券"无可用"
	#商品2没有设置单品券
	When bill访问jobs的webapp
	#第一次使用 购买商品2，提示无可用
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品2",
				"count": 1
			}]
		}
		"""
	Then bill提示"优惠券无可用":ui


Scenario: 3 购买商品时,选择使用优惠券后,显示"已抵用*元"
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""
	When bill访问jobs的webapp
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	Then bill提示"优惠券2张可用":ui
	#购买商品1，选择优惠券后,显示已抵用*元
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon1_id_1"
		}
		"""
	Then bill提示"优惠券已抵用1元":ui
	#点击取消使用后,更新优惠券"*张可用"或者"无可用"
	When bill点击取消使用:ui
	Then bill提示"优惠券2张可用":ui

Scenario: 4 购买商品时,使用积分抵扣时,不显示优惠券项
	#两者互斥
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""
	When bill获得jobs的50会员积分
	Then bill在jobs的webapp中拥有50会员积分
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
				"discount": 50,
				"discount_money": 100.0
			}]
		}]
		"""
	When bill访问jobs的webapp
	#第一次使用 购买商品1，成功
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	Then bill提示优惠券可用:ui
	Then bill提示积分可抵扣:ui
	When bill勾选积分可抵扣:ui
	Then bill优惠券消失:ui
	When bill取消勾选积分可抵扣:ui
	Then bill优惠券显示:ui
	When bill选择可使用优惠券:ui
	Then bill可抵扣积分消失:ui
	When bill取消选择可使用优惠券:ui
	Then bill可抵扣积分显示:ui

Scenario: 5 使用单品优惠劵进行购买(选择优惠券)，该单品券适用于商品1，如果商品2使用(用优惠券码)，则提示

	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""
	When bill访问jobs的webapp
	#第一次使用 购买商品1，成功
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon1_id_1"
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 199.0,
			"product_price": 200.0,
			"coupon_money": 1.0,
			"promotion_saved_money": 0.0,
			"postage": 0.00,
			"integral_money":0.00
		}
		"""
	#第二次使用 购买商品2(使用优惠码)提示
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品2",
				"count": 1
			}],
			"coupon": "coupon1_id_2"
		}
		"""
	Then bill获得创建订单失败的信息'该优惠券不能购买订单中的商品':ui
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""

Scenario: 6 使用单品优惠劵进行购买，该单品券适用于商品3并且商品3满50元才可以使用，而不是订单满50可用
		1 买3件商品3，共60元，满足条件，可用单品劵；
		2 买1件商品3，买一件商品2，订单满50，但单品不满50，不可以使用该单品卷
	
		Given jobs登录系统
		Then jobs能获得优惠券'优惠券2'的码库
			"""
			{
				"coupon2_id_1": {
					"money": 10.0,
					"status": "未使用",
					"consumer": "",
					"target": "bill"
				},
				"coupon2_id_2": {
					"money": 10.0,
					"status": "未使用",
					"consumer": "",
					"target": "bill"
				}
			}
			"""
		When bill访问jobs的webapp
		#第一次使用 购买3个商品3，满足使用条件，成功
		When bill购买jobs的商品
			"""
			{
				"products": [{
					"name": "商品3",
					"count": 3
				}],
				"coupon": "coupon2_id_1"
			}
			"""
		Then bill成功创建订单
			"""
			{
				"status": "待支付",
				"final_price": 50.0,
				"product_price": 60.0,
				"coupon_money": 10.0,
				"promotion_saved_money": 0.0,
				"postage": 0.00,
				"integral_money":0.00
			}
			"""
		#第二次使用 购买商品3+商品2 订单购买失败,使用优惠码
		When bill购买jobs的商品:ui
			"""
			{
				"products": [{
					"name": "商品3",
					"count": 1
				},{
					"name": "商品2",
					"count": 1
				}],
				"coupon": "coupon2_id_2"
			}
			"""
		Then bill获得创建订单失败的信息'该优惠券指定商品金额不满足使用条件':ui
		Given jobs登录系统
		Then jobs能获得优惠券'优惠券2'的码库
			"""
			{
				"coupon2_id_1": {
					"money": 10.0,
					"status": "已使用",
					"consumer": "bill",
					"target": "bill"
				},
				"coupon2_id_2": {
					"money": 10.0,
					"status": "未使用",
					"consumer": "",
					"target": "bill"
				}
			}
			"""

Scenario: 7 购买多规格商品，买1个商品的两个规格，总价格满足优惠劵使用条件
	
	
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券5'的码库
		"""
		{
			"coupon5_id_1": {
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""
	When bill访问jobs的webapp
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品5",
				"count": 1,
				"model": "M"
			},{
				"name": "商品5",
				"count": 1,
				"model": "S"
			}],
			"coupon": "coupon5_id_1"
		}
		"""
	Then bill成功创建订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 70.0,
			"product_price": 80.0,
			"coupon_money": 10.0
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券5'的码库
		"""
		{
			"coupon5_id_1": {
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			}
		}
		"""


Scenario: 8 使用多于商品价格的单品券进行购买，该单品券只适用于商品6
	且不抵扣其他商品金额和运费金额

	Given jobs登录系统
	Then jobs能获得优惠券'优惠券6'的码库
		"""
		{
			"coupon6_id_1": {
				"money": 100.0,
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			},
			"coupon6_id_2": {
				"money": 100.0,
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			}
		}
		"""
	When tom访问jobs的webapp
	When tom购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品3",
				"count": 1
			},{
				"name": "商品6",
				"count": 1
			}],
			"coupon": "coupon6_id_1"
		}
		"""
	Then tom成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 30.0,
			"product_price": 40.0,
			"postage": 10.00,
			"coupon_money": 20.0
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券6'的码库
		"""
		{
			"coupon6_id_1": {
				"status": "已使用",
				"consumer": "tom",
				"target": "tom"
			}
		}
		"""


Scenario: 9 不同等级的会员购买有会员价同时有单品券的商品
	1. 单品券和会员价不能同时使用
	2. 选择单品券，商品价格变回原价，取消使用单品券，价格变回会员价
	3. 和有会员价的商品同时购买，不影响其他会员价的商品

	Given jobs登录系统
	When jobs添加会员等级
		"""
		[{
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
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	When jobs更新"bill"的会员等级
		"""
		{
			"name": "bill",
			"member_rank": "金牌会员"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "普通会员"
		}, {
			"name": "bill",
			"member_rank": "金牌会员"
		}]
		"""
	When jobs更新商品'商品1'
		"""
		{
			"name": "商品1",
			"price": 200.00,
			"is_member_product": "on"
		}
		"""
	Then jobs能获取商品'商品1'
		"""
		{
			"name": "商品1",
			"is_member_product": "on"
		}
		"""
	When jobs更新商品'商品2'
		"""
		{
			"name": "商品2",
			"price": 200.00,
			"is_member_product": "on"
		}
		"""
	Then jobs能获取商品'商品2'
		"""
		{
			"name": "商品2",
			"is_member_product": "on"
		}
		"""
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""
	When bill访问jobs的webapp
	#使用单品券，商品金额就是原价
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon1_id_1"
		}
		"""
	Then bill成功创建订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 199.0,
			"product_price": 200.0,
			"coupon_money": 1.0,
			"promotion_saved_money": 0.0,
			"postage": 0.00,
			"integral_money":0.00,
			"products": [{
				"name": "商品1",
				"price": 200.0,
				"count": 1
			}]
		}
		"""
	#用会员价购买商品，就不能使用单品券
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 140.0,
			"product_price": 140.0,
			"coupon_money": 0.0,
			"promotion_saved_money": 0.0,
			"integral_money":0.00,
			"products": [{
				"name": "商品1",
				"price": 140.0,
				"count": 1
			}]
		}
		"""
	#购买多种会员价的商品，使用单品券，不影响其他会员价商品
	When bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品2",
			"count": 1
		}]
		"""
	Then bill能获得购物车
		"""
		{
			"product_groups": [{
				"products": [{
					"name": "商品1",
					"price": 140.00,
					"count": 1
				}, {
					"name": "商品2",
					"price": 140.00,
					"count": 1
				}]
			}],
			"invalid_products": []
		}
		"""
	When bill从购物车发起购买操作:ui
		"""
		{
			"action": "pay",
			"context": [{
				"name": "商品1"
			}, {
				"name": "商品2"
			}],
			"coupon": "coupon1_id_2"
		}
		"""
	And bill填写收货信息
	"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
	"""
	And bill在购物车订单编辑中点击提交订单
	"""
	{
		"pay_type": "微信付款"
	}
	"""
	Then bill成功创建订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 339.00,
			"product_price": 340.0,
			"coupon_money": 1.0,
			"promotion_saved_money": 0.0,
			"postage": 0.00,
			"integral_money":0.00,
			"products": [{
				"name": "商品1",
				"price": 200.00,
				"count": 1
			}, {
				"name": "商品2",
				"price": 140.00,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			}
		}
		"""

Scenario: 10 选择优惠券购买,订单经过处理处于"已取消"状态后，订单中的优惠券回复到"未使用"状态,并在未使用列表中

	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""
	When bill访问jobs的webapp
	#购买
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon1_id_1"
		}
		"""
	Then bill成功创建订单:ui
		"""
		{
			"order_no": "001",
			"status": "待支付",
			"final_price": 199.0,
			"product_price": 200.0,
			"coupon_money": 1.0,
			"promotion_saved_money": 0.0,
			"postage": 0.00,
			"integral_money":0.00
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""
	#取消订单
	When bill访问jobs的webapp
	When bill取消订单'001':ui
	Then bill购买jobs的商品:ui
	#未使用列表中仍可重新使用该优惠券
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon1_id_1"
		}
		"""
	Then bill成功创建订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 199.0,
			"product_price": 200.0,
			"coupon_money": 1.0,
			"promotion_saved_money": 0.0,
			"postage": 0.00,
			"integral_money":0.00
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""

Scenario: 11 使用优惠券码购买,订单经过处理处于"退款完成"状态后，订单中的优惠券回复到"未使用"状态,并在未使用列表中
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""
		#购买
	When bill访问jobs的webapp
	When bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品2",
				"count": 1
			}],
			"coupon": "coupon1_id_2"
		}
		"""
	Then bill成功创建订单:ui
		"""
		{
			"order_no": "001",
			"status": "待支付",
			"final_price": 199.0,
			"product_price": 200.0,
			"coupon_money": 1.0,
			"promotion_saved_money": 0.0,
			"postage": 0.00,
			"integral_money":0.00
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			}
		}
		"""
		#退款
	When bill访问jobs的webapp
	When bill申请退款'001':ui
	Then bill退款完成'001':ui
	Then bill购买jobs的商品:ui
	#未使用列表中仍可重新使用该优惠券
		"""
		{
			"products": [{
				"name": "商品2",
				"count": 1
			}],
			"coupon": "coupon1_id_2"
		}
		"""
	Then bill成功创建订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 199.0,
			"product_price": 200.0,
			"coupon_money": 1.0,
			"promotion_saved_money": 0.0,
			"postage": 0.00,
			"integral_money":0.00
		}
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.0,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			}
		}
		"""