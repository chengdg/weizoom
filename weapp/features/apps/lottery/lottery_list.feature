#_author_:张三香 2015.11.17

Feature:微信抽奖列表
	"""
	微信抽奖列表
		查询条件:
			活动名称:默认为空,模糊匹配查询
			状态:默认为'全部'，下拉菜单显示：全部、未开始、进行中、已结束
			活动时间:默认为空
		列表字段:
			【活动名称】:显示微信抽奖活动名称
			【开始时间】:显示活动的开始时间，格式为xxxx-xx-xx xx:xx
			【结束时间】:显示活动的结束时间，格式为xxxx-xx-xx xx:xx
			【状态】:微信抽奖活动的状态（进行中、未开始、已结束）
			【参与次数】:统计该活动的参与次数,同一用户参与多次的话,进行累加
			【操作】:
				未开始: 查看结果 删除 预览
				进行中: 查看结果 关闭 预览
				已结束: 查看结果 删除 预览
			排序：按照活动的创建时间进行倒序显示,每页最多显示10条数据
	"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 500,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖01",
			"start_date":"明天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":1,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一人一次",
			"win_rate":"50%",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		},{
			"name":"微信抽奖02",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":100,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一天一次",
			"win_rate":"50%",
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		},{
			"name":"微信抽奖03",
			"start_date":"3天前",
			"end_date":"昨天",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"不限",
			"win_rate":"50%",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
		"""

@apps @lottery @lottery_list
Scenario:1 微信抽奖活动列表查询
	Given jobs登录系统
	#空查询
		When jobs设置微信抽奖活动列表查询条件
			"""
			{}
			"""
		Then jobs获得微信抽奖活动列表
			"""
			[{
				"name":"微信抽奖03"
			},{
				"name":"微信抽奖02"
			},{
				"name":"微信抽奖01"
			}]
			"""

	#按照活动名称查询
		#查询结果为空
		When jobs设置微信抽奖活动列表查询条件
			"""
			{
				"name":"条件"
			}
			"""
		Then jobs获得微信抽奖活动列表
			"""
			[]
			"""

		#模糊匹配
		When jobs设置微信抽奖活动列表查询条件
			"""
			{
				"name":"微信抽奖"
			}
			"""
		Then jobs获得微信抽奖活动列表
			"""
			[{
				"name":"微信抽奖03"
			},{
				"name":"微信抽奖02"
			},{
				"name":"微信抽奖01"
			}]
			"""

		#精确匹配
		When jobs设置微信抽奖活动列表查询条件
			"""
			{
				"name":"微信抽奖01"
			}
			"""
		Then jobs获得微信抽奖活动列表
			"""
			[{
				"name":"微信抽奖01"
			}]
			"""

	#按照状态查询
		When jobs设置微信抽奖活动列表查询条件
			"""
			{
				"status":"全部"
			}
			"""
		Then jobs获得微信抽奖活动列表
			"""
			[{
				"name":"微信抽奖03"
			},{
				"name":"微信抽奖02"
			},{
				"name":"微信抽奖01"
			}]
			"""

		When jobs设置微信抽奖活动列表查询条件
			"""
			{
				"status":"未开始"
			}
			"""
		Then jobs获得微信抽奖活动列表
			"""
			[{
				"name":"微信抽奖01"
			}]
			"""

	#按照活动时间查询
		#查询结果为空
			When jobs设置微信抽奖活动列表查询条件
				"""
				{
					"start_date":"2天前",
					"end_date":"今天"
				}
				"""
			Then jobs获得微信抽奖活动列表
				"""
				[]
				"""

		#开始时间为空，结束时间非空
			When jobs设置微信抽奖活动列表查询条件
				"""
				{
					"start_date":"",
					"end_date":"明天"
				}
				"""
			Then jobs获得微信抽奖活动列表
				"""
				[{
					"name":"微信抽奖03"
				}]
				"""

		#开始时间非空，结束时间为空
			When jobs设置微信抽奖活动列表查询条件
				"""
				{
					"start_date":"昨天",
					"end_date":""
				}
				"""
			Then jobs获得微信抽奖活动列表
				"""
				[{
					"name":"微信抽奖02"
				},{
					"name":"微信抽奖01"
				}]
				"""

		#开始时间非空，结束时间非空
			When jobs设置微信抽奖活动列表查询条件
				"""
				{
					"start_date":"今天",
					"end_date":"3天后"
				}
				"""
			Then jobs获得微信抽奖活动列表
				"""
				[{
					"name":"微信抽奖02"
				},{
					"name":"微信抽奖01"
				}]
				"""

		#开始时间和结束时间相等
			When jobs设置微信抽奖活动列表查询条件
				"""
				{
					"start_date":"今天",
					"end_date":"今天"
				}
				"""
			Then jobs获得微信抽奖活动列表
				"""
				[]
				"""

	#组合查询
		When jobs设置微信抽奖活动列表查询条件
			"""
			{
				"name":"微信抽奖",
				"status":"已结束",
				"start_date":"3天前",
				"end_date":"今天"
			}
			"""
		Then jobs获得微信抽奖活动列表
				"""
				[{
					"name":"微信抽奖03"
				}]
				"""

@apps @lottery @lottery_list
Scenario:2 微信抽奖活动列表分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""
		#Then jobs获得微信抽奖活动列表共'3'页

	When jobs访问微信抽奖活动列表第'1'页
	Then jobs获得微信抽奖活动列表
		"""
		[{
			"name":"微信抽奖03",
			"status":"已结束"
		}]
		"""
	When jobs访问微信抽奖活动列表下一页
	Then jobs获得微信抽奖活动列表
		"""
		[{
			"name":"微信抽奖02",
			"status":"进行中"
		}]
		"""
	When jobs访问微信抽奖活动列表第'3'页
	Then jobs获得微信抽奖活动列表
		"""
		[{
			"name":"微信抽奖01",
			"status":"未开始"
		}]
		"""
	When jobs访问微信抽奖活动列表上一页
	Then jobs获得微信抽奖活动列表
		"""
		[{
			"name":"微信抽奖02",
			"status":"进行中"
		}]
		"""