#_author_:张三香 2015.12.02

Feature:微信投票活动列表
	"""
	1、查询条件：
		【活动名称】:支持模糊查询
		【状态】：下拉列表显示，包含'所有投票'、'未开始'、'进行中'和'已结束'，默认显示'所有投票''
		【活动时间】：查询时开始时间和结束时间允许为空
		【奖项类型】：下拉列表显示，包含'所有奖品'、'优惠券'和'积分'，默认显示'所有奖品'
	2、列表字段：
		【活动名称】:显示微信投票名称
		【参与人数】:显示参与的人数
		【奖项类型】:显示无奖励、积分或优惠券
		【开始时间】:显示活动的开始时间，格式为xxxx-xx-xx xx:xx
		【结束时间】:显示活动的结束时间，格式为xxxx-xx-xx xx:xx
		【状态】:显示活动的状态，未开始、进行中或已结束
		【操作】：不同状态的活动，操作列显示信息不同
				未开始:【删除】【链接】【预览】【统计】【查看结果】
				进行中:【关闭】【链接】【预览】【统计】【查看结果】
				已结束:【删除】【链接】【预览】【统计】【查看结果】
	3、排序：按照创建时间倒序排列，每页最多显示10条数据
	"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts":"无限",
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

@mall2 @apps @vote @vote_list
Scenario:1 微信投票活动列表查询
	Given jobs登录系统
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票03",
			"participant_count":0,
			"prize_type":"优惠券",
			"start_date":"2天前",
			"end_date":"昨天",
			"status":"已结束",
			"actions": ["删除","链接","预览","统计","查看结果"]
		},{
			"name":"微信投票02",
			"participant_count":0,
			"prize_type":"积分",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","统计","查看结果"]
		},{
			"name":"微信投票01",
			"participant_count":0,
			"prize_type":"无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["删除","链接","预览","统计","查看结果"]
		}]
		"""

	#空查询（默认查询）
		When jobs设置微信投票活动列表查询条件
			"""
			[]
			"""
		Then jobs获得微信投票活动列表
			"""
			[{
				"name":"微信投票03"
			},{
				"name":"微信投票02"
			},{
				"name":"微信投票01"
			}]
			"""

	#活动名称查询
		#查询结果为空
			When jobs设置微信投票活动列表查询条件
				"""
				{
					"name":"投 票"
				}
				"""
			Then jobs获得微信投票活动列表
				"""
				[]
				"""
		#模糊匹配
			When jobs设置微信投票活动列表查询条件
				"""
				{
					"name":"微信投票"
				}
				"""
			Then jobs获得微信投票活动列表
				"""
				[{
					"name":"微信投票03"
				},{
					"name":"微信投票02"
				},{
					"name":"微信投票01"
				}]
				"""
		#精确匹配
			When jobs设置微信投票活动列表查询条件
				"""
				{
					"name":"微信投票03"
				}
				"""
			Then jobs获得微信投票活动列表
				"""
				[{
					"name":"微信投票03"
				}]
				"""

	#状态查询
		When jobs设置微信投票活动列表查询条件
			"""
			{
				"status":"所有投票"
			}
			"""
		Then jobs获得微信投票活动列表
			"""
			[{
				"name":"微信投票03",
				"start_date":"2天前",
				"end_date":"昨天",
				"status":"已结束"
			},{
				"name":"微信投票02",
				"start_date":"今天",
				"end_date":"2天后",
				"status":"进行中"
			},{
				"name":"微信投票01",
				"start_date":"明天",
				"end_date":"2天后",
				"status":"未开始"
			}]
			"""

		When jobs设置微信投票活动列表查询条件
			"""
			{
				"status":"进行中"
			}
			"""
		Then jobs获得微信投票活动列表
			"""
			[{
				"name":"微信投票02",
				"start_date":"今天",
				"end_date":"2天后",
				"status":"进行中"
			}]
			"""

	#活动时间查询
		#查询结果为空
			When jobs设置微信投票活动列表查询条件
				"""
				{
					"start_date":"5天前",
					"end_date":"3天前"
				}
				"""
			Then jobs获得微信投票活动列表
				"""
				[]
				"""
		#开始时间为空，结束时间非空
			When jobs设置微信投票活动列表查询条件
				"""
				{
					"start_date":"",
					"end_date":"昨天"
				}
				"""
			Then jobs获得微信投票活动列表
				"""
				[{
					"name":"微信投票03",
					"start_date":"2天前",
					"end_date":"昨天"
				}]
				"""
		#开始时间非空，结束时间为空
			When jobs设置微信投票活动列表查询条件
				"""
				{
					"start_date":"今天",
					"end_date":""
				}
				"""
			Then jobs获得微信投票活动列表
				"""
				[{
					"name":"微信投票02",
					"start_date":"今天",
					"end_date":"2天后"
				},{
					"name":"微信投票01",
					"start_date":"明天",
					"end_date":"2天后"
				}]
				"""
		#开始时间和结束时间相等
			When jobs设置微信投票活动列表查询条件
				"""
				{
					"start_date":"今天",
					"end_date":"今天"
				}
				"""
			Then jobs获得微信投票活动列表
				"""
				[]
				"""

	#奖励类型查询
		When jobs设置微信投票活动列表查询条件
			"""
			{
				"prize_type":"所有奖品"
			}
			"""
		Then jobs获得微信投票活动列表
			"""
			[{
				"name":"微信投票03",
				"prize_type":"优惠券"
			},{
				"name":"微信投票02",
				"prize_type":"积分"
			},{
				"name":"微信投票01",
				"prize_type":"无奖励"
			}]
			"""

		When jobs设置微信投票活动列表查询条件
			"""
			{
				"prize_type":"积分"
			}
			"""
		Then jobs获得微信投票活动列表
			"""
			[{
				"name":"微信投票02",
				"prize_type":"积分"
			}]
			"""

	#组合条件查询
		When jobs设置微信投票活动列表查询条件
			"""
			{
				"name":"微信投票",
				"start_date":"昨天",
				"end_date":"5天后",
				"prize_type":"积分",
				"status":"进行中"
			}
			"""
		Then jobs获得微信投票活动列表
			"""
			[{
				"name":"微信投票02",
				"participant_count":0,
				"prize_type":"积分",
				"start_date":"今天",
				"end_date":"2天后",
				"status":"进行中",
				"actions": ["关闭","链接","预览","统计","查看结果"]
			}]
			"""

@mall2 @apps @vote @vote_list
Scenario:2 微信投票活动列表分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""
		#Then jobs获得微信投票活动列表共'3'页

	When jobs访问微信投票活动列表第'1'页
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票03"
		}]
		"""

	When jobs访问微信投票活动列表下一页
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票02"
		}]
		"""
	When jobs访问微信投票活动列表第'3'页
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票01"
		}]
		"""

	When jobs访问微信投票活动列表上一页
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票02"
		}]
		"""