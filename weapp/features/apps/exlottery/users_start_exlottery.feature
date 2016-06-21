#_author_:江秋丽 2016.06.20

Feature:微信用户进入抽奖页面进行抽奖


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
	Then jobs生成码库
	"""
		["el8s539t18"]
	"""

	

@mall2 @apps @apps_exlottery @users_start_exlottery 
Scenario:1 抽奖码校验通过
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的抽奖码
	When bill使用抽奖码"el8s539t18"参加抽奖活动'专项抽奖'
	Then bill获得抽奖结果
		"""
			{
				"prize_grade":"一等奖",
				"prize_name":"迪士尼门票"
			}
		"""
	Given jobs登录系统
	Then jobs获得码库详情列表
		"""
			[{
				"number":"el8s539t18",
				"prize_grade":"一等奖",
				"prize_name":"迪士尼门票"
				"member":"bill",
				"time":"今天"
			}]
		"""
Scenario:2 tom通过点击bill的朋友圈分享链接进行抽奖
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的抽奖码
	When bill使用抽奖码"el8s539t18"参加抽奖活动'专项抽奖'
	Then bill获得抽奖结果
		"""
			{
				"prize_grade":"一等奖",
				"prize_name":"迪士尼门票"
			}
		"""
	Given bill关注jobs的公众号
	When bill把jobs的抽奖活动链接分享到朋友圈
	#暂时用先关注再取消关注的方式来模拟非会员的情况
	When tom关注jobs的公众号
	And tom取消关注jobs的公众号
	When tom点击bill分享的抽奖链接进行抽奖
	When tom通过弹出的二维码关注jobs的公众号
	When tom访问jobs的webapp	
	When tom使用抽奖码"el8s539t18"参加抽奖活动'专项抽奖'
	Then tom获得抽奖结果
		"""
			{
				"reply":"抽奖码不正确"
			}
		"""
