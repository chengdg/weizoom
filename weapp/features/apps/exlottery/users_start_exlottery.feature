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
			"code_count":"2000",
			"automatic_reply:"谢谢"，
			"link":"立即抽奖"，
			"win_rate":"50%",
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
		}]
		"""
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的抽奖码
	Then bill在jobs的webapp中拥有抽奖码
	When bill使用抽奖码参加抽奖活动'专项抽奖'
@mall2 @apps @apps_exlottery @users_start_exlottery 
Scenario:1 抽奖码校验通过
	Then bill获得抽奖结果
		"""
			[{
				"prize_grade":"一等奖",
				"prize_name":"迪士尼门票"
			}]
		"""
	Given jobs登录系统
	Then jobs获得码库详情中的"抽奖码"和"抽奖信息"
		"""
			[{
				"number":"el12345678"
				"prize_grade":"一等奖",
				"prize_name":"迪士尼门票"
				"member":"bill",
				"time":"2016-06-20"
			}]
		"""
Scenario:2 抽奖码校验不通过
	Then bill获得公众号提示
		"""
			[{
				"reply":"抽奖码不正确"
			}]
		"""
