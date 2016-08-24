#author: 王丽 2015-10-27

Feature:带参数二维码-扫码后成交金额-交易订单
"""
	带参数二维码-扫码后成交金额-交易订单
	1 【扫码后成交金额】:关注此二维码的会员的订单的"下单时间"在此会员的"扫码时间"之后的，
						所有有效订单（待发货、已发货、已完成）的实付金额之和
						(1)"已关注会员可参与"同一微信账号交替扫不同的码[对应订单]跳转
	2 【商品名称】：订单中商品的名称
	3 【商品规格】：商品的规格
	4 【订单编号】：订单的编号；可以跳转到订单详情页
	5 【支付方式】：订单的实付方式；可以是"微信支付"、"货到付款"、"支付宝"、"优惠抵扣"
	6 【优惠金额】：积分抵扣、优惠券、直接减价三种方式优惠的金额总和
	7 【买家】：会员昵称；可以跳转到会员详情页
	8 【实付金额】：扣除优惠抵扣金额之后订单的金额；
	9 【运费】：订单的运费金额
	10 【订单状态】：可以为"待支付"、"已取消"、"待发货"、"已发货"、"已完成"、"退款中"、"退款成功"
	11 【下单时间】：订单的下单时间；精确到秒
	12 【付款时间】：订单的支付时间；精确到秒

	筛选条件
	13 【仅显示扫码后成交订单】：勾选或者不勾选；默认勾选；即下单时间在当前会员扫码时间之后的订单
	14 【下单时间筛选条件】：精确到秒
							(1)开始时间为空，结束时间为空；查询出所有
							(2)开始时间为空，结束时间不为空；查询结束时间之前所有
							(3)开始时间不为空，结束时间为空；查询开始时间之后所有
							(4)开始时间不为空，结束时间不为空；查询区间内所有
	汇总数据
	15 【现金支付】：查询结果订单中的实付金额减去微众卡支付金额的总和
	16 【微众卡支付】：查询结果订单中的微众卡支付金额总和
"""

