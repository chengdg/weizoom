# watcher: wangli@weizoom.com,benchi@weizoom.com
#_author_:王丽 2015.12.02

Feature: 应用和营销-活动报名列表
"""
	可以对活动报名进行不同维度的插叙
	1 活动报名列表
		1）【活动名称】：创建活动报名时的填写的活动标题
		2）【参与人数】：报名参与此项活动的人数
		3）【奖项类型】：无奖励、积分、优惠券中的一种，显示此活动设置的奖励
		4）【开始时间】：活动有效时间的开始时间
		5）【结束时间】：活动有效时间的结束时间
		6）【状态】：未开始、进行中、已结束中的一种，根据现在的时间和活动的有效期判断
		7）【操作】：状态为"未开始"：预览、查看结果
					状态为"进行中"：关闭、预览、查看结果
					状态为"已结束"：删除、预览、查看结果
	2 分页显示，每页10条数据
	3 查询条件：
		【活动名称】：模糊匹配列表中的"活动名称"
		【状态】：下拉选择：所有活动、未开始、进行中、已结束
		【活动时间】：开始时间和结束时间，活动时间在查询期间内的活动
		【奖项类型】：下拉选择：所有奖品、积分、优惠券
"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 10,
			"limit_counts": 3,
			"start_date": "4天前",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建活动报名
		"""
		[{
			"title":"活动报名-无奖励",
			"subtitle":"活动报名-副标题-无奖励",
			"content":"内容描述-无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"permission":"必须关注才可参与",
			"prize_type": "无奖励",
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
						"is_selected":"false"
					},{
						"item_name":"住址",
						"is_selected":"false"
					}],
			"items_add":[{
						"item_name":"其他",
						"is_required":"false"
					}]
		},{
			"title":"活动报名-积分",
			"subtitle":"活动报名-副标题-积分",
			"content":"内容描述-积分",
			"start_date":"1天前",
			"end_date":"2天后",
			"permission":"必须关注才可参与",
			"prize_type": "积分",
			"integral": 50,
			"items_select":[{
						"item_name":"姓名",
						"is_selected":"true"
					},{
						"item_name":"手机",
						"is_selected":"true"
					},{
						"item_name":"邮箱",
						"is_selected":"false"
					},{
						"item_name":"QQ",
						"is_selected":"false"
					},{
						"item_name":"职位",
						"is_selected":"false"
					},{
						"item_name":"住址",
						"is_selected":"false"
					}],
			"items_add":[{
						"item_name":"店铺类型",
						"is_required":"true"
					},{
						"item_name":"开店时间",
						"is_required":"true"
					}]
		},{
			"title":"活动报名-优惠券",
			"subtitle":"活动报名-副标题-优惠券",
			"content":"内容描述-优惠券",
			"start_date":"3天前",
			"end_date":"1天前",
			"permission":"无需关注即可参与",
			"prize_type": "优惠券",
			"coupon":"优惠券1",
			"items_select":[{
						"item_name":"姓名",
						"is_selected":"true"
					},{
						"item_name":"手机",
						"is_selected":"true"
					},{
						"item_name":"邮箱",
						"is_selected":"false"
					},{
						"item_name":"QQ",
						"is_selected":"false"
					},{
						"item_name":"职位",
						"is_selected":"false"
					},{
						"item_name":"住址",
						"is_selected":"true"
					}],
			"items_add":[{
						"item_name":"店铺类型",
						"is_required":"true"
					},{
						"item_name":"开店时间",
						"is_required":"true"
					}]
		}]
		"""

@apps @event @evnet_list
Scenario:1 活动报名-列表查询
	Given jobs登录系统
	#按照"活动名称"查询
		#模糊匹配
			When jobs设置活动报名列表查询条件
				"""
				{
					"name":"活动报名"
				}
				"""
			Then jobs获得活动报名列表
				"""
				[{
					"name":"活动报名-优惠券",
					"participant_count": 0,
					"prize_type": "优惠券",
					"start_date":"3天前",
					"end_date":"1天前",
					"status":"已结束",
					"actions": ["删除","链接","预览","查看结果"]
				},{
					"name":"活动报名-积分",
					"participant_count": 0,
					"prize_type": "积分",
					"start_date":"1天前",
					"end_date":"2天后",
					"status":"进行中",
					"actions": ["关闭","链接","预览","查看结果"]
				},{
					"name":"活动报名-无奖励",
					"participant_count": 0,
					"prize_type": "无奖励",
					"start_date":"明天",
					"end_date":"2天后",
					"status":"未开始",
					"actions": ["链接","预览","查看结果"]
				}]
				"""
		#完全匹配
			When jobs设置活动报名列表查询条件
				"""
				{
					"name":"活动报名-无奖励"
				}
				"""
			Then jobs获得活动报名列表
				"""
				[{
					"name":"活动报名-无奖励",
					"participant_count": 0,
					"prize_type": "无奖励",
					"start_date":"明天",
					"end_date":"2天后",
					"status":"未开始",
					"actions": ["链接","预览","查看结果"]
				}]
				"""
		#查询结果为空
			When jobs设置活动报名列表查询条件
				"""
				{
					"name":"查询"
				}
				"""
			Then jobs获得活动报名列表
				"""
				[]
				"""

	#按照"状态"查询
		#未开始
			When jobs设置活动报名列表查询条件
				"""
				{
					"status":"未开始"
				}
				"""
			Then jobs获得活动报名列表
				"""
				[{
					"name":"活动报名-无奖励",
					"participant_count": 0,
					"prize_type": "无奖励",
					"start_date":"明天",
					"end_date":"2天后",
					"status":"未开始",
					"actions": ["链接","预览","查看结果"]
				}]
				"""
		#进行中
			When jobs设置活动报名列表查询条件
				"""
				{
					"status":"进行中"
				}
				"""
			Then jobs获得活动报名列表
				"""
				[{
					"name":"活动报名-积分",
					"participant_count": 0,
					"prize_type": "积分",
					"start_date":"1天前",
					"end_date":"2天后",
					"status":"进行中",
					"actions": ["关闭","链接","预览","查看结果"]
				}]
				"""
		#已结束
			When jobs设置活动报名列表查询条件
				"""
				{
					"status":"已结束"
				}
				"""
			Then jobs获得活动报名列表
				"""
				[{
					"name":"活动报名-优惠券",
					"participant_count": 0,
					"prize_type": "优惠券",
					"start_date":"3天前",
					"end_date":"1天前",
					"status":"已结束",
					"actions": ["删除","链接","预览","查看结果"]
				}]
				"""

	#按照"活动时间"查询
			When jobs设置活动报名列表查询条件
				"""
				{
					"start_date":"1天前",
					"end_date":"2天后"
				}
				"""
			Then jobs获得活动报名列表
				"""
				[{
					"name":"活动报名-积分",
					"participant_count": 0,
					"prize_type": "积分",
					"start_date":"1天前",
					"end_date":"2天后",
					"status":"进行中",
					"actions": ["关闭","链接","预览","查看结果"]
				},{
					"name":"活动报名-无奖励",
					"participant_count": 0,
					"prize_type": "无奖励",
					"start_date":"明天",
					"end_date":"2天后",
					"status":"未开始",
					"actions": ["链接","预览","查看结果"]
				}]
				"""

	#按照"奖项类型"查询
		#优惠券
			When jobs设置活动报名列表查询条件
				"""
				{
					"prize_type":"优惠券"
				}
				"""
			Then jobs获得活动报名列表
				"""
				[{
					"name":"活动报名-优惠券",
					"participant_count": 0,
					"prize_type": "优惠券",
					"start_date":"3天前",
					"end_date":"1天前",
					"status":"已结束",
					"actions": ["删除","链接","预览","查看结果"]
				}]
				"""
		#积分
			When jobs设置活动报名列表查询条件
				"""
				{
					"prize_type":"积分"
				}
				"""
			Then jobs获得活动报名列表
				"""
				[{
					"name":"活动报名-积分",
					"participant_count": 0,
					"prize_type": "积分",
					"start_date":"1天前",
					"end_date":"2天后",
					"status":"进行中",
					"actions": ["关闭","链接","预览","查看结果"]
				}]
				"""

	#混合查询
		When jobs设置活动报名列表查询条件
			"""
			{
				"name":"活动报名",
				"status":"未开始",
				"start_date":"1天前",
				"end_date":"2天后",
				"prize_type":"所有奖品"
			}
			"""
		Then jobs获得活动报名列表
			"""
			[{
				"name":"活动报名-无奖励",
				"participant_count": 0,
				"prize_type": "无奖励",
				"start_date":"明天",
				"end_date":"2天后",
				"status":"未开始",
				"actions": ["链接","预览","查看结果"]
			}]
			"""

	#默认查询
		When jobs设置活动报名列表查询条件
			"""
			{
				"name":"",
				"status":"所有活动",
				"start_date":"",
				"end_date":"",
				"prize_type":"所有奖品"
			}
			"""
		Then jobs获得活动报名列表
			"""
			[{
				"name":"活动报名-优惠券",
				"participant_count": 0,
				"prize_type": "优惠券",
				"start_date":"3天前",
				"end_date":"1天前",
				"status":"已结束",
				"actions": ["删除","链接","预览","查看结果"]
			},{
				"name":"活动报名-积分",
				"participant_count": 0,
				"prize_type": "积分",
				"start_date":"1天前",
				"end_date":"2天后",
				"status":"进行中",
				"actions": ["关闭","链接","预览","查看结果"]
			},{
				"name":"活动报名-无奖励",
				"participant_count": 0,
				"prize_type": "无奖励",
				"start_date":"明天",
				"end_date":"2天后",
				"status":"未开始",
				"actions": ["链接","预览","查看结果"]
			}]
			"""

@apps @event @evnet_list
Scenario:2 活动报名-列表分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""
	When jobs访问百宝箱活动报名列表第'1'页
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-优惠券",
			"participant_count": 0,
			"prize_type": "优惠券",
			"start_date":"3天前",
			"end_date":"1天前",
			"status":"已结束",
			"actions": ["删除","链接","预览","查看结果"]
		}]
		"""
	When jobs访问百宝箱活动报名列表第'1'页
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-优惠券",
			"participant_count": 0,
			"prize_type": "优惠券",
			"start_date":"3天前",
			"end_date":"1天前",
			"status":"已结束",
			"actions": ["删除","链接","预览","查看结果"]
		}]

		"""
	When jobs访问活动报名列表下一页
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-积分",
			"participant_count": 0,
			"prize_type": "积分",
			"start_date":"1天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","查看结果"]
		}]
		"""
	When jobs访问百宝箱活动报名列表第'3'页
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-无奖励",
			"participant_count": 0,
			"prize_type": "无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["链接","预览","查看结果"]
		}]
		"""
	When jobs访问活动报名列表上一页
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-积分",
			"participant_count": 0,
			"prize_type": "积分",
			"start_date":"1天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","查看结果"]
		}]
		"""
