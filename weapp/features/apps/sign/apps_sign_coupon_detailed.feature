# __author__ : 邓成龙 2016-06-20
Feature: 签到-后台优惠券明细
"""
	优惠券明细列表
	【领取时间】：连续签到自动得到的优惠券时的时间
	【优惠券名称】：获得优惠券的名称
	【明细】：新建优惠券时给的类型：全部商品or部分商品
	【状态】：【全部、未使用、已使用、已过期】
	【去处】：【订单号】在商城购买商品下单时的订单号

"""
Background:
	Given jobs登录系统
	Given jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}]
		"""

	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 10.00,
			"limit_counts": "无限",
			"start_date": "1天前",
			"end_date": "30天后",
			"coupon_id_prefix": "coupon1_id_",
			"description":"使用说明"
		},{
			"name": "优惠券2",
			"money": 20.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "20天后",
			"coupon_id_prefix": "coupon2_id_",
			"description":"使用说明"
		},{
            "name": "优惠券M",
            "money": 20.00,
            "limit_counts": "无限",
            "start_date": "2天前",
            "end_date": "20天后",
            "coupon_id_prefix": "coupon3_id_",
            "coupon_product": "商品1",
            "description":"使用说明"
        },{
            "name": "优惠券3",
            "money": 20.00,
            "limit_counts": "无限",
            "start_date": "2天前",
            "end_date": "20天后",
            "coupon_id_prefix": "coupon4_id_",
            "coupon_product": "商品1",
            "description":"使用说明"
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
					"integral": "20"
				},{
					"sign_in":"2",
					"send_coupon":"优惠券M"
				},{
					"sign_in":"3",
					"send_coupon":"优惠券1"
				},{
					"sign_in":"5",
					"integral": "10",
					"send_coupon":"优惠券2"
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
	When jobs更新签到活动的状态
		"""
		{
			"name":"签到活动1",
			"status": "on"
		}
		"""

	Given bill关注jobs的公众号
	And tom关注jobs的公众号

	#会员签到

	#bill先连续签到5次，终止一天，再连续签到3次
		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入签到得优惠页面
		When bill参加签到活动于'8天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入签到得优惠页面
		When bill参加签到活动于'7天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入签到得优惠页面
		When bill参加签到活动于'6天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入签到得优惠页面
		When bill参加签到活动于'5天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入签到得优惠页面
		When bill参加签到活动于'4天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入签到得优惠页面
		When bill参加签到活动于'2天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入签到得优惠页面
		When bill参加签到活动于'1天前'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'
		Then bill收到自动回复'签到活动1'
		When bill点击图文'签到活动1'进入签到得优惠页面
		When bill参加签到活动于'今天'

	#tom先签到1次，终止一天，再连续签到2次
		When 清空浏览器
		When tom访问jobs的webapp
		When tom在微信中向jobs的公众号发送消息'签到'
		Then tom收到自动回复'签到活动1'
		When tom点击图文'签到活动1'进入签到得优惠页面
		When tom参加签到活动于'3天前'

		When 清空浏览器
		When tom访问jobs的webapp
		When tom在微信中向jobs的公众号发送消息'签到'
		Then tom收到自动回复'签到活动1'
		When tom点击图文'签到活动1'进入签到得优惠页面
		When tom参加签到活动于'1天前'

		When 清空浏览器
		When tom访问jobs的webapp
		When tom在微信中向jobs的公众号发送消息'签到'
		Then tom收到自动回复'签到活动1'
		When tom点击图文'签到活动1'进入签到得优惠页面
		When tom参加签到活动于'今天'

		When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信抽奖",
			"start_date":"1天前",
			"end_date":"今天",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":0,
			"send_integral_rules":"仅限未中奖用户",
			"lottery_limit":"不限",
			"win_rate":"100%",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券3",
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":0,
				"prize_type":"优惠券",
				"coupon":"优惠券2",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":0,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
		"""
	
	When bill访问jobs的webapp
	When bill参加微信抽奖活动'微信抽奖'
	Then bill获得抽奖结果
		"""
		[{
			"prize_grade":"一等奖",
			"prize_type":"优惠券",
			"prize_name":"优惠券3"
		}]
		"""

