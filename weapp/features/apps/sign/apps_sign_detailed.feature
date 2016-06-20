# __author__ : 邓成龙 2016.06.20

Feature: 签到-后台签到详情
"""
	【签到时间】：签到时间显示签到时间，精确到分;没有签到时显示当天日期，精确到分,默认为：年月日为当天时间，时分秒为0
	【获得奖励】:1.积分2.优惠券名称3.null
	【签到状态】为: √（签到） or ×（没有签到）
"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 10.00,
			"limit_counts": "无限",
			"start_date": "1天前",
			"end_date": "3天后",
			"coupon_id_prefix": "coupon1_id_"
		},{
			"name": "优惠券2",
			"money": 20.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_"
		},{
			"name": "优惠券M",
			"money": 20.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon3_id_"
		}]
		"""
	Given jobs添加签到活动"签到活动1",并且保存
		"""
		{
			"status": "off",
			"name": "签到活动1",
			"sign_describe": "签到赚积分！连续签到奖励更丰富哦！",
			"share_pic": "1.jpg",
			"share_describe": "签到送好礼！",
			"reply_content": "每日签到获得20积分,连续签到奖励更丰富哦！",
			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "10"
				},{
					"sign_in":"2",
					"send_coupon":"优惠券M"
				},{
					"sign_in":"3",
					"send_coupon":"优惠券1"
				},{
					"sign_in":"5",
					"send_coupon":"优惠券2"
				}]
		}
		"""
	When jobs已添加单图文
		"""
		[{
			"title":"签到得优惠",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"签到",
			"content":"签到",
			"jump_url":"签到活动1"
		}]
		"""
	And jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword":
				[{
					"keyword": "签到",
					"type": "equal"
				}],
			"keyword_reply":
				[{
					"reply_content":"签到得优惠",
					"reply_type":"text_picture"
				}]
		}]
		"""
	When jobs更新签到活动的状态
		"""
		{
			"name":"签到活动1",
			"status": "on"
		}
		"""

	Given bill关注jobs的公众号

	#会员签到

	#bill先连续签到5次，终止一天，再连续签到3次
		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到得优惠'
		When bill点击图文'签到得优惠'进入签到得优惠页面
		When bill参加签到活动于'2015-10-01 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到得优惠'
		When bill点击图文'签到得优惠'进入签到得优惠页面
		When bill参加签到活动于'2015-10-02 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到得优惠'
		When bill点击图文'签到得优惠'进入签到得优惠页面
		When bill参加签到活动于'2015-10-03 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到得优惠'
		When bill点击图文'签到得优惠'进入签到得优惠页面
		When bill参加签到活动于'2015-10-04 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到得优惠'
		When bill点击图文'签到得优惠'进入签到得优惠页面
		When bill参加签到活动于'2015-10-05 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到得优惠'
		When bill点击图文'签到得优惠'进入签到得优惠页面
		When bill参加签到活动于'2015-10-07 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到得优惠'
		When bill点击图文'签到得优惠'进入签到得优惠页面
		When bill参加签到活动于'2015-10-08 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到得优惠'
		When bill点击图文'签到得优惠'进入签到得优惠页面
		When bill参加签到活动于'2015-10-09 10:30:00'
@mall2 @apps @apps_sign @apps_sign_detailed
Scenario:1 会员签到统计详情列表
#倒序排列，一页显示15条记录
	Given jobs登录系统
	
	Then jobs获得'bill'签到详情列表
	"""
		[{
			"sign_time":"2015.10.15 00:00:00",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"2015.10.14 00:00:00",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"2015.10.13 00:00:00",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"2015.10.12 00:00:00",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"2015.10.11 00:00:00",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"2015.10.10 00:00:00",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"2015.10.09 10:30:00",
			"get_reward":"优惠券1",
			"sign_state":"1"
		},{
			"sign_time":"2015.10.08 10:30:00",
			"get_reward":"优惠券M",
			"sign_state":"1"
		},{
			"sign_time":"2015.10.07 10:30:00",
			"get_reward":"积分+10",
			"sign_state":"1"
		},{
			"sign_time":"2015.10.06 00:00:00",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"2015.10.05 10:30:00",
			"get_reward":"优惠券2",
			"sign_state":"1"
		},{
			"sign_time":"2015.10.04 10:30:00",
			"get_reward":"积分+10",
			"sign_state":"1"
		},{
			"sign_time":"2015.10.03 10:30:00",
			"get_reward":"优惠券1",
			"sign_state":"1"
		},{
			"sign_time":"2015.10.02 10:30:00",
			"get_reward":"优惠券M",
			"sign_state":"1"
		},{
			"sign_time":"2015.10.01 10:30:00",
			"get_reward":"积分+10",
			"sign_state":"1"
		}]
	""" 