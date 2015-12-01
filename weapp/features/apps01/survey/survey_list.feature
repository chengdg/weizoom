#_author_:张三香 2015.12.01

Feature:用户调研列表
	"""
	用户调研列表
		查询条件:
			活动名称:默认为空,模糊匹配查询
			状态:默认为'全部'，下拉菜单显示：全部、未开始、进行中、已结束
			活动时间:默认为空
			奖项类型：下拉框显示，包含所有奖品、优惠券和积分，默认显示所有奖品
		列表字段:
			【活动名称】:显示用户调研活动名称
			【参与人数】:统计该活动的参与次数,同一用户参与多次的话,进行累加
			【奖项类型】:
			【开始时间】:显示活动的开始时间，格式为xxxx-xx-xx xx:xx
			【结束时间】:显示活动的结束时间，格式为xxxx-xx-xx xx:xx
			【状态】:用户调研活动的状态（进行中、未开始、已结束）
			【操作】:
				未开始:【预览】【统计】【查看结果】
				进行中:【关闭】【预览】【统计】【查看结果】
				已结束:【删除】【预览】【统计】【查看结果】
		排序：按照活动的创建时间进行倒序显示,每页最多显示10条数据
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
			"sub_title":"",
			"content":"欢迎参加调研",
			"start_date":"明天",
			"end_date":"2天后",
			"authority":"无需关注即可参与",
			"prize_type":"无奖励",
			"answer":
				{
					"title":"问答题",
					"is_required":"是"
				}
		},{
			"title":"进行中用户调研02",
			"sub_title":"用户调研2",
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
			"sub_title":"",
			"content":"欢迎参加调研",
			"start_date":"3天前",
			"end_date":"昨天",
			"authority":"无需关注即可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"quick":
				{
					"name":"false",
					"phone":"true",
					"email":"true",
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

@apps @survey
Scenario:1 用户调研活动列表查询
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
			"actions":["删除","预览","统计","查看结果"]
		},{
			"name":"进行中用户调研02",
			"parti_person_cnt":0,
			"prize_type":"积分",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions":["关闭","预览","统计","查看结果"]
		},{
			"name":"未开始用户调研01",
			"parti_person_cnt":0,
			"prize_type":"无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions":["预览","统计","查看结果"]
		}]
		"""
	#空查询（默认查询）
		When jobs设置用户调研活动列表查询条件
			"""
			{}
			"""
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"已结束用户调研03"
			},{
				"name":"进行中用户调研02"
			},{
				"name":"未开始用户调研01"
			}]
			"""

	#按照活动名称查询
		#查询结果为空
			When jobs设置用户调研活动列表查询条件
				"""
				{
					"name":"用 户"
				}
				"""
			Then jobs获得用户调研活动列表
				"""
				[]
				"""
		#模糊匹配
			When jobs设置用户调研活动列表查询条件
				"""
				{
					"name":"用户调研"
				}
				"""
			Then jobs获得用户调研活动列表
				"""
				[{
					"name":"已结束用户调研03"
				},{
					"name":"进行中用户调研02"
				},{
					"name":"未开始用户调研01"
				}]
				"""
		#精确匹配
			When jobs设置用户调研活动列表查询条件
				"""
				{
					"name":"已结束用户调研03"
				}
				"""
			Then jobs获得用户调研活动列表
				"""
				[{
					"name":"已结束用户调研03"
				}]
				"""

	#按照状态查询
		When jobs设置用户调研活动列表查询条件
				"""
				{
					"status":"全部"
				}
				"""
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"已结束用户调研03"
			},{
				"name":"进行中用户调研02"
			},{
				"name":"未开始用户调研01"
			}]
			"""

		When jobs设置用户调研活动列表查询条件
				"""
				{
					"status":"进行中"
				}
				"""
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"进行中用户调研02"
			}]
			"""

	#按照活动时间查询
		#查询结果为空
			When jobs设置用户调研活动列表查询条件
				"""
				{
					"start_date":"昨天",
					"end_date":"今天"
				}
				"""
			Then jobs获得用户调研活动列表
				"""
				[]
				"""
		#开始时间为空，结束时间非空
			When jobs设置用户调研活动列表查询条件
				"""
				{
					"start_date":"",
					"end_date":"今天"
				}
				"""
			Then jobs获得用户调研活动列表
				"""
				[{
					"name":"已结束用户调研03",
					"start_date":"3天前",
					"end_date":"昨天"
				}]
				"""
		#开始时间非空，结束时间为空
			When jobs设置用户调研活动列表查询条件
				"""
				{
					"start_date":"今天",
					"end_date":""
				}
				"""
			Then jobs获得用户调研活动列表
				"""
				[{
					"name":"进行中用户调研02",
					"start_date":"今天",
					"end_date":"2天后"
				},{
					"name":"未开始用户调研01",
					"start_date":"明天",
					"end_date":"2天后"
				}]
				"""
		#开始时间和结束时间相等
			When jobs设置用户调研活动列表查询条件
				"""
				{
					"start_date":"今天",
					"end_date":"今天"
				}
				"""
			Then jobs获得用户调研活动列表
				"""
				[]
				"""

	#按照奖项类型查询
		When jobs设置用户调研活动列表查询条件
			"""
			{
				"prize_type":"所有奖品"
			}
			"""
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"已结束用户调研03",
				"prize_type":"优惠券"
			},{
				"name":"进行中用户调研02",
				"prize_type":"积分"
			},{
				"name":"未开始用户调研01",
				"prize_type":"无奖励"
			}]
			"""

		When jobs设置用户调研活动列表查询条件
			"""
			{
				"prize_type":"积分"
			}
			"""
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"进行中用户调研02",
				"prize_type":"积分"
			}]
			"""

	#组合条件查询
		When jobs设置用户调研活动列表查询条件
			"""
			{
				"name":"用户调研",
				"status":"已结束",
				"start_date":"5天前",
				"end_date":"明天",
				"prize_type":"优惠券"
			}
			"""
		Then jobs获得用户调研活动列表
			"""
			[{
				"name":"已结束用户调研03",
				"parti_person_cnt":0,
				"prize_type":"优惠券",
				"start_date":"3天前",
				"end_date":"昨天",
				"status":"已结束"
			}]
			"""

@apps @survey
Scenario:2 用户调研活动列表分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""
		#Then jobs获得用户调研活动列表共'3'页

	When jobs访问用户调研活动列表第'1'页
	Then jobs获得用户调研列表
		"""
		[{
			"name":"已结束用户调研03"
		}]
		"""
	When jobs访问用户调研活动列表下一页
	Then jobs获得用户调研列表
		"""
		[{
			"name":"进行中用户调研02"
		}]
		"""
	When jobs访问用户调研活动列表第'3'页
	Then jobs获得用户调研列表
		"""
		[{
			"name":"未开始用户调研01"
		}]
		"""
	When jobs访问用户调研活动列表上一页
	Then jobs获得用户调研列表
		"""
		[{
			"name":"进行中用户调研02"
		}]
		"""