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
			"money": 2.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_"
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
	Then jobs能获得优惠券'优惠券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 2.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
@apps_sign @apps_sign_frontend
Scenario:1 用户进入签到页面完成"签到活动1"签到
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
					"key_word": "签到"
				}],
			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "2",
					"send_coupon": "优惠券1"
				}]
		}
		"""
	And jobs更新签到活动的状态
		"""
		{
			"name":"签到活动1",
			"status": "on"
		}
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0会员积分
	When bill进入jobs签到页面进行签到
	Then bill获取签到成功的内容
		"""
		[{
			"serial_count": "1",
			"daily_prize":
				{
					"integral":"2",
					"coupon":"优惠券1"
				},
			"curr_prize":
				{
					"integral":"2",
					"coupon":"优惠券1"
				}
		}]
		"""
  	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有2会员积分
  	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 1.00,
			"status": "未使用"
		}]
		"""

@apps_sign @apps_sign_frontend
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
	Then bill获得系统回复的消息
    """
    签到成功！<br />已连续签到1天。<br />本次签到获得以下奖励:<br />2积分<br />签到说明：签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分<br />
    """
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'123'
	Then bill获得系统回复的消息
    """
    亲，今天您已经签到过了哦，<br />明天再来吧！<br />
    """
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'1234'
	Then bill获得系统回复的消息
    """
    亲，今天您已经签到过了哦，<br />明天再来吧！<br />
    """

@apps_sign @apps_sign_frontend
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
	When bill在微信中向jobs的公众号发送消息'1'
	Then bill获得系统回复的消息
    """

    """
	When jobs更新签到活动的状态
		"""
		{
			"name": "签到活动1",
			"status": "off"
		}
		"""
	When 清空浏览器
	And bill在微信中向jobs的公众号发送消息'1'
	Then bill获得系统回复的消息
    """

    """
@apps_sign @apps_sign_frontend
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
	Then bill获得系统回复的消息
    """
    签到活动未开始
    """
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'abc'
	Then bill获得系统回复的消息
    """
    签到活动未开始
    """
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'abcd'
	Then bill获得系统回复的消息
    """
    签到活动未开始
    """

@apps_sign @apps_sign_frontend
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
	Then bill获得系统回复的消息
    """
    签到成功！<br />已连续签到1天。<br />本次签到获得以下奖励:<br />0积分<br />优惠券1<br />
    """
	When 清空浏览器
	When bill在微信中向jobs的公众号发送消息'签到'
	Then bill获得系统回复的消息
    """
    亲，今天您已经签到过了哦，<br />明天再来吧！<br />
    """
    When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 1.00,
			"status": "未使用"
		}]
		"""

@apps_sign @apps_sign_frontend
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
	Then bill获得系统回复的消息
    """
    签到成功！<br />已连续签到1天。<br />本次签到获得以下奖励:<br />2积分<br />签到说明：签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分,连续签到3天获得优惠券1一张<br />
    """
	When 清空浏览器
	When 修改系统时间为'1天后'
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'签到'
	Then bill获得系统回复的消息
    """
    签到成功！<br />已连续签到2天。<br />本次签到获得以下奖励:<br />2积分<br />签到说明：签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分,连续签到3天获得优惠券1一张<br />
    """
	When 清空浏览器
	When 修改系统时间为'2天后'
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'签到'
	Then bill获得系统回复的消息
    """
    签到成功！<br />已连续签到3天。<br />本次签到获得以下奖励:<br />0积分<br />优惠券1<br />
    """
	When 还原系统时间
    When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 1.00,
			"status": "未使用"
		}]
		"""

@apps_sign @apps_sign_frontend
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
	Then bill获得系统回复的消息
    """
    签到成功！<br />已连续签到1天。<br />本次签到获得以下奖励:<br />2积分<br />签到说明：签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分<br />
    """
	When bill点击系统回复的链接
	When bill把jobs的签到活动链接分享到朋友圈
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	Then tom在jobs的webapp中拥有0会员积分
	When tom点击bill分享的签到链接进行签到
  	When tom访问jobs的webapp
	Then tom在jobs的webapp中拥有2会员积分

@apps_sign @apps_sign_frontend
Scenario:8 非会员用户访问签到分享进行签到
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
	Then bill获得系统回复的消息
    """
    签到成功！<br />已连续签到1天。<br />本次签到获得以下奖励:<br />2积分<br />签到说明：签到赚积分！连续签到奖励更丰富哦！<br />每日签到获得2积分<br />
    """
	When bill点击系统回复的链接
	When bill把jobs的签到活动链接分享到朋友圈
    #暂时用先关注再取消关注的方式来模拟非会员的情况
	When tom关注jobs的公众号
    And tom取消关注jobs的公众号
    When tom点击bill分享的签到链接进行签到
    When tom通过弹出的二维码关注jobs的公众号
    When tom访问jobs的webapp
	Then tom在jobs的webapp中拥有0会员积分
    When tom点击bill分享的签到链接进行签到
  	When tom访问jobs的webapp
	Then tom在jobs的webapp中拥有2会员积分

@apps_sign @apps_sign_frontend @kuku9
Scenario:9 对签到活动内容进行修改，会员访问活动页面
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
	And jobs更新签到活动的状态
		"""
		{
			"name":"签到活动1",
			"status": "on"
		}
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有0会员积分
	When bill进入jobs签到页面进行签到
	Then bill获取签到成功的内容
		"""
		[{
			"serial_count": "1",
			"daily_prize":
				{
					"integral":"2",
					"coupon":"优惠券1"
				},
			"curr_prize":
				{
					"integral":"2",
					"coupon":"优惠券1"
				}
		}]
		"""
  	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有2会员积分
  	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 1.00,
			"status": "未使用"
		}]
		"""
	When jobs编辑签到活动,并且保存
		"""
		{
			"name": "签到活动2",
			"status": "off",
			"sign_describe": "签到赚积分！连续签到奖励更丰富哦！",
			"share_pic": "2.jpg",
			"share_describe": "签到送好礼！",
			"reply_content": "每日签到获得5积分和优惠券2一张",
			"reply_keyword":
				[{
					"rule": "模糊",
					"key_word": "签到"
				}],

			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "5",
					"send_coupon":"优惠券2"
				}]
		}
		"""
	Then jobs更新签到活动的状态
		"""
		{
			"name": "签到活动2",
			"status": "on"
		}
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有2会员积分
	When bill进入jobs签到页面进行签到
	Then bill获取签到成功的内容
		"""
		[{
			"serial_count": "1",
			"daily_prize":
				{
					"integral":"5",
					"coupon":"优惠券2"
				},
			"curr_prize":
				{
					"integral":"5",
					"coupon":"优惠券2"
				}
		}]
		"""
  	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有7会员积分
  	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 1.00,
			"status": "未使用"
		},{
			"coupon_id": "coupon2_id_1",
			"money": 2.00,
			"status": "未使用"
		}]
		"""