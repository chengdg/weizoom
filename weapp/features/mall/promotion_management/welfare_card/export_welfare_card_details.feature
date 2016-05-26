# watcher: benchi@weizoom.com, zhangsanxiang@weizoom.com
#_author_:张三香 2016.05.20

Feature:导出福利卡券的码库详情

Background:
	Given 设置jobs为自营平台账号
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		},{
			"name": "分类2"
		}]
		"""
	And jobs已添加供货商
		"""
		[{
			"name": "微众",
			"responsible_person": "张大众",
			"supplier_tel": "15211223344",
			"supplier_address": "北京市海淀区海淀科技大厦",
			"remark": "备注"
		}, {
			"name": "稻香村",
			"responsible_person": "许稻香",
			"supplier_tel": "15311223344",
			"supplier_address": "北京市朝阳区稻香大厦",
			"remark": ""
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"is_active": "启用"
		},{
			"type": "支付宝",
			"is_active": "启用"
		}]
		"""
	When jobs开通使用微众卡权限
	When jobs添加支付方式
		"""
		[{
			"type": "微众卡支付",
			"description": "我的微众卡支付",
			"is_active": "启用"
		}]
		"""
	Given jobs已添加商品
		"""
		[{
			"name": "微众虚拟商品1",
			"product_type":"微众卡",
			"supplier": "微众",
			"purchase_price": 9.00,
			"promotion_title": "10元通用卡",
			"categories": "分类1,分类2",
			"bar_code":"112233",
			"min_limit":1,
			"is_member_product":"off",
			"price": 10.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 0,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			},{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"postage":0.00,
			"pay_interfaces":
				[{
					"type": "在线支付"
				},{
					"type": "货到付款"
				}],
			"detail":"微众虚拟商品1的详情",
			"status":"在售"
		}]
		"""
	And jobs已创建微众卡
		"""
		{
			"cards":[{
				"id":"0000001",
				"password":"1234567",
				"status":"未使用",
				"price":10.00
			},{
				"id":"0000002",
				"password":"2234567",
				"status":"未使用",
				"price":10.00
			},{
				"id":"0000003",
				"password":"3234567",
				"status":"未使用",
				"price":10.00
			},{
				"id":"0000004",
				"password":"4234567",
				"status":"未激活",
				"price":10.00
			}]
		}
		"""
	When jobs新建福利卡券活动
		"""
		[{
			"product":
				{
					"name":"微众虚拟商品1",
					"bar_code":"112233",
					"price":10.00
				},
			"activity_name":"10元通用卡",
			"card_start_date":"今天",
			"card_end_date":"30天后",
			"card_info":
				{
					"card_type":"微众卡",
					"card_stocks":3,
					"cards":
						[{
							"id":"0000001",
							"password":"1234567"
						},{
							"id":"0000002",
							"password":"2234567"
						},{
							"id":"0000003",
							"password":"3234567"
						}]
				},
			"creat_time":"今天"
		}]
		"""
	When bill关注jobs的公众号

	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"order_id": "001",
			"date":"今天",
			"products": [{
				"name": "微众虚拟商品1",
				"count": 1
			}],
			"pay_type":"微信支付",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
	When bill使用支付方式'微信支付'进行支付订单'001'
	Given jobs登录系统
	When jobs自动发放卡券给订单'001'
		"""
		[{
			"id":"0000001",
			"password":"1234567"
		}]
		"""

@welfare_card @weshop
Scenario:1 导出码库详情
	Given jobs登录系统
	Then jobs导出福利卡券活动'10元通用卡'的码库详情
		| card_id | create_time |start_date   |end_date     | status | get_time | member | order_no |
		| 0000001 |   今天      |   今天      |   30天后    | 已领取 | 今天     | bill   |   001    |
		| 0000002 |   今天      |   今天      |   30天后    | 未领取 |          |        |          |
		| 0000003 |   今天      |   今天      |   30天后    | 未领取 |          |        |          |

