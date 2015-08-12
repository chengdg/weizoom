@func:webapp.modules.mall.views.list_products
Feature: Add Product
	Jobs能通过管理系统在商城中添加"商品"

Background:
	Given jobs登录系统
	And jobs已添加商品分类
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

@mall2 @mall.product @after_rebuild @zy_ap01
Scenario: 添加商品
	Jobs添加商品后，能获取他添加的商品

	Given jobs登录系统
	And jobs已添加商品
		#东坡肘子(有分类，上架，无限库存，多轮播图), 叫花鸡(无分类，下架，有限库存，单轮播图)
		"""
		[{
			"name": "东坡肘子",
			"promotion_title": "促销的东坡肘子",
			"category": "分类1,分类2,分类3",
			"detail": "东坡肘子的详情",
			"status": "待售",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
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
			"detail": "叫花鸡的详情",
			"status": "待售",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
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
	When jobs添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00
		}]
		"""
	#When jobs选择'顺丰'运费配置
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"category": "分类1,分类2,分类3",
			"detail": "东坡肘子的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
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
	And jobs能获取商品'叫花鸡'
		"""
		{
			"name": "叫花鸡",
			"category": "",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"introduction": "",
			"detail": "叫花鸡的详情",
			"shelve_type": "下架",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
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
	Given bill登录系统
	Then bill能获取商品列表
		"""
		[]
		"""


@mall2 @mall.product @zy_ap02
Scenario: 添加'免运费'配置的商品
	Jobs添加商品后，能获取他添加的商品

	Given jobs登录系统
	And jobs已添加商品
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
	Then jobs能获取商品'红烧肉'
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

@mall2 @mall.product @zy_ap03
Scenario: 添加商品按倒序排列
	Jobs添加多个商品后，"商品列表"会按照添加的顺序倒序排列

	Given jobs已添加商品
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
		}, {
			"name": "商品3"
		}]
		"""
	Then jobs能获取商品列表
		"""
		[{
			"name": "商品3"
		}, {
			"name": "商品2"
		}, {
			"name": "商品1"
		}]
		"""
	Given bill登录系统
	Then bill能获取商品列表
		"""
		[]
		"""
