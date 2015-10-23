# __author__ : "许韦"

Feature: Sign
	用户进行签到

Background:
	Given jobs登录系统
	When jobs添加"签到活动1"
	"""
		{
			"name": "优惠券1",
			"money": 1.00,
			"limit_counts": "无限",
			"start_date": "2天前",
			"end_date": "1天前",
			"coupon_id": "优惠券1"
		}
	"""
	When jobs添加"签到活动1"
		"""
		[{
			"sign_id":"签到活动1",
			"sign_illustration":"签到赚积分！",
			"share_pic": [{
				"url": "/weappimg.b0.upaiyun.com/upload/119_20150707/1436273979099_278.jpg"
			}],

			"share_describe":"签到送好礼！",
			"key_word": [{
					"keyword": "12",
					"type": "equal"
				},{
					"keyword": "123",
					"type": "like"
				}],
			"key_word_reply": {
					"reply_content":"
					每日签到活动2积分和优惠券1一张
					连续签到3天获得5积分和优惠券1一张
					连续签到5天获得7积分和优惠券1一张",
					"reply_type":"text"
				},
			"prize":[{
					"serial_count":"1",
					"integral":"2",
					"coupon_id":[优惠券1]
				},{
					"serial_count":"2",
					"integral":"5",
					"coupon_id":[优惠券1]
				},{
					"serial_count":"3",
					"integral":"7",
					"coupon_id":[优惠券1]
				}]
		}]
		"""
	Then jobs能获取签到活动配置内容
		"""
		{
			"name": "签到活动1",
			"status": "关闭"
		}
		"""
	And jobs开启"签到活动1"
		"""
		{
			"name":"签到活动1",
			"status":"开启"
		}
		"""



Scenario: 1 用户浏览"签到活动1"
	Given jobs登录系统
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill的会员积分0
	When bill进入签到页面
	Then bill获取"签到活动1"内容
	"""
	[{
		"user_name":"bill",
		"integral_account":"0"
		"integral_num":"2",
		"coupon_id":"优惠券1"
		"sign_item":[{
			"title1":"签到说明",
			"sign_illustration":"签到赚积分！"
		},{
			"title2":"活动规则",
			"rule":"
			1.每日签到，获得2积分奖励"优惠券1"一张。
			2.连续签到至3天，获得5积分奖励"优惠券1"一张。
			3.连续签到至5天，获得7积分奖励"优惠券1"一张。
			"
		}]
	}]
	"""



Scenario: 2 用户回复精确关键字签到
	Given jobs登录系统
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill的会员积分0
	When bill回复关键字"12"
	Then bill获得系统回复的消息
	"""
	[{	
		"prize_item":{
			"serial_count":"1",
			"integral":"2",
			"coupon_id":[优惠券1],
			"name":"点击查看详情",
			"url_id_1":url1
	},{
		"sign_item":{
			"title1":"签到说明:",
			"sign_illustration":"签到赚积分！",
			"rule":"
			1.每日签到，获得2积分奖励"优惠券1"一张。
			2.连续签到至3天，获得5积分奖励"优惠券1"一张。
			3.连续签到至5天，获得7积分奖励"优惠券1"一张。",
			"name":"点击查看详情",
			"url_id_2":"url2"
	}]
	"""
	When bill访问系统回复的"url1"
	Then bill获得"优惠券1"
	"""
	{
		"name": "优惠券1",
		"money": 1.00,
		"limit_counts": "无限",
		"start_date": "2天前",
		"end_date": "1天前",
		"coupon_id": "优惠券1"
	}
	"""
	When bill访问系统回复的"url2"
	Then bill获得积分2
	"""
	{
		"integral_account":"2"
		"integral_num":"2",
		"coupon_id":"优惠券1"
	}
	"""



Scenario: 3 用户回复完全匹配模糊关键字签到
	Given jobs登录系统
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill的会员积分0
	When bill回复关键字"123"
	Then bill获得系统回复的消息
	"""
	[{	
		"prize_item":{
			"serial_count":"1",
			"integral":"2",
			"coupon_id":[优惠券1],
			"name":"点击查看详情",
			"url_id_1":url1
	},{
		"sign_item":{
			"title1":"签到说明:",
			"sign_illustration":"签到赚积分！",
			"rule":"
			1.每日签到，获得2积分奖励"优惠券1"一张。
			2.连续签到至3天，获得5积分奖励"优惠券1"一张。
			3.连续签到至5天，获得7积分奖励"优惠券1"一张。",
			"name":"点击查看详情",
			"url_id_2":"url2"
	}]
	"""



