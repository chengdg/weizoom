#author: 王丽 2015-10-27

Feature:带参数二维码-[关注数量]关注会员列表
"""
	带参数二维码-[关注会员]列表
	1 【关注数量】：通过扫码关注会员的数量；
					(1)扫码新增会员数量（【已关注会员可参与】设置为"否"）
					(2)扫码新增会员数量+之前关注过的会员(包含当前为"关注"状态或者"取消关注"状态)
					扫码的会员数量（【已关注会员可参与】设置为"是"）
					(3)"已关注会员可参与"同一微信账号重复扫码[关注数量]累计一次
					(4)"已关注会员可参与"同一微信账号交替扫不同的码[关注数量]跳转
	2 【会员】：会员名称和头像；会员名称和头像可以跳转链接到会员详情页
	3 【购买次数】：此会员的在系统中有效订单（待发货、已发货、已完成）的数量；可以点击排序
	4 【积分】：此会员在系统中的积分数；可以点击排序
	5 【消费总额】：此会员的在系统中有效订单（待发货、已发货、已完成）的实付金额之和；可以点击排序
	6 【会员等级】：此会员的会员等级
	7 【关注时间】：此会员进入系统的时间（精确到秒）；默认按此字段倒叙排列；可以点击排序
	8 支持分页显示，每页50条记录

	查询条件
	9 【关注时间】：精确到秒
					(1)开始时间为空，结束时间为空；查询出所有
					(2)开始时间为空，结束时间不为空；查询结束时间之前所有
					(3)开始时间不为空，结束时间为空；查询开始时间之后所有
					(4)开始时间不为空，结束时间不为空；查询区间内所有
	10 【仅显示通过二维码新关注会员】：勾选或者不勾选；默认勾选；即通过扫码新关注的会员
"""
Background:
	Given jobs登录系统

	#添加基础数据
		And jobs设定会员积分策略
			"""
			{
				"be_member_increase_count":20
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
		And jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2"
		}
		"""
		And jobs已添加商品
			"""
			[{
				"name": "商品1",
				"price": 100.00,
				"postage": 10
			},{
				"name": "商品2",
				"price": 100.00,
				"postage": 15
			}]
			"""

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

		When jobs添加带参数二维码
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"create_time": "2015-08-10 10:00:00",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "未分组",
				"is_attention_in": "true",
				"remarks": "",
				"is_relation_member": "false",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			},{
				"code_name": "带参数二维码-第二个二维码",
				"create_time": "今天",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "未分组",
				"is_attention_in": "true",
				"remarks": "",
				"is_relation_member": "false",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}]
			"""

		When bill关注jobs的公众号于'2015-05-10 00:00:00'
		And tom关注jobs的公众号于'2015-05-11 00:00:00'
		And tom取消关注jobs的公众号

	#扫码关注成为会员
		When 清空浏览器
		And jack扫描带参数二维码"带参数二维码-默认设置"于2015-08-11 10:00:00
		And jack访问jobs的webapp

		When 清空浏览器
		And nokia扫描带参数二维码"带参数二维码-默认设置"于2015-08-12 10:00:00
		And nokia访问jobs的webapp

		When 清空浏览器
		And marry扫描带参数二维码"带参数二维码-默认设置"于2015-08-13 10:00:00
		And marry访问jobs的webapp

	#已关注或者取消关注的会员，扫码
		When bill扫描带参数二维码"带参数二维码-默认设置"于2015-08-14 10:00:00

		And tom扫描带参数二维码"带参数二维码-默认设置"于2015-08-15 10:00:00

	#会员购买
		When 微信用户批量消费jobs的商品
			| order_id |    date    | consumer | product | payment | pay_type  |postage*|price*| paid_amount* |  action      | order_status* |
			|   0001   | 2015-06-01 |   bill   | 商品1,1 |         |  支付宝   |   10   | 100  |     110      |              |    待支付     |
			|   0002   | 2015-06-02 |   bill   | 商品1,1 |         |  支付宝   |   10   | 100  |     110      | jobs,取消    |    已取消     |
			|   0003   | 2015-06-03 |   bill   | 商品2,2 |   支付  |  微信支付 |   15   | 100  |     215      | jobs,发货    |    已发货     |
			|   0004   | 2015-06-04 |   bill   | 商品2,1 |   支付  |  货到付款 |   15   | 100  |     115      | jobs,完成    |    已完成     |
			|   0005   | 2015-06-05 |   bill   | 商品1,1 |   支付  |  支付宝   |   10   | 100  |     110      | jobs,退款    |    退款中     |
			|   0006   | 今天       |  marry   | 商品1,1 |   支付  |  支付宝   |   10   | 100  |     110      | jobs,完成退款|   退款成功    |
			|   0007   | 今天       |   jack   | 商品1,1 |   支付  |  货到付款 |   10   | 100  |     110      |              |    待发货     |
			|   0008   | 今天       |   tom    | 商品1,1 |   支付  |  支付宝   |   10   | 100  |     110      |              |    待发货     |
			|   0009   | 今天       |   tom    | 商品2,1 |   支付  |  货到付款 |   15   | 100  |     115      | jobs,取消    |    已取消     |
			|   0010   | 今天       |   tom    | 商品2,1 |   支付  |  货到付款 |   15   | 100  |     115      | jobs,发货    |    已发货     |

@mall2 @senior @bandParameterCode
Scenario:1 带参数二维码-[关注数量]关注会员列表查询-默认条件
	Given jobs登录系统

	#关注会员列表，默认查询"仅显示通过二维码新关注会员",按照"关注时间"倒叙排列
	Then jobs获得'带参数二维码-默认设置'关注会员列表
		"""
		[{
			"member_name": "marry",
			"status": "已关注",
			"pay_times": 1,
			"integral": 20,
			"pay_money": 110.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-13 10:00:00"
		},{
			"member_name": "nokia",
			"status": "已关注",
			"pay_times": 0,
			"integral": 20,
			"pay_money": 0.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-12 10:00:00"
		},{
			"member_name": "jack",
			"status": "已关注",
			"pay_times": 1,
			"integral": 20,
			"pay_money": 110.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-11 10:00:00"
		}]
		"""

@mall2 @senior @bandParameterCode
Scenario:2 带参数二维码-[关注数量]关注会员列表查询-仅显示通过二维码新关注会员
	Given jobs登录系统

	When jobs设置带参数二维码关注会员查询条件
		"""
		{
			"start_time": "",
			"end_time": "",
			"is_new_attention_member": "false"
		}
		"""
	Then jobs获得'带参数二维码-默认设置'关注会员列表
		"""
		[{
			"member_name": "marry",
			"status": "已关注",
			"pay_times": 1,
			"integral": 20,
			"pay_money": 110.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-13 10:00:00"
		},{
			"member_name": "nokia",
			"status": "已关注",
			"pay_times": 0,
			"integral": 20,
			"pay_money": 0.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-12 10:00:00"
		},{
			"member_name": "jack",
			"status": "已关注",
			"pay_times": 1,
			"integral": 20,
			"pay_money": 110.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-11 10:00:00"
		},{
			"member_name": "tom",
			"status": "已关注",
			"pay_times": 2,
			"integral": 20,
			"pay_money": 225.00,
			"member_rank": "普通会员",
			"attention_time": "2015-05-11 00:00:00"
		},{
			"member_name": "bill",
			"status": "已关注",
			"pay_times": 3,
			"integral": 20,
			"pay_money": 440.00,
			"member_rank": "普通会员",
			"attention_time": "2015-05-10 00:00:00"
		}]
		"""

	When jobs设置带参数二维码关注会员查询条件
		"""
		{
			"start_time": "",
			"end_time": "",
			"is_new_attention_member": "true"
		}
		"""
	Then jobs获得'带参数二维码-默认设置'关注会员列表
		"""
		[{
			"member_name": "marry",
			"status": "已关注",
			"pay_times": 1,
			"integral": 20,
			"pay_money": 110.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-13 10:00:00"
		},{
			"member_name": "nokia",
			"status": "已关注",
			"pay_times": 0,
			"integral": 20,
			"pay_money": 0.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-12 10:00:00"
		},{
			"member_name": "jack",
			"status": "已关注",
			"pay_times": 1,
			"integral": 20,
			"pay_money": 110.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-11 10:00:00"
		}]
		"""

@mall2 @senior @bandParameterCode
Scenario:3 带参数二维码-[关注数量]关注会员列表查询-关注时间
	Given jobs登录系统

	#关注时间：开始时间为空，结束时间为空
		When jobs设置带参数二维码关注会员查询条件
			"""
			{
				"start_time": "",
				"end_time": "",
				"is_new_attention_member": "true"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'关注会员列表
			"""
			[{
				"member_name": "marry",
				"status": "已关注",
				"pay_times": 1,
				"integral": 20,
				"pay_money": 110.00,
				"member_rank": "普通会员",
				"attention_time": "2015-08-13 10:00:00"
			},{
				"member_name": "nokia",
				"status": "已关注",
				"pay_times": 0,
				"integral": 20,
				"pay_money": 0.00,
				"member_rank": "普通会员",
				"attention_time": "2015-08-12 10:00:00"
			},{
				"member_name": "jack",
				"status": "已关注",
				"pay_times": 1,
				"integral": 20,
				"pay_money": 110.00,
				"member_rank": "普通会员",
				"attention_time": "2015-08-11 10:00:00"
			}]
			"""

	#关注时间：开始时间为空，结束时间不为空
		When jobs设置带参数二维码关注会员查询条件
			"""
			{
				"start_time": "",
				"end_time": "2015-05-11 00:00:00",
				"is_new_attention_member": "false"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'关注会员列表
			"""
			[{
				"member_name": "tom",
				"status": "已关注",
				"pay_times": 2,
				"integral": 20,
				"pay_money": 225.00,
				"member_rank": "普通会员",
				"attention_time": "2015-05-11 00:00:00"
			},{
				"member_name": "bill",
				"status": "已关注",
				"pay_times": 3,
				"integral": 20,
				"pay_money": 440.00,
				"member_rank": "普通会员",
				"attention_time": "2015-05-10 00:00:00"
			}]
			"""

	#关注时间：开始时间不为空，结束时间为空
		When jobs设置带参数二维码关注会员查询条件
			"""
			{
				"start_time": "2015-05-11 00:00:00",
				"end_time": "",
				"is_new_attention_member": "false"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'关注会员列表
			"""
			[{
				"member_name": "marry",
				"status": "已关注",
				"pay_times": 1,
				"integral": 20,
				"pay_money": 110.00,
				"member_rank": "普通会员",
				"attention_time": "2015-08-13 10:00:00"
			},{
				"member_name": "nokia",
				"status": "已关注",
				"pay_times": 0,
				"integral": 20,
				"pay_money": 0.00,
				"member_rank": "普通会员",
				"attention_time": "2015-08-12 10:00:00"
			},{
				"member_name": "jack",
				"status": "已关注",
				"pay_times": 1,
				"integral": 20,
				"pay_money": 110.00,
				"member_rank": "普通会员",
				"attention_time": "2015-08-11 10:00:00"
			},{
				"member_name": "tom",
				"status": "已关注",
				"pay_times": 2,
				"integral": 20,
				"pay_money": 225.00,
				"member_rank": "普通会员",
				"attention_time": "2015-05-11 00:00:00"
			}]
			"""

	#关注时间段查询
		When jobs设置带参数二维码关注会员查询条件
			"""
			{
				"start_time": "2015-05-10 9:10:00",
				"end_time": "2015-05-11 19:10:00",
				"is_new_attention_member": "false"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'关注会员列表
			"""
			[{
				"member_name": "tom",
				"status": "已关注",
				"pay_times": 2,
				"integral": 20,
				"pay_money": 225.00,
				"member_rank": "普通会员",
				"attention_time": "2015-05-11 00:00:00"
			}]
			"""

	#关注时间开始和结束时间一样
		When jobs设置带参数二维码关注会员查询条件
			"""
			{
				"start_time": "2015-08-11 10:00:00",
				"end_time": "2015-08-11 10:00:00",
				"is_new_attention_member": "true"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'关注会员列表
			"""
			[{
				"member_name": "jack",
				"status": "已关注",
				"pay_times": 1,
				"integral": 20,
				"pay_money": 110.00,
				"member_rank": "普通会员",
				"attention_time": "2015-08-11 10:00:00"
			}]
			"""

	#查询结果为空
		When jobs设置带参数二维码关注会员查询条件
			"""
			{
				"start_time": "3天前",
				"end_time": "2天前",
				"is_new_attention_member": "true"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'关注会员列表
			"""
			[]
			"""

@mall2 @senior @bandParameterCode
Scenario:4 带参数二维码-[关注数量]关注会员列表查询-分页
	Given jobs登录系统

	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""
	When jobs设置带参数二维码关注会员查询条件
		"""
		{
			"start_time": "",
			"end_time": "",
			"is_new_attention_member": "true"
		}
		"""

	#Then jobs获得带'带参数二维码-默认设置'会员列表共'3'页

	When jobs访问'带参数二维码-默认设置'关注会员列表第'1'页
	Then jobs获得'带参数二维码-默认设置'关注会员列表
		"""
		[{
			"member_name": "marry",
			"status": "已关注",
			"pay_times": 1,
			"integral": 20,
			"pay_money": 110.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-13 10:00:00"
		}]
		"""
	When jobs访问'带参数二维码-默认设置'关注会员列表下一页
	Then jobs获得'带参数二维码-默认设置'关注会员列表
		"""
		[{
			"member_name": "nokia",
			"status": "已关注",
			"pay_times": 0,
			"integral": 20,
			"pay_money": 0.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-12 10:00:00"
		}]
		"""
	When jobs访问'带参数二维码-默认设置'关注会员列表第'3'页
	Then jobs获得'带参数二维码-默认设置'关注会员列表
		"""
		[{
			"member_name": "jack",
			"status": "已关注",
			"pay_times": 1,
			"integral": 20,
			"pay_money": 110.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-11 10:00:00"
		}]
		"""
	When jobs访问'带参数二维码-默认设置'关注会员列表上一页
	Then jobs获得'带参数二维码-默认设置'关注会员列表
		"""
		[{
			"member_name": "nokia",
			"status": "已关注",
			"pay_times": 0,
			"integral": 20,
			"pay_money": 0.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-12 10:00:00"
		}]
		"""

@mall2 @senior @bandParameterCode
Scenario:5 带参数二维码[关注数量]关注会员列表查询-扫码会员取消关注不影响关注会员列表
	#"已关注会员不可参与"的带参数二维码，会员扫码之后，关注数量增加，
	#扫码会员取消关注不影响[关注数量]，关注数量不减少

	Given jobs登录系统

	When bill取消关注jobs的公众号

	Given jobs登录系统
	When jobs设置带参数二维码关注会员查询条件
		"""
		{
			"start_time": "",
			"end_time": "",
			"is_new_attention_member": "false"
		}
		"""
	Then jobs获得'带参数二维码-默认设置'关注会员列表
		"""
		[{
			"member_name": "marry",
			"status": "已关注",
			"pay_times": 1,
			"integral": 20,
			"pay_money": 110.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-13 10:00:00"
		},{
			"member_name": "nokia",
			"status": "已关注",
			"pay_times": 0,
			"integral": 20,
			"pay_money": 0.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-12 10:00:00"
		},{
			"member_name": "jack",
			"status": "已关注",
			"pay_times": 1,
			"integral": 20,
			"pay_money": 110.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-11 10:00:00"
		},{
			"member_name": "tom",
			"status": "已关注",
			"pay_times": 2,
			"integral": 20,
			"pay_money": 225.00,
			"member_rank": "普通会员",
			"attention_time": "2015-05-11 00:00:00"
		},{
			"member_name": "bill",
			"status": "取消关注",
			"pay_times": 3,
			"integral": 20,
			"pay_money": 440.00,
			"member_rank": "普通会员",
			"attention_time": "2015-05-10 00:00:00"
		}]
		"""

@mall2 @senior @bandParameterCode
Scenario:6 带参数二维码[关注数量]关注会员列表查询-"已关注会员可参与"同一微信账号交替扫不同的码[关注数量]关注会员列表跳转
	Given jobs登录系统

	When 清空浏览器
	When bill扫描带参数二维码"带参数二维码-第二个二维码"

	Given jobs登录系统
	When jobs设置带参数二维码关注会员查询条件
		"""
		{
			"start_time": "",
			"end_time": "",
			"is_new_attention_member": "false"
		}
		"""
	Then jobs获得'带参数二维码-默认设置'关注会员列表
		"""
		[{
			"member_name": "marry",
			"status": "已关注",
			"pay_times": 1,
			"integral": 20,
			"pay_money": 110.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-13 10:00:00"
		},{
			"member_name": "nokia",
			"status": "已关注",
			"pay_times": 0,
			"integral": 20,
			"pay_money": 0.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-12 10:00:00"
		},{
			"member_name": "jack",
			"status": "已关注",
			"pay_times": 1,
			"integral": 20,
			"pay_money": 110.00,
			"member_rank": "普通会员",
			"attention_time": "2015-08-11 10:00:00"
		},{
			"member_name": "tom",
			"status": "已关注",
			"pay_times": 2,
			"integral": 20,
			"pay_money": 225.00,
			"member_rank": "普通会员",
			"attention_time": "2015-05-11 00:00:00"
		}]
		"""

	When jobs设置带参数二维码关注会员查询条件
		"""
		{
			"start_time": "",
			"end_time": "",
			"is_new_attention_member": "false"
		}
		"""
	Then jobs获得'带参数二维码-第二个二维码'关注会员列表
		"""
		[{
			"member_name": "bill",
			"status": "已关注",
			"pay_times": 3,
			"integral": 20,
			"pay_money": 440.00,
			"member_rank": "普通会员",
			"attention_time": "2015-05-10 00:00:00"
		}]
		"""

@mall2 @senior @bandParameterCode
Scenario:7 带参数二维码[关注数量]关注会员列表查询-代言人扫自己的二维码
	#代言人扫自己的二维码，此二维码的[关注数量]关注会员列表不增加
	Given jobs登录系统
	When tom2关注jobs的公众号于'2015-10-12 08:00:00'

	#更新带参数二维码规则
	Given jobs登录系统
	When jobs更新带参数二维码'带参数二维码-默认设置'
		"""
		{
			"code_name": "带参数二维码-默认设置",
			"create_time": "2015-08-10 10:00:00",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "true",
			"relation_member": "tom2",
			"relation_time": "2015-10-13 08:00:00",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		}
		"""
	#代言人（二维码关联会员）扫自己的二维码，[关注数量]关注会员列表不增加
		When 清空浏览器
		When tom2扫描带参数二维码"带参数二维码-默认设置"

		Given jobs登录系统
		When jobs设置带参数二维码关注会员查询条件
			"""
			{
				"start_time": "",
				"end_time": "",
				"is_new_attention_member": "false"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'关注会员列表
			"""
			[{
				"member_name": "marry",
				"status": "已关注",
				"pay_times": 1,
				"integral": 20,
				"pay_money": 110.00,
				"member_rank": "普通会员",
				"attention_time": "2015-08-13 10:00:00"
			},{
				"member_name": "nokia",
				"status": "已关注",
				"pay_times": 0,
				"integral": 20,
				"pay_money": 0.00,
				"member_rank": "普通会员",
				"attention_time": "2015-08-12 10:00:00"
			},{
				"member_name": "jack",
				"status": "已关注",
				"pay_times": 1,
				"integral": 20,
				"pay_money": 110.00,
				"member_rank": "普通会员",
				"attention_time": "2015-08-11 10:00:00"
			},{
				"member_name": "tom",
				"status": "已关注",
				"pay_times": 2,
				"integral": 20,
				"pay_money": 225.00,
				"member_rank": "普通会员",
				"attention_time": "2015-05-11 00:00:00"
			},{
				"member_name": "bill",
				"status": "已关注",
				"pay_times": 3,
				"integral": 20,
				"pay_money": 440.00,
				"member_rank": "普通会员",
				"attention_time": "2015-05-10 00:00:00"
			}]
			"""


@mall2 @senior @bandParameterCode
Scenario:8 带参数二维码[批量修改]
	When jobs登录系统
	Then jobs能获取二维码列表
		"""
			[{
				"name": "带参数二维码-第二个二维码",
				"attention_number": 0,
				"attention_money": 0.00,
				"create_time": "2015-08-10 10:00:00",
				"scan_reward": ""
			}, {
				"name": "带参数二维码-默认设置",
				"attention_number": 0,
				"attention_money": 0.00,
				"create_time": "2015-08-10 10:00:00"
				"scan_reward": ""
			}]
		"""
	When jobs访问二维码列表
	When jobs选择二维码
		| name                      |attention_number |  create_time             |scan_reward|
		| 带参数二维码-第二个二维码 |   0             | 2015-08-10 10:00:00      |           |
		| 带参数二维码-默认设置     |   0             | 2015-08-10 10:00:00      |           |

	When jobs批量修改二维码
		"""
			[{
				"code_name": ["带参数二维码-默认设置","带参数二维码-第二个二维码"],
				"create_time": "2015-08-10 10:00:00",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "分组1",
				"is_attention_in": "false",
				"remarks": "",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复批量修改"
			}]
		"""
	Then jobs能获取二维码'带参数二维码-默认设置'
		"""
			[{	
				"code_name": "带参数二维码-默认设置",
				"create_time": "2015-08-10 10:00:00",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "分组1",
				"is_attention_in": "false",
				"remarks": "",
				"is_relation_member": "false",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复批量修改"
			}]
		"""






