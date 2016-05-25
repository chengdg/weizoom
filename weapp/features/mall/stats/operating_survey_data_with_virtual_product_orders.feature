# watcher: benchi@weizoom.com, zhangsanxiang@weizoom.com
#_author_:张三香 2016.05.23

Feature:数据罗盘中不统计微众卡相关的订单
	"""
		微众商城的数据罗盘中，不统计商品类型为'微众卡'的相关订单
	"""

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
			"stocks": 100,
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
		},{
			"name": "微众普通商品2",
			"product_type":"普通商品",
			"supplier": "微众",
			"purchase_price": 19.00,
			"promotion_title": "普通商品",
			"categories": "",
			"bar_code":"212233",
			"min_limit":2,
			"is_member_product":"off",
			"price": 20.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 200,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.00,
			"pay_interfaces":
				[{
					"type": "在线支付"
				},{
					"type": "货到付款"
				}],
			"detail": "微众普通商品2的详情",
			"status": "在售"
		},{
			"name": "微众普通商品3",
			"product_type":"普通商品",
			"supplier": "微众",
			"purchase_price": 30.00,
			"promotion_title": "普通商品3",
			"categories": "分类2",
			"bar_code":"412233",
			"min_limit":1,
			"is_member_product":"off",
			"price": 30.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 40,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.00,
			"pay_interfaces":
				[{
					"type": "在线支付"
				},{
					"type": "货到付款"
				}],
			"detail":"微众普通商品3的详情",
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
				"id":"0000011",
				"password":"1234567",
				"status":"未使用",
				"price":20.00
			},{
				"id":"0000012",
				"password":"2234567",
				"status":"未使用",
				"price":20.00
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
			"cards":
				[{
					"id":"0000001",
					"password":"1234567"
				},{
					"id":"0000002",
					"password":"2234567"
				}],
			"create_time":"今天"
		}]
		"""
	When bill关注jobs的公众号
	When tom关注jobs的公众号
	#订单数据
		#001-已完成，微众虚拟商品1
			When bill访问jobs的webapp
			And bill购买jobs的商品
				"""
				{
					"order_id": "001",
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
		#002-待发货，微众普通商品2
			When bill访问jobs的webapp
			And bill购买jobs的商品
				"""
				{
					"order_id": "002",
					"products": [{
						"name": "微众普通商品2",
						"count": 1
					}],
					"pay_type":"货到付款",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦"
				}
				"""
		#003-已发货，微众普通商品3
			When tom访问jobs的webapp
			And tom购买jobs的商品
				"""
				{
					"order_id": "003",
					"products": [{
						"name": "微众普通商品3",
						"count": 1
					}],
					"pay_type":"货到付款",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦"
				}
				"""
			When tom使用支付方式'微信支付'进行支付订单'003'
			Given jobs登录系统
			When jobs对订单进行发货
				"""
				{
					"order_no": "003",
					"logistics": "申通快递",
					"number": "001",
					"shipper": "jobs"
				}
				"""

@welfare_card @weizoom
Scenario:1 经营概况-店铺经营报告（不统计微众卡相关的订单）
	Given jobs登录系统
	When jobs设置筛选日期
		"""
		[{
			"begin_date":"5天前",
			"end_date":"今天"
		}]
		"""
	And 查询'店铺经营概况'
	Then 获得店铺经营概况数据
		"""
		{
			"buyer_count": 2,
			"transaction_money": "50.00",
			"vis_price": "25.00",
			"transaction_orders": 2
		}
		"""