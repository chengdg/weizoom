#_author_:许韦 2016.06.20

Feature:更新微信专项抽奖活动
	"""
	1、未开始状态的微信抽奖可以进行编辑并保存，进行中和已结束状态的不能进行更改；
	2、不同状态的微信抽奖，对应的操作列按钮不同:
		未开始:【码库】【查看结果】【链接】【删除】【预览】
		进行中:【码库】【查看结果】【链接】【关闭】【预览】
		已结束:【码库】【查看结果】【链接】【删除】【预览】
	3、进行中的微信抽奖可以进行'关闭'操作，关闭后结束时间会随之更改为关闭时的时间，状态变为'已结束'
	4、未开始和已结束状态的微信抽奖，可以进行'删除'操作
	"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 500,
			"limit_counts": 10,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
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
			"jump_url":"新建百事抽奖活动"
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
			"name":"专项抽奖01",
			"share_intro":"百事专项抽奖活动",
			"desc":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"start_date":"明天",
			"end_date":"2天后",
			"reduce_integral":0,
			"send_integral":1,
			"win_rate":"100%",
			"lottory_code_num":5,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":0,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":0,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		},{
			"name":"专项抽奖02",
			"share_intro":"百事专项抽奖活动",
			"desc":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"start_date":"今天",
			"end_date":"2天后",
			"reduce_integral":100,
			"send_integral":0,
			"win_rate":"100%",
			"lottory_code_num":5,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":0,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":0,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		},{
			"name":"专项抽奖03",
			"share_intro":"百事专项抽奖活动",
			"desc":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"start_date":"3天前",
			"end_date":"昨天",
			"reduce_integral":0,
			"send_integral":0,
			"win_rate":"100%",
			"lottory_code_num":5,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":0,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":0,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
		"""

	Then jobs生成'专项抽奖01'码库
	"""
		["el8s539t18","el2f5e754g","el58fe24rf","elm8v6uj41","elmn782f2r"]
	"""


@mall2 @apps @apps_exlottery @update_exlottery
Scenario:1 编辑'未开始'状态的微信专项抽奖活动
	Given jobs登录系统
	Then jobs获得专项抽奖活动列表
		"""
		[{
			"name":"专项抽奖03",
			"status":"已结束"
		},{
			"name":"专项抽奖02",
			"status":"进行中"
		},{
			"name":"专项抽奖01",
			"status":"未开始"
		}]
		"""
	Then jobs能获得'专项抽奖01'码库列表
		"""
		[{
			"lottery_code":"el8s539t18"
		},{
			"lottery_code":"el2f5e754g"
		},{
			"lottery_code":"el58fe24rf"
		},{
			"lottery_code":"elm8v6uj41"
		},{
			"lottery_code":"elmn782f2r"
		}]
		"""
	#修改名称、时间、自动回复语、中奖规则、码库数量及奖项设置
	When jobs编辑专项抽奖活动'专项抽奖01'
		"""
		[{
			"name":"微信抽奖001",
			"share_intro":"百事专项抽奖活动",
			"desc":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"start_date":"今天",
			"end_date":"2天后",
			"reduce_integral":0,
			"send_integral":1,
			"win_rate":"100%",
			"lottory_code_num":2,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":0,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":0,
				"prize_type":"积分",
				"integral":30,
				"pic":"1.jpg"
			}]
		}]
		"""
	Then jobs获得专项抽奖活动列表
		"""
		[{
			"name":"专项抽奖03",
			"status":"已结束"
		},{
			"name":"专项抽奖02",
			"status":"进行中"
		},{
			"name":"微信抽奖001",
			"status":"进行中"
		}]
		"""
	And jobs获得专项抽奖活动'微信抽奖001'
		"""
		[{
			"name":"微信抽奖001",
			"share_intro":"百事专项抽奖活动",
			"desc":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"start_date":"今天",
			"end_date":"2天后",
			"reduce_integral":0,
			"send_integral":1,
			"win_rate":"100%",
			"lottory_code_num":2,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":0,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":0,
				"prize_type":"积分",
				"integral":30,
				"pic":"1.jpg"
			}]
		}]
		"""
	Then jobs生成'微信抽奖001'码库
	"""
		["el3h5uj74u","elf8t1t5ha"]
	"""
	And jobs能获得'微信抽奖001'码库列表
		"""
		[{
			"lottery_code":"el3h5uj74u"
		},{
			"lottery_code":"elf8t1t5ha"
		}]
		"""

@mall2 @apps @apps_exlottery @update_exlottery
Scenario:2 关闭'进行中'状态的微信专项抽奖活动
	Given jobs登录系统
	Then jobs获得专项抽奖活动列表
		"""
		[{
			"name":"专项抽奖03",
			"status":"已结束"
		},{
			"name":"专项抽奖02",
			"status":"进行中"
		},{
			"name":"专项抽奖01",
			"status":"未开始"
		}]
		"""
	When jobs关闭专项抽奖活动'专项抽奖02'
	Then jobs获得专项抽奖活动列表
		"""
		[{
			"name":"专项抽奖03",
			"status":"已结束"
		},{
			"name":"专项抽奖02",
			"status":"已结束"
		},{
			"name":"专项抽奖01",
			"status":"未开始"
		}]
		"""

@mall2 @apps @apps_exlottery @update_exlottery
Scenario:3 删除'未开始'和'已结束'状态的微信专项抽奖活动
	Given jobs登录系统
	Then jobs获得专项抽奖活动列表
		"""
		[{
			"name":"专项抽奖03",
			"status":"已结束",
			"actions": ["码库","查看结果","链接","删除","预览"]
		},{
			"name":"专项抽奖02",
			"status":"进行中",
			"actions": ["码库","查看结果","链接","关闭","预览"]
		},{
			"name":"专项抽奖01",
			"status":"未开始",
			"actions": ["码库","查看结果","链接","删除","预览"]
		}]
		"""
	#删除'未开始'状态的专项抽奖01
	When jobs删除专项抽奖活动'专项抽奖01'
	Then jobs获得专项抽奖活动列表
		"""
		[{
			"name":"专项抽奖03",
			"status":"已结束",
			"actions": ["码库","查看结果","链接","删除","预览"]
		},{
			"name":"专项抽奖02",
			"status":"进行中",
			"actions": ["码库","查看结果","链接","关闭","预览"]
		}]
		"""

	#删除'已结束'状态的专项抽奖03
	When jobs删除专项抽奖活动'专项抽奖03'
	Then jobs获得专项抽奖活动列表
		"""
		[{
			"name":"专项抽奖02",
			"status":"进行中",
			"actions": ["码库","查看结果","链接","关闭","预览"]
		}]
		"""