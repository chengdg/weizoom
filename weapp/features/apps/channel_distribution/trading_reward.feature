#author: 邓成龙 2016-08-03

Feature:交易记录详情和奖励明细
"""
		1.一个微信用户扫码下单交易记录列表
		2.一个微信用户扫码下单2次交易记录列表
		3.一个微信用户扫码下单1另一个微信用户下单2次交易记录列表
		4.奖励明细列表一条记录
		5.奖励明细列表2条记录
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
	And jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1"
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
		}]
		"""
	And bigs关注jobs的公众号于'2015-10-01 10:00:00'
	And bill关注jobs的公众号于'2015-10-02 10:00:00'
	Given jobs登录系统
	When jobs新建渠道分销二维码
		"""
		[{
			"code_name": "渠道分销二维码-佣金设置1",
			"relation_member": "bigs",
			"distribution_prize_type": "佣金",
			"commission_return_rate":"10",
			"minimum_cash_discount":"80",
			"commission_return_standard":50.00,
			"is_seven_day_settlement_standard":"false",
			"tags": "未分组",
			"prize_type": "无",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本",
			"create_time": "2015-10-10 10:20:30"
		},{
			"code_name": "渠道分销二维码-佣金设置2",
			"relation_member": "bill",
			"distribution_prize_type": "佣金",
			"commission_return_rate":"10",
			"minimum_cash_discount":"80",
			"commission_return_standard":50.00,
			"is_seven_day_settlement_standard":"false",
			"tags": "分组1",
			"prize_type": "优惠券",
			"coupon":"优惠券1",
			"reply_type": "图文",
			"scan_code_reply": "图文1",
			"create_time": "2015-10-10 10:20:30"
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type":"货到付款"
		},{
			"type":"微信支付"
		},{
			"type":"支付宝"
		}]
		"""

	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"count":"10",
			"discount":"0.5"
		},{
			"name": "商品2",
			"price": 100.00,
			"count":"10",
			"discount":"1"
		}]
		"""

	#扫码关注成为会员
		When 清空浏览器
		And jack扫描带参数二维码"渠道分销二维码-佣金设置1"于2015-08-10 10:00:00
		And jack访问jobs的webapp

		When 清空浏览器
		And nokia扫描带参数二维码"渠道分销二维码-佣金设置2"于2015-08-11 10:00:00
		And nokia访问jobs的webapp
	
		When 清空浏览器
		And marry扫描带参数二维码"渠道分销二维码-佣金设置1"于2015-08-12 10:00:00
		And marry访问jobs的webapp

	#会员购买
		When jack批量消费jobs的商品
			"""
			[{
				"relation_member":"bigs",
				"order_id": "002",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bigs",
				"order_id": "003",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bigs",
				"order_id": "004",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bigs",
				"order_id": "005",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bigs",
				"order_id": "006",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bigs",
				"order_id": "007",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}]
			"""
		When jack批量消费jobs的商品
			"""
			[{
				"relation_member":"bigs",
				"order_id": "022",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bigs",
				"order_id": "033",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bigs",
				"order_id": "044",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bigs",
				"order_id": "055",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bigs",
				"order_id": "066",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When marry批量消费jobs的商品
			"""
			[{
				"relation_member":"bigs",
				"order_id": "222",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bigs",
				"order_id": "333",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bigs",
				"order_id": "444",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bigs",
				"order_id": "555",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bigs",
				"order_id": "666",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When nokia批量消费jobs的商品
			"""
			[{
				"relation_member":"bill",
				"order_id": "008",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			},{
				"relation_member":"bill",
				"order_id": "009",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品1",
					"count":1 
				}]
			},{
				"relation_member":"bill",
				"order_id": "010",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品1",
					"count":1 
				}]
			}]
			"""

@mall2 @apps @senior @trading_reward
Scenario:1 一个微信用户扫码下单交易记录列表
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"
		When bigs访问jobs的webapp
		When bigs申请返现于2015-08-12 10:00:00
		When jobs已返现给jack金额"50.00"
		
		Then jobs获得交易记录列表
			"""
			[{
				"relation_member": "bigs",
				"user_name":"jack",
				"pay_money":500.00,
				"cash_back_amount":50.00
			}]
			"""

@mall2 @apps @senior @trading_reward
Scenario:2 一个微信用户扫码下单2次交易记录列表
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"

		When bigs访问jobs的webapp
		When bigs申请返现于2015-08-12 10:00:00
		When jobs已返现给bigs金额"50.00"

		When jobs完成订单"022"
		When jobs完成订单"033"
		When jobs完成订单"044"
		When jobs完成订单"055"
		When jobs完成订单"066"
		When bigs申请返现于2015-08-15 10:00:00
		When jobs已返现给bigs金额"50.00"
		When jobs设置查看条件
			"""
			{
				"type":"本期交易"
			}
			"""
		Then jobs获得交易记录列表
			"""
			[{
				"relation_member": "bigs",
				"user_name":"jack",
				"pay_money":500.00,
				"cash_back_amount":50.00
			}]
			"""

		When jobs设置查看条件
			"""
			{
				"type":"所有交易"
			}
			"""
		Then jobs获得交易记录列表
			"""
			[{
				"relation_member": "bigs",
				"user_name":"jack",
				"pay_money":1000.00,
				"cash_back_amount":100.00
			}]
			"""
@mall2 @apps @senior @trading_reward
Scenario:3 一个微信用户扫码下单1另一个微信用户下单2次交易记录列表
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"

		When bigs访问jobs的webapp
		When bigs申请返现于2015-08-12 10:00:00
		When jobs已返现给bigs金额"50.00"

		When jobs完成订单"022"
		When jobs完成订单"033"
		When jobs完成订单"044"
		When jobs完成订单"055"
		When jobs完成订单"066"
		When jobs完成订单"222"
		When jobs完成订单"333"
		When jobs完成订单"444"
		When jobs完成订单"555"
		When jobs完成订单"666"
		When bigs申请返现于2015-08-15 10:00:00
		When jobs已返现给bigs金额"100.00"
		When jobs设置查看条件
			"""
			{
				"type":"本期交易"
			}
			"""
		Then jobs获得交易记录列表
			"""
			[{
				"relation_member": "bigs",
				"user_name":"marry",
				"pay_money":500.00,
				"cash_back_amount":50.00
			},{
				"relation_member": "bigs",
				"user_name":"jack",
				"pay_money":500.00,
				"cash_back_amount":50.00
			}]
			"""

		When jobs设置查看条件
			"""
			{
				"type":"所有交易"
			}
			"""
		Then jobs获得交易记录列表
			"""
			[{
				"relation_member": "bigs",
				"user_name":"jack",
				"pay_money":1000.00,
				"cash_back_amount":100.00
			},{
				"relation_member": "bigs",
				"user_name":"jack",
				"pay_money":500.00,
				"cash_back_amount":50.00
			}]
			"""

@mall2 @apps @senior @trading_reward
Scenario:4 奖励明细列表一条记录
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"
		When jack访问jobs的webapp
		When bigs申请返现于2015-08-12 10:00:00
		When jobs已返现给bigs金额"50.00"
		
		Then jobs获得奖励明细列表
			"""
			[{
				"relation_member": "bigs",
				"cycle_time_start":"2015-08-12 10:00:00",
				"cycle_time_end":"今天",
				"commission_return_rate":"10",
				"pay_money":500.00,
				"cash_back_amount":50.00
			}]
			"""

@mall2 @apps @senior @trading_reward
Scenario:5 奖励明细列表2条记录
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"

		When jack访问jobs的webapp
		When bigs申请返现于2015-08-12 10:00:00
		When jobs已返现给bigs金额"50.00"

		When jobs完成订单"022"
		When jobs完成订单"033"
		When jobs完成订单"044"
		When jobs完成订单"055"
		When jobs完成订单"066"
		When jobs完成订单"222"
		When jobs完成订单"333"
		When jobs完成订单"444"
		When jobs完成订单"555"
		When jobs完成订单"666"
		When bigs申请返现于2015-08-15 10:00:00
		When jobs已返现给bigs金额"100.00"

		Then jobs获得奖励明细列表
			"""
			[{
				"relation_member": "bigs",
				"cycle_time_start":"2015-08-15 10:00:00",
				"cycle_time_end":"今天",
				"commission_return_rate":"10",
				"pay_money":1000.00,
				"cash_back_amount":100.00
			},{
				"relation_member": "bigs",
				"cycle_time_start":"2015-08-12 10:00:00",
				"cycle_time_end":"2015-08-15 10:00:00",
				"commission_return_rate":"10",
				"pay_money":500.00,
				"cash_back_amount":50.00
			}]
			"""