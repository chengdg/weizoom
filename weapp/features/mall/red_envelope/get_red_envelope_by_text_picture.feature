#author:张三香 2015.10.20

Feature:获取图文领取分享红包

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name":"商品1",
			"price":10.0
		}]
		"""
	When jobs添加优惠券规则
		"""
		[{
			"name": "单品券1",
			"money": 5.00,
			"count": 5,
			"limit_counts": "无限",
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "商品1"
		},{
			"name": "全体券2",
			"money": 10.00,
			"count": 5,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "2天后",
			"coupon_id_prefix": "coupon2_id_"

		}]
		"""
	When jobs添加分享红包
		"""
		[{
			"name": "红包1",
			"prize_info": "单品券1",
			"is_permanant_active": true,
			"limit_money": "无限制",
			"receive_method":"图文领取",
			"detail": "图文领取领红包1",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"remark":"分享描述1"
		},{
			"name": "红包2",
			"prize_info": "全体券2",
			"is_permanant_active": false,
			"start_date": "今天",
			"end_date": "2天后",
			"limit_money": "无限制",
			"receive_method":"图文领取",
			"detail": "图文领取红包2",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"remark":"分享描述2"
		}]
		"""

	When jobs已添加单图文
		"""
		[{
			"title":"红包1单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"cover_in_the_text":"false",
			"summary":"红包1图文文本摘要",
			"content":"红包1图文文本内容",
			"jump_url":"分享红包-红包1"
		}]
		"""
	When jobs已添加多图文
		"""
		[{
			"title":"多图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
				}],
			"cover_in_the_text":"true",
			"content":"文本内容1"
		},{
			"title":"sub图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
				}],
				"cover_in_the_text":"true",
				"content":"sub单条图文1文本内容"
		},{
			"title":"sub红包2图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/wufan1.jpg"
				}],
			"cover_in_the_text":"false",
			"jump_url":"分享红包-红包2",
			"content":"sub红包2图文文本内容"
		}]
		"""
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": [{
					"keyword": "红包1",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"红包1单图文",
					"reply_type":"text_picture"
				}]
		},{
			"rules_name":"规则2",
			"keyword": [{
					"keyword": "红包2",
					"type": "equal"
				}],
			"keyword_reply": [{
				"reply_type":"text_picture",
				"reply_content":"多图文"
				}]

		}]
		"""

@mall2 @promotion @promotionRedbag
Scenario:1 自动回复获取图文领取分享红包
	#自动回复单图文领取分享红包
	When 清空浏览器
	When bill关注jobs的公众号
	When bill在微信中向jobs的公众号发送消息'红包1'
	Then bill收到自动回复'红包1单图文'
	When bill点击图文"红包1单图文"
	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 5.00,
			"status": "未使用"
		}]
		"""
	#自动回复多图文领取分享红包
	When bill在微信中向jobs的公众号发送消息'红包2'
	Then bill收到自动回复'多图文'
	When bill点击图文"sub红包2图文"
	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_1",
			"money": 10.00,
			"status": "未使用"
		},{
			"coupon_id": "coupon1_id_1",
			"money": 5.00,
			"status": "未使用"
		}]
		"""

	#同一个图文领取分享红包，只能领一次
	When bill在微信中向jobs的公众号发送消息'红包1'
	Then bill收到自动回复'红包1单图文'
	When bill点击图文"红包1单图文"
	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_1",
			"money": 10.00,
			"status": "未使用"
		},{
			"coupon_id": "coupon1_id_1",
			"money": 5.00,
			"status": "未使用"
		}]
		"""

@mall2 @promotion @promotionRedbag
Scenario:2 通过好友分享获取图文领取分享红包
	When 清空浏览器
	When bill关注jobs的公众号
	When bill在微信中向jobs的公众号发送消息'红包1'
	Then bill收到自动回复'红包1单图文'
	When bill点击图文"红包1单图文"
	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 5.00,
			"status": "未使用"
		}]
		"""
	When bill把jobs的分享红包链接分享到朋友圈
	#会员通过分享链接领取分享红包
	When 清空浏览器
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom点击bill分享红包链接
	Then tom能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_2",
			"money": 5.00,
			"status": "未使用"
		}]
		"""

	#非会员通过分享链接领取分享红包
	#暂时用先关注再取消关注的方式来模拟非会员的情况，需要改进
	When tom2关注jobs的公众号
	And tom2取消关注jobs的公众号
	When tom2访问jobs的webapp
	When tom2点击bill分享红包链接
	Then tom2能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_3",
			"money": 5.00,
			"status": "未使用"
		}]
		"""

	#好友分享的红包，只能领取1个
	When tom访问jobs的webapp
	When tom点击bill分享红包链接
	Then tom能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_2",
			"money": 5.00,
			"status": "未使用"
		}]
		"""

@mall2 @promotion @promotionRedbag
Scenario:3 优惠券库存为0,红包领取失败
	Given bill关注jobs的公众号
	And tom关注jobs的公众号
	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"name": "单品券1",
			"count": 4,
			"members": ["bill"],
			"coupon_ids": ["coupon1_id_4","coupon1_id_3","coupon1_id_2","coupon1_id_1"]
		}
		"""
	When bill在微信中向jobs的公众号发送消息'红包1'
	Then bill收到自动回复'红包1单图文'
	When bill点击图文"红包1单图文"
	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_5",
			"money": 5.00,
			"status": "未使用"
		},{
			"coupon_id": "coupon1_id_4",
			"money": 5.00,
			"status": "未使用"
			},{
			"coupon_id": "coupon1_id_3",
			"money": 5.00,
			"status": "未使用"
		},{
			"coupon_id": "coupon1_id_2",
			"money": 5.00,
			"status": "未使用"
		},{
			"coupon_id": "coupon1_id_1",
			"money": 5.00,
			"status": "未使用"
		}]
		"""
	When bill把jobs的分享红包链接分享到朋友圈

	#tom点击bill分享链接页面展示'很遗憾，红包已经领完了'

	When tom点击bill分享红包链接
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[]
		"""
	Given jobs登录系统
	When jobs为优惠券'单品券1'添加库存
		"""
		{
			"count": 1,
			"coupon_id_prefix": "coupon1_id_"
		}
		"""
	When bill访问jobs的webapp
	When bill把jobs的分享红包链接分享到朋友圈
	When tom访问jobs的webapp
	When tom点击bill分享红包链接
	Then tom能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_6",
			"money": 5.00,
			"status": "未使用"
		}]
		"""

@mall2 @promotion @promotionRedbag
Scenario:4 删除分享红包,红包领取失败
	Given jobs登录系统
	Then jobs能获取分享红包列表
		"""
		[{
			"name": "【图文领取】红包2",
			"status": "开启",
			"actions": ["分析","删除","查看"]
		},{
			"name": "【图文领取】红包1",
			"status": "开启",
			"actions": ["分析","删除","查看"]
		}]
		"""
	When jobs'删除'分享红包'【图文领取】红包1'
	When 清空浏览器
	When bill关注jobs的公众号
	When bill在微信中向jobs的公众号发送消息'红包1'
	Then bill收到自动回复'红包1单图文'
	When bill点击图文"红包1单图文"
	#页面展示'很遗憾，红包已经领完了'
	Then bill能获得webapp优惠券列表
		"""
		[]
		"""