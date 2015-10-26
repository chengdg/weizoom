# __author__ : "许韦"

Feature: Sign
	用户进行签到

Background:
	Given jobs登录系统
	Given jobs已添加优惠券规则
	"""
		{
			"name": "优惠券1",
			"money": 1.00,
			"limit_counts": "无限",
			"start_date": "2天前",
			"end_date": "1天前",
			"coupon_id_prefix": "coupon1_id_"
		}
	"""



Scenario: 1 用户浏览"签到活动1"
	Given jobs添加"签到活动1"
	"""
	{
		"name":"签到活动1",
		"sign_desc":"签到赚积分！连续签到奖励更丰富哦！",
		"share":
			{
				"img": 1.img,
				"desc":"签到送好礼！"
			},
		"key_word": 
				[{
					"keyword": "12",
					"type": "equal"
				},
				{
					"keyword": "123",
					"type": "like"
				}],
		"reply": 
			{
				"content":
				"每日签到活动2积分和优惠券1一张
				连续签到3天获得5积分和优惠券1一张
				连续签到5天获得7积分和优惠券1一张",
				"reply_type":"text"
			},
		"prize_settings":
			[{
				"serial_count":"1",
				"integral":"2",
				"coupon_name":"优惠券1"
			},{
				"serial_count":"3",
				"integral":"5",
				"coupon_name":"优惠券1"
			},{
				"serial_count":"5",
				"integral":"7",
				"coupon_name":"优惠券1"
			}]
	}
	"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill的会员积分0
	When bill进入jobs的签到页面
	Then bill获取"签到活动1"内容
	"""
	[{
		"user_name":"bill",
		"integral_account":"0",
		"integral":"2",
		"coupon_name":"优惠券1",
		"sign_item":
		{
			"sign_desc":"签到赚积分！连续签到奖励更丰富哦！",
			"sign_rule":
				"1.每日签到，获得2积分奖励"优惠券1"一张。
				2.连续签到至3天，获得5积分奖励"优惠券1"一张。
				3.连续签到至5天，获得7积分奖励"优惠券1"一张。"
		}
	}]
	"""



Scenario: 2 用户回复精确关键字、完全匹配模糊关键字、不完全匹配模糊关键字签到
	Given jobs添加"签到活动1"
	"""
	{
		"name":"签到活动1",
		"sign_desc":"签到赚积分！连续签到奖励更丰富哦！",
		"share":
			{
				"img": 1.img,
				"desc":"签到送好礼！"
			},
		"key_word": 
			[{
				"keyword": "12",
				"type": "equal"
			},{
				"keyword": "123",
					"type": "like"
			}],
		"reply": 
			{
				"content":
				"每日签到活动2积分和优惠券1一张
				连续签到3天获得5积分和优惠券1一张
				连续签到5天获得7积分和优惠券1一张",
				"reply_type":"text"
			},
		"prize_settings":
			[{
				"serial_count":"1",
				"integral":"2",
				"coupon_name":"优惠券1"
			},{
				"serial_count":"3",
				"integral":"5",
				"coupon_name":"优惠券1"
			},{
				"serial_count":"5",
				"integral":"7",
				"coupon_name":"优惠券1"
			}]
	}
	"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill的会员积分0
	When bill回复关键字

	Examples: 
		| keyword | type | 
		| 12      | equal|
		| 123     | like | 
		| 1234    | like |

	Then bill获得系统回复的消息
	"""
	{	
		"prize_item":
			{
				"serial_count":"1",
				"integral":"2",
				"coupon_name":["优惠券1"]
			},
		"url_id_1":url1,
		"reply": 
			{
				"content":
				"每日签到活动2积分和优惠券1一张
				连续签到3天获得5积分和优惠券1一张
				连续签到5天获得7积分和优惠券1一张",
				"reply_type":"text"
			}
		"url_id_2":url2
	}
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
		"coupon_id_prefix": "coupon1_id_"
	}
	"""
	When bill访问系统回复的"url2"
	Then bill获取"签到活动1"内容
	"""
	{
		"user_name":"bill",
		"integral_account":"2",
		"serial_count"："1",
		"integral":"5",
		"coupon_name":"优惠券1"
	}
	"""



