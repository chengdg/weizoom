#_author_:张三香 2015.12.02

Feature:新建微信投票活动

@apps @vote
Scenario:1 新建微信投票活动,只添加选择题模块,无奖励
	#活动权限-必须关注才可参与
	#奖励类型-无奖励
	#包含模块-2个选择题模块
	#状态-进行中

	Given jobs登录系统
	When jobs新建微信投票活动
		"""
		[{
			"title":"多个选择题微信投票",
			"sub_title":"微信投票01",
			"content":"谢谢投票",
			"start_date":"今天",
			"end_date":"2天后",
			"authority":"必须关注才可参与",
			"prize_type":"无奖励",
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
				},{
					"title":"选择题2",
					"single_or_multiple":"多选",
					"is_required":"否",
					"option":[{
							"options":"选项A"
						},{
							"options":"选项B"
						},{
							"options":"选项C"
						}]
				}]
		}]
		"""
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"多个选择题微信投票",
			"parti_person_cnt":0,
			"prize_type":"无奖励",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","预览","统计","查看结果"]
		}]
		"""

@apps @vote
Scenario:2 新建微信投票活动,只添加快捷模块,积分奖励
	#活动权限-无需关注即可参与
	#奖励类型-积分
	#包含模块-1个快捷模块
	#状态-未开始

	Given jobs登录系统
	When jobs新建微信投票活动
		"""
		[{
			"title":"快捷模块微信投票",
			"sub_title":"微信投票02",
			"content":"谢谢投票",
			"start_date":"明天",
			"end_date":"2天后",
			"authority":"无需关注即可参与",
			"prize_type":"积分",
			"integral":20,
			"quick":
				{
					"name":"ture",
					"phone":"false",
					"email":"true",
					"QQ":"true",
					"item":[{
						"name":"填写项1",
						"is_required":"是"
					},{
						"name":"填写项2",
						"is_required":"否"
					},{
						"name":"填写项3",
						"is_required":"否"
					}]
				}
		}]
		"""
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"快捷模块微信投票",
			"parti_person_cnt":0,
			"prize_type":"积分",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["删除","预览","统计","查看结果"]
		}]
		"""

@apps @vote
Scenario:3 新建微信投票活动,添加选择题和快捷模块,优惠券奖励
	#活动权限-必须关注才可参与
	#奖励类型-优惠券
	#包含模块-1个选择题模块和1个快捷模块
	#状态-已结束

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
	When jobs新建微信投票活动
		"""
		[{
			"title":"多个模块微信投票",
			"sub_title":"微信投票03",
			"content":"谢谢投票",
			"start_date":"3天前",
			"end_date":"昨天",
			"authority":"必须关注才可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
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
				}],
			"quick":
				{
					"name":"ture",
					"phone":"false",
					"item":[{
						"name":"填写项1",
						"is_required":"是"
					},{
						"name":"填写项2",
						"is_required":"否"
					}]
				}
		}]
		"""
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"多个模块微信投票",
			"parti_person_cnt":0,
			"prize_type":"优惠券",
			"start_date":"3天前",
			"end_date":"昨天",
			"status":"已结束",
			"actions": ["删除","预览","统计","查看结果"]
		}]
		"""