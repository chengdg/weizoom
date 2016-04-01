# watcher: fengxuejing@weizoom.com
#_author_:冯雪静

Feature: 自营平台待售商品列表页
	"""
	待售商品列表页：
		1.商品信息-供货商-分组-商品价格-库存-总销量-同步时间-操作
		2.同步过来的商品这些信息不同步(1.分组信息 2.会员折扣 3.运费设置 4.总销量 5.支付方式 6.发票设置 7.配送时间)
		3.商品列表排序：不填采购价的商品置顶-同步时间(放入待售的时间)自己创建商品时间倒序排列
		4.批量同步商品：按照商品池的顺序排列(商品池按照创建商品倒序排列)
		5.同步时间-以每次更新的时间为主
		6.下架后的商品还是按照现在的规则处理，最后下架的商品排列在不填采购价商品的下面
		7.批量下架的商品以同步时间和创建时间的倒序排列在不填采购价商品的下面
		8.商户(供货商)下架商品，待售列表中此商品自动删除(钉钉通知运营人员)
		9.商户(供货商)删除商品，待售列表中此商品自动删除(钉钉通知运营人员)
		10.商户(供货商)修改商品为多规格，待售列表中此商品自动删除(钉钉通知运营人员)
		11.自营平台彻底删除商户(供货商)提交的商品，对商户没有影响
		12.在待售列表修改商品，(供货商和属性不可修改)，采购价必填，商品池信息不变
		13.在商品池更新之后，(采购价，库存，总销量，分组，会员折扣，运费，支付方式，保留更新之前设置的数值)，别的修改项更新之后被覆盖
		14.商品上架后，更新商品，商品回到待售列表
		15.供货商查询，同步时间查询
	"""
#特殊说明：jobs，nokia表示自营平台，bill，tom表示商家
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
						"stocks": "无限"
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
						"stocks": "无限"
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
			"categories": [],
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
						"stocks": "无限"
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
						"stocks": "无限"
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
						"stocks": "无限"
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
			"categories": [],
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
						"stocks": "无限"
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

