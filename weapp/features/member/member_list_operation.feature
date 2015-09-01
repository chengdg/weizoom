# __author__ : "王丽"

Feature: 筛选会员列表-操作
"""
	1、【调分组】：将当前会员的分组调整为调整后的分组，下拉选择会员的"会员分组"模块中的所有分组，可多选
		例：会员"A"现在分组是"分组1,分组2"，"调分组"设置为"分组3,分组4"；现在会员"A"的分组是"分组3,分组4"
	2、【设等级】：为会员设置等级，弹出"会员等级"模块所有等级，下拉单选
	3、【发优惠券】：给当前会员发放优惠券；弹窗选择所有有效的优惠券，设置发送张数；单选，每次只能发放一种优惠券
	4、【加积分】：给会员在现有积分的基础上加积分；填写"分数"（可以是负数），"原因"调整积分的原因
		例：会员A的积分是50；
			1）当加积分为10，则会员的积分变成60
			2）当加积分为-10，则会员的积分变成40
	5、【查看聊天记录】：新页面跳转到【微信互动平台】-【消息互动】-【实时消息】下的本会员的消息详情页
"""

Background:

	Given jobs登录系统

	#添加相关基础数据
		When jobs添加会员等级
			"""
			[{
				"name": "银牌会员",
				"upgrade": "手动升级",
				"discount": "10"
			},{
				"name": "金牌会员",
				"upgrade": "手动升级",
				"discount": "9"
			}]
			"""
		Then jobs能获取会员等级列表
			"""
			[{
				"name": "普通会员",
				"upgrade": "自动升级",
				"discount": "10"
			},{
				"name": "银牌会员",
				"upgrade": "手动升级",
				"discount": "10"
			},{
				"name": "金牌会员",
				"upgrade": "手动升级",
				"discount": "9"
			}]
			"""
		When jobs添加会员分组
			"""
			{
				"tag_id_1": "分组1",
				"tag_id_2": "分组2",
				"tag_id_3": "分组3"
			}
			"""

	#批量获取微信用户关注
		When jobs批量获取微信用户关注
			| member_name   |   attention_time     | member_source |
			| tom1 			| 2014-08-04 23:59:59  |    直接关注   |
			| tom2 			| 2014-08-05 00:00:00  |    推广扫码   |
			| tom3	 	    | 2014-08-05 08:00:00  |    会员分享   |

		#And tom2取消关注jobs的公众号

	#获取会员积分
		When 清空浏览器
		When tom1访问jobs的webapp
		When tom1获得jobs的50会员积分
		Then tom1在jobs的webapp中拥有50会员积分

		When 清空浏览器
		When tom2访问jobs的webapp
		When tom2获得jobs的100会员积分
		Then tom2在jobs的webapp中拥有100会员积分

	#会员聊天记录
	#	When tom1关注jobs的公众号
	#	When tom1在模拟器中发送消息'tom1发送一条文本消息，未回复'
	#
	#	When tom2关注jobs的公众号
	#	When tom2在模拟器中发送消息'tom2发送一条文本消息，回复文本消息'
	#	When jobs在模拟器中给tom2回复消息'jobs回复tom2消息'

