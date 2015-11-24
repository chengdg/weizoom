#_author_:张雪 许韦 2015.11.17

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
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动1",
			"start_date":"今天",
			"end_date":"3天后",
			"status":"进行中",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","关闭"]
		},{
			"name":"微助力活动2",
			"start_date":"今天",
			"end_date":"1天后",
			"status":"进行中",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","关闭"]

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

@apps @powerme @frontend @kuki1
Scenario:1 会员帮助会员好友助力
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	Then bill获得jobs的'微助力活动1'的内容
	"""
		{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式"
			"my_rank": "无",
			"my_power_score": "0",
			"total_participant_count": "0"
		}
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
		{
			"name": "微助力活动1",
			"is_show_countdown": "true",
			"desc": "微助力活动描述",
			"background_pic": "2.jpg",
			"background_color": "冬日暖阳",
			"rules": "获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式"
			"my_rank": "1",
			"my_power_score": "1",
			"total_participant_count": "1"
		}
	"""
  	Then tom获得"微助力活动1"的助力值排名
		| rank | name | value |
		|  1   | bill |   1   |

@apps @powerme @frontend
Scenario:2 会员重复帮好友助力
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0助力值
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复"图文1"链接
	When bill进入"微助力活动1"活动页面
	Then bill获得jobs的'微助力活动1'
		"""
			{
				"link_name":"微助力活动1",
				"is_show_countdown":"true",
				"buttons":[帮好友助力],["立即分享召唤小伙伴"],
				"rules":"微助力活动1",
				"my_rank":"0",
				"my_power_score":"0",
				"participant":"0"
			}
		"""
	And bill获得"微助力活动1"的"助力值TOP100"
		| rank |name |value |
		| 0    |bill |  0   |

	#tom点击bill分享的链接,查看默认活动页

	When tom关注jobs的公众号
	When tom通过bill分享的"微助力活动1"链接进入活动页面
	Then tom获得jobs的webapp页面'微助力活动1'
			"""
				{
					"link_name":"微助力活动1",
					"is_show_countdown":"true",
					"buttons":["帮bill助力","我也要参加"],["立即分享召唤小伙伴"],
					"rules":"微助力活动1",
					"my_rank":"无",
					"my_power_score":"0",
					"participant":"1"
				}
			"""
	#tom点击帮bill助力按钮,助力成功后再次访问bill的活动页面
	When tom完成'帮bill助力'操作
	Then tom获得弹出公众号带参数二维码"带参数二维码1"
	When tom关注jobs的公众号
	Then tom获得公众号返回的参数:"感谢您的的参与，为好友助力成功！"
	When 清空浏览器
	When tom访问jobs的webapp的"微助力活动1"活动页
	Then tom获得jobs的webapp页面'微助力活动1'
			"""
				{
					"link_name":"微助力活动1",
					"is_show_countdown":"true",
					"buttons":["已帮bill助力"],["我也要参加"],
					"rules":"微助力活动1",
					"my_rank":"无",
					"my_power_score":"0",
					"participant":"1"
				}
			"""
		And tom获得"微助力活动1"的"助力值TOP100"
			| rank |name |value |
			|  0   |bill |  1   |


	When tom再次完成'帮bill助力'操作
	When 清空浏览器
	Then ttom获得jobs的webapp页面'微助力活动1'
		| rank |name |value |
		|  0   |bill |  1   |

  @apps @powerme @frontend
Scenario:3 会员通过会员分享的活动页进行我要参与
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0助力值
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复"图文1"链接
	When bill进入"微助力活动1"活动页面
	Then bill获得jobs的'微助力活动1'
		"""
			{
				"link_name":"微助力活动1",
				"is_show_countdown":"true",
				"buttons":[帮好友助力],["我也要参加"],
				"rules":"微助力活动1",
				"my_rank":"0",
				"my_power_score":"0",
				"participant":"0"
			}
		"""
	And bill获得"微助力活动1"的"助力值TOP100"
		| rank |name |value |
		| 0    |bill |  0   |

	#tom点击bill分享的链接,查看默认活动页

	When tom关注jobs的公众号
	When tom通过bill分享的"微助力活动1"链接进入活动页面
	Then tom获得jobs的webapp页面'微助力活动1'
			"""
				{
					"link_name":"微助力活动1",
					"is_show_countdown":"true",
					"buttons":["帮bill助力"],["我也要参加"],
					"rules":"微助力活动1",
					"my_rank":"无",
					"my_power_score":"0",
					"participant":"1"
				}
			"""
	#tom点击帮bill助力按钮,助力成功后再次访问bill的活动页面
	When tom完成'我也要参加'操作
	Then tom获得弹出公众号二维码
	When tom关注jobs的公众号
	Then tom进入jobs的公众号
	When 清空浏览器
	When tom访问jobs的webapp的"微助力活动1"活动页
	Then tom获得jobs的webapp页面'微助力活动1'
			"""
				{
					"link_name":"微助力活动1",
					"is_show_countdown":"true",
					"buttons":["立即分享召唤小伙伴"],
					"rules":"微助力活动1",
					"my_rank":"无",
					"my_power_score":"0",
					"participant":"1"
				}
			"""
		And tom获得"微助力活动1"的"助力值TOP100"
			| rank |name |value |
			|  0   |bill |  1   |




@apps @powerme @frontend
Scenario:4 会员通过会员分享的活动页重复进行我要参与
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0助力值
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复"图文1"链接
	When bill进入"微助力活动1"活动页面
	Then bill获得jobs的'微助力活动1'
		"""
			{
				"link_name":"微助力活动1",
				"is_show_countdown":"true",
				"buttons":[帮好友助力],["我也要参加"],
				"rules":"微助力活动1",
				"my_rank":"0",
				"my_power_score":"0",
				"participant":"0"
			}
		"""
	And bill获得"微助力活动1"的"助力值TOP100"
		| rank |name |value |
		| 0    |bill |  0   |

	#tom点击bill分享的链接,查看默认活动页

	When tom关注jobs的公众号
	When tom通过bill分享的"微助力活动1"链接进入活动页面
	Then tom获得jobs的webapp页面'微助力活动1'
			"""
				{
					"link_name":"微助力活动1",
					"is_show_countdown":"true",
					"buttons":["帮bill助力"],["我也要参加"],
					"rules":"微助力活动1",
					"my_rank":"无",
					"my_power_score":"0",
					"participant":"1"
				}
			"""
	#tom点击帮bill助力按钮,助力成功后再次访问bill的活动页面
	When tom完成'我也要参加'操作
	Then tom获得弹出公众号二维码
	When tom关注jobs的公众号
	Then tom进入jobs的公众号
	When 清空浏览器
	When tom访问jobs的webapp的"微助力活动1"活动页
	Then tom获得jobs的webapp页面'微助力活动1'
			"""
				{
					"link_name":"微助力活动1",
					"is_show_countdown":"true",
					"buttons":["立即分享召唤小伙伴"],
					"rules":"微助力活动1",
					"my_rank":"无",
					"my_power_score":"0",
					"participant":"1"
				}
			"""
	And tom获得"微助力活动1"的"助力值TOP100"
			| rank |name |value |
			|  0   |bill |  1   |
	When tom再次完成'我也要参加'操作
	When tom再次完成'帮bill助力'操作
	When 清空浏览器
	Then tom获得jobs的webapp页面'微助力活动1'
		| rank |name |value |
		|  0   |bill |  1   |

@apps @powerme @frontend
Scenario:5  会员在自己专属页面点击按钮分享活动
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0助力值
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复"图文1"链接
	When bill进入"微助力活动1"活动页面
	Then bill获得jobs的'微助力活动1'
		"""
			{
				"link_name":"微助力活动1",
				"is_show_countdown":"true",
				"buttons":["立即分享召唤小伙伴"],
				"rules":"微助力活动1",
				"my_rank":"0",
				"my_power_score":"0",
				"participant":"0"
			}
		"""
	When bill把jobs的微助力活动"微助力活动1"链接分享到朋友圈
	When 清空浏览器
	Then bill获得jobs的webapp页面'微助力活动1'
	And bill获得"微助力活动1"的"助力值TOP100"
		| rank |name |value |
		| 0    |bill |  1   |
	

	

@apps @powerme @frontend
Scenario:6 会员在自己的专属页面重复点击按钮分享活动
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0助力值
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复"图文1"链接
	When bill进入"微助力活动1"活动页面
	Then bill获得jobs的'微助力活动1'
		"""
			{
				"link_name":"微助力活动1",
				"is_show_countdown":"true",
				"buttons":["立即分享召唤小伙伴"],
				"rules":"微助力活动1",
				"my_rank":"0",
				"my_power_score":"0",
				"participant":"0"
			}
		"""
	When bill把jobs的微助力活动"微助力活动1"链接分享到朋友圈
	When 清空浏览器
	Then bill获得jobs的webapp页面'微助力活动1'
	And bill获得"微助力活动1"的"助力值TOP100"
		| rank |name |value |
		| 0    |bill |  1   |
	When 清空浏览器
	Then bill再次获得jobs的webapp页面'微助力活动1'
	When bill再次把jobs的微助力活动"微助力活动1"链接分享到朋友圈
	And bill获得"微助力活动1"的"助力值TOP100"
		| rank |name |value |
		| 0    |bill |  1   |


@apps @powerme @frontend
Scenario:7 创建不带参数二维码的微助力活动，非会员通过会员好友分享的活动页帮好友助力
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复"图文1"
	When bill点击"图文1"链接
	When bill参与"微助力活动1"活动
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"0",
			"participant":"1"
		}
		"""
	When tom通过bill分享的"微助力活动1"链接帮助好友助力
	Then tom可以查看jobs公众号二维码图片
	When tom关注jobs的公众号
	When bill清空浏览器
	When bill点击"图文1"链接
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"1",
			"participant":"1"
		}
		"""

