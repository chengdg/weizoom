#author: 冯雪静
#editor: 张三香 2015.10.13

Feature: 删除优惠券
	Jobs能通过管理系统删除已过期、已失效、未领取的"优惠券"

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
		}, {
			"name": "全体券3",
			"money": 100.00,
			"limit_counts": 10,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
		}, {
			"name": "单品券4",
			"money": 1.00,
			"limit_counts": 10,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon4_id_",
			"coupon_product": "商品2"
		}]
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill领取jobs的优惠券
		"""
		[{
			"name": "全体券1",
			"coupon_ids": ["coupon1_id_2", "coupon1_id_1"]
		}, {
			"name": "单品券2",
			"coupon_ids": ["coupon2_id_2", "coupon2_id_1"]
		}, {
			"name": "全体券3",
			"coupon_ids": ["coupon3_id_2", "coupon3_id_1"]
		}]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'全体券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.00,
				"status": "已过期",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 1.00,
				"status": "已过期",
				"consumer": "",
				"target": "bill"
			}
		}
		"""
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
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
	Then jobs能获得优惠券'全体券3'的码库
		"""
		{
			"coupon3_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon3_id_2": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon3_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	Then jobs能获得优惠券'单品券4'的码库
		"""
		{
			"coupon4_id_1": {
				"money": 1.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon4_id_2": {
				"money": 1.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon4_id_3": {
				"money": 1.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon4_id_4": {
				"money": 1.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

@mall2 @promotion @promotionCoupon   @zy_cp1
Scenario: 1 删除已过期的优惠券
	jobs添加"优惠券"后，优惠券已过期
	1.如果优惠券没有被使用，可以删除已过期的优惠券
	2.jobs的删除操作不影响会员的其他优惠券

	Given jobs登录系统
	When jobs删除优惠券'全体券1'的码库
	Then jobs能获得优惠券'全体券1'的码库
		"""
		[]
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon3_id_2",
				"money": 100.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon3_id_1",
				"money": 100.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_2",
				"money": 10.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_1",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""

@mall2 @promotion @promotionCoupon   @zy_cp2
Scenario: 2 删除已失效的优惠券
	jobs添加"优惠券规则"后，使优惠券失效后
	1.如果优惠券没有被领取和使用，可以删除已失效的优惠券
	2.jobs的失效和删除操作不影响被领取的优惠券

	Given jobs登录系统
	When jobs失效优惠券'单品券2'
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
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
	When jobs删除优惠券'单品券2'的码库
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""

@mall2 @promotion @promotionCoupon   @zy_cp3 @eugene
Scenario: 3 删除未领取的优惠券
	jobs添加"优惠券规则"后
	1.如果优惠券没有被领取和使用，可以删除未领取的优惠券
	2.jobs的删除操作不影响被领取的优惠券

	Given jobs登录系统
	When jobs删除优惠券'全体券3'的码库
	Then jobs能获得优惠券'全体券3'的码库
		"""
		{
			"coupon3_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon3_id_2": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""

@mall2 @promotion @promotionCoupon   @eugene
Scenario: 4 删除已过期的优惠券规则
	jobs添加"优惠券"后，优惠券已过期
	1.jobs可以删除已过期的优惠券规则
	2.jobs的删除操作不影响其他优惠券规则
	3.jobs的删除操作不影响会员的其他优惠券

	Given jobs登录系统
	When jobs删除优惠券'全体券1'
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "单品券4",
			"start_date": "今天",
			"end_date": "2天后",
			"status": "进行中"
		}, {
			"name": "全体券3",
			"start_date": "今天",
			"end_date": "2天后",
			"status": "进行中"
		}, {
			"name": "单品券2",
			"start_date": "今天",
			"end_date": "1天后",
			"status": "进行中"
		}]
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon3_id_2",
				"money": 100.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon3_id_1",
				"money": 100.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_2",
				"money": 10.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_1",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""

#author: 王丽 补充在查询结果中删除活动
@mall2 @promotion @promotionCoupon
Scenario: 5 在按"优惠券名称"查询的查询结果下删除优惠券
	Given jobs登录系统
	When jobs设置优惠券规则列表查询条件
		"""
		{
			"name":"全体券1"
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "全体券1",
			"start_date": "2天前",
			"end_date": "1天前",
			"status": "已过期"
		}]
		"""
	When jobs删除优惠券'全体券1'
	Then jobs能获得优惠券规则列表
		"""
		[]
		"""

@mall2 @promotion @promotionCoupon
Scenario: 6 在按"优惠码"查询的查询结果下删除优惠券
	Given jobs登录系统
	When jobs设置优惠券规则列表查询条件
		"""
		{
			"coupon_code":"coupon1_id_1"
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "全体券1",
			"start_date": "2天前",
			"end_date": "1天前",
			"status": "已过期"
		}]
		"""
	When jobs删除优惠券'全体券1'
	Then jobs能获得优惠券规则列表
		"""
		[]
		"""

@mall2 @promotion @promotionCoupon
Scenario: 7 在按"优惠券类型"查询的查询结果下删除优惠券
	Given jobs登录系统
	And jobs已添加商品
		"""
		[ {
			"name": "商品3",
			"price": 200.00
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "单品券a",
			"money": 10.00,
			"limit_counts": 2,
			"start_date": "4天前",
			"end_date": "3天前",
			"coupon_id_prefix": "coupon6_id_",
			"coupon_product": "商品3"
		}]
		"""
	When jobs设置优惠券规则列表查询条件
		"""
		{
			"coupon_promotion_type":"多商品券"
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "单品券a",
			"type": "多商品券",
			"start_date": "4天前",
			"end_date": "3天前",
			"status": "已过期"
		},{
			"name": "单品券4",
			"type": "多商品券",
			"start_date": "今天",
			"end_date": "2天后",
			"status": "进行中"
		},{
			"name": "单品券2",
			"type": "多商品券",
			"start_date": "今天",
			"end_date": "1天后",
			"status": "进行中"
		}]
		"""
	When jobs删除优惠券'单品券a'
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name":"单品券4",
			"type":"多商品券",
			"start_date":"今天",
			"end_date":"2天后",
			"status": "进行中"
		},{
			"name":"单品券2",
			"type":"多商品券",
			"start_date":"今天",
			"end_date":"1天后",
			"status": "进行中"
		}]
		"""

@mall2 @promotion @promotionCoupon
Scenario: 8 在按"促销状态"查询的查询结果下删除优惠券
	Given jobs登录系统
	When jobs设置优惠券规则列表查询条件
		"""
		{
			"promotion_status":"已过期"
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "全体券1",
			"start_date": "2天前",
			"end_date": "1天前",
			"status": "已过期"
		}]
		"""
	When jobs删除优惠券'全体券1'
	Then jobs能获得优惠券规则列表
		"""
		[]
		"""

@mall2 @promotion @promotionCoupon
Scenario: 9 在按"活动时间"查询的查询结果下删除优惠券
	Given jobs登录系统
	When jobs设置优惠券规则列表查询条件
		"""
		{
			"start_date":"2天前",
			"end_date":"1天后"
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "单品券2",
			"start_date": "今天",
			"end_date": "1天后",
			"status": "进行中"
		}, {
			"name": "全体券1",
			"start_date": "2天前",
			"end_date": "1天前",
			"status": "已过期"
		}]
		"""
	When jobs删除优惠券'全体券1'
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "单品券2",
			"type": "多商品券",
			"money": 10.00,
			"remained_count": 2,
			"limit_counts": 10,
			"use_count": 0,
			"start_date": "今天",
			"end_date": "1天后",
			"status": "进行中"
		}]
		"""



