# watcher: benchi@weizoom.com, zhangsanxiang@weizoom.com
#_author_:张三香 2016.05.20

Feature:微众商城添加虚拟商品
	"""
		0、特别备注：该功能给微众商城开放
		1、新建/编辑商品页面增加'商品类型'字段，包含普通、虚拟和微众卡三种类型
			普通:为正常的商品
			虚拟:是指第三方的卡密，如影票、蛋糕券
			微众卡:实际上也是虚拟的一种，单拿出来是因为微众卡只能单独下单，并且数据罗盘里不统计微众卡订单的数据，不然拿这批购买的微众卡再来买别的东西时，销售额会统计两遍
		2、虚拟和微众卡类型的商品创建成功后，在售/待售商品列表，用"码"小图标来标识其为虚拟商品
		3、目前没有控制商品类型的修改（不管商品是否创建福利卡券，均可修改商品类型）因该功能只是微商城内部使用，会约束行为，暂不考虑这种场景
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

Scenario:1 微众商城添加虚拟商品
	#微众虚拟商品01-微众卡（有图标"码"）
	#微众普通商品02-普通（无图标"码"）
	#稻香村虚拟商品03-虚拟（有图标"码"）
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "微众普通商品01",
			"product_type":"普通",
			"is_virtual_product":"false",
			"supplier": "微众",
			"purchase_price": 9.00,
			"promotion_title": "普通商品",
			"categories": "分类1,分类2",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"on",
			"price": 10.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 100,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"postage":0.00,
			"pay_interfaces":
				[{
					"type": "在线支付"
				},{
					"type": "货到付款"
				}],
			"detail": "微众普通商品01的详情",
			"status": "在售"
		}, {
			"name": "微众虚拟商品02",
			"product_type":"微众卡",
			"is_virtual_product":"true",
			"supplier": "微众",
			"purchase_price": 19.00,
			"promotion_title": "20元微众卡",
			"categories": "分类2",
			"bar_code":"212233",
			"min_limit":1,
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
				}],
			"detail": "微众虚拟商品02的详情",
			"status": "在售"
		}, {
			"name": "稻香村虚拟商品03",
			"product_type":"虚拟",
			"is_virtual_product":"true",
			"supplier": "稻香村",
			"purchase_price": 29.00,
			"promotion_title": "稻香村代金券",
			"categories": "分类1",
			"bar_code":"312233",
			"min_limit":1,
			"is_member_product":"off",
			"price": 30.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 30,
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
			"detail": "稻香村虚拟商品03的详情",
			"status": "在售"
		}]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name":"稻香村虚拟商品03",
			"is_virtual_product":"true",
			"supplier": "稻香村"
		},{
			"name":"微众虚拟商品02",
			"is_virtual_product":"true",
			"supplier": "微众"
		},{
			"name":"微众普通商品01",
			"is_virtual_product":"false",
			"supplier": "微众"
		}]
		"""
	And jobs能获取商品'微众虚拟商品02'
		"""
		{
			"name": "微众虚拟商品02",
			"product_type":"微众卡",
			"is_virtual_product":"true",
			"supplier": "微众",
			"purchase_price": 19.00,
			"promotion_title": "20元微众卡",
			"categories": "分类2",
			"bar_code":"212233",
			"min_limit":1,
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
				}],
			"detail": "微众虚拟商品02的详情"
		}
		"""