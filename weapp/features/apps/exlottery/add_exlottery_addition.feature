#_author_:江秋丽 2015.06.30

Feature: 新建微信专项抽奖活动

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
	"""
		[
			"name": "优惠券1",
			"money": 100.00,
			"count": 50,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		]
	"""

@mall2 @apps @apps_lottery  @add_exlottery_addition
Scenario:1 新建微信专项抽奖
	Given jobs登录系统
	When jobs新建专项抽奖活动
	"""
		[{
			"name":"专项抽奖活动01",
			"share_intro":"百事专项抽奖活动",
			"rule":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"start_date":"今天",
			"end_date":"2天后",
			"reduce_integral":0,
			"send_integral":0,
			"win_rate":"100%",
			"lottory_code_num":10,
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
				"pic":"4.jpg"
			}]
		},{
			"name":"专项抽奖活动02",
			"share_intro":"百事专项抽奖活动",
			"rule":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"start_date":"3天前",
			"end_date":"昨天",
			"reduce_integral":0,
			"send_integral":0,
			"win_rate":"100%",
			"lottory_code_num":10,
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
				"pic":"4.jpg"
			}]
		},{
			"name":"专项抽奖活动03",
			"share_intro":"百事专项抽奖活动",
			"rule":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"start_date":"2天后",
			"end_date":"3天后",
			"reduce_integral":0,
			"send_integral":0,
			"win_rate":"100%",
			"lottory_code_num":10,
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
				"pic":"4.jpg"
			}]
		}]
	"""
	Then jobs获得专项抽奖活动列表
	"""
		[{
			"name":"专项抽奖活动03",
			"start_date":"2天后",
			"end_date":"3天后",
			"status":"未开始",
			"participant_count":0,
			"actions": ["码库","查看结果","链接","删除","预览"]
		},{
			"name":"专项抽奖活动02",
			"start_date":"3天前",
			"end_date":"昨天",
			"status":"已结束",
			"participant_count":0,
			"actions": ["码库","查看结果","链接","删除","预览"]
		},{
			"name":"专项抽奖活动01",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"participant_count":0,
			"actions": ["码库","查看结果","链接","关闭","预览"]
		}]
	"""