Scenario: 4 用户回复不完全匹配模糊关键字签到
	Given jobs登录系统
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill的会员积分0
	When bill回复关键字"1234"
	Then bill获得系统回复的消息
	"""
	[{	
		"prize_item":{
			"serial_count":"1",
			"integral":"2",
			"coupon_id":[优惠券1],
			"name":"点击查看详情",
			"url_id_1":url1
	},{
		"sign_item":{
			"title1":"签到说明:",
			"sign_illustration":"签到赚积分！",
			"rule":"
			1.每日签到，获得2积分奖励"优惠券1"一张。
			2.连续签到至3天，获得5积分奖励"优惠券1"一张。
			3.连续签到至5天，获得7积分奖励"优惠券1"一张。",
			"name":"点击查看详情",
			"url_id_2":"url2"
	}]
	"""



Scenario: 5 用户回复不匹配关键字签到
	Given jobs登录系统
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill的会员积分0
	When bill回复关键字"1"
	Then bill没有获得系统回复的消息

	

Scenario: 6 签到活动结束后用户回复精确关键字签到
	Given jobs登录系统
	And jobs更改"签到活动1"状态
	"""
	{
		"name":"签到活动1",
		"status":"关闭"
	}
	"""
	When bill关注jobs的公众号
	When bill访问jobs的weapp
	When bill的会员积分0
	When bill回复关键字"12"
	Then bill获得系统自动回复的消息"签到活动还未开始。"

	

Scenario: 7 签到活动结束后用户回复完全匹配模糊关键字签到
	Given jobs登录系统
	And jobs更改"签到活动1"状态
	"""
	{
		"name":"签到活动1",
		"status":"关闭"
	}
	"""
	When bill关注jobs的公众号
	When bill访问jobs的weapp
	When bill的会员积分0
	When bill回复关键字"123"
	Then bill获得系统自动回复的消息"签到活动还未开始。"



Scenario: 8 签到活动结束后用户回复不完全匹配模糊关键字签到
	Given jobs登录系统
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill的会员积分0
	When bill回复关键字"1234"
	Then bill获得系统自动回复的消息"签到活动还未开始。"



Scenario: 9 签到活动结束后用户回复不匹配关键字签到
	Given jobs登录系统
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill的会员积分0
	When bill回复关键字"1"
	Then bill没有获得系统回复的消息



Scenario: 10 用户一天内连续两次签到
	Given jobs登录系统
	When bill关注jobs的公众号
	When bill访问jobs的weapp
	When bill的会员积分0
	When bill回复有效关键字签到
	Then bill获得系统回复的消息
	"""
	[{	
		"prize_item":{
			"serial_count":"1",
			"integral":"2",
			"coupon_id":[优惠券1],
			"name":"点击查看详情",
			"url_id_1":url1
	},{
		"sign_item":{
			"title1":"签到说明:",
			"sign_illustration":"签到赚积分！",
			"rule":"
			1.每日签到，获得2积分奖励"优惠券1"一张。
			2.连续签到至3天，获得5积分奖励"优惠券1"一张。
			3.连续签到至5天，获得7积分奖励"优惠券1"一张。",
			"name":"点击查看详情",
			"url_id_2":"url2"
	}]
	"""
	When bill访问系统回复的"url1"
	Then bill获得"优惠券1"
	"""
	{
		"name": "优惠券1",
		"money": 1.00,
		"limit_counts": "无限",
		"start_date": "2天前",
		"end_date": "1天前",
		"coupon_id": "优惠券1"
	}
	"""
	When bill访问系统回复的"url2"
	Then bill获得积分2
	"""
	{
		"integral_account":"2"
		"integral_num":"2",
		"coupon_id":"优惠券1"
	}
	"""
	When bill退出jobs的weapp
	When bill再次访问jobs的weapp
	When bill回复有效关键字签到
	Then bill获得系统回复的消息
	"""
	{
		"reply":"
		亲，今天您已经签到过了哦，
		明天再来吧！",
		"url_id_2":"url2"
	}