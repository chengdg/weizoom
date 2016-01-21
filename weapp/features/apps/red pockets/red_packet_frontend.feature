# __author__ : 许韦

Feature: 会员参加拼红包活动
	"""

	"""

Background:
	Given jobs登录系统
	And jobs添加带参数二维码
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
			scan_code_reply":"感谢您的参与，为好友点赞成功！"
		}]
		"""
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
		},{
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
	When jobs已添加单图文
		"""
		[{
			"title":"拼红包活动1单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容",
			"jump_url":"拼红包-拼红包活动1"
		},{
			"title":"拼红包活动2单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文2文本摘要",
			"content":"单条图文2文本内容",
			"jump_url":"拼红包-拼红包活动2"
		}]
		"""
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": [{
					"keyword": "拼红包活动1",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"拼红包活动1单图文",
					"reply_type":"text_picture"
				}]
		},{
			"rules_name":"规则2",
			"keyword": [{
					"keyword": "拼红包活动2",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"拼红包活动2单图文",
					"reply_type":"text_picture"
				}]
		}]
		"""

@mall2 @apps_red_packet @apps_red_packet_frontend
Scenario:1 非会员通过会员分享的活动链接为其点赞（没有参数二维码）
	#非会员tom点击会员bill分享的链接为bill点赞，弹层显示公众号二维码
	#tom关注jobs的公众号
	#更新贡献好友列表，bill活动页显示tom已贡献金额
	When bill关注jobs的公众号
	When bill访问jobs的weapp
	When bill在微信中向jobs的公众号发送消息"拼红包活动1"
	Then bill收到自动回复"拼红包活动1单图文"
	When bill点击图文"拼红包活动1单图文"进入拼红包活动页面
	Then bill获得jobs的"拼红包活动1"的内容
		"""
		[{	
			"name":"拼红包活动1",
			"is_show_countdown":"true",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放现金奖励"
		}]
		"""
	When 更新贡献好友列表
	Then bill获得"拼红包活动1"的已贡献好友列表
		"""
		[]
		"""
	When bill把jobs的拼红包活动链接分享到朋友圈
	When tom关注jobs的公众号
	When tom访问jobs的weapp
	When tom取消关注jobs的公众号
	When tom点击bill分享的拼红包活动链接点赞
	#Then tom获得弹层提示信息'1.长按二维码关注"惠中大酒店"公众<br />号<br />2.回复："拼红包活动1",即可参加活动'
	When tom通过识别弹层中的公众号二维码关注jobs的公众号
	#关注成功后，点赞成功即bill获得一个随机金额的红包
	When bill访问jobs的weapp
	When bill在微信中向jobs的公众号发送消息"拼红包活动1"
	Then bill收到自动回复"拼红包活动1单图文"
	When bill点击图文"拼红包活动1单图文"进入拼红包活动页面
	Then bill获得jobs的"拼红包活动1"的内容
		"""
		[{	
			"name":"拼红包活动1",
			"is_show_countdown":"true",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放"
		}]
		"""
	When 更新贡献好友列表
	Then bill获得"拼红包活动1"的已贡献好友列表
		| name |
		| tom  |

@mall2 @apps_red_packet @apps_red_packet_frontend
Scenario:2 非会员通过会员分享的活动链接为其点赞（带参数二维码）
	#非会员tom点击会员bill分享的链接为bill点赞，弹层显示带参数二维码
	#tom关注jobs的公众号
	#更新贡献好友列表，bill活动页显示tom已贡献金额
	When bill关注jobs的公众号
	When bill访问jobs的weapp
	When bill在微信中向jobs的公众号发送消息"拼红包活动2"
	Then bill收到自动回复"拼红包活动2单图文"
	When bill点击图文"拼红包活动2单图文"进入拼红包活动页面
	Then bill获得jobs的"拼红包活动2"的内容
		"""
		[{	
			"name":"拼红包活动2",
			"is_show_countdown":"false",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放现金奖励"
		}]
		"""
	When 更新贡献好友列表
	Then bill获得"拼红包活动2"的已贡献好友列表
		"""
		[]
		"""
	When bill把jobs的拼红包活动链接分享到朋友圈
	When tom关注jobs的公众号
	When tom访问jobs的weapp
	When tom取消关注jobs的公众号
	When tom点击bill分享的拼红包活动链接点赞
	#Then tom获得弹层提示信息'1.长按二维码关注"惠中大酒店"公众<br />号<br />2.关注公众号即可为好友点赞拼红包<br />3.回复："拼红包活动2",即可参加活动'
	When tom通过识别弹层中的带参数二维码关注jobs的公众号
	#关注成功后，点赞成功即bill获得一个随机金额的红包
	When bill访问jobs的weapp
	When bill在微信中向jobs的公众号发送消息"拼红包活动2"
	Then bill收到自动回复"拼红包活动2单图文"
	When bill点击图文"拼红包活动2单图文"进入拼红包活动页面
	Then bill获得jobs的"拼红包活动2"的内容
		"""
		[{	
			"name":"拼红包活动2",
			"is_show_countdown":"false",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放"
		}]
		"""
	When 更新贡献好友列表
	Then bill获得"拼红包活动2"的已贡献好友列表
		| name |
		| tom  |


