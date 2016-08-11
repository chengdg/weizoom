#author: 江秋丽 2016-08-03

Feature:渠道分销-前台会员列表

Background:
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
		}]
		"""
	And bigs关注jobs的公众号于'2015-10-01'
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
			"discount":"0.5"
		},{
			"name": "商品2",
			"price": 100.00,
			"discount":"1"
		}]
		"""
@mall2 @apps @senior @member_list
Scenario:1 前台会员列表详情
	#扫码关注成为会员
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
		When 清空浏览器
		And jack扫描带参数二维码"分销二维码1"于'2015-08-10 10:00:00'
		And jack访问jobs的webapp
		When 清空浏览器
		And bill扫描带参数二维码"分销二维码1"于'2015-08-11 10:00:00'
		And bill访问jobs的webapp

	#会员购买
		When 微信用户批量消费jobs的商品
			"""
			[{
				"wx_name":"jack",
				"order_id": "001",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品1",
					"count":1 
				}]
			},{
				"wx_name":"jack",
				"order_id": "002",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}]
			"""
		When bill批量消费jobs的商品
			"""
			[{
				"wx_name":"bill",
				"order_id": "003",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品1",
					"count":1 
				}]
			},{
				"wx_name":"bill",
				"order_id": "004",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}]
			"""
		Given jobs登录系统
		Then jobs获得已有会员列表详情
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
