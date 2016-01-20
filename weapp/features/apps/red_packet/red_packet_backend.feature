# __author__ : 许韦

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
		10.【分项描述】：必填项，不超过26个字符

	"""

Background:
	Given jobs登录系统
	When jobs添加带参数二维码
		"""
		[{
			"code_name":"带参数二维码1",
			"create_time":"2015-10-10 10:20:30",
			"prize_type":"无奖励",
			"member_rank":"普通会员",
			"tags":"未分组",
			"is_attention_in":"false",
			"remarks":"",
			"is_relation_member":"false",
			"reply_type":"文字",
			"scan_code_reply":"感谢您的参与，为好友点赞成功！"
		}]
		"""
@mall2 @apps_red_packet @apps_red_packet_backend
Scenario:1 新建拼手气红包活动，用户二维码为空
	Given jobs登录系统
	When jobs新建拼红包活动
		"""
		[{
			"name":"拼红包活动1",
			"start_date":"今天",
			"end_date":"明天",
			"is_show_countdown":"ture",
			"red_packet":[{
				"type":"拼手气红包",
				"total_amount":"500",
				"packet_num":"10"	
			}],
			"contribution_start_range":"0.5",
			"contribution_end_range":"1.5",
			"reply":"拼红包",
			"qr_code":"",
			"license":"apiclient_cert.pem",
			"license_key":"apiclient_key.pem",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
			"share_pic":"1.jpg",
			"share_describe":"分享到朋友圈邀请好友点赞集齐红包金额即可获得现金奖励!"
		}]
		"""
	Then jobs获得拼红包活动列表
		"""
		[{
			"name":"拼红包活动1",
			"participant_count":"0",
			"type":"拼手气",
			"status":"进行中",
			"total_amount":"10",
			"send_amount":"0",
			"start_date":"今天",
			"end_date":"明天",
			"actions": ["关闭","链接","预览","查看"]
		}]
		"""

@mall2 @apps_red_packet @apps_red_packet_backend
Scenario:2 新建普通红包活动，用户二维码非空
	Given jobs登录系统
	When jobs新建普通红包活动
		"""
		[{
			"name":"拼红包活动2",
			"start_date":"明天",
			"end_date":"两天后",
			"is_show_countdown":"false",
			"red_packet":[{
				"type":"普通红包",
				"packet_num":"10",
				"single_packet_amount":"10"
			}]
			"contribution_start_range":"0.5",
			"contribution_end_range":"1.5",
			"reply":"拼红包",
			"qr_code":"带参数二维码1",
			"license":"apiclient_cert.pem",
			"license_key":"apiclient_key.pem",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
			"share_pic":"1.jpg",
			"share_describe":"分享到朋友圈邀请好友点赞集齐红包金额即可获得现金奖励!"
		}]
		"""
	Then jobs获得拼红包活动列表
		"""
		[{
			"name":"拼红包活动2",
			"participant_count":"0",
			"type":"普通",
			"status":"未开始",
			"total_amount":"100",
			"send_amount":"0",
			"start_date":"明天",
			"end_date":"两天后",
			"actions": ["删除","链接","预览","查看"]
		}]
		"""