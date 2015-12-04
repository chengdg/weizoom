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
			"count": 50,
			"limit_counts": "不限",
			"start_date": "今天",
			"end_date": "10天后",
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
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	Then jobs能获得优惠券'优惠券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 50.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分

@mall2 @apps_lottery @apps_lottery_frontend @kuki
Scenario:1 会员参加微信抽奖活动,需要消耗积分
	Given jobs登录系统
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":15,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"不限",
			"win_rate":"100%",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			}]
		}]
		"""
	#积分充足时，可以参加抽奖活动
#	When bill参加微信抽奖活动'微信抽奖'
#	Then bill获得抽奖结果
#		"""
#		{
#			"prize_grade":"一等奖",
#			"prize_type":"优惠券",
#			"coupon":"优惠券1",
#			"msg":"恭喜您获得了一张优惠券！<br />快去个人中心查看吧！<br />"
#		}
#		"""
#	When bill访问jobs的webapp
#	Then bill能获得webapp优惠券列表
#		"""
#		[{
#			"coupon_id": "coupon1_id_1",
#			"money": 100.00,
#			"status": "未使用"
#		}]
#		"""
#	And bill在jobs的webapp中拥有5会员积分
#	And bill在jobs的webapp中获得积分日志
#		"""
#		[{
#			"content":"参与抽奖，消耗积分",
#			"integral":-15
#		},{
#			"content":"首次关注",
#			"integral":20
#		}]
#		"""
#	#积分不足时，无法参加抽奖活动
#	When bill参加微信抽奖活动'微信抽奖'
#	Then bill获得错误提示'积分不足'
#
#	#增加积分后，则可正常参加抽奖活动
#	Given jobs登录系统
#	When jobs给"bill"加积分
#			"""
#			{
#				"integral":10,
#				"reason":""
#			}
#			"""
#
#	When bill访问jobs的webapp
#	And bill在jobs的webapp中拥有15会员积分
#
#	When bill参加微信抽奖活动'微信抽奖'
#	Then bill获得抽奖结果
#		"""
#		{
#			"prize_grade":"一等奖",
#			"prize_type":"优惠券",
#			"coupon":"优惠券1"
#		}
#		"""
#	When bill访问jobs的webapp
#	Then bill在jobs的webapp中拥有0会员积分

