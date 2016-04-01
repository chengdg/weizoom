#author: 王丽 2015-10-28

Feature:带参数二维码-代言人
"""
	手机端-代言人二维码页
	1 【会员昵称】
	2 【会员头像】
	3 【头衔】：在带参数二维码中设置的代言人"头衔"
	4 【带店铺图标的二维码】
	5 【活动说明】：在带参数二维码中设置的代言人"二维码描述"
	6 【已推荐扫码人数】：此二维码的"关注数量"
					(1)扫码新增会员数量（【已关注会员可参与】设置为"否"）
					(2)扫码新增会员数量+之前关注过的会员(包含当前为"关注"状态或者"取消关注"状态)
					扫码的会员数量（【已关注会员可参与】设置为"是"）
					(3)"已关注会员可参与"同一微信账号重复扫码[关注数量]累计一次
					(4)"已关注会员可参与"同一微信账号交替扫不同的码[关注数量]跳转
					(5)扫码人数为零，不能点击进入；扫码人数不为零，可以点击进入"推荐详情页"

	手机端-代言人-推荐详情页
	1 【扫码人数】：扫过此二维码的会员数量
					(1)扫码新增会员数量（【已关注会员可参与】设置为"否"）
					(2)扫码新增会员数量+之前关注过的会员(包含当前为"关注"状态或者"取消关注"状态)
					扫码的会员数量（【已关注会员可参与】设置为"是"）
					(3)"已关注会员可参与"同一微信账号重复扫码[关注数量]累计一次
					(4)"已关注会员可参与"同一微信账号交替扫不同的码[关注数量]跳转
	2 【下单人数】:扫码后下单的会员数
	3 【成交金额】:扫码后会员的有效订单（待发货、已发货、已完成）的订单的实付金额总和
	4 【会员列表】:扫码的会员列表
"""

Background:
	Given jobs登录系统
	#必须添加分组和等级数据库中才会有默认分组和等级
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}]
		"""
	And jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1"
		}
		"""

