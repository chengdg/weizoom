#__author__ : "许韦"
Feature:用户进行签到

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
			"money": 5.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "3天后",
			"coupon_id_prefix": "coupon2_id_"
		},{
			"name": "优惠券3",
			"money": 10.00,
			"limit_counts": "无限",
			"start_date": "2天前",
			"end_date": "3天后",
			"coupon_id_prefix": "coupon3_id_"
		}]
		"""
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 1.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
@apps_sign @apps_sign_frontend @kuku
Scenario:1 用户浏览"签到活动1"
	Given jobs添加签到活动"签到活动1",并且保存
		"""
		{
			"status":"off",
			"name": "签到活动1",
			"sign_describe":"签到赚积分！连续签到奖励更丰富哦！",
			"share_pic":"1.img",
			"share_describe": "签到送好礼！",
			"reply_content":"每日签到获得2积分和优惠券1一张,连续签到3天获得5积分和优惠券1一张,连续签到5天获得7积分和优惠券1一张",
			"reply_keyword":
				[{
					"rule": "精确",
					"key_word": "12"
				},{
					"rule":"模糊",
					"key_word": "123"
				}],

			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "2",
					"send_coupon": "优惠券1",
					"prize_counts":50
				},{
					"sign_in": "3",
					"integral": "5",
					"send_coupon": "优惠券1",
					"prize_counts":50
				},{
					"sign_in": "5",
					"integral": "7",
					"send_coupon": "优惠券1",
					"prize_counts":50
				}]
		}
		"""
	And jobs更新签到活动的状态
		"""
		{
			"name":"签到活动1",
			"statis": "on"
		}
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0会员积分
	When bill进入jobs的签到页面
	Then bill获取"签到活动1"内容
		"""
		{
			"user_name":"bill",
			"integral_account":"0",
			"prize_item":
				{
					"integral":"2",
					"coupon_name":"优惠券1"
				},
			"sign_item":
			{
				"sign_desc":"签到赚积分！连续签到奖励更丰富哦！",
				"sign_rule":"1.每日签到,获得2积分奖励优惠券1一张,2.连续签到至3天,获得5积分奖励优惠券1一张,3.连续签到至5天,获得7积分奖励优惠券1一张"
			}
		}
		"""
@apps_sign @apps_sign_frontend @kuki
Scenario:2 用户回复精确关键字、完全匹配模糊关键字、不完全匹配模糊关键字签到
	Given jobs添加签到活动"签到活动1",并且保存
		"""
		{
			"status": "off",
			"name": "签到活动1",
			"sign_describe": "签到赚积分！连续签到奖励更丰富哦！",
			"share_pic": "1.jpg",
			"share_describe": "签到送好礼！",
			"reply_content": "每日签到获得2积分",
			"reply_keyword":
				[{
					"rule": "精确",
					"key_word": "12"
				},{
					"rule": "模糊",
					"key_word": "123"
				}],

			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "2"
				}]
		}
		"""
	And jobs更新签到活动的状态
		"""
		{
			"name": "签到活动1",
			"status": "on"
		}
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0会员积分
	When bill在微信中向jobs的公众号发送消息'12'
	Then bill获得系统回复的消息'签到成功！<br />已连续签到1天。<br />本次签到获得以下奖励:<br />2积分<br />签到说明：签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分<br />'
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'123'
	Then bill获得系统回复的消息'亲，今天您已经签到过了哦，<br />明天再来吧！<br />'
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'1234'
	Then bill获得系统回复的消息'亲，今天您已经签到过了哦，<br />明天再来吧！<br />'
	When bill点击系统回复的链接
#   Then bill获取"签到活动1"内容
#       """
#       {
#           "user_name":"bill",
#           "integral_account":"2",
#           "serial_count":"1",
#           "prize_item":
#               {
#                   "serial_count_next":"3",
#                   "integral":"5"
#               }
#       }
#       """
@apps_sign @apps_sign_frontend @kuki
Scenario:3 用户回复完全不匹配关键字签到
	Given jobs添加签到活动"签到活动1",并且保存
		"""
		{
			"status":"off",
			"name": "签到活动1",
			"sign_describe":"签到赚积分！连续签到奖励更丰富哦！",
			"share_pic":"1.jpg",
			"share_describe": "签到送好礼！",
			"reply_content":"每日签到获得优惠券1一张",
			"reply_keyword":
				[{
					"rule": "精确",
					"key_word": "12"
				},{
					"rule": "模糊",
					"key_word": "123"
				}],

			"sign_settings":
				[{
					"sign_in": "0",
					"send_coupon": "优惠券1",
					"prize_counts": 50
				}]
		}
		"""
	And jobs更新签到活动的状态
		"""
		{
			"name": "签到活动1",
			"status": "on"
		}
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0会员积分
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'1'
	Then bill获得系统回复的消息' '
	When jobs更新签到活动的状态
		"""
		{
			"name": "签到活动1",
			"status": "off"
		}
		"""
	When 清空浏览器
	And bill在微信中向jobs的公众号发送消息'1'
	Then bill获得系统回复的消息' '

@apps_sign @apps_sign_frontend @kuki
Scenario: 4 签到活动关闭时用户回复精确关键字、完全匹配模糊关键字、不完全匹配模糊关键字签到
	Given jobs添加签到活动"签到活动1",并且保存
		"""
		{
			"status": "off",
			"name": "签到活动1",
			"sign_describe": "签到赚积分！连续签到奖励更丰富哦！",
			"share_pic": "1.jpg",
			"share_describe": "签到送好礼！",
			"reply_content": "每日签到获得2积分和优惠券1一张",
			"reply_keyword":
				[{
					"rule": "精确",
					"key_word": "78"
				},{
					"rule": "模糊",
					"key_word": "abc"
				}],
			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "2",
					"send_coupon": "优惠券1"
				}]
		}
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0会员积分
	When bill在微信中向jobs的公众号发送消息'78'
	Then bill获得系统回复的消息'签到活动未开始'
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'abc'
	Then bill获得系统回复的消息'签到活动未开始'
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'abcd'
	Then bill获得系统回复的消息'签到活动未开始'

