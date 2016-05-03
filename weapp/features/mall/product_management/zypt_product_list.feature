# watcher: fengxuejing@weizoom.com
#_author_:冯雪静

Feature: 自营平台在售商品列表页
	"""
	在售商品列表页：
		1.商品信息-供货商-分组-商品价格-库存-总销量-同步时间-排序-操作
		2.商户(供货商)下架商品，在售列表中此商品自动删除(钉钉通知运营人员)
		3.商户(供货商)删除商品，在售列表中此商品自动删除(钉钉通知运营人员)
		4.商户(供货商)修改商品为多规格，在售列表中此商品自动删除(钉钉通知运营人员)
		5.在商品池更新之后，(采购价，库存，总销量，分组，会员折扣，运费，支付方式，保留更新之前设置的数值)，别的修改项更新之后被覆盖，商品回到待售列表
		5.供货商查询，同步时间查询
	"""
#特殊说明：jobs，nokia表示自营平台，bill，tom表示商家,tom1表示用户
Background:
	#商家bill的商品信息
	Given 添加bill店铺名称为'bill商家'
	Given bill登录系统
	When bill已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	And bill添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00
		}]
		"""
	And bill选择'顺丰'运费配置
	And bill添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	And bill已添加商品规格
		"""
		[{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	And bill添加属性模板
		"""
		[{
			"name": "计算机模板",
			"properties": [{
				"name": "CPU",
				"description": "CPU描述"
			}, {
				"name": "内存",
				"description": "内存描述"
			}]
		},{
			"name": "大米模板",
			"properties": [{
				"name": "产地",
				"description": "产地描述"
			}]
		}]
		"""
	And bill已添加商品
		"""
		[{
			"name": "bill无规格商品1",
			"created_at": "2015-07-02 10:20",
			"promotion_title": "促销的东坡肘子",
			"categories": "分类1,分类2,分类3",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"on",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":10.00,
			"pay_interfaces":[{
					"type": "在线支付"
				},{
					"type": "货到付款"
				}],
			"invoice":true,
			"distribution_time":"on",
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息",
			"status": "在售"
		},{
			"name": "bill无规格商品2",
			"created_at": "2015-07-03 10:20",
			"promotion_title": "促销的叫花鸡",
			"categories": "分类1,分类3",
			"bar_code":"2123456",
			"min_limit":2,
			"is_member_product":"on",
			"model": {
				"models": {
					"standard": {
						"price": 22.12,
						"user_code":"2212",
						"weight":1.0,
						"stock_type": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":10.00,
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"invoice":true,
			"distribution_time":"on",
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息",
			"status": "待售"
		},{
			"name": "bill无规格商品3",
			"created_at": "2015-07-04 10:20",
			"promotion_title": "促销的蜜桔",
			"categories": "",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":100
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage": "顺丰",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"invoice":true,
			"distribution_time":"on",
			"properties": [{
					"name": "规格大小",
					"description": "规格大小描述"
				}, {
					"name": "产地",
					"description": "产地描述"
				}],
			"detail": "商品描述信息",
			"status": "在售"
		},{
			"name": "bill多规格商品4",
			"created_at": "2015-07-05 10:20",
			"promotion_title": "促销的苹果",
			"categories": "分类1",
			"bar_code":"4123456",
			"min_limit":2,
			"is_member_product":"off",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"M": {
						"price": 44.12,
						"user_code":"4412",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":100
					},
					"S": {
						"price": 44.13,
						"user_code":"4413",
						"weight":1.0,
						"stock_type": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":10.00,
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"invoice":true,
			"distribution_time":"on",
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息",
			"status": "在售"
		}]
		"""

	#商家tom的商品信息
	Given 添加tom店铺名称为'tom商家'
	Given tom登录系统
	When tom已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}]
		"""
	And tom添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00
		}]
		"""
	And tom选择'顺丰'运费配置
	And tom添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	And tom已添加商品规格
		"""
		[{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	And tom添加属性模板
		"""
		[{
			"name": "计算机模板",
			"properties": [{
				"name": "CPU",
				"description": "CPU描述"
			}, {
				"name": "内存",
				"description": "内存描述"
			}]
		},{
			"name": "大米模板",
			"properties": [{
				"name": "产地",
				"description": "产地描述"
			}]
		}]
		"""
	And tom已添加商品
		"""
		[{
			"name": "tom无规格商品1",
			"created_at": "2015-07-02 10:20",
			"promotion_title": "促销的东坡肘子",
			"categories": "分类1,分类2,分类3",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"on",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":10.00,
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"invoice":true,
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息",
			"status": "在售"
		},{
			"name": "tom无规格商品2",
			"created_at": "2015-07-03 10:20",
			"promotion_title": "促销的叫花鸡",
			"categories": "分类1,分类3",
			"bar_code":"2123456",
			"min_limit":2,
			"is_member_product":"on",
			"model": {
				"models": {
					"standard": {
						"price": 22.12,
						"user_code":"2212",
						"weight":1.0,
						"stock_type": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":10.00,
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"invoice":true,
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息",
			"status": "待售"
		},{
			"name": "tom无规格商品3",
			"created_at": "2015-07-04 10:20",
			"promotion_title": "促销的蜜桔",
			"categories": "",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":100
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage": "顺丰",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"invoice":true,
			"properties": [{
					"name": "规格大小",
					"description": "规格大小描述"
				}, {
					"name": "产地",
					"description": "产地描述"
				}],
			"detail": "商品描述信息",
			"status": "在售"
		},{
			"name": "tom多规格商品4",
			"created_at": "2015-07-05 10:20",
			"promotion_title": "促销的苹果",
			"categories": "分类1",
			"bar_code":"4123456",
			"min_limit":2,
			"is_member_product":"off",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"M": {
						"price": 44.12,
						"user_code":"4412",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":100
					},
					"S": {
						"price": 44.13,
						"user_code":"4413",
						"weight":1.0,
						"stock_type": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":10.00,
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"invoice":true,
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息",
			"status": "在售"
		}]
		"""

	#自营平台jobs登录
	Given 设置jobs为自营平台账号
	Given jobs登录系统
	When jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	And jobs已添加商品分类
		"""
		[{
			"name": "分组1"
		},{
			"name": "分组2"
		},{
			"name": "分组3"
		}]
		"""

	#自营平台nokia登录
	Given 设置nokia为自营平台账号
	Given nokia登录系统
	When nokia已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	And nokia已添加商品分类
		"""
		[{
			"name": "分组1"
		},{
			"name": "分组2"
		},{
			"name": "分组3"
		}]
		"""

@mall2 @product_pool @eugene
Scenario:1 自营平台把商品从商品池放入待售商品列表上架商品，获取在售商品列表
	#自营平台jobs登录
	Given jobs登录系统
	When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
	And jobs将商品'tom无规格商品1'放入待售于'2015-08-02 11:30'
	And jobs将商品池商品批量放入待售于'2015-08-02 12:30'
		"""
		[
			"tom无规格商品3", "bill无规格商品3"
		]
		"""
	When jobs更新商品'tom无规格商品3'
		"""
		{
			"name": "tom商品3",
			"supplier":"tom商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的蜜桔",
			"categories": "分组1",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":"免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "规格大小",
					"description": "规格大小描述"
				}, {
					"name": "产地",
					"description": "产地描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'tom无规格商品1'
		"""
		{
			"name": "tom商品1",
			"supplier":"tom商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的东坡肘子",
			"categories": "分组1",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":"免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'bill无规格商品3'
		"""
		{
			"name": "bill商品3",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的蜜桔",
			"categories": "分组2",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage": "免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "规格大小",
					"description": "规格大小描述"
				}, {
					"name": "产地",
					"description": "产地描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'bill无规格商品1'
		"""
		{
			"name": "bill商品1",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的东坡肘子",
			"categories": "分组2",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":10.00,
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs批量上架商品
		"""
		[
			"tom商品3",
			"tom商品1",
			"bill商品3",
			"bill商品1"
		]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "tom商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 33.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "bill商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": ["分组2"],
			"price": 33.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "tom商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 11.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "bill商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": ["分组2"],
			"price": 11.12,
			"stock_type": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		}]
		"""

@mall2 @product_pool @eugene
Scenario:2 自营平台把商品从商品池放入待售商品列表上架后，商户(供货商)下架商品和删除商品
	#自营平台jobs登录
	Given jobs登录系统
	When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
	And jobs将商品'tom无规格商品1'放入待售于'2015-08-02 11:30'
	And jobs将商品池商品批量放入待售于'2015-08-02 12:30'
		"""
		[
			"tom无规格商品3", "bill无规格商品3"
		]
		"""
	And jobs更新商品'tom无规格商品3'
		"""
		{
			"name": "tom商品3",
			"supplier":"tom商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的蜜桔",
			"categories": "分组1",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":"免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "规格大小",
					"description": "规格大小描述"
				}, {
					"name": "产地",
					"description": "产地描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'tom无规格商品1'
		"""
		{
			"name": "tom商品1",
			"supplier":"tom商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的东坡肘子",
			"categories": "分组1",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":"免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'bill无规格商品3'
		"""
		{
			"name": "bill商品3",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的蜜桔",
			"categories": "分组2",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage": "免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "规格大小",
					"description": "规格大小描述"
				}, {
					"name": "产地",
					"description": "产地描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'bill无规格商品1'
		"""
		{
			"name": "bill商品1",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的东坡肘子",
			"categories": "分组2",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":10.00,
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs批量上架商品
		"""
		[
			"tom商品3",
			"tom商品1",
			"bill商品3",
			"bill商品1"
		]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "tom商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 33.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "bill商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": ["分组2"],
			"price": 33.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "tom商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 11.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "bill商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": ["分组2"],
			"price": 11.12,
			"stock_type": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		}]
		"""

	#商家tom的商品信息
	Given tom登录系统
	When tom'下架'商品'tom无规格商品3'

	#商家bill的商品信息
	Given bill登录系统
	When bill'永久删除'商品'bill无规格商品3'

	#自营平台jobs登录
	Given jobs登录系统
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "tom商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 11.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "bill商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": ["分组2"],
			"price": 11.12,
			"stock_type": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		}]
		"""

@mall2 @product_pool @eugene
Scenario:3 自营平台把商品从商品池放入待售商品列表上架后，商户(供货商)修改商品为多规格
	#自营平台jobs登录
	Given jobs登录系统
	When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
	And jobs将商品'tom无规格商品1'放入待售于'2015-08-02 11:30'
	And jobs将商品池商品批量放入待售于'2015-08-02 12:30'
		"""
		[
			"tom无规格商品3",
			"bill无规格商品3"
		]
		"""
	And jobs更新商品'tom无规格商品3'
		"""
		{
			"name": "tom商品3",
			"supplier":"tom商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的蜜桔",
			"categories": "分组1",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":"免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "规格大小",
					"description": "规格大小描述"
				}, {
					"name": "产地",
					"description": "产地描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'tom无规格商品1'
		"""
		{
			"name": "tom商品1",
			"supplier":"tom商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的东坡肘子",
			"categories": "分组1",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":"免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'bill无规格商品3'
		"""
		{
			"name": "bill商品3",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的蜜桔",
			"categories": "分组2",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage": "免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "规格大小",
					"description": "规格大小描述"
				}, {
					"name": "产地",
					"description": "产地描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'bill无规格商品1'
		"""
		{
			"name": "bill商品1",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的东坡肘子",
			"categories": "分组2",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":10.00,
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs批量上架商品
		"""
		[
			"tom商品3",
			"tom商品1",
			"bill商品3",
			"bill商品1"
		]
		"""

	#商家tom的商品信息
	Given tom登录系统
	#修改商品为多规格
	When tom更新商品'tom无规格商品3'
		"""
		{
			"name": "tom多规格商品3",
			"created_at": "2015-07-05 10:20",
			"promotion_title": "促销的苹果",
			"categories": "分类1",
			"bar_code":"4123456",
			"min_limit":2,
			"is_member_product":"off",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"M": {
						"price": 44.12,
						"user_code":"4412",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":100
					},
					"S": {
						"price": 44.13,
						"user_code":"4413",
						"weight":1.0,
						"stock_type": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":10.00,
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"invoice":true,
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息",
			"status": "在售"
		}
		"""

	#自营平台jobs登录
	Given jobs登录系统
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "bill商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": ["分组2"],
			"price": 33.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "tom商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 11.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "bill商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": ["分组2"],
			"price": 11.12,
			"stock_type": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		}]
		"""

@mall2 @product_pool @eugene
Scenario:4 自营平台把商品从商品池放入待售商品列表上架后，用户购买商品,商户(供货商)修改商品，自营平台更新商品再上架
	#自营平台jobs登录
	Given jobs登录系统
	When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
	And jobs将商品'tom无规格商品1'放入待售于'2015-08-02 11:30'
	And jobs将商品池商品批量放入待售于'2015-08-02 12:30'
		"""
		[
			"tom无规格商品3",
			"bill无规格商品3"
		]
		"""
	And jobs更新商品'tom无规格商品3'
		"""
		{
			"name": "tom商品3",
			"supplier":"tom商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的蜜桔",
			"categories": "分组1",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":"免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "规格大小",
					"description": "规格大小描述"
				}, {
					"name": "产地",
					"description": "产地描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'tom无规格商品1'
		"""
		{
			"name": "tom商品1",
			"supplier":"tom商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的东坡肘子",
			"categories": "分组1",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":"免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'bill无规格商品3'
		"""
		{
			"name": "bill商品3",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的蜜桔",
			"categories": "分组2",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage": "免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "规格大小",
					"description": "规格大小描述"
				}, {
					"name": "产地",
					"description": "产地描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'bill无规格商品1'
		"""
		{
			"name": "bill商品1",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的东坡肘子",
			"categories": "分组2",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":10.00,
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs批量上架商品
		"""
		[
			"tom商品3",
			"tom商品1",
			"bill商品3",
			"bill商品1"
		]
		"""

	#tom1用户登录
	Given tom1关注jobs的公众号
	When tom1访问jobs的webapp
	And tom1购买jobs的商品
		"""
		{
			"pay_type":"微信支付",
			"products": [{
				"name": "tom商品3",
				"count": 2
			}]
		}
		"""
	And tom1使用支付方式'微信支付'进行支付
	Given jobs登录系统
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "tom商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 33.12,
			"stocks":97,
			"sales": 2,
			"sync_time":"2015-08-02 12:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "bill商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": ["分组2"],
			"price": 33.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "tom商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 11.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "bill商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": ["分组2"],
			"price": 11.12,
			"stock_type": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		}]
		"""

	#商家tom的商品信息
	Given tom登录系统
	#修改商品金额
	When tom更新商品'tom无规格商品3'
		"""
		{
			"name": "tom无规格商品3",
			"created_at": "2015-07-04 10:20",
			"promotion_title": "促销的蜜桔",
			"categories": "",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 99.99,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":100
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage": "顺丰",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"invoice":true,
			"properties": [{
					"name": "规格大小",
					"description": "规格大小描述"
				}, {
					"name": "产地",
					"description": "产地描述"
				}],
			"detail": "商品描述信息",
			"status": "在售"
		}
		"""

	#自营平台jobs登录
	Given jobs登录系统
	When jobs更新商品池商品'tom无规格商品3'于'2015-08-03 12:30'
	#跟新商品后，库存，销量，采购价，分组保留之前数据
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "tom无规格商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 99.99,
			"stocks":97,
			"sales": 2,
			"sync_time":"2015-08-03 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""
	When jobs'上架'商品'tom无规格商品3'
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "tom无规格商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 99.99,
			"stocks":97,
			"sales": 2,
			"sync_time":"2015-08-03 12:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "bill商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": ["分组2"],
			"price": 33.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "tom商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 11.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "bill商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": ["分组2"],
			"price": 11.12,
			"stock_type": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		}]
		"""

@mall2 @product_pool @eugene
Scenario:5 在售商品列表查询
	#自营平台jobs登录
	Given jobs登录系统
	When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
	And jobs将商品'tom无规格商品1'放入待售于'2015-08-02 11:30'
	And jobs将商品池商品批量放入待售于'2015-08-02 12:30'
		"""
		[
			"tom无规格商品3",
			"bill无规格商品3"
		]
		"""
	When jobs更新商品'tom无规格商品3'
		"""
		{
			"name": "tom商品3",
			"supplier":"tom商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的蜜桔",
			"categories": "分组1",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":"免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "规格大小",
					"description": "规格大小描述"
				}, {
					"name": "产地",
					"description": "产地描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'tom无规格商品1'
		"""
		{
			"name": "tom商品1",
			"supplier":"tom商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的东坡肘子",
			"categories": "分组1",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":"免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'bill无规格商品3'
		"""
		{
			"name": "bill商品3",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的蜜桔",
			"categories": "分组2",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage": "免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "规格大小",
					"description": "规格大小描述"
				}, {
					"name": "产地",
					"description": "产地描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'bill无规格商品1'
		"""
		{
			"name": "bill商品1",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的东坡肘子",
			"categories": "分组2",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":10.00,
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs批量上架商品
		"""
		[
			"tom商品3",
			"tom商品1",
			"bill商品3",
			"bill商品1"
		]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "tom商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 33.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "bill商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": ["分组2"],
			"price": 33.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "tom商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 11.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "bill商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": ["分组2"],
			"price": 11.12,
			"stock_type": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		}]
		"""

	#供货商模糊查询
	When jobs设置商品查询条件
		"""
		{
			"supplier": "tom"
		}
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "tom商品3"
		},{
			"name": "tom商品1"
		}]
		"""

	#供货商精确查询
	When jobs设置商品查询条件
		"""
		{
			"supplier": "bill商家"
		}
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "bill商品3"
		},{
			"name": "bill商品1"
		}]
		"""

	#输入错误供货商查询
	When jobs设置商品查询条件
		"""
		{
			"supplier": "bill  商家"
		}
		"""
	Then jobs能获得'在售'商品列表
		"""
		[]
		"""

	#同步时间查询
	When jobs设置商品查询条件
		"""
		{
			"startDate":"2015-08-01 00:00",
			"endDate":"2015-08-03 00:00"
		}
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "tom商品3"
		},{
			"name": "bill商品3"
		},{
			"name": "tom商品1"
		},{
			"name": "bill商品1"
		}]
		"""

	#同步时间查询
	When jobs设置商品查询条件
		"""
		{
			"startDate":"2015-08-01 00:00",
			"endDate":"2015-08-02 00:00"
		}
		"""
	Then jobs能获得'在售'商品列表
		"""
		[]
		"""

	#供货商和同步时间查询
	When jobs设置商品查询条件
		"""
		{
			"supplier": "bill商家",
			"startDate":"2015-08-01 00:00",
			"endDate":"2015-08-03 00:00"
		}
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "bill商品3"
		},{
			"name": "bill商品1"
		}]
		"""

#补充：张三香 2016.05.03
	#1.'在售商品列表'中同步商品的供货商名称前添加‘同’标签;自建供货商只显示供货商名称
	#2.增加筛选条件"供货商类型"：全部、同步供货商、自建供货商；默认"全部"

@product_pool @eugene
Scenario:6 在售商品列表按照'供货商类型'查询
	#自营平台jobs登录
	Given jobs登录系统
	And jobs已添加供货商
		"""
		[{
			"name": "供货商1",
			"responsible_person": "宝宝",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}, {
			"name": "供货商2",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}]
		"""

	When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
	And jobs将商品'tom无规格商品1'放入待售于'2015-08-02 11:30'
	And jobs更新商品'tom无规格商品1'
		"""
		{
			"name": "tom商品1",
			"supplier":"tom商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的东坡肘子",
			"categories": "分组1",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":"免运费",
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs更新商品'bill无规格商品1'
		"""
		{
			"name": "bill商品1",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"promotion_title": "促销的东坡肘子",
			"categories": "分组2",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"postage":10.00,
			"pay_interfaces":[{
					"type": "在线支付"
				}],
			"properties": [{
					"name": "CPU",
					"description": "CPU描述"
				}, {
					"name": "内存",
					"description": "内存描述"
				}],
			"detail": "商品描述信息"
		}
		"""
	And jobs批量上架商品
		"""
		[
			"tom商品1",
			"bill商品1"
		]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "tom商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"is_sync_supplier": "true",
			"categories": ["分组1"],
			"price": 11.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		},{
			"name": "bill商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"is_sync_supplier": "true",
			"categories": ["分组2"],
			"price": 11.12,
			"stock_type": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"display_index": 0,
			"actions": ["修改", "下架", "彻底删除"]
		}]
		"""
	Given jobs已添加商品
		"""
		[{
			"supplier": "供货商1",
			"name": "商品1a",
			"price": 10.00,
			"purchase_price": 9.00,
			"weight": 1.0,
			"stock_type": "无限",
			"pay_interfaces":[{
				"type": "货到付款"
			}]
		}, {
			"supplier": "供货商1",
			"name": "商品1b",
			"price": 20.00,
			"purchase_price": 19.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 10,
			"pay_interfaces":[{
				"type": "货到付款"
			}]
		}, {
			"supplier": "供货商2",
			"name": "商品2a",
			"price": 20.00,
			"purchase_price": 19.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 10,
			"pay_interfaces":[{
				"type": "货到付款"
			}]
		}]
		"""

	#供货商类型-全部
	When jobs设置商品查询条件
		"""
		{
			"supplier_type": "全部"
		}
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "商品2a",
			"supplier":"供货商2",
			"is_sync_supplier": "false"
		},{
			"name": "商品1b",
			"supplier":"供货商1",
			"is_sync_supplier": "false"
		},{
			"name": "商品1a",
			"supplier":"供货商1",
			"is_sync_supplier": "false"
		},{
			"name": "tom商品1",
			"supplier":"tom商家",
			"is_sync_supplier": "true"
		},{
			"name": "bill商品1",
			"supplier":"bill商家",
			"is_sync_supplier": "true"
		}]
		"""

	#供货商类型-同步供货商
	When jobs设置商品查询条件
		"""
		{
			"supplier_type": "同步供货商"
		}
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "tom商品1",
			"supplier":"tom商家",
			"is_sync_supplier": "true"
		},{
			"name": "bill商品1",
			"supplier":"bill商家",
			"is_sync_supplier": "true"
		}]
		"""

	#供货商类型-自建供货商
	When jobs设置商品查询条件
		"""
		{
			"supplier_type": "自建供货商"
		}
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "商品2a",
			"supplier":"供货商2",
			"is_sync_supplier": "false"
		},{
			"name": "商品1b",
			"supplier":"供货商1",
			"is_sync_supplier": "false"
		},{
			"name": "商品1a",
			"supplier":"供货商1",
			"is_sync_supplier": "false"
		}]
		"""