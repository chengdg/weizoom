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
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的抽奖码
	Then bill在jobs的webapp中拥有抽奖码

@mall2 @apps @apps_exlottery @users_participate_exlottery 
Scenario:1专项抽奖活动未开始
	Given jobs登录系统
	When jobs新建抽奖活动
	"""
		[{
			"name":"专项抽奖",
			"desc":"抽奖啦",
			"start_date":"2天后",
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
	When bill访问jobs的webapp
	When bill使用抽奖码参加抽奖活动'专项抽奖'
	Then bill获得公众号回复
		"""
		[{
			"reply":"该抽奖码尚未生效"
		}]
		"""
@mall2 @apps @apps_exlottery @users_participate_exlottery 
Scenario:2 活动已结束并且抽奖码已使用
	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"desc":"抽奖啦",
			"start_date":"4天前",
			"end_date":"1天前",
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
	When bill访问jobs的webapp
	When bill使用抽奖码参加抽奖活动'专项抽奖'
	Then bill获得公众号回复
		"""
		[{
			"reply":"该抽奖码已使用"
		}]
		"""
@mall2 @apps @apps_exlottery @users_participate_exlottery 
Scenario:3 活动已结束并且抽奖码未使用
	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"desc":"抽奖啦",
			"start_date":"4天前",
			"end_date":"1天前",
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
	When bill访问jobs的webapp
	When bill使用抽奖码参加抽奖活动'专项抽奖'
	Then bill获得公众号回复
		"""
		[{
			"reply":"该抽奖码已过期"
		}]
		"""
@mall2 @apps @apps_exlottery @users_participate_exlottery 
Scenario:4 活动进行中，抽奖码已使用
	Given jobs登录系统
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
	When bill访问jobs的webapp
	When bill使用抽奖码参加抽奖活动'专项抽奖'
	Then bill获得公众号回复
		"""
		[{
			"reply":"该抽奖码已使用"
		}]
		"""
@mall2 @apps @apps_exlottery @users_participate_exlottery 
Scenario:5 抽奖码不正确
	Given jobs登录系统
	When jobs新建微信抽奖活动
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
	When bill访问jobs的webapp
	When bill使用抽奖码参加抽奖活动'专项抽奖'
	Then bill获得公众号回复
		"""
		[{
			"reply":"请输入正确的抽奖码"
		}]
		"""
@mall2 @apps @apps_exlottery @users_participate_exlottery 
Scenario:6 活动进行中，抽奖码正确且未使用
	Given jobs登录系统
	When jobs新建抽奖活动
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
	When bill访问jobs的webapp
	When bill使用抽奖码参加抽奖活动'专项抽奖'
	Then bill获得公众号回复
		"""
		[{
			"reply":[{
				"content":"感谢",
				"link":"立即抽奖"
			}]
		}]
		"""
	