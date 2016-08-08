#author:张三香 2015.10.19

Feature:分享红包列表查询
	"""
		【活动名称】:默认为空；支持模糊查询
		【奖励】:默认为'所有奖励'，下拉列表显示，下拉列表中只显示领取限制为'不限'且已被创建分享红包的优惠券名称
		【奖励时间】:默认为空
	"""

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name":"商品1",
			"price":10.00
		}]
		"""
	When jobs添加优惠券规则
		"""
		[{
			"name": "单品券1",
			"money": 5.00,
			"count": 10,
			"limit_counts": "不限",
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "商品1"
		},{
			"name": "全体券2",
			"money": 20.00,
			"count": 5,
			"limit_counts": "不限",
			"start_date": "今天",
			"end_date": "2天后",
			"coupon_id_prefix": "coupon2_id_"
		},{
			"name": "全体券3",
			"money": 30.00,
			"count": 5,
			"limit_counts": "不限",
			"start_date": "今天",
			"end_date": "3天后",
			"coupon_id_prefix": "coupon3_id_"
		},{
			"name": "全体券4",
			"money": 40.00,
			"count": 5,
			"limit_counts": 2,
			"start_date": "今天",
			"end_date": "3天后",
			"coupon_id_prefix": "coupon4_id_"
		}]
		"""
	When jobs添加分享红包
		"""
		[{
			"name": "分享红包1",
			"prize_info": "单品券1",
			"is_permanant_active": false,
			"start_date": "今天",
			"end_date": "2天后",
			"receive_method":"下单领取",
			"limit_money": 100.00,
			"detail": "下订单领红包1",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"remark":"分享描述1"
		},{
			"name": "红包2",
			"prize_info": "全体券2",
			"is_permanant_active": true,
			"receive_method":"图文领取",
			"detail": "图文领取领红包2",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"remark":"分享描述2"
		},{
			"name": "红包3",
			"prize_info": "全体券3",
			"is_permanant_active": true,
			"limit_money": "无限制",
			"receive_method":"下单领取",
			"detail": "下订单领红包3",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"remark":"分享描述3"
		},{
			"name": "红包4",
			"prize_info": "全体券3",
			"is_permanant_active": false,
			"start_date": "今天",
			"end_date": "3天后",
			"receive_method":"图文领取",
			"detail": "图文领取红包4",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"remark":"分享描述4"
		}]
		"""

@mall2 @promotion @promotionRedbag 
Scenario:1 分享红包列表查询
	Given jobs登录系统
	#默认条件查询
		When jobs设置查询条件
			"""
			{}
			"""
		Then jobs能获取分享红包列表
			"""
			[{
				"name": "【图文领取】红包4"
			},{
				"name": "红包3"
			},{
				"name": "【图文领取】红包2"
			},{
				"name": "分享红包1"
			}]
			"""

	#活动名称
		#部分匹配
		When jobs设置查询条件
			"""
			{
				"name": "红包"
			}
			"""
		Then jobs能获取分享红包列表
			"""
			[{
				"name": "【图文领取】红包4"
			},{
				"name": "红包3"
			},{
				"name": "【图文领取】红包2"
			},{
				"name": "分享红包1"
			}]
			"""

		#完全匹配
		When jobs设置查询条件
			"""
			{
				"name":"分享红包1"
			}
			"""
		Then jobs能获取分享红包列表
			"""
			[{
				"name": "分享红包1"
			}]
			"""

		#查询结果为空
		When jobs设置查询条件
			"""
			{
				"name":"红 包"
			}
			"""
		Then jobs能获取分享红包列表
			"""
			[]
			"""

	#奖励
		#查询结果非空
		When jobs设置查询条件
			"""
			{
				"prize_info": "全体券3"
			}
			"""
		Then jobs能获取分享红包列表
			"""
			[{
				"name": "【图文领取】红包4"
			},{
				"name": "红包3"
			}]
			"""

	#奖励时间
		#查询结果非空
		When jobs设置查询条件
			"""
			{
				"start_date": "今天",
				"end_date": "5天后"
			}
			"""
		Then jobs能获取分享红包列表
			"""
			[{
				"name": "【图文领取】红包4"
			},{
				"name": "分享红包1"
			}]
			"""

		#查询结果为空
		When jobs设置查询条件
			"""
			{
				"start_date": "昨天",
				"end_date": "今天"
			}
			"""
		Then jobs能获取分享红包列表
			"""
			[]
			"""