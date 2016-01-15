#_auther_:许韦

Feature: 拼红包活动列表
	"""
	说明：
		1.拼红包活动列表的"查询"：
			【活动名称】：支持模糊查询
			【状态】：默认为"全部"，下拉框显示：全部、未开始、进行中和已结束
			【活动时间】：开始时间和结束时间允许为空
		2.拼红包活动列表的"分页"，每10条记录一页
	"""

Background:
	Given jobs登录系统
	And jobs添加会员分组
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
			"scan_code_reply": "感谢您的参与，为好友点赞成功！"
		}]
		"""
	When jobs新建拼红包活动
		"""
		[{
			"name":"拼红包活动1",
			"start_date":"今天",
			"end_date":"明天",
			"is_show_countdown":"ture",
			"red_packet":{
				"type":"random",
				"random_total_money":"500",
				"random_packets_number":"10",
				"regular_packets_number":"",
				"regular_per_money":""
			},
			"contribution_start_range":"0.5",
			"contribution_end_range":"1.5",
			"reply":"拼红包",
			"qr_code":"",
			"open_packet_reply":"点赞帮好友赢现金红包",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
			"share_pic":"1.jpg",
			"share_desc":"分享到朋友圈邀请好友点赞集齐红包金额即可获得现金奖励!"
		},{
			"name":"拼红包活动2",
			"start_date":"明天",
			"end_date":"2天后",
			"is_show_countdown":"false",
			"red_packet":{
				"type":"normal",
				"random_total_money":"",
				"random_packets_number":"",
				"regular_packets_number":"10",
				"regular_per_money":"10"
			},
			"contribution_start_range":"0.1",
			"contribution_end_range":"2",
			"reply":"拼红包",
			"qr_code":"带参数二维码1",
			"open_packet_reply":"点赞帮好友赢现金红包",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
			"share_pic":"2.jpg",
			"share_desc":"分享到朋友圈邀请好友点赞集齐红包金额即可获得现金奖励!"
		},{
			"name":"拼红包活动3",
			"start_date":"2天前",
			"end_date":"昨天",
			"is_show_countdown":"true",
			"red_packet":{
				"type":"normal",
				"random_total_money":"",
				"random_packets_number":"",
				"regular_packets_number":"5",
				"regular_per_money":"30"
			},
			"contribution_start_range":"1",
			"contribution_end_range":"3",
			"reply":"拼红包",
			"qr_code":"",
			"open_packet_reply":"点赞帮好友赢现金红包",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
			"share_pic":"3.jpg",
			"share_desc":"分享到朋友圈邀请好友点赞集齐红包金额即可获得现金奖励!"
		}]
		"""
@mall2 @apps_redpacket @apps_redpacket_list
Scenario:1 拼红包活动列表查询
	Given jobs登录系统
	Then jobs获得拼红包活动列表
		"""
		[{
			"name":"拼红包活动3",
			"participant_count":"0",
			"type":"普通",
			"status":"已结束",
			"total_money":"150.00",
			"already_paid_money":"0.00",
			"start_date":"2天前",
			"end_date":"昨天",
			"actions":["查看","预览","复制链接","删除"]
		},{
			"name":"拼红包活动2",
			"participant_count":"0",
			"type":"普通",
			"status":"未开始",
			"total_money":"100.00",
			"already_paid_money":"0.00",
			"start_date":"明天",
			"end_date":"2天后",
			"actions": ["查看","预览","复制链接"]
		},{
			"name":"拼红包活动1",
			"participant_count":"0",
			"type":"拼手气",
			"status":"进行中",
			"total_money":"500.00",
			"already_paid_money":"0.00",
			"start_date":"今天",
			"end_date":"明天",
			"actions":["查看","预览","复制链接"]
		}]
		"""
	#空查询（默认查询）
		When jobs设置拼红包活动列表查询条件
			"""
			{}
			"""
		Then jobs获得拼红包活动列表
			"""
			[{
				"name":"拼红包活动3"
			},{
				"name":"拼红包活动2"
			},{
				"name":"拼红包活动1"
			}]
			"""
	#活动名称
		#模糊匹配
			When jobs设置拼红包活动列表查询条件
				"""
				{
					"name":"拼红包"
				}
				"""
			Then jobs获得拼红包活动列表
				"""
				[{
					"name":"拼红包活动3"
				},{
					"name":"拼红包活动2"
				},{
					"name":"拼红包活动1"
				}]
				"""
		#精确匹配
			When jobs设置拼红包活动列表查询条件
				"""
				{
					"name":"拼红包活动3"
				}
				"""
			Then jobs获得拼红包活动列表
				"""
				[{
					"name":"拼红包活动3"
				}]
				"""
		#查询结果为空
			When jobs设置拼红包活动列表查询条件
				"""
				{
					"name":"测试"
				}
				"""
			Then jobs获得拼红包活动列表
				"""
				[]
				"""
		#状态（全部、未开始、进行中、已结束）
			When jobs设置拼红包活动列表查询条件
				"""
				{
					"status":"全部"
				}
				"""
			Then jobs获得拼红包活动列表
				"""
				[{
					"name":"拼红包活动3",
					"status":"已结束"
				},{
					"name":"拼红包活动2",
					"status":"未开始"
				},{
					"name":"拼红包活动1",
					"status":"进行中"
				}]
				"""
			When jobs设置拼红包活动列表查询条件
				"""
				{
					"status":"进行中"
				}
				"""
			Then jobs获得拼红包活动列表
				"""
				[{
					"name":"拼红包活动1",
					"status":"进行中"
				}]
				"""
	#活动时间
		#开始时间非空，结束时间为空
			When jobs设置拼红包活动列表查询条件
				"""
				{
					"start_date":"今天",
					"end_date":""
				}
				"""
			Then jobs获得拼红包活动列表
				"""
				[{
					"name":"拼红包活动2",
					"start_date":"明天",
					"end_date":"2天后"
				},{
					"name":"拼红包活动1",
					"start_date":"今天",
					"end_date":"明天"
				}]
				"""

		#开始时间为空，结束时间非空
			When jobs设置拼红包活动列表查询条件
				"""
				{
					"start_date":"",
					"end_date":"今天"
				}
				"""
			Then jobs获得拼红包活动列表
				"""
				[{
					"name":"拼红包活动3",
					"start_date":"2天前",
					"end_date":"昨天"
				}]
				"""

		#开始时间与结束时间相等
			When jobs设置拼红包活动列表查询条件
				"""
				{
					"start_date":"今天",
					"end_date":"今天"
				}
				"""
			Then jobs获得拼红包活动列表
				"""
				[]
				"""

		#开始时间和结束时间不相等
			When jobs设置拼红包活动列表查询条件
				"""
				{
					"start_date":"2天前",
					"end_date":"明天"
				}
				"""
			Then jobs获得拼红包活动列表
				"""
				[{
					"name":"拼红包活动3",
					"start_date":"2天前",
					"end_date":"昨天"
				},{
					"name":"拼红包活动1",
					"start_date":"今天",
					"end_date":"明天"
				}]
				"""

	#组合条件查询
		When jobs设置拼红包活动列表查询条件
			"""
			{
				"name":"拼红包活动2",
				"status":"未开始",
				"start_date":"明天",
				"end_date":"2天后"
			}
			"""
		Then jobs获得拼红包活动列表
			"""
			[{
				"name":"拼红包活动2",
				"start_date":"明天",
				"end_date":"2天后"
			}]
			"""
@mall2 @apps_redpacket @apps_redpacket_list
Scenario:2 拼红包活动列表分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""
		#Then jobs获得拼红包活动列表共'3'页

	When jobs访问拼红包活动列表第'1'页
	Then jobs获得拼红包活动列表
		"""
		[{
			"name":"拼红包活动3",
			"start_date":"2天前",
			"end_date":"昨天",
			"status":"已结束",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","删除"]
		}]
		"""
	When jobs访问拼红包活动列表下一页
	Then jobs获得拼红包活动列表
		"""
		[{
			"name":"拼红包活动2",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"participant_count":0,
			"actions": ["查看","预览","复制链接"]
		}]
		"""
	When jobs访问拼红包活动列表第'3'页
	Then jobs获得拼红包活动列表
		"""
		[{
			"name":"拼红包活动1",
			"start_date":"今天",
			"end_date":"明天",
			"status":"进行中",
			"participant_count":0,
			"actions": ["查看","预览","复制链接"]
		}]
		"""
	When jobs访问拼红包活动列表上一页
	Then jobs获得拼红包活动列表
		"""
		[{
			"name":"拼红包活动2",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"participant_count":0,
			"actions": ["查看","预览","复制链接"]
		}]
		"""