#_author_:江秋丽 2016.07.25

Feature: 新建砸金蛋活动

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 50,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "优惠券2",
			"money": 50.00,
			"count": 50,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "5天后",
			"coupon_id_prefix": "coupon2_id_"
		}, {
			"name": "优惠券3",
			"money": 30.00,
			"count": 50,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "5天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
		}]
		"""

@mall2 @apps @apps_egg @apps_add_egg
Scenario:1 新建砸金蛋活动,抽奖限制一人一次
	Given jobs登录系统
	When jobs新建砸金蛋活动
		"""
		[{
			"name":"一人一次砸金蛋抽奖",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":1,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"一人一次",
			"win_rate":"50%",
			"is_repeat_win":"是",
			"lottory_color":"#0000FF",
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
	Then jobs获得砸金蛋活动列表
		"""
		[{
			"name":"一人一次砸金蛋抽奖",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"participant_count":0,
			"actions": ["查看结果","链接","关闭","预览"]
		}]
		"""

@mall2 @apps @apps_egg @apps_add_egg
Scenario:2 新建砸金蛋活动,抽奖限制一天一次
	Given jobs登录系统
	When jobs新建砸金蛋活动
		"""
		[{
			"name":"一天一次砸金蛋抽奖",
			"start_date":"明天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":10,
			"send_integral":0,
			"send_integral_rules":"所有用户",
			"lottery_limit":"一天一次",
			"win_rate":"60%",
			"is_repeat_win":"否",
			"lottory_color":"#0000FF",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":1000
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"积分",
				"integral":500
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"积分",
				"integral":100
			}]
		}]
		"""
	Then jobs获得砸金蛋活动列表
		"""
		[{
			"name":"一天一次砸金蛋抽奖",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"participant_count":0,
			"actions": ["查看结果","链接","删除","预览"]
		}]
		"""

@mall2 @apps @apps_egg @apps_add_egg
Scenario:3 新建砸金蛋活动,抽奖限制不限
	Given jobs登录系统
	When jobs新建砸金蛋活动
		"""
		[{
			"name":"不限制砸金蛋抽奖",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":100,
			"send_integral":1,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"不限",
			"win_rate":"50%",
			"is_repeat_win":"否",
			"lottory_color":"#0000FF",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券1"
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券2"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"优惠券",
				"coupon":"优惠券3"
			}]
		}]
		"""
	Then jobs获得砸金蛋活动列表
		"""
		[{
			"name":"不限制砸金蛋抽奖",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"participant_count":0,
			"actions": ["查看结果","链接","关闭","预览"]
		}]
		"""