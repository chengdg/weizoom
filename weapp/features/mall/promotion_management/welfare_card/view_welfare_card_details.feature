# watcher: benchi@weizoom.com, zhangsanxiang@weizoom.com
#_author_:张三香 2016.05.20

Feature:福利卡券详情
	"""
		1、点击操作【卡券详情】跳转到对应福利卡券的卡券详情页面
		2、卡券详情页面信息
			a.查询条件
				卡券码:精确匹配
				领取人：模糊查询
				领取时间：开始时间必须小于等于结束时间
				订单号：精确匹配
				状态：精确匹配（全部、未领取、已领取和已过期）
			b.操作按钮：查询、重置、导出所有
			c.列表字段
				卡券码:卡的号码
				创建时间:卡的创建时间，如果是后补充的码库则显示码库补充时的时间
				有效期：显示卡的有效期
				状态：未领取、已领取、已过期
				领取时间：用户个人中心得到卡的时间
				领取人：下单的用户名称
				订单号：链接显示，点击跳转到对应的订单详情页
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
				"id":"0000003",
				"password":"3234567",
				"status":"未使用",
				"price":10.00
			},{
				"id":"0000004",
				"password":"4234567",
				"status":"未激活",
				"price":10.00
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
			"card_info":
				{
					"card_type":"微众卡",
					"card_stocks":3,
					"cards":
						[{
							"id":"0000001",
							"password":"1234567"
						},{
							"id":"0000002",
							"password":"2234567"
						},{
							"id":"0000003",
							"password":"3234567"
						}]
				},
			"creat_time":"今天"
		}]
		"""
	When bill关注jobs的公众号
	When tom关注jobs的公众号

@welfare_card @weizoom
Scenario:1 查看卡券详情
	Given jobs登录系统
	Then jobs获得福利卡券活动列表
		"""
		[{
			"activity_name":"10元通用卡",
			"product":{
				"name":"微众虚拟商品1",
				"bar_code":"112233"
			},
			"card_stocks":3,
			"card_sales":0,
			"create_time":"今天",
			"actions":["卡券详情","编辑","结束"]
		}]
		"""
	When jobs访问福利卡券活动'10元通用卡'的卡券详情
	Then jobs获得福利卡券活动'10元通用卡'的卡券详情列表
		"""
		[{
			"card_id":"000001",
			"create_time":"今天",
			"start_date":"今天",
			"end_date":"30天后",
			"status":"未领取",
			"get_time":"",
			"member":"",
			"order_no":""
		},{
			"card_id":"000002",
			"create_time":"今天",
			"start_date":"今天",
			"end_date":"30天后",
			"status":"未领取",
			"get_time":"",
			"member":"",
			"order_no":""
		},{
			"card_id":"000003",
			"create_time":"今天",
			"start_date":"今天",
			"end_date":"30天后",
			"status":"未领取",
			"get_time":"",
			"member":"",
			"order_no":""
		}]
		"""
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"order_id": "001",
			"date":"今天",
			"products": [{
				"name": "微众虚拟商品1",
				"count": 1
			}],
			"pay_type":"微信支付",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
	When bill使用支付方式'微信支付'进行支付订单'001'
	Given jobs登录系统
	When jobs自动发放卡券给订单'001'
		"""
		[{
			"id":"0000001",
			"password":"1234567"
		}]
		"""
	Then jobs获得福利卡券活动列表
		"""
		[{
			"activity_name":"10元通用卡",
			"product":{
				"name":"微众虚拟商品1",
				"bar_code":"112233"
			},
			"card_stocks":2,
			"card_sales":1,
			"create_time":"今天",
			"actions":["卡券详情","编辑","结束"]
		}]
		"""
	When jobs访问福利卡券活动'10元通用卡'的卡券详情
	Then jobs获得福利卡券活动'10元通用卡'的卡券详情列表
		"""
		[{
			"card_id":"000001",
			"create_time":"今天",
			"start_date":"今天",
			"end_date":"30天后",
			"status":"已领取",
			"get_time":"今天",
			"member":"bill",
			"order_no":"001"
		},{
			"card_id":"000002",
			"create_time":"今天",
			"start_date":"今天",
			"end_date":"30天后",
			"status":"未领取",
			"get_time":"",
			"member":"",
			"order_no":""
		},{
			"card_id":"000003",
			"create_time":"今天",
			"start_date":"今天",
			"end_date":"30天后",
			"status":"未领取",
			"get_time":"",
			"member":"",
			"order_no":""
		}]
		"""

