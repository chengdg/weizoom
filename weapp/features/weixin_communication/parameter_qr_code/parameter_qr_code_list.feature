#author: 王丽 2015-10-27

Feature:带参数二维码-列表查询和导出
"""
	带参数二维码列表
	1 【二维码名称】：带参数二维码的名称
	2 【关注数量】：通过扫码关注会员的数量；
					(1)扫码新增会员数量（【已关注会员可参与】设置为"否"）
					(2)扫码新增会员数量+之前关注过的会员(包含当前为"关注"状态或者"取消关注"状态)
					扫码的会员数量（【已关注会员可参与】设置为"是"）

	3 【扫码后成交金额】:关注此二维码的会员的订单的"下单时间"在此会员的"扫码时间"之后的，
						所有有效订单（待发货、已发货、已完成）的实付金额之和

	4 【扫码奖励】：设置的扫此二位码获得的奖励
					(1)【扫码奖励】设置为"无奖励"：无奖励
					(2)【扫码奖励】设置为"积分"10：[积分]10
					(3)【扫码奖励】设置为"优惠券"优惠券名称：[优惠券]优惠券名称

	5 【创建时间】：此二维码规则的创建时间，精确到秒；默认按照创建时间倒叙排列
	6 【备注】：文本备注
	7 【关联会员】：设置的"关联会员"的会员名称；
					(1)点击会员名称，跳转到此会员的会员详情页
					(2)鼠标移动到会员名称上显示："关联时间"和"取消关联时间",精确到秒（多次关联和取消关联的，显示最后一次的时间）；
	8 【操作】：显示"查看二维码"；点击新页面打开此二维码的二维码图片

	9 带参数二维码列表的"查询"，可以按照带参数二维码的名称进行模糊匹配查询，查询条件为空时，查询全部

	10 带参数二维码列表的"分页"，每20条记录一页

	11 带参数二维码列表的"导出"，导出当前查询结果的所有记录，不受分页影响
"""

