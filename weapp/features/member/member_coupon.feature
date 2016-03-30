# __author__ : "新新 2016.3.29"

Feature: 会员列表-会员详情-优惠券明细列表
"""

	1、列表标题为优惠券明细，表头为领取时间、优惠券名称、明细、状态(和来源/去处暂不开发)
	2、列表以领取时间倒序排列，列表一页默认显示10条记录
	3、优惠券明细中要显示优惠券属性包括金额和（单品\全店通用券）
	4、优惠券状态为已使用、未使用和已过期可以进行筛选

	5、来源/去处暂不开发:
	直接领取：通过优惠券链接领取
	后台发放：通过会员管理发放优惠券
	扫码：推广扫码和带参数二维码的统称


"""

Background:

	Given bill关注jobs的公众号
	#添加优惠券规则
	Given jobs登录系统
	Given jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "单品券1",
			"money": 10.00,
			"limit_counts": 1,
			"count": 3,
			"start_date": "2015-05-20",
			"end_date": "2020-05-20",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "商品1"
		},{
			"name": "全店券2",
			"money": 20.00,
			"limit_counts": "无限",
			"count": 5,
			"start_date": "2015-06-20",
			"end_date": "2020-06-20",
			"coupon_id_prefix": "coupon2_id_"
		},{
			"name": "过期券3",
			"money": 50.00,
			"limit_counts": "无限",
			"count": 2,
			"start_date": "2015-01-01",
			"end_date": "2015-12-20",
			"coupon_id_prefix": "coupon3_id_"
		}]
		"""

	When jobs创建优惠券发放规则发放优惠券于'2015-05-01'
		"""
		{
			"name": "过期券3",
			"count": 1,
			"members": ["bill"],
			"coupon_ids": ["coupon3_id_1"]

		}
		"""

	When jobs创建优惠券发放规则发放优惠券于'2016-01-01'
		"""
		{
			"name": "单品券1",
			"count": 1,
			"members": ["bill"],
			"coupon_ids": ["coupon1_id_1"]
		}
		"""
	When jobs创建优惠券发放规则发放优惠券于'2016-01-05'
		"""
		{
			"name": "全店券2",
			"count": 2,
			"members": ["bill"],
			"coupon_ids": ["coupon2_id_2","coupon2_id_1"]
		}
		"""



Scenario:1 会员(未使用,已使用,已过期)优惠券明细
	jobs查看日期为当前日期

	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"order_id": "00001",
			"pay_type": "微信支付",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon1_id_1"
		}
		"""

	Given jobs登录系统
	Then jobs能获得weapp系统bill拥有优惠券
		| 领取时间   | 优惠券名称 |       明细     | 全部 |
		| 2016-01-05 | 全店券2    | 20.00全店通用券|未使用| 
		| 2016-01-05 | 全店券2    | 20.00全店通用券|未使用|
		| 2016-01-01 | 单品券2    | 10.00单品券    |已使用| 
		| 2015-05-01 | 过期券3    | 50.00全店通用券|已过期|


Scenario:2 会员使用优惠码
	bill直接用优惠码,使用时间即领取时间

	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"order_id": "00002",
			"pay_type": "微信支付",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon1_id_2"
		}
		"""

	Given jobs登录系统
	Then jobs能获得weapp系统bill拥有优惠券
		| 领取时间   | 优惠券名称 |       明细     | 全部 |
		| 今天       | 单品券2    | 10.00单品券    |已使用|
		| 2016-01-05 | 全店券2    | 20.00全店通用券|未使用| 
		| 2016-01-05 | 全店券2    | 20.00全店通用券|未使用|
		| 2016-01-01 | 单品券2    | 10.00单品券    |未使用| 
		| 2015-05-01 | 过期券3    | 50.00全店通用券|已过期|


Scenario:3 按优惠券状态进行筛选


	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"order_id": "00001",
			"pay_type": "微信支付",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"coupon": "coupon1_id_1"
		}
		"""

	Given jobs登录系统
	Then jobs能获得weapp系统bill拥有优惠券默认查询条件
		"""
		[{
			"status":"全部"
		}]
		"""
	Then jobs能获得weapp系统bill拥有优惠券
		| 领取时间   | 优惠券名称 |       明细     | 全部 |
		| 2016-01-05 | 全店券2    | 20.00全店通用券|未使用|
		| 2016-01-05 | 全店券2    | 20.00全店通用券|未使用|
		| 2016-01-01 | 单品券2    | 10.00单品券    |已使用|
		| 2015-05-01 | 过期券3    | 50.00全店通用券|已过期|

	When jobs设置优惠券状态查询条件
		"""
		[{
			"status":"未使用"
		}]
		"""
	Then jobs能获得weapp系统bill拥有优惠券
		| 领取时间   | 优惠券名称 |       明细     | 全部 |
		| 2016-01-05 | 全店券2    | 20.00全店通用券|未使用|
		| 2016-01-05 | 全店券2    | 20.00全店通用券|未使用|

	When jobs设置优惠券状态查询条件
		"""
		[{
			"status":"已使用"
		}]
		"""
	Then jobs能获得weapp系统bill拥有优惠券
		| 领取时间   | 优惠券名称 |       明细     | 全部 |
		| 2016-01-01 | 单品券2    | 10.00单品券    |已使用|

	When jobs设置优惠券状态查询条件
		"""
		[{
			"status":"已过期"
		}]
		"""
	Then jobs能获得weapp系统bill拥有优惠券
		| 领取时间   | 优惠券名称 |       明细     | 全部 |
		| 2015-05-01 | 过期券3    | 50.00全店通用券|已过期|