@mall2 @apps_lottery @apps_lottery_frontend
Scenario:2 非会员通过分享链接参加微信抽奖活动
	Given jobs登录系统
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"不限",
			"win_rate":"100%",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":50,
				"pic":""
			}]
		}]
		"""
	When bill参加微信抽奖活动'微信抽奖'
	When bill把jobs的微信抽奖活动'微信抽奖'的活动链接分享到朋友圈

	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom取消关注jobs的公众号

	When tom点击bill分享的微信抽奖活动'微信抽奖'的活动链接
	When tom参加微信抽奖活动'微信抽奖'
	Then tom获得抽奖结果
		"""
		{
			"prize_grade":"一等奖",
			"prize_type":"积分",
			"integral":50,
			"msg":"恭喜您获得了积分奖励！<br />快去个人中心查看吧！<br />"
		}
		"""

@mall2 @apps_lottery @apps_lottery_frontend
Scenario:3 会员参加微信抽奖活动，抽奖限制为一人一次
	Given jobs登录系统
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖",
			"start_date":"3天前",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":15,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一人一次",
			"win_rate":"50%",
			"is_repeat_win":"否",
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

	When bill参加微信抽奖活动'微信抽奖'

	When 清空浏览器
	When bill参加微信抽奖活动'微信抽奖'
	Then bill获得抽奖次数用完提示'您今天的抽奖机会已经用完,<br />明天再来吧~'

	When tom参加微信抽奖活动'微信抽奖'
	When tom把jobs的微信抽奖活动'微信抽奖'的活动链接分享到朋友圈

	When 清空浏览器
	When bill取消关注jobs的公众号
	When bill点击tom分享的微信抽奖活动'微信抽奖'的活动链接
	When bill参与微信抽奖活动'微信抽奖'
	Then bill获得错误提示'您今天的抽奖机会已经用完,<br />明天再来吧~'

@mall2 @apps_lottery @apps_lottery_frontend
Scenario:4 会员参加微信抽奖活动，抽奖限制为一天两次
	Given jobs登录系统
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖",
			"start_date":"3天前",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一天两次",
			"win_rate":"50%",
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

	#bill昨天参加2次抽奖活动
	When bill参加微信抽奖活动'微信抽奖'于'昨天'

	When 清空浏览器
	When bill参加微信抽奖活动'微信抽奖'于'昨天'

	#bill今天仍有2次抽奖机会
	When bill参加微信抽奖活动'微信抽奖'

	When 清空浏览器
	When bill参加微信抽奖活动'微信抽奖'

	When 清空浏览器
	When bill参加微信抽奖活动'微信抽奖'
	Then bill获得错误提示'您今天的抽奖机会已经用完,<br />明天再来吧~'

#补充：张雪 2015.12.02
@mall2 @apps_lottery @apps_lottery_frontend
Scenario:5 中奖概率率为0,中奖用户为0
	Given jobs登录系统
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"不限",
			"win_rate":"0%",
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

	When bill参加微信抽奖活动'微信抽奖'
	Then bill获得抽奖结果
		"""
		{
			"prize_grade":"谢谢参与",
			"msg":"没有中奖,再接再厉吧~"
		}
		"""

@mall2 @apps_lottery @apps_lottery_frontend
Scenario:6 优惠券数量为0，用户无法获得优惠券奖励
	#中奖概率：100%；抽奖限制：一天两次
	#奖项设置：
		#一等奖，1，优惠券3
		#二等奖，2，优惠券3
		#三等奖，3，优惠券3

	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券3",
			"money": 100.00,
			"count": 1,
			"limit_counts": "不限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon3_id_"
		}]
		"""
	Then jobs能获得优惠券'优惠券3'的码库
		"""
		{
			"coupon3_id_1": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一天两次",
			"win_rate":"100%",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":1,
				"prize_type":"优惠券",
				"coupon":优惠券3,
				"pic":""
			}]
		}]
		"""

	When jobs为会员发放优惠券
		"""
		{
			"name": "优惠券3",
			"count": 1,
			"members": ["bill"]
		}
		"""
	Then jobs能获得优惠券'优惠券3'的码库
		"""
		{
			"coupon3_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		"""

	#优惠券库存为0的情况下，用户参加抽奖将不会获得奖励
	When tom关注jobs的公众号
	When tom参加微信抽奖活动'微信抽奖'
	Then tom获得抽奖结果
		"""
		{
			"prize_grade":"谢谢参与",
			"msg":"没有中奖,再接再厉吧~"
		}
		"""

	When tom参加微信抽奖活动'微信抽奖'
	Then tom获得抽奖结果
		"""
		{
			"prize_grade":"谢谢参与",
			"msg":"没有中奖,再接再厉吧~"
		}
		"""

@mall2 @apps_lottery @apps_lottery_frontend
Scenario:7 优惠券有领取限制，用户无法获得优惠券奖励
	#中奖概率：100%；抽奖限制：一天两次
	#奖项设置：
		#一等奖，1，优惠券3
		#二等奖，2，优惠券3
		#三等奖，3，优惠券3
	#优惠券领取限制为1，当用户在活动期间内已经抽到过此优惠券 ，那么此用户将不会再抽到此优惠券奖励

	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券3",
			"money": 100.00,
			"count": 3,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon3_id_"
		}]
		"""
	Then jobs能获得优惠券'优惠券3'的码库
		"""
		{
			"coupon3_id_1": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一天两次",
			"win_rate":"100%",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":1,
				"prize_type":"优惠券",
				"coupon":优惠券3,
				"pic":""
			}]
		}]
		"""

	When tom关注jobs的公众号
	When tom参加微信抽奖活动'微信抽奖'
	Then tom获得抽奖结果
		"""
		{
			"prize_grade":"一等奖",
			"prize_type":"优惠券",
			"coupon":优惠券3,
			"msg":"恭喜您获得了一张优惠券！<br />快去个人中心查看吧！<br />"
		}
		"""
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		{
			"coupon_id": "coupon3_id_1",
			"money": 100.00,
			"status": "未使用"
		}
		"""

	When tom参加微信抽奖活动'微信抽奖'
	Then tom获得抽奖结果
		"""
		{
			"prize_grade":"谢谢参与",
			"msg":"没有中奖,再接再厉吧~"
		}
		"""
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		{
			"coupon_id": "coupon3_id_1",
			"money": 100.00,
			"status": "未使用"
		}
		"""