@mall2 @member @memberList 
Scenario:1 调分组
	Given jobs登录系统
	#给没有分组的人设置分组
		When jobs给"tom1"调分组
			"""
			[
				"分组1", "分组3"
			]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags    |
			| tom3  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-08-05    | 会员分享 |            |
			| tom2  |   普通会员  |       0      |     100  |   0.00    |    0.00    |      0    |   2014-08-05    | 推广扫码 |            |
			| tom1  |   普通会员  |       0      |     50   |   0.00    |    0.00    |      0    |   2014-08-04    | 直接关注 |分组1,分组3 |

	#给有分组的人设置分组
		When jobs给"tom1"调分组
			"""
			["分组2"]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags    |
			| tom3  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-08-05    | 会员分享 |            |
			| tom2  |   普通会员  |       0      |     100  |   0.00    |    0.00    |      0    |   2014-08-05    | 推广扫码 |            |
			| tom1  |   普通会员  |       0      |     50   |   0.00    |    0.00    |      0    |   2014-08-04    | 直接关注 |   分组2    |

	#给有分组的人设置成分组为空
		When jobs给"tom1"调分组
			"""
			[]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags    |
			| tom3  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-08-05    | 会员分享 |            |
			| tom2  |   普通会员  |       0      |     100  |   0.00    |    0.00    |      0    |   2014-08-05    | 推广扫码 |            |
			| tom1  |   普通会员  |       0      |     50   |   0.00    |    0.00    |      0    |   2014-08-04    | 直接关注 |            |

@mall2 @member @memberList
Scenario:2 设等级

	Given jobs登录系统
	#给当前会员设置等级
		When jobs给"tom2"设等级
			"""
			{
				"member_rank":"金牌会员"
			}
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags    |
			| tom3  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-08-05    | 会员分享 |            |
			| tom2  |   金牌会员  |       0      |     100  |   0.00    |    0.00    |      0    |   2014-08-05    | 推广扫码 |            |
			| tom1  |   普通会员  |       0      |     50   |   0.00    |    0.00    |      0    |   2014-08-04    | 直接关注 |            |

	#给当前会员设置现在的等级

		When jobs给"tom2"设等级
			"""
			{
				"member_rank":"金牌会员"
			}
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags    |
			| tom3  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-08-05    | 会员分享 |            |
			| tom2  |   金牌会员  |       0      |     100  |   0.00    |    0.00    |      0    |   2014-08-05    | 推广扫码 |            |
			| tom1  |   普通会员  |       0      |     50   |   0.00    |    0.00    |      0    |   2014-08-04    | 直接关注 |            |

@mall2 @member @memberList
Scenario:3 发优惠券

	Given bill关注jobs的公众号
	And tom关注jobs的公众号
	And tom取消关注jobs的公众号

	#添加优惠券规则
		Given jobs登录系统
		Given jobs已添加商品
			"""
			[{
				"name": "商品1",
				"price": 100.00
			}]
			"""

		And jobs已添加了优惠券规则
			"""
			[{
				"name": "单品券1",
				"money": 10.00,
				"limit_counts": 1,
				"count": 3,
				"start_date": "今天",
				"end_date": "1天后",
				"coupon_id_prefix": "coupon1_id_",
				"coupon_product": "商品1"
			},{
				"name": "全店券2",
				"money": 20.00,
				"limit_counts": "无限",
				"count": 5,
				"start_date": "今天",
				"end_date": "1天后",
				"coupon_id_prefix": "coupon2_id_"
			}]
			"""

		Then jobs能获得优惠券'单品券1'的码库
			"""
			{
				"coupon1_id_1": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_2": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_3": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""

		Then jobs能获得优惠券'全店券2'的码库
			"""
			{
				"coupon2_id_1": {
					"money": 20.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_2": {
					"money": 20.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_3": {
					"money": 20.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_4": {
					"money": 20.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_5": {
					"money": 20.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""

	#给一个人发单品优惠券，当达到本优惠券的单人限制上限，不能再领取

		#给bill发放限领一张的单品优惠券，bill可以成功获得优惠券
			When jobs给"bill"发优惠券
				"""
				[{
					"name":"单品券1",
					"money": 10.00,
					"count":1
				}]
				"""
			When bill访问jobs的webapp
			Then bill能获得webapp优惠券列表
				"""
				[{
					"coupon_id": "coupon1_id_1",
					"money": 10.00,
					"status": "未使用"
				}]
				"""
			Given jobs登录系统
			Then jobs能获得优惠券'单品券1'的码库
				"""
				{
					"coupon1_id_1": {
						"money": 10.00,
						"status": "未使用",
						"consumer": "",
						"target": "bill"
					},
					"coupon1_id_2": {
						"money": 10.00,
						"status": "未领取",
						"consumer": "",
						"target": ""
					},
					"coupon1_id_3": {
						"money": 10.00,
						"status": "未领取",
						"consumer": "",
						"target": ""
					}
				}
				"""

		#给bill发放限领一张的单品优惠券，bill已经领取了一张，可发送成功，但是bill只有一张优惠券
			When jobs给"bill"发优惠券
				"""
				[{
					"name":"单品券1",
					"money": 10.00,
					"count":1
				}]
				"""
			When bill访问jobs的webapp
			Then bill能获得webapp优惠券列表
				"""
				[{
					"coupon_id": "coupon1_id_1",
					"money": 10.00,
					"status": "未使用"
				}]
				"""
			Given jobs登录系统
			Then jobs能获得优惠券'单品券1'的码库
				"""
				{
					"coupon1_id_1": {
						"money": 10.00,
						"status": "未使用",
						"consumer": "",
						"target": "bill"
					},
					"coupon1_id_2": {
						"money": 10.00,
						"status": "未领取",
						"consumer": "",
						"target": ""
					},
					"coupon1_id_3": {
						"money": 10.00,
						"status": "未领取",
						"consumer": "",
						"target": ""
					}
				}
				"""

	#给取消关注的一个人发全店优惠券，无单人领取限制，可以发放多次，领取多张，此会员关注后，可以看到在取消关注时发放的优惠券

		#给取消关注的tom发放无领取限制的全店优惠券，tom可以成功获得优惠券
			When jobs给"tom"发优惠券
				"""
				[{
					"name":"全店券2",
					"money": 20.00,
					"count":2
				}]
				"""
			When tom关注jobs的公众号
			When tom访问jobs的webapp
			Then tom能获得webapp优惠券列表
				"""
				[{
					"coupon_id": "coupon2_id_1",
					"money": 20.00,
					"status": "未使用"
				},{
					"coupon_id": "coupon2_id_2",
					"money": 20.00,
					"status": "未使用"
				}]
				"""
			Given jobs登录系统
			Then jobs能获得优惠券'全店券2'的码库
				"""
				{
					"coupon2_id_1": {
						"money": 20.00,
						"status": "未使用",
						"consumer": "",
						"target": "tom"
					},
					"coupon2_id_2": {
						"money": 20.00,
						"status": "未使用",
						"consumer": "",
						"target": "tom"
					},
					"coupon2_id_3": {
						"money": 20.00,
						"status": "未领取",
						"consumer": "",
						"target": ""
					},
					"coupon2_id_4": {
						"money": 20.00,
						"status": "未领取",
						"consumer": "",
						"target": ""
					},
					"coupon2_id_5": {
						"money": 20.00,
						"status": "未领取",
						"consumer": "",
						"target": ""
					}
				}
				"""

		#给tom发放无领取限制的全店优惠券，tom已经领取了两张，不能发送，tom只能领取到第一次发放的优惠券
		#超过优惠券剩余的个数，不能再领取
			When jobs给"tom"发优惠券
				"""
				[{
					"name":"全店券2",
					"money": 20.00,
					"count":4
				}]
				"""
			When tom访问jobs的webapp
			Then tom能获得webapp优惠券列表
				"""
				[{
					"coupon_id": "coupon2_id_1",
					"money": 20.00,
					"status": "未使用"
				},{
					"coupon_id": "coupon2_id_2",
					"money": 20.00,
					"status": "未使用"
				}]
				"""
			Given jobs登录系统
			Then jobs能获得优惠券'全店券2'的码库
				"""
				{
					"coupon2_id_1": {
						"money": 20.00,
						"status": "未使用",
						"consumer": "",
						"target": "tom"
					},
					"coupon2_id_2": {
						"money": 20.00,
						"status": "未使用",
						"consumer": "",
						"target": "tom"
					},
					"coupon2_id_3": {
						"money": 20.00,
						"status": "未领取",
						"consumer": "",
						"target": ""
					},
					"coupon2_id_4": {
						"money": 20.00,
						"status": "未领取",
						"consumer": "",
						"target": ""
					},
					"coupon2_id_5": {
						"money": 20.00,
						"status": "未领取",
						"consumer": "",
						"target": ""
					}
				}
				"""

@mall2 @member @memberList
Scenario:4 加积分

	Given jobs登录系统

	#给当前会员积分为零时加积分负数，积分变为负数
		When jobs给"tom3"加积分
			"""
			{
				"integral":-10,
				"reason":""
			}
			"""
		Then jobs可以获得会员列表
		| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags    |
		| tom3  |   普通会员  |       0      |   -10    |   0.00    |    0.00    |      0    |   2014-08-05    | 会员分享 |            |
		| tom2  |   普通会员  |       0      |     100  |   0.00    |    0.00    |      0    |   2014-08-05    | 推广扫码 |            |
		| tom1  |   普通会员  |       0      |     50   |   0.00    |    0.00    |      0    |   2014-08-04    | 直接关注 |            |


	#给当前会员积分为零时加积分正数
		When jobs给"tom3"加积分
			"""
			{
				"integral":20,
				"reason":"添加积分的原因"
			}
			"""
		Then jobs可以获得会员列表
		| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags    |
		| tom3  |   普通会员  |       0      |    10    |   0.00    |    0.00    |      0    |   2014-08-05    | 会员分享 |            |
		| tom2  |   普通会员  |       0      |     100  |   0.00    |    0.00    |      0    |   2014-08-05    | 推广扫码 |            |
		| tom1  |   普通会员  |       0      |     50   |   0.00    |    0.00    |      0    |   2014-08-04    | 直接关注 |            |

@member @memberList
Scenario:5 查看聊天记录

	#查看有会员消息的会员消息记录
		When jobs查看"tom1"聊天记录
			"""
			{
				"name":"tom1"
			}
			"""

		Then jobs获得"tom1"聊天记录列表
			"""
			[{
				"name":"tom1",
				"time":"今天",
				"inf_content":"tom1发送一条文本消息，未回复"
				"have_read": false
			}]
			"""

	#查看已回复消息的会员消息记录
		When jobs查看"tom2"聊天记录
			"""
			{
				"name":"tom2"
			}
			"""

		Then jobs获得"tom2"聊天记录列表
			"""
			[{
				"name":"jobs",
				"time":"今天",
				"inf_content":"jobs回复tom2消息 "
				"have_read": true
			},{
				"name":"tom2",
				"time":"今天",
				"inf_content":"tom2发送一条文本消息，回复文本消息"
				"have_read": true
			}]
			"""

	#查看无聊天记录的会员消息记录
		When jobs查看"tom3"聊天记录
			"""
			{
				"name":"tom3"
			}
			"""

		Then jobs不会打开新页面跳转到会员的"消息详情"页面