Background:
	Given jobs登录系统

	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	And jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		},{
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		},{
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	And jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2"
		}
		"""
	And jobs已添加多图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
				}],
			"cover_in_the_text":"true",
			"content":"单条图文1文本内容"
		},{
			"title":"sub图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
				}],
			"cover_in_the_text":"true",
			"content":"sub单条图文1文本内容"
		},{
			"title":"sub图文2",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
			"cover_in_the_text":"false",
			"content":"sub单条图文2文本内容"
		},{
			"title":"sub图文3",
			"cover": [{
				"url": "/standard_static/test_resource_img/wufan1.jpg"
				}],
			"cover_in_the_text":"false",
			"jump_url":"www.baidu.com",
			"content":"sub单条图文3文本内容"
		}]
		"""

	And bill关注jobs的公众号于'2015-10-01 10:00:00'
	And tom关注jobs的公众号于'2015-10-02'

	#添加默认条件：无奖励、普通会员、未分组、否、无备注、否、扫码后回复文本
	#添加：积分奖励、金牌会员、分组1、是、带参数二维码备注、是、扫码后回复图文
			#（设置了关联会员后又取消设置关联会员）
	#添加：优惠券奖励、金牌会员、分组1、是、带参数二维码备注、是、扫码后回复图文（设置了关联会员）
	Given jobs登录系统
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-默认设置",
			"create_time": "2015-10-10 10:20:30",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		},{
			"code_name": "带参数二维码-积分奖励",
			"create_time": "2015-10-11 10:20:30",
			"prize_type": "积分",
			"integral": 10,
			"member_rank": "金牌会员",
			"tags": "分组1",
			"is_attention_in": "true",
			"remarks": "带参数二维码备注",
			"is_relation_member": "true",
			"relation_time": "2015-10-13 08:00:00",
			"relation_member": "bill",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "图文",
			"scan_code_reply": "图文1"
		},{
			"code_name": "带参数二维码-优惠券奖励",
			"create_time": "今天",
			"prize_type": "优惠券",
			"coupon":"优惠券1",
			"member_rank": "金牌会员",
			"tags": "分组1",
			"is_attention_in": "true",
			"remarks": "带参数二维码备注",
			"is_relation_member": "true",
			"relation_time": "今天",
			"relation_member": "tom",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "图文",
			"scan_code_reply": "图文1"
		}]
		"""
	#实现"取消关联时间"的数据
		#更新二维码，关联会员修改为"否"
		When jobs更新带参数二维码'带参数二维码-积分奖励'
			"""
			{
				"code_name": "带参数二维码-积分奖励",
				"create_time": "2015-10-11 10:20:30",
				"prize_type": "积分",
				"integral": 10,
				"member_rank": "金牌会员",
				"tags": "分组1",
				"is_attention_in": "true",
				"remarks": "带参数二维码备注",
				"is_relation_member": "false",
				"relation_time": "2015-10-13 08:00:00",
				"relation_member": "bill",
				"title": "星级代言人",
				"code_description": "星级代言人二维码描述",
				"reply_type": "图文",
				"scan_code_reply": "图文1"
			}
			"""

@mall2 @senior @bandParameterCode
Scenario:1 带参数二维码的查询
	Given jobs登录系统

	#空查询
		When jobs设置带参数二维码查询条件
			"""
			{
				"code_name": ""
			}
			"""
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-优惠券奖励",
				"attention_number": 0,
				"order_money": 0.00,
				"prize": "[优惠券]优惠券1",
				"create_time": "今天",
				"remarks": "带参数二维码备注",
				"relation_member": "tom",
				"relation_time": "今天",
				"cancel_related_time": ""
			},{
				"code_name": "带参数二维码-积分奖励",
				"attention_number": 0,
				"order_money": 0.00,
				"prize": "[积分]10",
				"create_time": "2015-10-11 10:20:30",
				"remarks": "带参数二维码备注",
				"relation_member": "bill",
				"relation_time": "2015-10-13 08:00:00",
				"cancel_related_time": "今天"
			},{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 0,
				"order_money": 0.00,
				"prize": "无奖励",
				"create_time": "2015-10-10 10:20:30",
				"remarks": "",
				"relation_member": "",
				"relation_time": "",
				"cancel_related_time": ""
			}]
			"""

	#模糊匹配查询
		When jobs设置带参数二维码查询条件
			"""
			{
				"code_name": "积分"
			}
			"""
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-积分奖励",
				"attention_number": 0,
				"order_money": 0.00,
				"prize": "[积分]10",
				"create_time": "2015-10-11 10:20:30",
				"remarks": "带参数二维码备注",
				"relation_member": "bill",
				"relation_time": "2015-10-13 08:00:00",
				"cancel_related_time": "今天"
			}]
			"""

	#精确匹配查询
		When jobs设置带参数二维码查询条件
			"""
			{
				"code_name": "带参数二维码-优惠券奖励"
			}
			"""
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-优惠券奖励",
				"attention_number": 0,
				"order_money": 0.00,
				"prize": "[优惠券]优惠券1",
				"create_time": "今天",
				"remarks": "带参数二维码备注",
				"relation_member": "tom",
				"relation_time": "今天",
				"cancel_related_time": ""
			}]
			"""

	#无查询结果查询
		When jobs设置带参数二维码查询条件
			"""
			{
				"code_name": "我们"
			}
			"""
		Then jobs获得带参数二维码列表
			"""
			[]
			"""

