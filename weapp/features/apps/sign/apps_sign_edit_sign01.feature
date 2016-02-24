#_author_:许韦 2015.11.30

Feature:测试修改签到活动最高连续签到天数
	"""
		商户登录云商通系统，在保持签到活动开启的情况下，修改签到活动配置的最高连续签到天数并保存：
		1.如果当前活动中会员累计签到的天数大于修改后的最高连续签到天数，继续签到则重新开始
		2.如果当前活动中会员累计签到的天数小于修改后的最高连续签到天数，继续签到则获的新规则下的奖励
	"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 1.00,
			"limit_counts": "无限",
			"start_date": "1天前",
			"end_date": "3天后",
			"coupon_id_prefix": "coupon1_id_"
		},{
			"name": "优惠券2",
			"money": 2.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""

@mall2 @apps @apps_sign @edited_sign
Scenario:1 修改最高连续签到天数，当会员累计签到达到该天数，继续签到从头开始
	When jobs添加签到活动"签到活动1",并且保存
		"""
		{
			"status":"off",
			"name":"签到活动1",
			"sign_describe":"1签到赚积分！连续签到奖励更丰富哦！",
			"share_pic":"1.jpg",
			"share_describe":"签到送好礼！",
			"reply_content":"每日签到获得2积分和优惠券1一张，连续签到4天获得10积分和优惠券2一张",
			"reply_keyword":
				[{
					"rule":"精确",
					"key_word":"签到1"
				}],
			"sign_settings":
				[{
					"sign_in":"0",
					"integral":"2",
					"send_coupon":"优惠券1"
				},{
					"sign_in":"4",
					"integral":"10",
					"send_coupon":"优惠券2"
				}]
		}
		"""
	When jobs更新签到活动的状态
		"""
		{
			"name":"签到活动1",
			"status":"on"
		}
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'签到1'
	Then bill获得系统回复的消息
	"""
	签到成功！<br />已连续签到1天。<br />本次签到获得以下奖励:<br />2积分<br />优惠券1<br />签到说明：1签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分和优惠券1一张，连续签到4天获得10积分和优惠券2一张<br />
	"""
	When 修改bill的签到时间为前一天
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'签到1'
	Then bill获得系统回复的消息
	"""
	签到成功！<br />已连续签到2天。<br />本次签到获得以下奖励:<br />2积分<br />优惠券1<br />签到说明：1签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分和优惠券1一张，连续签到4天获得10积分和优惠券2一张<br />
	"""
	When 修改bill的签到时间为前一天
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'签到1'
	Then bill获得系统回复的消息
	"""
	签到成功！<br />已连续签到3天。<br />本次签到获得以下奖励:<br />2积分<br />优惠券1<br />签到说明：1签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分和优惠券1一张，连续签到4天获得10积分和优惠券2一张<br />
	"""
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有6会员积分
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id":"coupon1_id_1",
			"money":1.00,
			"status":"未使用"
		},{
			"coupon_id":"coupon1_id_2",
			"money":1.00,
			"status":"未使用"
		},{
			"coupon_id":"coupon1_id_3",
			"money":1.00,
			"status":"未使用"
		}]
		"""

	#在开启状态下修改签到活动
	Given jobs登录系统
	When jobs编辑签到活动,并且保存
		"""
		{
			"name":"签到活动1",
			"sign_describe":"1签到赚积分！连续签到奖励更丰富哦！",
			"share_pic":"1.jpg",
			"share_describe":"签到送好礼！",
			"reply_content":"每日签到获得2积分和优惠券1一张，连续签到2天获得5积分和优惠券2一张",
			"reply_keyword":
				[{
					"rule":"精确",
					"key_word":"签到1"
				}],
			"sign_settings":
				[{
					"sign_in":"0",
					"integral":"2",
					"send_coupon":"优惠券1"
				},{
					"sign_in":"2",
					"integral":"5",
					"send_coupon":"优惠券2"
				}]
		}
		"""
	When 修改bill的签到时间为前一天
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'签到1'
	Then bill获得系统回复的消息
	"""
	签到成功！<br />已连续签到1天。<br />本次签到获得以下奖励:<br />2积分<br />优惠券1<br />签到说明：1签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分和优惠券1一张，连续签到2天获得5积分和优惠券2一张<br />
	"""
	When 修改bill的签到时间为前一天
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'签到1'
	Then bill获得系统回复的消息
	"""
	签到成功！<br />已连续签到2天。<br />本次签到获得以下奖励:<br />5积分<br />优惠券2<br />签到说明：1签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分和优惠券1一张，连续签到2天获得5积分和优惠券2一张<br />
	"""
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有13会员积分
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id":"coupon1_id_1",
			"money":1.00,
			"status":"未使用"
		},{
			"coupon_id":"coupon1_id_2",
			"money":1.00,
			"status":"未使用"
		},{
			"coupon_id":"coupon1_id_3",
			"money":1.00,
			"status":"未使用"
		},{
			"coupon_id":"coupon1_id_4",
			"money":1.00,
			"status":"未使用"
		},{
			"coupon_id":"coupon2_id_1",
			"money":2.00,
			"status":"未使用"
		}]
		"""