@mall2 @apps_red_packet @apps_red_packet_frontend
Scenario:3 非会员通过会员分享的活动链接参加活动
	#非会员tom点击会员bill分享的活动链接参加活动，弹层显示公众号二维码
	#tom分享活动页到朋友圈
	#会员bill通过tom分享到的链接重复参加活动，弹层显示公众号二维码
	When bill关注jobs的公众号
	When bill访问jobs的weapp
	When bill在微信中向jobs的公众号发送消息"拼红包活动2"
	Then bill收到自动回复"拼红包活动2单图文"
	When bill点击图文"拼红包活动2单图文"进入拼红包活动页面
	When bill把jobs的拼红包活动链接分享到朋友圈
	#tom点击bill分享的链接
	When tom关注jobs的公众号
	When tom访问jobs的weapp
	When tom取消关注jobs的公众号
	When tom点击bill分享的拼红包活动链接参与活动
	#Then tom获得弹层提示信息'1.长按二维码关注"惠中大酒店"公众<br />号<br />2.回复："拼红包活动2",即可参加活动'
	When tom通过识别弹层中的公众号二维码关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息"拼红包活动2"
	Then tom收到自动回复"拼红包活动2单图文"
	When tom点击图文"拼红包活动2单图文"进入拼红包活动页面
	Then tom获得jobs的"拼红包活动2"的内容
		"""
		[{	
			"name":"拼红包活动2",
			"is_show_countdown":"false",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放现金奖励"
		}]
		"""
	When 更新贡献好友列表
	Then tom获得"拼红包活动2"的已贡献好友列表
		"""
		[]
		"""
	When tom把jobs的微助力活动链接分享到朋友圈
	When 清空浏览器
	When bill点击tom分享的拼红包活动链接参与活动
  	#Then bill获得弹层提示信息'1.长按二维码关注"惠中大酒店"公众<br />号<br />2.回复："拼红包活动2",即可参加活动'
	When bill通过识别弹层中的公众号二维码关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息"拼红包活动2"
	Then bill收到自动回复"拼红包活动2单图文"
	When bill点击图文"拼红包活动2单图文"进入拼红包活动页面
	Then bill获得jobs的"拼红包活动2"的内容
		"""
		[{	
			"name":"拼红包活动2",
			"is_show_countdown":"false",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放现金奖励"
		}]
		"""
	When 更新贡献好友列表
	Then bill获得"拼红包活动2"的已贡献好友列表
		"""
		[]
		"""

@mall2 @apps_red_packet @apps_red_packet_frontend
Scenario:4 会员帮好友点赞成功，取消关注公众号后再帮好友点赞，取消关注后已贡献好友列表汇总仍显示该会员，按钮状态“已帮XX好友点赞”，点击按钮弹层显示公众号二维码
	#会员tom点击会员bill分享的链接为bill点赞
	#tom取消关注jobs的公众号
	#tom关注jobs的公众号，再次点击bill分享的链接为bill点赞
	When bill关注jobs的公众号
	When bill访问jobs的weapp
	When bill在微信中向jobs的公众号发送消息"拼红包活动2"
	Then bill收到自动回复"拼红包活动2单图文"
	When bill点击图文"拼红包活动2图文"进入拼红包活动页面
	Then bill获得jobs的"拼红包活动2"的内容
		"""
		[{
			"name":"拼红包活动2",
			"is_show_countdown":"false",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放现金奖励"
		}]
		"""
	When 更新贡献好友列表
	Then bill获得"拼红包活动2"的已贡献好友列表
		"""
		[]
		"""
	When tom关注jobs的公众号
	When tom访问jobs的weapp
	When tom访问bill分享的拼红包活动链接点赞
	#点赞成功即bill获得一个随机金额的红包
	When 更新贡献好友列表
	When bill访问jobs的weapp
	When bill在微信中向jobs的公众号发送消息"拼红包活动2"
	Then bill收到自动回复"拼红包活动2单图文"
	When bill点击图文"拼红包活动2图文"进入拼红包活动页面
	Then bill获得jobs的"拼红包活动2"的内容
		"""
		[{
			"name":"拼红包活动2"，
			"is_show_countdown":"false",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放现金奖励"
		}]
		"""
	When 更新好友贡献列表
	Then bill获得"拼红包活动2"的已贡献好友列表
		| name |
		| tom  |
	
	When tom取消关注jobs的公众号
	#tom取消关注后，bill活动页面的已贡献好友列表中仍然显示tom
	When bill访问jobs的weapp
	When bill在微信中向jobs的公众号发送消息"拼红包活动2"
	Then bill收到自动回复"拼红包活动2单图文"
	When bill点击图文"拼红包活动2图文"进入拼红包活动页面
	Then bill获得jobs的"拼红包活动2"的内容
		"""
		[{
			"name":"拼红包活动2"，
			"is_show_countdown":"false",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放现金奖励"
		}]
		"""
	When 更新好友贡献列表
	Then bill获得"拼红包活动2"的已贡献好友列表
		| name |
		| tom  |
	#tom取消关注后，不能再帮bill点赞
	When tom点击bill分享的拼红包活动链接点赞
	#Then tom获得弹层提示信息'1.长按二维码关注"惠中大酒店"公众<br />号<br />2.回复："拼红包活动2",即可参加活动'
	When tom关注jobs的公众号
	#关注成功后，bill红包的金额不变
	When bill访问jobs的weapp
	When bill在微信中向jobs的公众号发送消息"拼红包活动2"
	Then bill收到自动回复"拼红包活动2单图文"
	When bill点击图文"拼红包活动2单图文"进入拼红包活动页面
	Then bill获得jobs的"拼红包活动2"的内容
		"""
		[{	
			"name":"拼红包活动2",
			"is_show_countdown":"false",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放"
		}]
		"""
	When 更新贡献好友列表
	Then bill获得"拼红包活动2"的已贡献好友列表
		| name |
		| tom  |