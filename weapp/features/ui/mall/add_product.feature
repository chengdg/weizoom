@func:webapp.modules.mall.views.list_products
Feature: Add Product
	Jobs能通过管理系统在商城中添加"商品"

Background:
	Given jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	When jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用",
			"weixin_appid": "12345",
			"weixin_partner_id": "22345",
			"weixin_partner_key": "32345",
			"weixin_sign": "42345"
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
	And jobs登录系统:ui


@ui @ui-mall @ui-mall.product
Scenario: 添加商品
	Jobs添加商品后，能获取他添加的商品

	When jobs添加商品:ui
		#东坡肘子(有分类，上架，无限库存，多轮播图), 叫花鸡(无分类，下架，有限库存，单轮播图)
		"""
		[{
			"name": "东坡肘子",
			"category": "分类1",
			"physical_unit": "包",
			"thumbnails_url": "./test/imgs/hangzhou1.jpg",
			"pic_url": "./test/imgs/hangzhou1.jpg",
			"introduction": "东坡肘子的简介",
			"detail": "东坡肘子的详情",
			"remark": "东坡肘子的备注",
			"shelve_type": "上架",
			"swipe_images": [{
				"url": "./test/imgs/hangzhou1.jpg"
			}, {
				"url": "./test/imgs/hangzhou1.jpg"
			}, {
				"url": "./test/imgs/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"category": "",
			"physical_unit": "盘",
			"price": 12.0,
			"weight": 5.5,
			"thumbnails_url": "./test/imgs/hangzhou2.jpg",
			"pic_url": "./test/imgs/hangzhou2.jpg",
			"introduction": "叫花鸡的简介",
			"detail": "叫花鸡的详情",
			"shelve_type": "下架",
			"stock_type": "有限",
			"stocks": 3,
			"swipe_images": [{
				"url": "./test/imgs/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"weight": 5.5,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}]
		"""
	Then jobs能获取商品'东坡肘子':ui
		"""
		{
			"name": "东坡肘子",
			"category": "分类1",
			"physical_unit": "包",
			"detail": "东坡肘子的详情",
			"remark": "东坡肘子的备注",
			"shelve_type": "上架",
			"is_use_custom_model": "否",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	And jobs能获取商品'叫花鸡':ui
		"""
		{
			"name": "叫花鸡",
			"category": "",
			"physical_unit": "盘",
			"detail": "叫花鸡的详情",
			"shelve_type": "下架",
			"is_use_custom_model": "否",
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"weight": 5.5,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}
		"""
	Given bill登录系统:ui
	Then bill能获取商品列表:ui
		"""
		[]
		"""


@ui @ui-mall @ui-mall.product
Scenario: 添加商品按倒序排列
	Jobs添加多个商品后，"商品列表"会按照添加的顺序倒序排列

	Given jobs登录系统
	When "jobs"添加商品
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
		}, {
			"name": "商品3"
		}]
		"""
	Then jobs能获取商品列表:ui
		"""
		[{
			"name": "商品3"
		}, {
			"name": "商品2"
		}, {
			"name": "商品1"
		}]
		"""
	Given bill登录系统:ui
	Then bill能获取商品列表:ui
		"""
		[]
		"""

Scenario: 添加'免运费'配置的商品
	Jobs添加商品后，能获取他添加的商品

	Given jobs登录系统:ui
	And jobs已添加商品:ui
		"""
		[{
			"name": "红烧肉",
			"category": "",
			"price": 12.0,
			"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"introduction": "红烧肉的简介",
			"detail": "红烧肉的详情",
			"shelve_type": "上架",
			"stock_type": "有限",
			"stocks": 3,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"weight": 5.5,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			},
			"postage": "免运费"
		}]
		"""
	Then jobs能获取商品'红烧肉':ui
		"""
		{
			"name": "红烧肉",
			"category": "",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"detail": "红烧肉的详情",
			"shelve_type": "上架",
			"stock_type": "有限",
			"stocks": 3,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"weight": 5.5,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			},
			"pay_interfaces":[{
				"type": "在线支付"
			},{
				"type": "货到付款"
			}],
			"postage": "免运费"
		}
		"""
