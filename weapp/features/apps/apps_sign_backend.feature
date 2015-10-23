# __author__ : 张雪

Feature: 后台配置数据
"""
	用户通过jobs签到成功，活动签到奖励
	1、【活动名称】：不能为空
	2、【签到设置】：每日和连续签到天数获得奖励
	3、【奖励条件】:每日签到获得？奖励；连续？天获得？奖励
	4、【领取方式】：通过回复关键字和快捷按钮签到
	Scenario bill浏览签到页面
	Scenario bill通过快捷按钮签到
	Scenario bill通过回复关键字签到
	Scenario bill一天内两次签到
	Scenario bill两天内连续签到
	Scenario bill间隔一天后签到
	Scenario bill在签到结束后进行签到
	Scenario 优惠券在签到结束前过期
	Scenario -bill进行签到
	Scenario 签到和其他活动同时进行，签到获得优先级获取图文链接

"""
Background:
	Given jobs登录系统
	When jobs添加优惠券
	"""
		[{
			"name": "优惠券1",
			"money": 1,
			"counts":50,
			"start_date": "今天",
			"end_date": "1天后",
			},{
			"name": "优惠券2",
			"money": 1,
			"counts":50,
			"start_date": "一天前",
			"end_date": "今天",
			"name": "优惠券3",
			"money": 1,
			"counts":0,
			"start_date": "今天",
			"end_date": "1天后",
		}]

		"""
@sign
Scenario:配置后台所有数据，优惠券数量足，没有过期
	When jobs添加签到活动"签到活动1"
	"""
		[{
			"name": "签到活动1",
			"sign_illustration":"签到即可获得积分，连续签到奖励更大哦",
			"share_pic":"C:\Users\Administrator\Desktop\截图微众"
			"key_words": {
				"rule": "精确",
				"key_word": "78"
				"rule": "精确",
				"key_word": "12"
				"rule":"模糊"
				"key_word": "123456"

			},
			"share_describe": "签到获得奖励"
			"sign_settings":{
				items:[{
					"sign_in": "1",
					"integral": "100",
					"send_coupon": "优惠券1"
				},{
					"sign_in": "3",
					"integral": "300",
					"send_coupon": "优惠券1"
				},{
					"sign_in": "5",
					"integral": "500",
					"send_coupon": "优惠券1"
					]}

	"""
	Then jobs获得签到活动"签到活动1"
	"""
		"name":"签到活动1",
		"sign_illustration":"签到即可获得积分，连续签到奖励更大哦"
		"key_word":12
		"key_word":123456
		"key_word":78
		"share_pic":"C:\Users\Administrator\Desktop\截图微众"
		"sign_settings"
			items:[{
					"sign_in": "1",
					"integral": "100",
					"send_coupon": "优惠券1"
				},{
					"sign_in": "3",
					"integral": "300",
					"send_coupon": "优惠券1"
				},{
					"sign_in": "5",
					"integral": "500",
					"send_coupon": "优惠券1"
					]}

	"""

Scenario:配置后台所有数据，优惠券数量足，过期
	When jobs添加签到活动"签到活动2"
	"""
	[{
			"name": "签到活动1",
			"sign_illustration":"签到即可获得积分，连续签到奖励更大哦",
			"share_pic":"C:\Users\Administrator\Desktop\截图微众"
			"key_words": {
				"rule": "精确",
				"key_word": "78"
				"rule": "精确",
				"key_word": "12"
				"rule":"模糊"
				"key_word": "123456"

			},
			"share_describe": "签到获得奖励"
			"sign_settings":{
				items:[{
					"sign_in": "1",
					"integral": "100",
					"send_coupon": "优惠券2"
				}]
			}
		}]
	"""
	Then jobs获得签到活动"签到活动2"
	"""
		"name":"签到活动2",
		"sign_illustration":"签到即可获得积分，连续签到奖励更大哦"
		"key_word":12
		"key_word":123456
		"key_word":78
		"share_pic":"C:\Users\Administrator\Desktop\截图微众"
		"sign_settings"
			items:[{
					"sign_in": "1",
					"integral": "100",
					"send_coupon": "优惠券2"
				 ]}

	"""

Scenario:配置后台所有数据，优惠券数量为0，没有过期
	When jobs添加签到活动"签到活动3"
	"""
	[{
			"name": "签到活动3",
			"sign_illustration":"签到即可获得积分，连续签到奖励更大哦",
			"share_pic":"C:\Users\Administrator\Desktop\截图微众"
			"key_words": {
				"rule": "精确",
				"key_word": "78"
				"rule": "精确",
				"key_word": "12"
				"rule":"模糊"
				"key_word": "123456"

			},
			"share_describe": "签到获得奖励"
			"sign_settings":{
				items:[{
					"sign_in": "1",
					"integral": "100",
					"send_coupon": "优惠券3"
				}]
			}
		}]
	"""
	Then jobs获得签到活动"签到活动3"
	"""
		"name":"签到活动3",
		"sign_illustration":"签到即可获得积分，连续签到奖励更大哦"
		"key_word":12
		"key_word":123456
		"key_word":78
		"share_pic":"C:\Users\Administrator\Desktop\截图微众"
		"sign_settings"
			items:[{
					"sign_in": "1",
					"integral": "100",
					"send_coupon": "优惠券3"
				 ]}

	"""
	And jobs保存签到活动"签到活动1"
	And jobs开启签到活动"签到活动1"

	