@apps_sign @apps_sign_frontend @kuki
Scenario:5 用户一天内连续两次签到，获取优惠券奖励
	Given jobs添加签到活动"签到活动1",并且保存
		"""
		{
			"status": "off",
			"name": "签到活动1",
			"sign_describe": "签到赚积分！连续签到奖励更丰富哦！",
			"share_pic": "1.jpg",
			"share_describe": "签到送好礼！",
			"reply_content": "每日签到获得优惠券1一张",
			"reply_keyword":
				[{
					"rule": "精确",
					"key_word": "签到"
				},{
					"rule": "模糊",
					"key_word": "123"
				}],
			"sign_settings":
				[{
					"sign_in": "0",
					"send_coupon": "优惠券1"
				}]
		}
		"""
	And jobs更新签到活动的状态
		"""
		{
			"name": "签到活动1",
			"status": "on"
		}
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0会员积分
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'签到'
	Then bill获得系统回复的消息'签到成功！<br />已连续签到1天。<br />本次签到获得以下奖励:<br />0积分<br />优惠券1<br />'
	When bill点击系统回复的链接
#   Then bill获取"签到活动1"内容
#       """
#       {
#           "user_name":"bill",
#           "integral_account":"0",
#           "serial_count":"1",
#           "prize_item":
#               {
#                   "serial_count_next":"3",
#                   "coupon_name":"优惠券2"
#               }
#       }
#       """
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 1.00,
			"status": "未使用"
		}]
		"""

@apps_sign @apps_sign_frontend @kuki
Scenario:6 用户连续3天进行签到
	Given jobs添加签到活动"签到活动1",并且保存
		"""
		{
			"status": "off",
			"name": "签到活动1",
			"sign_describe":  "签到赚积分！连续签到奖励更丰富哦！",
			"share_pic":  "1.jpg",
			"share_describe": "签到获得奖励",
			"reply_content": "每日签到获得2积分,连续签到3天获得优惠券1一张",
			"reply_keyword":
				[{
					"rule": "精确",
					"key_word": "签到"
				}],
			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "2"
				},{
					"sign_in":"3",
					"send_coupon":"优惠券1"
				}]
		}
		"""
	And jobs更新签到活动的状态
		"""
		{
			"name": "签到活动1",
			"status": "on"
		}
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0会员积分
	When bill在微信中向jobs的公众号发送消息'签到'
	Then bill获得系统回复的消息'签到成功！<br />已连续签到1天。<br />本次签到获得以下奖励:<br />2积分<br />签到说明：签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分,连续签到3天获得优惠券1一张<br />'
	When 清空浏览器
	When 修改系统时间为'1天后'
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'签到'
	Then bill获得系统回复的消息'签到成功！<br />已连续签到2天。<br />本次签到获得以下奖励:<br />2积分<br />签到说明：签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分,连续签到3天获得优惠券1一张<br />'
	When 清空浏览器
	When 修改系统时间为'2天后'
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'签到'
	Then bill获得系统回复的消息'签到成功！<br />已连续签到3天。<br />本次签到获得以下奖励:<br />0积分<br />优惠券1<br />'
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 1.00,
			"status": "未使用"
		}]
		"""
	When 还原系统时间

@apps_sign @apps_sign_frontend @kuki7
Scenario:7 用户分享"签到活动1"到朋友圈,会员通过分享到朋友圈的链接参与签到
	Given jobs添加签到活动"签到活动1",并且保存
		"""
		{
			"status": "off",
			"name": "签到活动1",
			"sign_describe":  "签到赚积分！连续签到奖励更丰富哦！",
			"share_pic":  "1.jpg",
			"share_describe": "签到获得奖励",
			"reply_content": "每日签到获得2积分",
			"reply_keyword":
				[{
					"rule": "精确",
					"key_word": "签到"
				}],
			"sign_settings":
				[{
					"sign_in": "0",

					"integral": "2"
				}]
		}
		"""
	And jobs更新签到活动的状态
		"""
		{
			"name": "签到活动1",
			"status": "on"
		}
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0会员积分
	When bill在微信中向jobs的公众号发送消息'签到'
	Then bill获得系统回复的消息'签到成功！<br />已连续签到1天。<br />本次签到获得以下奖励:<br />2积分<br />签到说明：签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分<br />'
	When bill点击系统回复的链接
	When bill把jobs的签到活动链接分享到朋友圈
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	Then tom在jobs的webapp中拥有0会员积分
	When tom点击bill分享的签到链接

