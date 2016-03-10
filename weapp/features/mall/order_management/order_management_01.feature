# watcher: zhangsanxiang@weizoom.com,benchi@weizoom.com
#_author_:张三香 2016.01.19

Feature:商家后台查看自营平台同步过来的订单列表及订单详情信息
	"""
		订单列表显示:
			1.只同步微众系列自营平台中的有效订单,待发货、已发货和已完成
			2.微众系列自营平台同步过来的有效订单显示规则:
				a.同步过来的订单,订单列表中'订单编号'显示子订单编号
				b.订单列表中增加'来源'一列,其中来源包括'商城'和'本店',其中微众系列自营平台统称为'商城'
				c.同步过来的订单,订单列表中不显示'单价'、'优惠金额'和'运费'
				d.同步过来的订单,订单列表中'商品名称'显示的是商家这边的商品名称,不显示自营平台中的商品名称
				e.同步过来的订单,订单列表中'实付金额'=采购价*数量
				f.同步过来的订单操作项限制,禁止对订单进行'申请退款'和'取消订单'操作;操作列会将其隐藏不显示
				g.所有与买赠相关的订单，本期暂不处理
				h.同步过来的订单,卖家和买家备注信息不同步到商家,订单列表中的'买家'不能点击
		订单详情页显示:
			1.同步过来的订单,订单详情页不显示单品优惠、优惠和微众卡支付金额;只显示"支付金额:xx"
			2.支付信息中的支付方式,全部显示为'微信支付'
			3.订单详情页中单价显示的是商品的采购价
	"""

#特殊说明：jobs、Nokia表示自营平台;bill、tom表示商家;lily、jack表示会员

