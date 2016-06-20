# __author__ : 邓成龙 2016-06-20
Feature: 签到-后台优惠券明细
"""
	优惠券明细列表
	领取时间：连续签到自动得到的优惠券时的时间
	优惠券名称：获得优惠券的名称
	明细：新建优惠券时给的类型：全部商品or部分商品
	状态：【全部、未使用、已使用、已过期】
	去处：【订单号】在商城购买商品下单时的订单号

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
			"coupon_id_prefix": "coupon1_id_",
			"detailed":"currency"
		},{
			"name": "优惠券2",
			"money": 20.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_",
			"detailed":"currency"
		},{
			"name": "优惠券M",
			"money": 20.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon3_id_",
			"detailed":"part"
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
			"reply_keyword":
				[{
					"rule": "精确",
					"key_word": "签到"
				}],
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
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-01 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-02 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-03 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-04 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-05 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-07 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-08 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-09 10:30:00'

	#tom先签到1次，终止一天，再连续签到2次
		When 清空浏览器
		When tom访问jobs的webapp
		When tom在微信中向jobs的公众号发送消息'签到'于'前两天'

		When 清空浏览器
		When tom访问jobs的webapp
		When tom在微信中向jobs的公众号发送消息'签到'于'前一天'

		When 清空浏览器
		When tom访问jobs的webapp
		When tom在微信中向jobs的公众号发送消息'签到'于'今天'
@mall2 @apps @apps_sign @apps_sign_backend @sign_statistics
Scenario:1 优惠券明细列表
	Given jobs登录系统
	When jobs查看'bill'的优惠券明细
	Then jobs获得'bill'优惠券明细列表
	"""
		[{
			"collection_time":"2015/10/09 10:30:00",
			"coupon":"优惠券1",
			"detailed":"通用券",
			"state":"已过期"
		},{
			"collection_time":"2015/10/05 10:30:00",
			"coupon":"优惠券2",
			"detailed":"通用券",
			"state":"已过期"
		},{
			"collection_time":"2015/10/02 10:30:00",
			"coupon":"优惠券M",
			"detailed":"多商品券",
			"state":"已过期"
		}]
	"""
	When jobs查看'tom'的优惠券明细
	Then jobs获得'tom'优惠券明细列表
	"""
		[{
			"collection_time":"今天",
			"coupon":"优惠券M",
			"detailed":"多商品券",
			"state":"未使用"
		}]
	"""
