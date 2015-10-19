#author:张三香 2015.10.19

Feature:删除分享红包
	"""
		1、'下单领取'方式的分享红包,默认状态为关闭，可以进行删除；开启状态下不能进行删除
		2、'图文领取'方式的分享红包，默认状态为开启（只有一个开启状态），可以进行删除
	"""

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name":"商品1",
			"price":10.0
		}]
		"""
	When jobs添加优惠券规则
		"""
		[{
			"name": "单品券1",
			"money": 5.00,
			"count": 10,
			"each_limit": "不限",
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品1"
		},{
			"name": "全体券2",
			"money": 20.00,
			"count": 5,
			"each_limit": "不限",
			"start_date": "今天",
			"end_date": "2天后",
			"coupon_id_prefix": "coupon2_id_"
		},{
			"name": "全体券3",
			"money": 30.00,
			"count": 5,
			"each_limit": "不限",
			"start_date": "今天",
			"end_date": "3天后",
			"coupon_id_prefix": "coupon3_id_"
		}]
		"""
	When jobs添加分享红包
		"""
		[{
			"name": "红包1",
			"prize_info": "单品券1",
			"start_date": "今天",
			"end_date": "2天后",
			"get_type":'下单领取',
			"limit_money": 100,
			"desc": "下订单领红包1",
			"logo_url": "/static/upload/6_20140710/1404981209095_5.jpg"
		},{
			"name": "红包2",
			"prize_info": "全体券2",
			"is_permanant_active": true,
			"get_type":'图文领取',
			"desc": "图文领取领红包2",
			"logo_url": "/static/upload/6_20140710/1404981209095_5.jpg"
		},{
			"name": "红包3",
			"prize_info": "全体券3",
			"is_permanant_active": true,
			"limit_money": "无限制",
			"get_type":'下单领取',
			"desc": "下订单领红包3",
			"logo_url": "/static/upload/6_20140710/1404981209095_5.jpg"
		},{
			"name": "红包4",
			"prize_info": "全体券3",
			"start_date": "今天",
			"end_date": "2天后",
			"get_type":'图文领取',
			"desc": "图文领取红包4",
			"logo_url": "/static/upload/6_20140710/1404981209095_5.jpg"
		}]
		"""

@promotion @promotionRedbag 
Scenario:1 删除分享红包
	Given jobs登录系统
	When jobs开启分享红包'红包1'
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "【图文领取】红包4",
			"status": "开启",
			"actions": ["分析","删除","查看"]
		},{
			"name": "红包3",
			"status": "关闭",
			"actions": ["分析","开启","删除","查看"]
		},{
			"name": "【图文领取】红包2",
			"status": "开启",
			"actions": ["分析","删除","查看"]
		},{
			"name": "红包1",
			"status": "开启",
			"actions": ["分析","关闭","查看"]
		}]
		"""
	#删除'图文领取'方式的分享红包
	When jobs删除分享红包"【图文领取】红包4"
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "红包3",
			"status": "关闭",
			"actions": ["分析","开启","删除","查看"]
		},{
			"name": "【图文领取】红包2",
			"status": "开启",
			"actions": ["分析","删除","查看"]
		},{
			"name": "红包1",
			"status": "开启",
			"actions": ["分析","关闭","查看"]
		}]
		"""
	#删除'下单领取'方式的分享红包（状态必须为'关闭'）
	When jobs删除分享红包"红包3"
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "【图文领取】红包2",
			"status": "开启",
			"actions": ["分析","删除","查看"]
		},{
			"name": "红包1",
			"status": "开启",
			"actions": ["分析","关闭","查看"]
		}]
		"""

@promotion @promotionRedbag
Scenario:2 在查询"活动名称"结果中删除分享红包
	When jobs设置查询条件
		"""
		{
			"name": "红包4",
			"prize_info": "所有奖励"
		}
		"""
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "【图文领取】红包4",
			"status": "开启",
			"actions": ["分析","删除","查看"]
		}]
		"""
	When jobs删除分享红包"【图文领取】红包4"
	Then jobs能获取分享红包列表
		"""
		[]
		"""

@promotion @promotionRedbag
Scenario:3 在查询"奖励"结果中删除分享红包
	When jobs设置查询条件
		"""
		{
			"prize_info":"全体券3"
		}
		"""
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "【图文领取】红包4",
			"status": "开启",
			"actions": ["分析","删除","查看"]
		},{
			"name": "红包3",
			"status": "关闭",
			"actions": ["分析","开启","删除","查看"]
		}]
		"""
	When jobs删除分享红包"红包3"
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "【图文领取】红包4",
			"status": "开启",
			"actions": ["分析","删除","查看"]
		}]
		"""

@promotion @promotionRedbag
Scenario:4 在查询"奖励时间"结果中删除分享红包
	When jobs设置查询条件
		"""
		{
			"prize_info": "所有奖励",
			"start_date": "今天",
			"end_date": "2天后"
		}
		"""
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "【图文领取】红包4",
			"status": "开启",
			"actions": ["分析","删除","查看"]
		},{
			"name": "红包1",
			"status": "关闭",
			"actions": ["分析","开启","删除","查看"]
		}]
		"""
	When jobs删除分享红包"红包1"
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "【图文领取】红包4",
			"status": "开启",
			"actions": ["分析","删除","查看"]
		}]
		"""