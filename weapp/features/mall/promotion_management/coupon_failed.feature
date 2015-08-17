# __author__ : "师帅"
# __edite__ : "benchi"

Feature: 优惠券与促销活动互斥问题
"""
	1.给商品1建单品券，并发送给jobs，jobs领取后，使单品券失效（但是单品券没有过有效期，仍可使用）
	2.给商品1建促销活动
	错误值：在订单页商品1参加了促销活动，也可以使用单品券
	期望值（正确值）：该商品如果是先建立的单品优惠劵，则不能参加促销活动
					  该商品如果是先建立的促销活动，则不能建立该商品的单品优惠劵

"""

Background:
	Given jobs登录系统
	And jobs已添加商品
	"""
		[{
			"name": "商品1",
			"stock_type": "无限",
			"price": 200.00
		}, {
			"name": "商品2",
			"stock_type": "无限",
			"price": 200.00
		}, {
			"name": "商品3",
			"stock_type": "无限",
			"price": 200.00
		}]
	"""

@wip.cp1
Scenario: 1先建优惠券，不能参加促销活动
	When jobs添加优惠券规则
	"""
		[{
			"name": "优惠券4",
			"money": 10.00,
			"count": 5,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon4_id_",
			"coupon_product": "商品2"
		}]
	"""
	Then jobs能获得优惠券规则列表
	"""
		[{
			"name": "优惠券4",
			"type": "单品券",
			"money": 10.00,
			"remained_count": 5,
			"limit_counts": 1,
			"use_count": 0,
			"start_date": "今天",
			"end_date": "2天后"
		}]
	"""
	When jobs创建限时抢购活动
	Then jobs能获取商品列表
	"""
		[{
			"name": "商品1",
			"stock_type": "无限",
			"operate": True,
			"price": 200.00
		}, {
			"name": "商品2",
			"stock_type": "无限",
			"operate": False,
			"price": 200.00
		}, {
			"name": "商品3",
			"stock_type": "无限",
			"operate": True,
			"price": 200.00
		}]
	"""

Scenario: 2先建立促销活动，不能建立该商品的单品券
	When jobs创建限时抢购活动
	"""
		[{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"member_grade": "全部",
			"count_per_purchase": 2,
			"promotion_price": 11.5
		}]
	"""
	Then jobs能获取限时抢购活动列表
	"""
		[{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"price": 200,
			"promotion_price": 11.5
		}]
	"""
	When jobs添加单品优惠券规则
	Then jobs能获取商品列表
	"""
		[{
			"name": "商品1",
			"stock_type": "无限",
			"operate": False,
			"price": 200.00
		}, {
			"name": "商品2",
			"stock_type": "无限",
			"operate": True,
			"price": 200.00
		}, {
			"name": "商品3",
			"stock_type": "无限",
			"operate": True,
			"price": 200.00
		}]
	"""