@mall2 @senior @bandParameterCode
Scenario:1 带参数二维码[关联会员]-代言人二维码页
	Given jobs登录系统

	When bill关注jobs的公众号于'2015-10-11 00:00:00'

	Given jobs登录系统
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-代言人二维码页",
			"create_time": "2015-10-10 10:20:30",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "true",
			"relation_time": "2015-10-11 10:20:30",
			"cancel_related_time": "",
			"relation_member": "bill",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		}]
		"""
	When 清空浏览器
	And bill访问jobs的webapp
	Then bill获得代言人二维码页
		"""
		{
			"member_name": "bill",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"recommended_number": 0
		}
		"""

@mall2 @senior @bandParameterCode
Scenario:2 带参数二维码[关联会员]-代言人二维码页-已推荐扫码人数
	Given jobs登录系统

	When bill关注jobs的公众号于'2015-10-11 00:00:00'

	#"已关注会员不可参与"的带参数二维码
		Given jobs登录系统
		When jobs添加带参数二维码
			"""
			[{
				"code_name": "带参数二维码-代言人二维码页-已推荐扫码人数",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "未分组",
				"is_attention_in": "false",
				"remarks": "",
				"is_relation_member": "true",
				"relation_time": "2015-10-11 10:20:30",
				"cancel_related_time": "",
				"relation_member": "bill",
				"title": "星级代言人",
				"code_description": "星级代言人二维码描述",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}]
			"""

		#"已关注会员不可参与"的带参数二维码：未关注微信用户扫码关注，已推荐扫码人数增加
			#tom扫码关注
			When 清空浏览器
			And tom扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"
			And tom访问jobs的webapp

			When 清空浏览器
			And bill访问jobs的webapp
			Then bill获得代言人二维码页
				"""
				{
					"member_name": "bill",
					"title": "星级代言人",
					"code_description": "星级代言人二维码描述",
					"recommended_number": 1
				}
				"""
		#"已关注会员不可参与"的带参数二维码：已关注会员扫码，已推荐扫码人数不增加
			#已关注会员jack扫码
			When 清空浏览器
			And jack关注jobs的公众号
			And jack访问jobs的webapp
			And jack扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"

			When 清空浏览器
			And bill访问jobs的webapp
			Then bill获得代言人二维码页
				"""
				{
					"member_name": "bill",
					"title": "星级代言人",
					"code_description": "星级代言人二维码描述",
					"recommended_number": 1
				}
				"""
		#"已关注会员不可参与"的带参数二维码：取消关注会员扫码关注，已推荐扫码人数不增加
			#取消关注会员marry扫码关注
			When 清空浏览器
			And marry关注jobs的公众号
			And marry访问jobs的webapp
			And marry取消关注jobs的公众号

			And marry扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"

			When 清空浏览器
			And bill访问jobs的webapp
			Then bill获得代言人二维码页
				"""
				{
					"member_name": "bill",
					"title": "星级代言人",
					"code_description": "星级代言人二维码描述",
					"recommended_number": 1
				}
				"""

	#"已关注会员可参与"的带参数二维码
		Given jobs登录系统
		When jobs更新带参数二维码'带参数二维码-代言人二维码页-已推荐扫码人数'
			"""
			{
				"code_name": "带参数二维码-代言人二维码页-已推荐扫码人数",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "未分组",
				"is_attention_in": "true",
				"remarks": "",
				"is_relation_member": "true",
				"relation_time": "2015-10-11 10:20:30",
				"cancel_related_time": "",
				"relation_member": "bill",
				"title": "星级代言人",
				"code_description": "星级代言人二维码描述",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}
			"""
		#"已关注会员可参与"的带参数二维码：未关注微信用户扫码关注，已推荐扫码人数增加
			#nokia扫码关注
			When 清空浏览器
			And nokia扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"
			And nokia访问jobs的webapp

			When 清空浏览器
			And bill访问jobs的webapp
			Then bill获得代言人二维码页
				"""
				{
					"member_name": "bill",
					"title": "星级代言人",
					"code_description": "星级代言人二维码描述",
					"recommended_number": 2
				}
				"""
		#"已关注会员可参与"的带参数二维码：已关注会员扫码，已推荐扫码人数增加
			#已关注会员jack扫码
			When 清空浏览器
			And jack关注jobs的公众号
			And jack访问jobs的webapp
			And jack扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"

			When 清空浏览器
			And bill访问jobs的webapp
			Then bill获得代言人二维码页
				"""
				{
					"member_name": "bill",
					"title": "星级代言人",
					"code_description": "星级代言人二维码描述",
					"recommended_number": 3
				}
				"""
		#"已关注会员可参与"的带参数二维码：取消关注会员扫码关注，已推荐扫码人数增加
			#取消关注会员marry扫码关注
			When 清空浏览器
			And marry关注jobs的公众号
			And marry访问jobs的webapp
			And marry取消关注jobs的公众号

			And marry扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"

			When 清空浏览器
			And bill访问jobs的webapp
			Then bill获得代言人二维码页
				"""
				{
					"member_name": "bill",
					"title": "星级代言人",
					"code_description": "星级代言人二维码描述",
					"recommended_number": 4
				}
				"""

	#扫码会员取消关注不影响已推荐扫码人数
		When 清空浏览器
		When marry取消关注jobs的公众号

		When 清空浏览器
		And bill访问jobs的webapp
		Then bill获得代言人二维码页
			"""
			{
				"member_name": "bill",
				"title": "星级代言人",
				"code_description": "星级代言人二维码描述",
				"recommended_number": 4
			}
			"""

@mall2 @senior @bandParameterCode
Scenario:3 带参数二维码[关联会员]-推荐详情页-[扫码人数][会员列表]
	Given jobs登录系统

	When bill关注jobs的公众号于'2015-10-11 00:00:00'
	When tom2关注jobs的公众号于'2015-10-12 00:00:00'

	#"已关注会员不可参与"的带参数二维码
		Given jobs登录系统
		When jobs添加带参数二维码
			"""
			[{
				"code_name": "带参数二维码-代言人二维码页-已推荐扫码人数",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "未分组",
				"is_attention_in": "false",
				"remarks": "",
				"is_relation_member": "true",
				"relation_time": "2015-10-11 10:20:30",
				"cancel_related_time": "",
				"relation_member": "bill",
				"title": "星级代言人",
				"code_description": "星级代言人二维码描述",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			},{
				"code_name": "带参数二维码-代言人二维码页-已推荐扫码人数22",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "未分组",
				"is_attention_in": "true",
				"remarks": "",
				"is_relation_member": "true",
				"relation_time": "2015-10-12 10:20:30",
				"cancel_related_time": "",
				"relation_member": "tom2",
				"title": "星级代言人",
				"code_description": "星级代言人二维码描述",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}]
			"""

		#"已关注会员不可参与"的带参数二维码：未关注微信用户扫码关注，已推荐扫码人数增加
			#tom扫码关注
			When 清空浏览器
			And tom扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"
			And tom访问jobs的webapp

			When 清空浏览器
			And bill访问jobs的webapp
			Then bill获得推荐详情页
				"""
				{
					"recommended_number": 1,
					"members":[{
						"member_name": "tom",
						"status": "已关注"
					}]
				}
				"""
		#"已关注会员不可参与"的带参数二维码：已关注会员扫码，已推荐扫码人数不增加
			#已关注会员jack扫码
			When 清空浏览器
			And jack关注jobs的公众号
			And jack访问jobs的webapp
			And jack扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"

			When 清空浏览器
			And bill访问jobs的webapp
			Then bill获得推荐详情页
				"""
				{
					"recommended_number": 1,
					"members":[{
						"member_name": "tom",
						"status": "已关注"
					}]
				}
				"""
		#"已关注会员不可参与"的带参数二维码：取消关注会员扫码关注，已推荐扫码人数不增加
			#取消关注会员marry扫码关注
			When 清空浏览器
			And marry关注jobs的公众号
			And marry访问jobs的webapp
			And marry取消关注jobs的公众号

			And marry扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"

			When 清空浏览器
			And bill访问jobs的webapp
			Then bill获得推荐详情页
				"""
				{
					"recommended_number": 1,
					"members":[{
						"member_name": "tom",
						"status": "已关注"
					}]
				}
				"""

	#"已关注会员可参与"的带参数二维码
		Given jobs登录系统
		When jobs更新带参数二维码'带参数二维码-代言人二维码页-已推荐扫码人数'
			"""
			{
				"code_name": "带参数二维码-代言人二维码页-已推荐扫码人数",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "未分组",
				"is_attention_in": "true",
				"remarks": "",
				"is_relation_member": "true",
				"relation_time": "2015-10-11 10:20:30",
				"cancel_related_time": "",
				"relation_member": "bill",
				"title": "星级代言人",
				"code_description": "星级代言人二维码描述",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}
			"""
		#"已关注会员可参与"的带参数二维码：未关注微信用户扫码关注，已推荐扫码人数增加
			#nokia扫码关注
			When 清空浏览器
			And nokia扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"
			And nokia访问jobs的webapp

			When 清空浏览器
			And bill访问jobs的webapp
			Then bill获得推荐详情页
				"""
				{
					"recommended_number": 2,
					"members":[{
						"member_name": "tom",
						"status": "已关注"
					},{
						"member_name": "nokia",
						"status": "已关注"
					}]
				}
				"""
		#"已关注会员可参与"的带参数二维码：已关注会员扫码，已推荐扫码人数增加
			#已关注会员jack扫码
			When 清空浏览器
			And jack关注jobs的公众号
			And jack访问jobs的webapp
			And jack扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"

			When 清空浏览器
			And bill访问jobs的webapp
			Then bill获得推荐详情页
				"""
				{
					"recommended_number": 3,
					"members":[{
						"member_name": "tom",
						"status": "已关注"
					},{
						"member_name": "nokia",
						"status": "已关注"
					},{
						"member_name": "jack",
						"status": "已关注"
					}]
				}
				"""
		#"已关注会员可参与"的带参数二维码：取消关注会员扫码关注，已推荐扫码人数增加
			#取消关注会员marry扫码关注
			When 清空浏览器
			And marry关注jobs的公众号
			And marry访问jobs的webapp
			And marry取消关注jobs的公众号

			And marry扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"

			When 清空浏览器
			And bill访问jobs的webapp
			Then bill获得推荐详情页
				"""
				{
					"recommended_number": 4,
					"members":[{
						"member_name": "tom",
						"status": "已关注"
					},{
						"member_name": "nokia",
						"status": "已关注"
					},{
						"member_name": "jack",
						"status": "已关注"
					},{
						"member_name": "marry",
						"status": "已关注"
					}]
				}
				"""

	#扫码会员取消关注不影响扫码人数和会员列表
		When 清空浏览器
		When marry取消关注jobs的公众号

		When 清空浏览器
		And bill访问jobs的webapp
		Then bill获得推荐详情页
			"""
			{
				"recommended_number": 4,
				"members":[{
					"member_name": "tom",
					"status": "已关注"
				},{
					"member_name": "nokia",
					"status": "已关注"
				},{
					"member_name": "jack",
					"status": "已关注"
				},{
					"member_name": "marry",
					"status": "已跑路"
				}]
			}
			"""

	#"已关注会员可参与"同一微信账号交替扫不同的码[扫码人数][会员列表]跳转
		When 清空浏览器
		When marry扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数22"

		When 清空浏览器
		And bill访问jobs的webapp
		Then bill获得推荐详情页
			"""
			{
				"recommended_number": 3,
				"members":[{
						"member_name": "tom",
						"status": "已关注"
					},{
						"member_name": "nokia",
						"status": "已关注"
					},{
						"member_name": "jack",
						"status": "已关注"
					}]
			}
			"""
		When 清空浏览器
		And tom2访问jobs的webapp
		Then tom2获得推荐详情页
			"""
			{
				"recommended_number": 1,
				"members":[{
					"member_name": "marry",
					"status": "已关注"
				}]
			}
			"""

@mall2 @senior @bandParameterCode @gyct
Scenario:4 带参数二维码[关联会员]-推荐详情页-[下单人数][成交金额]
	Given jobs登录系统

	#添加基础数据
		And jobs设定会员积分策略
			"""
			{
				"be_member_increase_count":200,
				"use_ceiling": 50,
				"use_condition":"on",
				"integral_each_yuan":1
			}
			"""
		When jobs添加支付方式
			"""
			[{
				"type": "货到付款",
				"description": "我的货到付款",
				"is_active": "启用"
			},{
				"type": "微信支付",
				"description": "我的微信支付",
				"is_active": "启用"
			},{
				"type": "支付宝",
				"description": "我的支付宝支付",
				"is_active": "启用"
			}]
			"""
		And jobs开通使用微众卡权限
		And jobs添加支付方式
			"""
			[{
				"type": "微众卡支付",
				"description": "我的微众卡支付",
				"is_active": "启用"
			}]
			"""
		Given jobs已创建微众卡
			"""
			{
				"cards":[{
					"id":"0000001",
					"password":"1234567",
					"status":"未使用",
					"price":100.00
				},{
					"id":"0000002",
					"password":"1234567",
					"status":"未使用",
					"price":90.00
				},{
					"id":"0000003",
					"password":"1234567",
					"status":"未使用",
					"price":100.00
				}]
			}
			"""

		When jobs添加商品规格
			"""
			[{
				"name": "颜色",
				"type": "文字",
				"values": [{
					"name": "黑色"
				},{
					"name": "白色"
				}]
			},{
				"name": "尺寸",
				"type": "文字",
				"values": [{
					"name": "M"
				},{
					"name": "S"
				}]
			}]
			"""
		And jobs已添加商品
			"""
			[{
				"name": "商品1",
				"postage": 10,
				"price": 100.00,
				"weight": 5.0,
				"stock_type": "无限"
			},{
				"name": "商品2",
				"postage": 15,
				"is_enable_model": "启用规格",
				"model": {
					"models": {
						"黑色 M": {
							"price": 100.00,
							"weight": 5.0,
							"stock_type": "无限"
						},
						"白色 S": {
							"price": 100.00,
							"weight": 5.0,
							"stock_type": "无限"
						}
					}
				}
			},{
				"name": "商品3",
				"price": 10.00,
				"postage": 0.00
			}]
			"""

		And jobs添加优惠券规则
			"""
			[{
				"name": "全体券1",
				"money": 10,
				"start_date": "2015-01-01",
				"end_date": "10天后",
				"coupon_id_prefix": "coupon1_id_"
			}]
			"""

		When nokia关注jobs的公众号于'2015-05-09 10:00:00'
		When tom2关注jobs的公众号于'2015-05-09 10:00:00'
		When bill关注jobs的公众号于'2015-05-10 10:00:00'
		And tom关注jobs的公众号于'2015-05-11 10:00:00'
		And tom取消关注jobs的公众号

	Given jobs登录系统
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-代言人二维码页-已推荐扫码人数",
			"create_time": "2015-10-10 10:20:30",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "true",
			"remarks": "",
			"is_relation_member": "true",
			"relation_time": "2015-10-11 10:20:30",
			"cancel_related_time": "",
			"relation_member": "nokia",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		},{
			"code_name": "带参数二维码-代言人二维码页-已推荐扫码人数22",
			"create_time": "2015-10-10 10:20:30",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "true",
			"remarks": "",
			"is_relation_member": "true",
			"relation_time": "2015-10-11 10:20:30",
			"cancel_related_time": "",
			"relation_member": "tom2",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		}]
		"""

	#扫码关注成为会员
		When 清空浏览器
		And jack扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"于2015-10-20 10:00:00
		And jack访问jobs的webapp

		When 清空浏览器
		And marry扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"于2015-10-21 10:00:00
		And marry访问jobs的webapp

	#已关注或者取消关注的会员，扫码
		When 清空浏览器
		When bill扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"于2015-10-22 10:00:00

		When 清空浏览器
		And tom扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数"

	#会员购买
		When 微信用户批量消费jobs的商品
			| order_id |    date    | payment_time | consumer |    product     | payment | pay_type  |postage*|price*|integral |       coupon         | paid_amount* |  weizoom_card     | alipay* | wechat* | cash* |   action      | order_status* |
			|   0001   | 2015-06-07 |              |   bill   | 商品1,1        |         |  支付宝   |   10   | 100  |   0     |                      |     110      |                   |    0    |    0    |   0   |               |    待支付     |
			|   0002   | 2015-06-08 |              |   tom    | 商品1,1        |         |  支付宝   |   10   | 100  |   0     |                      |     110      |                   |    0    |    0    |   0   |  jobs,取消    |    已取消     |
			|   0003   | 2015-06-09 |  2014-06-10  |   tom    | 商品2,黑色 M,2 |   支付  |  微信支付 |   15   | 100  |   0     | 全体券1,coupon1_id_1 |     205      |                   |    0    |   205   |   0   |  jobs,发货    |    已发货     |
			|   0004   | 2天前      |     2天前    |   bill   | 商品1,1        |   支付  |  支付宝   |   10   | 100  |  50     |                      |     60       |                   |   60    |    0    |   0   |  jobs,退款    |    退款中     |
			|   0005   | 2天前      |     2天前    |   tom    | 商品1,1        |   支付  |  支付宝   |   10   | 100  |  50     |                      |     60       |                   |   60    |    0    |   0   |  jobs,完成退款|   退款成功    |
			|   0006   | 今天       |     今天     |  marry   | 商品1,1        |   支付  |  支付宝   |   10   | 100  |  50     |                      |     60       |                   |   60    |    0    |   0   |               |    待发货     |
			|   0007   | 今天       |     今天     |  jack    | 商品1,1        |   支付  |  货到付款 |   10   | 100  |   0     |                      |     110      |                   |    0    |    0    |   110 |               |    待发货     |
			|   0008   | 今天       |     今天     |  marry   | 商品2,白色 S,1 |   支付  |  货到付款 |   15   | 100  |   0     | 全体券1,coupon1_id_2 |     105      |  0000002,1234567  |    0    |    0    |   15  |  jobs,取消    |    已取消     |
			|   0009   | 今天       |     今天     |  jack    | 商品3,1        |   支付  |  微信支付 |   0    | 10   |   0     | 全体券1,coupon1_id_3 |     0        |                   |    0    |    0    |   0   |  jobs,发货    |    已发货     |
			|   0010   | 今天       |     今天     |   bill   | 商品2,白色 S,1 |   支付  |  货到付款 |   15   | 100  |   0     | 全体券1,coupon1_id_4 |     105      |  0000001,1234567  |    0    |    0    |   5   |  jobs,完成    |    已完成     |
			|   0011   | 今天       |     今天     |   tom    | 商品2,白色 S,1 |   支付  |  微信支付 |   15   | 100  |   0     |                      |     115      |  0000003,1234567  |    0    |    0    |   15  |  jobs,退款    |    退款中     |

	#校验推荐详情页-[下单人数][成交金额]
		When 清空浏览器
		And nokia访问jobs的webapp
		Then nokia获得推荐详情页
			"""
			{
				"pay_member_number": 2,
				"order_money": 275.00
			}
			"""
	#"已关注会员可参与"同一微信账号交替扫不同的码[下单人数][成交金额]跳转
		When 清空浏览器
		When jack扫描带参数二维码"带参数二维码-代言人二维码页-已推荐扫码人数22"于2015-10-23 10:00:00

		When 清空浏览器
		And nokia访问jobs的webapp
		Then nokia获得推荐详情页
			"""
			{
				"pay_member_number": 1,
				"order_money": 165.00
			}
			"""

		When 清空浏览器
		And tom2访问jobs的webapp
		Then tom2获得推荐详情页
			"""
			{
				"pay_member_number": 1,
				"order_money": 110.00
			}
			"""
