# __author__ : "冯雪静"
Feature: 添加优惠券规则
	Jobs能通过管理系统添加"优惠券规则"

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[ {
			"name": "商品1",
			"price": 200.00
		},{
			"name": "商品2",
			"price": 200.00
		}]
		"""

@mall2 @market_tool.coupon @market_tool @eugene
Scenario: 添加优惠券规则
	jobs添加多个"优惠券规则"后
	1. jobs能获得添加的优惠券规则
	2. 优惠券规则列表按添加的顺序倒序排列
	3. bill不能获得jobs添加的优惠券规则

	#优惠券规则包含全店优惠券和单品券
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "优惠券2",
			"money": 1.00,
			"count": 5,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品1"
		}, {
			"name": "优惠券3",
			"money": 1.00,
			"count": 5,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
		}, {
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
		'''
		[{
			"name": "优惠券4",
			"type": "单品券",
			"money": 10.00,
			"remained_count": 5,
			"limit_counts": 1,
			"use_count": 0,
			"start_date": "今天",
			"end_date": "2天后"
		}, {
			"name": "优惠券3",
			"type": "全店通用券",
			"money": 1.00,
			"remained_count": 5,
			"limit_counts": 1,
			"use_count": 0,
			"start_date": "今天",
			"end_date": "2天后"
		}, {
			"name": "优惠券2",
			"type": "单品券",
			"money": 1.00,
			"remained_count": 5,
			"limit_counts": 1,
			"use_count": 0,
			"start_date": "今天",
			"end_date": "1天后"
		}, {
			"name": "优惠券1",
			"type": "全店通用券",
			"money": 100.00,
			"remained_count": 5,
			"limit_counts": 1,
			"use_count": 0,
			"start_date": "今天",
			"end_date": "1天后"
		}]
		'''
	Given bill登录系统
	Then bill能获得优惠券规则列表
		'''
		[]
		'''