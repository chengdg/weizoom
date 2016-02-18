# watcher: wangli@weizoom.com,benchi@weizoom.com
# __author__ : "王丽"

Feature:商品池
"""
	1、有效商家是指：
		(1)正式账号（不包含体验账号）并且在有效期内的，状态为"启用"的商家
		(2)商家由于过了有效期，或者被强制"关闭"，从而从有效商家变为无效商家，之前同步到自营平台的商品，被直接自动删除，如果当前商品在自营平台参与活动，活动结束，钉钉提示该商品因为商家失效被删除(钉钉消息提示模板？？？)
	2、系统中"有效商家"的"在售商品管理"中的[非多规格商品]商品列表：
		(1)【商品信息】：始终显示商家的对应商品信息，包含商品的图片，标题，商品编码；更新状态的显示“更新”标记
		(2)【供货商】：显示商品的来源的商家名称（开通商家账号时填写的商家名称）
		(3)【库存】：始终显示商家的对应商品的库存数量
		(4)【状态】：三种状态{"未选择"，"已选择"，"待更新"}
			"已选择"和"待更新"标红，"未选择"为黑色字体；
			1)"未选择"：没有选择同步到自营平台的商品
			2)"已选择"：已经选择同步到自营平台，并且没有更新的商品
			3)"待更新"：已经选择同步到自营平台，并且有更新的商品
		(5)【同步时间】：此商品同步到自营平台的时间(精确到分) ；状态为"未选择"的商品，显示未空
		(6)【操作】：{"放入待售","无更新","更新"}；"无更新"灰色字体，其他为蓝色字体
			1)商家商品有更新，商品池中的对应的该商品【商品信息】的商品标题显示"更新"标签；【状态】列变为"待更新"；【操作】列变为"更新"
				1> 判断更新时不识别以下字段：【店内分组】，【会员折扣】，【运费设置】，【支付方式】，【总销量】，【库存】；
				2> 商家商品下架或删除，不提示更新，自营平台的商品直接删除处理，如果当前商品在自营平台参与活动，活动结束，钉钉提示该商品因为商家下架或删除商品被删除(钉钉消息提示模板？？？)
				3> 商家的商品由无规格修改为有规格，不提示更新，自营平台的商品直接删除处理，如果当前商品在自营平台参与活动，活动结束，钉钉提示该商品因为增加规格被删除(钉钉消息提示模板？？？)
			2)操作项
				1> "放入待售"：没有选择同步的商品；
					点击"放入待售"商品同步到待售列表，此列表中此商品的【状态】字段变为"已选择"，商品的【操作】字段变为"无更新"
					同步商品的如下字段：除了【店内分组】，【会员折扣】，【运费设置】，【支付方式】，【总销量】,【采购价】其他字段都同步
				2> "无更新"：已经选择同步到自营平台，并且没有更新的商品；此按钮不使能
				3> "更新"：已经选择同步到自营平台，并且有更新的商品；
					1)点击"更新"商品同步更新商品，商品此列表中此商品的【状态】字段变为"已选择"，商品的【操作】字段变为"无更新"
					2)更新商品的字段如下：除了【店内分组】，【会员折扣】，【运费设置】，【支付方式】，【总销量】，【库存】,【采购价】
					3)点击"更新"弹出确认窗体"是否确认更新该商品？"，确认更新商品；
					4)参与活动的商品，更新时弹出提示窗体"该商品正在参加活动，更新后活动将结束，是否确认更新该商品？"，确认更新商品；参与优惠券活动的商品，更新后，活动结束，领取过活动发的优惠劵还可以使用
					5)当商品池中商品的商品信息在商家系统被修改，该商品是待更新的状态，此时出现更新提示。更新内容同时要以钉钉消息的方式提示用户，什么商品，更新什么信息(钉钉消息提示模板？？？)
					6)在商品池列表点击"更新"，更新商品后，自营平台对应的同步商品被下架，进入待售列表
		(7)同步到自营平台的商品，自营平台删除之后，在商品池列表中，此商品的【状态】列表变为"未选择"，【操作】按钮列变为"放入待售"
		(8)备注：首次同步商品时，同步【库存】字段，之后更新商品时不再更新【库存】字段
		(9)商品池商品列表排序
			按照【状态】为"待更新"-"未选择"-"已选择"的顺序，再按照商品的在商家的【创建时间】倒序排列；创建时间相同的按照商品的ID倒叙排序
		(10)商品池商品列表分页显示，每页显示12条商品数据
	3、"批量放入待售"功能
		(1)只有【状态】为"未选择"的商品，选择框使能；其他状态的商品的选择框不使能
		(2)点击"全选"按钮，本页【状态】为"未选择"的商品，全部被勾选
		(3)选择商品后，点击"批量放入待售"，弹出窗体提示"是否确认批量保存XX个商品至待售商品管理？"；要提示出选择放入待售的商品数量
	4、"查看下架商品"功能
	5、商品池的搜索功能
		(1)按照【商品名称】、【供货商】、【状态】字段查询
			1)按照【商品名称】查询：模糊匹配
			2)按照【供货商】查询：模糊匹配
			3)按照【状态】查询：下拉列表（全部、未选择、已选择、未更新）
			4)"重置"功能：清空查询条件
"""

###特殊说明：jobs，Nokia表示自营平台，bill，tom, jack表示商家
Background:
	Given jobs登录系统

Scenario:1 有效商家的"无规格"的上架的"待售商品管理"中的商品展示到商品池
	#商家bill的商品信息
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
				"name": "颜色",
				"type": "图片",
				"values": [{
					"name": "红色",
					"image": "/standard_static/test_resource_img/icon_color/icon_1.png"
				}, {
					"name": "黄色",
					"image": "/standard_static/test_resource_img/icon_color/icon_5.png"
				}, {
					"name": "蓝色",
					"image": "/standard_static/test_resource_img/icon_color/icon_9.png"
				}]
			},{
				"name": "尺寸",
				"type": "文字",
				"values": [{
					"name": "M"
				}, {
					"name": "S"
				}, {
					"name": "L"
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
				"postage":10.00,
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
						"红色 M": {
							"price": 44.12,
							"user_code":"4412",
							"weight":1.0,
							"stock_type": "有限",
							"stocks":100
						},
						"黄色 L": {
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
		Given tom登录系统
		When tom已添加支付方式
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
				"name": "颜色",
				"type": "图片",
				"values": [{
					"name": "红色",
					"image": "/standard_static/test_resource_img/icon_color/icon_1.png"
				}, {
					"name": "黄色",
					"image": "/standard_static/test_resource_img/icon_color/icon_5.png"
				}, {
					"name": "蓝色",
					"image": "/standard_static/test_resource_img/icon_color/icon_9.png"
				}]
			},{
				"name": "尺寸",
				"type": "文字",
				"values": [{
					"name": "M"
				}, {
					"name": "S"
				}, {
					"name": "L"
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
				"postage":10.00,
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
						"红色 M": {
							"price": 44.12,
							"user_code":"4412",
							"weight":1.0,
							"stock_type": "有限",
							"stocks":100
						},
						"黄色 L": {
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

	#自营平台商品池，只可以浏览到商家在售商品列表中无规格的商品
		Given jobs登录系统

		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择"，
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择"，
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"未选择"，
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品1",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"未选择"，
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

		Given Nokia登录系统

		Then Nokia获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择"，
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择"，
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"未选择"，
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品1",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"未选择"，
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

Scenario:2 有效商家的"无规格"的上架的"待售商品管理"中的商品展示到商品池