#_author_: 张雪 许韦 2015.11.17
#_editor_: 张三香 2015.11.24

Feature: 会员参加微助力助力
	"""
		说明：
		带参数的二维码：
		1、会员帮助会员好友助力
		2、会员重复帮好友助力
		3、会员通过会员分享的活动页进行我要参与
		4、会员通过会员分享的活动页重复进行我要参与
		5、会员在自己专属页面点击按钮分享活动
		6、会员在自己的专属页面重复点击按钮分享活动
		7、非会员通过会员好友分享的活动页帮好友助力
		8、非会员通过会员好友分享的活动页帮我要参与
		9、取消关注的会员，排名取消，为会员好友的助力值不变，参与人数减少
		10、取消关注的会员通过会员好友分享页再次帮助好友助力
		11、取消关注的会员通过会员好友分享页再次进行我要参与
		12、取消关注的会员通过之前会员好友分享的链接为非会员好友助力
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
			"tags": "未分组",
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
			"start_date":"今天",
			"end_date":"3天后",
			"is_show_countdown":"true",
			"desc":"微助力活动描述",
			"reply":"微助力1",
			"qr_code":"",
			"share_pic":"1.jpg",
			"background_pic":"2.jpg",
			"background_color":"冬日暖阳",
			"rules":"获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式"
		},{
			"name":"微助力活动2",
			"start_date":"今天",
			"end_date":"1天后",
			"is_show_countdown":"false",
			"desc":"微助力活动描述",
			"reply":"微助力2",
			"qr_code":"带参数二维码1",
			"share_pic":"3.jpg",
			"background_pic":"4.jpg",
			"background_color":"热带橙色",
			"rules":"按上按上打算四大的撒的撒<br />撒打算的撒的撒大声地<br />按上打算打算<br />阿萨德按上打"
		}]
		"""
	When jobs已添加单图文
		"""
		[{
			"title":"微助力1单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容",
			"jump_url":"微助力-微助力活动1"
		},{
			"title":"微助力2单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文2文本摘要",
			"content":"单条图文2文本内容",
			"jump_url":"微助力-微助力活动2"
		}]
		"""
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": [{
					"keyword": "微助力1",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"微助力1单图文",
					"reply_type":"text_picture"
				}]
		},{
			"rules_name":"规则2",
			"keyword": [{
					"keyword": "微助力2",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"微助力2单图文",
					"reply_type":"text_picture"
				}]
		}]
		"""

@apps @powerme @frontend @kuki
Scenario:1 用户重复参与微助力活动
	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	Then bill获得jobs的'微助力活动1'的内容
		"""
		[{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式",
			"my_rank": "无",
			"my_power_score": "0",
			"total_participant_count": "0"
		}]
		"""
	Then bill获得"微助力活动1"的助力值排名
		"""
		[]
		"""
	When bill把jobs的微助力活动链接分享到朋友圈
	When bill点击图文"微助力1单图文"进入微助力活动页面
	Then bill获得jobs的'微助力活动1'的内容
		"""
		[{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式",
			"my_rank": "1",
			"my_power_score": "0",
			"total_participant_count": "1"
		}]
		"""
	Then bill获得"微助力活动1"的助力值排名
		| rank | name | value |
		|  1   | bill |   0   |

	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微助力1'
	Then tom收到自动回复'微助力1单图文'
	When tom点击图文"微助力1单图文"进入微助力活动页面
	When tom把jobs的微助力活动链接分享到朋友圈
	When bill点击tom分享的微助力活动链接进行参与
	Then bill获得弹层提示信息'您已参加该活动!<br />长按二维码进入公众号<br />获取你自己的专属页,<br />分享到朋友圈,发动小伙伴帮你助力<br />赢大奖!'

@apps @powerme @frontend @kuki
Scenario:2 会员帮助会员好友助力
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	Then bill获得jobs的'微助力活动1'的内容
		"""
		[{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式",
			"my_rank": "无",
			"my_power_score": "0",
			"total_participant_count": "0"
		}]
		"""
	Then bill获得"微助力活动1"的助力值排名
		"""
		[]
		"""
	When bill把jobs的微助力活动链接分享到朋友圈
	When bill点击图文"微助力1单图文"进入微助力活动页面
	Then bill获得"微助力活动1"的助力值排名
		| rank | name | value |
		|  1   | bill |   0   |
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom点击bill分享的微助力活动链接进行助力
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	Then bill获得jobs的'微助力活动1'的内容
		"""
		[{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式",
			"my_rank": "1",
			"my_power_score": "1",
			"total_participant_count": "1"
		}]
		"""
	Then bill获得"微助力活动1"的助力值排名
		| rank | name | value |
		|  1   | bill |   1   |

@apps @powerme @frontend @kuki
Scenario:3 非会员帮助会员好友助力
	#bill参加'微助力活动1',无识别二维码
	#tom取消关注后帮bill助力,弹层中显示公众号的二维码

	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	Then bill获得jobs的'微助力活动1'的内容
		"""
		[{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式",
			"my_rank": "无",
			"my_power_score": "0",
			"total_participant_count": "0"
		}]
		"""
	Then bill获得"微助力活动1"的助力值排名
		"""
		[]
		"""
	When bill把jobs的微助力活动链接分享到朋友圈
	When bill点击图文"微助力1单图文"进入微助力活动页面
	Then bill获得"微助力活动1"的助力值排名
		| rank | name | value |
		|  1   | bill |   0   |
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom取消关注jobs的公众号
	When tom点击bill分享的微助力活动链接进行助力
	Then tom获得弹层提示信息'1.长按二维码关注"惠中大酒店"公众<br />号<br />2.关注公众号即可为好友助力值+1<br />3.回复："微助力1",即可参加活动'
	When tom通过识别弹层中的公众号二维码关注jobs的公众号
	#关注成功后，助力成功即bill助力值加1
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	Then bill获得jobs的'微助力活动1'的内容
	"""
		[{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式",
			"my_rank": "1",
			"my_power_score": "1",
			"total_participant_count": "1"
		}]
	"""
	Then bill获得"微助力活动1"的助力值排名
		| rank | name | value |
		|  1   | bill |   1   |

@apps @powerme @frontend @kuki
Scenario:4 连续帮助会员好友助力
	#bill参加'微助力活动2',有识别二维码
	#tom取消关注后（已非会员身份）帮bill助力,点击'帮bill助力'按钮,弹层中显示带参数二维码
	#tom再次帮bill助力,点击'已帮bill助力'按钮,获得提示信息

	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力2'
	Then bill收到自动回复'微助力2单图文'
	When bill点击图文"微助力2单图文"进入微助力活动页面
	Then bill获得jobs的'微助力活动2'的内容
		"""
		[{
			"name": "微助力活动2",
			"is_show_countdown": "false",
			"desc": "微助力活动描述",
			"background_pic": "4.jpg",
			"background_color": "热带橙色",
			"rules": "按上按上打算四大的撒的撒<br />撒打算的撒的撒大声地<br />按上打算打算<br />阿萨德按上打",
			"my_rank": "无",
			"my_power_score": "0",
			"total_participant_count": "0"
		}]
		"""
	Then bill获得"微助力活动2"的助力值排名
		"""
		[]
		"""
	When bill把jobs的微助力活动链接分享到朋友圈
	When bill点击图文"微助力2单图文"进入微助力活动页面
	Then bill获得"微助力活动2"的助力值排名
		| rank | name | value |
		|  1   | bill |   0   |
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom取消关注jobs的公众号
	When tom点击bill分享的微助力活动链接进行助力
	Then tom获得弹层提示信息'1.长按二维码关注"惠中大酒店"公众<br />号<br />2.关注公众号即可为好友助力值+1<br />3.回复："微助力2",即可参加活动'
	When tom通过识别弹层中的带参数二维码关注jobs的公众号
	#tom关注成功后，助力成功即bill助力值加1
	When tom点击bill分享的微助力活动链接
	Then tom获得jobs的'微助力活动2'的内容
		"""
		[{
			"name": "微助力活动2",
			"is_show_countdown": "false",
			"desc": "微助力活动描述",
			"background_pic": "4.jpg",
			"background_color": "热带橙色",
			"rules": "按上按上打算四大的撒的撒<br />撒打算的撒的撒大声地<br />按上打算打算<br />阿萨德按上打",
			"my_rank": "无",
			"my_power_score": "0",
			"total_participant_count": "1"
		}]
		"""
	Then tom获得"微助力活动2"的助力值排名
		| rank | name | value |
		|  1   | bill |   1   |
	#tom重复帮助好友bill助力
	When tom点击bill分享的微助力活动链接进行助力
	Then tom获得弹层提示信息'好的事物,一起分享<br />邀请好友或者分享到朋友圈,<br />发动小伙伴帮bill赢大奖!'

@apps @powerme @frontend @kuki
Scenario:5 会员帮好友助力成功后，取消关注公众号再帮好友助力
	#会员bill分享微助力活动链接
	#会员tom帮bill助力
	#会员tom取消关注公众号
	#会员tom点击bill分享的链接再帮bill助力

	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	Then bill获得jobs的'微助力活动1'的内容
		"""
		[{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式",
			"my_rank": "无",
			"my_power_score": "0",
			"total_participant_count": "0"
		}]
		"""
	Then bill获得"微助力活动1"的助力值排名
		"""
		[]
		"""
	When bill把jobs的微助力活动链接分享到朋友圈

	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom点击bill分享的微助力活动链接进行助力
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	Then bill获得jobs的'微助力活动1'的内容
		"""
		[{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式",
			"my_rank": "1",
			"my_power_score": "1",
			"total_participant_count": "1"
		}]
		"""
	Then bill获得"微助力活动1"的助力值排名
		| rank | name | value |
		|  1   | bill |   1   |

	When tom取消关注jobs的公众号
	#取消关注后，帮bill的助力值不变
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	Then bill获得jobs的'微助力活动1'的内容
		"""
		[{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式",
			"my_rank": "1",
			"my_power_score": "1",
			"total_participant_count": "1"
		}]
		"""
	Then bill获得"微助力活动1"的助力值排名
		| rank | name | value |
		|  1   | bill |   1   |

	#取消关注后，不能再帮bill助力
	When tom点击bill分享的微助力活动链接进行助力
	Then tom获得弹层提示信息'好的事物,一起分享<br />邀请好友或者分享到朋友圈,<br />发动小伙伴帮bill赢大奖!'

@apps @powerme @frontend @kuki
Scenario:6 会员通过好友分享链接参加微助力活动（无识别二维码）
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	When bill把jobs的微助力活动链接分享到朋友圈

	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom点击bill分享的微助力活动链接进行参与
	Then tom获得弹层提示信息'1.长按二维码关注"惠中大酒店"公众<br />号<br />2.回复："微助力1",即可参加活动'
	When tom通过识别弹层中的公众号二维码关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微助力1'
	Then tom收到自动回复'微助力1单图文'
	When tom点击图文"微助力1单图文"进入微助力活动页面
	Then tom获得jobs的'微助力活动1'的内容
		"""
		[{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式",
			"my_rank": "无",
			"my_power_score": "0",
			"total_participant_count": "1"
		}]
		"""
	Then tom获得"微助力活动1"的助力值排名
		| rank | name | value |
		|  1   | bill |   0   |
	When tom把jobs的微助力活动链接分享到朋友圈
	When tom点击图文"微助力1单图文"进入微助力活动页面
	Then tom获得jobs的'微助力活动1'的内容
		"""
		[{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式",
			"my_rank": "2",
			"my_power_score": "0",
			"total_participant_count": "2"
		}]
		"""
	Then tom获得"微助力活动1"的助力值排名
		| rank | name | value |
		|  1   | bill |   0   |
		|  2   | tom  |   0   |

@apps @powerme @frontend @kuki
Scenario:7 非员通过好友分享链接参加微助力活动（有识别二维码）
	#bill分享微助力链接
	#tom关注后点击bill分享的链接帮bill助力
	#tom再点击bill分享的链接，点击'我要参与',并分享链接
	#tom取消关注,tom的微助力排名消失

	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力2'
	Then bill收到自动回复'微助力2单图文'
	When bill点击图文"微助力2单图文"进入微助力活动页面
	When bill把jobs的微助力活动链接分享到朋友圈

	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom点击bill分享的微助力活动链接进行助力

	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力2'
	Then bill收到自动回复'微助力2单图文'
	When bill点击图文"微助力2单图文"进入微助力活动页面
	Then bill获得jobs的'微助力活动2'的内容
		"""
		[{
			"name": "微助力活动2",
			"is_show_countdown": "false",
			"desc": "微助力活动描述",
			"background_pic": "4.jpg",
			"background_color": "热带橙色",
			"rules":"按上按上打算四大的撒的撒<br />撒打算的撒的撒大声地<br />按上打算打算<br />阿萨德按上打",
			"my_rank": "1",
			"my_power_score": "1",
			"total_participant_count": "1"
		}]
		"""
	Then bill获得"微助力活动2"的助力值排名
		| rank | name | value |
		|  1   | bill |   1   |

	When tom取消关注jobs的公众号
	#取消关注后tom通过bill的分享链接进行参与（页面按钮:'已帮bill助力','我要参与'）
	When tom点击bill分享的微助力活动链接进行参与
	Then tom获得弹层提示信息'1.长按二维码关注"惠中大酒店"公众<br />号<br />2.回复："微助力2",即可参加活动'
	When tom通过识别弹层中的带参数二维码关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微助力2'
	Then tom收到自动回复'微助力2单图文'
	When tom点击图文"微助力2单图文"进入微助力活动页面
	Then tom获得jobs的'微助力活动2'的内容
		"""
		[{
			"name": "微助力活动2",
			"is_show_countdown": "false",
			"desc": "微助力活动描述",
			"background_pic": "4.jpg",
			"background_color": "热带橙色",
			"rules":"按上按上打算四大的撒的撒<br />撒打算的撒的撒大声地<br />按上打算打算<br />阿萨德按上打",
			"my_rank": "无",
			"my_power_score": "0",
			"total_participant_count": "1"
		}]
		"""
	Then tom获得"微助力活动2"的助力值排名
		| rank | name | value |
		|  1   | bill |   1   |
	When tom把jobs的微助力活动链接分享到朋友圈
	When tom点击图文"微助力2单图文"进入微助力活动页面
	Then tom获得jobs的'微助力活动2'的内容
		"""
		[{
			"name": "微助力活动2",
			"is_show_countdown": "false",
			"desc": "微助力活动描述",
			"background_pic": "4.jpg",
			"background_color": "热带橙色",
			"rules":"按上按上打算四大的撒的撒<br />撒打算的撒的撒大声地<br />按上打算打算<br />阿萨德按上打",
			"my_rank": "2",
			"my_power_score": "0",
			"total_participant_count": "2"
		}]
		"""
	Then tom获得"微助力活动2"的助力值排名
		| rank | name | value |
		|  1   | bill |   1   |
		|  2   | tom  |   0   |

	#取消关注后,tom的排名消失，tom帮好友的助力值不消失
	When tom取消关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力2'
	Then bill收到自动回复'微助力2单图文'
	When bill点击图文"微助力2单图文"进入微助力活动页面
	Then bill获得jobs的'微助力活动2'的内容
		"""
		[{
			"name": "微助力活动2",
			"is_show_countdown": "false",
			"desc": "微助力活动描述",
			"background_pic": "4.jpg",
			"background_color": "热带橙色",
			"rules":"按上按上打算四大的撒的撒<br />撒打算的撒的撒大声地<br />按上打算打算<br />阿萨德按上打",
			"my_rank": "1",
			"my_power_score": "1",
			"total_participant_count": "1"
		}]
		"""
	Then bill获得"微助力活动2"的助力值排名
		| rank | name | value |
		|  1   | bill |   1   |

@apps @powerme @frontend @kuki8
Scenario:8 会员B分享会员A的微助力活动链接
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	When bill把jobs的微助力活动链接分享到朋友圈
	#tom点击bill分享的链接助力后并分享bill的活动页到朋友圈
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom点击bill分享的微助力活动链接进行助力
	When tom把jobs的微助力活动链接分享到朋友圈
	#tom2点击tom分享的bill的活动页，帮bill进行助力
	When tom2关注jobs的公众号
	When tom2访问jobs的webapp
	When tom2点击tom分享的微助力活动链接进行助力
	Then tom2获得jobs的'微助力活动1'的内容
		"""
		[{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式",
			"my_rank": "无",
			"my_power_score": "0",
			"total_participant_count": "1"
		}]
		"""
	Then tom2获得"微助力活动1"的助力值排名
		| rank | name | value |
		|  1   | bill |   2   |

@apps @powerme @frontend
Scenario:9 用户参加'未开始'和'已结束'的微助力活动
	When jobs新建微助力活动
		"""
		[{
			"name":"未开始微助力活动",
			"start_date":"明天",
			"end_date":"3天后",
			"is_show_countdown":"true",
			"desc":"微助力活动描述",
			"reply":"未开始微助力",
			"qr_code":"",
			"share_pic":"1.jpg",
			"background_pic":"2.jpg",
			"background_color":"冬日暖阳",
			"rules":"获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式"
		},{
			"name":"已结束微助力活动",
			"start_date":"3天前",
			"end_date":"昨天",
			"is_show_countdown":"false",
			"desc":"微助力活动描述",
			"reply":"已结束微助力",
			"qr_code":"",
			"share_pic":"3.jpg",
			"background_pic":"4.jpg",
			"background_color":"热带橙色",
			"rules":"按上按上打算四大的撒的撒<br />撒打算的撒的撒大声地<br />按上打算打算<br />阿萨德按上打"
		}]
		"""
	When jobs已添加单图文
		"""
		[{
			"title":"微助力1单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容",
			"jump_url":"微助力-未开始微助力"
		},{
			"title":"微助力2单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文2文本摘要",
			"content":"单条图文2文本内容",
			"jump_url":"微助力-已结束微助力"
		}]
		"""
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": [{
					"keyword": "未开始微助力",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"微助力1单图文",
					"reply_type":"text_picture"
				}]
		},{
			"rules_name":"规则2",
			"keyword": [{
					"keyword": "已结束微助力",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"微助力2单图文",
					"reply_type":"text_picture"
				}]
		}]
		"""

	#bill参加未开始微助力活动
		When bill关注jobs的公众号
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'未开始微助力'
		Then bill收到自动回复'微助力1单图文'
		When bill点击图文"微助力1单图文"进入微助力活动页面
		Then bill获得jobs的'未开始微助力活动'的内容
			"""
			[{
				"name": "未开始微助力活动",
				"is_show_countdown": "true",
				"desc": "微助力活动描述",
				"background_pic": "2.jpg",
				"background_color": "冬日暖阳",
				"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式",
				"my_rank": "无",
				"my_power_score": "0",
				"total_participant_count": "0"
			}]
			"""
		Then bill获得"未开始微助力活动"的助力值排名
			"""
			[]
			"""
		And bill获得提示信息'活动尚未开始,敬请期待'
	#tom参加已结束微助力活动
		When tom关注jobs的公众号
		When tom访问jobs的webapp
		When tom在微信中向jobs的公众号发送消息'已结束微助力'
		Then tom收到自动回复'微助力2单图文'
		When tom点击图文"微助力2单图文"进入微助力活动页面
		Then tom获得jobs的'已结束微助力活动'的内容
			"""
			[{
				"name": "已结束微助力活动",
				"is_show_countdown": "false",
				"desc": "微助力活动描述",
				"background_pic":"4.jpg",
				"background_color":"热带橙色",
				"rules":"按上按上打算四大的撒的撒<br />撒打算的撒的撒大声地<br />按上打算打算<br />阿萨德按上打",
				"my_rank": "无",
				"my_power_score": "0",
				"total_participant_count": "0"
			}]
			"""
		Then tom获得"已结束微助力活动"的助力值排名
			"""
			[]
			"""
		And tom获得提示信息'活动已结束'