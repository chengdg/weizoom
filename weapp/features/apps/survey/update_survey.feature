#_author_:张三香 2015.12.01

Feature:更新用户调研活动
	"""
	1、未开始状态的用户调研可以进行编辑并保存，进行中和已结束状态的不能进行更改；
	2、不同状态的用户调研，对应的操作列按钮不同:
		未开始:【链接】【预览】【统计】【查看结果】
		进行中:【关闭】【链接】【预览】【统计】【查看结果】
		已结束:【删除】【链接】【预览】【统计】【查看结果】
	3、进行中的用户调研可以进行'关闭'操作，关闭后结束时间会随之更改为关闭时的时间，状态变为'已结束'
	4、已结束状态的用户调研，可以进行'删除'操作
	"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建用户调研活动
		"""
		[{
			"title":"未开始用户调研01",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"明天",
			"end_date":"2天后",
			"authority":"无需关注即可参与",
			"prize_type":"无奖励",
			"answer":
				[{
					"title":"问答题",
					"is_required":"是"
				}]
		},{
			"title":"进行中用户调研02",
			"subtitle":"用户调研2",
			"content":"欢迎参加调研",
			"start_date":"今天",
			"end_date":"2天后",
			"authority":"必须关注才可参与",
			"prize_type":"积分",
			"integral": 10,
			"choose":
				[{
					"title":"选择题1",
					"single_or_multiple":"单选",
					"is_required":"是",
					"option":[{
							"options":"1"
						},{
							"options":"2"
						},{
							"options":"3"
						}]
				}]
		},{
			"title":"已结束用户调研03",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"3天前",
			"end_date":"昨天",
			"authority":"无需关注即可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"quick":
				[{
					"items_select":[{
						"item_name":"姓名",
						"is_selected":false
					},{
						"item_name":"手机",
						"is_selected":true
					},{
						"item_name":"邮箱",
						"is_selected":true
				}],
					"item_add":[{
						"item_name":"填写项1",
						"is_required":"是"
					},{
						"item_name":"填写项2",
						"is_required":"否"
					}]
				}]
		}]
		"""

@apps @survey
Scenario:1 编辑'未开始'状态的用户调研活动
	Given jobs登录系统
	When jobs编辑用户调研活动'未开始用户调研01'
		"""
		[{
			"title":"用户调研01",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"今天",
			"end_date":"2天后",
			"authority":"必须关注才可参与",
			"prize_type":"积分",
			"integral":10,
			"answer":
				[{
					"title":"问答题01",
					"is_required":"否"
				}]
		}]
		"""
	Then jobs获得用户调研活动'用户调研01'
		"""
		[{
			"title":"用户调研01",
			"subtitle":"",
			"content":"欢迎参加调研",
			"start_date":"今天",
			"end_date":"2天后",
			"authority":"必须关注才可参与",
			"prize_type":"积分",
			"integral":10,
			"answer":
				{
					"title":"问答题01",
					"is_required":"否"
				}
		}]
		"""

@apps @survey
Scenario:2 关闭'进行中'状态的用户调研活动
	Given jobs登录系统
	Then jobs获得用户调研活动列表
		"""
		[{
			"name":"已结束用户调研03",
			"parti_person_cnt":0,
			"prize_type":"优惠券",
			"start_date":"3天前",
			"end_date":"昨天",
			"status":"已结束",
			"actions":["删除","链接","预览","统计","查看结果"]
		},{
			"name":"进行中用户调研02",
			"parti_person_cnt":0,
			"prize_type":"积分",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions":["关闭","链接","预览","统计","查看结果"]
		},{
			"name":"未开始用户调研01",
			"parti_person_cnt":0,
			"prize_type":"无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions":["链接","预览","统计","查看结果"]
		}]
		"""
	When jobs关闭用户调研活动'进行中用户调研02'
	Then jobs获得用户调研活动列表
		"""
		[{
			"name":"已结束用户调研03",
			"parti_person_cnt":0,
			"prize_type":"优惠券",
			"start_date":"3天前",
			"end_date":"昨天",
			"status":"已结束",
			"actions":["删除","链接","预览","统计","查看结果"]
		},{
			"name":"进行中用户调研02",
			"parti_person_cnt":0,
			"prize_type":"积分",
			"start_date":"今天",
			"end_date":"今天",
			"status":"已结束",
			"actions":["删除","链接","预览","统计","查看结果"]
		},{
			"name":"未开始用户调研01",
			"parti_person_cnt":0,
			"prize_type":"无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions":["链接","预览","统计","查看结果"]
		}]
		"""

@apps @survey
Scenario:3 删除'已结束'状态的用户调研活动
	Given jobs登录系统
	Then jobs获得用户调研活动列表
		"""
		[{
			"name":"已结束用户调研03",
			"status":"已结束",
			"actions":["删除","链接","预览","统计","查看结果"]
		},{
			"name":"进行中用户调研02",
			"status":"进行中",
			"actions":["关闭","链接","预览","统计","查看结果"]
		},{
			"name":"未开始用户调研01",
			"status":"未开始",
			"actions":["链接","预览","统计","查看结果"]
		}]
		"""
	When jobs删除用户调研活动'已结束用户调研03'
	Then jobs获得用户调研活动列表
		"""
		[{
			"name":"进行中用户调研02",
			"status":"进行中",
			"actions":["关闭","链接","预览","统计","查看结果"]
		},{
			"name":"未开始用户调研01",
			"status":"未开始",
			"actions":["链接","预览","统计","查看结果"]
		}]
		"""