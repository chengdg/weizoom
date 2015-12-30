#_author_:张三香 2015.12.03

Feature:更新微信投票活动
	"""
	1、不同状态的活动，操作列显示信息不同
		未开始:【删除】【链接】【预览】【统计】【查看结果】
		进行中:【关闭】【链接】【预览】【统计】【查看结果】
		已结束:【删除】【链接】【预览】【统计】【查看结果】
	2、'未开始'状态的微信投票活动，可以进行编辑并保存
	3、'进行中'状态的微信投票活动，可以进行关闭操作，关闭后状态变为'已结束'，同时结束时间也会变为关闭时的时间
	4、'未开始'和'已结束'状态的微信投票活动，可以进行删除操作
	"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts":"不限",
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建微信投票活动
		"""
		[{
			"title":"微信投票01",
			"subtitle":"微信投票01",
			"content":"谢谢投票",
			"start_date":"明天",
			"end_date":"2天后",
			"permission":"必须关注才可参与",
			"prize_type":"无奖励",
			"text_options":
				[{
					"title":"选择题1",
					"type":"单选",
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
			"title":"微信投票02",
			"subtitle":"微信投票02",
			"content":"谢谢投票",
			"start_date":"今天",
			"end_date":"2天后",
			"permission":"无需关注即可参与",
			"prize_type":"积分",
			"integral":20,
			"text_options":
				[{
					"title":"选择题1",
					"type":"单选",
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
			"title":"微信投票03",
			"subtitle":"微信投票03",
			"content":"谢谢投票",
			"start_date":"2天前",
			"end_date":"昨天",
			"permission":"无需关注即可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"text_options":
				[{
					"title":"选择题1",
					"type":"单选",
					"is_required":"是",
					"option":[{
							"options":"1"
						},{
							"options":"2"
						},{
							"options":"3"
						}]
				}]
		}]
		"""

@apps @vote
Scenario:1 编辑'未开始'状态的微信投票活动
	Given jobs登录系统
	When jobs编辑微信投票活动'微信投票01'
		"""
		{
			"title":"微信投票001",
			"subtitle":"微信投票001",
			"content":"谢谢投票001",
			"start_date":"今天",
			"end_date":"2天后",
			"permission":"无需关注即可参与",
			"prize_type":"积分",
			"integral":10,
			"text_options":
				[{
					"title":"选择题1",
					"type":"多选",
					"is_required":"否",
					"option":[{
							"options":"1"
						},{
							"options":"2"
						},{
							"options":"3"
						}]
				}],
			"participate_info":[{
				"items_select":[{
							"item_name":"姓名",
							"is_selected":"true"
						},{
							"item_name":"手机",
							"is_selected":"true"
						},{
							"item_name":"邮箱",
							"is_selected":"true"
						},{
							"item_name":"QQ",
							"is_selected":"true"
						},{
							"item_name":"职位",
							"is_selected":"true"
						},{
							"item_name":"住址",
							"is_selected":"false"
						}],
				"items_add":[{
						"item_name":"填写项1",
						"is_required":"是"
					},{
						"item_name":"填写项2",
						"is_required":"否"
					}]
				}]
		}
		"""
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票03",
			"start_date":"2天前",
			"end_date":"昨天",
			"status":"已结束",
			"actions": ["删除","链接","预览","统计","查看结果"]
		},{
			"name":"微信投票02",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","统计","查看结果"]
		},{
			"name":"微信投票001",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","统计","查看结果"]
		}]
		"""

@apps @vote
Scenario:2 关闭'进行中'状态的微信投票活动
	Given jobs登录系统
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票03",
			"start_date":"2天前",
			"end_date":"昨天",
			"status":"已结束",
			"actions": ["删除","链接","预览","统计","查看结果"]
		},{
			"name":"微信投票02",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","统计","查看结果"]
		},{
			"name":"微信投票01",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["删除","链接","预览","统计","查看结果"]
		}]
		"""
	When jobs关闭微信投票活动'微信投票02'
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票03",
			"start_date":"2天前",
			"end_date":"昨天",
			"status":"已结束",
			"actions": ["删除","链接","预览","统计","查看结果"]
		},{
			"name":"微信投票02",
			"start_date":"今天",
			"end_date":"今天",
			"status":"已结束",
			"actions": ["删除","链接","预览","统计","查看结果"]
		},{
			"name":"微信投票01",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["删除","链接","预览","统计","查看结果"]
		}]
		"""

@apps @vote
Scenario:3 删除'未开始'和'已结束'状态的微信投票活动
	Given jobs登录系统
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票03",
			"status":"已结束",
			"actions": ["删除","链接","预览","统计","查看结果"]
		},{
			"name":"微信投票02",
			"status":"进行中",
			"actions": ["关闭","链接","预览","统计","查看结果"]
		},{
			"name":"微信投票01",
			"status":"未开始",
			"actions": ["删除","链接","预览","统计","查看结果"]
		}]
		"""

	#删除'已结束'状态的微信投票活动
	When jobs删除微信投票活动'微信投票03'
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票02",
			"status":"进行中",
			"actions": ["关闭","链接","预览","统计","查看结果"]
		},{
			"name":"微信投票01",
			"status":"未开始",
			"actions": ["删除","链接","预览","统计","查看结果"]
		}]
		"""

	#删除'未开始'状态的微信投票活动
	When jobs删除微信投票活动'微信投票01'
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票02",
			"status":"进行中",
			"actions": ["关闭","链接","预览","统计","查看结果"]
		}]
		"""