@apps @powerme @frontend
Scenario:8 创建带参数二维码的微助力活动，非会员通过会员好友分享的活动页帮好友助力
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力2'
	Then bill收到自动回复"图文2"
	When bill点击"图文2"链接
	When bill参与"微助力活动2"活动
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"0",
			"participant":"1"
		}
		"""
	When tom通过bill分享的"微助力活动2"链接帮助好友助力
	Then tom可以查看"带参数二维码1"图片
	When tom关注jobs的公众号
	Then tom收到自动回复"感谢您的的参与，为好友助力成功！"
	When bill清空浏览器
	When bill点击"图文2"链接
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"1",
			"participant":"1"
		}
		"""

@apps @powerme @frontend
Scenario:9 非会员通过会员好友分享的活动页参与助力
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复"图文1"
	When bill点击"图文1"链接
	When bill参与"微助力活动1"活动
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"0",
			"participant":"1"
		}
		"""
	When tom通过bill分享的"微助力活动1"链接参与活动
	Then tom可以查看jobs公众号二维码图片
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微助力1'
	Then tom收到自动回复"图文1"
	When tom点击"图文1"链接
	When tom参与"微助力活动1"活动
	Then tom获取个人活动页面
		"""
		{
			"rankings":"2",
			"power_score":"0",
			"participant":"2"
		}
		"""
	When bill清空浏览器
	When bill点击"图文1"链接
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"0",
			"participant":"2"
		}
		"""

