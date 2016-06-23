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
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"desc":"抽奖啦",
			"start_date":"今天",
			"end_date":"5天后",
			"reduce_integral":0,
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

@mall2 @apps @apps_exlottery @users_start_exlottery 
Scenario:1 抽奖码校验通过
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'el8s539t18'
	Then bill获得'专项抽奖'系统回复的消息
	"""
    感谢您对杭州百事可乐的关注<br />立即抽奖<br />
    """
    When bill使用抽奖码'el8s539t18'参加专项抽奖活动'专项抽奖'
	Then bill获得抽奖结果
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
Scenario:2 tom通过点击bill的朋友圈分享链接进行抽奖
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'el8s539t18'
	Then bill获得'专项抽奖'系统回复的消息
	"""
    感谢您对杭州百事可乐的关注<br />立即抽奖<br />
    """
	When bill点击'立即抽奖'进入'专项抽奖'活动页面
	When bill把jobs的'专项抽奖'活动链接分享到朋友圈

    When 清空浏览器
    Given tom关注jobs的公众号
    When tom访问jobs的webapp
    When tom在微信中向jobs的公众号发送消息'el8s539t18'
	Then tom获得'专项抽奖'系统回复的消息
	"""
    	该抽奖码已使用
    """
    When 清空浏览器
    When jerry点击bill分享的'专项抽奖'活动链接进行抽奖
	Then jerry获得抽奖结果
	"""
		该抽奖码已使用
	"""
