#watcher:fengxuejing@weizoom.com,benchi@weizoom.com,zhangsanxiang@weizoom.com
#author: 冯雪静
#editor: 张三香 2015.10.13

Feature: 更新优惠券规则
	Jobs能通过管理系统更新"优惠券规则"

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
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

@mall2 @promotion @promotionCoupon   @coupon @eugene
Scenario: 更改优惠券规则名
	jobs添加"优惠券规则"后
	1. jobs能更改优惠券的规则名

	Given jobs登录系统
	When jobs更新优惠券规则'单品券2'为
		"""
		{
			"name": "单品券"
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "单品券",
			"type": "单品券",
			"money": 10.00,
			"remained_count": 4,
			"limit_counts": 10,
			"use_count": 0,
			"start_date": "今天",
			"end_date": "1天后"
		}, {
			"name": "全体券1",
			"type": "全店通用券",
			"money": 1.00,
			"remained_count": 4,
			"limit_counts": 10,
			"use_count": 0,
			"start_date": "2天前",
			"end_date": "1天前"
		}]
		"""
