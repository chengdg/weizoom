# __author__ : "王新蕊"
# __author__ : "王丽"
Feature: 群发优惠券
"""
	筛选出会员发送优惠券
	#除已跑路外
"""

Background:
	Given jobs登录系统

	#添加单品优惠券
		And jobs已添加商品
			"""
			[{
				"name": "商品1",
				"price": 200.00
			}]
			"""
		And jobs已添加了优惠券规则
			"""
			[{
				"name": "单品券2",
				"money": 10.00,
				"each_limit": "不限",
				"count": 10,
				"start_date": "今天",
				"end_date": "1天后",
				"coupon_id_prefix": "coupon2_id_",
				"coupon_product": "商品1"
			}]
			"""
		Then jobs能获得优惠券'单品券2'的码库
			"""
			{
				"coupon2_id_1": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_2": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_3": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_4": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_5": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_6": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_7": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_8": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_9": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_10": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""

	#构造系统会员
		Given nokia关注jobs的公众号
		And tom关注jobs的公众号
		And tom2关注jobs的公众号
		And tom3关注jobs的公众号
		And tom5关注jobs的公众号

		And tom5取消关注jobs的公众号

@memberList
Scenario:1 给筛选出选中的部分会员发送优惠券

	Given jobs登录系统

	#给筛选出来的选中的部分会员发放优惠券
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom",
				"status":"全部"
			}]
			"""
		When jobs选择会员
			| member_name | member_rank |
			|     tom     |   普通会员  |
			|     tom5    |   普通会员  |

		When jobs批量发优惠券
			"""
			[{
				"modification_method":"给选中的人发优惠券(已取消关注的除外)",
				"coupon_name":"单品券2",
				"count":2
			}]
			"""
		Then jobs优惠券发放成功

	#校验会员领取优惠券
		When tom访问jobs的webapp
		Then tom能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon2_id_1",
				"money": 10.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon2_id_2",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom2访问jobs的webapp
		Then tom2能获得webapp优惠券列表
			"""
			[ ]
			"""

		When tom3访问jobs的webapp
		Then tom3能获得webapp优惠券列表
			"""
			[ ]
			"""

		When tom5访问jobs的webapp
		Then tom5能获得webapp优惠券列表
			"""
			[ ]
			"""

		When nokia访问jobs的webapp
		Then nokia能获得webapp优惠券列表
			"""
			[ ]
			"""
	#校验jobs后台发放优惠券的情况
		Given jobs登录系统
		Then jobs能获得优惠券'单品券2'的码库
			"""
			{
				"coupon2_id_1": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom"
				},
				"coupon2_id_2": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom"
				},
				"coupon2_id_3": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_4": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_5": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_6": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_7": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_8": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_9": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_10": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""

@memberList
Scenario:2 给筛选出会员发送优惠券

	Given jobs登录系统

	#给筛选出来的会员发放优惠券
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom",
				"status":"全部"
			}]
			"""
		When jobs选择会员
			| member_name | member_rank |

		When jobs批量发优惠券
			"""
			[{
				"modification_method":"给筛选出来的所有人发优惠券(已取消关注的除外)",
				"coupon_name":"单品券2",
				"count":2
			}]
			"""
		Then jobs优惠券发放成功

	#校验会员领取优惠券
		When tom访问jobs的webapp
		Then tom能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon2_id_1",
				"money": 10.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon2_id_2",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom2访问jobs的webapp
		Then tom2能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon2_id_3",
				"money": 10.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon2_id_4",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom3访问jobs的webapp
		Then tom3能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon2_id_5",
				"money": 10.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon2_id_6",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom5访问jobs的webapp
		Then tom5能获得webapp优惠券列表
			"""
			[ ]
			"""

		When nokia访问jobs的webapp
		Then nokia能获得webapp优惠券列表
			"""
			[ ]
			"""
	#校验jobs后台发放优惠券的情况
		Given jobs登录系统
		Then jobs能获得优惠券'单品券2'的码库
			"""
			{
				"coupon2_id_1": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom"
				},
				"coupon2_id_2": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom"
				},
				"coupon2_id_3": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom2"
				},
				"coupon2_id_4": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom2"
				},
				"coupon2_id_5": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom3"
				},
				"coupon2_id_6": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom3"
				},
				"coupon2_id_7": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_8": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_9": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_10": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""