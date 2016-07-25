#_author_:江秋丽 2016.07.26

Feature:更新刮刮卡活动
	"""
	1、未开始状态的刮刮卡活动可以进行编辑并保存，进行中和已结束状态的不能进行更改；
	2、不同状态的刮刮卡活动，对应的操作列按钮不同:
		未开始:【查看结果】【链接】【删除】【预览】
		进行中:【查看结果】【链接】【关闭】【预览】
		已结束:【查看结果】【链接】【删除】【预览】
	3、进行中的刮刮卡活动可以进行'关闭'操作，关闭后结束时间会随之更改为关闭时的时间，状态变为'已结束'
	4、未开始和已结束状态的刮刮卡活动，可以进行'删除'操作
	"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 500,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建刮刮卡活动
		"""
		[{
			"name":"刮刮卡刮奖01",
			"start_date":"明天",
			"end_date":"2天后",
			"desc":"刮奖啦刮奖啦",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"reduce_integral":0,
			"send_integral":1,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一人一次",
			"win_rate":"50%",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"实物",
				"gift":"精美礼品"
			}]
		},{
			"name":"刮刮卡刮奖02",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"刮奖啦刮奖啦",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"reduce_integral":100,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一天一次",
			"win_rate":"50%",
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"实物",
				"gift":"精美礼品"
			}]
		},{
			"name":"刮刮卡刮奖03",
			"start_date":"3天前",
			"end_date":"昨天",
			"desc":"刮奖啦刮奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"不限",
			"win_rate":"50%",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"实物",
				"gift":"精美礼品"
			}]
		}]
		"""

@mall2 @apps @apps_scratch @update_scratch
Scenario:1 编辑'未开始'状态的刮刮卡活动
	Given jobs登录系统
	Then jobs获得刮刮卡活动列表
		"""
		[{
			"name":"刮刮卡刮奖03",
			"status":"已结束"
		},{
			"name":"刮刮卡刮奖02",
			"status":"进行中"
		},{
			"name":"刮刮卡刮奖01",
			"status":"未开始"
		}]
		"""
	#修改名称、时间、参与限制及奖项设置
	When jobs编辑刮刮卡活动'刮刮卡刮奖01'
		"""
		[{
			"name":"刮刮卡刮奖001",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"刮奖啦刮奖啦",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"reduce_integral":0,
			"send_integral":1,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一天一次",
			"win_rate":"50%",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券1"
			},{
				"prize_grade":"二等奖",
				"prize_counts":20,
				"prize_type":"积分",
				"integral":100
			},{
				"prize_grade":"三等奖",
				"prize_counts":30,
				"prize_type":"积分",
				"integral":30
			}]
		}]
		"""
	Then jobs获得刮刮卡活动列表
		"""
		[{
			"name":"刮刮卡刮奖03",
			"status":"已结束"
		},{
			"name":"刮刮卡刮奖02",
			"status":"进行中"
		},{
			"name":"刮刮卡刮奖001",
			"status":"进行中"
		}]
		"""
	And jobs获得刮刮卡活动'刮刮卡刮奖001'
		"""
		[{
			"name":"刮刮卡刮奖001",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"刮奖啦刮奖啦",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"reduce_integral":0,
			"send_integral":1,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一天一次",
			"win_rate":"50%",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券1"
			},{
				"prize_grade":"二等奖",
				"prize_counts":20,
				"prize_type":"积分",
				"integral":100
			},{
				"prize_grade":"三等奖",
				"prize_counts":30,
				"prize_type":"积分",
				"integral":30
			}]
		}]
		"""

@mall2 @apps @apps_scratch @update_scratch
Scenario:2 关闭'进行中'状态的刮刮卡活动
	Given jobs登录系统
	Then jobs获得刮刮卡活动列表
		"""
		[{
			"name":"刮刮卡刮奖03",
			"status":"已结束"
		},{
			"name":"刮刮卡刮奖02",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中"
		},{
			"name":"刮刮卡刮奖01",
			"status":"未开始"
		}]
		"""
	When jobs关闭刮刮卡活动'刮刮卡刮奖02'
	Then jobs获得刮刮卡活动列表
		"""
		[{
			"name":"刮刮卡刮奖03",
			"status":"已结束"
		},{
			"name":"刮刮卡刮奖02",
			"start_date":"今天",
			"end_date":"今天",
			"status":"已结束"
		},{
			"name":"刮刮卡刮奖01",
			"status":"未开始"
		}]
		"""

@mall2 @apps @apps_scratch @update_scratch
Scenario:3 删除'未开始'和'已结束'状态的刮刮卡活动
	Given jobs登录系统
	Then jobs获得刮刮卡活动列表
		"""
		[{
			"name":"刮刮卡刮奖03",
			"status":"已结束",
			"actions": ["查看结果","链接","删除","预览"]
		},{
			"name":"刮刮卡刮奖02",
			"status":"进行中",
			"actions": ["查看结果","链接","关闭","预览"]
		},{
			"name":"刮刮卡刮奖01",
			"status":"未开始",
			"actions": ["查看结果","链接","删除","预览"]
		}]
		"""
	#删除'未开始'状态的刮刮卡刮奖01
	When jobs删除刮刮卡活动'刮刮卡刮奖01'
	Then jobs获得刮刮卡活动列表
		"""
		[{
			"name":"刮刮卡刮奖03",
			"status":"已结束",
			"actions": ["查看结果","链接","删除","预览"]
		},{
			"name":"刮刮卡刮奖02",
			"status":"进行中",
			"actions": ["查看结果","链接","关闭","预览"]
		}]
		"""

	#删除'已结束'状态的刮刮卡刮奖03
	When jobs删除刮刮卡活动'刮刮卡刮奖03'
	Then jobs获得刮刮卡活动列表
		"""
		[{
			"name":"刮刮卡刮奖02",
			"status":"进行中",
			"actions": ["查看结果","链接","关闭","预览"]
		}]
		"""

@mall2 @apps @apps_scratch @update_scratch
Scenario:4 编辑'进行中'状态的刮刮卡活动
	Given jobs登录系统
	Then jobs获得刮刮卡活动列表
		"""
		[{
			"name":"刮刮卡刮奖03",
			"status":"已结束"
		},{
			"name":"刮刮卡刮奖02",
			"status":"进行中"
		},{
			"name":"刮刮卡刮奖01",
			"status":"未开始"
		}]
		"""
	#修改奖品数量设置
	When jobs编辑刮刮卡活动'刮刮卡刮奖02'
		"""
		[{
			"name":"刮刮卡刮奖02",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"刮奖啦刮奖啦",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"reduce_integral":100,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一天一次",
			"win_rate":"50%",
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":15,
				"prize_type":"积分",
				"integral":100
			},{
				"prize_grade":"二等奖",
				"prize_counts":40,
				"prize_type":"优惠券",
				"coupon":"优惠券1"
			},{
				"prize_grade":"三等奖",
				"prize_counts":60,
				"prize_type":"实物",
				"gift":"精美礼品"
			}]
		}]
		"""
	Then jobs获得刮刮卡活动列表
		"""
		[{
			"name":"刮刮卡刮奖03",
			"status":"已结束"
		},{
			"name":"刮刮卡刮奖02",
			"status":"进行中"
		},{
			"name":"刮刮卡刮奖01",
			"status":"未开始"
		}]
		"""
	And jobs获得刮刮卡活动'刮刮卡刮奖02'
		"""
		[{
			"name":"刮刮卡刮奖02",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"刮奖啦刮奖啦",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"reduce_integral":100,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一天一次",
			"win_rate":"50%",
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":15,
				"prize_type":"积分",
				"integral":100
			},{
				"prize_grade":"二等奖",
				"prize_counts":40,
				"prize_type":"优惠券",
				"coupon":"优惠券1"
			},{
				"prize_grade":"三等奖",
				"prize_counts":60,
				"prize_type":"实物",
				"gift":"精美礼品"
			}]
		}]
		"""