@eugene @product_pool
Scenario:1 自营平台把商品从商品池放入待售商品列表，获取待售商品列表
	jobs把商品放入待售列表，nokia把商品放入待售列表
	1.jobs获得商品池商品列表
	2.jobs能获得'待售'商品列表
	3.nokia获得商品池商品列表
	4.nokia能获得'待售'商品列表

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
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "tom无规格商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""

	#自营平台nokia登录
	Given nokia登录系统
	When nokia将商品池商品批量放入待售于'2015-08-02 12:30'
		"""
		[
			"tom无规格商品3",
			"bill无规格商品3"
		]
		"""
	Then nokia能获得'待售'商品列表
		"""
		[{
			"name": "tom无规格商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""

@eugene @product_pool
Scenario:2 自营平台修改待售列表的商品

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
	#(1.分组信息 2.会员折扣 3.运费设置 4.总销量 5.支付方式 6.发票设置 7.配送时间)这些信息不同步,更新后库存不同步
	Then jobs能获取商品'tom无规格商品3'
		"""
		{
			"name": "tom无规格商品3",
			"supplier":"tom商家",
			"purchase_price": "",
			"promotion_title": "促销的蜜桔",
			"categories": [],
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"bar_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":100
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.0,
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
	#修改商品名称，分组，采购价，商品编码，库存
	#供货商和属性不可修改
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
						"user_code":"3333",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.0,
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
	#优先显示未填写采购价的商品，填写完采购价才可以上架
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "bill无规格商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom商品3",
			"user_code": "3333",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 33.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""

	#自营平台nokia登录
	Given nokia登录系统
	When nokia将商品池商品批量放入待售于'2015-08-02 12:30'
		"""
		[
			"tom无规格商品3",
			"bill无规格商品3"
		]
		"""
	#(1.分组信息 2.会员折扣 3.运费设置 4.总销量 5.支付方式 6.发票设置)这些信息不同步,更新后库存不同步
	Then nokia能获取商品'bill无规格商品3'
		"""
		{
			"name": "bill无规格商品3",
			"supplier":"bill商家",
			"purchase_price": "",
			"promotion_title": "促销的蜜桔",
			"categories": [],
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"off",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"bar_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":100
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage": 0.0,
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
	#修改商品名称，分组，采购价，商品编码，库存，开启会员价，运费
	#供货商和属性不可修改
	When nokia更新商品'bill无规格商品3'
		"""
		{
			"name": "bill商品3",
			"supplier":"bill商家",
			"purchase_price": 11.00,
			"promotion_title": "促销的蜜桔",
			"categories": "分组1,分组2",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"on",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3111",
						"weight":1.0,
						"stocks": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage": 11.00,
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
	Then nokia能获得'待售'商品列表
		"""
		[{
			"name": "tom无规格商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill商品3",
			"user_code":"3111",
			"supplier":"bill商家",
			"categories": ["分组1","分组2"],
			"price": 33.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""

@eugene @product_pool
Scenario:3 自营平台把商品从商品池放入待售商品列表后，商户(供货商)修改商品
	bill修改商品后，tom修改商品后
	1.已放入待售列表，商品池更新，同步时间变更
	2.已放入待售列表并更新商品，商品池更新，商品数据被覆盖(除采购价和库存)

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

	#商家bill的商品信息
	Given bill登录系统
	#商户修改商品，商品池显示更新
	When bill更新商品'bill无规格商品1'
		"""
		{
			"name": "bill商品1",
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
						"stocks": "无限"
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
		}
		"""

	#自营平台jobs登录
	Given jobs登录系统
	When jobs更新商品池商品'bill商品1'于'2015-08-03 10:30'
	#同步时间-以每次更新的时间为主
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "bill商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-03 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""
	#修改商品名称，分组，采购价，商品编码，库存
	#供货商和属性不可修改
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
						"user_code":"3333",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.0,
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

	#商家tom的商品信息
	Given tom登录系统
	#修改商品金额
	When tom更新商品'tom无规格商品3'
		"""
		{
			"name": "tom无规格商品3",
			"created_at": "2015-07-04 10:20",
			"promotion_title": "促销的蜜桔",
			"categories": [],
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
	#同步时间-以每次更新的时间为主,(采购价，库存，总销量，分组，会员折扣，运费，支付方式，保留更新之前设置的数值)，别的修改项更新之后被覆盖
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "bill商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-03 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 99.99,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-03 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""
	#商户更新商品，商品池跟新后(商品名称，商品编码都被覆盖了)，库存、采购价、分组保留之前数据
	Then jobs能获取商品'tom无规格商品3'
		"""
		{
			"name": "tom无规格商品3",
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
						"price": 99.99,
						"bar_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.0,
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

@eugene @product_pool
Scenario:4 自营平台把商品从商品池放入待售商品列表后，商户(供货商)下架商品和删除商品
	商户下架商品和删除商品
	1.自营平台的商品池和待售列表自动删除此商品

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
	#商家tom的商品信息
	Given tom登录系统
	When tom'下架'商品'tom无规格商品3'

	#商家bill的商品信息
	Given bill登录系统
	When bill'永久删除'商品'bill无规格商品3'

	#自营平台jobs登录
	Given jobs登录系统
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""

@eugene @product_pool
Scenario:5 自营平台把商品从商品池放入待售商品列表后，商户(供货商)修改商品为多规格
	商户修改商品为多规格
	1.自营平台的商品池和待售列表自动删除此商品

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
						"stocks": "无限"
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
	Given jobs登录系统
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "bill无规格商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""

@eugene @product_pool
Scenario:6 自营平台把商品从商品池放入待售商品列表后，上架商品再下架
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
	#修改商品名称，分组，采购价，商品编码，库存
	#供货商和属性不可修改
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
						"user_code":"3333",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.0,
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
	And jobs更新商品'bill无规格商品3'
		"""
		{
			"name": "bill商品3",
			"supplier":"bill商家",
			"purchase_price": 11.00,
			"promotion_title": "促销的蜜桔",
			"categories": "分组1,分组2",
			"bar_code":"3123456",
			"min_limit":2,
			"is_member_product":"on",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3111",
						"weight":1.0,
						"stocks": "无限"
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage": 11.00,
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
	And jobs'上架'商品'tom商品3'
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill商品3",
			"user_code":"3111",
			"supplier":"bill商家",
			"categories": ["分组1","分组2"],
			"price": 33.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""
	When jobs'下架'商品'tom商品3'
	#上架后再下架的商品排在采购价后(未填采购价-最新下架-已填采购价)
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom商品3",
			"user_code": "3333",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 33.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill商品3",
			"user_code":"3111",
			"supplier":"bill商家",
			"categories": ["分组1","分组2"],
			"price": 33.12,
			"stocks":"无限",
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""

@eugene @product_pool
Scenario:7 自营平台把商品从商品池放入待售商品列表上架商品后，商户修改商品
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
	#修改商品名称，分组，采购价，商品编码，库存
	#供货商和属性不可修改
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
						"user_code":"3333",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.0,
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
	And jobs'上架'商品'tom商品3'
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "bill无规格商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""

	Given tom登录系统
	#修改商品金额
	When tom更新商品'tom无规格商品3'
		"""
		{
			"name": "tom无规格商品3",
			"created_at": "2015-07-04 10:20",
			"promotion_title": "促销的蜜桔",
			"categories": [],
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
	#商品上架，更新商品后，商品回到待售列表
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "bill无规格商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 99.99,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-03 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""

@eugene @product_pool
Scenario:8 自营平台把商品从商品池放入待售商品列表后，删除商品
	自营平台删除商品，不影响商户

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
	And jobs'永久删除'商品'bill无规格商品3'
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "tom无规格商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""
	Given bill登录系统
	Then bill能获得'在售'商品列表
		"""
		[{
			"name": "bill多规格商品4"
		},{
			"name": "bill无规格商品3"
		}, {
			"name": "bill无规格商品1"
		}]
		"""
	Then bill能获得'待售'商品列表
		"""
		[{
			"name": "bill无规格商品2"
		}]
		"""

@eugene @product_pool
Scenario:9 自营平台把商品从商品池放入待售商品列表后，自营平台创建商品
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
	And jobs已添加供货商
		"""
		[{
			"name": "土小宝",
			"responsible_person": "宝宝",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}, {
			"name": "丹江湖",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "jobs商品1",
			"supplier":"土小宝",
			"purchase_price": 9.00,
			"created_at": "2015-08-03 12:30",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"weight": 5.0,
						"stocks": "无限"
					}
				}
			}
		}]
		"""
	And jobs'下架'商品'jobs商品1'
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "tom无规格商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "jobs商品1",
			"user_code":"1",
			"supplier":"土小宝",
			"categories": [],
			"price": 100.00,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-03 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
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
						"user_code":"3333",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":99
					}
				}
			},
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.0,
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
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "bill无规格商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "jobs商品1",
			"user_code":"1",
			"supplier":"土小宝",
			"categories": [],
			"price": 100.00,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-03 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom商品3",
			"user_code": "3333",
			"supplier":"tom商家",
			"categories": ["分组1"],
			"price": 33.12,
			"stocks":99,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""

@eugene @product_pool @eugeneTMP
Scenario:10 待售商品列表查询
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
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "tom无规格商品3",
			"user_code": "3312",
			"supplier":"tom商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品3",
			"user_code":"3312",
			"supplier":"bill商家",
			"categories": [],
			"price": 33.12,
			"stocks":100,
			"sales": 0,
			"sync_time":"2015-08-02 12:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "tom无规格商品1",
			"user_code":"1112",
			"supplier":"tom商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 11:30",
			"actions": ["修改", "上架", "彻底删除"]
		},{
			"name": "bill无规格商品1",
			"user_code":"1112",
			"supplier":"bill商家",
			"categories": [],
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"sync_time":"2015-08-02 10:30",
			"actions": ["修改", "上架", "彻底删除"]
		}]
		"""
	#供货商模糊查询
	When jobs设置商品查询条件
		"""
		{
			"supplier": "tom"
		}
		"""
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "tom无规格商品3"
		},{
			"name": "tom无规格商品1"
		}]
		"""
	#供货商精确查询
	When jobs设置商品查询条件
		"""
		{
			"supplier": "bill商家"
		}
		"""
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "bill无规格商品3"
		},{
			"name": "bill无规格商品1"
		}]
		"""
	#输入错误供货商查询
	When jobs设置商品查询条件
		"""
		{
			"supplier": "bill  商家"
		}
		"""
	Then jobs能获得'待售'商品列表
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
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "tom无规格商品3"
		},{
			"name": "bill无规格商品3"
		},{
			"name": "tom无规格商品1"
		},{
			"name": "bill无规格商品1"
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
	Then jobs能获得'待售'商品列表
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
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "bill无规格商品3"
		},{
			"name": "bill无规格商品1"
		}]
		"""