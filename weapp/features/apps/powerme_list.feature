#_author_:张三香 2015.11.23

Feature:微助力活动列表
"""
	说明：
		1 微助力活动列表的"查询":
			【活动名称】：支持模糊查询
			【状态】：默认为'全部'，下拉框显示：全部、未开始、进行中和已结束
			【活动时间】：开始时间和结束时间允许为空

		2 微助力活动列表的"分页"，每10条记录一页
"""
Background:
	Given jobs登录系统
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	When jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1"
		}
		"""
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码1",
			"create_time": "2015-10-10 10:20:30",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "分组1",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "感谢您的的参与，为好友助力成功！"
		}]
		"""
	When jobs新建微助力活动
		"""
		[{
			"name":"微助力活动1",
			"start_date":"3天前",
			"end_date":"昨天",
			"is_show_countdown":"false",
			"desc":"微助力活动描述1",
			"reply":"微助力活动",
			"qr_code":"带参数二维码1",
			"share_pic":"1.jpg",
			"background_pic":"2.jpg",
			"background_color":"冬日暖阳",
			"rules":"获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式"
		},{
			"name":"微助力活动2",
			"start_date":"明天",
			"end_date":"3天后",
			"is_show_countdown":"ture",
			"desc":"微助力活动描述2",
			"reply":"微助力活动",
			"qr_code":"",
			"share_pic":"1.jpg",
			"background_pic":"2.jpg",
			"background_color":"玫瑰茜红",
			"rules":"获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式"
		},{
			"name":"微助力活动3",
			"start_date":"今天",
			"end_date":"3天后",
			"is_show_countdown":"false",
			"desc":"微助力活动描述3",
			"reply":"微助力活动",
			"qr_code":"",
			"share_pic":"1.jpg",
			"background_pic":"2.jpg",
			"background_color":"热带橙色",
			"rules":"获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式"
		}]
		"""

@apps @apps_powerme @apps_powerme_backend
Scenario:1 微助力活动列表查询
	Given jobs登录系统
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动3",
			"start_date":"今天",
			"end_date":"3天后",
			"status":"进行中",
			"parti_person_cnt":0,
			"actions": ["查看","预览","复制链接","关闭"]
		},{
			"name":"微助力活动2",
			"start_date":"明天",
			"end_date":"3天后",
			"status":"未开始",
			"parti_person_cnt":0,
			"actions": ["查看","预览","复制链接","关闭"]
		},{
			"name":"微助力活动1",
			"start_date":"3天前",
			"end_date":"昨天",
			"status":"已结束",
			"parti_person_cnt":0,
			"actions": ["查看","预览","复制链接","删除"]
		}]
		"""
	#空查询（默认查询）
		When jobs设置微助力活动列表查询条件
			"""
			{}
			"""
		Then jobs获得微助力活动列表
			"""
			[{
				"name":"微助力活动3"
			},{
				"name":"微助力活动2"
			},{
				"name":"微助力活动1"
			}]
			"""

	#活动名称
		#模糊匹配
			When jobs设置微助力活动列表查询条件
				"""
				{
					"name":"微助力"
				}
				"""
			Then jobs获得微助力活动列表
				"""
				[{
					"name":"微助力活动3"
				},{
					"name":"微助力活动2"
				},{
					"name":"微助力活动1"
				}]
				"""
		#精确匹配
			When jobs设置微助力活动列表查询条件
				"""
				{
					"name":"微助力活动3"
				}
				"""
			Then jobs获得微助力活动列表
				"""
				[{
					"name":"微助力活动3"
				}]
				"""
		#查询结果为空
			When jobs设置微助力活动列表查询条件
				"""
				{
					"name":"测试"
				}
				"""
			Then jobs获得微助力活动列表
				"""
				[]
				"""

	#状态（全部、未开始、进行中、已结束）
		When jobs设置微助力活动列表查询条件
			"""
			{
				"status":"全部"
			}
			"""
		Then jobs获得微助力活动列表
			"""
			[{
				"name":"微助力活动3",
				"status":"进行中"
			},{
				"name":"微助力活动2",
				"status":"未开始"
			},{
				"name":"微助力活动1",
				"status":"已结束"
			}]
			"""
		When jobs设置微助力活动列表查询条件
			"""
			{
				"status":"进行中"
			}
			"""
		Then jobs获得微助力活动列表
			"""
			[{
				"name":"微助力活动3",
				"status":"进行中"
			}]
			"""

	#活动时间
		#开始时间非空，结束时间为空
			When jobs设置微助力活动列表查询条件
				"""
				{
					"stare_date":"今天",
					"end_date":""
				}
				"""
			Then jobs获得微助力活动列表
				"""
				[{
					"name":"微助力活动3",
					"start_date":"今天",
					"end_date":"3天后"
				},{
					"name":"微助力活动2",
					"start_date":"明天",
					"end_date":"3天后"
				}]
				"""
		#开始时间为空，结束时间非空
			When jobs设置微助力活动列表查询条件
				"""
				{
					"stare_date":"",
					"end_date":"今天"
				}
				"""
			Then jobs获得微助力活动列表
				"""
				[{
					"name":"微助力活动1",
					"start_date":"3天前",
					"end_date":"昨天"
				}]
				"""
		#开始时间与结束时间相等
			When jobs设置微助力活动列表查询条件
				"""
				{
					"stare_date":"今天",
					"end_date":"今天"
				}
				"""
			Then jobs获得微助力活动列表
				"""
				[]
				"""

@apps @apps_powerme @apps_powerme_backend
Scenario:2 微助力活动列表分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""
		#Then jobs获得微助力活动列表共'3'页

	When jobs访问微助力活动列表第'1'页
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动3",
			"start_date":"今天",
			"end_date":"3天后",
			"status":"进行中",
			"parti_person_cnt":0,
			"actions": ["查看","预览","复制链接","关闭"]
		}]
		"""
	When jobs访问微助力活动列表下一页
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动2",
			"start_date":"明天",
			"end_date":"3天后",
			"status":"未开始",
			"parti_person_cnt":0,
			"actions": ["查看","预览","复制链接","关闭"]
		}]
		"""
	When jobs访问微助力活动列表第'3'页
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动1",
			"start_date":"3天前",
			"end_date":"昨天",
			"status":"已结束",
			"parti_person_cnt":0,
			"actions": ["查看","预览","复制链接","删除"]
		}]
		"""
	When jobs访问微助力活动列表上一页
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动2",
			"start_date":"明天",
			"end_date":"3天后",
			"status":"未开始",
			"parti_person_cnt":0,
			"actions": ["查看","预览","复制链接","关闭"]
		}]
		"""