Background:
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

		When bill关注jobs的公众号于'2015-05-10 10:00:00'
		And tom关注jobs的公众号于'2015-05-11 10:00:00'
		And tom取消关注jobs的公众号

	Given jobs登录系统
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-默认设置",
			"create_time": "2015-06-09 10:00:00",
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
			"create_time": "2015-06-08 10:00:00",
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

	#扫码关注成为会员
		When 清空浏览器
		And jack扫描带参数二维码"带参数二维码-默认设置"于2015-08-10 10:00:00
		And jack访问jobs的webapp

		When 清空浏览器
		And nokia扫描带参数二维码"带参数二维码-默认设置"于2015-08-11 10:00:00
		And nokia访问jobs的webapp

		When 清空浏览器
		And marry扫描带参数二维码"带参数二维码-默认设置"于2015-08-12 10:00:00
		And marry访问jobs的webapp

	#已关注或者取消关注的会员，扫码
		When bill扫描带参数二维码"带参数二维码-默认设置"于2015-06-10 10:00:00

		And tom扫描带参数二维码"带参数二维码-默认设置"于2015-06-10 11:00:00
		And tom关注jobs的公众号

	#会员购买
		When 微信用户批量消费jobs的商品
			| order_id |    date    | payment_time | consumer |    product     | payment | pay_type  |postage*|price*|integral |       coupon         | paid_amount* |  weizoom_card     | alipay* | wechat* | cash* |   action      | order_status* |
			|   0001   | 2015-06-07 |              |   bill   | 商品1,1        |         |  支付宝   |   10   | 100  |   0     |                      |     110      |                   |    0    |    0    |   0   |               |    待支付     |
			|   0002   | 2015-06-08 |              |   tom    | 商品1,1        |         |  支付宝   |   10   | 100  |   0     |                      |     110      |                   |    0    |    0    |   0   |  jobs,取消    |    已取消     |
			|   0003   | 2015-06-09 |  2014-06-10  |   tom    | 商品2,黑色 M,2 |   支付  |  微信支付 |   15   | 100  |   0     | 全体券1,coupon1_id_1 |     205      |                   |    0    |   205   |   0   |  jobs,发货    |    已发货     |
			|   0004   | 2015-07-12 |  2015-07-12  |   bill   | 商品1,1        |   支付  |  支付宝   |   10   | 100  |  50     |                      |     60       |                   |   60    |    0    |   0   |  jobs,退款    |    退款中     |
			|   0005   | 2015-07-13 |  2015-07-13  |   tom    | 商品1,1        |   支付  |  支付宝   |   10   | 100  |  50     |                      |     60       |                   |   60    |    0    |   0   |  jobs,完成退款|   退款成功    |
			|   0006   | 2015-09-01 |  2015-09-02  |  marry   | 商品1,1        |   支付  |  支付宝   |   10   | 100  |  50     |                      |     60       |                   |   60    |    0    |   0   |               |    待发货     |
			|   0007   | 2015-09-02 |  2015-09-02  |  jack    | 商品1,1        |   支付  |  货到付款 |   10   | 100  |   0     |                      |     110      |                   |    0    |    0    |   110 |               |    待发货     |
			|   0008   | 2015-09-03 |  2015-09-03  |  marry   | 商品2,白色 S,1 |   支付  |  货到付款 |   15   | 100  |   0     | 全体券1,coupon1_id_2 |     105      |  0000002,1234567  |    0    |    0    |   15  |  jobs,完成    |    已完成     |
			|   0009   | 2015-09-04 |  2015-09-04  |  jack    | 商品3,1        |   支付  |  微信支付 |   0    | 10   |   0     | 全体券1,coupon1_id_3 |     0        |                   |    0    |    0    |   0   |  jobs,发货    |    已发货     |
			|   0010   | 2015-09-05 |  2015-09-05  |   bill   | 商品2,白色 S,1 |   支付  |  货到付款 |   15   | 100  |   0     | 全体券1,coupon1_id_4 |     105      |  0000001,1234567  |    0    |    0    |   5   |  jobs,完成    |    已完成     |

@mall2 @senior @bandParameterCode
Scenario:1 带参数二维码-[扫码后成交金额]交易订单列表-默认条件
	Given jobs登录系统

	#交易订单列表，默认查询"  仅显示扫码后成交订单",按照"下单时间"倒叙排列
	Then jobs获得'带参数二维码-默认设置'交易订单列表汇总
		"""
		{
			"cash": 190.00,
			"weizoom_card": 190.00
		}
		"""
	Then jobs获得'带参数二维码-默认设置'交易订单列表
		| order_no | order_time | payment_time | consumer |    product     | price  | pay_type | postage | discount_amount | paid_amount | order_status |
		|   0010   | 2015-09-05 | 2015-09-05   |   bill   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
		|   0009   | 2015-09-04 | 2015-09-04   |  jack    | 商品3,1        | 10.00  | 优惠抵扣 |  0.00   |      10.00      |   0.00      |    已发货    |
		|   0008   | 2015-09-03 | 2015-09-03   |  marry   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
		|   0007   | 2015-09-02 | 2015-09-02   |  jack    | 商品1,1        | 100.00 | 货到付款 |  10.00  |       0.00      |   110.00    |    待发货    |
		|   0006   | 2015-09-01 | 2015-09-02   |  marry   | 商品1,1        | 100.00 | 支付宝   |  10.00  |      50.00      |   60.00     |    待发货    |