@mall2 @apps @apps_sign @edited_sign
Scenario:2 修改最高连续签到天数，当会员累计签到未达到该天数，继续签到获得新规则下的奖励
	When jobs添加签到活动"签到活动2",并且保存
		"""
		{
			"status":"off",
			"name":"签到活动2",
			"sign_describe":"2签到赚积分！连续签到奖励更丰富哦！",
			"share_pic":"2.jpg",
			"share_describe":"签到送好礼！",
			"reply_content":"每日签到获得2积分和优惠券1一张，连续签到2天获得5积分和优惠券1一张",
			"reply_keyword":
				[{
					"rule":"精确",
					"key_word":"签到2"
				}],
			"sign_settings":
				[{
					"sign_in":"0",
					"integral":"2",
					"send_coupon":"优惠券1"
				},
				{
					"sign_in":"2",
					"integral":"5",
					"send_coupon":"优惠券1"
				}]

		}
		"""
	When jobs更新签到活动的状态
		"""
		{
			"name":"签到活动2",
			"status":"on"
		}
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'签到2'
	Then bill获得系统回复的消息
	"""
	签到成功！<br />已连续签到1天。<br />本次签到获得以下奖励:<br />2积分<br />优惠券1<br />签到说明：2签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分和优惠券1一张，连续签到2天获得5积分和优惠券1一张<br />
	"""
	When 修改bill的签到时间为前一天
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'签到2'
	Then bill获得系统回复的消息
	"""
	签到成功！<br />已连续签到2天。<br />本次签到获得以下奖励:<br />5积分<br />优惠券1<br />签到说明：2签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分和优惠券1一张，连续签到2天获得5积分和优惠券1一张<br />
	"""
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有7会员积分
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id":"coupon1_id_1",
			"money":1.00,
			"status":"未使用"
		},{
			"coupon_id":"coupon1_id_2",
			"money":1.00,
			"status":"未使用"
		}]
		"""

	#在开启状态下修改签到活动
	Given jobs登录系统
	When jobs编辑签到活动,并且保存
		"""
		{
			"name":"签到活动2",
			"sign_describe":"2签到赚积分！连续签到奖励更丰富哦！",
			"share_pic":"2.jpg",
			"share_describe":"签到送好礼！",
			"reply_content":"每日签到获得2积分和优惠券1一张，连续签到3天获得10积分和优惠券2一张",
			"reply_keyword":
				[{
					"rule":"精确",
					"key_word":"签到2"
				}],
			"sign_settings":
				[{
					"sign_in":"0",
					"integral":"2",
					"send_coupon":"优惠券1"
				},{
					"sign_in":"3",
					"integral":"10",
					"send_coupon":"优惠券2"
				}]
		}
		"""
	When 修改bill的签到时间为前一天
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'签到2'
	Then bill获得系统回复的消息
	"""
	签到成功！<br />已连续签到3天。<br />本次签到获得以下奖励:<br />10积分<br />优惠券2<br />签到说明：2签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分和优惠券1一张，连续签到3天获得10积分和优惠券2一张<br />
	"""
	When 修改bill的签到时间为前一天
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'签到2'
	Then bill获得系统回复的消息
	"""
	签到成功！<br />已连续签到1天。<br />本次签到获得以下奖励:<br />2积分<br />优惠券1<br />签到说明：2签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分和优惠券1一张，连续签到3天获得10积分和优惠券2一张<br />
	"""
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有19会员积分
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id":"coupon1_id_1",
			"money":1.00,
			"status":"未使用"
		},{
			"coupon_id":"coupon1_id_2",
			"money":1.00,
			"status":"未使用"
		},{
			"coupon_id":"coupon1_id_3",
			"money":1.00,
			"status":"未使用"
		},{
			"coupon_id":"coupon2_id_1",
			"money":2.00,
			"status":"未使用"
		}]
		"""