Scenario: 3 用户回复完全不匹配关键字签到
	Given jobs添加"签到活动1"
	"""
	{
		"name":"签到活动1",
		"sign_desc":"签到赚积分！连续签到奖励更丰富哦！",
		"share":
			{
				"img": 1.img,
				"desc":"签到送好礼！"
			},
		"key_word": 
			[{
				"keyword": "12",
				"type": "equal"
			},{
				"keyword": "123",
					"type": "like"
			}],
		"reply": 
			{
				"content":
				"每日签到活动2积分和优惠券1一张
				连续签到3天获得5积分和优惠券1一张
				连续签到5天获得7积分和优惠券1一张",
				"reply_type":"text"
			},
		"prize_settings":
			[{
				"serial_count":"1",
				"integral":"2",
				"coupon_name":"优惠券1"
			},{
				"serial_count":"3",
				"integral":"5",
				"coupon_name":"优惠券1"
			},{
				"serial_count":"5",
				"integral":"7",
				"coupon_name":"优惠券1"
			}]
	}
	"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill的会员积分0
	When bill回复关键字"1"
	Then bill没有获得系统回复的消息	



Scenario: 4 签到活动结束后用户回复精确关键字、完全匹配模糊关键字、不完全匹配模糊关键字签到
	Given jobs添加"签到活动1"
	"""
	{
		"name":"签到活动1",
		"sign_desc":"签到赚积分！连续签到奖励更丰富哦！",
		"share":
			{
				"img": 1.img,
				"desc":"签到送好礼！"
			},
		"key_word": 
			[{
				"keyword": "12",
				"type": "equal"
			},{
				"keyword": "123",
					"type": "like"
			}],
		"reply": 
			{
				"content":
				"每日签到活动2积分和优惠券1一张
				连续签到3天获得5积分和优惠券1一张
				连续签到5天获得7积分和优惠券1一张",
				"reply_type":"text"
			},
		"prize_settings":
			[{
				"serial_count":"1",
				"integral":"2",
				"coupon_name":"优惠券1"
			},{
				"serial_count":"3",
				"integral":"5",
				"coupon_name":"优惠券1"
			},{
				"serial_count":"5",
				"integral":"7",
				"coupon_name":"优惠券1"
			}]
	}
	"""
	And jobs更改"签到活动1"状态
	"""
	{
		"name":"签到活动1",
		"status":"关闭"
	}
	"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill的会员积分0
	When bill回复关键字

	Examples: 
		| keyword | type | 
		| 12      | equal|
		| 123     | like | 
		| 1234    | like |

	Then bill获得系统自动回复的消息"签到活动还未开始。"