@welfare_card @weizoom
Scenario:2 卡券详情列表的查询
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"order_id": "001",
			"date":"今天",
			"products": [{
				"name": "微众虚拟商品1",
				"count": 1
			}],
			"pay_type":"微信支付",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
	When bill使用支付方式'微信支付'进行支付订单'001'
	Given jobs登录系统
	When jobs自动发放卡券给订单'001'
		"""
		[{
			"id":"0000001",
			"password":"1234567"
		}]
		"""
	When tom访问jobs的webapp
	And tom购买jobs的商品
		"""
		{
			"order_id": "002",
			"date":"今天",
			"products": [{
				"name": "微众虚拟商品1",
				"count": 1
			}],
			"pay_type":"货到付款",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
	Given jobs登录系统
	When jobs自动发放卡券给订单'002'
		"""
		[{
			"id":"0000002",
			"password":"2234567"
		}]
		"""
	When jobs访问福利卡券活动'10元通用卡'的卡券详情
	Then jobs获得福利卡券活动'10元通用卡'的卡券详情列表
		"""
		[{
			"card_id":"000001",
			"create_time":"今天",
			"start_date":"今天",
			"end_date":"30天后",
			"status":"已领取",
			"get_time":"今天",
			"member":"bill",
			"order_no":"001"
		},{
			"card_id":"000002",
			"create_time":"今天",
			"start_date":"今天",
			"end_date":"30天后",
			"status":"已领取",
			"get_time":"今天",
			"member":"tom",
			"order_no":"002"
		},{
			"card_id":"000003",
			"create_time":"今天",
			"start_date":"今天",
			"end_date":"30天后",
			"status":"未领取",
			"get_time":"",
			"member":"",
			"order_no":""
		}]
		"""

	#按照'卡券码'进行查询
		When jobs访问福利卡券活动'10元通用卡'的卡券详情
		And jobs设置卡券详情列表查询条件
			"""
			{
				"card_id":"0000001",
				"member":"",
				"get_start_time":"",
				"get_end_time":"",
				"order_no":"",
				"status":""
			}
			"""
		Then jobs获得福利卡券活动'10元通用卡'的卡券详情列表
			"""
			[{
				"card_id":"000001"
			}]
			"""

	#按照'领取人'进行查看
		#模糊匹配
			When jobs设置卡券详情列表查询条件
				"""
				{
					"card_id":"",
					"member":"b",
					"get_start_time":"",
					"get_end_time":"",
					"order_no":"",
					"status":""
				}
				"""
			Then jobs获得福利卡券活动'10元通用卡'的卡券详情列表
				"""
				[{
					"card_id":"000001",
					"member":"bill"
				}]
				"""
		#精确匹配
			When jobs设置卡券详情列表查询条件
				"""
				{
					"card_id":"",
					"member":"bill",
					"get_start_time":"",
					"get_end_time":"",
					"order_no":"",
					"status":""
				}
				"""
			Then jobs获得福利卡券活动'10元通用卡'的卡券详情列表
				"""
				[{
					"card_id":"000001",
					"member":"bill"
				}]
				"""

	#按照'领取时间'进行查询
		#开始时间和结束时间相等
			When jobs设置卡券详情列表查询条件
				"""
				{
					"card_id":"",
					"member":"",
					"get_start_time":"今天",
					"get_end_time":"今天",
					"order_no":"",
					"status":""
				}
				"""
			Then jobs获得福利卡券活动'10元通用卡'的卡券详情列表
				"""
				[{
					"card_id":"000001"
				},{
					"card_id":"000002"
				},{
					"card_id":"000003"
				}]
				"""
		#开始时间和结束时间不等
			When jobs设置卡券详情列表查询条件
				"""
				{
					"card_id":"",
					"member":"",
					"get_start_time":"昨天",
					"get_end_time":"明天",
					"order_no":"",
					"status":""
				}
				"""
			Then jobs获得福利卡券活动'10元通用卡'的卡券详情列表
				"""
				[{
					"card_id":"000001"
				},{
					"card_id":"000002"
				},{
					"card_id":"000003"
				}]
				"""
		#查询结果为空
			When jobs设置卡券详情列表查询条件
				"""
				{
					"card_id":"",
					"member":"",
					"get_start_time":"明天",
					"get_end_time":"2天后",
					"order_no":"",
					"status":""
				}
				"""
			Then jobs获得福利卡券活动'10元通用卡'的卡券详情列表
				"""
				[]
				"""

	#按照'订单编号'进行查询
		#查询结果为空
			When jobs设置卡券详情列表查询条件
				"""
				{
					"card_id":"",
					"member":"",
					"get_start_time":"",
					"get_end_time":"",
					"order_no":"00",
					"status":""
				}
				"""
			Then jobs获得福利卡券活动'10元通用卡'的卡券详情列表
				"""
				[]
				"""
		#精确匹配
			When jobs设置卡券详情列表查询条件
				"""
				{
					"card_id":"",
					"member":"",
					"get_start_time":"",
					"get_end_time":"",
					"order_no":"002",
					"status":""
				}
				"""
			Then jobs获得福利卡券活动'10元通用卡'的卡券详情列表
				"""
				[{
					"card_id":"000002",
					"order_no":"002"
				}]
				"""

	#按照'状态'进行查询
			When jobs设置卡券详情列表查询条件
				"""
				{
					"card_id":"",
					"member":"",
					"get_start_time":"",
					"get_end_time":"",
					"order_no":"",
					"status":"未领取"
				}
				"""
			Then jobs获得福利卡券活动'10元通用卡'的卡券详情列表
				"""
				[{
					"card_id":"000003",
					"create_time":"今天",
					"start_date":"今天",
					"end_date":"30天后",
					"status":"未领取",
					"get_time":"",
					"member":"",
					"order_no":""
				}]
				"""

	#组合查询
			When jobs设置卡券详情列表查询条件
			"""
			{
				"card_id":"0000001",
				"member":"bill",
				"get_start_time":"今天",
				"get_end_time":"今天",
				"order_no":"001",
				"status":"已领取"
			}
			"""
			Then jobs获得福利卡券活动'10元通用卡'的卡券详情列表
				"""
				[{
					"card_id":"000001",
					"create_time":"今天",
					"start_date":"今天",
					"end_date":"30天后",
					"status":"已领取",
					"get_time":"今天",
					"member":"bill",
					"order_no":"001"
				}]
				"""

