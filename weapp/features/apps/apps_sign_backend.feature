# __author__ : 张雪

Feature: 后台配置数据
"""
	用户通过jobs签到成功，活动签到奖励
	1、【活动名称】：不能为空
	2、【签到设置】：每日和连续签到天数获得奖励
	3、【奖励条件】:每日签到获得？奖励；连续？天获得？奖励
	4、【领取方式】：通过回复关键字和快捷按钮签到
	Scenario 配置后台所有数据，优惠券数量足，没有过期
	Scenario:一条奖励下，不添加优惠券，有积分
	Scenario:一条奖励下，添加优惠券，不添加积分
	Scenario:一条奖励下，添加优惠券，添加积分
	Scenario:三条奖励下，一条优惠券，一条积分，一条优惠券加积分



Scenario: 保存后开启签到活动


"""
Background:
	Given jobs登录系统
	When jobs添加积分
	"""
		"integral":0
	"""
	When jobs添加优惠券
	"""
		[{
			"name": "优惠券1",
			"limit_money"：1,
			"counts":50,
			"start_date": "今天",
			"end_date": "1天后",
		},{
			"name": "优惠券2",
			"limit_money": 1,
			"counts":0,
			"start_date": "今天",
			"end_date": "1天后",
		}]

		"""

@sign
Scenario:配置后台所有数据，优惠券数量足，没有过期
	When jobs添加签到活动"签到活动1"
	"""
	{
		"name": "签到活动1",
		"sign_illustration":"签到即可获得积分，连续签到奖励更大哦",
		"share_pic":"1.jpg",
		"key_words":
		[{
			"rule": "精确",
			"key_word": "78"
		},{
			"rule": "精确",
			"key_word": "12"
		},{
			"rule":"模糊",
			"key_word": "123456"

		}],

		"share_describe": "签到获得奖励",
		"sign_settings":
		[{
			"sign_in": "1",
			"integral": "100",
			"send_coupon": "优惠券1",
			"prize_counts":50
		},{
			"sign_in": "3",
			"integral": "300",
			"send_coupon": "优惠券1",
			"prize_counts":50
		},{
			"sign_in": "5",
			"integral": "500",
			"send_coupon": "优惠券1",
			"prize_counts":50
		}]
	}

	"""
	Then jobs获得签到活动"签到活动1"
	"""
		"name":"签到活动1",
		"sign_illustration":"签到即可获得积分，连续签到奖励更大哦"
		"key_words":
		[{
			"rule": "精确",
			"key_word":"78"
		},{
			"rule": "精确",
			"key_word":"12"
		},{
			"rule":"模糊",
			"key_word":"123456"
		}],
		"share_pic":"1.jpg"
		"sign_settings"：
			[{
				"sign_in": "1",
				"integral": "100",
				"send_coupon": "优惠券1",
				"prize_counts":50
			},{
				"sign_in": "3",
				"integral": "300",
				"send_coupon": "优惠券1",
				"prize_counts":50
			},{
				"sign_in": "5",
				"integral": "500",
				"send_coupon": "优惠券1",
				"prize_counts":50
			]}

	"""
Scenario:一条奖励下，不添加优惠券，有积分
	When jobs添加签到活动"签到活动2"
	"""
	{
		"name": "签到活动2",
		"sign_illustration":"签到即可获得积分，连续签到奖励更大哦",
		"share_pic":"2.jpg",
		"key_words":
		[{
			"rule": "精确",
			"key_word": "78"
		},{
			"rule": "精确",
			"key_word": "12"
		},{
			"rule":"模糊",
			"key_word": "123456"

		}],

		"share_describe": "签到获得奖励",
		"sign_settings":
		[{
			"sign_in": "1",
			"integral": "100"
		},{
			"sign_in": "3",
			"integral": "300"
		},{
			"sign_in": "5",
			"integral": "500"
		}]
	}

	"""
	Then jobs获得签到活动"签到活动2"
	"""
		"name":"签到活动2",
		"sign_illustration":"签到即可获得积分，连续签到奖励更大哦"
		"key_words":
		[{
			"rule": "精确",
			"key_word":"78"
		},{
			"rule": "精确",
			"key_word":"12"
		},{
			"rule":"模糊",
			"key_word":"123456"
		}],
		"share_pic":"2.jpg"
		"sign_settings"：
			[{
				"sign_in": "1",
				"integral": "100"
			},{
				"sign_in": "3",
				"integral": "300"
			},{
				"sign_in": "5",
				"integral": "500"
			]}

	"""

