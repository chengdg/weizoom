# __author__ : "冯雪静"

Feature: 添加红包
"""
	Jobs能通过管理系统添加"添加红包"

	# __author__ : 王丽
	1、【活动名称】：只在分享红包活动列表中显示
	2、【奖励】：选择现有的优惠券，只能选择到【每人限领】为无限的优惠券
	3、【奖励时间】：开始结束时间只能选择今天及其之后的时间，结束时间必须在开始时间之后
		勾选"永久"：活动永久有效,除非手动结束活动，活动才结束
	4、【奖励条件】：订单满（？）元；设置订单满多少元可以得到红包；空为不限制，只要提交订单就能获得红包
	5、【活动说明】：设置本活动的活动说明
	6、【分享图文设置】：分享到朋友圈或者分享给单个好友的情况下，显示的图文图片和文字描述
"""

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		}, {
			"name": "商品2",
			"price": 200.00
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "全体券1",
			"money": 1.00,
			"limit_counts": "无限",
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
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
		}, {
			"name": "单品券4",
			"money": 1.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon4_id_",
			"coupon_product": "商品2"
		}]
		"""
@eugeneX
Scenario: 添加分享红包
	jobs添加"分享红包"后，"红包"列表会按照添加的倒序排列
	1.bill能获取红包列表

	Given jobs登录系统
	#jobs添加有领取限制的红包和没有领取限制的红包(1.有限制，活动时间段有效 2.无限制，活动永久有效)
	When jobs添加分享红包
		"""
		[{
			"name": "红包1",
			"prize_info": ["全体券3"],
			"start_date": "今天",
			"end_date": "2天后",
			"limit_money": 200,
			"desc": "下订单领红包",
			"logo_url": "/static/upload/6_20140710/1404981209095_5.jpg"
		}, {
			"name": "红包2",
			"prize_info": ["单品券4"],
			"is_permanant_active": true,
			"limit_money": "无限制",
			"desc": "下订单领红包",
			"logo_url": "/static/upload/6_20140710/1404981209095_5.jpg"
		}]
		"""
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "红包2",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "红包1",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}]
		"""
	And bill能获取红包列表
		"""
		[]
		"""