@mall2 @senior @bandParameterCode
Scenario:2 带参数二维码-[扫码后成交金额]交易订单列表-仅显示扫码后成交订单
	Given jobs登录系统

	#仅显示扫码后成交订单-不勾选
		When jobs设置带参数二维码交易订单列表查询条件
			"""
			{
				"start_time": "",
				"end_time": "",
				"is_after_code_order": "false"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表汇总
			"""
			{
				"cash": 395.00,
				"weizoom_card": 190.00
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表
			| order_no | order_time | payment_time | consumer |    product     | price  | pay_type | postage | discount_amount | paid_amount | order_status |
			|   0010   | 2015-09-05 | 2015-09-05   |   bill   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
			|   0009   | 2015-09-04 | 2015-09-04   |  jack    | 商品3,1        | 10.00  | 优惠抵扣 |  0.00   |      10.00      |   0.00      |    已发货    |
			|   0008   | 2015-09-03 | 2015-09-03   |  marry   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
			|   0007   | 2015-09-02 | 2015-09-02   |  jack    | 商品1,1        | 100.00 | 货到付款 |  10.00  |       0.00      |   110.00    |    待发货    |
			|   0006   | 2015-09-01 | 2015-09-02   |  marry   | 商品1,1        | 100.00 | 支付宝   |  10.00  |      50.00      |   60.00     |    待发货    |
			|   0003   | 2015-06-09 | 2014-06-10   |   tom    | 商品2,黑色 M,2 | 100.00 | 微信支付 |  15.00  |      10.00      |   205.00    |    已发货    |

	#仅显示扫码后成交订单-勾选
		When jobs设置带参数二维码交易订单列表查询条件
			"""
			{
				"start_time": "",
				"end_time": "",
				"is_after_code_order": "true"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表汇总
			"""
			{
				"cash": 190.00,
				"weizoom_card": 190.00
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表
			| order_no | order_time | payment_time | consumer |    product     | price  | pay_type | postage | discount_amount | paid_amount | order_status |
			|   0010   | 2015-09-05 | 2015-09-05   |   bill   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
			|   0009   | 2015-09-04 | 2015-09-04   |  jack    | 商品3,1        | 10.00  | 优惠抵扣 |  0.00   |      10.00      |   0.00      |    已发货    |
			|   0008   | 2015-09-03 | 2015-09-03   |  marry   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
			|   0007   | 2015-09-02 | 2015-09-02   |  jack    | 商品1,1        | 100.00 | 货到付款 |  10.00  |       0.00      |   110.00    |    待发货    |
			|   0006   | 2015-09-01 | 2015-09-02   |  marry   | 商品1,1        | 100.00 | 支付宝   |  10.00  |      50.00      |   60.00     |    待发货    |

@mall2 @senior @bandParameterCode
Scenario:3 带参数二维码-[扫码后成交金额]交易订单列表-下单时间查询
	Given jobs登录系统

	#下单时间：开始时间为空，结束时间为空
		When jobs设置带参数二维码交易订单列表查询条件
			"""
			{
				"start_time": "",
				"end_time": "",
				"is_after_code_order": "false"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表汇总
			"""
			{
				"cash": 395.00,
				"weizoom_card": 190.00
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表
			| order_no | order_time | payment_time | consumer |    product     | price  | pay_type | postage | discount_amount | paid_amount | order_status |
			|   0010   | 2015-09-05 | 2015-09-05   |   bill   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
			|   0009   | 2015-09-04 | 2015-09-04   |  jack    | 商品3,1        | 10.00  | 优惠抵扣 |  0.00   |      10.00      |   0.00      |    已发货    |
			|   0008   | 2015-09-03 | 2015-09-03   |  marry   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
			|   0007   | 2015-09-02 | 2015-09-02   |  jack    | 商品1,1        | 100.00 | 货到付款 |  10.00  |       0.00      |   110.00    |    待发货    |
			|   0006   | 2015-09-01 | 2015-09-02   |  marry   | 商品1,1        | 100.00 | 支付宝   |  10.00  |      50.00      |   60.00     |    待发货    |
			|   0003   | 2015-06-09 | 2014-06-10   |   tom    | 商品2,黑色 M,2 | 100.00 | 微信支付 |  15.00  |      10.00      |   205.00    |    已发货    |

	#下单时间：开始时间不为空，结束时间为空
		When jobs设置带参数二维码交易订单列表查询条件
			"""
			{
				"start_time": "2015-09-01 00:00:00",
				"end_time": "",
				"is_after_code_order": "false"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表汇总
			"""
			{
				"cash": 190.00,
				"weizoom_card": 190.00
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表
			| order_no | order_time | payment_time | consumer |    product     | price  | pay_type | postage | discount_amount | paid_amount | order_status |
			|   0010   | 2015-09-05 | 2015-09-05   |   bill   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
			|   0009   | 2015-09-04 | 2015-09-04   |  jack    | 商品3,1        | 10.00  | 优惠抵扣 |  0.00   |      10.00      |   0.00      |    已发货    |
			|   0008   | 2015-09-03 | 2015-09-03   |  marry   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
			|   0007   | 2015-09-02 | 2015-09-02   |  jack    | 商品1,1        | 100.00 | 货到付款 |  10.00  |       0.00      |   110.00    |    待发货    |
			|   0006   | 2015-09-01 | 2015-09-02   |  marry   | 商品1,1        | 100.00 | 支付宝   |  10.00  |      50.00      |   60.00     |    待发货    |

	#下单时间：开始时间为空，结束时间不为空
		When jobs设置带参数二维码交易订单列表查询条件
			"""
			{
				"start_time": "",
				"end_time": "2015-06-09 00:00:00",
				"is_after_code_order": "false"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表汇总
			"""
			{
				"cash": 205.00,
				"weizoom_card": 0.00
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表
			| order_no | order_time | payment_time | consumer |    product     | price  | pay_type | postage | discount_amount | paid_amount | order_status |
			|   0003   | 2015-06-09 | 2014-06-10   |   tom    | 商品2,黑色 M,2 | 100.00 | 微信支付 |  15.00  |      10.00      |   205.00    |    已发货    |

	#下单时间：开始时间不为空，结束时间不为空
		When jobs设置带参数二维码交易订单列表查询条件
			"""
			{
				"start_time": "2015-09-02 00:00:00",
				"end_time": "2015-09-02 00:00:00",
				"is_after_code_order": "false"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表汇总
			"""
			{
				"cash": 110.00,
				"weizoom_card": 0.00
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表
			| order_no | order_time | payment_time | consumer |    product     | price  | pay_type | postage | discount_amount | paid_amount | order_status |
			|   0007   | 2015-09-02 | 2015-09-02   |  jack    | 商品1,1        | 100.00 | 货到付款 |  10.00  |       0.00      |   110.00    |    待发货    |

	#查询结果为空
		When jobs设置带参数二维码交易订单列表查询条件
			"""
			{
				"start_time": "2015-06-05 00:00:00",
				"end_time": "2015-06-08 00:00:00",
				"is_after_code_order": "true"
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表汇总
			"""
			{
				"cash": 0.00,
				"weizoom_card": 0.00
			}
			"""
		Then jobs获得'带参数二维码-默认设置'交易订单列表
			| order_no | order_time | payment_time | consumer |    product     |price | pay_type  |postage |discount_amount | paid_amount | order_status |

@mall2 @senior @bandParameterCode
Scenario:4 带参数二维码-[扫码后成交金额]交易订单列表-分页
	Given jobs登录系统

	And jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""
	When jobs设置带参数二维码交易订单列表查询条件
		"""
		{
			"start_time": "",
			"end_time": "",
			"is_after_code_order": "true"
		}
		"""
	#交易订单列表共'3'页

	When jobs访问'带参数二维码-默认设置'交易订单列表第'1'页
	Then jobs获得'带参数二维码-默认设置'交易订单列表
		| order_no | order_time | payment_time | consumer |    product     | price  | pay_type | postage | discount_amount | paid_amount | order_status |
		|   0010   | 2015-09-05 | 2015-09-05   |   bill   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
		|   0009   | 2015-09-04 | 2015-09-04   |  jack    | 商品3,1        | 10.00  | 优惠抵扣 |  0.00   |      10.00      |   0.00      |    已发货    |
	When jobs访问交易订单列表下一页
	Then jobs获得'带参数二维码-默认设置'交易订单列表
		| order_no | order_time | payment_time | consumer |    product     | price  | pay_type | postage | discount_amount | paid_amount | order_status |
		|   0008   | 2015-09-03 | 2015-09-03   |  marry   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
		|   0007   | 2015-09-02 | 2015-09-02   |  jack    | 商品1,1        | 100.00 | 货到付款 |  10.00  |       0.00      |   110.00    |    待发货    |
	When jobs访问'带参数二维码-默认设置'交易订单列表第'3'页
	Then jobs获得'带参数二维码-默认设置'交易订单列表
		| order_no | order_time | payment_time | consumer |    product     | price  | pay_type | postage | discount_amount | paid_amount | order_status |
		|   0006   | 2015-09-01 | 2015-09-02   |  marry   | 商品1,1        | 100.00 | 支付宝   |  10.00  |      50.00      |   60.00     |    待发货    |
	When jobs访问交易订单列表上一页
	Then jobs获得'带参数二维码-默认设置'交易订单列表
		| order_no | order_time | payment_time | consumer |    product     | price  | pay_type | postage | discount_amount | paid_amount | order_status |
		|   0008   | 2015-09-03 | 2015-09-03   |  marry   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
		|   0007   | 2015-09-02 | 2015-09-02   |  jack    | 商品1,1        | 100.00 | 货到付款 |  10.00  |       0.00      |   110.00    |    待发货    |

@mall2 @senior @bandParameterCode
Scenario:5 带参数二维码-[扫码后成交金额]交易订单列表-"已关注会员可参与"同一微信账号交替扫不同的码[扫码后成交金额]交易订单跳转
	Given jobs登录系统

	When 清空浏览器
	When bill扫描带参数二维码"带参数二维码-第二个二维码"

	Given jobs登录系统
	When jobs设置带参数二维码交易订单列表查询条件
		"""
		{
			"start_time": "",
			"end_time": "",
			"is_after_code_order": "true"
		}
		"""
	Then jobs获得'带参数二维码-默认设置'交易订单列表汇总
		"""
		{
			"cash": 185.00,
			"weizoom_card": 90.00
		}
		"""
	Then jobs获得'带参数二维码-默认设置'交易订单列表
		| order_no | order_time | payment_time | consumer |    product     | price  | pay_type | postage | discount_amount | paid_amount | order_status |
		|   0009   | 2015-09-04 | 2015-09-04   |  jack    | 商品3,1        | 10.00  | 优惠抵扣 |  0.00   |      10.00      |   0.00      |    已发货    |
		|   0008   | 2015-09-03 | 2015-09-03   |  marry   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
		|   0007   | 2015-09-02 | 2015-09-02   |  jack    | 商品1,1        | 100.00 | 货到付款 |  10.00  |       0.00      |   110.00    |    待发货    |
		|   0006   | 2015-09-01 | 2015-09-02   |  marry   | 商品1,1        | 100.00 | 支付宝   |  10.00  |      50.00      |   60.00     |    待发货    |

	When jobs设置带参数二维码交易订单列表查询条件
		"""
		{
			"start_time": "",
			"end_time": "",
			"is_after_code_order": "false"
		}
		"""
	Then jobs获得'带参数二维码-第二个二维码'交易订单列表汇总
		"""
		{
			"cash": 5.00,
			"weizoom_card": 100.00
		}
		"""
	Then jobs获得'带参数二维码-第二个二维码'交易订单列表
		| order_no | order_time | payment_time | consumer |    product     | price  | pay_type | postage | discount_amount | paid_amount | order_status |
		|   0010   | 2015-09-05 | 2015-09-05   |   bill   | 商品2,白色 S,1 | 100.00 | 货到付款 |  15.00  |      10.00      |   105.00    |    已完成    |
