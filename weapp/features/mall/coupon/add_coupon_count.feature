# __author__ : "冯雪静"
Feature: 优惠券添加库存
	Jobs能通过管理系统添加"优惠券库存"

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[ {
			"name": "商品1",
			"price": 200.00
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "全体券1",
			"money": 1.00,
			"limit_counts": 10,
			"start_date": "2天前",
			"end_date": "1天前",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "单品券2",
			"money": 10.00,
			"limit_counts": 10,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品1"
		}]
		"""
	Then jobs能获得优惠券'全体券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.00,
				"status": "已过期",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_2": {
				"money": 1.00,
				"status": "已过期",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_3": {
				"money": 1.00,
				"status": "已过期",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_4": {
				"money": 1.00,
				"status": "已过期",
				"consumer": "",
				"target": ""
			}
		}
		"""
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

@mall2 @add_coupon @eugene
Scenario: 1 给有效优惠券规则增加库存
	jobs添加"优惠券规则"后，优惠券有效
	1. 可以给优惠券码库添加库存
	2. jobs能获得包含新添加的优惠券的码库

	Given jobs登录系统
	When jobs为优惠券'单品券2'添加库存
		"""
		{
			"count": 2,
			"coupon_id_prefix": "coupon2_id_"
		}
		"""
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_5": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_6": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

@mall2 @add_coupon @eugene
Scenario: 2 给已过期优惠券规则增加库存
	jobs添加"优惠券规则"后，优惠券已过期
	1. 给已过期的优惠券码库添加库存，码库不变

	Given jobs登录系统
	When jobs为优惠券'全体券1'添加库存
		"""
		{
			"count": 2,
			"coupon_id_prefix": "coupon1_id_"
		}
		"""
	Then jobs能获得优惠券'全体券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.00,
				"status": "已过期",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_2": {
				"money": 1.00,
				"status": "已过期",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_3": {
				"money": 1.00,
				"status": "已过期",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_4": {
				"money": 1.00,
				"status": "已过期",
				"consumer": "",
				"target": ""
			}
		}
		"""

@mall2 @add_coupon @eugeneZ
Scenario: 3 给已失效优惠券规则增加库存
	jobs添加"优惠券规则"后，优惠券已失效
	1. 给已失效的优惠券码库添加库存，码库不变

	Given jobs登录系统
	When jobs失效优惠券'单品券2'
	When jobs为优惠券'单品券2'添加库存
		"""
		{
			"count": 2,
			"coupon_id_prefix": "coupon2_id_"
		}
		"""
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "已失效",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "已失效",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "已失效",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "已失效",
				"consumer": "",
				"target": ""
			}
		}
		"""
