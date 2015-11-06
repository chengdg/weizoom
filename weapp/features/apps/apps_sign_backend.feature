# __author__ : 张雪

Feature: 后台配置数据
"""
	用户通过jobs签到成功,活动签到奖励
	1.【活动名称】:不能为空
	2.【签到设置】:每日和连续签到天数获得奖励
	3.【奖励条件】:每日签到获得？奖励；连续？天获得？奖励
	4.【领取方式】:通过回复关键字和快捷按钮签到
	5.配置后台所有数据,优惠券数量足,没有过期
	6.一条奖励下,不添加优惠券,有积分
	7.一条奖励下,添加优惠券,不添加积分
	8.一条奖励下,添加优惠券,添加积分
	9.三条奖励下,一条优惠券,一条积分,一条优惠券加积分
	10.优惠券数量为0,无法添加优惠券
	11.保存后开启签到活动
"""


Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
			[{
				"name": "优惠券1",
				"money":1.00,
				"limit_counts":50,
				"start_date": "今天",
				"end_date": "1天后",
				"coupon_id_prefix": "coupon1_id_"
			},{
				"name": "优惠券2",
				"money":1.00,
				"counts":0,
				"start_date": "今天",
				"end_date": "1天后",
				"coupon_id_prefix": "coupon2_id_"
			}]

		"""

@apps_sign @apps_sign_backend
Scenario:配置后台所有数据,优惠券数量足,没有过期
	When jobs添加签到活动"签到活动1",并且保存
		"""
		{
			"status":"off",
			"name": "签到活动1",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",

			"share_pic":"1.jpg",
			"share_describe": "签到获得奖励",
			"reply_content":"签到",
			"reply_keyword":
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
		{
			"status":"off",
			"name": "签到活动1",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",

			"share_pic":"1.jpg",
			"share_describe": "签到获得奖励",
			"reply_content":"签到",
			"reply_keyword":
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
@apps_sign @apps_sign_backend
Scenario:一条奖励下,不添加优惠券,有积分
	When jobs添加签到活动"签到活动2",并且保存
		"""
		{
			"status":"off",
			"name": "签到活动2",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",

			"share_pic":"2.jpg",
			"share_describe": "签到获得奖励",
			"reply_content":"签到",
			"reply_keyword":
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
			"sign_settings":
				[{
					"sign_in": "1",
					"integral": "100"
				}]
		}

		"""
	Then jobs获得签到活动"签到活动2"
		"""
		{
			"status":"off",
			"name": "签到活动2",
			"sign_describe":"签到即可获得积分,连续签到奖励更大哦",

			"share_pic":"2.jpg",
			"share_describe": "签到获得奖励",
			"reply_content":"签到",
			"reply_keyword":
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
			"sign_settings":
				[{
					"sign_in": "1",
					"integral": "100"
				}]
		}
		"""
@apps_sign @apps_sign_backend
Scenario:一条奖励下,添加优惠券,不添加积分
	When jobs添加签到活动"签到活动3",并且保存
		"""
        {
            "status":"off",
            "name": "签到活动3",
            "sign_describe":"签到即可获得积分,连续签到奖励更大哦",

            "share_pic":"3.jpg",
            "share_describe": "签到获得奖励",
            "reply_content":"签到",
            "reply_keyword":
                [{
                    "rule": "精确",
                    "key_word": "78"
                }],

            "sign_settings":
                [{
                    "sign_in": "1",
                    "send_coupon": "优惠券1",
                    "prize_counts":50
                }]
        }
		"""
	Then jobs获得签到活动"签到活动3"
		"""
        {
            "status":"off",
            "name": "签到活动3",
            "sign_describe":"签到即可获得积分,连续签到奖励更大哦",

            "share_pic":"3.jpg",
            "share_describe": "签到获得奖励",
            "reply_content":"签到",
            "reply_keyword":
                [{
                    "rule": "精确",
                    "key_word": "78"
                }],

            "sign_settings":
                [{
                    "sign_in": "1",
                    "send_coupon": "优惠券1",
                    "prize_counts":50
                }]
        }

		"""
@apps_sign @apps_sign_backend
Scenario:一条奖励下,添加优惠券,添加积分
	When jobs添加签到活动"签到活动4",并且保存
		"""
        {
            "status":"off",
            "name": "签到活动4",
            "sign_describe":"签到即可获得积分,连续签到奖励更大哦",

            "share_pic":"4.jpg",
            "share_describe": "签到获得奖励",
            "reply_content":"签到",
            "reply_keyword":
                [{
                    "rule":"模糊",
                    "key_word": "123456"
                }],

            "sign_settings":
                [{
                    "sign_in": "1",
                    "integral": "100",
                    "send_coupon": "优惠券1",
                    "prize_counts":50
                }]
        }

		"""
	Then jobs获得签到活动"签到活动4"
		"""
        {
            "status":"off",
            "name": "签到活动4",
            "sign_describe":"签到即可获得积分,连续签到奖励更大哦",

            "share_pic":"4.jpg",
            "share_describe": "签到获得奖励",
            "reply_content":"签到",
            "reply_keyword":
                [{
                    "rule":"模糊",
                    "key_word": "123456"
                }],

            "sign_settings":
                [{
                    "sign_in": "1",
                    "integral": "100",
                    "send_coupon": "优惠券1",
                    "prize_counts":50
                }]
        }
		"""
@apps_sign @apps_sign_backend
Scenario:三条奖励下,一条优惠券,一条积分,一条优惠券加积分
	When jobs添加签到活动"签到活动5",并且保存
		"""
        {
            "status":"off",
            "name": "签到活动5",
            "sign_describe":"签到即可获得积分,连续签到奖励更大哦",

            "share_pic":"5.jpg",
            "share_describe": "签到获得奖励",
            "reply_content":"签到",
            "reply_keyword":
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

            "sign_settings":
                [{
                    "sign_in": "1",
                    "integral": "100",
                    "send_coupon": "优惠券1",
                    "prize_counts":50
                },{
                    "sign_in": "3",
                    "integral": "300"
                },{
                    "sign_in": "5",
                    "integral": "500",
                    "send_coupon": "优惠券1",
                    "prize_counts":50
                }]
        }
		"""
	Then jobs获得签到活动"签到活动5"
		"""
        {
            "status":"off",
            "name": "签到活动5",
            "sign_describe":"签到即可获得积分,连续签到奖励更大哦",

            "share_pic":"5.jpg",
            "share_describe": "签到获得奖励",
            "reply_content":"签到",
            "reply_keyword":
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

            "sign_settings":
                [{
                    "sign_in": "1",
                    "integral": "100",
                    "send_coupon": "优惠券1",
                    "prize_counts":50
                },{
                    "sign_in": "3",
                    "integral": "300"
                },{
                    "sign_in": "5",
                    "integral": "500",
                    "send_coupon": "优惠券1",
                    "prize_counts":50
                }]
        }
		"""


@apps_sign @apps_sign_backend @kuku
Scenario: 保存活动后，立刻开启签到活动
	When jobs添加签到活动"签到活动6",并且保存
	"""
	{
		"status":"off",
		"name": "签到活动6",
		"sign_describe":"签到即可获得积分,连续签到奖励更大哦",

		"share_pic":"6.jpg",
		"share_describe": "签到获得奖励",
		"reply_content":"签到",
		"reply_keyword":
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
	And jobs开启签到活动"签到活动6"
	"""
	{
		"name": "签到活动6",
		"enable": true
	}
	"""
	Then jobs能获得签到活动"签到活动6"的状态为"已开启"



@apps_sign @apps_sign_backend
Scenario: 保存后开启签到活动
  When jobs开启签到活动"签到活动7"
	"""
	{
		"name": "签到活动7",
		"enable": false
	}
	"""
  Then jobs能获得签到活动"签到活动7"的状态为"未开启"
  When jobs开启签到活动"签到活动7"
  Then jobs能获得签到活动"签到活动7"的状态为"已开启"

