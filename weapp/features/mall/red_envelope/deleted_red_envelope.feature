# __author__ : "冯雪静"

Feature: 删除红包
"""
	Jobs能通过管理系统删除"分享红包"

	# __author__ : 王丽
	1、分享红包活动创建后，必须开始才能生效
	2、每个店铺只能开启一个分享红包活动，只有活动期的分享红包活动才能"开启"
	3、可以手动"关闭"在活动期已开启的分享红包活动
	3、在活动期的未开启的分享红包活动和已结束的分享红包活动才能"删除"
	4、"查看"查看分享红包活动的详情
	5、在有查询条件，删除查询结果中的分享红包时候，查询结果应该还是按照之前的查询条件过滤
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
	And jobs已添加分享红包
	"""
	[{
		"name": "分享红包1",
		"prize_info": "全体券3",
		"start_date": "今天",
		"end_date": "2天后",
		"limit_money": 200,
		"desc": "下订单领红包",
		"logo_url": "/static/upload/6_20140710/1404981209095_5.jpg"
	}, {
		"name": "分享红包2",
		"prize_info": "单品券4",
		"limit_money": "无限制",
		"desc": "下订单领红包",
		"logo_url": "/static/upload/6_20140710/1404981209095_5.jpg"
	}, {
		"name": "分享红包3",
		"prize_info": "单品券4",
		"limit_money": "无限制",
		"desc": "下订单领红包",
		"logo_url": "/static/upload/6_20140710/1404981209095_5.jpg"
	}]
	"""

@mall2
Scenario: 1 开启分享红包
	jobs成功创建红包后，是关闭状态，可以进行开启操作
	1.分享红包列表中只允许一个红包是开启状态

	Given jobs登录系统
	When jobs-开启分享红包"分享红包1"
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包2",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包1",
			"status": "开启",
			"actions": ["关闭","查看"]
		}]
		"""
	When jobs-开启分享红包"分享红包2"
	Then jobs获得错误提示"请先关闭其他分享红包活动！"
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包2",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包1",
			"status": "开启",
			"actions": ["关闭","查看"]
		}]
		"""
	
@mall2
Scenario: 2 删除分享红包
	jobs成功创建红包后，是关闭状态，可以进行删除操作
	1.开启红包后不可以进行删除操作

	Given jobs登录系统
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包2",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包1",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}]
		"""
	When jobs-删除分享红包"分享红包1"
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包2",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}]
		"""
	When jobs-开启分享红包"分享红包2"
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包2",
			"status": "开启",
			"actions": ["关闭","查看"]
		}]
		"""
	#开启红包后不可删除
	When jobs-删除分享红包"分享红包2"
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}]
		"""

Scenario: 3 在查询"活动名称"结果中删除分享红包

		When jobs设置查询条件
			"""
			{
				"name":"分享红包1",
				"prize_info":"所有奖励"
				"start_date": "",
				"end_date": ""
			}
			"""
		Then jobs能获取红包列表
			"""
			[{
				"name": "分享红包1",
				"prize_info": ["全体券3"],
				"start_date": "今天",
				"end_date": "2天后",
				"status": "关闭",
				"actions": ["开启","删除","查看"]
			}]
			"""
		When jobs删除分享红包'分享红包1'
		Then jobs能获取红包列表
			"""
			[{ }]
			"""

Scenario: 4 在查询"奖励"结果中删除分享红包

		When jobs设置查询条件
			"""
			{
				"name":"",
				"prize_info":"单品券4"
				"start_date": "",
				"end_date": ""
			}
			"""
		Then jobs能获取红包列表
			"""
			[{
				"name": "分享红包3",
				"prize_info": ["单品券4"],
				"status": "关闭",
				"actions": ["开启","删除","查看"]
			},{
				"name": "分享红包2",
				"prize_info": ["单品券4"],
				"status": "关闭",
				"actions": ["开启","删除","查看"]
			}]
			"""
		When jobs删除分享红包'分享红包3'
		Then jobs能获取红包列表
			"""
			[{
				"name": "分享红包2",
				"prize_info": ["单品券4"],
				"status": "关闭",
				"actions": ["开启","删除","查看"]
			}]
			"""

Scenario: 5 在查询"奖励时间"结果中删除分享红包

		When jobs设置查询条件
			"""
			{
				"name":"",
				"prize_info":"所有奖励"
				"start_date": "今天",
				"end_date": "2天后"
			}
			"""
		Then jobs能获取红包列表
			"""
			[{
				"name": "分享红包1",
				"prize_info": ["全体券3"],
				"start_date": "今天",
				"end_date": "2天后",
				"status": "关闭",
				"actions": ["开启","删除","查看"]
			}]
			"""
		When jobs删除分享红包'分享红包1'
		Then jobs能获取红包列表
			"""
			[{ }]
			"""

		
