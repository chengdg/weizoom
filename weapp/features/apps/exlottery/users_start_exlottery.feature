#_author_:江秋丽 2016.06.20

Feature:微信用户进入专项抽奖页面进行抽奖


Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 50,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "优惠券2",
			"money": 50.00,
			"count": 50,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "5天后",
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	When jobs已添加单图文
		"""
		[{
			"title":"百事抽奖活动单图文",
			"cover": [{
				"url": "6.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"百事抽奖",
			"content":"百事抽奖",
			"jump_url":"专项抽奖"
		}]
		"""
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"抽奖规则",
			"keyword":
				[{
					"keyword": "百事抽奖",
					"type": "equal"
				}],
			"keyword_reply":
				[{
					"reply_content":"百事抽奖活动单图文",
					"reply_type":"text_picture"
				}]
		}]
		"""
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"share_intro":"百事专项抽奖活动",
			"desc":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"start_date":"今天",
			"end_date":"2天后",
			"reduce_integral":0,
			"send_integral":0,
			"win_rate":"100%",
			"lottory_code_num":1,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":0,
				"prize_type":"积分",
				"integral":1000,
				"pic":"2.jpg"
			},{
				"prize_grade":"二等奖",
				"prize_counts":0,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券2",
				"pic":"4.jpg"
			}]
		}]
		"""
	Then jobs生成'专项抽奖'码库
	"""
		["el8s539t18"]
	"""	

@mall2 @apps @apps_exlottery @users_start_exlottery
Scenario:1 抽奖码校验通过
	Given bill关注jobs的公众号
	When bill访问jobs的webapp	
	When bill在微信中向jobs的公众号发送消息'百事抽奖'
	Then bill收到自动回复'百事抽奖活动单图文'
	When bill点击图文'百事抽奖活动单图文'进入专项抽奖活动页面
	Then bill在专项抽奖活动首页获得验证码'tudf'
	When bill在专项抽奖活动首页中输入验证码'tudf'
	When bill在专项抽奖活动首页中输入抽奖码'el8s539t18'
	When bill点击'立即抽奖'进入专项抽奖活动内容页
	When bill参加专项抽奖活动'专项抽奖'
	Then bill获得专项抽奖结果
	"""
		{
			"prize_grade":"三等奖",
			"prize_name":"优惠券2"
		}
	"""

	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
	"""
		[{
			"coupon_id": "coupon2_id_1",
			"money": 50.00,
			"status": "未使用"
		}]
	"""
	Given jobs登录系统
	Then jobs能获得'专项抽奖'码库列表
		"""
			[{
				"lottery_code":"el8s539t18",
				"user":"bill",
				"use_date":"今天",
				"prize_grade":"三等奖",
				"prize_name":"优惠券2"
			}]
		"""

@mall2 @apps @apps_exlottery @users_start_exlottery
Scenario:2 其他微信用户通过回复分享至朋友圈的专项抽奖活动页面参与活动
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'百事抽奖'
	Then bill收到自动回复'百事抽奖活动单图文'
	When bill点击图文'百事抽奖活动单图文'进入专项抽奖活动页面
	Then bill在专项抽奖活动首页获得验证码'tudf'
	When bill在专项抽奖活动首页中输入验证码'tudf'
	When bill在专项抽奖活动首页中输入抽奖码'el8s539t18'
	When bill点击'立即抽奖'进入专项抽奖活动内容页	
	When bill把jobs的'专项抽奖'活动链接分享到朋友圈

    When 清空浏览器
    Given tom关注jobs的公众号
    When tom访问jobs的webapp
    When tom点击bill分享的'专项抽奖'活动链接参加专项抽奖活动
	Then tom获得页面提示的消息
	"""
    	该抽奖码已使用
    """
    When 清空浏览器
    When jerry点击bill分享的'专项抽奖'活动链接参加专项抽奖活动
	When jerry通过识别弹层中的公众号二维码关注jobs的公众号
	When jerry点击bill分享的'专项抽奖'活动链接参加专项抽奖活动
	Then jerry获得专项抽奖结果
	"""
		该抽奖码已使用
	"""
