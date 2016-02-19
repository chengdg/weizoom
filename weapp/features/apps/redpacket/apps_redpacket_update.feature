# __author__ : 许韦 2016.01.20

Feature: 更新拼红包活动
	"""
		1 编辑拼红包活动:只能编辑'未开始'状态的，'进行中'和'已结束'状态的不能进行编辑

		2 删除拼红包活动:只能删除'已结束'状态的，'未开始'和'进行中'的不能进行删除

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
			"code_name":"带参数二维码1",
			"create_time":"2015-10-10 10:20:30",
			"prize_type":"无奖励",
			"member_rank":"普通会员",
			"tags":"分组1",
			"is_attention_in":"false",
			"remarks":"",
			"is_relation_member":"false",
			"reply_type":"文字",
			"scan_code_reply":"感谢您的参与，为好友点赞成功！"
		}]
		"""
	When jobs新建拼红包活动
		"""
		[{
			"name":"活动1",
			"start_date":"3天后",
			"end_date":"5天后",
			"is_show_countdown":"true",
			"red_packet":{
				"type":"random",
				"random_total_money":"200",
				"random_packets_number":"20",
				"regular_packets_number":"",
				"regular_per_money":""
			},
			"contribution_start_range":"0.5",
			"contribution_end_range":"1.0",
			"reply":"拼红包",
			"qr_code":"",
			"open_packet_reply":"点赞帮好友赢现金红包",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
			"share_pic":"1.jpg",
			"share_desc":"分享到朋友圈邀请好友点赞集齐红包金额即可获得现金奖励!"
		},{
			"name":"活动2",
			"start_date":"2天前",
			"end_date":"2天后",
			"is_show_countdown":"false",
			"red_packet":{
				"type":"regular",
				"random_total_money":"",
				"random_packets_number":"",
				"regular_packets_number":"10",
				"regular_per_money":"10"
			},
			"contribution_start_range":"1.0",
			"contribution_end_range":"2.0",
			"reply":"拼红包",
			"qr_code":"带参数二维码1",
			"open_packet_reply":"点赞帮好友赢现金红包",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
			"share_pic":"2.jpg",
			"share_desc":"分享到朋友圈邀请好友点赞集齐红包金额即可获得现金奖励!"
		}
		,{
			"name":"活动3",
			"start_date":"2天前",
			"end_date":"昨天",
			"is_show_countdown":"true",
			"red_packet":{
				"type":"random",
				"random_total_money":"20",
				"random_packets_number":"10",
				"regular_packets_number":"",
				"regular_per_money":""
			},
			"contribution_start_range":"0.25",
			"contribution_end_range":"1.25",
			"reply":"拼红包",
			"qr_code":"",
			"open_packet_reply":"点赞帮好友赢现金红包",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
			"share_pic":"3.jpg",
			"share_desc":"分享到朋友圈邀请好友点赞集齐红包金额即可获得现金奖励!"
		}]
		"""

@mall2 @apps @apps_redpacket @apps_redpacket_update @kuki
Scenario:1 编辑"未开始"的拼红包活动
	Given jobs登录系统
	When jobs编辑拼红包活动'活动1'
		"""
		[{
			"name":"拼红包活动1",
			"start_date":"今天",
			"end_date":"3天后",
			"is_show_countdown":"false",
			"red_packet":{
				"type":"regular",
				"random_total_money":"",
				"random_packets_number":"",
				"regular_packets_number":"5",
				"regular_per_money":"10"
			},
			"contribution_start_range":"1.5",
			"contribution_end_range":"2.0",
			"reply":"抢红包",
			"qr_code":"带参数二维码1",
			"open_packet_reply":"集齐红包金额即可领取现金奖励！",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
			"share_pic":"4.jpg",
			"share_desc":"这是一个神奇的活动！"
		}]
		"""
	Then jobs获得拼红包活动列表
		"""
		[{
			"name":"活动3",
			"start_date":"2天前",
			"end_date":"昨天",
			"type":"拼手气",
			"status":"已结束",
			"participant_count":"0",
			"total_money":"20.00",
			"already_paid_money":"0.00",
			"actions": ["查看","预览","复制链接","删除"]
		},{
			"name":"活动2",
			"start_date":"2天前",
			"end_date":"2天后",
			"type":"普通",
			"status":"进行中",
			"participant_count":"0",
			"total_money":"100.00",
			"already_paid_money":"0.00",
			"actions": ["查看","预览","复制链接"]
		},{
			"name":"拼红包活动1",
			"start_date":"今天",
			"end_date":"3天后",
			"type":"普通",
			"status":"进行中",
			"participant_count":0,
			"total_money":"50.00",
			"already_paid_money":"0.00",
			"actions": ["查看","预览","复制链接"]
		}]
		"""
@mall2 @apps @apps_redpacket @apps_redpacket_update
Scenario:2 删除'已结束'的拼红包活动
	Given jobs登录系统
	When jobs删除拼红包活动'活动3'
	Then jobs获得拼红包活动列表
		"""
		[{
			"name":"活动2",
			"start_date":"2天前",
			"end_date":"2天后",
			"type":"普通",
			"status":"进行中",
			"participant_count":"0",
			"total_money":"100.00",
			"already_paid_money":"0.00",
			"actions": ["查看","预览","复制链接"]
		},{
			"name":"活动1",
			"start_date":"3天后",
			"end_date":"5天后",
			"type":"拼手气",
			"status":"未开始",
			"participant_count":"0",
			"total_money":"200.00",
			"already_paid_money":"0.00",
			"actions": ["查看","预览","复制链接"]
		}]
		"""

