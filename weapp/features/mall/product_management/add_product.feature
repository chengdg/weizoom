#watcher:wangli@weizoom.com,benchi@weizoom.com
#editor：王丽 2015.10.14

@func:webapp.modules.mall.views.list_products
Feature: 添加新商品
"""
	Add Product
	Jobs能通过管理系统在商城中添加"商品"
"""

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
	And jobs已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"name": "白色",
				"image": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
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
		},{
			"type": "支付宝",
			"is_active": "启用"
		}]
		"""

@mall2 @product @addProduct   @mall.product @after_rebuild @zy_ap01
Scenario:1 添加商品
	Jobs添加商品后，能获取他添加的商品

	Given jobs登录系统
	And jobs已添加商品
		#东坡肘子(有分类，上架，无限库存，多轮播图), 叫花鸡(无分类，下架，有限库存，单轮播图)
		"""
		[{
			"name": "东坡肘子",
			"promotion_title": "促销的东坡肘子",
			"categories": "分类1,分类2,分类3",
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

@mall2 @product @addProduct   @mall.product @zy_ap02
Scenario:2 添加'免运费'配置的商品
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

@mall2 @product @addProduct   @mall.product @zy_ap03
Scenario:3 添加商品按倒序排列
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

# __author__ : "冯雪静"
@mall2 @product @addProduct
Scenario:4 添加有会员折扣的商品
	jobs添加会员折扣的商品后，能获取他添加的商品

	#系统默认一个会员等级"普通会员"、"自动升级"、
	#"所有关注过您的公众号的用户"、"购物折扣：10.0"
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""

	#添加的商品使用了会员等级折扣
	Given jobs登录系统
	When jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"is_member_product": "on",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "商品2",
			"is_member_product": "on",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 300,
						"stock_type": "无限"
					},
					"S": {
						"price": 300,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	Then jobs能获取商品'商品1'
		"""
		{
			"name": "商品1",
			"is_member_product": "on",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}
		"""
	Then jobs能获取商品'商品2'
		"""
		{
			"name": "商品2",
			"is_member_product": "on",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 300,
						"stock_type": "无限"
					},
					"S": {
						"price": 300,
						"stock_type": "无限"
					}
				}
			}
		}
		"""

#_author_:王丽 2016.01.20
@mall2 @product @addProduct
Scenario:5 添加'配送时间'配置的商品
	Jobs添加商品后，能获取他添加的商品

	Given jobs登录系统
	When jobs已添加商品
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
			"postage": "免运费",
			"distribution_time":"on"
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
			"postage": "免运费",
			"distribution_time":"on"
		}
		"""

	When jobs已添加商品
		"""
		[{
			"name": "红烧肉-无配送时间",
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
			"postage": "免运费",
			"distribution_time":"off"
		}]
		"""
	Then jobs能获取商品'红烧肉-无配送时间'
		"""
		{
			"name": "红烧肉-无配送时间",
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
			"postage": "免运费",
			"distribution_time":"off"
		}
		"""

#_author_:张三香 2016.01.20
@mall2 @product @addProduct
Scenario:6 添加无规格新商品,支持开票
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "支持开票商品",
			"category": "",
			"detail": "商品的详情",
			"status": "待售",
			"invoice":true,
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
	Then jobs能获取商品'支持开票商品'
		"""
		{
			"name": "支持开票商品",
			"category": "",
			"detail": "商品的详情",
			"invoice":true,
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

@mall2 @product @addProduct 
Scenario:7 添加多规格新商品,支持开票
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "多规格支持开票",
			"is_enable_model": "启用规格",
			"invoice":true,
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 S": {
						"price": 9.1,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	Then jobs能获取商品'多规格支持开票'
		"""
		{
			"is_enable_model": "启用规格",
			"invoice":true,
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 S": {
						"price": 9.1,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		}
		"""

@mall2 @product @addProduct 
Scenario:8 添加新商品,不支持开票
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "不支持开票商品",
			"category": "",
			"detail": "商品的详情",
			"status": "待售",
			"invoice":false,
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
	Then jobs能获取商品'不支持开票商品'
		"""
		{
			"name": "不支持开票商品",
			"category": "",
			"detail": "商品的详情",
			"invoice":false,
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