@apps @powerme @frontend
Scenario:10 已帮助好友助力会员取消关注公众号
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力2'
	Then bill收到自动回复"图文2"
	When bill点击"图文2"链接
	When bill参与"微助力活动2"活动
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"0",
			"participant":"1"
		}
		"""
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微助力2'
	Then tom收到自动回复"图文2"
	When tom参与"微助力活动2"活动
	Then tom获取个人活动页面
		"""
		{
			"rankings":"2",
			"power_score":"0",
			"participant":"2"
		}
		"""
	When tom清空浏览器
	When tom通过bill分享的"微助力活动2"链接帮助好友助力
	Then tom收到自动回复"好友助力值+1，关系好就是任性！"
	When bill清空浏览器
	When bill点击"图文2"链接
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"1",
			"participant":"2"
		}
		"""
	When tom清空浏览器
	When tom取消关注jobs的公众号
	When bill清空浏览器
	When bill点击"图文2"链接
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"1",
			"participant":"1"
		}
		"""

@apps @powerme @frontend
Scenario:11 取消关注的会员通过会员好友分享页再次参加活动
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复"图文1"
	When bill点击"图文1"链接
	When bill参与"微助力活动1"活动
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"0",
			"participant":"1"
		}
		"""
	When tom关注jobs的公众号
	When tom通过bill分享的"微助力活动1"链接参与活动
	Then tom可以查看jobs公众号二维码图片
	When tom在微信中向jobs的公众号发送消息'微助力1'
	Then tom收到自动回复"图文1"
	When tom击"图文1"链接
	When tom参与"微助力活动1"活动
	Then tom获取个人活动页面
		"""
		{
			"rankings":"2",
			"power_score":"0",
			"participant":"2"
		}
		"""
	When tom清空浏览器
	When tom取消关注jobs的公众号
	When bill清空浏览器
	When bill点击"图文1"链接
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"0",
			"participant":"1"
		}
		"""
	When tom通过bill分享的"微助力活动1"链接参与活动
	Then tom可以查看jobs公众号二维码图片
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微助力1'
	Then tom收到自动回复"图文1"
	When tom点击"图文1"链接
	When tom参与"微助力活动1"活动
	Then tom获取个人活动页面
		"""
		{
			"rankings":"2",
			"power_score":"0",
			"participant":"2"
		}
		"""

@apps @powerme @frontend
Scenario:12 非会员通过分享链接为非会员好友助力
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力2'
	Then bill收到自动回复"图文2"
	When bill点击"图文2"链接
	When bill参与"微助力活动2"活动
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"0",
			"participant":"1"
		}
		"""
	When tom通过bill分享的"微助力活动2"链接帮助好友助力
	Then tom可以查看"带参数二维码1"图片
	When tom关注jobs的公众号
	When bill清空浏览器
	When bill点击"图文2"链接
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"1",
			"participant":"1"
		}
		"""
	When tom清空浏览器
	When tom取消关注jobs的公众号
	When bill清空浏览器
	When bill取消关注jobs的公众号
	When tom通过bill分享的"微助力活动2"链接帮助好友助力
	Then tom可以查看"带参数二维码1"图片
	When tom关注jobs的公众号
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力2'
	Then bill收到自动回复"图文2"
	When bill点击"图文2"链接
	When bill参与"微助力活动2"活动
	Then bill获取个人活动页面
		"""
		{
			"rankings":"1",
			"power_score":"0",
			"participant":"1"
		}
		"""
