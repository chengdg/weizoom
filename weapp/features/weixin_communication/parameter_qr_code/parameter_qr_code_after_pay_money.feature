#author: 王丽 2015-10-27

Feature:带参数二维码-列表-扫码后成交金额
"""
	带参数二维码-列表-扫码后成交金额
	1 【扫码后成交金额】:关注此二维码的会员的订单的"下单时间"在此会员的"扫码时间"之后的，
						所有有效订单（待发货、已发货、已完成）的实付金额之和
						(1)"已关注会员可参与"同一微信账号交替扫不同的码[对应订单]跳转
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
				"postage": 10.00,
				"price": 100.00,
				"weight": 5.0,
				"stock_type": "无限"
			},{
				"name": "商品2",
				"postage": 15.00,
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
		And jack扫描带参数二维码"带参数二维码-默认设置"
		And jack访问jobs的webapp

		When 清空浏览器
		And nokia扫描带参数二维码"带参数二维码-默认设置"
		And nokia访问jobs的webapp

		When 清空浏览器
		And marry扫描带参数二维码"带参数二维码-默认设置"
		And marry访问jobs的webapp

	#已关注或者取消关注的会员，扫码
		When bill扫描带参数二维码"带参数二维码-默认设置"于2015-06-10 10:00:00

		And tom扫描带参数二维码"带参数二维码-默认设置"

	#会员购买
		When 微信用户批量消费jobs的商品
			| order_id |    date    | payment_time | consumer |    product     | payment | pay_type  |postage   *|price   *|integral |       coupon         | paid_amount   * |  weizoom_card     | alipay*    | wechat*    | cash*    |   action      | order_status* |
			|   0001   | 2015-06-07 |              |   bill   | 商品1,1        |         |  支付宝   |   10.00   | 100.00  |   0     |                      |     110.00      |                   |    0.00    |    0.00    |   0.00   |               |    待支付     |
			|   0002   | 2015-06-08 |              |   tom    | 商品1,1        |         |  支付宝   |   10.00   | 100.00  |   0     |                      |     110.00      |                   |    0.00    |    0.00    |   0.00   |  jobs,取消    |    已取消     |
			|   0003   | 2015-06-09 |  2014-06-10  |   tom    | 商品2,黑色 M,2 |   支付  |  微信支付 |   15.00   | 100.00  |   0     | 全体券1,coupon1_id_1 |     205.00      |                   |    0.00    |   205.00   |   0.00   |  jobs,发货    |    已发货     |
			|   0004   | 2天前      |     2天前    |   bill   | 商品1,1        |   支付  |  支付宝   |   10.00   | 100.00  |  50     |                      |     60.00       |                   |   60.00    |    0.00    |   0.00   |  jobs,退款    |    退款中     |
			|   0005   | 2天前      |     2天前    |   tom    | 商品1,1        |   支付  |  支付宝   |   10.00   | 100.00  |  50     |                      |     60.00       |                   |   60.00    |    0.00    |   0.00   |  jobs,完成退款|   退款成功    |
			|   0006   | 今天       |     今天     |  marry   | 商品1,1        |   支付  |  支付宝   |   10.00   | 100.00  |  50     |                      |     60.00       |                   |   60.00    |    0.00    |   0.00   |               |    待发货     |
			|   0007   | 今天       |     今天     |  jack    | 商品1,1        |   支付  |  货到付款 |   10.00   | 100.00  |   0     |                      |     110.00      |                   |    0.00    |    0.00    |   110.00 |               |    待发货     |
			|   0008   | 今天       |     今天     |  marry   | 商品2,白色 S,1 |   支付  |  货到付款 |   15.00   | 100.00  |   0     | 全体券1,coupon1_id_2 |     105.00      |  0000002,1234567  |    0.00    |    0.00    |   15.00  |  jobs,完成    |    已完成     |
			|   0009   | 今天       |     今天     |  jack    | 商品3,1        |   支付  |  微信支付 |   0.00    | 10.00   |   0     | 全体券1,coupon1_id_3 |     0.00        |                   |    0.00    |    0.00    |   0.00   |  jobs,发货    |    已发货     |
			|   0010   | 今天       |     今天     |   bill   | 商品2,白色 S,1 |   支付  |  货到付款 |   15.00   | 100.00  |   0     | 全体券1,coupon1_id_4 |     105.00      |  0000001,1234567  |    0.00    |    0.00    |   5.00   |  jobs,完成    |    已完成     |

@mall2 @senior @bandParameterCode
Scenario:1 带参数二维码-[扫码后成交金额]
	Given jobs登录系统

	Then jobs获得带参数二维码列表
		"""
		[{
			"code_name": "带参数二维码-默认设置",
			"order_money": 380.00
		},{
			"code_name": "带参数二维码-第二个二维码",
			"order_money": 0.00
		}]
		"""

@mall2 @senior @bandParameterCode
Scenario:2 带参数二维码-[扫码后成交金额]-"已关注会员可参与"同一微信账号交替扫不同的码[扫码后成交金额]跳转
	Given jobs登录系统

	When 清空浏览器
	When bill扫描带参数二维码"带参数二维码-第二个二维码"于2015-06-15 10:00:00

	Given jobs登录系统
	Then jobs获得带参数二维码列表
		"""
		[{
			"code_name": "带参数二维码-默认设置",
			"order_money": 275.00
		},{
			"code_name": "带参数二维码-第二个二维码",
			"order_money": 105.00
		}]
		"""
