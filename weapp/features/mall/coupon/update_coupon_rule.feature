#author: 冯雪静
#editor: 张三香 2015.10.13
#editor: 王丽 2016.04.15

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
			"description":"使用说明全体券",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "单品券2",
			"money": 10.00,
			"limit_counts": 10,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明单品券",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品1"
		}]
		"""

@mall2 @promotion @promotionCoupon   @coupon @eugene
Scenario:1 更改优惠券规则名和使用说明
	jobs添加"优惠券规则"后
	1. jobs能更改优惠券的规则名
	2. jobs能更改优惠券的使用说明

	Given jobs登录系统
	When jobs更新优惠券规则'单品券2'为
		"""
		{
			"name": "单品券",
			"description":"使用说明单品券-修改",
		}
		"""
	Then jobs获得优惠券规则'单品券'
		"""
		{
			"name": "单品券2",
			"money": 10.00,
			"limit_counts": 10,
			"count": 4,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明单品券-修改"
		}
		"""

	When jobs更新优惠券规则'全体券1'为
		"""
		{
			"name": "全体券",
			"description":"使用说明全体券-修改",
		}
		"""
	Then jobs获得优惠券规则'全体券'
		"""
		{
			"name": "全体券",
			"money": 1.00,
			"limit_counts": 10,
			"count": 4,
			"start_date": "2天前",
			"end_date": "1天前",
			"description":"使用说明全体券-修改"
		}
		"""

