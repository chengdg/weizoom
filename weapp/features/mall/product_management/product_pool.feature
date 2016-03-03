# watcher: wangli@weizoom.com,benchi@weizoom.com
# __author__ : "王丽" 2016-02-19

Feature:商品池
"""
	1、有效商家是指：
		(1)正式账号（不包含体验账号）并且在有效期内的,状态为"启用"的商家
		(2)商家由于过了有效期,或者被强制"关闭",从而从有效商家变为无效商家,之前同步到自营平台的商品,被直接自动删除,如果当前商品在自营平台参与活动,活动结束,钉钉提示该商品因为商家失效被删除
	2、系统中"有效商家"的"在售商品管理"中的[非多规格商品（包含一个规格的多规格商品）]商品列表：
		(1)【商品信息】：始终显示商家的对应商品信息,包含商品的图片,标题,商品编码；更新状态的显示“更新”标记
		(2)【供货商】：显示商品的来源的商家名称（开通商家账号时填写的商家名称）
		(3)【库存】：始终显示商家的对应商品的库存数量
		(4)【状态】：三种状态{"未选择","已选择","待更新"}
			"已选择"和"待更新"标红,"未选择"为黑色字体；
			1)"未选择"：没有选择同步到自营平台的商品
			2)"已选择"：已经选择同步到自营平台,并且没有更新的商品
			3)"待更新"：已经选择同步到自营平台,并且有更新的商品
		(5)【同步时间】：此商品同步到自营平台的时间(精确到分)；每次更新之后,取更新的时间 ；状态为"未选择"的商品,显示未空
		(6)【操作】：{"放入待售","无更新","更新"}；"无更新"灰色字体,其他为蓝色字体
			1)商家商品有更新,商品池中的对应的该商品【商品信息】的商品标题显示"更新"标签；【状态】列变为"待更新"；【操作】列变为"更新"
				1> 判断更新时不识别以下字段：【店内分组】,【会员折扣】,【运费设置】,【支付方式】,【商品发票】,【配送时间】,【总销量】,【库存】；
				2> 商家商品下架或删除,不提示更新,自营平台的商品直接删除处理,如果当前商品在自营平台参与活动,活动结束,钉钉提示该商品因为商家下架或删除商品被删除
				3> 商家的商品由无规格修改为有规格,不提示更新,自营平台的商品直接删除处理,如果当前商品在自营平台参与活动,活动结束,钉钉提示该商品因为增加规格被删除
			2)操作项
				1> "放入待售"：没有选择同步的商品；
					点击"放入待售"商品同步到待售列表,此列表中此商品的【状态】字段变为"已选择",商品的【操作】字段变为"无更新"
					同步商品的如下字段：除了【店内分组】,【会员折扣】,【运费设置】,【支付方式】,【商品发票】,【配送时间】,【总销量】,【采购价】其他字段都同步
				2> "无更新"：已经选择同步到自营平台,并且没有更新的商品；此按钮不使能
				3> "更新"：已经选择同步到自营平台,并且有更新的商品；
					1)点击"更新"商品同步更新商品,商品此列表中此商品的【状态】字段变为"已选择",商品的【操作】字段变为"无更新"
					2)更新商品的字段如下：除了【店内分组】,【会员折扣】,【运费设置】,【支付方式】,【商品发票】,【配送时间】,【总销量】,【库存】,【采购价】;不更新的字段保留修改值
					3)点击"更新"弹出确认窗体"是否确认更新该商品？",确认更新商品；
					4)参与活动的商品,更新时弹出提示窗体"该商品正在参加活动,更新后活动将结束,是否确认更新该商品？",确认更新商品；参与优惠券活动的商品,更新后,活动结束,领取过活动发的优惠劵还可以使用
					5)当商品池中商品的商品信息在商家系统被修改,该商品是待更新的状态,此时出现更新提示。更新内容同时要以钉钉消息的方式提示用户,什么商品,更新什么信息
		(7)同步到自营平台的商品,自营平台删除之后,在商品池列表中,此商品的【状态】列表变为"未选择",【操作】按钮列变为"放入待售"
		(8)备注：首次同步商品时,同步【库存】字段,之后更新商品时不再更新【库存】字段
		(9)商品池商品列表排序
			按照【状态】为"待更新"-"未选择"-"已选择"的顺序,再按照商品的在商家的【创建时间】倒序排列；创建时间相同的按照商品的ID倒叙排序
		(10)商品池商品列表分页显示,每页显示12条商品数据
	3、"批量放入待售"功能
		(1)只有【状态】为"未选择"的商品,选择框使能；其他状态的商品的选择框不使能
		(2)点击"全选"按钮,本页【状态】为"未选择"的商品,全部被勾选,其他状态的商品不勾选
		(3)选择商品后,点击"批量放入待售",弹出窗体提示"是否确认批量保存XX个商品至待售商品管理？"；要提示出选择放入待售的商品数量
	4、"查看下架商品"功能
		（1）商家对同步到自营平台的商品进行下架、删除或者增加规格时,自营商城的对应商品要删除,并在【查看失效商品】中记录商品名称（取自营平台）和删除时间（自营平台删除时间）。
		（2）钉钉提示用户什么商品,进行了删除操作
		（3）"查看失效商品"窗体
			1)【商品名称】：商品在自营平台的商品名称
			2)【日期】：此商品在自营平台删除的时间
			3)列表的查询功能,按照【日期】区间查询
			4)列表分页展示,每页8条数据
	5、商品池的搜索功能
		(1)按照【商品名称】、【供货商】、【状态】字段查询
			1)按照【商品名称】查询：模糊匹配
			2)按照【供货商】查询：模糊匹配
			3)按照【状态】查询：下拉列表（全部、未选择、已选择、未更新）
			4)"重置"功能：清空查询条件
"""

