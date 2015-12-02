#_author_:张三香 2015.11.30

Feature:手机端用户参与微信抽奖活动

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
			"count": 10,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		},{
			"name": "优惠券2",
			"money": 50.00,
			"count": 20,
			"limit_counts": "不限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分

@apps @lottery
Scenario:1 会员参加微信抽奖活动,需要消耗积分
	Given jobs登录系统
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖01",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":15,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"不限",
			"win_rate":50%,
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":20,
				"prize_type":"优惠券",
				"coupon":"优惠券2",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts"30,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
		"""
	#积分充足时，可以参加抽奖活动
	When bill参加微信抽奖活动'微信抽奖01'
	Then bill获得抽奖结果
		"""
		{
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"msg":"恭喜您获得了一张优惠券！<br />快去个人中心查看吧！<br />"
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	And bill在jobs的webapp中拥有5会员积分
	And bill在jobs的webapp中获得积分日志
		"""
		[{
			"content":"参与抽奖,消耗积分",
			"integral":-15
		},{
			"content":"首次关注",
			"integral":20
		}]
		"""
	#积分不足时，无法参加抽奖活动
	When bill参加微信抽奖活动'微信抽奖01'
	Then bill获得错误提示'积分不足'

	#增加积分后，则可正常参加抽奖活动
	Given jobs登录系统
	When jobs给"bill"加积分
			"""
			{
				"integral":10,
				"reason":""
			}
			"""

	When bill访问jobs的webapp
	And bill在jobs的webapp中拥有15会员积分

	When bill参加微信抽奖活动'微信抽奖01'
	Then bill获得抽奖结果
		"""
		{
			"prize_type":"优惠券",
			"coupon":"优惠券2",
			"msg":"恭喜您获得了一张优惠券！<br />快去个人中心查看吧！<br />"
		}
		"""
	Then bill在jobs的webapp中拥有0会员积分

@apps @lottery
Scenario:2 非会员通过分享链接参加微信抽奖活动
	Given jobs登录系统
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖02",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"不限",
			"win_rate":50%,
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":50,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":20,
				"prize_type":"积分",
				"integral":30,

				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts"30,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
		"""
	When bill参加微信抽奖活动'微信抽奖02'
	When bill把jobs的微信抽奖活动链接分享到朋友圈

	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom取消关注jobs的公众号

	When tom点击bill分享的微信抽奖活动链接
	When tom参加微信抽奖活动'微信抽奖02'
	Then tom获得抽奖结果
		"""
		{
			"prize_type":"积分",
			"integral":50,
			"msg":"恭喜您获得了积分奖励！<br />快去个人中心查看吧！<br />"
		}
		"""

@apps @lottery
Scenario:3 会员参加微信抽奖活动，抽奖限制为一人一次
	Given jobs登录系统
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖03",
			"start_date":"3天前",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":15,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一人一次",
			"win_rate":50%,
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":20,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts"30,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
		"""

	When bill参加微信抽奖活动'微信抽奖03'

	When 清空浏览器
	When bill参加微信抽奖活动'微信抽奖03'
	Then bill获得抽奖次数用完提示'您今天的抽奖机会已经用完,<br />明天再来吧~'

	When tom参加微信抽奖活动'微信抽奖03'
	When tom把jobs的微信抽奖活动链接分享到朋友圈

	When 清空浏览器
	When bill取消关注jobs的公众号
	When bill点击tom分享的微信抽奖活动链接
	When bill参与微信抽奖活动'微信抽奖03'
	Then bill获得错误提示'您今天的抽奖机会已经用完,<br />明天再来吧~'

@apps @lottery
Scenario:4 会员参加微信抽奖活动，抽奖限制为一天两次
	Given jobs登录系统
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖04",
			"start_date":"3天前",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一天两次",
			"win_rate":50%,
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":20,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts"30,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
		"""

	When bill参加微信抽奖活动'微信抽奖04'

	When 清空浏览器
	When bill参加微信抽奖活动'微信抽奖04'

	When 清空浏览器
	When bill参加微信抽奖活动'微信抽奖04'
	Then bill获得错误提示'您今天的抽奖机会已经用完,<br />明天再来吧~'

@apps @lottery
Scenario:5 会员参加微信抽奖活动，抽奖限制为不限
	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"name": "优惠券1",
			"count": 1,
			"members": ["bill"]
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖05",
			"start_date":"3天前",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一天两次",
			"win_rate":50%,
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":20,
				"prize_type":"优惠券",
				"coupon":"优惠券2",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts"30,
				"prize_type":"积分",
				"integral":100,
				"pic":"1.jpg"
			}]
		}]
		"""

	When bill参加微信抽奖活动'微信抽奖04'于'2天前'
	Then bill获得抽奖结果
		"""
		{
			"prize_type":"优惠券",
			"coupon":"优惠券2",
			"msg":"恭喜您获得了一张优惠券！<br />快去个人中心查看吧！<br />"
		}
		"""

	When 清空浏览器
	When bill参加微信抽奖活动'微信抽奖04'于'昨天'
	Then bill获得抽奖结果
		"""
		{
			"prize_type":"优惠券",
			"coupon":"优惠券2",
			"msg":"恭喜您获得了一张优惠券！<br />快去个人中心查看吧！<br />"
		}
		"""

	When 清空浏览器
	When bill参加微信抽奖活动'微信抽奖04'
	Then bill获得抽奖结果
		"""
		{
			"prize_type":"积分",
			"integral":100,
			"msg":"恭喜您获得了积分奖励！<br />快去个人中心查看吧！<br />"
		}
		"""

	When 清空浏览器
	When bill参加微信抽奖活动'微信抽奖04'
	Then bill获得抽奖结果
		"""
		{
			"msg":"没有中奖，再接再励吧~"
		}
		"""
@apps @lottery
Scenario:6 中获奖率为0中奖用户为0
	Given jobs登录系统
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖06",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"不限",
			"win_rate":0,
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":50,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":20,
				"prize_type":"积分",
				"integral":30,

				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts"30,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
		"""
	When bill参加微信抽奖活动'微信抽奖06'
	Then bill获得抽奖结果
		"""
		{
			"msg":"很遗憾，没有中奖，再接再厉吧！"
		}
		"""
@apps @lottery
Scenario:7 优惠券数量为0，用户无法获得优惠券奖励
	#重新设置优惠券规则，积分数量足，当添加的优惠券数量都为0时，用户无法获得奖励
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
			"count": 0,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		},{
			"name": "优惠券2",
			"money": 50.00,
			"count": 0,
			"limit_counts": "不限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	Given jobs登录系统
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖07",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"不限",
			"win_rate":50,
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":优惠券1,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":20,
				"prize_type":"优惠券",
				"coupon":优惠券2,
				"pic":""
		}]
		"""
	When bill参加微信抽奖活动'微信抽奖07'
	Then bill获得抽奖结果
		"""
		{
			"msg":"谢谢参与！"
		}
		"""
@apps @lottery
Scenario:8 中奖概率校验
	Given jobs登录系统
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖06",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":10,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"不限",
			"win_rate":5,
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":50,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":20,
				"prize_type":"积分",
				"integral":30,

				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts"30,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
		"""
	When bill参加微信抽奖活动'微信抽奖08'
	Then bill获得抽奖结果
		"""
		{
			"msg":"很遗憾，没有中奖，再接再厉吧！"
		}
		"""
	When 清空浏览器
	When Tom参加微信抽奖活动'微信抽奖08'
	Then Tom获得抽奖结果
		"""
		{
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"msg":"恭喜您获得了一张优惠券！<br />快去个人中心查看吧！<br />"
		}
		"""

