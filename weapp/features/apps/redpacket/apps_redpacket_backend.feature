# __author__ : 许韦 2016.01.20

Feature: 新建红包活动
	"""
		用户通过拼红包活动获得好友点赞和帮助好友点赞
		1.【活动名称】:必填项，不超过30个字符
		2.【活动时间】:必填项
		3.显示倒计时:勾选则在活动页面显示倒计时：图标：xx天xx时xx分xx秒
		4.【红包方式】：分为拼手气红包和普通红包
		5.【好友贡献金额区间】：为分享好友后，每个好友贡献的金额区间
		6.【参与活动回复语】:必填项，不超过5个字符，需在微信-自动回复创建该关键词
		7.【用户识别二维码】：非必填项，此处若空缺，则使用公众号二维码代替
		8.【活动规则】：非必填项，不超过500个字符
		9.【分享图标】：必填项，建议图片长宽100px*100px，正方形图片
		10.【分享描述】：必填项，不超过26个字符

	"""

Background:
	Given jobs登录系统
	When jobs添加会员分组
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
@mall2 @apps @apps_redpacket @apps_redpacket_backend
Scenario:1 新建拼手气红包活动，用户二维码为空
	Given jobs登录系统
	When jobs新建拼红包活动
		"""
		[{
			"name":"拼红包活动1",
			"start_date":"今天",
			"end_date":"明天",
			"is_show_countdown":"true",
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
		}]
		"""
	Then jobs获得拼红包活动列表
		"""
		[{
			"name":"拼红包活动1",
			"participant_count":"0",
			"type":"拼手气",
			"status":"进行中",
			"total_money":"500.00",
			"already_paid_money":"0.00",
			"start_date":"今天",
			"end_date":"明天",
			"actions": ["查看","预览","复制链接"]
		}]
		"""

@mall2 @apps @apps_redpacket @apps_redpacket_backend
Scenario:2 新建普通红包活动，用户二维码非空
	Given jobs登录系统
	When jobs新建普通红包活动
		"""
		[{
			"name":"拼红包活动2",
			"start_date":"明天",
			"end_date":"2天后",
			"is_show_countdown":"false",
			"red_packet":{
				"type":"regular",
				"random_total_money":"",
				"random_packets_number":"",
				"regular_packets_number":"10",
				"regular_per_money":"10"
			},
			"contribution_start_range":"0.5",
			"contribution_end_range":"1.5",
			"reply":"拼红包",
			"qr_code":"带参数二维码1",
			"open_packet_reply":"点赞帮好友赢现金红包",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
			"share_pic":"2.jpg",
			"share_desc":"分享到朋友圈邀请好友点赞集齐红包金额即可获得现金奖励!"
		}]
		"""
	Then jobs获得拼红包活动列表
		"""
		[{
			"name":"拼红包活动2",
			"participant_count":"0",
			"type":"普通",
			"status":"未开始",
			"total_money":"100.00",
			"already_paid_money":"0.00",
			"start_date":"明天",
			"end_date":"2天后",
			"actions": ["查看","预览","复制链接"]
		}]
		"""