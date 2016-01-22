#_author_: 张雪  2016.01.20
#_editor_: 张三香 2016.01.20

Feature: 手机端前台塞红包
	"""
		说明：
		带参数的二维码：
		1、会员在自己专属页面点击按钮分享活动，邀请好友帮忙拼红包
		2、会员已帮好友点赞，弹出引导页面
		3、会员帮助会员好友点赞，拼红包成功（弹出提示贡献成功）
		4、非会员通过会员好友分享的活动页帮好友点赞（弹出二维码弹层）
		5、会员通过会员分享的活动页进行我也要拼红包（弹出公众号的二维码）
		6、非会员通过会员好友分享的活动页进行我也要拼红包（弹出公众号的二维码）
		7、会员通过会员好友分享的活动页面已经参加，再次点击我也要参加（弹出引导页）
		8、不设置带参数二维码的情况下，为好友点赞，弹出公众号二维码
		9、会员通过好友分享的页面再次进行我也要拼红包（弹出公众号二维码）
		10、取关会员，其好友在活动期间为其点赞，弹出错误提示（该用户已经取消关注 暂不能点赞）
		
		备注：
		1、取消关注的会员，在列表里不会消失，只要为好友拼过红包就一直存在
		2、列表里的会员按照时间的倒序来排序

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
			"scan_code_reply": "感谢您的的参与，为好友点赞成功！"
		}]
		"""
	When jobs新建塞红包活动
		"""
		[{
			"name":"拼红包活动1",
			"start_date":"今天",
			"end_date":"明天",
			"is_show_countdown":"ture",
			"red_packet":[{
				"type":"拼手气红包",
				"total_amount":"10",
				"packet_num":"2"	
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
			"end_date":"2天后",
			"is_show_countdown":"false",
			"red_packet":[{
				"type":"普通红包",
				"packet_num":"3",
				"single_packet_amount":"5"
			}]
			"contribution_start_range":"0.5",
			"contribution_end_range":"1.5",
			"reply":"普通红包",
			"qr_code":"带参数二维码1",
			"license":"apiclient_cert.pem",
			"license_key":"apiclient_key.pem",
			"rules":"获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
			"share_pic":"2.jpg",
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
			"jump_url":"塞红包-拼红包活动1"
		},{
			"title":"拼红包活动2单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文2文本摘要",
			"content":"单条图文2文本内容",
			"jump_url":"塞红包-拼红包活动2"
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
					"reply_content":"拼包活动2单图文",
					"reply_type":"text_picture"
				}]
		}]
		"""


	

@apps_redpockets_frontend
Scenario:1 会员进入自己专属页面系统自动发放一个固定金额的红包（普通红包）
#主要验证普通红包获得系统自动发放的红包金额
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'拼红包活动2'
	Then bill收到自动回复'拼红包活动2单图文'
	When bill点击图文"拼红包活动2单图文"进入塞红包活动页面
	Then bill获得jobs的'拼红包活动2'的内容
		"""
		[{
			"name": "拼红包活动2",
			"is_show_countdown": "true",
			"single_packet_amount":"5",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放"
		}]
		"""
	
 
