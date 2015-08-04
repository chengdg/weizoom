# __edit__ : "benchi"
Feature: 在webapp中购买参与限时抢购活动的商品
	用户能在webapp中购买"参与限时抢购活动的商品"

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
			"price": 100.00,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}, {
			"name": "商品2",
			"price": 200.00
		}, {
			"name": "商品3",
			"price": 50.00
		}, {
			"name": "商品4",
			"model": {
				"models": {
					"standard": {
						"price": 40.00,
						"stock_type": "有限",
						"stocks": 20
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
	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"member_grade_name_name": "全部",
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}, {
			"name": "商品2限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品2"],
			"member_grade_name_name": "全部",
			"promotion_price": 2.1,
			"limit_period": 1
		}, {
			"name": "商品3限时抢购",
			"start_date": "2天前",
			"end_date": "1天前",
			"products": ["商品3"],
			"member_grade_name_name": "全部",
			"promotion_price": 3.1
		}]
		"""
	Given bill关注jobs的公众号
	And tom关注jobs的公众号
	And sam关注jobs的公众号
	Then jobs可以获得会员列表
	"""
		[{
			"name": "bill",
			"member_rank": "普通会员"
		}, {
			"name": "tom",
			"member_rank": "铜牌会员"
		}, {
			"name": "sam",
			"member_rank": "银牌会员"
		}]
	"""
	#会员等级
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"shop_discount": "90%"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"shop_discount": "80%"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "70%"
		}]
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"shop_discount": "100%"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"shop_discount": "90%"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"shop_discount": "80%"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "70%"
		}]
		"""


@mall2 @mall.promotion @mall.webapp.promotion
Scenario: 1 购买单个限时抢购商品，限时抢购进行中
	没有设置限购周期，可以连续购买

	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 23.00,
			"product_price": 23.00,
			"promotion_saved_money": 177.0,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 2,
				"promotion": {
					"promotioned_product_price": 11.5,
					"type": "flash_sale"
				}
			}]
		}
		"""
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
			"status": "待支付",
			"final_price": 11.5
		}
		"""

@mall2 @mall.promotion @mall.webapp.promotion @zy_fs02
Scenario:2 购买单个限时抢购商品，限时抢购已过期（在购物车中是限时抢购商品，但，去提交订单时已经不是限时抢购商品）

	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品3",
				"count": 1
			}]
		}
		"""
	Then bill获得创建订单失败的信息
		"""
		{
			"detail": [{
				"id": "商品3",
				"msg": "该活动已经过期",
				"short_msg": "已经过期"
			}]
		}
		"""

@mall2 @mall.promotion @mall.webapp.promotion @zy_fs03
Scenario:3 购买单个限时抢购商品，限时抢购活动没开始，按原价下单

	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
		{
			"name": "商品4限时抢购",
			"start_date": "1天后",
			"end_date": "3天后",
			"products": ["商品4"],
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}
		"""
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 80.0
		}
		"""


@mall2 @mall.promotion @mall.webapp.promotion @zy_fs04
Scenario: 4 购买多个商品，带有限时抢购商品

	When bill访问jobs的webapp
	When bill购买jobs的商品
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
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 65.1,
			"product_price": 65.1,
			"promotion_saved_money": 374.9,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 2,
				"promotion": {
					"promotioned_product_price": 11.5,
					"type": "flash_sale"
				}
			}, {
				"name": "商品2",
				"count": 1,
				"promotion": {
					"promotioned_product_price": 2.1,
					"type": "flash_sale"
				}
			}, {
				"name": "商品4",
				"count": 1,
				"price": 40.0,
				"promotion": null
			}]
		}
		"""


@mall2 @mall.promotion @mall.webapp.promotion @zy_fs05
Scenario: 5 购买单个限时抢购商品，超出库存限制
	第一次购买2个，成功；第二次购买2个，超出商品库存，确保缓存更新

	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 23.0
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

