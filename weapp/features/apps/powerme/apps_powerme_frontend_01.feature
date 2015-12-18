
#_author_:张三香 2015.11.27

Feature:会员参加微助力活动
	"""
		1、会员取消关注公众号后,再次关注公众号,之前的活动排名不会恢复
		2、会员A分享活动链接,取消关注公众号后，好友B点击A之前分享的链接帮其助力，A再关注公众号后，不会出现A的排名
		3、会员A分享活动链接,取消关注公众号,再关注公众号后，好友B点击A之前分享的链接帮其助力后,A的排名出现
	备注：
		2015-12-18 业务逻辑修改:取消关注的会员，其助力值和排名不消失（前台和后台都保留）
	"""

Background:
	Given jobs登录系统
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
		}]
		"""

	When bill关注jobs的公众号
	When tom关注jobs的公众号

@mall2 @apps_powerme @apps_powerme_frontend
Scenario:1 会员取消关注公众号后,再次关注公众号,之前的活动排名恢复
	#会员A'分享'活动链接,有A的排名
	#会员A'取消关注'公众号,A的排名不消失
	#会员A'关注'公众号号,之前A的排名会再出现

	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	When bill把jobs的微助力活动链接分享到朋友圈

	When 清空浏览器
	When tom点击bill分享的微助力活动链接进行助力
	When tom点击bill分享的微助力活动链接
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
		|  1   | bill |   1   |

	Given jobs登录系统
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动1",
			"participant_count":1
		}]
		"""
	When jobs查看微助力活动'微助力活动1'
	Then jobs获得微助力活动'微助力活动1'的结果列表
		| rank | member_name | powerme_value | parti_time |
		|  1   | bill        |     1         | 今天       |

	When bill取消关注jobs的公众号

	Given jobs登录系统
	When jobs查看微助力活动'微助力活动1'
	Then jobs获得微助力活动'微助力活动1'的结果列表
		| rank | member_name | powerme_value | parti_time |
		|  1   | bill        |     1         | 今天       |
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动1",
			"participant_count":1
		}]
		"""
	When bill关注jobs的公众号
	Given jobs登录系统
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动1",
			"participant_count":1
		}]
		"""
	When jobs查看微助力活动'微助力活动1'
	Then jobs获得微助力活动'微助力活动1'的结果列表
		| rank | member_name | powerme_value | parti_time |
		|  1   | bill        |     1         | 今天       |

@mall2 @apps_powerme @apps_powerme_frontend
Scenario:2 会员A分享活动链接,取消关注公众号后，好友B帮其助力
	#会员A'分享'活动链接,有A的排名
	#会员A'取消关注'公众号,A的排名不消失
	#会员B'点击'A之前分享的链接，帮其助力,有A的排名
	#A再次'关注'公众号,有A的排名

	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	When bill把jobs的微助力活动链接分享到朋友圈

	Given jobs登录系统
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动1",
			"participant_count":1
		}]
		"""
	When jobs查看微助力活动'微助力活动1'
	Then jobs获得微助力活动'微助力活动1'的结果列表
		| rank | member_name | powerme_value | parti_time |
		|  1   | bill        |     0         | 今天       |

	When bill取消关注jobs的公众号

	When 清空浏览器
	When tom点击bill分享的微助力活动链接进行助力

	Given jobs登录系统
	When jobs查看微助力活动'微助力活动1'
	Then jobs获得微助力活动'微助力活动1'的结果列表
		| rank | member_name | powerme_value | parti_time |
		|  1   | bill        |     0         | 今天       |
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动1",
			"participant_count":1
		}]
		"""

	When bill关注jobs的公众号

	Given jobs登录系统
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动1",
			"participant_count":1
		}]
		"""
	When jobs查看微助力活动'微助力活动1'
	Then jobs获得微助力活动'微助力活动1'的结果列表
		| rank | member_name | powerme_value | parti_time |
		|  1   | bill        |     0         | 今天       |

@mall2 @apps_powerme @apps_powerme_frontend
Scenario:3 会员A分享活动链接,取消关注公众号,再关注公众号后，好友B帮其助力
	#会员A'分享'活动链接,有A的排名
	#会员A'取消关注'公众号,A的排名不消失
	#会员A'关注'公众号号,有A的排名
	#会员B'点击'A分享的活动链接，给其助力,A的排名出现

	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微助力1'
	Then bill收到自动回复'微助力1单图文'
	When bill点击图文"微助力1单图文"进入微助力活动页面
	When bill把jobs的微助力活动链接分享到朋友圈

	When bill取消关注jobs的公众号

	When 清空浏览器
	When bill关注jobs的公众号

	When 清空浏览器
	When tom点击bill分享的微助力活动链接进行助力
	When tom点击bill分享的微助力活动链接
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
		|  1   | bill |   1   |

	Given jobs登录系统
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动1",
			"participant_count":1
		}]
		"""
	When jobs查看微助力活动'微助力活动1'
	Then jobs获得微助力活动'微助力活动1'的结果列表
		| rank | member_name | powerme_value | parti_time |
		|  1   | bill        |     1         | 今天       |