@apps_redpockets_frontend
Scenario:2 会员帮助会员好友点赞，拼红包成功（弹出提示贡献成功）
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'拼红包活动1'
	Then bill收到自动回复'拼红包活动1单图文'
	When bill点击图文"拼红包活动1单图文"进入塞红包活动页面
	Then bill获得jobs的'拼红包活动1'的内容
		"""
		[{
			"name": "拼红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	When bill把jobs的塞红包活动链接分享到朋友圈
	When 更新塞红包活动
	When bill点击图文"拼红包活动1单图文"进入微助力活动页面
	Then bill获得jobs的'拼红包活动1'的内容
		"""
		[{
			"name": "拼红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom点击bill分享的塞红包活动链接进行拼红包
	Then tom获得jobs的'拼红包活动1'的内容
		"""
		[{
			"name": "拼红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	When tom为好友点赞
	Then tom点击bill分享的塞红包活动链接进行塞红包
	When 更新塞红包活动
	Then tom获得jobs的'拼红包活动1'的内容
	"""
		[{
			"name": "拼红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	
@apps_redpockets_frontend
Scenario:3 会员在好友页面点击“已帮好友点赞”按钮，弹出引导页面
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'拼红包活动1'
	Then bill收到自动回复'拼红包活动1单图文'
	When bill点击图文"拼红包活动1单图文"进入塞红包活动页面
	Then bill获得jobs的'拼红包活动1'的内容
		"""
		[{
			"name": "拼红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	When bill把jobs的塞红包活动链接分享到朋友圈
	When 更新塞红包活动
	When bill点击图文"拼红包活动1单图文"进入微助力活动页面
	Then bill获得jobs的'拼红包活动1'的内容
		"""
		[{
			"name": "拼红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom点击bill分享的塞红包活动链接进行拼红包
	Then tom获得jobs的'拼红包活动1'的内容
		"""
		[{
			"name": "拼红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	When tom为好友点赞
	When 更新塞红包活动
	Then tom获得jobs的'拼红包活动1'的内容
	"""
		[{
			"name": "拼红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	
	When tom再次为好友点赞
	#Then tom获得蒙版提示：点击右上角，选择发送给指定好友或者朋友圈，来帮“XX”点赞


@apps_redpockets_frontend
Scenario:4 会员通过好友分享的页面进行我也要拼红包，弹出公众号二维码
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'拼红包活动1'
	Then bill收到自动回复'拼红包活动1单图文'
	When bill点击图文"拼红包活动1单图文"进入塞红包活动页面
	Then bill获得jobs的'拼红包活动1'的内容
		"""
		[{
			"name": "拼红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	When bill把jobs的塞红包活动链接分享到朋友圈
	When 更新塞红包活动
	When bill点击图文"拼红包活动1单图文"进入微助力活动页面
	Then bill获得jobs的'拼红包活动1'的内容
		"""
		[{
			"name": "塞红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom点击bill分享的塞红包活动链接进行我也要拼红包
	Then tom通过识别弹层中的带参数二维码关注jobs的公众号
	When 更新塞红包活动
	When tom在微信中向jobs的公众号发送消息'拼红包活动1'
	Then tom收到自动回复'拼红包活动1单图文'
	When tom点击图文"拼红包活动1单图文"进入塞红包活动页面
	Then tom获得jobs的'拼红包活动1'的内容
	"""
		[{
			"name": "拼红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	When tom点击bill分享的塞红包活动链接再次进行我也要拼红包
	Then tom通过识别弹层中的带参数二维码关注jobs的公众号
	#tom再次通过好友分享的链接进行我也要拼红包，再次弹出公众号的二维码，通过识别二维码进入公众号

	
@apps_redpockets_frontend
Scenario:5 好友在活动期间不能为取关会员点赞
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'拼红包活动1'
	Then bill收到自动回复'拼红包活动1单图文'
	When bill点击图文"拼红包活动1单图文"进入塞红包活动页面
	Then bill获得jobs的'拼红包活动1'的内容
		"""
		[{
			"name": "拼红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	When bill把jobs的塞红包活动链接分享到朋友圈
	When 更新塞红包活动
	When bill点击图文"拼红包活动1单图文"进入微助力活动页面
	Then bill获得jobs的'拼红包活动1'的内容
		"""
		[{
			"name": "塞红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom点击bill分享的塞红包活动链接进行我也要拼红包
	Then tom通过识别弹层中的带参数二维码关注jobs的公众号
	When 更新塞红包活动
	When tom在微信中向jobs的公众号发送消息'拼红包活动1'
	Then tom收到自动回复'拼红包活动1单图文'
	When tom点击图文"拼红包活动1单图文"进入塞红包活动页面
	Then tom获得jobs的'拼红包活动1'的内容
	"""
		[{
			"name": "拼红包活动1",
			"is_show_countdown": "true",
			"rules": "获奖条件必须要在活动时间内攒够红包金额<br />点赞达到红包金额，系统会自动发放",
		}]
		"""
	When tom点击bill分享的塞红包活动链接再次进行我也要拼红包
	Then tom通过识别弹层中的带参数二维码关注jobs的公众号