@mall2 @mall.promotion @mall.webapp.promotion @zy_fs06
Scenario: 6  购买单个限时抢购商品，未超过库存限制，但超过单次购买限制

	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
		{
			"name": "商品4限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品4"],
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}
		"""
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 23.0
		}
		"""
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 3
			}]
		}
		"""
	Then bill获得创建订单失败的信息'限购2件'


@mall2 @mall.promotion @mall.webapp.promotion @zy_fs07
Scenario: 7 在限购周期内连续购买限时抢购商品

	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品2",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 2.1
		}
		"""
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品2",
				"count": 1
			}]
		}
		"""
		Then bill获得创建订单失败的信息
		"""
		{
			"detail": [{
				"id": "商品2",
				"msg": "在限购周期内不能多次购买",
				"short_msg": "限制购买"
			}]
		}
		"""

@mall2 @mall.promotion @mall.webapp.promotion @zy_fs08
Scenario: 8 购买多规格限时抢购商品
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
		{
			"name": "商品5限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品5"],
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}
		"""
	When bill访问jobs的webapp
	When bill购买jobs的商品
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
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 23.0
		}
		"""
	When bill购买jobs的商品
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
	Then bill获得创建订单失败的信息'限购2件'

@mall2 @mall.promotion @mall.webapp.promotion @zy_fs09
Scenario: 9 购买多规格限时抢购商品同时适用于积分规则

	Given jobs登录系统
	And jobs设定会员积分策略
		"""
		{
			"一元等价的积分数量": 2,
			"订单积分抵扣上限": 50
		}
		"""


	When jobs创建限时抢购活动
		"""
		{
			"name": "商品5限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品5"],
			"count_per_purchase": 2,
			"promotion_price": 10
		}
		"""
	When bill访问jobs的webapp
	When bill获得jobs的50会员积分
	Then bill在jobs的webapp中拥有50会员积分
	When bill购买jobs的商品
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
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 10.0,
			"product_price": 20.00,
			"promotion_saved_money":60.00,
			"postage": 0.00,
			"integral_money":10.00,
			"integral":20.00,
			"coupon_money":0.00,
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
	Then bill在jobs的webapp中拥有30会员积分

@mall2 @mall.promotion @mall.webapp.promotion @zy_fs10
Scenario: 10 购买单个限时抢购商品，购买时活动进行中，提交订单时，该活动被商家手工结束

	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
		{
			"name": "商品4限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品4"],
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}
		"""
	And jobs结束促销活动'商品4限时抢购'

	When bill访问jobs的webapp
	And bill购买jobs的商品
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

	Then bill获得创建订单失败的信息
		"""
		{
			"detail": [{
				"id": "商品4",
				"msg": "该活动已经过期",
				"short_msg": "已经过期"
			}]
		}
		"""


# 后续补充.雪静
@zy_fs11 @mall2 @mall.promotion @mall.webapp.promotion
Scenario: 11 购买单个限时抢购商品，未支付然后取消订单，还可以再次下单
	有限购周期和限购数量设置

	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
		{
			"name": "商品4限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品4"],
			"count_per_purchase": 2,
			"promotion_price": 11.5,
			"limit_period": 1
		}
		"""
	When bill访问jobs的webapp
	And bill购买jobs的商品
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
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 11.5
		}
		"""
	Given jobs登录系统
	Then jobs可以获得最新订单详情
		"""
		{
			"status": "待支付",
			"final_price": 11.5,
			"actions": ["取消", "支付","修改价格"]
		}
		"""
	When jobs'取消'最新订单
		"""
		 {
		 	"reason": "不想要了"
		 }
		"""
	Then jobs可以获得最新订单详情
		"""
		{
			"status": "已取消",
			"final_price": 11.5,
			"actions": []
		}
		"""
	When bill访问jobs的webapp
	And bill购买jobs的商品
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
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 23.00
		}
		"""
	Given jobs登录系统
	Then jobs可以获得最新订单详情
		"""
		{
			"status": "待支付",
			"final_price": 23.00,
			"actions": ["取消", "支付","修改价格"]
		}
		"""


#后续补充会员等级价.师帅
Scenario:12 不同等级的会员购买有会员价同时有限时抢购的商品（限时抢购优先于会员价）
	When jobs修改"商品1"
	"""
		[{
			"name": "商品1",
			"price": 100.00,
			"member_price": "True",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 30
					}
				}
			}
		}]
	"""
	And jobs创建限时抢购活动
	"""
		[{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"member_grade_name": "全部",
			"promotion_price": 11.5
		}]
	"""
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 23.00,
			"product_price": 23.00,
			"promotion_saved_money": 177.0,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 2,
				"promotion": {
					"promotioned_product_price": 11.5,
					"type": "flash_sale"
				}
			}]
		}
		"""
	When tom购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then tom成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 23.00,
			"product_price": 23.00,
			"promotion_saved_money": 177.0,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 2,
				"promotion": {
					"promotioned_product_price": 11.5,
					"type": "flash_sale"
				}
			}]
		}
		"""

Scenario:13 不同等级的会员购买有会员价同时有会员等级限时抢购的商品（限时抢购优先于会员价）
	When jobs修改"商品1"
	"""
		[{
			"name": "商品1",
			"price": 100.00,
			"member_price": "True",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 30
					}
				}
			}
		}]
	"""
	And jobs创建限时抢购活动
	"""
		[{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"member_grade_name": "银牌",
			"promotion_price": 50.0
		}]
	"""
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 200.0,
			"product_price": 200.0,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 2,
				"promotion": {
					"promotioned_product_price": 100.0,
					"type": "flash_sale"
				}
			}]
		}
		"""
	When tom购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then tom成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 180.0,
			"product_price": 180.0,
			"promotion_saved_money": 20.0,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 2,
				"promotion": {
					"promotioned_product_price": 100,
					"type": "flash_sale"
				}
			}]
		}
		"""
	When sam购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then sam成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 100.0,
			"product_price": 100.0,
			"promotion_saved_money": 100.0,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 2,
				"promotion": {
					"promotioned_product_price": 100,
					"type": "flash_sale"
				}
			}]
		}
		"""