Scenario: 5 签到活动结束后用户完全不匹配关键字签到
	Given jobs添加"签到活动1"
	"""
	{
		"name":"签到活动1",
		"sign_desc":"签到赚积分！连续签到奖励更丰富哦！",
		"share":
			{
				"img": 1.img,
				"desc":"签到送好礼！"
			},
		"key_word": 
			[{
				"keyword": "12",
				"type": "equal"
			},{
				"keyword": "123",
					"type": "like"
			}],
		"reply": 
			{
				"content":
				"每日签到活动2积分和优惠券1一张
				连续签到3天获得5积分和优惠券1一张
				连续签到5天获得7积分和优惠券1一张",
				"reply_type":"text"
			},
		"prize_settings":
			[{
				"serial_count":"1",
				"integral":"2",
				"coupon_name":"优惠券1"
			},{
				"serial_count":"3",
				"integral":"5",
				"coupon_name":"优惠券1"
			},{
				"serial_count":"5",
				"integral":"7",
				"coupon_name":"优惠券1"
			}]
	}
	"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill的会员积分0
	When bill回复关键字"1"
	Then bill没有获得系统回复的消息回复的消息



Scenario: 6 用户一天内连续两次签到
	Given jobs登录系统
	When bill关注jobs的公众号
	When bill访问jobs的weapp
	When bill的会员积分0
	When bill回复有效关键字进行签到
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
	Then bill获取"签到活动1"内容
	"""
	{
		"user_name":"bill",
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
	"""
	When bill访问系统回复的"url2"
	Then bill获取"签到活动1"内容
	"""
	{
		"user_name":"bill",
		"integral_account":"2"
		"integral_num":"2",
		"coupon_id":"优惠券1"
	}
	"""


Scenario: 11 优惠券数量为0,用户进行签到
	Given jobs登录系统
	And "优惠券1"数量为0
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
			"reply":"奖励已发完，请联系客服补发。"
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


Scenario: 12

	





















		"""
		[{
			"name":"活动名称",
			"details":"签到说明",
			"share pic": [{
				"url": "/weappimg.b0.upaiyun.com/upload/119_20150707/1436273979099_278.jpg"
			}],

			"share details":"分享至朋友圈、微信群、好友的文字内容",
			"keyword": [{
					"keyword": "关键字1",
					"type": "equal"
				},{
					"keyword": "关键字2",
					"type": "like"
				},{
					"keyword": "关键字3",
					"type": "like"
				},{
					"keyword": "关键字4",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"关键字回复内容",
					"reply_type":"text"
				}],
			"prize":[{
					"daily_points":"积分数1",
					"coupon_id":[优惠券1]
				},{
					"serial_count":"连续签到天数2",
					"serial_count_points":"积分数2",
					"coupon_id":[优惠券2]
				},{
					"serial_count":"连续签到天数3",
					"serial_count_points":"积分数3",
					"coupon_id":[优惠券3]
				}]
		}]
		"""
	Then jobs能获取签到活动配置内容
		"""
		{
			"name": "活动名称",
			"status": "关闭"
		}
		"""
	And jobs能开启签到活动
		"""
		{
			"name":"活动名称",
			"status":"关闭",
			"actions": ["开启]
		}
		"""

Scenario: 1 用户关注公众号进行签到
	bill在jobs的公众号进行签到
	Given jobs登录系统
	When jobs添加"签到活动1"
	"""
		{
			"name":"签到活动1",
			"prize":
				{
				"daily_points":10,
				"coupon_id":[优惠券1]
				}
		}
	"""
	When jobs开启"签到活动1"
	When bill关注jobs公众号
	When bill积分0
	When bill参加"签到活动1"
	Then bill积分10
	Then bill获得优惠券1
Scenario: 2 非会员用户通过朋友圈分享签到
	bill分享jobs公众号的签到活动到微信朋友圈
	非会员好友签到
	Given jobs登录系统
	When jobs添加"签到活动1"
	"""
		{
			"name":"签到活动1",
			"prize":
				{
				"daily_points":10,
				"coupon_id":[优惠券1]
				}
		}
	"""
	When jobs开启"签到活动1"
	When bill关注jobs公众号
	When bill积分0
	When bill参加"签到活动1"
	Then bill积分10
	Then bill获得优惠券1
	When bill分享"签到活动1"到朋友圈
	When jack关注jobs公众号
	When jack积分0
	When jack参加"签到活动1"
	Then jack积分10
	Then jack获得优惠券1
Scenario: 3 会员用户通过朋友圈分享签到
	bill分享jobs公众号的签到活动到微信朋友圈
	会员好友签到
	Given jobs登录系统
	When jobs添加"签到活动1"
	"""
		{
			"name":"签到活动1",
			"prize":
				{
				"daily_points":10,
				"coupon_id":[优惠券1]
				}
		}
	"""
	When jobs开启"签到活动1"
	When bill关注jobs公众号
	When bill积分0
	When bill参加"签到活动1"
	Then bill积分10
	Then bill获得优惠券1
	When bill分享"签到活动1"到朋友圈
	When jack积分10
	When jack参加"签到活动1"
	Then jack积分20
	Then jack获得优惠券1
Scenario: 4 用户分享签到活动给非会员微信朋友
	bill分享jobs公众号的签到活动给非会员jack
	Given jobs登录系统
	When jobs添加"签到活动1"
	"""
		{
			"name":"签到活动1",
			"prize":
				{
				"daily_points":10,
				"coupon_id":[优惠券1]
				}
		}
	"""
	When jobs开启"签到活动1"
	When bill关注jobs公众号
	When bill积分0
	When bill参加"签到活动1"
	Then bill积分10
	Then bill获得优惠券1
	When bill分享"签到活动1"给jack
	When 关注jobs公众号
	When jack积分0
	When jack参加"签到活动1"
	Then jack积分10
	Then jack获得优惠券1
Scenario: 5 用户分享签到活动给会员微信朋友
	bill分享jobs公众号的签到活动给会员jack
	Given jobs登录系统
	When jobs添加"签到活动1"
	"""
		{
			"name":"签到活动1",
			"prize":
				{
				"daily_points":10,
				"coupon_id":[优惠券1]
				}
		}
	"""
	When jobs开启"签到活动1"
	When bill关注jobs公众号
	When bill积分0
	When bill参加"签到活动1"
	Then bill积分10
	Then bill获得优惠券1
	When bill分享"签到活动1"给jack
	When jack积分10
	When jack参加"签到活动1"
	Then jack积分20
	Then jack获得优惠券1