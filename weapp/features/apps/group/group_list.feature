#_author_:许韦 2016.3.9

Feature:团购活动列表
	"""
	说明：
		1 团购活动列表的"查询":
			【商品名称】：支持模糊查询
			【状态】：默认为'全部'，下拉框显示：全部、未开启、进行中和已结束
			【起止时间】：开始时间和结束时间允许为空
			【团购名称】：支持模糊查询
		2 团购活动列表的"分页"，每10条记录一页
	"""
Background:
	Given jobs登录系统
	When jobs新建团购活动
		"""
		[{
			"group_name":"团购活动1",
			"start_time":"今天",
			"end_time":"明天",
			"product_name":"酱牛肉",
			"group_dict":[{
					"group_type":5,
					"group_day":1,
					"group_price":45
			},{
					"group_type":10,
					"group_day":2,
					"group_price":30
			}],
			"ship_date":10,
			"product_counts":200,
			"material_image":"1.jpg",
			"share_description":"团购分享描述"
		},{
			"group_name":"团购活动2",
			"start_time":"明天",
			"end_time":"2天后",
			"product_name":"花生酱",
			"group_dict":[{
					"group_type":10,
					"group_day":2,
					"group_price":8.5
			}],
			"ship_date":20,
			"product_counts":150,
			"material_image":"2.jpg",
			"share_description":"团购分享描述"
		},{
			"group_name":"团购活动3",
			"start_time":"3天前",
			"end_time":"昨天",
			"product_name":"酱牛肉",
			"group_dict":[{
					"group_type":5,
					"group_day":1,
					"group_price":40.5
			}],
			"ship_date":5,
			"product_counts":100,
			"material_image":"3.jpg",
			"share_description":"团购分享描述"
		}]
		"""
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动2",
			"opengroup_num":"",
			"consumer_num":"",
			"visitor_num":"",
			"status":"未开启",
			"start_date":"明天",
			"end_date":"2天后",
			"actions": ["参团详情","编辑","开启"]
		},{
			"name":"团购活动1",
			"opengroup_num":"",
			"consumer_num":"",
			"visitor_num":"",
			"status":"未开启",
			"start_date":"今天",
			"end_date":"明天",
			"actions": ["参团详情","编辑","开启"]
		},{
			"name":"团购活动3",
			"opengroup_num":"",
			"consumer_num":"",
			"visitor_num":"",
			"status":"已结束",
			"start_date":"3天前",
			"end_date":"昨天",
			"actions": ["参团详情","删除"]
		}]
		"""
	When jobs对"团购活动1"进行"开启"操作
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动1",
			"opengroup_num":"",
			"consumer_num":"",
			"visitor_num":"",
			"status":"进行中",
			"start_date":"今天",
			"end_date":"明天",
			"actions": ["参团详情","编辑","开启"]
		},{
			"name":"团购活动2",
			"opengroup_num":"",
			"consumer_num":"",
			"visitor_num":"",
			"status":"未开启",
			"start_date":"明天",
			"end_date":"2天后",
			"actions": ["参团详情","编辑","开启"]
		},{
			"name":"团购活动3",
			"opengroup_num":"",
			"consumer_num":"",
			"visitor_num":"",
			"status":"已结束",
			"start_date":"3天前",
			"end_date":"昨天",
			"actions": ["参团详情","删除"]
		}]
		"""