Scenario: 14 不同等级的会员购买原价有会员等级限时抢购的商品
	When jobs修改"商品1"
	"""
		[{
			"name": "商品1",
			"price": 100.00,
			"member_price": "False",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 30
					}
				}
			}
		}]
	"""
	And jobs创建限时抢购活动
	"""
		[{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"member_grade_name": "银牌",
			"promotion_price": 50.0
		}]
	"""
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 200.0,
			"product_price": 200.0,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 2,
				"promotion": {
					"promotioned_product_price": 100.0,
					"type": "flash_sale"
				}
			}]
		}
		"""
	When tom购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then tom成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 200.0,
			"product_price": 200.0,
			"promotion_saved_money": 0.00,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 2,
				"promotion": {
					"promotioned_product_price": 100,
					"type": "flash_sale"
				}
			}]
		}
		"""
	When sam购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then sam成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 100.0,
			"product_price": 100.0,
			"promotion_saved_money": 100.0,
			"postage": 0.00,
			"integral_money":0.00,
			"coupon_money":0.00,
			"products": [{
				"name": "商品1",
				"count": 2,
				"promotion": {
					"promotioned_product_price": 100,
					"type": "flash_sale"
				}
			}]
		}
		"""


Scenario: 15 购买多规格限时抢购商品同时适用于积分规则和会员等级

	Given jobs登录系统
	And jobs设定会员积分策略
		"""
		{
			"一元等价的积分数量": 2,
			"订单积分抵扣上限": 50
		}
		"""


	When jobs创建限时抢购活动
		"""
		{
			"name": "商品5限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品5"],
			"member_grade_name": "银牌",
			"promotion_price": 10
		}
		"""
	When bill访问jobs的webapp
	When bill获得jobs的100会员积分
	Then bill在jobs的webapp中拥有100会员积分
	When tom获得jobs的100会员积分
	Then tom在jobs的webapp中拥有100会员积分
	When sam获得jobs的100会员积分
	Then sam在jobs的webapp中拥有100会员积分
	When bill购买jobs的商品
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
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 40.00,
			"product_price": 80.00,
			"promotion_saved_money":0.00,
			"postage": 0.00,
			"integral_money":40.00,
			"integral":80.00,
			"coupon_money":0.00,
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
	Then bill在jobs的webapp中拥有20会员积分
	When tom购买jobs的商品
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
	Then tom成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 36.00,
			"product_price": 72.00,
			"promotion_saved_money":0.00,
			"postage": 0.00,
			"integral_money":40.00,
			"integral":72.00,
			"coupon_money":0.00,
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
	Then tom在jobs的webapp中拥有28会员积分
	When sam购买jobs的商品
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
	Then sam成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 10.00,
			"product_price": 20.00,
			"promotion_saved_money":0.00,
			"postage": 0.00,
			"integral_money":40.00,
			"integral":20.00,
			"coupon_money":0.00,
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
	Then sam在jobs的webapp中拥有80会员积分