Scenario:一条奖励下，添加优惠券，不添加积分
		When jobs添加签到活动"签到活动3"
	"""
	{
		"name": "签到活动3",
		"sign_illustration":"签到即可获得积分，连续签到奖励更大哦",
		"share_pic":"3.jpg",
		"key_words":
		{
			"rule": "精确",
			"key_word": "78"
		},

		"share_describe": "签到获得奖励",
		"sign_settings":
		[{
			"sign_in": "1",
			"send_coupon": "优惠券1",
			"counts":50
		},{
			"sign_in": "3",
			"send_coupon": "优惠券1",
			"counts":50
		},{
			"sign_in": "5",
			"send_coupon": "优惠券1",
			"counts":50
		}]
	}

	"""
	Then jobs获得签到活动"签到活动3"
	"""
		"name":"签到活动3",
		"sign_illustration":"签到即可获得积分，连续签到奖励更大哦"
		"share_pic":"3.jpg",
		"key_words":
		{
			"rule": "精确",
			"key_word":"78"
		},
		"share_pic":"1.jpg"
		"sign_settings"：
			[{
				"sign_in": "1",
				"send_coupon": "优惠券1"
			},{
				"sign_in": "3",
				"send_coupon": "优惠券1"
			},{
				"sign_in": "5",
				"send_coupon": "优惠券1"
			]}

	"""

Scenario:一条奖励下，添加优惠券，添加积分
"""
	{
		"name": "签到活动4",
		"sign_illustration":"签到即可获得积分，连续签到奖励更大哦",
		"share_pic":"4.jpg",
		"key_words":
		{
			"rule":"模糊",
			"key_word": "123456"
		},

		"share_describe": "签到获得奖励",
		"sign_settings":
		[{
			"sign_in": "1",
			"integral": "100",
			"send_coupon": "优惠券1",
			"prize_counts":50
		},{
			"sign_in": "3",
			"integral": "300",
			"send_coupon": "优惠券1",
			"prize_counts":50
		},{
			"sign_in": "5",
			"integral": "500",
			"send_coupon": "优惠券1",
			"prize_counts":50
		}]
	}

	"""
	Then jobs获得签到活动"签到活动4"
	"""
		"name":"签到活动4",
		"share_pic":"4.jpg",
		"sign_illustration":"签到即可获得积分，连续签到奖励更大哦"
		"key_words":
		{
			"rule":"模糊",
			"key_word":"123456"
		},
		"share_pic":"1.jpg"
		"sign_settings"：
			[{
				"sign_in": "1",
				"integral": "100",
				"send_coupon": "优惠券1",
				"prize_counts":50
			},{
				"sign_in": "3",
				"integral": "300",
				"send_coupon": "优惠券1",
				"prize_counts":50
			},{
				"sign_in": "5",
				"integral": "500",
				"send_coupon": "优惠券1",
				"prize_counts":50
			]}

	"""

Scenario:三条奖励下，一条优惠券，一条积分，一条优惠券加积分



Scenario: 保存后开启签到活动
  When jobs创建签到活动
  	"""
  	{
  		"name": "xxx",
  		"enable": false,
  		...
  	}
  	"""
  Then jobs能获得签到活动"xxx"的状态为"未开启"
  When jobs开启签到活动"xxx"
  Then jobs能获得签到活动"xxx"的状态为"已开启"


Scenario: 保存的同时开启签到活动
  When jobs创建签到活动
  	"""
  	{
  		"name": "xxx",
  		"enable": true,
  		...
  	}
  	"""
  Then jobs能获得签到活动"xxx"的状态为"已开启"