@apps_sign @apps_sign_frontend
Scenario:8 非会员用户访问签到分享进行签到
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
					"keyword": "签到",
					"type": "equal"
				},{
					"keyword": "123",
						"type": "like"
				}],
			"reply":
				{
					"content":
					"每日签到获得优惠券1
					连续签到2天获得优惠券2
					连续签到3天获得30积分",
					"reply_type":"text"
				},
			"prize_settings":
				[{
					"serial_count":"1",
					"coupon_name":"优惠券1"
				},{

					"serial_count":"2",
					"coupon_name":"优惠券2"
				},{
					"serial_count":3",
					"integral":"30"
				}]
		}
		"""
	And jobs设置"签到活动1"状态
		"""
		{
			"name":"签到活动1",
			"status":"开启"
		}
		"""
	When bill分享"签到活动1"到朋友圈
	When jack没有关注公众号jobs
	When jack访问分享链接"share"
	Then jack获取"签到活动1"内容
		"""
		{
			"user_name":"jack",
			"integral_account":"0",
			"prize_item":
				{
					"coupon_name":"优惠券1",
				}
		}
		"""
	When jack进行签到
	Then jack获取"二维码1"
		"""
		{
			"img":2.img,
			"url_name":"识别图中二维码",
			"url":url3
		}
		"""
	When jack访问"url3"
	When jack关注jobs的公众号
	When jack访问jobs的webapp
	When jack的会员积分0
	When jack访问分享链接"share"
	Then jack获取"签到活动1"内容
		"""
		{
			"user_name":"jack",
			"integral_account":"0",
			"prize_item":
				{
					"coupon_name":"优惠券1"
				}
		}
		"""
	When jack进行签到
	Then jack获取"签到活动1"内容
		"""
		{
			"user_name":"jack",
			"integral_account":"0",
			"serial_count":"1",
			"coupom_name":"优惠券1",
			"prize_item":
				{
					"serial_count_next":"2",
					"coupon_name":"优惠券2"
				}
		}
		"""