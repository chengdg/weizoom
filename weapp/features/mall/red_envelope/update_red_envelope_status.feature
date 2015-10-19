#author:张三香 2015.10.19

Feature:更新分享红包状态

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
			"start_time": "今天",
			"end_time": "2天后",
			"receive_method":"下单领取",
			"limit_order_money": 100,
			"use_info": "下订单领红包1",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"share_title":"分享描述1"
		},{
			"name": "红包2",
			"prize_info": "全体券2",
			"limit_time": true,
			"receive_method":"图文领取",
			"use_info": "图文领取领红包2",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"share_title":"分享描述2"
		},{
			"name": "红包3",
			"prize_info": "全体券3",
			"limit_time": true,
			"limit_order_money": "无限制",
			"receive_method":"下单领取",
			"use_info": "下订单领红包3",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"share_title":"分享描述3"
		}]
		"""

@promotion @promotionRedbag
Scenario:1 更新分享红包状态
	Given jobs登录系统
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
			"status": "关闭",
			"actions": ["分析","开启","删除","查看"]
		}]
		"""
	#开启分享红包
	When jobs开启分享红包'红包1'
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
			"actions": ["分析","关闭",查看"]
		}]
		"""
	#关闭分享红包（只能关闭领取方式为'下单领取'的分享红包）
	When jobs关闭分享红包'红包1'
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
			"status": "关闭",
			"actions": ["分析","开启","删除","查看"]
		}]
		"""
