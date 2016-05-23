# watcher: benchi@weizoom.com, zhangsanxiang@weizoom.com
#_author_:张三香 2016.05.23

Feature:查看含虚拟商品的订单列表
	"""
		1、订单列表页的虚拟商品(电影票等第三方的密卡)显示"码"图标（备注-购买此类商品，无法实现steps）
		2、订单列表页的微众卡商品显示"卡"图标
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
			"name": "微众虚拟商品2",
			"product_type":"微众卡",
			"supplier": "微众",
			"purchase_price": 19.00,
			"promotion_title": "20元通用卡",
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
			"detail": "微众虚拟商品2的详情",
			"status": "在售"
		},{
			"name": "稻香村虚拟商品3",
			"product_type":"虚拟",
			"supplier": "稻香村",
			"purchase_price": 30.00,
			"promotion_title": "稻香村代金券",
			"categories": "分类2",
			"bar_code":"312233",
			"min_limit":1,
			"is_member_product":"off",
			"price": 30.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 2,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.00,
			"pay_interfaces":
				[{
					"type": "在线支付"
				}],
			"detail":"稻香村虚拟商品3的详情",
			"status":"在售"
		},{
			"name": "微众普通商品4",
			"product_type":"普通",
			"supplier": "微众",
			"purchase_price": 40.00,
			"promotion_title": "非虚拟商品",
			"categories": "分类2",
			"bar_code":"412233",
			"min_limit":1,
			"is_member_product":"off",
			"price": 40.00,
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
			"detail":"微众普通商品4的详情",
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
			"creat_time":"今天"
		},{
			"product":
				{
					"name":"微众虚拟商品2",
					"bar_code":"212233",
					"price":20.00
				},
			"activity_name":"20元通用卡",
			"card_start_date":"今天",
			"card_end_date":"35天后",
			"cards":
				[{
					"id":"0000011",
					"password":"1234567"
				},{
					"id":"0000012",
					"password":"2234567"
				}],
			"creat_time":"今天"
		}]
		"""
	When bill关注jobs的公众号
	When tom关注jobs的公众号

Scenario:1 查看含虚拟商品的订单列表
	#bill购买微众卡商品
	When bill访问jobs的webapp
	When bill加入jobs的商品到购物车
		"""
		[{
			"name": "微众虚拟商品1",
			"count": 1
		},{
			"name": "微众虚拟商品2",
			"count": 1
		}]
		"""
	When bill从购物车发起购买操作
		"""
		{
			"action": "pay",
			"context": [{
				"name": "微众虚拟商品1"
			}, {
				"name": "微众虚拟商品2"
			}]
		}
		"""
	And bill在购物车订单编辑中点击提交订单
		"""
		{
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "货到付款",
			"order_id": "001",
			"date":"今天"
		}
		"""
	Given jobs登录系统
	When jobs自动发放卡券给订单'001'
		"""
		[{
			"id":"0000001",
			"password":"1234567"
		},{
			"id":"0000011",
			"password":"1234567"
		}]
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no":"001",
			"final_price":30.00,
			"status":"已完成",
			"products": [{
				"name": "微众虚拟商品1",
				"price":10.00,
				"count": 1,
				"type":"微众卡",
				"supplier": "微众",
				"is_sync_supplier": "false",
				"status":"已完成"
			},{
				"name": "微众虚拟商品2",
				"price":20.00,
				"count": 1,
				"type":"微众卡",
				"supplier": "微众",
				"is_sync_supplier": "false",
				"status":"已完成"
			}]
		}]
		"""
	And jobs能获得订单'001'
		"""
		{
			"order_no": "001",
			"status":"已完成",
			"final_price": 30.00,
			"products": [{
				"name": "微众虚拟商品1",
				"price":10.00,
				"count": 1,
				"type":"微众卡",
				"supplier": "微众",
				"is_sync_supplier": "false",
				"status":"已完成"
			},{
				"name": "微众虚拟商品2",
				"price":20.00,
				"count": 1,
				"type":"微众卡",
				"supplier": "微众",
				"is_sync_supplier": "false",
				"status":"已完成"
			}]
		}
		"""
	#tom购买普通商品
	When tom访问jobs的webapp
	And tom购买jobs的商品
		"""
		{
			"order_id": "002",
			"products": [{
				"name": "微众普通商品4",
				"count": 1
			}],
			"pay_type":"微信支付",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
	When bill使用支付方式'微信支付'进行支付订单'002'
	Then jobs可以看到订单列表
		"""
		[{
			"order_no":"002",
			"final_price":40.00,
			"status":"待发货",
			"products": [{
				"name": "微众普通商品4",
				"price":40.00,
				"count": 1,
				"type":"普通",
				"supplier": "微众",
				"is_sync_supplier": "false",
				"status": "待发货"
			}]
		},{
			"order_no":"001",
			"final_price":30.00,
			"status":"已完成",
			"products": [{
				"name": "微众虚拟商品1",
				"price":10.00,
				"count": 1,
				"type":"微众卡",
				"supplier": "微众",
				"is_sync_supplier": "false",
				"status": "已完成"
			},{
				"name": "微众虚拟商品2",
				"price":20.00,
				"count": 1,
				"type":"微众卡",
				"supplier": "微众",
				"is_sync_supplier": "false",
				"status": "已完成"
			}]
		}]
		"""