@mall2 @senior @bandParameterCode
Scenario:2 带参数二维码的分页
	Given jobs登录系统

	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""
	#Then jobs获得带参数二维码列表共'3'页

	When jobs访问带参数二维码列表第'1'页
	Then jobs获得带参数二维码列表
		"""
		[{
			"code_name": "带参数二维码-优惠券奖励",
			"attention_number": 0,
			"order_money": 0.00,
			"prize": "[优惠券]优惠券1",
			"create_time": "今天",
			"remarks": "带参数二维码备注",
			"relation_member": "tom",
			"relation_time": "今天",
			"cancel_related_time": ""
		}]
		"""
	When jobs访问带参数二维码列表下一页
	Then jobs获得带参数二维码列表
		"""
		[{
			"code_name": "带参数二维码-积分奖励",
			"attention_number": 0,
			"order_money": 0.00,
			"prize": "[积分]10",
			"create_time": "2015-10-11 10:20:30",
			"remarks": "带参数二维码备注",
			"relation_member": "bill",
			"relation_time": "2015-10-13 08:00:00",
			"cancel_related_time": "今天"
		}]
		"""
	When jobs访问带参数二维码列表第'3'页
	Then jobs获得带参数二维码列表
		"""
		[{
			"code_name": "带参数二维码-默认设置",
			"attention_number": 0,
			"order_money": 0.00,
			"prize": "无奖励",
			"create_time": "2015-10-10 10:20:30",
			"remarks": "",
			"relation_member": "",
			"relation_time": "",
			"cancel_related_time": ""
		}]
		"""
	When jobs访问带参数二维码列表上一页
	Then jobs获得带参数二维码列表
		"""
		[{
			"code_name": "带参数二维码-积分奖励",
			"attention_number": 0,
			"order_money": 0.00,
			"prize": "[积分]10",
			"create_time": "2015-10-11 10:20:30",
			"remarks": "带参数二维码备注",
			"relation_member": "bill",
			"relation_time": "2015-10-13 08:00:00",
			"cancel_related_time": "今天"
		}]
		"""

@mall2 @senior @bandParameterCode
Scenario:3 带参数二维码的导出
	Given jobs登录系统

	#在多页数据下导出结果，定位到第一页，导出结果为所有页数据
		And jobs设置分页查询参数
			"""
			{
				"count_per_page":1
			}
			"""
		#Then jobs获得带参数二维码列表共'3'页

		When jobs访问带参数二维码列表第'1'页
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-优惠券奖励",
				"attention_number": 0,
				"order_money": 0.00,
				"prize": "[优惠券]优惠券1",
				"create_time": "今天",
				"remarks": "带参数二维码备注",
				"relation_member": "tom",
				"relation_time": "今天",
				"cancel_related_time": ""
			}]
			"""

		When jobs导出带参数二维码列表
		Then jobs获得带参数二维码列表导出结果
			"""
			[{
				"code_name": "带参数二维码-优惠券奖励",
				"attention_number": 0,
				"total_final_price": 0.00,
				"cash_money": 0.00,
				"weizoom_card_money": 0.00,
				"prize": "[优惠券]优惠券1",
				"create_time": "今天"
			},{
				"code_name": "带参数二维码-积分奖励",
				"attention_number": 0,
				"total_final_price": 0.00,
				"cash_money": 0.0,
				"weizoom_card_money": 0.00,
				"prize": "[积分]10",
				"create_time": "2015-10-11 10:20:30"
			},{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 0,
				"total_final_price": 0.00,
				"cash_money": 0.00,
				"weizoom_card_money": 0.00,
				"prize": "无奖励",
				"create_time": "2015-10-10 10:20:30"
			}]
			"""


	#在查询结果下导出数据，导出结果为查询结果
		When jobs设置带参数二维码查询条件
			"""
			{
				"code_name": "优惠券奖励"
			}
			"""

		When jobs导出带参数二维码列表
		Then jobs获得带参数二维码列表导出结果
			"""
			[{
				"code_name": "带参数二维码-优惠券奖励",
				"attention_number": 0,
				"total_final_price": 0.00,
				"cash_money": 0.00,
				"weizoom_card_money": 0.00,
				"prize": "[优惠券]优惠券1",
				"create_time": "今天"
			}]
			"""
