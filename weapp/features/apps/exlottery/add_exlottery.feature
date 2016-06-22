#_author_:许韦 2015.06.20

Feature: 新建微信专享抽奖活动

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
	"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 50,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "优惠券2",
			"money": 50.00,
			"count": 50,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "5天后",
			"coupon_id_prefix": "coupon2_id_"
		}, {
			"name": "优惠券3",
			"money": 30.00,
			"count": 50,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "5天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
		}]
	"""

@mall2 @apps @apps_lottery @add_exlottery @apps_exlottery_backend @vito
Scenario:1 新建微信专项抽奖
	Given jobs登录系统
	When jobs新建专项抽奖活动
	"""
		[{
			"name":"专项抽奖活动01",
			"desc":"百事专项抽奖活动",
			"start_date":"今天",
			"end_date":"2天后",
			"reduce_integral":0,
			"send_integral":1,
			"win_rate":"50%",
			"lottory_code_num":10,
			"reply":"感谢您对杭州百事可乐的关注",
			"link_reply":"立即抽奖",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		},{
			"name":"专项抽奖活动02",
			"desc":"百事专项抽奖活动",
			"start_date":"3天前",
			"end_date":"昨天",
			"reduce_integral":10,
			"send_integral":5,
			"win_rate":"80%",
			"lottory_code_num":5,
			"reply":"感谢您对杭州百事可乐的关注",
			"link_reply":"立即抽奖",
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		},{
			"name":"专项抽奖活动03",
			"desc":"百事专项抽奖活动",
			"start_date":"2天后",
			"end_date":"3天后",
			"reduce_integral":0,
			"send_integral":0,
			"win_rate":"100%",
			"lottory_code_num":15,
			"reply":"感谢您对杭州百事可乐的关注",
			"link_reply":"立即抽奖",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
	"""
#	Then jobs获得专项抽奖活动列表
#	"""
#		[{
#			"name":"专项抽奖活动03",
#			"start_date":"2天后",
#			"end_date":"3天后",
#			"status":"未开始",
#			"participant_count":0,
#			"actions": ["码库","查看结果","链接","删除","预览"]
#		},{
#			"name":"专项抽奖活动02",
#			"start_date":"3天前",
#			"end_date":"昨天",
#			"status":"已过期",
#			"participant_count":0,
#			"actions": ["码库","查看结果","链接","删除","预览"]
#		},{
#			"name":"专项抽奖活动01",
#			"start_date":"今天",
#			"end_date":"2天后",
#			"status":"进行中",
#			"participant_count":0,
#			"actions": ["码库","查看结果","链接","关闭","预览"]
#		}]
#	"""


@mall2 @apps @apps_lottery @add_exlottery @apps_exlottery_backend
Scenario:2 新建微信专项抽奖活动，查看码库列表
	Given jobs登录系统
	When jobs新建专项抽奖活动
	"""
		[{
			"name":"专项抽奖活动001",
			"desc":"百事专项抽奖活动",
			"start_date":"明天",
			"end_date":"2天后",
			"reduce_integral":10,
			"send_integral":0,
			"win_rate":"60%",
			"lottory_code_num":5,
			"reply":"感谢您对杭州百事可乐的关注",
			"link_reply":"立即抽奖",
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":1000,
				"pic":"2.jpg"
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券2",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"优惠券",
				"coupon":"优惠券3",
				"pic":"4.jpg"
			}]
		}]
	"""
	Then jobs生成'专项抽奖活动001'码库
	"""
		["el8s539t18","el2f5e754g","el58fe24rf","elm8v6uj41","elmn782f2r"]
	"""
	Then jobs能获得'专项抽奖活动001'码库列表
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