@mall2 @apps_group @apps_powerme_backend @apps_group_list
Scenario:1 团购活动列表查询
	Given jobs登录系统
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动1",
			"opengroup_num":"",
			"consumer_num":"",
			"visitor_num":"",
			"status":"进行中",
			"start_date":"今天",
			"end_date":"明天",
			"actions": ["参团详情","编辑","开启"]
		},{
			"name":"团购活动2",
			"opengroup_num":"",
			"consumer_num":"",
			"visitor_num":"",
			"status":"未开启",
			"start_date":"明天",
			"end_date":"2天后",
			"actions": ["参团详情","编辑","开启"]
		},{
			"name":"团购活动3",
			"opengroup_num":"",
			"consumer_num":"",
			"visitor_num":"",
			"status":"已结束",
			"start_date":"3天前",
			"end_date":"昨天",
			"actions": ["参团详情","删除"]
		}]
		"""
	#空查询（默认查询）
		When jobs设置团购活动列表查询条件
			"""
			{}
			"""
		Then jobs获得团购活动列表
			"""
			[{
				"name":"团购活动1"
			},{
				"name":"团购活动2"
			},{
				"name":"团购活动3"
			}]
			"""
	#活动名称
		#模糊匹配
			When jobs设置团购活动列表查询条件
				"""
				{
					"name":"团购"
				}
				"""
			Then jobs获得微助力活动列表
				"""
				[{
					"name":"团购活动1"
				},{
					"name":"团购活动2"
				},{
					"name":"团购活动3"
				}]
				"""
		#精确匹配
			When jobs设置团购活动列表查询条件
				"""
				{
					"name":"团购活动3"
				}
				"""
			Then jobs获得团购活动列表
				"""
				[{
					"name":"团购活动3"
				}]
				"""
		#查询结果为空
			When jobs设置团购活动列表查询条件
				"""
				{
					"name":"测试"
				}
				"""
			Then jobs获得团购活动列表
				"""
				[]
				"""
	#状态（全部、未开始、进行中、已结束）
		When jobs设置团购活动列表查询条件
			"""
			{
				"status":"全部"
			}
			"""
		Then jobs获得团购活动列表
			"""
			[{
				"name":"团购活动1",
				"status":"进行中"
			},{
				"name":"团购活动2",
				"status":"未开启"
			},{
				"name":"团购活动3",
				"status":"已结束"
			}]
			"""
		When jobs设置团购活动列表查询条件
			"""
			{
				"status":"进行中"
			}
			"""
		Then jobs获得团购活动列表
			"""
			[{
				"name":"团购活动1",
				"status":"进行中"
			}]
			"""
	#活动时间
		#开始时间非空，结束时间为空
			When jobs设置团购活动列表查询条件
				"""
				{
					"start_date":"今天",
					"end_date":""
				}
				"""
			Then jobs获得团购活动列表
				"""
				[{
					"name":"团购活动1",
					"start_date":"今天",
					"end_date":"明天"
				},{
					"name":"团购活动2",
					"start_date":"明天",
					"end_date":"2天后"
				}]
				"""

		#开始时间为空，结束时间非空
			When jobs设置团购活动列表查询条件
				"""
				{
					"start_date":"",
					"end_date":"今天"
				}
				"""
			Then jobs获得团购活动列表
				"""
				[{
					"name":"团购活动3",
					"start_date":"3天前",
					"end_date":"昨天"
				}]
				"""

		#开始时间与结束时间相等
			When jobs设置团购活动列表查询条件
				"""
				{
					"start_date":"今天",
					"end_date":"今天"
				}
				"""
			Then jobs获得团购活动列表
				"""
				[]
				"""

		#开始时间和结束时间不相等
			When jobs设置团购活动列表查询条件
				"""
				{
					"start_date":"3天前",
					"end_date":"明天"
				}
				"""
			Then jobs获得微助力活动列表
				"""
				[{
					"name":"团购活动1",
					"start_date":"今天",
					"end_date":"明天"
				},{
					"name":"团购活动3",
					"start_date":"3天前",
					"end_date":"昨天"
				}]
				"""
		#组合条件查询
		When jobs设置团购活动列表查询条件
			"""
			{
				"name":"团购活动2",
				"status":"未开启",
				"start_date":"明天",
				"end_date":"3天后"
			}
			"""
		Then jobs获得团购活动列表
			"""
			[{
				"name":"团购活动2",
				"start_date":"明天",
				"end_date":"2天后"
			}]
			"""

@mall2 @apps_group @apps_powerme_backend @apps_group_list
Scenario:2 团购活动列表分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""
		#Then jobs获得团购活动列表共'3'页

	When jobs访问团购活动列表第'1'页
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动1",
			"opengroup_num":"",
			"consumer_num":"",
			"visitor_num":"",
			"status":"进行中",
			"start_date":"今天",
			"end_date":"明天",
			"actions": ["参团详情","编辑","开启"]
		}]
		"""
	When jobs访问团购活动列表下一页
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动2",
			"opengroup_num":"",
			"consumer_num":"",
			"visitor_num":"",
			"status":"未开启",
			"start_date":"明天",
			"end_date":"2天后",
			"actions": ["参团详情","编辑","开启"]
		}]
		"""
	When jobs访问团购活动列表第'3'页
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动3",
			"opengroup_num":"",
			"consumer_num":"",
			"visitor_num":"",
			"status":"已结束",
			"start_date":"3天前",
			"end_date":"昨天",
			"actions": ["参团详情","删除"]
		}]
		"""
	When jobs访问团购活动列表上一页
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动2",
			"opengroup_num":"",
			"consumer_num":"",
			"visitor_num":"",
			"status":"未开启",
			"start_date":"明天",
			"end_date":"2天后",
			"actions": ["参团详情","编辑","开启"]
		}]
		"""
