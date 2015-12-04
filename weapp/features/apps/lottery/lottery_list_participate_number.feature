#_author_:张三香 2015.11.30

Feature:微信抽奖列表-参与次数

Background:
	Given jobs登录系统
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
	When tom关注jobs的公众号
	When marry关注jobs的公众号

@mall2 @apps_lottery @participate_number
Scenario:1 微信抽奖活动列表参与次数的校验
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
				"prize_type":"积分",
				"integral":100,
				"pic":"1.jpg"
			}]
		}]
		"""
	Then jobs获得微信抽奖活动列表
		"""
		[{
			"name":"微信抽奖01",
			"part_num":0
		}]
		"""

	#bill参加2次
	When bill参加微信抽奖活动'微信抽奖01'

	When 清空浏览器
	When bill参加微信抽奖活动'微信抽奖01'

	#tom参加1次
	When 清空浏览器
	When tom参加微信抽奖活动'微信抽奖01'

	When tom把jobs的微信抽奖活动链接分享到朋友圈


	#marry取消关注后参加1次，关注后参加1次
	When marry取消关注jobs的公众号
	When marry点击jobs分享的微信抽奖活动链接
	When marry参加微信抽奖活动'微信抽奖01'

	When 清空浏览器
	When marry关注jobs的公众号
	When marry点击jobs分享的微信抽奖活动链接
	When marry参加微信抽奖活动'微信抽奖01'

	Given jobs登录系统
	Then jobs获得微信抽奖活动列表
		"""
		[{
			"name":"微信抽奖01",
			"part_num":5
		}]
		"""