@mall2 @apps @apps_sign @apps_sign_coupon_detailed
Scenario:1 优惠券明细列表
	Given jobs登录系统

	Then jobs获得'bill'参加'签到活动1'的优惠券明细列表
		"""
			[{
				"collection_time":"今天",
				"name":"优惠券1",
				"coupon_id":"coupon1_id_2",
				"type":"通用券",
				"status":"未使用"
			},{
				"collection_time":"1天前",
				"name":"优惠券M",
				"coupon_id":"coupon3_id_2",
				"type":"多商品券",
				"status":"未使用"
			},{
				"collection_time":"4天前",
				"name":"优惠券2",
				"coupon_id":"coupon2_id_1",
				"type":"多商品券",
				"status":"未使用"
			},{
				"collection_time":"5天前",
				"name":"优惠券1",
				"coupon_id":"coupon1_id_1",
				"type":"通用券",
				"status":"未使用"
			},{
				"collection_time":"6天前",
				"name":"优惠券M",
				"coupon_id":"coupon3_id_1",
				"type":"多商品券",
				"status":"未使用"
			}]
		"""
	
	Then jobs获得'tom'参加'签到活动1'的优惠券明细列表
		"""
			[{
				"collection_time":"今天",
				"coupon":"优惠券M",
				"detailed":"多商品券",
				"state":"未使用"
			}]
		"""

@mall2 @apps @apps_sign @apps_sign_coupon_detailed
Scenario:2 优惠券明细列表查询
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
			{
				"order_id": "00001",
				"pay_type": "微信支付",
				"products": [{
					"name": "商品1",
					"count": 1
				}],
				"coupon": "coupon1_id_1"
			}
		"""
	Given jobs登录系统
	Then jobs获得'bill'参加'签到活动1'的优惠券明细列表默认查询条件
		"""
			[{
				"status":"全部"
			}]
		"""
	Then jobs获得'bill'参加'签到活动1'的优惠券明细列表
		"""
			[{
				"collection_time":"今天",
				"name":"优惠券1",
				"coupon_id":"coupon1_id_2",
				"type":"通用券",
				"status":"未使用"
			},{
				"collection_time":"1天前",
				"name":"优惠券M",
				"coupon_id":"coupon3_id_2",
				"type":"多商品券",
				"status":"未使用"
			},{
				"collection_time":"4天前",
				"name":"优惠券2",
				"coupon_id":"coupon2_id_1",
				"type":"多商品券",
				"status":"未使用"
			},{
				"collection_time":"5天前",
				"name":"优惠券1",
				"coupon_id":"coupon1_id_1",
				"type":"通用券",
				"status":"未使用"
			},{
				"collection_time":"6天前",
				"name":"优惠券M",
				"coupon_id":"coupon3_id_1",
				"type":"多商品券",
				"status":"未使用"
			}]
		"""

	When jobs获得'bill'参加'签到活动1'的优惠券明细列表默认查询条件
		"""
			[{
				"status":"未使用"
			}]
		"""
	Then jobs获得'bill'参加'签到活动1'的优惠券明细列表
		"""
			[{
				"collection_time":"今天",
				"name":"优惠券1",
				"coupon_id":"coupon1_id_2",
				"type":"通用券",
				"status":"未使用"
			},{
				"collection_time":"1天前",
				"name":"优惠券M",
				"coupon_id":"coupon3_id_2",
				"type":"通用券",
				"status":"未使用"
			},{
				"collection_time":"4天前",
				"name":"优惠券2",
				"coupon_id":"coupon2_id_1",
				"type":"多商品券",
				"status":"未使用"
			},{
				"collection_time":"6天前",
				"name":"优惠券M",
				"coupon_id":"coupon3_id_1",
				"type":"通用券",
				"status":"未使用"
			}]
		"""

	When jobs获得'bill'参加'签到活动1'的优惠券明细列表默认查询条件
		"""
			[{
				"status":"已使用"
			}]
		"""
	Then jobs获得'bill'参加'签到活动1'的优惠券明细列表
		"""
			[{
				"collection_time":"今天",
				"name":"优惠券1",
				"coupon_id":"coupon1_id_1",
				"type":"通用券",
				"status":"已使用"
			}]
		"""
	When jobs获得'bill'参加'签到活动1'的优惠券明细列表默认查询条件
		"""
		[{
			"status":"已过期"
		}]
		"""
	Then jobs获得'bill'参加'签到活动1'的优惠券明细列表
		"""
		[]
		"""