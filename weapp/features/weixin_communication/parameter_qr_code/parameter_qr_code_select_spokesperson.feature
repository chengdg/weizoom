#author: 王丽 2015-10-28

Feature:带参数二维码-关联会员-选择关联会员
"""
	设置关联会员，可以选择到系统中所有处于[已关注]状态的会员
	1 【用户名称】：会员昵称
	2 【用户等级】：会员等级
	3 【消费金额】：此会员在系统中所有的有效订单（待发货、已发货、已完成）的实付金额之和
	4 【平均客单价】：【消费金额】/【购买次数】
	5 【购买次数】：此会员在系统中所有的有效订单（待发货、已发货、已完成）的个数
	6 【拥有积分】：此会员在系统的积分数
"""

Background:
	Given jobs登录系统

	#添加基础数据
		And jobs设定会员积分策略
			"""
			{
				"be_member_increase_count":200,
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
		When jobs已添加商品
			"""
			[{
				"name": "商品1",
				"postage": 10.00,
				"price": 100.00,
				"weight": 5.0,
				"stock_type": "无限"
			}]
			"""
		When jobs添加会员分组
			"""
			{
				"tag_id_1": "分组1"
			}
			"""
		And jobs添加会员等级
			"""
			[{
				"name": "银牌会员",
				"upgrade": "手动升级",
				"shop_discount": "10"
			}]
			"""

	When bill关注jobs的公众号于'2015-05-10 00:00:00'
	When tom关注jobs的公众号
	When marry关注jobs的公众号
	When jack关注jobs的公众号
	When tom1关注jobs的公众号
	When tom1取消关注jobs的公众号

	When 微信用户批量消费jobs的商品
		| order_id |    date    | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | alipay*    | wechat*    | cash*    |   action      | order_status* |
		|   0001   | 2015-10-10 |   bill   | 商品1,1 |         |  支付宝   |   10.00   | 100.00  |     110.00      |    0.00    |    0.00    |   0.00   |               |    待支付     |
		|   0002   | 2015-10-11 |   bill   | 商品1,1 |         |  支付宝   |   10.00   | 100.00  |     110.00      |    0.00    |    0.00    |   0.00   |  jobs,取消    |    已取消     |
		|   0003   | 2015-10-12 |   bill   | 商品1,2 |   支付  |  微信支付 |   10.00   | 100.00  |     210.00      |    0.00    |   210.00   |   0.00   |  jobs,发货    |    已发货     |
		|   0004   | 今天       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 100.00  |     110.00      |   110.00   |    0.00    |   0.00   |  jobs,退款    |    退款中     |
		|   0005   | 今天       |   tom    | 商品1,1 |   支付  |  货到付款 |   10.00   | 100.00  |     110.00      |    0.00    |    0.00    |  110.00  |  jobs,完成退款|   退款成功    |
		|   0006   | 今天       |  marry   | 商品1,1 |   支付  |  支付宝   |   10.00   | 100.00  |     110.00      |   110.00   |    0.00    |   0.00   |  jobs,完成    |    已完成     |
		|   0007   | 今天       |  jack    | 商品1,1 |   支付  |  货到付款 |   10.00   | 100.00  |     110.00      |    0.00    |    0.00    |  110.00  |               |    待发货     |

@mall2 @senior @bandParameterCode
Scenario:1 带参数二维码-选择关联会员列表
	Given jobs登录系统

	Then jobs获得选择关联会员列表
		"""
		[{
			"member_name": "jack",
			"member_rank": "普通会员",
			"pay_money": 110.00,
			"average_pay_money": 110.00,
			"pay_times": 1,
			"integral": 200
		},{
			"member_name": "marry",
			"member_rank": "普通会员",
			"pay_money": 110.00,
			"average_pay_money": 110.00,
			"pay_times": 1,
			"integral": 200
		},{
			"member_name": "tom",
			"member_rank": "普通会员",
			"pay_money": 110.00,
			"average_pay_money": 110.00,
			"pay_times": 1,
			"integral": 200
		},{
			"member_name": "bill",
			"member_rank": "普通会员",
			"pay_money": 320.00,
			"average_pay_money": 160.00,
			"pay_times": 2,
			"integral": 200
		}]
		"""

@mall2 @bandParameterCode
Scenario:2 带参数二维码-选择关联会员列表查询
	Given jobs登录系统

	#按照用户名称查询
		#模糊查询
		When jobs设置选择关联会员列表查询条件
			"""
			{
				"member_name": "a"
			}
			"""
		Then jobs获得选择关联会员列表
			"""
			[{
				"member_name": "jack",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "marry",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			}]
			"""

		#精确匹配
		When jobs设置选择关联会员列表查询条件
			"""
			{
				"member_name": "jack"
			}
			"""
		Then jobs获得选择关联会员列表
			"""
			[{
				"member_name": "jack",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			}]
			"""

		#查询结果为空
		When jobs设置选择关联会员列表查询条件
			"""
			{
				"member_name": "22"
			}
			"""
		Then jobs获得选择关联会员列表
			"""
			[]
			"""

	#按照分组查询
		#查询全部
		When jobs设置选择关联会员列表查询条件
			"""
			{
				"tags": "全部"
			}
			"""
		Then jobs获得选择关联会员列表
			"""
			[{
				"member_name": "jack",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "marry",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "tom",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "bill",
				"member_rank": "普通会员",
				"pay_money": 320.00,
				"average_pay_money": 160.00,
				"pay_times": 2,
				"integral": 200
			}]
			"""

		#查询分组
		When jobs设置选择关联会员列表查询条件
			"""
			{
				"tags": "未分组"
			}
			"""
		Then jobs获得选择关联会员列表
			"""
			[{
				"member_name": "jack",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "marry",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "tom",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "bill",
				"member_rank": "普通会员",
				"pay_money": 320.00,
				"average_pay_money": 160.00,
				"pay_times": 2,
				"integral": 200
			}]
			"""

		#查询结果为空
		When jobs设置选择关联会员列表查询条件
			"""
			{
				"tags": "分组1"
			}
			"""
		Then jobs获得选择关联会员列表
			"""
			[]
			"""

	#按照会员等级查询
		#查询全部
		When jobs设置选择关联会员列表查询条件
			"""
			{
				"member_rank": "全部"
			}
			"""
		Then jobs获得选择关联会员列表
			"""
			[{
				"member_name": "jack",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "marry",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "tom",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "bill",
				"member_rank": "普通会员",
				"pay_money": 320.00,
				"average_pay_money": 160.00,
				"pay_times": 2,
				"integral": 200
			}]
			"""

		#查询分组
		When jobs设置选择关联会员列表查询条件
			"""
			{
				"member_rank": "普通会员"
			}
			"""
		Then jobs获得选择关联会员列表
			"""
			[{
				"member_name": "jack",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "marry",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "tom",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "bill",
				"member_rank": "普通会员",
				"pay_money": 320.00,
				"average_pay_money": 160.00,
				"pay_times": 2,
				"integral": 200
			}]
			"""

		#查询结果为空
		When jobs设置选择关联会员列表查询条件
			"""
			{
				"member_rank": "银牌会员"
			}
			"""
		Then jobs获得选择关联会员列表
			"""
			[]
			"""

	#组合查询
		When jobs设置选择关联会员列表查询条件
			"""
			{
				"member_name": "a",
				"tags": "全部",
				"member_rank": "普通会员"
			}
			"""
		Then jobs获得选择关联会员列表
			"""
			[{
				"member_name": "jack",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			},{
				"member_name": "marry",
				"member_rank": "普通会员",
				"pay_money": 110.00,
				"average_pay_money": 110.00,
				"pay_times": 1,
				"integral": 200
			}]
			"""