Background:
	#自营平台jobs的信息
		Given jobs登录系统
		And jobs已添加支付方式
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
		When jobs开通使用微众卡权限
		When jobs添加支付方式
			"""
			[{
				"type": "微众卡支付",
				"is_active": "启用"
			}]
			"""
		Given jobs设定会员积分策略
			"""
			{
				"integral_each_yuan": 2,
				"use_ceiling": 50
			}
			"""
		Given jobs已创建微众卡
			"""
			[{
				"cards": [{
					"id": "0000001",
					"password": "1234567",
					"status": "未使用",
					"price": 100
				},{
					"id": "0000002",
					"password": "1",
					"status": "未使用",
					"price": 200
				}]
			}]
			"""

	#自营平台Nokia的信息

	#商家bill的信息
		Given bill登录系统
		And bill已添加支付方式
			"""
			[{
				"type": "微信支付",
				"is_active": "启用"
			}]
			"""
		And bill已添加商品规格
			"""
			[{
				"name": "颜色",
				"type": "图片",
				"values": [{
					"name": "黑色",
					"image": "/standard_static/test_resource_img/icon_color/icon_1.png"
				}, {
					"name": "白色色",
					"image": "/standard_static/test_resource_img/icon_color/icon_5.png"
				}]
			},{
				"name": "尺寸",
				"type": "文字",
				"values": [{
					"name": "M"
				}, {
					"name": "S"
				}]
			}]
			"""
		And bill已添加商品
			"""
			[{
				"name":"bill商品1",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0101",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.0
			},{
				"name":"bill商品2",
				"model": {
					"models": {
						"standard": {
							"price": 20.00,
							"user_code":"0102",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
			},{
				"name":"bill商品3",
				"is_enable_model": "启用规格",
				"model": {
					"models": {
						"黑色 S": {
							"price": 30.0,
							"weight": 1,
							"stock_type": "有限",
							"stocks": 100
						},
						"白色 S": {
							"price": 30.0,
							"weight": 2,
							"stock_type": "无限"
						}
					}
				}
			}]
			"""
		Given jobs已添加了优惠券规则
			"""
			[{
				"name": "优惠券1",
				"money": 5,
				"start_date": "今天",
				"end_date": "10天后",
				"coupon_id_prefix": "coupon1_id_",
				"coupon_product": "bill商品1"
			}]
			"""

	#商家tom的信息
		Given tom登录系统
		And tom已添加支付方式
			"""
			[{
				"type": "微信支付",
				"is_active": "启用"
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
		And tom已添加商品
			"""
			[{
				"name":"tom商品1",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0201",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"status":"在售"
			},{
				"name":"tom商品2",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 20.00,
							"user_code":"0202",
							"weight":1.0,
							"stock_type": "有限",
							"stocks":200
						}
					}
				},
				"status":"在售"
			},{
				"name":"tom商品3",
				"is_enable_model": "启用规格",
				"model": {
					"models": {
						"M": {
							"price": 30.0,
							"weight": 1,
							"stock_type": "有限",
							"stocks": 100
						},
						"S": {
							"price": 30.0,
							"weight": 2,
							"stock_type": "无限"
						}
					}
				},
				"status":"在售"
			}]
			"""

	#jobs后台商品信息
		Given jobs登录系统
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom商品2",
				"user_code":"0202",
				"supplier":"tom商家",
				"stocks":200,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom商品1",
				"user_code":"0201",
				"supplier":"tom商家",
				"stock_type":"无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill商品2",
				"user_code":"0102",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill商品1",
				"user_code":"0101",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""
		When jobs批量将商品放入待售
			"""
			[{
				"name": "tom商品2"
			}, {
				"name": "tom商品1"
			}, {
				"name": "bill商品2"
			}, {
				"name": "bill商品1"
			}]
			"""
		When jobs更新商品'bill商品1'
			"""
			{
				"name":"bill商品11",
				"supplier":"bill商家",
				"purchase_price": 9.00,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0101",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.00
			}
			"""
		When jobs更新商品'bill商品2'
			"""
			{
				"name":"bill商品2",
				"supplier":"bill商家",
				"purchase_price": 19.00,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 20.00,
							"user_code":"0102",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":0.00
			}
			"""
		When jobs更新商品'tom商品1'
			"""
			{
				"name":"tom商品1",
				"supplier":"tom商家",
				"purchase_price": 9.00,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0201",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.00
			}
			"""
		When jobs更新商品'tom商品2'
			"""
			{
				"name":"tom商品2",
				"supplier":"tom商家",
				"purchase_price": 19.00,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 20.00,
							"user_code":"0202",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				}
			}
			"""
		When jobs批量上架商品
			"""
			["bill商品11","bill商品2","tom商品1","tom商品2"]
			"""

	#nokia的后台商品信息
		Given nokia登录系统
		Then nokia获得商品池商品列表
			"""
			[{
				"name": "tom商品2",
				"user_code":"0202",
				"supplier":"tom商家",
				"stocks":200,
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "tom商品1",
				"user_code":"0201",
				"supplier":"tom商家",
				"stock_type":"无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill商品2",
				"user_code":"0102",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill商品1",
				"user_code":"0101",
				"supplier":"bill商家",
				"stock_type": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""
		When nokia批量将商品放入待售
			"""
			[{
				"name": "tom商品2"
			}, {
				"name": "tom商品1"
			}, {
				"name": "bill商品2"
			}, {
				"name": "bill商品1"
			}]
			"""
		When nokia更新商品'bill商品2'
			"""
			{
				"name":"bill商品2",
				"supplier":"bill商家",
				"purchase_price": 19.00,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 20.00,
							"user_code":"0102",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				}
			}
			"""
		When nokia更新商品'tom商品1'
			"""
			{
				"name":"tom商品1",
				"supplier":"tom商家",
				"purchase_price": 9.00,
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0201",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				}
			}
			"""
		When nokia批量上架商品
			"""
			["bill商品2","tom商品1"]
			"""

	#lily购买商品（jobs自营平台、商家bill的平台）
		When lily关注jobs的公众号
		When lily访问jobs的webapp
		When lily领取jobs的优惠券
			"""
			[{
				"name": "优惠券1",
				"coupon_ids": ["coupon1_id_1"]
			}]
			"""
		When lily关注nokia的公众号
		When lily关注bill的公众号
		When lily关注tom的公众号
		#待支付-001(bill商品1)
			When lily访问jobs的webapp
			When lily购买jobs的商品
				"""
				{
					"order_id":"001",
					"pay_type":"微信支付",
					"products":[{
						"name":"bill商品11",
						"count":1
					}]
				}
				"""

		#待发货-002(bill商品1、bill商品2),单品优惠
			When lily购买jobs的商品
				"""
				{
					"order_id":"002",
					"pay_type":"微信支付",
					"products":[{
						"name":"bill商品11",
						"count":1
					},{
						"name":"bill商品2",
						"count":1
					}],
					"coupon":"coupon1_id_1"
				}
				"""
			When lily使用支付方式'微信支付'进行支付订单'002'

		#待发货-003(bill商品1、bill商品2、tom商品1)
			When lily购买jobs的商品
				"""
				{
					"order_id":"003",
					"pay_type":"货到付款",
					"products":[{
						"name":"bill商品11",
						"count":1
					},{
						"name":"bill商品2",
						"count":1
					},{
						"name":"tom商品1",
						"count":1
					}]
				}
				"""

		#待发货-004（bill商品1）,整单优惠
			When lily购买jobs的商品
				"""
				{
					"order_id":"004",
					"pay_type":"微信支付",
					"products":[{
						"name":"bill商品11",
						"count":5
					}],
					"integral_money":25.00,
					"integral":50.00,
					"weizoom_card":[{
							"card_name":"0000001",
							"card_pass":"1234567"
							}]
				}
				"""

		#待支付-005-本店(bill商品1)
			When lily访问bill的webapp
				"""
				{
					"order_id":"005",
					"pay_type":"微信支付",
					"products":[{
						"name":"bill商品1",
						"count":1
					}]
				}
				"""

	#jack购买商品(nokia自营平台,bill商品2、tom商品1)
		When jack关注nokia的公众号
		When jack访问nokia的webapp
		When jack购买nokia的商品
			"""
			{
				"order_id":"006",
				"pay_type":"微信支付",
				"products":[{
					"name":"bill商品2",
					"count":2
				},{
					"name":"tom商品1",
					"count":1
				}]
			}
			"""
		When jack使用支付方式'微信支付'进行支付订单'006'

Scenario:1 商家后台查看订单列表,包含自营平台同步过来的订单
	Given bill登录系统
	Then bill可以看到订单列表
		"""
		[{
			"order_no":"006-bill商家",
			"sources": "商城",
			"status": "待发货",
			"buyer":"jack",
			"final_price":38.00,
			"save_money":"",
			"methods_of_payment": "微信支付",
			"actions": ["发货"],
			"products":
				[{
					"name":"bill商品2",
					"price":"",
					"count":2
				}]
			},{
				"order_no":"005",
				"sources": "本店",
				"buyer":"lily",
				"status": "待支付",
				"final_price": 20.00,
				"postage": 10.0,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"actions": ["支付","修改价格","取消订单"],
				"products":
					[{
						"name":"bill商品1",
						"price":10.0,
						"count":1
					}]
			},{
				"order_no":"004",
				"sources": "商城",
				"buyer":"lily",
				"status": "待发货",
				"final_price":45.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"actions": ["发货"],
				"products":
					[{
						"name":"bill商品1",
						"price":"",
						"count":5
					}]
			},{
				"order_no":"003-bill商家",
				"sources": "商城",
				"buyer":"lily",
				"status": "待发货",
				"final_price":28.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"actions": ["发货"],
				"products":
					[{
						"name":"bill商品1",
						"price":"",
						"count":1
					},{
						"name":"bill商品2",
						"price":"",
						"count":1
					}]
			},{
				"order_no":"002",
				"sources": "商城",
				"buyer":"lily",
				"status": "待发货",
				"final_price":28.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"actions": ["发货"],
				"products":
					[{
						"name":"bill商品1",
						"price":"",
						"count":1
					},{
						"name":"bill商品2",
						"price":"",
						"count":1
					}]
		}]
		"""

	#校验'待发货'和'已发货'状态订单的操作列信息
		#商家bill对自营平台同步过来的订单进行发货-需要物流
		When bill对订单进行发货
			"""
			{
				"order_no": "006-bill商家",
				"logistics": "申通快递",
				"number": "1122006",
				"shipper": "bill"
			}
			"""
		#商家bill对自营平台同步过来的订单进行发货-不需要物流
		When bill对订单进行发货
			"""
			{
				"order_no": "004",
				"logistics":"off",
				"shipper": ""
			}
			"""
		Then bill可以看到订单列表
			"""
			[{
				"order_no":"006-bill商家",
				"sources": "商城",
				"status": "已发货",
				"buyer":"jack",
				"final_price":38.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"logistics": "申通快递",
				"number": "1122006",
				"shipper": "bill",
				"actions": ["标记完成","修改物流"],
				"products":
					[{
						"name":"bill商品2",
						"price":"",
						"count":2
					}]
				},{
					"order_no":"005",
					"sources": "本店",
					"buyer":"lily",
					"status": "待支付",
					"final_price": 20.00,
					"postage": 10.0,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["支付","修改价格","取消订单"],
					"products":
						[{
							"name":"bill商品1",
							"price":10.0,
							"count":1
						}]
				},{
					"order_no":"004",
					"sources": "商城",
					"buyer":"lily",
					"status": "已发货",
					"final_price":45.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["标记完成"],
					"products":
						[{
							"name":"bill商品1",
							"price":"",
							"count":5
						}]
				},{
					"order_no":"003-bill商家",
					"sources": "商城",
					"buyer":"lily",
					"status": "待发货",
					"final_price":28.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["发货"],
					"products":
						[{
							"name":"bill商品1",
							"price":"",
							"count":1
						},{
							"name":"bill商品2",
							"price":"",
							"count":1
						}]
				},{
					"order_no":"002",
					"sources": "商城",
					"buyer":"lily",
					"status": "待发货",
					"final_price":28.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["发货"],
					"products":
						[{
							"name":"bill商品1",
							"price":"",
							"count":1
						},{
							"name":"bill商品2",
							"price":"",
							"count":1
						}]
			}]
			"""

	#校验'已完成'状态订单的操作列信息
		When bill'完成'订单'006-bill商家'
		When bill'完成'订单'004'
		Then bill可以看到订单列表
			"""
			[{
				"order_no":"006-bill商家",
				"sources": "商城",
				"status": "已完成",
				"buyer":"jack",
				"final_price":38.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"logistics": "申通快递",
				"number": "1122006",
				"shipper": "bill",
				"actions": [],
				"products":
					[{
						"name":"bill商品2",
						"price":"",
						"count":2
					}]
				},{
					"order_no":"005",
					"sources": "本店",
					"buyer":"lily",
					"status": "待支付",
					"final_price": 20.00,
					"postage": 10.0,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["支付","修改价格","取消订单"],
					"products":
						[{
							"name":"bill商品1",
							"price":10.0,
							"count":1
						}]
				},{
					"order_no":"004",
					"sources": "商城",
					"buyer":"lily",
					"status": "已完成",
					"final_price":45.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": [],
					"products":
						[{
							"name":"bill商品1",
							"price":"",
							"count":5
						}]
				},{
					"order_no":"003-bill商家",
					"sources": "商城",
					"buyer":"lily",
					"status": "待发货",
					"final_price":28.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["发货"],
					"products":
						[{
							"name":"bill商品1",
							"price":"",
							"count":1
						},{
							"name":"bill商品2",
							"price":"",
							"count":1
						}]
				},{
					"order_no":"002",
					"sources": "商城",
					"buyer":"lily",
					"status": "待发货",
					"final_price":28.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["发货"],
					"products":
						[{
							"name":"bill商品1",
							"price":"",
							"count":1
						},{
							"name":"bill商品2",
							"price":"",
							"count":1
						}]
			}]
			"""

Scenario:2 自营平台进行订单相关操作后,查看对应商家后台订单列表的变化
	Given jobs登录系统
	Then jobs可以看到订单列表
		"""
		[{
				"order_no":"004",
				"buyer":"lily",
				"status": "待发货",
				"final_price":0.00,
				"integral_money":25.00,
				"postage":10.0,
				"save_money":25.00,
				"methods_of_payment": "优惠抵扣",
				"actions": ["发货",取消订单"],
				"products":
					[{
						"name":"bill商品11",
						"price":10.0,
						"count":5
					}]
			},{
				"order_no":"003",
				"buyer":"lily",
				"status": "待发货",
				"final_price":60.00,
				"save_money":"",
				"postage":20.0,
				"methods_of_payment": "货到付款",
				"actions": ["取消订单"],
				"products":
					[{
						"name":"bill商品11",
						"price":10.0,
						"count":1,
						"supplier": "bill商家",
						"status": "待发货",
						"actions": ["发货"]
					},{
						"name":"bill商品2",
						"price":20.0,
						"count":1,
						"supplier": "bill商家",
						"status": "待发货",
						"actions": ["发货"]
					},{
						"name":"tom商品1",
						"price":10.0,
						"count":1,
						"supplier": "tom商家",
						"status": "待发货",
						"actions": ["发货"]
					}]
			},{
				"order_no":"002",
				"buyer":"lily",
				"status": "待发货",
				"final_price":35.00,
				"postage":10.0,
				"save_money":5.00,
				"coupon_money":5.00,
				"methods_of_payment": "微信支付",
				"actions": ["发货","申请退款"],
				"products":
					[{
						"name":"bill商品11",
						"price":10.0,
						"count":1,
						"supplier": "bill商家"
					},{
						"name":"bill商品2",
						"price":20.0,
						"count":1,
						"supplier": "bill商家"
					}]
		}]
		"""
	#自营平台jobs进行'发货'操作
		When jobs对订单进行发货
			"""
			{
				"order_no": "003-bill商家",
				"logistics": "申通快递",
				"number": "1122006",
				"shipper": "jobs"
			}
			"""
		Given bill登录系统
		Then bill可以看到订单列表
			"""
			[{
				"order_no":"006-bill商家",
				"sources": "商城",
				"status": "待发货",
				"buyer":"jack",
				"final_price":38.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"actions": ["发货"],
				"products":
					[{
						"name":"bill商品2",
						"price":"",
						"count":2
					}]
				},{
					"order_no":"005",
					"sources": "本店",
					"buyer":"lily",
					"status": "待支付",
					"final_price": 20.00,
					"postage": 10.0,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["支付","修改价格","取消订单"],
					"products":
						[{
							"name":"bill商品1",
							"price":10.0,
							"count":1
						}]
				},{
					"order_no":"004",
					"sources": "商城",
					"buyer":"lily",
					"status": "待发货",
					"final_price":45.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["发货"],
					"products":
						[{
							"name":"bill商品1",
							"price":"",
							"count":5
						}]
				},{
					"order_no":"003-bill商家",
					"sources": "商城",
					"buyer":"lily",
					"status": "已发货",
					"final_price":28.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"logistics": "申通快递",
					"number": "1122006",
					"shipper": "jobs",
					"actions": ["标记完成","修改物流"],
					"products":
						[{
							"name":"bill商品1",
							"price":"",
							"count":1
						},{
							"name":"bill商品2",
							"price":"",
							"count":1
						}]
				},{
					"order_no":"002",
					"sources": "商城",
					"buyer":"lily",
					"status": "待发货",
					"final_price":28.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["发货"],
					"products":
						[{
							"name":"bill商品1",
							"price":"",
							"count":1
						},{
							"name":"bill商品2",
							"price":"",
							"count":1
						}]
			}]
			"""

	#自营平台jobs进行'标记完成'操作
		When jobs'完成'订单'003-bill商家'
		Given bill登录系统
		Then bill可以看到订单列表
			"""
			[{
				"order_no":"006-bill商家",
				"sources": "商城",
				"status": "待发货",
				"buyer":"jack",
				"final_price":38.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"actions": ["发货"],
				"products":
					[{
						"name":"bill商品2",
						"price":"",
						"count":2
					}]
				},{
					"order_no":"005",
					"sources": "本店",
					"buyer":"lily",
					"status": "待支付",
					"final_price": 20.00,
					"postage": 10.0,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["支付","修改价格","取消订单"],
					"products":
						[{
							"name":"bill商品1",
							"price":10.0,
							"count":1
						}]
				},{
					"order_no":"004",
					"sources": "商城",
					"buyer":"lily",
					"status": "待发货",
					"final_price":45.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["发货"],
					"products":
						[{
							"name":"bill商品1",
							"price":"",
							"count":5
						}]
				},{
					"order_no":"003-bill商家",
					"sources": "商城",
					"buyer":"lily",
					"status": "已完成",
					"final_price":28.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"logistics": "申通快递",
					"number": "1122006",
					"shipper": "jobs",
					"actions": [],
					"products":
						[{
							"name":"bill商品1",
							"price":"",
							"count":1
						},{
							"name":"bill商品2",
							"price":"",
							"count":1
						}]
				},{
					"order_no":"002",
					"sources": "商城",
					"buyer":"lily",
					"status": "待发货",
					"final_price":28.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["发货"],
					"products":
						[{
							"name":"bill商品1",
							"price":"",
							"count":1
						},{
							"name":"bill商品2",
							"price":"",
							"count":1
						}]
			}]
			"""

	#自营平台'取消订单'或'申通退款'后,查看对应商家后台订单列表的变化
		When jobs'取消'订单'004'
		When jobs'申请退款'订单'002'
		Given bill登录系统
		Then bill可以看到订单列表
			"""
			[{
				"order_no":"006-bill商家",
				"sources": "商城",
				"status": "已完成",
				"buyer":"jack",
				"final_price":38.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"logistics": "申通快递",
				"number": "1122006",
				"shipper": "bill",
				"actions": [],
				"products":
					[{
						"name":"bill商品2",
						"price":"",
						"count":2
					}]
				},{
					"order_no":"005",
					"sources": "本店",
					"buyer":"lily",
					"status": "待支付",
					"final_price": 20.00,
					"postage": 10.0,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"actions": ["支付","修改价格","取消订单"],
					"products":
						[{
							"name":"bill商品1",
							"price":10.0,
							"count":1
						}]
				},{
					"order_no":"003-bill商家",
					"sources": "商城",
					"buyer":"lily",
					"status": "已完成",
					"final_price":28.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"logistics": "申通快递",
					"number": "1122006",
					"shipper": "jobs",
					"actions": [],
					"products":
						[{
							"name":"bill商品1",
							"price":"",
							"count":1
						},{
							"name":"bill商品2",
							"price":"",
							"count":1
						}]
				
			}]
			"""

Scenario:3 商家后台查看订单详情页,自营平台同步过来的订单
	Given bill登录系统
	Then bill能获得订单'004'
		"""
		{
			"order_no":"004",
			"sources": "商城",
			"status": "待发货",
			"final_price":28.00,
			"methods_of_payment": "微信支付",
			"actions": ["发货"],
			"products":
				[{
					"name":"bill商品1",
					"price":9.0,
					"count":1
				},{
					"name":"bill商品2",
					"price":19.0,
					"count":1
				}]
		}
		"""
	And bill能获得订单'002'
		"""
		{
			"order_no":"002",
			"sources": "商城",
			"status": "待发货",
			"final_price":45.00,
			"methods_of_payment": "微信支付",
			"actions": ["发货"],
			"products":
				[{
					"name":"bill商品1",
					"price":9.0,
					"count":5
				}]
		}
		"""