###特殊说明：jobs,Nokia表示自营平台,bill,tom表示商家
Background:
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
			},{
				"name": "bill一个规格的多规格商品5",
				"created_at": "2015-07-06 10:20",
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

	#jobs数据
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
		And jobs添加商品分类
			"""
			[{
				"name": "jobs分类1"
			}, {
				"name": "jobs分类2"
			}, {
				"name": "jobs分类3"
			}]
			"""

Scenario:1 有效商家的"无规格"的上架的"待售商品管理"中的商品展示到商品池
	#自营平台商品池,只可以浏览到商家在售商品列表中无规格的商品
		Given jobs登录系统
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

		Given Nokia登录系统
		Then Nokia获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

Scenario:2 有效商家上下架"无规格"的没有同步的商品,商品池中展示的商品变化
	#商家bill上下架无规格的没有同步的商品
		Given bill登录系统
		When bill'上架'商品'bill无规格商品2'
		When bill'下架'商品'bill无规格商品1'
	#自营平台商品池,只可以浏览到商家在售商品列表中无规格的商品
		Given jobs登录系统
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品2",
				"user_code":"2212",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

Scenario:3 有效商家修改未同步商品的【库存】【商品名称】【商品编码】,商品池中展示的商品变化
	#商家bill修改在售商品的【库存】【商品名称】【商品编码】,商品池中展示的商品对应字段对应更新变化
		Given bill登录系统
		When bill更新商品'bill无规格商品1'
			"""
			{
				"name": "bill无规格商品1-修改",
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
							"user_code":"1112000",
							"weight": 5.0,
							"stock_type": "有限",
							"stocks":200
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

		Given jobs登录系统
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品1-修改",
				"user_code":"1112000",
				"supplier":"bill商家",
				"stocks":200,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

Scenario:4 自营平台同步商品池中的商品
	#1 不同的自营平台同步商家商品,对商品池中的商品的"商品信息","供货商","库存"没有影响,同步的商品放入待售列表
	#2 同步商品的如下字段：除了【店内分组】,【会员折扣】,【运费设置】,【支付方式】,【商品发票】,【配送时间】,【总销量】,【采购价】其他字段都同步
	#3 自营平台同步商品后,商品池中的对应商品【状态】字段变为"已选择",商品的【操作】字段变为"无更新",同步时间变为当前时间

	#jobs自营平台同步商品池中的商品
		Given jobs登录系统

		When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
		When jobs将商品'tom无规格商品1'放入待售于'2015-08-03 10:30'

		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-03 10:30",
				"actions": ["无更新"]
			},{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-02 10:30",
				"actions": ["无更新"]
			}]
			"""

		Then jobs能获取商品'tom无规格商品1'
			"""
			[{
				"name": "tom无规格商品1",
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-03 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""
		Then jobs能获取商品'bill无规格商品1'
			"""
			[{
				"name": "bill无规格商品1",
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-02 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""

	#nokia自营平台同步商品池中的商品
		Given nokia登录系统

		When nokia将商品'bill无规格商品1'放入待售于'2015-08-04 10:30'
		When nokia将商品'tom无规格商品1'放入待售于'2015-08-05 10:30'

		Then nokia获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-05 10:30",
				"actions": ["无更新"]
			},{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-04 10:30",
				"actions": ["无更新"]
			}]
			"""
		Then jobs能获取商品'tom无规格商品1'
			"""
			[{
				"name": "tom无规格商品1",
				"created_at": "2015-08-05 10:30",
				"sync_time":"2015-08-05 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""
		Then jobs能获取商品'bill无规格商品1'
			"""
			[{
				"name": "bill无规格商品1",
				"created_at": "2015-08-04 10:30",
				"sync_time":"2015-08-04 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""

Scenario:5 自营平台同步的商品在"待售列表",商家更新被自营平台同步商品的【商品名称】【促销标题】
	#1 商家修改被自营平台同步的商品,自营平台商品池对应商品【状态】字段变为"待更新",商品的【操作】字段变为"更新"
	#2 更新商品除部分字段（【店内分组】【会员折扣】【运费设置】【支付方式】【总销量】【库存】）保留自营平台更改值,其他的都更新成与商家同步

	#jobs自营平台同步商品池中的商品
		Given jobs登录系统

		When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
		When jobs将商品'tom无规格商品1'放入待售于'2015-08-03 10:30'

		Then jobs能获取商品'tom无规格商品1'
			"""
			[{
				"name": "tom无规格商品1",
				"supplier": "tom商家",
				"purchase_price": "",
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-03 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""
		Then jobs能获取商品'bill无规格商品1'
			"""
			[{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": "",
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-02 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""

	#更新【商品名称】或【促销标题】触发更新
		#bill更新商品"bill无规格商品1"的【商品名称】字段
		Given bill登录系统
		When bill更新商品'bill无规格商品1'
			"""
			{
				"name": "修改名称-bill无规格商品1",
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
			}
			"""

		#tom更新商品"bill无规格商品1"的【促销标题】字段
		Given tom登录系统 
		When tom更新商品'tom无规格商品1'
			"""
			{
				"name": "tom无规格商品1",
				"created_at": "2015-07-02 10:20",
				"promotion_title": "tom修改-促销的东坡肘子",
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
			}
			"""

	#jobs在商品池中获得同步商品在更新后,变成待更新状态
		Given jobs登录系统
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-03 10:30",
				"actions": ["更新"]
			},{
				"name": "修改名称-bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-02 10:30",
				"actions": ["更新"]
			},{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

		#jobs更新同步商品"tom无规格商品1"的所有明细字段,填写采购价
		When jobs更新商品'tom无规格商品1'
			"""
			{
				"name": "jobs修改-tom无规格商品1",
				"supplier": "tom商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-03 10:30",
				"promotion_title": "jobs修改-促销的东坡肘子",
				"categories": "jobs分类2",
				"bar_code":"77112233",
				"min_limit":4,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 110.12,
							"user_code":"11012",
							"weight": 1.0,
							"stock_type": "无限"
						}
					}
				},
				"swipe_images": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
				"postage":5.00,
				"pay_interfaces":[{
						"type": "货到付款"
					}],
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "jobs修改-商品描述信息"
			}
			"""

		#jobs在商品池更新商品
		When jobs更新商品池商品'修改名称-bill无规格商品1'于'2015-08-05 10:30'
		When jobs更新商品池商品'tom无规格商品1'于'2015-08-06 10:30'

		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-06 10:30",
				"actions": ["无更新"]
			},{
				"name": "修改名称-bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-05 10:30",
				"actions": ["无更新"]
			}]
			"""

		#jobs更新商品后,jobs修改过或者未修改过的同步商品,
		#除部分字段（【店内分组】【会员折扣】【运费设置】【支付方式】【总销量】【库存】）保留jobs更改值,其他的都更新成与商家同步
		Then jobs能获取商品'tom无规格商品1'
			"""
			[{
				"name": "tom无规格商品1",
				"supplier": "tom商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-06 10:30",
				"promotion_title": "tom修改-促销的东坡肘子",
				"categories": "jobs分类2",
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
				"postage":5.00,
				"pay_interfaces":[{
						"type": "货到付款"
					}],
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""
		Then jobs能获取商品'修改名称-bill无规格商品1'
			"""
			[{
				"name": "修改名称-bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": "",
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-05 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""

Scenario:6 自营平台同步商品在"在售列表",商家更新被自营平台同步商品的【商品条码】【起购数量】
	#同步到自营平台上架的在"在售列表"商品,商品池中更新,自动下架到待售列表

	#jobs自营平台同步商品池中的商品
		Given jobs登录系统

		When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
		When jobs将商品'tom无规格商品1'放入待售于'2015-08-03 10:30'

		#更新商品,填写同步商品的采购价
		When jobs更新商品'bill无规格商品1'
			"""
			{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-02 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
		When jobs更新商品'tom无规格商品1'
			"""
			{
				"name": "jobs修改-tom无规格商品1",
				"supplier": "tom商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-03 10:30",
				"promotion_title": "jobs修改-促销的东坡肘子",
				"categories": "jobs分类2",
				"bar_code":"77112233",
				"min_limit":4,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 110.12,
							"user_code":"11012",
							"weight": 1.0,
							"stock_type": "无限"
						}
					}
				},
				"swipe_images": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
				"postage":5.00,
				"pay_interfaces":[{
						"type": "货到付款"
					}],
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "jobs修改-商品描述信息"
			}
			"""

		When jobs'上架'商品'bill无规格商品1'
		When jobs'上架'商品'tom无规格商品1'

		Then jobs能获取商品'jobs修改-tom无规格商品1'
			"""
			[{
				"name": "jobs修改-tom无规格商品1",
				"supplier": "tom商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-03 10:30",
				"promotion_title": "jobs修改-促销的东坡肘子",
				"categories": "jobs分类2",
				"bar_code":"77112233",
				"min_limit":4,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 110.12,
							"user_code":"11012",
							"weight": 1.0,
							"stock_type": "无限"
						}
					}
				},
				"swipe_images": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
				"postage":5.00,
				"pay_interfaces":[{
						"type": "货到付款"
					}],
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "jobs修改-商品描述信息",
				"status": "在售"
			}]
			"""
		Then jobs能获取商品'bill无规格商品1'
			"""
			[{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-02 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "在售"
			}]
			"""

	#更新【商品条码】【起购数量】触发更新
		#bill更新更新商品"bill无规格商品1"的【商品条码】
		Given bill登录系统
		When bill更新商品'bill无规格商品1'
			"""
			{
				"name": "bill无规格商品1",
				"created_at": "2015-07-02 10:20",
				"promotion_title": "促销的东坡肘子",
				"categories": "分类1,分类2,分类3",
				"bar_code":"000112233",
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
			}
			"""

		#tom更新更新商品"tom无规格商品1"的【起购】
		Given tom登录系统 
		When tom更新商品'tom无规格商品1'
			"""
			{
				"name": "tom无规格商品1",
				"created_at": "2015-07-02 10:20",
				"promotion_title": "促销的东坡肘子",
				"categories": "分类1,分类2,分类3",
				"bar_code":"112233",
				"min_limit":0,
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
			}
			"""

		Given jobs登录系统
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-03 10:30",
				"actions": ["更新"]
			},{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-02 10:30",
				"actions": ["更新"]
			},{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

		When jobs更新商品池商品'bill无规格商品1'于'2015-08-05 10:30'
		When jobs更新商品池商品'tom无规格商品1'于'2015-08-06 10:30'

		Then jobs能获得'在售'商品列表
			"""
			[]
			"""
		Then jobs能获取商品'tom无规格商品1'
			"""
			[{
				"name": "tom无规格商品1",
				"supplier": "tom商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-06 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "jobs分类2",
				"bar_code":"112233",
				"min_limit":0,
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
				"postage":5.00,
				"pay_interfaces":[{
						"type": "货到付款"
					}],
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""
		Then jobs能获取商品'bill无规格商品1'
			"""
			[{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-05 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
				"bar_code":"000112233",
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""

Scenario:7 自营平台同步商品参与限时抢购或买赠活动,商家更新被自营平台同步商品的【商品单价】【商品编码】
	#同步到自营平台上的商品,上架之后再更新,自动下架到待售列表,参与的活动自动结束
	#更新同步商品时,不同更新的字段保留自营平台修改后的值不变

	#jobs自营平台同步商品池中的商品
		Given jobs登录系统

		When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
		When jobs将商品'tom无规格商品1'放入待售于'2015-08-03 10:30'

		#更新商品,填写同步商品的采购价
		When jobs更新商品'bill无规格商品1'
			"""
			{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-02 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
				"bar_code":"112233",
				"min_limit":0,
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
				"postage":0.00,
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
		When jobs更新商品'tom无规格商品1'
			"""
			{
				"name": "jobs修改-tom无规格商品1",
				"supplier": "tom商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-03 10:30",
				"promotion_title": "jobs修改-促销的东坡肘子",
				"categories": "jobs分类2",
				"bar_code":"77112233",
				"min_limit":4,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 110.12,
							"user_code":"11012",
							"weight": 1.0,
							"stock_type": "无限"
						}
					}
				},
				"swipe_images": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
				"postage":5.00,
				"pay_interfaces":[{
						"type": "货到付款"
					}],
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "jobs修改-商品描述信息"
			}
			"""

		When jobs'上架'商品'bill无规格商品1'
		When jobs'上架'商品'jobs修改-tom无规格商品1'

		#商品'bill无规格商品1'参与限时抢购活动
		When jobs创建限时抢购活动
			"""
			[{
				"name": "bill无规格商品1限时抢购",
				"promotion_title":"限时抢购",
				"start_date": "今天",
				"end_date": "1天后",
				"product_name":"bill无规格商品1",
				"member_grade": "全部会员",
				"count_per_purchase": 2,
				"promotion_price": 5.00,
				"limit_period": 1
			}]
			"""
		Then jobs获取限时抢购活动列表
			"""
			[{
				"name": "bill无规格商品1限时抢购",
				"product_name": "bill无规格商品1",
				"product_price": 11.12,
				"promotion_price": 5.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			}]
			"""

		#商品'jobs修改-tom无规格商品1'参与买赠活动
		When jobs创建买赠活动
			"""
			[{
				"name": "tom无规格商品1买一赠一",
				"promotion_title":"买一赠一",
				"start_date": "今天",
				"end_date": "1天后",
				"member_grade": "全部会员",
				"product_name": "jobs修改-tom无规格商品1",
				"premium_products": [{
						"name": "jobs修改-tom无规格商品1",
						"count": 1
					}],
				"count": 1,
				"is_enable_cycle_mode": true
			}]
			"""
		Then jobs获取买赠活动列表
			"""
			[{
				"name": "tom无规格商品1买一赠一",
				"product_name": "jobs修改-tom无规格商品1",
				"product_price":11.12,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			}]
			"""

	#更新【商品单价】【商品编码】触发更新
		#bill更新商品'bill无规格商品1'的【商品单价】
		Given bill登录系统
		When bill更新商品'bill无规格商品1'
			"""
			{
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
							"price": 110.12,
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
			}
			"""

		#tom更新商品'tom无规格商品1'的【商品编码】
		Given tom登录系统 
		When tom更新商品'tom无规格商品1'
			"""
			{
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
							"user_code":"0001112",
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
			}
			"""

		Given jobs登录系统
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-03 10:30",
				"actions": ["更新"]
			},{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-02 10:30",
				"actions": ["更新"]
			},{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

		When jobs更新商品池商品'bill无规格商品1'于'2015-08-05 10:30'
		When jobs更新商品池商品'tom无规格商品1'于'2015-08-06 10:30'

		Then jobs能获得'在售'商品列表
			"""
			[]
			"""
		Then jobs能获取商品'tom无规格商品1'
			"""
			[{
				"name": "tom无规格商品1",
				"supplier": "tom商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-06 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "jobs分类2",
				"bar_code":"112233",
				"min_limit":2,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 11.12,
							"user_code":"0001112",
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
				"postage":5.00,
				"pay_interfaces":[{
						"type": "货到付款"
					}],
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""
		Then jobs能获取商品'bill无规格商品1'
			"""
			[{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-05 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
				"bar_code":"112233",
				"min_limit":2,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 110.12,
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""
		#被更新商品参与的活动自动结束
		Then jobs获取限时抢购活动列表
			"""
			[{
				"name": "bill无规格商品1限时抢购",
				"product_name": "bill无规格商品1",
				"product_price": 11.12,
				"promotion_price": 5.00,
				"status":"已结束",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","删除"]
			}]
			"""
		Then jobs获取买赠活动列表
			"""
			[{
				"name": "tom无规格商品1买一赠一",
				"product_name": "tom无规格商品1",
				"product_price":11.12,
				"status":"已结束",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","删除"]
			}]
			"""

Scenario:8 自营平台同步商品参与积分应用或优惠券活动,商家更新被自营平台同步商品的【商品重量】【商品图片】
	#同步到自营平台上的商品,上架之后再更新,自动下架到待售列表,参与的活动自动结束
	#更新同步商品时,不同更新的字段保留自营平台修改后的值不变

	#jobs自营平台同步商品池中的商品
		Given jobs登录系统			
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

		When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
		When jobs将商品'tom无规格商品1'放入待售于'2015-08-03 10:30'

		#更新商品,填写同步商品的采购价
		When jobs更新商品'bill无规格商品1'
			"""
			{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-02 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
		When jobs更新商品'tom无规格商品1'
			"""
			{
				"name": "jobs修改-tom无规格商品1",
				"supplier": "tom商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-03 10:30",
				"promotion_title": "jobs修改-促销的东坡肘子",
				"categories": "jobs分类2",
				"bar_code":"77112233",
				"min_limit":4,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 110.12,
							"user_code":"11012",
							"weight": 1.0,
							"stock_type": "无限"
						}
					}
				},
				"swipe_images": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
				"postage":5.00,
				"pay_interfaces":[{
						"type": "货到付款"
					}],
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "jobs修改-商品描述信息"
			}
			"""

		When jobs'上架'商品'bill无规格商品1'
		When jobs'上架'商品'jobs修改-tom无规格商品1'

		#商品'bill无规格商品1'参与单品积分活动
		When jobs创建积分应用活动
			"""
			[{
				"name": "bill无规格商品1积分应用",
				"start_date": "今天",
				"end_date": "1天后",
				"product_name": "bill无规格商品1",
				"is_permanant_active": false,
				"discount": 50,
				"discount_money": 5.56
			}]
			"""
		Then jobs获取积分应用活动列表
			"""
			[{
				"name":"bill无规格商品1积分应用",
				"product_name": "bill无规格商品1",
				"product_price":11.12,
				"discount": "50%",
				"discount_money": 5.56,
				"status":"进行中",
				"actions": ["详情","结束"]
			}]
			"""

		#商品'jobs修改-tom无规格商品1'参与单品优惠券
		When jobs已添加了优惠券规则
			"""
			[{
				"name": "tom无规格商品1单品券",
				"money": 10.00,
				"count": 10,
				"limit_counts": 2,
				"start_date": "今天",
				"end_date": "1天后",
				"coupon_id_prefix": "coupon1_id_",
				"coupon_product": "jobs修改-tom无规格商品1"
			}]
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "tom无规格商品1单品券",
				"type": "单品券",
				"money": 10.00,
				"remained_count": 10,
				"limit_counts": 2,
				"use_count": 0,
				"start_date": "今天",
				"end_date": "1天后",
				"status":"进行中"
			}]
			"""

	#更新【商品重量】【商品图片】触发更新
		#bill更新商品'bill无规格商品1'的【商品重量】
		Given bill登录系统
		When bill更新商品'bill无规格商品1'
			"""
			{
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
							"weight": 1.0,
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
			}
			"""

		#bill更新商品'tom无规格商品1'的【商品图片】
		Given tom登录系统 
		When tom更新商品'tom无规格商品1'
			"""
			{
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

		Given jobs登录系统
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-03 10:30",
				"actions": ["更新"]
			},{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-02 10:30",
				"actions": ["更新"]
			},{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

		When jobs更新商品池商品'bill无规格商品1'于'2015-08-05 10:30'
		When jobs更新商品池商品'tom无规格商品1'于'2015-08-06 10:30'

		Then jobs能获得'在售'商品列表
			"""
			[]
			"""
		Then jobs能获取商品'tom无规格商品1'
			"""
			[{
				"name": "tom无规格商品1",
				"supplier": "tom商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-06 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "jobs分类2",
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
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
				"postage":5.00,
				"pay_interfaces":[{
						"type": "货到付款"
					}],
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""
		Then jobs能获取商品'bill无规格商品1'
			"""
			[{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-05 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
				"bar_code":"000112233",
				"min_limit":2,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 11.12,
							"user_code":"1112",
							"weight": 1.0,
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""
		#被更新商品参与的活动自动结束
		Then jobs获取积分应用活动列表
			"""
			[{
				"name":"bill无规格商品1积分应用",
				"product_name": "bill无规格商品1",
				"product_price":11.12,
				"discount": "50%",
				"discount_money": 5.56,
				"status":"已结束",
				"actions": ["详情","删除"]
			}]
			"""
		Then jobs能获得优惠券规则列表
			"""
			[{
				"name": "tom无规格商品1单品券",
				"type": "单品券",
				"money": 10.00,
				"remained_count": 10,
				"limit_counts": 2,
				"use_count": 0,
				"start_date": "今天",
				"end_date": "1天后",
				"status":"已结束"
			}]
			"""

Scenario:9 自营平台同步商品,商家更新被自营平台同步商品的【商品描述】
	#同步到自营平台上的商品,上架之后再更新,自动下架到待售列表
	#更新同步商品时,不同更新的字段保留自营平台修改后的值不变

	#jobs自营平台同步商品池中的商品
		Given jobs登录系统

		When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'

		#更新商品,填写同步商品的采购价
		When jobs更新商品'bill无规格商品1'
			"""
			{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-02 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
				"detail": "jobs修改-商品描述信息"
			}
			"""

	#更新【商品描述】触发更新
		Given bill登录系统
		When bill更新商品'bill无规格商品1'
			"""
			{
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
				"detail": "bill修改-商品描述信息",
				"status": "在售"
			}
			"""

		Given jobs登录系统
		When jobs更新商品池商品'bill无规格商品1'于'2015-08-05 10:30'
		Then jobs能获取商品'bill无规格商品1'
			"""
			[{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-05 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
				"bar_code":"000112233",
				"min_limit":2,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 11.12,
							"user_code":"1112",
							"weight": 1.0,
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
				"postage":0.00,
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
				"detail": "bill修改-商品描述信息",
				"status": "待售"
			}]
			"""

Scenario:10 商家更新被自营平台同步商品的【店铺分组】【会员折扣】【运费设置】【支付方式】【商品发票】【配送时间】【库存】,不触发自营平台商品的更新
	#jobs自营平台同步商品池中的商品
		Given jobs登录系统
		When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'

	#商家更新被同步商品的【店铺分组】【会员折扣】【运费设置】【支付方式】【商品发票】【配送时间】【库存】字段
		Given bill登录系统
		When bill更新商品'bill无规格商品1'
			"""
			{
				"name": "bill无规格商品1",
				"created_at": "2015-07-02 10:20",
				"promotion_title": "促销的东坡肘子",
				"categories": "分类1",
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
							"stocks": 200
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
				"postage":5.00,
				"pay_interfaces":[{
						"type": "在线支付"
					}],
				"invoice":false,
				"distribution_time":"off",
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
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-02 10:30",
				"actions": ["无更新"]
			}]
			"""

Scenario:11 商家更新被自营平台同步商品的规格为多规格,自营平台的对应商品被删除
	#jobs自营平台同步商品池中的商品
		Given jobs登录系统
		When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
		Then jobs能获取商品'bill无规格商品1'
			"""
			[{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": "",
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-02 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""

	#商家更新被自营平台同步商品的规格为多规格,自营平台的对应商品被删除,商品池无此商品
		Given bill登录系统
		When bill更新商品'bill无规格商品1'
			"""
			{
				"name": "bill无规格商品1",
				"created_at": "2015-07-02 10:20",
				"promotion_title": "促销的东坡肘子",
				"categories": "分类1",
				"bar_code":"112233",
				"min_limit":2,
				"is_member_product":"on",
				"model": {
					"models": {
						"红色 M": {
							"price": 11.12,
							"user_code":"1112",
							"weight": 5.0,
							"stock_type": "有限",
							"stocks": 200
						},
						"黄色 L": {
							"price": 12.12,
							"user_code":"1212",
							"weight": 5.0,
							"stock_type": "有限",
							"stocks": 300
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
				"postage":5.00,
				"pay_interfaces":[{
						"type": "在线支付"
					}],
				"invoice":false,
				"distribution_time":"off",
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "bill修改-商品描述信息",
				"status": "在售"
			}
			"""

		Given jobs登录系统
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""
		Then jobs能获得'待售'商品列表
			"""
			[]
			"""

Scenario:12 商家下架或删除被自营平台同步商品,自营平台的对应商品被删除,商品参加的活动结束
	#jobs自营平台同步商品池中的商品
		Given jobs登录系统

		When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
		When jobs将商品'tom无规格商品1'放入待售于'2015-08-03 10:30'

		#更新商品,填写同步商品的采购价
		When jobs更新商品'bill无规格商品1'
			"""
			{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-02 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
		When jobs更新商品'tom无规格商品1'
			"""
			{
				"name": "jobs修改-tom无规格商品1",
				"supplier": "tom商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-03 10:30",
				"promotion_title": "jobs修改-促销的东坡肘子",
				"categories": "jobs分类2",
				"bar_code":"77112233",
				"min_limit":4,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 110.12,
							"user_code":"11012",
							"weight": 1.0,
							"stock_type": "无限"
						}
					}
				},
				"swipe_images": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
				"postage":5.00,
				"pay_interfaces":[{
						"type": "货到付款"
					}],
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "jobs修改-商品描述信息"
			}
			"""

		When jobs'上架'商品'bill无规格商品1'
		When jobs'上架'商品'jobs修改-tom无规格商品1'

		Then jobs能获取商品'jobs修改-tom无规格商品1'
			"""
			[{
				"name": "jobs修改-tom无规格商品1",
				"supplier": "tom商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-03 10:30",
				"promotion_title": "jobs修改-促销的东坡肘子",
				"categories": "jobs分类2",
				"bar_code":"77112233",
				"min_limit":4,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 110.12,
							"user_code":"11012",
							"weight": 1.0,
							"stock_type": "无限"
						}
					}
				},
				"swipe_images": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
				"postage":5.00,
				"pay_interfaces":[{
						"type": "货到付款"
					}],
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "jobs修改-商品描述信息",
				"status": "在售"
			}]
			"""
		Then jobs能获取商品'bill无规格商品1'
			"""
			[{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-02 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "在售"
			}]
			"""

		#商品'bill无规格商品1'参与限时抢购活动
		When jobs创建限时抢购活动
			"""
			[{
				"name": "bill无规格商品1限时抢购",
				"promotion_title":"限时抢购",
				"start_date": "今天",
				"end_date": "1天后",
				"product_name":"bill无规格商品1",
				"member_grade": "全部会员",
				"count_per_purchase": 2,
				"promotion_price": 5.00,
				"limit_period": 1
			}]
			"""
		Then jobs获取限时抢购活动列表
			"""
			[{
				"name": "bill无规格商品1限时抢购",
				"product_name": "bill无规格商品1",
				"product_price": 11.12,
				"promotion_price": 5.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			}]
			"""

		#商品'jobs修改-tom无规格商品1'参与买赠活动
		When jobs创建买赠活动
			"""
			[{
				"name": "tom无规格商品1买一赠一",
				"promotion_title":"买一赠一",
				"start_date": "今天",
				"end_date": "1天后",
				"member_grade": "全部会员",
				"product_name": "jobs修改-tom无规格商品1",
				"premium_products": [{
						"name": "jobs修改-tom无规格商品1",
						"count": 1
					}],
				"count": 1,
				"is_enable_cycle_mode": true
			}]
			"""
		Then jobs获取买赠活动列表
			"""
			[{
				"name": "tom无规格商品1买一赠一",
				"product_name": "tom无规格商品1",
				"product_price":11.12,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			}]
			"""

	#商家下架或删除被自营平台同步商品
		Given bill登录系统
		When bill'下架'商品'bill无规格商品1'

		Given tom登录系统 
		When tom'永久删除'商品'tom无规格商品1'

		Given jobs登录系统
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

		Then jobs能获得'待售'商品列表
			"""
			[]
			"""
		Then jobs能获得'在售'商品列表
			"""
			[]
			"""

		#被更新商品参与的活动自动结束
		Then jobs获取限时抢购活动列表
			"""
			[{
				"name": "bill无规格商品1限时抢购",
				"product_name": "bill无规格商品1",
				"product_price": 11.12,
				"promotion_price": 5.00,
				"status":"已结束",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","删除"]
			}]
			"""
		Then jobs获取买赠活动列表
			"""
			[{
				"name": "tom无规格商品1买一赠一",
				"product_name": "bill",
				"product_price":11.12,
				"status":"已结束",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","删除"]
			}]
			"""

Scenario:13 自营平台删除同步的商品,商品池中的对应商品变为未同步模式,可以再同步
	#jobs自营平台同步商品池中的商品,删除商品
		Given jobs登录系统
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

		When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
		When jobs将商品'tom无规格商品1'放入待售于'2015-08-03 10:30'

		When jobs'永久删除'商品'jobs修改-tom无规格商品1'

	#再次同步自营平台删除的商家的商品
		When jobs将商品'tom无规格商品1'放入待售于'2015-08-04 10:30'

		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-04 10:30",
				"actions": ["无更新"]
			},{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-02 10:30",
				"actions": ["无更新"]
			}]
			"""
		Then jobs能获取商品'tom无规格商品1'
			"""
			[{
				"name": "tom无规格商品1",
				"supplier": "tom商家",
				"purchase_price": "",
				"created_at": "2015-08-04 10:30",
				"sync_time":"2015-08-04 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""
		Then jobs能获取商品'bill无规格商品1'
			"""
			[{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": "",
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-02 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
				"detail": "商品描述信息",
				"status": "待售"
			}]
			"""

Scenario:14 自营平台对商家商品"批量放入待售"
	Given jobs登录系统

	#批量放入一个商品到待售
		When jobs将商品池商品批量放入待售于'2015-08-02 10:30'
			"""
			{
				"bill无规格商品1"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-02 10:30",
				"actions": ["无更新"]
			}]
			"""

	#批量放入多个商品到待售
		When jobs将商品池商品批量放入待售于'2015-08-03 10:30'
			"""
			{
				"tom无规格商品3",
				"bill无规格商品3",
				"tom无规格商品1"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"已选择",
				"sync_time":"2015-08-03 10:30",
				"actions": ["无更新"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"已选择",
				"sync_time":"2015-08-03 10:30",
				"actions": ["无更新"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-03 10:30",
				"actions": ["无更新"]
			},{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-02 10:30",
				"actions": ["无更新"]
			}]
			"""

Scenario:15 "查看失效商品"功能
	#jobs自营平台同步商品池中的商品
		Given jobs登录系统

		When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
		When jobs将商品'tom无规格商品1'放入待售于'2015-08-03 10:30'
		When jobs将商品'tom无规格商品3'放入待售于'2015-08-04 10:30'

		#更新商品,填写同步商品的采购价
		When jobs更新商品'bill无规格商品1'
			"""
			{
				"name": "bill无规格商品1",
				"supplier": "bill商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-02 10:30",
				"sync_time":"2015-08-02 10:30",
				"promotion_title": "促销的东坡肘子",
				"categories": "",
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
				"postage":0.00,
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
		When jobs更新商品'tom无规格商品1'
			"""
			{
				"name": " ",
				"supplier": "tom商家",
				"purchase_price": 10.00,
				"created_at": "2015-08-03 10:30",
				"sync_time":"2015-08-03 10:30",
				"promotion_title": "jobs修改-促销的东坡肘子",
				"categories": "jobs分类2",
				"bar_code":"77112233",
				"min_limit":4,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 110.12,
							"user_code":"11012",
							"weight": 1.0,
							"stock_type": "无限"
						}
					}
				},
				"swipe_images": [{
					"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
				"postage":5.00,
				"pay_interfaces":[{
						"type": "货到付款"
					}],
				"properties": [{
						"name": "CPU",
						"description": "CPU描述"
					}, {
						"name": "内存",
						"description": "内存描述"
					}],
				"detail": "jobs修改-商品描述信息"
			}
			"""

		When jobs'上架'商品'bill无规格商品1'
		When jobs'上架'商品'tom无规格商品1'

	#商家对自营平台同步商品下架或删除,修改商品为多规格
		Given bill登录系统
		When bill'下架'商品'bill无规格商品1'

		Given tom登录系统 
		When tom'永久删除'商品'tom无规格商品1'
		#tom更新商品'tom无规格商品3'为多规格
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
						"红色 M": {
							"price": 33.12,
							"user_code":"3312",
							"weight":1.0,
							"stock_type": "有限",
							"stocks":100
						},
						"黄色 L": {
							"price": 34.12,
							"user_code":"3412",
							"weight":2.0,
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
			}
			"""

		Given jobs登录系统
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

		Then jobs能获得'待售'商品列表
			"""
			[]
			"""
		Then jobs能获得'在售'商品列表
			"""
			[]
			"""

	#查看失效商品
		Given jobs登录系统
		Then jobs获得失效商品列表
			"""
			[{
				"name":"tom无规格商品3",
				"delete_time":"今天"
			},{
				"name":"jobs修改-tom无规格商品1",
				"delete_time":"今天"
			},{
				"name":"bill无规格商品1",
				"delete_time":"今天"
			}]
			"""

	#查看失效商品列表查询
		When jobs设置失效商品列表查询条件
			"""
			{
				"start_date":"今天",
				"end_date":"今天"
			}
			"""
		Then jobs获得失效商品列表
			"""
			[{
				"name":"tom无规格商品3",
				"delete_time":"今天"
			},{
				"name":"jobs修改-tom无规格商品1",
				"delete_time":"今天"
			},{
				"name":"bill无规格商品1",
				"delete_time":"今天"
			}]
			"""

		When jobs设置失效商品列表查询条件
			"""
			{
				"start_date":"1天前",
				"end_date":"1天前"
			}
			"""
		Then jobs获得失效商品列表
			"""
			[]
			"""

	#查看失效商品列表分页
		When jobs设置分页查询参数
			"""
			{
				"count_per_page":1
			}
			"""
		Then jobs获得失效商品列表
			"""
			[{
				"name":"tom无规格商品3",
				"delete_time":"今天"
			}]
			"""
		When jobs浏览下一页
		Then jobs获得失效商品列表
			"""
			[{
				"name":"jobs修改-tom无规格商品1",
				"delete_time":"今天"
			}]
			"""
		When jobs浏览失效商品列表第'3'页
		Then jobs获得失效商品列表
			"""
			[{
				"name":"bill无规格商品1",
				"delete_time":"今天"
			}]
			"""
		When jobs浏览上一页
		Then jobs获得失效商品列表
			"""
			[{
				"name":"jobs修改-tom无规格商品1",
				"delete_time":"今天"
			}]
			"""

Scenario:16 商品池的搜索功能
	#jobs自营平台同步商品池中的商品
		Given jobs登录系统

		When jobs将商品'bill无规格商品1'放入待售于'2015-08-02 10:30'
		When jobs将商品'tom无规格商品1'放入待售于'2015-08-03 10:30'

	#更新【商品重量】触发更新
		Given bill登录系统
		When bill更新商品'bill无规格商品1'
			"""
			{
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
							"weight": 1.0,
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
			}
			"""

		Given jobs登录系统
	#商品池列表搜索
		#默认条件搜索
		When jobs设置商品池列表查询条件
			"""
			{
				"name":"",
				"supplier":"",
				"status":"全部"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-02 10:30",
				"actions": ["更新"]
			},{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-03 10:30",
				"actions": ["无更新"]
			}]
			"""
		#按照【商品名称】搜索
		When jobs设置商品池列表查询条件
			"""
			{
				"name":"bill"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-02 10:30",
				"actions": ["更新"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			""" 

		When jobs设置商品池列表查询条件
			"""
			{
				"name":"bill无规格商品3"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			""" 

		When jobs设置商品池列表查询条件
			"""
			{
				"name":"marry"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[]
			""" 

		#按照【供应商】查询
		When jobs设置商品池列表查询条件
			"""
			{
				"supplier":"bill"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-02 10:30",
				"actions": ["更新"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			""" 

		When jobs设置商品池列表查询条件
			"""
			{
				"supplier":"bill商家"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-02 10:30",
				"actions": ["更新"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			""" 

		When jobs设置商品池列表查询条件
			"""
			{
				"supplier":"marry"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[]
			""" 	

		#按照【状态】查询
		When jobs设置商品池列表查询条件
			"""
			{
				"status":"全部"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-02 10:30",
				"actions": ["更新"]
			},{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-03 10:30",
				"actions": ["无更新"]
			}]
			"""

		When jobs设置商品池列表查询条件
			"""
			{
				"status":"待更新"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "bill无规格商品1",
				"user_code":"1112",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"待更新",
				"sync_time":"2015-08-02 10:30",
				"actions": ["更新"]
			}]
			"""

		When jobs设置商品池列表查询条件
			"""
			{
				"status":"未选择"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill无规格商品3",
				"user_code":"3312",
				"supplier":"bill商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

		When jobs设置商品池列表查询条件
			"""
			{
				"status":"已选择"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品1",
				"user_code":"1112",
				"supplier":"tom商家",
				"stock_type": "无限",
				"status":"已选择",
				"sync_time":"2015-08-03 10:30",
				"actions": ["无更新"]
			}]
			"""

		#条件组合查询
		When jobs设置商品池列表查询条件
			"""
			{
				"name":"tom",
				"supplier":"商家",
				"status":"未选择"
			}
			"""
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3",
				"user_code":"3312",
				"supplier":"tom商家",
				"stocks":100,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""

Scenario:17 商品池的分页功能
	#商品池列表分页
		Given jobs登录系统
		When jobs设置分页查询参数
			"""
			{
				"count_per_page":1
			}
			"""

		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品3"
			}]
			"""
		When jobs浏览下一页
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "bill无规格商品3"
			}]
			"""
		When jobs浏览商品池列表第'3'页
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom无规格商品1"
			}]
			"""
		When jobs浏览上一页
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "bill无规格商品3"
			}]
			"""
