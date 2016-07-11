# __author__ : 邓成龙 2016.06.20
#editor: 邓成龙 2016.07.06

Feature: 签到-后台签到详情
"""
	【签到时间】：签到时间显示签到时间，精确到分;没有签到时显示当天日期，精确到分,默认为：年月日为当天时间，时分秒为0
	【获得奖励】:1.积分2.优惠券名称3.null
	【签到状态】为:1表示 √（签到） or 0表示×（没有签到）
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
	Given jobs添加专项签到活动"签到活动1",并且保存
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
					"coupons":[{
						"send_coupon": "优惠券M",
						"member_grade":"全部"
					}]
				},{
					"sign_in":"3",
					"coupons":[{
						"send_coupon": "优惠券1",
						"member_grade":"全部"
					}]
				},{
					"sign_in":"5",
					"integral": "10",
					"coupons":[{
						"send_coupon": "优惠券2",
						"member_grade":"全部"
					}]
				}]
		}
		"""
	When jobs已添加单图文
		"""
		[{
			"title":"签到活动1",
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
					"reply_content":"签到活动1",
					"reply_type":"text_picture"
				}]
		}]
		"""
	When jobs更新专项签到活动的状态
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
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入专项签到活动页面
		When bill参加专项签到活动于'14天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入专项签到活动页面
		When bill参加专项签到活动于'13天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入专项签到活动页面
		When bill参加专项签到活动于'12天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入专项签到活动页面
		When bill参加专项签到活动于'11天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入专项签到活动页面
		When bill参加专项签到活动于'10天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入专项签到活动页面
		When bill参加专项签到活动于'8天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入专项签到活动页面
		When bill参加专项签到活动于'7天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入专项签到活动页面
		When bill参加专项签到活动于'6天前'

@mall2 @apps @apps_exsign @apps_exsign_detailed @cl_e
Scenario:1 会员签到统计详情列表
#倒序排列，一页显示15条记录
	Given jobs登录系统

	Then jobs获得'bill'参加专项签到'签到活动1'的签到详情列表
	"""
		[{
			"sign_time":"今天",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"1天前",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"2天前",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"3天前",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"4天前",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"5天前",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"6天前",
			"get_reward":"优惠券1",
			"sign_state":"1"
		},{
			"sign_time":"7天前",
			"get_reward":"优惠券M",
			"sign_state":"1"
		},{
			"sign_time":"8天前",
			"get_reward":"积分+10",
			"sign_state":"1"
		},{
			"sign_time":"9天前",
			"get_reward":"",
			"sign_state":"0"
		},{
			"sign_time":"10天前",
			"get_reward":"优惠券2",
			"sign_state":"1"
		},{
			"sign_time":"11天前",
			"get_reward":"积分+10",
			"sign_state":"1"
		},{
			"sign_time":"12天前",
			"get_reward":"优惠券1",
			"sign_state":"1"
		},{
			"sign_time":"13天前",
			"get_reward":"优惠券M",
			"sign_state":"1"
		},{
			"sign_time":"14天前",
			"get_reward":"积分+10",
			"sign_state":"1"
		}]
	"""
