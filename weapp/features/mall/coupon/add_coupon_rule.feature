#watcher:fengxuejing@weizoom.com,benchi@weizoom.com,zhangsanxiang@weizoom.com
#author: 冯雪静
#editor: 张三香 2015.10.15

Feature: 添加优惠券规则
	Jobs能通过管理系统添加"优惠券规则"
	"""
		补充_2015.10.15:
			1.单商品支持添加多个单品优惠券
			2.商品下架、修改后对优惠券无影响，各个模块均可选择该优惠券且优惠券管理处优惠券不为失效状态，添加劵码可继续使用。
			3.禁止优惠券商品与创建单品券无关
			4.单品优惠券选择商品时,'已参与促销'字段显示规则：
				a.此商品参与了促销活动，那么显示促销的活动名称
				b.此商品被设置了单品优惠券，不管设置了多少单品优惠券，已参与促销的地方都显示'单品券'三个字
	"""

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

@mall2 @promotion @promotionCoupon   @market_tool.coupon @market_tool @eugene
Scenario:1 添加优惠券规则
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
		"""
	Given bill登录系统
	Then bill能获得优惠券规则列表
		"""
		[]
		"""

#补充：张三香
@mall2 @promotion @promotionCoupon @as
Scenario:2 添加单品优惠券规则,单商品支持多个单品优惠券
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "单品券01",
			"money": 1.00,
			"count": 5,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "商品1"
		}]
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "单品券01",
			"type": "单品券",
			"money": 1.00,
			"remained_count": 5,
			"limit_counts": 1,
			"use_count": 0,
			"start_date": "今天",
			"end_date": "1天后"
		}]
		"""
	When jobs添加优惠券规则
		"""
		[{
			"name": "单品券02",
			"money": 5.00,
			"count": 10,
			"limit_counts": 2,
			"start_date": "今天",
			"end_date": "2天后",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品1"
		}]
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "单品券02",
			"type": "单品券",
			"money": 5.00,
			"remained_count": 10,
			"limit_counts": 2,
			"use_count": 0,
			"start_date": "今天",
			"end_date": "2天后"
		},{
			"name": "单品券01",
			"type": "单品券",
			"money": 1.00,
			"remained_count": 5,
			"limit_counts": 1,
			"use_count": 0,
			"start_date": "今天",
			"end_date": "1天后"
		}]
		"""