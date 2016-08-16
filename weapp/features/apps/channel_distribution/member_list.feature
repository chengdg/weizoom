#author: 江秋丽 2016-08-03

Feature:渠道分销-前台会员列表

Background:
	Given jobs登录系统
	When bigs关注jobs的公众号于'2015-10-01'
	Given jobs登录系统
	When jobs新建渠道分销二维码
		"""
		[{
			"code_name": "分销二维码1",
			"relation_member": "bigs",
			"distribution_prize_type": "佣金",
			"commission_return_rate":"10",
			"minimum_cash_discount":"80",
			"commission_return_standard":50.00,
			"settlement_time":"0",
			"tags": "未分组",
			"prize_type": "无",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本",
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
			"price": 50.00,
			"count":"10"
		},{
			"name": "商品2",
			"price": 100.00,
			"count":"10"
		}]
		"""
		When 清空浏览器
		And jack扫描渠道二维码"分销二维码1"于2015-08-10 10:00:00
		And jack访问jobs的webapp
		When 清空浏览器
		And bill扫描渠道二维码"分销二维码1"于2015-08-11 10:00:00
		And bill访问jobs的webapp

	#会员购买
		When jack购买jobs的商品
			"""
			{
				"order_id": "002",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品1",
					"count":1 
				}]
			}
			"""
		When jack购买jobs的商品
			"""
			{
				"wx_name":"jack",
				"order_id": "003",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When bill购买jobs的商品
			"""
			{
				"order_id": "004",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品1",
					"count":1 
				}]
			}
			"""
		When bill购买jobs的商品
			"""
			{
				"order_id": "005",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
	

@mall2 @apps @senior @member_list @sjq

Scenario:1 前台会员列表详情
	#扫码关注成为会员
		Given jobs登录系统
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When 后台执行channel_distribution_update
		Given bigs登录系统
		Then bigs获得已有会员列表详情
			"""
			[{
				"wx_name": "jack",
				"order_money": 150.00,
				"commision":15.00,
				"purchase_count":2,
				"concern_time":"今天"
			},{
				"wx_name": "bill",
				"order_money": 150.00,
				"commision":15.00,
				"purchase_count":2,
				"concern_time":"昨天"
			}]
			"""
