#_author_:江秋丽 2016.06.20

Feature:微信用户参与专项抽奖活动

Background:
	Given jobs登录系统
	And jobs设定会员积分策略
		"""
		{
			"be_member_increase_count":20
		}
		"""
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

@mall2 @apps @apps_exlottery @users_participate_exlottery 
Scenario:1 活动进行中，抽奖码正确且未使用
	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"desc":"抽奖啦",
			"start_date":"今天",
			"end_date":"5天后",
			"reduce_integral":5,
			"send_integral":0,
			"win_rate":"60%",
			"lottory_code_num":1,
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
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
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
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'el8s539t18'
	Then bill获得'专项抽奖'系统回复的消息
	"""
    感谢您对杭州百事可乐的关注<br />立即抽奖<br />
    """
	
@mall2 @apps @apps_exlottery @users_participate_exlottery 
Scenario:2专项抽奖活动未开始,bill使用抽奖码进行抽奖
	Given jobs登录系统
	When jobs新建专项抽奖活动
	"""
		[{
			"name":"专项抽奖",
			"desc":"抽奖啦",
			"start_date":"2天后",
			"end_date":"5天后",
			"reduce_integral":5,
			"send_integral":0,
			"win_rate":"60%",
			"lottory_code_num":1,
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
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
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
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'el8s539t18'
	Then bill获得'专项抽奖'系统回复的消息
	"""
		该抽奖码尚未生效
	"""
	
@mall2 @apps @apps_exlottery @users_participate_exlottery
Scenario:3 活动已结束并且抽奖码已使用，bill使用抽奖码进行抽奖
	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"desc":"抽奖啦",
			"start_date":"今天",
			"end_date":"明天",
			"reduce_integral":5,
			"send_integral":0,
			"win_rate":"100%",
			"lottory_code_num":1,
			"reply":"感谢您对杭州百事可乐的关注",
			"link_reply":"立即抽奖",
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":0,
				"prize_type":"积分",
				"integral":1000,
				"pic":"2.jpg"
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":0,
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
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'el8s539t18'
	Then bill获得'专项抽奖'系统回复的消息
	"""
    感谢您对杭州百事可乐的关注<br />立即抽奖<br />
    """
	When bill点击'立即抽奖'进入'专项抽奖'活动页面
	When bill参加专项抽奖活动'专项抽奖'
	Then bill获得专项抽奖结果
	"""
		{
			"prize_grade":"二等奖",
			"prize_name":"优惠券1"
		}
	"""
	When bill在微信中向jobs的公众号发送消息'el8s539t18'
	Then bill获得'专项抽奖'系统回复的消息
	"""
		该抽奖码已使用
	"""

@mall2 @apps @apps_exlottery @users_participate_exlottery 
Scenario:4 活动已结束并且抽奖码未使用，bill使用抽奖码进行抽奖
	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"desc":"抽奖啦",
			"start_date":"4天前",
			"end_date":"1天前",
			"reduce_integral":5,
			"send_integral":0,
			"win_rate":"60%",
			"lottory_code_num":1,
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
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
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
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'el8s539t18'
	Then bill获得'专项抽奖'系统回复的消息
	"""
    该抽奖码已过期
    """

@mall2 @apps @apps_exlottery @users_participate_exlottery
Scenario:5 活动进行中，抽奖码已使用，bill使用抽奖码进行抽奖
	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"desc":"抽奖啦",
			"start_date":"4天前",
			"end_date":"2天后",
			"reduce_integral":5,
			"send_integral":0,
			"win_rate":"100%",
			"lottory_code_num":1,
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
				"prize_counts":0,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":0,
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
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'el8s539t18'
	Then bill获得'专项抽奖'系统回复的消息
	"""
    感谢您对杭州百事可乐的关注<br />立即抽奖<br />

    """
    When bill点击'立即抽奖'进入'专项抽奖'活动页面
	When bill参加专项抽奖活动'专项抽奖'
	Then bill获得专项抽奖结果
	"""
		{
			"prize_grade":"一等奖",
			"prize_name":"1000积分"
		}
	"""
	When bill在微信中向jobs的公众号发送消息'el8s539t18'
	Then bill获得'专项抽奖'系统回复的消息
	"""
    该抽奖码已使用

    """
	
@mall2 @apps @apps_exlottery @users_participate_exlottery 
Scenario:6 抽奖码不正确，bill使用抽奖码进行抽奖
	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"desc":"抽奖啦",
			"start_date":"今天",
			"end_date":"5天后",
			"reduce_integral":5,
			"send_integral":0,
			"win_rate":"60%",
			"lottory_code_num":1,
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
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
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
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'el12345678'
	Then bill获得'专项抽奖'系统回复的消息
	"""
    请输入正确的抽奖码

    """